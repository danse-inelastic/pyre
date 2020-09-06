#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from .Ternary import Ternary


class Range(Ternary):


    def __call__(self, candidate):
        if candidate >= self.v1 and candidate < self.v2:
            return candidate

        raise ValueError("{0!s} is not {1!s}".format(candidate, self))


    def __str__(self):
        return "(in the range [{0!s}, {1!s}])".format(self.v1, self.v2)


# version
__id__ = "$Id: Range.py,v 1.1.1.1 2006-11-27 00:10:03 aivazis Exp $"

# End of file 
