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


from pyre.parsing.locators.Traceable import Traceable
from .Schemer import Schemer

class Table(Traceable, metaclass=Schemer):

    def __init__(self):
        Traceable.__init__(self)
        # local storage for the descriptors created by the various traits
        self._priv_columns = {}
        self._retrieveDefaults()
        return

    def getColumnValue(self, name):
        return self._priv_columns.get(name)

    def getValues(self):
        return [self.__getattribute__(name) for name in self._columnRegistry]

    def getWriteableValues(self):
        return [self.__getattribute__(name) for name in self._writeable]


    def getFormattedWriteableValues(self):
        writable = self._writeable
        values = {}
        for name, column in self._columnRegistry.items():
            if name not in writable: continue
            values[name] = column.getFormattedValue(self)
            continue
        return [values[name] for name in self._writeable]

    def getColumnNames(self):
        return list(self._columnRegistry.keys())
 
    def getNumColumns(self):
        return len(list(self._columnRegistry.keys()))

    def getWriteableColumnNames(self):
        return self._writeable

    # the low level interface
    def _getColumnValue(self, name):
        return self._priv_columns[name]

    def _getFormattedColumnValue(self, name):
        column = self._columnRegistry[name]
        return column.getFormattedValue(self)

    def _setColumnValue(self, name, value):
        self._priv_columns[name] = value
        return value

    #
    def _retrieveDefaults(self):
        for column in self._columnRegistry.values():
            value = column.__get__(self)
            column.__set__(self, value)
            continue
        return

    # column registries
    _writeable = []
    _columnRegistry = {}

 
    @classmethod
    def getTableName(cls):
        if hasattr(cls, 'pyredbtablename'):
            return cls.pyredbtablename
        try:
            name = cls.name
        except:
            name = cls.__name__.lower()
        return name


# version
__id__ = "$Id: Table.py,v 1.5 2008-04-21 03:08:46 aivazis Exp $"

# End of file 
