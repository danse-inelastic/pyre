#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class reference:

    separator = '###'

    def __init__(self, id, table):
        self.table = table
        self.id = id
        return


    def dereference(self, db):
        return db.dereference(self)


    def __str__(self):
        table = self.table
        if not isinstance(table, basestring):
            table = table.name
        return '%s%s%s' % (table, self.separator, self.id)


    def __eq__(self, rhs):
        if not rhs: return False
        return self.table == rhs.table and self.id == rhs.id
    


# version
__id__ = "$Id$"

# End of file 
