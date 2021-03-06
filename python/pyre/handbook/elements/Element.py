#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Element(object):


    def __init__(self, number, symbol, name, weight):
        self.name = name
        self.symbol = symbol
        self.atomicNumber = number
        self.atomicWeight = weight
        return


    def __str__(self):
        return "{0!s} ({1!s}) - atomic number: {2:d}, atomic weight: {3:g} amu".format(self.name, self.symbol, self.atomicNumber, self.atomicWeight)


# version
__id__ = "$Id: Element.py,v 1.1.1.1 2006-11-27 00:09:59 aivazis Exp $"

#
# End of file
