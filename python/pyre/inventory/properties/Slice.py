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
        if sys.version_info[:2] == (2, 7):
            if isinstance(value, basestring):
                try:
                    value = pyre.util.range.sequence(value)
                except:
                    raise TypeError("property '{0!s}': could not convert '{1!s}' to a slice".format(self.name, value))
        elif sys.version_info[0] == (3,):
            if isinstance(value, str):
                try:
                    value = pyre.util.range.sequence(value)
                except:
                    raise TypeError("property '{0!s}': could not convert '{1!s}' to a slice".format(self.name, value))
        else:
            raise RuntimeError("This version of Python is not supported. Please use Python 2.7 or Python 3.")

        if isinstance(value, list):
            return value
            
        raise TypeError("property '{0!s}': could not convert '{1!s}' to a slice".format(self.name, value))
    

# version
__id__ = "$Id: Slice.py,v 1.1.1.1 2006-11-27 00:10:03 aivazis Exp $"

# End of file 
