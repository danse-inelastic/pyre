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


class Sphere(Primitive):


    def identify(self, visitor):
        return visitor.onSphere(self)


    def __init__(self, radius):
        self.radius = radius

        self._info.log("new {0!s}".format(self))
                 
        return


    def __str__(self):
        return "sphere: radius={0!s}".format(self.radius)


# version
__id__ = "$Id: Sphere.py,v 1.1.1.1 2006-11-27 00:09:59 aivazis Exp $"

#
# End of file
