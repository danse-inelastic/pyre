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

from pyre.inventory.Property import Property


class Bool(Property):


    def __init__(self, name, default=False, meta=None, validator=None):
        Property.__init__(self, name, "bool", default, meta, validator)
        return


    def _cast(self, value):
        from ..._2to3 import isstr
        if isstr(value):
            import pyre.util.bool
            return pyre.util.bool.bool(value)

        return bool(value)
    

# version
__id__ = "$Id: Bool.py,v 1.1.1.1 2006-11-27 00:10:02 aivazis Exp $"

# End of file 
