#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from Column import Column

class VarChar(Column):
    '''note the default length is 48'''

    def type(self):
        return "character varying (%d)" % self.length

    def __init__(self, name=None, length=48, default="", **kwds):
        if name is None:
            name = 'str'+str(id(self))
        Column.__init__(self, name, default, **kwds)
        self.length = length


# version
__id__ = "$Id: VarChar.py,v 1.2 2008-04-13 05:59:22 aivazis Exp $"

# End of file 
