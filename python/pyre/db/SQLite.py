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


import sqlite3
from .DBManager import DBManager


class SQLite(DBManager):


    # exceptions
    ProgrammingError = sqlite3.ProgrammingError
    IntegrityError = sqlite3.IntegrityError

    # interface
    def connect(self, **kwds):
        return wrapper(sqlite3.connect(**kwds))


class wrapper(object):

    def __init__(self, core):
        self._core = core
        return


    def __getattr__(self, name):
        return getattr(self._core, name)


    def autocommit(self, on_off=1):
        """autocommit(on_off=1) -> switch autocommit on (1) or off (0)"""
        if on_off:
            self._core.isolation_level = None
        else:
            self._core.isolation_level = 'DEFERRED'


    def cursor(self):
        cursor = self._core.cursor()
        return cursorWrapper(cursor)



class cursorWrapper(object):

    def __init__(self, core):
        self._core = core
        return


    def __getattr__(self, name):
        return getattr(self._core, name)


    def execute(self, sql, *args):
        sql = sql.replace('%s', '?')
        return self._core.execute(sql, *args)


# version
__id__ = "$Id$"

# End of file 
