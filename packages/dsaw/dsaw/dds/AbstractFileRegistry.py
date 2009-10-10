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


# abstract class of file registry
# a file registry is used by a file_mirror to track the availability
# of a file in a node of the mirror


class AbstractFileRegistry(object):


    def getNodes(self, path):
        '''get the list of nodes in which path exists'''
        raise NotImplementedError
    

    def register(self, path, node):
        '''declare that the given path exists in the given node
        It does not check whether this node:path url really exists.
        '''
        raise NotImplementedError


    def remove(self, path, node):
        '''declare that the given path does not exist in the given node.
        It does not check whether this node:path url really exists or not.
        '''
        raise NotImplementedError


    def check(self, path, node):
        """check if the given path exists in the given node
        This check only checks the information recorded in this
        registry.
        """
        raise NotImplementedError
    

# version
__id__ = "$Id$"

# End of file 
