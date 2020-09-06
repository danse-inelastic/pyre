#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


class Inspector(object):


    def onCharacterDevice(self, node):
        raise NotImplementedError(
            "class '{0!s}' must override 'onCharacterDevice'".format(self.__class__.__name__))


    def onBlockDevice(self, node):
        raise NotImplementedError(
            "class '{0!s}' must override 'onBlockDevice'".format(self.__class__.__name__))


    def onDirectory(self, node):
        raise NotImplementedError(
            "class '{0!s}' must override 'onDirectory'".format(self.__class__.__name__))


    def onFile(self, node):
        raise NotImplementedError(
            "class '{0!s}' must override 'onFile'".format(self.__class__.__name__))


    def onLink(self, node):
        raise NotImplementedError(
            "class '{0!s}' must override 'onLink'".format(self.__class__.__name__))


    def onNamedPipe(self, node):
        raise NotImplementedError(
            "class '{0!s}' must override 'onNamedPipe'".format(self.__class__.__name__))


    def onSocket(self, node):
        raise NotImplementedError(
            "class '{0!s}' must override 'onSocket'".format(self.__class__.__name__))


# version
__id__ = "$Id: Inspector.py,v 1.1.1.1 2006-11-27 00:09:56 aivazis Exp $"

#  End of file 
