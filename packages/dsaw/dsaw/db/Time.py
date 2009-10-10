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


from Column import Column


class Time(Column):


    def type(self):
        if not self.tz:
            return "time without time zone"
        return "time"


    def __init__(self, name, tz=True, **kwds):
        Column.__init__(self, name, **kwds)
        self.tz = tz
        return


    def __get__(self, instance, cls=None):
        ret = Column.__get__(self, instance, cls = cls)
        if ret is None:
            return self._getDefaultValue()
        return self._cast(ret)


    def _cast(self, value):
        format = '%a %b %d %H:%M:%S %Y'
        if isinstance(value, basestring):
            t =calendar.timegm(time.strptime(value, format))
        elif isinstance(value, time.struct_time):
            t =calendar.timegm(value)
        elif isinstance(value, float) or isinstance(value, int):
            t =value
        elif isinstance(value, datetime.datetime):
            return value
        else:
            raise ValueError, '%s(%s)' % (value.__class__, value)
        return datetime.datetime(*time.gmtime(t)[:6])


    def _format(self, value):
        if not value:
            value = self._getDefaultValue()
        return value
        return datetime.datetime(*time.gmtime(value)[:6])
        return time.asctime(time.gmtime(value))


    def _getDefaultValue(self):
        return datetime.datetime.now()
    

import time, calendar, datetime

# version
__id__ = "$Id: Time.py,v 1.1.1.1 2006-11-27 00:09:55 aivazis Exp $"

# End of file 
