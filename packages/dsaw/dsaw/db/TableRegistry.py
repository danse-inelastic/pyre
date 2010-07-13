# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def tableRegistry( ):
    return TableRegistry()

class TableRegistry:

    'registry to map table name to table'

    def __init__(self):
        self._store = {}
        return


    def register(self, table):
        try:
            name = table.getTableName()
        except:
            name = table.__class__.__name__
        self._store[ name ] = table
        return


    def registered(self, table):
        # check if a table is already registered
        try:
            name = table.getTableName()
        except:
            name = table.__class__.__name__
        return name in self._store


    def get(self, name):
        ret = self._store.get( name )
        if ret is None:
            raise KeyError, "Table %s is not yet registered. Registered tables are %s" %(
                name, self._store.keys() )
        return ret


    def tables(self):
        return self._store.values()


    def itertables(self):
        return self._store.itervalues()


# version
__id__ = "$Id$"

# End of file 
