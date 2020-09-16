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


class Array(Property):


    def __init__(self, name, default=[], converter=None, meta=None, validator=None):
        Property.__init__(self, name, "array", default, meta, validator)

        if converter is None:
            converter = float

        self.converter = converter
        
        return


    def _cast(self, text):
        from ..._2to3 import isstr
        if isstr(text):
            if text and text[0] in '[({':
                text = text[1:]
            if text and text[-1] in '])}':
                text = text[:-1]

            value = text.split(",")
        else:
            value = text

        if isinstance(value, list):
            try:
                return list(map(self.converter, value))
            except ValueError:
                pass
            
        raise TypeError(
            "property '{0!s}': could not convert '{1!s}' to an array of {2!s}s".format(self.name, text, self.converter.__name__))
    

# version
__id__ = "$Id: Array.py,v 1.1.1.1 2006-11-27 00:10:02 aivazis Exp $"

# End of file 
