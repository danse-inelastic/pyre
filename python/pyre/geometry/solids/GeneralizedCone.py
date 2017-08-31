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


class GeneralizedCone(Primitive):


    def identify(self, visitor):
        return visitor.onGeneralizedCone(self)


    def __init__(self, major, minor, scale, height):
        self.major = major
        self.minor = minor
        self.scale = scale
        self.height = height

        self._info.log("new {0!s}".format(self))
                 
        return


    def __str__(self):
        return "cone: major={0!s}, minor={1!s}, scale={2!s}, height={3!s}".format(self.major, self.minor, self.scale, self.height)


# version
__id__ = "$Id: GeneralizedCone.py,v 1.1.1.1 2006-11-27 00:09:59 aivazis Exp $"

#
# End of file
