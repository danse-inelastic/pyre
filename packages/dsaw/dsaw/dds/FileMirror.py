# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2008-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

'''
The facility to mirror a directory tree within a network
of nodes.
'''

class FileMirror:

    def __init__(self, masternode, transferfile=None,
                 readfile=None, writefile=None, makedirs=None,
                 rename=None, symlink=None, fileexists=None,
                 ):
        '''create a file mirror

        maternode: a "file mirror" must have a master node
        transferfile: the facility to transfer a file from one node to another
        rename: the facility to rename a file in one node. rename(oldpath, newpath, "server.address")
        symlink: the facility to create a symbolic link to a file in one node. symlink(oldpath, newpath, "server.address")
        readfile: the facility to read a text file. readfile("server.address:/a/b/c")
        writefile: the facility to write a text file. writefile("server.address:/a/b/c", "contents")
        makedirs: the facility to make a directory. it should be able to make the intermediate directories automatically
        fileexists: the facility to check if a file exists on a node or not. fileexists("server.address:/a/b/c")
        '''
        self.masternode = masternode
        self.nodes = [masternode]
        self._transferfile = transferfile
        self._readfile = readfile
        self._writefile = writefile
        self._makedirs = makedirs
        self._fileexists = fileexists
        self._rename = rename
        self._symlink = symlink
        return


    def setFileRegistry(self, registry):
        self._fileRegistry = registry
        return


    def addNode(self, node):
        self.nodes.append(node)
        return


    def abspath(self, path, node=None):
        if node is None: node = self.masternode
        return os.path.join(node.rootpath, path)


    def rename(self, old, new, node=None):
        if node is None: node = self.masternode
        oldpath = '%s/%s' % (node.rootpath, old)
        newpath = '%s/%s' % (node.rootpath, new)
        d = os.path.split(new)[0]
        self._makedirs(_url(node,d))
        self._rename(oldpath, newpath, node.address)
        self.forget(old, node)
        self.remember(new, node)
        return


    def copy(self, old, new, node=None):
        if node is None: node = self.masternode
        oldpath = '%s/%s' % (node.rootpath, old)
        newpath = '%s/%s' % (node.rootpath, new)
        d = os.path.split(new)[0]
        self._makedirs(_url(node,d))

        self._transferfile(_url(node,old), _url(node,new))
        
        self.remember(new, node)
        return


# it looks a bad idea to have symlink because it is hard to maintain across nodes
    def symlink(self, old, new, node=None):
        if node is None: node = self.masternode
        oldpath = '%s/%s' % (node.rootpath, old)
        newpath = '%s/%s' % (node.rootpath, new)
        d = os.path.split(new)[0]
        self._makedirs(_url(node,d))
        self._symlink(oldpath, newpath, node.address)
        self.remember(new, node)
        return


    def remember(self, path, node=None):
        '''remember that a path of a node exists

        node: the node that the path exists. None means master node
        path: the path
        '''
        if node is None: node = self.masternode
        url = _url(node,path)
        if not self._fileexists(url):
            raise RuntimeError, "url %s does not exist" % url

        self._fileRegistry.register(path, node)
        return


    def forget(self, path, node=None):
        if node is None: node = self.masternode
        url = _url(node,path)
        if self._fileexists(url):
            raise RuntimeError, "url %s still exists" % url

        self._fileRegistry.remove(path, node)
        return
        

    def isAvailable(self, path, node=None):
        if node is None: node = self.masternode
        return self._fileRegistry.check(path, node)


    def makeAvailable(self, path, node=None):
        '''make file at given path available at given node'''
        if self.isAvailable(path, node): return
        if node is None: node = self.masternode
        node1 = self.findNode(path)
        if node1 is None: raise RuntimeError, "%s is not available anywhere" % path
        debug.log( 'node1=%s, node=%s' % (node1, node) )
        self._transfer(path, node1, node)
        self.remember(path, node)
        return


    def findNode(self, path):
        '''find the node which has the file whose path is given'''

        # first loop through the nodes in the registry
        # if we find any node in the registry that works,
        # we just stop
        nodes = self._fileRegistry.getNodes(path)
        expired = []; ret = None
        for node in nodes:
            if not self._fileexists(_url(node,path)): expired.append(node)
            else: ret = node; break
            continue
        # for the expired entries in the registry, we need to remove them
        if expired:
            self._fileRegistry.remove(path, node)
        # if we find a good node, just return
        if ret: return ret

        # did not find anything, loop over all other nodes
        all = self.nodes
        nodes2 = filter(lambda n: n not in nodes, all)
        for node in nodes2:
            if self._fileexists(_url(node, path)):
                self._fileRegistry.register(path, node)
                return node
            continue

        # find nothing
        raise RuntimeError, "no node has the path %r" % path


    def _transfer(self, path, srcnode, destnode):
        debug.log('path=%s, srcnode=%s, destnode=%s' % (path, srcnode, destnode))
        d = os.path.split(path)[0]
        self._makedirs(_url(destnode,d))
        return self._transferfile(_url(srcnode,path), _url(destnode,path))

    pass # end of FileMirror




# current implementation here is to construct a string url.
# it would be more generic to just create a class Url, but
# that means all the file manipulation facilities such as
# transferfile, copyfile etc need to take url instances as inputs
def _url1(nodestr,path):
    return '%s/%s' % (nodestr, path)

def _url(node,path):
    if node.address:
        return '%s:%s/%s' % (node.address, node.rootpath, path)
    else:
        return '%s/%s' % (node.rootpath, path)


def _str(node):
    if node.address:
        return '%s:%s' % (node.address, node.rootpath)
    return node.rootpath


def _node(s):
    words = s.split(':')
    from Node import Node
    if len(words) == 1: return Node('', s)
    if len(words) == 2: return Node(words[0], words[1])
    raise ValueError, "not a node: %s" % (s,)


import os
from _debug import debug


def test(masternode, node1, transferfile, readfile, writefile, makedirs, rename, symlink, fileexists):
    #
    import os, shutil
    
    # file mirror
    file_mirror = FileMirror(
        masternode, transferfile=transferfile,
        readfile=readfile, writefile=writefile, makedirs=makedirs,
        rename=rename, symlink=symlink, fileexists=fileexists)

    # file registry
    from SimpleFileRegistry import SimpleFileRegistry
    registry = SimpleFileRegistry(file_mirror)
    file_mirror.setFileRegistry(registry)

    # clean up
    if os.path.exists(masternode.rootpath): shutil.rmtree(masternode.rootpath)

    # method "remember" on masternode
    try:
        file_mirror.remember('file1')
    except RuntimeError:
        pass
    else: raise Exception, "should have raised RuntimeError"

    # method "remember" on masternode
    os.makedirs(masternode.rootpath)
    open(os.path.join(masternode.rootpath, 'file1'), 'w').write('')

    import time
    time.sleep(0.1)
    file_mirror.remember('file1')

    # 
    file_mirror.addNode(node1)
    if os.path.exists(node1.rootpath): shutil.rmtree(node1.rootpath)
    file_mirror.makeAvailable('file1', node1)
    assert os.path.exists(os.path.join(node1.rootpath,'file1'))
    assert file_mirror.isAvailable('file1', node1)

    open(os.path.join(node1.rootpath, 'file2'), 'w').write('file2')
    file_mirror.remember('file2', node1)
    file_mirror.makeAvailable('file2')
    assert os.path.exists(os.path.join(masternode.rootpath,'file2'))
    assert file_mirror.isAvailable('file2', masternode)

    file_mirror.rename('file2', 'file3')
    assert not file_mirror.isAvailable('file2')
    assert file_mirror.isAvailable('file3')

    file_mirror.symlink('file3', 'file4')
    assert file_mirror.isAvailable('file4')
    return


def test1():
    import os
    from Node import Node
    masternode = Node( '', os.path.abspath('masternode') )
    node1 = Node( '', os.path.abspath('node1') )
    
    import os, shutil
    def transferfile(path1, path2):
        shutil.copyfile(path1, path2)
        return

    def readfile(path):
        return open(path).read()

    def writefile(path, content):
        open(path, 'w').write(content)
        return

    def makedirs(path):
        if os.path.exists(path): return
        os.makedirs(path)
        return

    def rename(path1, path2, dummy):
        os.rename(path1, path2)
        return

    def symlink(path1, path2, dummy):
        os.symlink(path1, path2)
        return
    
    test(masternode, node1, transferfile, readfile, writefile, makedirs, rename, symlink, os.path.exists)
    return


def test2():
    from Node import Node
    import os
    curdir = os.path.abspath('.')
    masternode = Node( 'localhost', os.path.join(curdir,'masternode'))
    node1 = Node( 'localhost', os.path.join(curdir,'node1') )
    
    import os, shutil
    def transferfile(path1, path2):
        cmd = 'scp %s %s' % (path1,path2)
        print 'executing %s...' % cmd
        code = os.system(cmd)
        print 'returned %s' % code
        if code: raise RuntimeError
        return

    def readfile(path):
        path = path.split(':')[1]
        return open(path).read()

    def writefile(path, content):
        path = path.split(':')[1]
        open(path, 'w').write(content)
        return

    def makedirs(path):
        path = path.split(':')[1]
        if os.path.exists(path): return
        os.makedirs(path)
        return

    def rename(path1, path2, host):
        cmd = 'ssh %s mv %s %s' % (host, path1, path2)
        print 'executing %s...' % cmd
        code = os.system(cmd)
        print 'returned %s' % code
        if code: raise RuntimeError
        return

    def symlink(path1, path2, host):
        cmd = 'ssh %s ln -s %s %s' % (host, path1, path2)
        print 'executing %s...' % cmd
        code = os.system(cmd)
        print 'returned %s' % code
        if code: raise RuntimeError
        return

    def fileexists(path):
        path = path.split(':')[1]
        return os.path.exists(path)
    
    test(masternode, node1, transferfile, readfile, writefile, makedirs, rename, symlink, fileexists)
    return


def main():
    test1()
    test2()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
