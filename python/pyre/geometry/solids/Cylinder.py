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

from Primitive import Primitive


class Cylinder(Primitive):


    def identify(self, visitor):
        return visitor.onCylinder(self)


    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

        self._info.log("new {0!s}".format(self))
                 
        return


    def __str__(self):
        return "cylinder: radius={0!s}, height={1!s}".format(self.radius, self.height)
    

# version
__id__ = "$Id: Cylinder.py,v 1.1.1.1 2006-11-27 00:09:59 aivazis Exp $"

#
# End of file
