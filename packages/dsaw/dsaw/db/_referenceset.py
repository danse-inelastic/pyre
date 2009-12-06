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


    def count(self, db):
        return self._count_referencetable_records(db) or 0


    def dereference(self, db):
        self._establishIndexes(db)
        
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


    # access element
    def getElement(self, key=None, db=None, index=None):
        self._establishIndexes(db)

        if key is not None: return self.getElementByKey(key, db)
        if index is not None: return self.getElementByIndex(index, db)
        raise ValueError, 'must supply a way to identify the element to delete: key or index'
    

    def setElement(self, key=None, element=None, db=None, index=None):
        self._establishIndexes(db)

        if key is not None: return self.setElementByKey(key, element, db)
        if index is not None: return self.setElementByIndex(index, element, db)
        raise ValueError, 'must supply a way to identify the element to delete: key or index'
    

    def delElement(self, key=None, db=None, index=None, element=None):
        self._establishIndexes(db)

        if key is not None: return self.delElementByKey(key, db)
        if index is not None: return self.delElementByIndex(index, db)
        if element:
            return self.delete(element, db)
        raise ValueError, 'must supply a way to identify the element to delete: key, index, or element record'



    # list-like access
    def getElementByIndex(self, index, db):
        q = self._queryall(db)
        if q is None: return None
        r = q.filter_by(elementindex=index).one()
        return r.element.dereference(db)
    

    def setElementByIndex(self, index, element, db):
        'set element. this only changes pointer, does not change the old or new element'
        q = self._queryall(db)
        r = q.filter_by(elementindex=index).one()
        r.element = element
        db.updateRecord(r)
        return element


    def delElementByIndex(self, index, db):
        'delete element. this only changes pointer, does not change the element'
        q = self._queryall(db)
        r = q.filter_by(elementindex=index).one()

        # remove from the set
        refset_table = self._refsetTable()
        where = self._where(db, elementindex=index)
        db.deleteRow(refset_table, where = where)
        
        # shift left
        self._shiftIndexes(db, startindex=index+1, shift=-1)

        return r.element.dereference(db)
        

    # dict-like access
    def getElementByKey(self, key, db):
        q = self._queryall(db)
        if q is None: return None
        r = q.filter_by(elementlabel=key).one()
        return r.element.dereference(db)


    def setElementByKey(self, key, element, db):
        'set element. this only changes pointer, does not change the old or new element'
        q = self._queryall(db)
        if q:
            rs = q.filter_by(elementlabel=key).all()
            if len(rs)>1: raise RuntimeError, 'this referenceset does not behave like a dictionary'
        else:
            rs = []

        if len(rs)==0:
            self.add(element, db, name=key)
        else:
            r = rs[0]
            r.element = element
            db.updateRecord(r)
            
        return element


    def delElementByKey(self, key, db):
        'delete element. this only changes pointer, does not change the element'
        q = self._queryall(db)
        if q:
            rs = q.filter_by(elementlabel=key).all()
            if len(rs)>1: raise RuntimeError, 'this referenceset does not behave like a dictionary'
        else:
            rs = []

        if len(rs)==0:
            raise KeyError, key

        r = rs[0]

        # remove from the set
        refset_table = r.__class__
        where = self._where(db, elementkey=key)
        db.deleteRow(refset_table, where = where)
        
        # shift left
        self._shiftIndexes(db, startindex=r.elementindex+1, shift=-1)
        
        return r.element.dereference(db)


    #
    def delete(self, record, db):
        self._establishIndexes(db)

        # here, the record is a db record that this reference set
        # refers to.
        # The record itself is not removed. it should be manually removed if necessary.

        # check if container is really referred
        container_gid = self._container_gid(db)
        if not container_gid: return

        # check if element is really referred
        element_gptr = record.globalpointer
        if not element_gptr: return

        # the index of this record
        index = self._find_referencetable_record(record, db).elementindex

        # remove from the set
        refset_table = self._refsetTable()
        where = self._where(db, element=record)
        db.deleteRow( refset_table, where = where)
        
        # shift left
        self._shiftIndexes(db, startindex=index+1, shift=-1)
        return record


    def add(self, record, db, name='', key='', index=None):
        """add a record to the set.
        key: key of the new element
        name: alias of key
        index: index of new element. !!! make sure index is unique! If index is None, it will be appended to the end of the set
        """
        self._establishIndexes(db)

        if key and name:
            raise ValueError, "both name and key are supplied: name:%s, key:%s" % (name, key)
        if name: key=name

        if index is None: index = self.count(db)
        
        container = self._container(db)

        refset_table = self._refsetTable()
        row = refset_table()
        row.containerlabel = self.name
        row.container = container
        row.element = record
        row.elementlabel = key
        row.elementindex = index
        row = db.insertRow(row)

        return db.query(record.__class__).filter_by(id=record.id).one()


    def insert(self, record, before=None, after=None, db=None, name=''):
        "insert a record"
        
        self._establishIndexes(db)

        newrecord = record
        newname = name
        
        if before and after: raise RuntimeError
        ref = before or after
        if not ref: raise RuntimeError

        #
        found = self._find_referencetable_record(ref, db).elementindex
        if found is None: raise RuntimeError, 'Cannot find %s in [%s]' % (
            ref.id, ', '.join([ '%s###%s' % (r.name, r.id) for d, r in elements]),
            )

        if after: index = found + 1
        else: index = found

        # shift right
        self._shiftIndexes(db, startindex=index, shift=1)

        # add
        self.add(newrecord, db, key=newname, index=index)
        return


    # helpers
    
    #  for backward compatibilities
    def _establishIndexes(self, db):
        n = self.count(db)
        if n==0: return

        rs = self._get_referencetable_records(db)
        r0 = rs[0]

        if r0.elementindex is not None: return

        for i, r in enumerate(rs):
            r.elementindex = i
            self._update_referencetable_record(
                [('elementindex', i)], db=db, element=r.element.dereference(db))
            
        return

    
    def _shiftIndexes(self, db, startindex=None, endindex=None, shift=1):
        filter = []
        if startindex: filter.append('elementindex>=%s' % startindex)
        if endindex: filter.append('elementindex<%s' % endindex)
        filter = ' and '.join(filter)

        q = self._queryall(db)
        if filter:
            q = q.filter(filter)
        q = q.order_by('elementindex')
        
        rs = q.all()
        for r in rs:
            oldindex = r.elementindex
            newindex = oldindex + shift
            elementgid = r.element.id
            self._update_referencetable_record(
                [('elementindex', newindex)], db, elementgid=elementgid)
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


    def _queryall(self, db):
        container_gid = self._container_gid(db)
        if not container_gid: return
        refset_table = self._refsetTable()
        return db.query(refset_table).filter_by(
            containerlabel=self.name, container=container_gid)


    def _find_referencetable_record(self, record, db):
        container_gid = self._container_gid(db)
        if not container_gid: return
        refset_table = self._refsetTable()
        where = self._where(db, element=record)
        return db.query(refset_table).filter(where).one()
    #containerlabel=self.name, container=container_gid, element=record.globalpointer)\
    #       .one()


    def _where(self, db, elementindex=None, elementkey=None, element=None, elementgid=None):
        if element and elementgid is not None:
            raise ValueError, "both element and elementgid are supplied: element: %s, elementgid: %s" % (element, elementgid)
        
        container_gid = self._container_gid(db)
        w  = [
            "containerlabel='%s'" % self.name,
            "container=%s" % container_gid,
            ]
        if elementindex is not None: w.append('elementindex=%s' % elementindex)
        if elementkey is not None: w.append("elementlabel='%s'" % elementkey)
        if element is not None: w.append("element=%s" % element.globalpointer.id)
        if elementgid is not None: w.append("element=%s" % elementgid)
        return ' and '.join(w)


    def _update_referencetable_record(self, assignments, db, elementindex=None, elementkey=None, element=None, elementgid=None):
        where = self._where(
            db,
            elementindex=elementindex, elementkey=elementkey,
            element=element, elementgid=elementgid)
        db.updateRow(self._refsetTable(), assignments, where=where)
        return


    def _get_referencetable_records(self, db):
        q = self._queryall(db)
        if q is None: return
        return q.order_by('elementindex').all()


    def _count_referencetable_records(self, db):
        q = self._queryall(db)
        if q is None: return
        return q.count()


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
    elementindex = dsaw.db.integer(name = 'elementindex') 

    from VersatileReference import VersatileReference
    container = VersatileReference(name = 'container')
    element = VersatileReference(name = 'element')


import _system_tables
_system_tables.tables.register(_ReferenceSetTable)


# version
__id__ = "$Id$"

# End of file 
