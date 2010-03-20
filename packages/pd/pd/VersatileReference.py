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


'''
It is assumed that all tables that can be referred to are
derived from GloballyReferrable.

Compared to "Reference", VersatileReference can refer
to records in different tables. The purpose is to
have a "abstract" reference. For example, say we
have an abstract class "shape", and several subclasses
exist: block, cylinder, and sphere. Blocks, cylinders,
and spheres are in three different tables. And in another
table, we should be able to create a versatile reference
called "shape".

'''


from Column import Column


class VersatileReference(Column):


    def __init__(self, name, **kwds):
        '''a versatile reference column
        
        - name: name of this reference
        '''
        Column.__init__(self, name, **kwds)
        return


    def __get__(self, instance, cls = None):
        ret = Column.__get__(self, instance, cls = cls)
        
        # class variable request
        if ret is self: return self
        
        if not isinstance(ret, vreference):
            ret = vreference(ret)
        return ret


    def __set__(self, instance, value):
        from GloballyReferrable import GloballyReferrable
        
        if isinstance(value, int) or isinstance(value, long):
            pass
        elif not value:
            value = None
        elif isinstance(value, basestring):
            pass
        elif isinstance(value, vreference):
            value = value.id
        elif isinstance(value, GloballyReferrable):
            pass
        else:
            raise ValueError, '%s(%s)' % (type(value), value)

        debug.log('name, value=%s, %s' % (self.name, value))
        
        instance._setColumnValue(self.name, value)
        return value
    

    def _format(self, reference):
        return reference.id




from Table import Table

class global_pointer(Table):

    '''
    table of global pointers

    tables derived from GloballyReferrable have a column
    globalpointer that is bound to the id column of this table.
    '''

    name = 'global_pointers'

    import dsaw.db
    id = dsaw.db.integer(name='id')
    id.constraints = 'PRIMARY KEY'

    type = dsaw.db.varchar(name='type', length=128)

    def getPointed(self, db):
        table = db.getTable(self.type)
        return db.query(table).filter_by(globalpointer=self.id).one()
    
# import _system_tables
# _system_tables.tables.register(global_pointer)


class vreference:

    def __init__(self, id):
        # id is the id in the "global_pointers" table
        self.id = id
        return


    def dereference(self, db):
        return db.dereference(self)


    def __str__(self):
        return str(self.id)


    def __eq__(self, rhs):
        if not rhs: return False
        return self.id == rhs.id
    


import journal
debug = journal.debug('dsaw.db.VersatileReference')

# version
__id__ = "$Id$"

# End of file 
