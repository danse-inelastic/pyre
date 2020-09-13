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


class Preformatted(Property):


    def __init__(self, name, default="", meta=None, validator=None):
        Property.__init__(self, name, "str", default, meta, validator)
        return


    def _cast(self, value):
        from ..._2to3 import isstr
        if isstr(value):
            return self._splitlines(value)
        return value


    def _splitlines(self, value):
        return value.split('\n')


# version
__id__ = "$Id: Preformatted.py,v 1.1.1.1 2006-11-27 00:10:03 aivazis Exp $"

# End of file 
