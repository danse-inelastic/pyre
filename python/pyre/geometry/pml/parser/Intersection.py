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

from Binary import Binary
import pyre.geometry.operations


class Intersection(Binary):

    tag = "intersection"


    def notify(self, parent):
        if not self._b1 or not self._b2:
            raise ValueError("'{0!s}' requires exactly two children".format(self.tag))

        intersection = pyre.geometry.operations.intersect(self._b1, self._b2)
        parent.onIntersection(intersection)
        return


# version
__id__ = "$Id: Intersection.py,v 1.1.1.1 2006-11-27 00:09:57 aivazis Exp $"

# End of file
