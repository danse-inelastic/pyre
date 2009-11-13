# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.db.Table import Table as base

class Table(base):

    from Schemer import Schemer
    __metaclass__ = Schemer
    
    @classmethod
    def getTableName(cls):
        try:
            name = cls.name
        except:
            name = cls.__name__.lower()
        return name


# version
__id__ = "$Id$"

# End of file 
