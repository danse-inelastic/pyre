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

import sys

import pyre.util.range
from pyre.inventory.Property import Property


class Slice(Property):


    def __init__(self, name, default=[], meta=None, validator=None):
        Property.__init__(self, name, "slice", default, meta, validator)
        return


    def _cast(self, value):
        from ..._2to3 import isstr
        if isstr(value):
            try:
                value = pyre.util.range.sequence(value)
            except:
                raise TypeError("property '{0!s}': could not convert '{1!s}' to a slice".format(self.name, value))

        if isinstance(value, list):
            return value
            
        raise TypeError("property '{0!s}': could not convert '{1!s}' to a slice".format(self.name, value))
    

# version
__id__ = "$Id: Slice.py,v 1.1.1.1 2006-11-27 00:10:03 aivazis Exp $"

# End of file 
