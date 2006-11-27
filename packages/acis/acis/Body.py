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


import acis
from Entity import Entity


class Body(Entity):

    
    def intersects(self, other):
        return acis.bodiesIntersectQ(self._handle, other._handle)

        
    # debugging support
    
    def printBRep(self):
        acis.printBRep(self._handle)
        return


    def printFaces(self):
        acis.printFaces(self._handle)
        return


# version
__id__ = "$Id: Body.py,v 1.1.1.1 2006-11-27 00:09:21 aivazis Exp $"

#
# End of file
