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
It is assumed that all tables that can be referred to have
a column "id" and it is the primary key for that table.
Also assumed is that the id column is "varchar" type.
Refer to Table.
'''

from Column import Column
from _reference import reference

class Reference(Column):


    def __init__(self, table, name=None,  backref=None, default=None, **kwds):
        '''a reference column
        - table: the table this reference refers to
        - name: name of this reference
        '''
        # length is not a valid input
        length = kwds.get('length')
        if length: raise ValueError, "'length' is not a valid keyword for 'Reference'"
        # we don't want to check for id
        #self._checkReferredTable(table)
        if name is None:
            name = table.__class__.__name__
            name = table.__name__
        Column.__init__(self, name, default, **kwds)
        # 
        self.referred_table = table
        if backref:
            from BackReference import BackReference
            br = BackReference(self)
            setattr(table, backref, br)
        # establish constraint
        try:
            tablename = table.getTableName()
        except:
            tablename = table.__class__.__name__
        self.constraints = 'REFERENCES %s (id)' % tablename

    def __get__(self, instance, cls = None):
        ret = Column.__get__(self, instance, cls = cls)
        # class variable request
        if ret is self: return self
        return self._cast( ret )

    def _checkReferredTable(self, table):
        try: table.id
        except AttributeError:
            msg = "Table %s does not have a 'id' column. Cannot create reference." % (
                table, )
            raise RuntimeError, msg
        #from pyre.db.VarChar import VarChar
        #assert isinstance(table.id, VarChar), "'id' column of table %r is not a varchar" %(
        #    table)
        return

    def _cast(self, value):
        """allowed values are: 
        1) instance of referred class (with or w/o db id set)
        2) Class itself...desired id must be set later
        """
        if not value: return None
        if isinstance( value, reference ): return value
        if isinstance( value, self.referred_table ): 
            return reference( value.id, self.referred_table )
        #value is the id of a row in the referred table
        if isinstance(value, int) or isinstance(value, long) or isinstance(value, basestring):
            return reference( value, self.referred_table )
        raise ValueError, "%s(%s)" % (type(value), value)

    def _format(self, value):
        reference = self._cast( value )
        if reference is None: return
        return reference.id

# version
__id__ = "$Id$"

# End of file 
