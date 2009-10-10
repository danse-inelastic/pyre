# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# distributed data store
# This store gives a data object a unique path in the file system,
# and this unique path is a directory dedicated to this data object.
# All datasets about this data object can be store in that directory.
# If this is combined with a db, which is used to store the data object's
# meta data, then we have a complete "data store" of this data object:
#   - meta data: stored in db
#   - datasets: stored in files in the unique directory
# This unique mapping is done in "datapathmapper".
#
# futheremore, this data store is distributed. The unique directory
# actually could exist in many "nodes". Each node can be a computer, or
# a cluster.
# This "mirroring" is done by "filemirror".


class DistributedDataStore(object):

    def __init__(self, filemirror, datapathmapper):
        self.filemirror = filemirror
        self.datapathmapper = datapathmapper
        return


    def addNode(self, node):
        self.filemirror.addNode(node)
        return


    def remember(self, obj=None, filename=None, files=None, node=None):
        files = _files(obj, filename, files)
        for f in files:
            path = self.path(obj, f)
            self._remember(path, node=node)
            continue
        return

    
    def forget(self, obj=None, filename=None, node=None, files=list()):
        files = _files(obj, filename=filename, files=files)
        for f in files:
            path = self.path(obj, f)
            self._forget(path, node=node)
            continue
        return


    def move(self, obj1=None, filename1=None, obj2=None, filename2=None, node=None):
        path1 = self.path(obj1, filename1)
        path2 = self.path(obj2, filename2)
        return self._rename(path1, path2, node=node)


    def copy(self, obj1=None, filename1=None, obj2=None, filename2=None, node=None):
        path1 = self.path(obj1, filename1)
        path2 = self.path(obj2, filename2)
        return self._copy(path1, path2, node=node)


    def symlink(self, obj1=None, filename1=None, obj2=None, filename2=None, node=None):
        path1 = self.path(obj1, filename1)
        path2 = self.path(obj2, filename2)
        return self._symlink(path1, path2, node=node)


    def makeAvailable(self, obj=None, files=None, filename=None, node=None):
        files = _files(obj, filename=filename, files=files)
        for f in files:
            p = self.path(obj, f)
            self._makeAvailable(p, node=node)
            continue
        return


    def isAvailable(self, obj=None, filename=None, node=None):
        p = self.path(obj, filename)
        ret = self._isAvailable(p, node=node)
        msg = 'File %s for obj %s:%s is ' % (filename, obj.name, obj.id)
        if not ret: msg += 'not '
        msg += 'available on %s.' % (node,)
        debug.log(msg)
        return ret


    def path(self, obj=None, filename=None):
        d = self.datapathmapper(obj)
        if filename: return os.path.join(d, filename)
        return d


    def abspath(self, obj=None, filename=None, node=None):
        return self.filemirror.abspath(self.path(obj, filename), node)
    

    def _rename(self, path1, path2, node=None):
        return self.filemirror.rename(path1, path2, node=node)


    def _copy(self, path1, path2, node=None):
        return self.filemirror.copy(path1, path2, node=node)


    def _symlink(self, path1, path2, node=None):
        return self.filemirror.symlink(path1, path2, node=node)


    def _remember(self, path, node=None):
        return self.filemirror.remember(path, node=node)


    def _forget(self, path, node=None):
        return self.filemirror.forget(path, node=node)


    def _makeAvailable(self, path, node=None):
        return self.filemirror.makeAvailable(path, node=node)


    def _isAvailable(self, path, node=None):
        return self.filemirror.isAvailable(path, node=node)
 

import os
from _debug import debug



def _files(obj=None, filename=None, files=None):
    files = files or []
    if filename:
        files.append(filename)
    if not files:
        files = _default_files(obj)
    return files


def _default_files(obj):
    try:
        return obj.datafiles
    except AttributeError:
        return []




# tests
def test(masternode, node1, transferfile, readfile, writefile, makedirs, rename, symlink, fileexists):
    #
    import os, shutil
    
    # file mirror
    from FileMirror import FileMirror
    file_mirror = FileMirror(
        masternode, transferfile=transferfile,
        readfile=readfile, writefile=writefile, makedirs=makedirs,
        rename=rename, symlink=symlink, fileexists=fileexists)

    # file registry
    from SimpleFileRegistry import SimpleFileRegistry
    registry = SimpleFileRegistry(file_mirror)
    file_mirror.setFileRegistry(registry)

    # obj->path mapper
    from SimpleDataPathMapper import SimpleDataPathMapper
    mapper = SimpleDataPathMapper()
    
    # dds
    dds = DistributedDataStore(file_mirror, mapper)
    
    # clean up
    if os.path.exists(masternode.rootpath): shutil.rmtree(masternode.rootpath)

    # obj
    class user:
        id = '12345'
        name = 'users'
        
    # method "remember" on masternode
    try:
        dds.remember(user, 'file1')
    except RuntimeError:
        pass
    else: raise Exception, "should have raised RuntimeError"

    # method "remember" on masternode
    os.makedirs(masternode.rootpath)
    dir = os.path.join(masternode.rootpath, user.name, user.id)
    os.makedirs(dir)
    open(os.path.join(dir, 'file1'), 'w').write('')

    import time
    time.sleep(0.1)
    dds.remember(user, filename='file1')

    # 
    dds.filemirror.addNode(node1)
    if os.path.exists(node1.rootpath): shutil.rmtree(node1.rootpath)
    dds.makeAvailable(obj=user, filename='file1', node=node1)
    assert os.path.exists(os.path.join(node1.rootpath,user.name,user.id,'file1'))
    assert dds.isAvailable(obj=user, filename='file1', node=node1)

    open(os.path.join(node1.rootpath, user.name, user.id, 'file2'), 'w').write('file2')
    dds.remember(obj=user, filename='file2', node=node1)
    dds.makeAvailable(obj=user, filename='file2')
    assert os.path.exists(os.path.join(masternode.rootpath,user.name,user.id,'file2'))
    assert dds.isAvailable(obj=user, filename='file2', node=masternode)
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


# version
__id__ = "$Id$"

# End of file 
