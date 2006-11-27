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


class Face(Entity):


    def intersects(self, other):
        return acis.facesIntersectQ(self._handle, other._handle)
        


# version
__id__ = "$Id: Face.py,v 1.1.1.1 2006-11-27 00:09:21 aivazis Exp $"

#
# End of file
