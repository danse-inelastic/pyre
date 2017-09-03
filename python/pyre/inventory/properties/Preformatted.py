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
        if sys.version_info[:2] == (2, 7):
            if isinstance(value, basestring):
                return self._splitlines(value)
        elif sys.version[0] == (3,):
            if isinstance(value, str):
                return self._splitlines(value)
        else:
            raise RuntimeError("This version of Python is not supported. Please use Python 2.7 or Python 3.")

        return value


    def _splitlines(self, value):
        return value.split('\n')


# version
__id__ = "$Id: Preformatted.py,v 1.1.1.1 2006-11-27 00:10:03 aivazis Exp $"

# End of file 
