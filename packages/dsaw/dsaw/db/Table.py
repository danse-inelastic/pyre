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
    def addColumn(cls, col):
        """add a new column to the table
        """
        # cf. pyre.db.Schemer

        #
        setattr(cls, col.name, col)
        
        # the registry
        colreg = cls._columnRegistry
        colreg[col.name] = col

        # the writables
        if not col.auto:
            writeable = cls._writeable
            writeable.append(col.name)
        return
    

# version
__id__ = "$Id$"

# End of file 
