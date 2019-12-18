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


from .Binary import Binary


class Greater(Binary):


    def __call__(self, candidate):
        if candidate > self.value:
            return candidate

        raise ValueError("{0!s} is not {1!s}".format(candidate, self))


    def __str__(self):
        return "(greater than {0!s})".format(self.value)


# version
__id__ = "$Id: Greater.py,v 1.1.1.1 2006-11-27 00:10:03 aivazis Exp $"

# End of file 
