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


from .Validator import Validator


class Or(Validator):


    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
        return


    def __call__(self, candidate):
        g1 = True
        try:
            self.op1(candidate)
        except ValueError:
            g1 = False

        g2 = True
        try:
            self.op2(candidate)
        except ValueError:
            g2 = False

        if g1 or g2:
            return candidate

        raise ValueError("{0!s} is not {1!s}".format(candidate, self))


    def __str__(self):
        return "({0!s} or {1!s})".format(self.op1, self.op2)


# version
__id__ = "$Id: Or.py,v 1.1.1.1 2006-11-27 00:10:03 aivazis Exp $"

# End of file 
