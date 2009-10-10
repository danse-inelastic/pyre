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


from pyre.components.Component import Component as base


class DistributedDataStore(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        dataroot = pyre.inventory.str('dataroot', default='data-store-root')

        import dsaw.components
        remoteaccess = pyre.inventory.facility(
            'remoteaccess', factory=dsaw.components.ssher)

        from SimpleDataPathMapper import SimpleDataPathMapper
        obj2path = pyre.inventory.facility('obj2path', factory=SimpleDataPathMapper)


    def __init__(self, name='dds', facility='dds'):
        super(DistributedDataStore, self).__init__(name, facility)
        return
    

    def addComputingNode(self, computingNode=None):
        return self._call('addNode', computingNode=computingNode)


    def remember(self, obj=None, filename=None, computingNode=None, files=None):
        return self._call(
            'remember', computingNode=computingNode,
            obj=obj, filename=filename, files=files)


    def forget(self, obj=None, filename=None, computingNode=None, files=None):
        return self._call(
            'forget', computingNode=computingNode,
            obj=obj, filename=filename, files=files)


    def getmtime(self, obj=None, filename=None, computingNode=None):
        path = self.abspath(obj, filename=filename, computingNode=computingNode)
        
        from dsaw.computing_server import configuration_dir, default_envvars_sh
        import os
        evsh = os.path.join(configuration_dir, default_envvars_sh)
        
        cmd = '. ~/%s; getmtime.py --path="%s"' % (evsh, path)
        failed, output, error = self.remoteaccess.execute(cmd, computingNode, '/tmp')
        
        # no output means the directory does not exist in the computingNode
        if not output: return

        mtime = eval(output)
        return mtime


    def move(self, obj1=None, filename1=None, obj2=None, filename2=None,
             computingNode=None):
        return self._call(
            'move', computingNode=computingNode,
            obj1=obj1, filename1=filename1,
            obj2=obj2, filename2=filename2)


    def copy(self, obj1=None, filename1=None, obj2=None, filename2=None,
             computingNode=None):
        return self._call(
            'copy', computingNode=computingNode,
            obj1=obj1, filename1=filename1,
            obj2=obj2, filename2=filename2)


    def symlink(self, obj1=None, filename1=None, obj2=None, filename2=None,
                computingNode=None):
        return self._call(
            'symlink', computingNode=computingNode,
            obj1=obj1, filename1=filename1,
            obj2=obj2, filename2=filename2)


    def makeAvailable(self, obj=None, files=None, filename=None, computingNode=None):
        return self._call(
            'makeAvailable', computingNode=computingNode,
            obj=obj, files=files, filename=filename)


    def isAvailable(self, obj=None, filename=None, computingNode=None):
        return self._call(
            'isAvailable', computingNode=computingNode,
            obj=obj, filename=filename)


    def path(self, obj=None, filename=None):
        return self.engine.path(obj=obj, filename=filename)


    def abspath(self, obj=None, filename=None, computingNode=None):
        return self._call(
            'abspath', computingNode=computingNode,
            obj=obj, filename=filename)
    

    def _call(self, method, computingNode=None, **kwds):
        node = _node(computingNode)
        method = getattr(self.engine, method)
        return method(node=node, **kwds)


    def _configure(self):
        base._configure(self)
        self.dataroot = self.inventory.dataroot
        self.remoteaccess = self.inventory.remoteaccess
        self.obj2path = self.inventory.obj2path
        return
    
    
    def _init(self):
        base._init(self)

        from dsaw.dds import dds, filemirror, node
        masternode = node(address='localhost', rootpath=self.dataroot)

        ddscomponent = self
        def readfile(url):
            computingNode, path = _decodeurl(url)
            if _islocal(computingNode):
                return open(path).read()
            import tempfile
            d = tempfile.mkdtemp()
            ddscomponent.remoteaccess.getfile(computingNode, path, d)
            filename = os.path.split(path)[1]
            ret = open(os.path.join(d, filename)).read()
            shutil.rmtree(d)
            return ret
            
        def writefile(url, content):
            computingNode, path = _decodeurl(url)
            if _islocal(computingNode):
                return open(path, 'w').write(content)
            import tempfile
            f = tempfile.mktemp()
            open(f, 'w').write(content)
            ddscomponent.remoteaccess.copyfile(localhost, f, computingNode, path)
            os.remove(f)
            return

        def makedirs(url):
            computingNode, path = _decodeurl(url)
            if _islocal(computingNode):
                if os.path.exists(path): return
                return os.makedirs(path)
            cmd = 'mkdir -p %s' % path
            ddscomponent.remoteaccess.execute(cmd, computingNode, '')
            return

        def rename(path1, path2, surl):
            computingNode = _decodesurl(surl)
            if _islocal(computingNode):
                try:
                    return os.rename(path1, path2)
                except Exception, e:
                    msg = 'Unable to rename path %r to %r: %s' % (path1, path2, e)
                    raise RuntimeError, msg
            cmd = 'mv %s %s' % (path1, path2)
            ddscomponent.remoteaccess.execute(cmd, computingNode, '')
            return

        def symlink(path1, path2, surl):
            computingNode = _decodesurl(surl)
            if _islocal(computingNode):
                try:
                    return os.symlink(path1, path2)
                except Exception, e:
                    msg = 'Unable to symlink path %r to %r: %s' % (path1, path2, e)
                    raise RuntimeError, msg
            cmd = 'ln -s %s %s' % (path1, path2)
            ddscomponent.remoteaccess.execute(cmd, computingNode, '')
            return

        def fileexists(url):
            computingNode, path = _decodeurl(url)
            self._debug.log('computingNode=%r,path=%r'%(_surl(computingNode),path))
            if _islocal(computingNode):
                return os.path.exists(path)
            cmd = 'ls %s' % path
            self._debug.log('cmd=%r'%cmd)
            failed, out, err = ddscomponent.remoteaccess.execute(cmd, computingNode, '', suppressException=True)
            return not failed
            
            
        def transferfile(url1, url2):
            computingNode1, path1 = _decodeurl(url1)
            computingNode2, path2 = _decodeurl(url2)
            self._debug.log('computingNode1: %s, path1: %s; computingNode2: %s, path2: %s' % (
                computingNode1, path1, computingNode2, path2))
            self._debug.log('computingNode1 is localhost?: %s' % _islocal(computingNode1))
            self._debug.log('computingNode2 is localhost?: %s' % _islocal(computingNode2))
            if _islocal(computingNode1) and _islocal(computingNode2):
                import shutil
                shutil.copy(path1, path2)
                return
            ddscomponent.remoteaccess.copyfile(computingNode1, path1, computingNode2, path2)
            return
            
        mirror = filemirror(
            masternode=masternode,
            transferfile=transferfile,
            readfile=readfile, writefile=writefile, makedirs=makedirs,
            rename=rename, symlink=symlink, fileexists=fileexists,
            )
        # file registry
        from dsaw.dds.SimpleFileRegistry import SimpleFileRegistry
        registry = SimpleFileRegistry(mirror)
        mirror.setFileRegistry(registry)

        self.masternode = masternode
        self.engine = dds(mirror, self.obj2path)

        return

    pass # end of DistributedDataStore


import os


def _islocal(computingNode):
    return computingNode.isLocalhost()


def _node(computingNode):
    import dsaw.dds as dds
    if computingNode is None: return
    if _islocal(computingNode):
        return dds.node(address='localhost', rootpath=computingNode.workdir)
    return dds.node(
        address='%s@%s(%s)' % (computingNode.username, computingNode.address, computingNode.port),
        rootpath = computingNode.workdir)

def _decodeurl(url):
    #url: username@address(port):path
    splits = url.split(':')
    if len(splits)==1:
        s, path = '', url
    elif len(splits)==2:
        s, path = splits
    else:
        raise ValueError, url
    s = _decodesurl(s)
    return s, path

def _decodesurl(s):
    #url: username@address(port)
    if s.find('(')!=-1:
        a,p = s.split('(')
        p = p.strip()
        assert p[-1]==')'
        p = p[:-1]
    else:
        a = s
        p = ''
    port = p
    if a.find('@') == -1:
        username = ''; address = a
    else:
        username,address = a.split('@')

    if address == '': address = 'localhost'

    from dsaw.ComputingNode import ComputingNode
    s = ComputingNode()
    s.username = username
    s.port = p
    s.address = address
    return s

def _surl(computingNode):
    return '%s@%s(%s)' % (computingNode.username, computingNode.address, computingNode.port)


import os


# version
__id__ = "$Id$"

# End of file 
