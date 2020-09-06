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


class OutputFile(Property):


    def __init__(self, name, mode="w", default=None, meta=None, validator=None):
        if default is None:
            import sys
            default = sys.stdout
            
        Property.__init__(self, name, "file", default, meta, validator)

        self.mode = mode

        return


    def _cast(self, value):
        if sys.version_info[:2] == (2, 7):
            if isinstance(value, basestring):
                if value == "stdout":
                    value = sys.stdout
                elif value == "stderr":
                    value = sys.stderr
                else:
                    value = open(value, self.mode)
        elif sys.version_info[0] == (3,):
            if isinstance(value, str):
                if value == "stdout":
                    value = sys.stdout
                elif value == "stderr":
                    value = sys.stderr
                else:
                    value = open(value, self.mode)
        else:
            raise RuntimeError("This version of Python is not supported. Please use Python 2.7 or Python 3.")
        
        return value


# version
__id__ = "$Id: OutputFile.py,v 1.2 2007-01-10 00:50:56 aivazis Exp $"

# End of file 
