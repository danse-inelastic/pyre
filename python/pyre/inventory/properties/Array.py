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
        if sys.version_info[:2] == (2,7): 
            if isinstance(text, basestring):
                if text and text[0] in '[({':
                    text = text[1:]
                if text and text[-1] in '])}':
                    text = text[:-1]
                
                value = text.split(",")
            else:
                value = text
        elif sys.version_info[0] == (3,):
            if isinstance(text, str):
                if text and text[0] in '[({':
                    text = text[1:]
                if text and text[-1] in '])}':
                    text = text[:-1]
                
                value = text.split(",")
            else:
                value = text
        else:
            raise RuntimeError("This version of Python is not supported. This software requires Python 2.7 or Python 3.")


        if isinstance(value, list):
            try:
                return map(self.converter, value)
            except ValueError:
                pass
            
        raise TypeError(
            "property '{0!s}': could not convert '{1!s}' to an array of {2!s}s".format(self.name, text, self.converter.__name__))
    

# version
__id__ = "$Id: Array.py,v 1.1.1.1 2006-11-27 00:10:02 aivazis Exp $"

# End of file 
