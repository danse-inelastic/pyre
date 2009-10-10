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


# simple, file-based  file registry


from AbstractFileRegistry import AbstractFileRegistry as base
class SimpleFileRegistry(base):


    def __init__(self, filemirror):
        self._filemirror = filemirror
        self._masternode = filemirror.masternode
        self._fileexists = filemirror._fileexists
        self._readfile = filemirror._readfile
        self._writefile = filemirror._writefile
        self._makedirs = filemirror._makedirs
        return
    
    
    def register(self, path, node):
        l = self._read_availability_list(path)
        
        s = _str(node)
        if s not in l: l.append(s)
        
        self._update_availability_list(path, l)
        return


    def getNodes(self, path):
        l = self._read_availability_list(path)
        return [_node(s) for s in l]


    def remove(self, path, node):
        l = self._read_availability_list(path)
        
        s = _str(node)
        if s in l: del l[l.index(s)]
        
        self._update_availability_list(path, l)
        return
        

    def check(self, path, node):
        l = self._read_availability_list(path)
        return _str(node) in l
    

    def _read_availability_list(self, path):
        p = self._registry_path(path)
        if self._fileexists(p):
            try:
                content = self._readfile(p)
            except IOError, err:
                raise RuntimeError, "unable to read content of %s: %s" % (
                    p, err)
            return content.split('\n')
        return []
    

    def _update_availability_list(self, path, list):
        p = self._registry_path(path)
        return self._writefile(p, '\n'.join(list))


    ext = '__dds_nodelist'
    prefix = '.__dds_nodelist'
    def _registry_path(self, path):

        d, p = os.path.split(path)
        
        # the path to the registry file
        registrypath = os.path.join(d, '%s.%s.%s' % (self.prefix, p, self.ext))
        # the url
        registryurl = _url(self._masternode, registrypath)

        # check if the directory exists. if not, create it
        durl = _url(self._masternode, d)
        if not self._fileexists(durl):
            self._makedirs(durl)

        #
        return registryurl
        


from FileMirror import _str, _node, _url
import os


# version
__id__ = "$Id$"

# End of file 
