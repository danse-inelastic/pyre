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

from .Primitive import Primitive


class Block(Primitive):


    def identify(self, visitor):
        return visitor.onBlock(self)


    def __init__(self, diagonal):
        self.diagonal = tuple(diagonal)

        self._info.log("new {0!s}".format(self))
                 
        return


    def __str__(self):
        return "block: diagonal=({0!s}, {1!s}, {2!s})".format(*self.diagonal)


# version
__id__ = "$Id: Block.py,v 1.1.1.1 2006-11-27 00:09:58 aivazis Exp $"

#
# End of file
