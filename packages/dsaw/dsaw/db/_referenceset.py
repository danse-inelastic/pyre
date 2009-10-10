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


# a handler to handle database requests about a referenceset for
# a particular container
class referenceset:


    def __init__(self, name, id, table):
        '''
        table, id: identify the parent record
        '''
        self.name = name
        self.table = table
        self.id = id
        return


    def dereference(self, db):
        records = self._get_referencetable_records( db )
        ret = []
        for record in records:
            key = record.elementlabel
            value = record.element.dereference( db )
            ret.append( (key, value) )
            continue
        return ret



    def clear(self, db):
        '''clear all references to my elements.
        The elements themselves are not removed. You will need to remove them manually.
        '''
        name = self.name
        container_gid = self._container_gid(db)
        if not container_gid: return
        
        where = "containerlabel='%s' and container='%s'" % (name, container_gid)
        db.deleteRow(self._refsetTable(), where = where)
        return


    def delete(self, record, db):
        # here, the record is a db record that this reference set
        # refers to.
        # The record itself is not removed. it should be manually removed if necessary.

        container_gid = self._container_gid(db)
        if not container_gid: return
        
        element_gptr = record.globalpointer
        if not element_gptr: return
        element_gid = element_gptr.id
        
        refset_table = self._refsetTable()

        where = "containerlabel='%s' and container='%s' and element='%s'" % (
            self.name, container_gid, element_gid)
        db.deleteRow( refset_table, where = where)
        return


    def add(self, record, db, name = ''):
        container = self._container(db)

        refset_table = self._refsetTable()
        row = refset_table()
        row.containerlabel = self.name
        row.container = container
        row.element = record
        row.elementlabel = name
        row = db.insertRow( row )

        return db.query(record.__class__).filter_by(id=record.id).one()


    def insert(self, record, before=None, after=None, db=None, name=''):
        "insert a record"
        
        # slow implementation
        newrecord = record
        newname = name
        
        if before and after: raise RuntimeError
        ref = before or after
        if not ref: raise RuntimeError

        #
        elements = self.dereference(db)
        found = None
        for index, (name, record) in enumerate(elements):
            if record.id == ref.id: found = index; break
            continue

        if found is None: raise RuntimeError, 'Cannot find %s in [%s]' % (
            ref.id, ', '.join([ '%s###%s' % (r.name, r.id) for d, r in elements]),
            )

        if after: index = found + 1
        else: index = found

        for name, record in elements[index:]:
            self.delete(record, db)
            continue

        self.add(newrecord, db, name=newname)

        for name, record in elements[index:]:
            self.add(record, db)
            continue
        return


    def _container_ref(self):
        return self.table, self.id


    def _container(self, db):
        container_table, container_id = self._container_ref()
        return db.query(container_table).filter_by(id=container_id).one()


    def _container_gid(self, db):
        container = self._container(db)
        gptr = container.globalpointer
        if not gptr: return
        return gptr.id


    def _get_referencetable_records(self, db):
        container_gid = self._container_gid(db)
        if not container_gid: return []
        refset_table = self._refsetTable()
        return db.query(refset_table).filter_by(
            containerlabel=self.name, container=container_gid).all()


    def _refsetTable(self):
        return _ReferenceSetTable



# The table that stores referenceset
from Table import Table
class _ReferenceSetTable(Table):

    name = "_____referenceset_____"

    import dsaw.db

    # columns
    id = dsaw.db.integer(name = 'id')
    id.constraints = 'PRIMARY KEY'

    containerlabel = dsaw.db.varchar(
        name = 'containerlabel', length = 64 )
    elementlabel = dsaw.db.varchar(
        name = "elementlabel", length = 64 )

    from VersatileReference import VersatileReference
    container = VersatileReference(name = 'container')
    element = VersatileReference(name = 'element')


import _system_tables
_system_tables.tables.register(_ReferenceSetTable)


# version
__id__ = "$Id$"

# End of file 
