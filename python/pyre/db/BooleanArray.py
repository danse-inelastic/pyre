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


# "array" types are only supported by psycopg2 (postgresql)


from .Column import Column

import numpy

class BooleanArray(Column):


    def type(self):
        return "boolean[]"


    def declaration(self):
        default = self.default
        self.default = None
        ret = Column.declaration(self)
        self.default = default
        return ret


    def __init__(self, name, shape=None, **kwds):
        Column.__init__(self, name, **kwds)
        self.shape = shape
        return


    def _cast(self, value):
        if isinstance(value, str): value = eval(value)
        if value is None: return
        value = numpy.array(value, bool)
        if self.shape:
            try:
                value.shape = self.shape
            except:
                raise ValueError(str(value))
        return value


    def _format(self, value):
        if self.shape:
            value = numpy.copy(value)
            value.shape = -1,
        value = list(value)
        s = str(value)
        s = '{' + s[1:-1] + '}'
        return s

# version
__id__ = "$Id$"

# End of file 
