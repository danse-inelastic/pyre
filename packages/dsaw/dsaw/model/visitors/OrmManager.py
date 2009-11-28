# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import journal
debug = journal.debug('dsaw.model')


class OrmManager(object):

    def __init__(self, db, guid, object2record = None, record2object = None):
        if object2record is None:
            from Object2DBRecord import Object2DBRecord
            object2record = Object2DBRecord()
        self.object2record = object2record

        if record2object is None:
            from DBRecord2Object import DBRecord2Object
            record2object = DBRecord2Object(object2record, db)
        self.record2object = record2object

        self.db = db
        self.guid = guid

        # tables that are registered with db manager
        self._registered_tables = []
        return


    def registerObjectType(self, type):
        self.object2record.object2dbtable(type)
        self._registerTables()
        return


    def registerObjectTypes(self, types):
        for type in types: self.registerObjectType(type)
        return


    def save(self, object):
        if object is None: return
        record = self.object2record(object)
        self._registerTables()
        self._saveRecordRecursively(object, record)
        return


    def load(self, Object, id):
        self.registerObjectType(Object)
        Table = self.object2record.object2dbtable(Object)
        record = self.db.query(Table).filter_by(id=id).one()
        obj = self.record2object(record)
        return obj


    def destroy(self, object):
        db = self.db
        record = self.object2record(object)
        for descriptor in object.Inventory.getDescriptors():
            type = descriptor.type
            name = descriptor.name
            if type == 'reference':
                value = getattr(object.inventory, name)
                setattr(record, name, None)
                self.db.updateRecord(record)
                if descriptor.owned:
                    self.destroy(value)
            if type == 'referenceset':
                value = getattr(object.inventory, name)
                refset = getattr(record, name)
                for elem in value:
                    elemrec = self.object2record(elem)
                    # remove the associateion
                    refset.delete(elemrec, db)
                    # destroy the element
                    self.destroy(elem)
                    continue
            continue
        self.db.deleteRecord(record)
        self.object2record.registry.remove(obj=object, rec=record)
        return


    def _registerTables(self):
        db = self.db
        for t in self.object2record.object2dbtable.registry.iterTables():
            if t in self._registered_tables: continue
            db.registerTable(t)
            self._registered_tables.append(t)
            continue
        db.createAllTables()
        return


    def _getRecordFromDB(self, record):
        # an object and its corresponding record are cached in the object2record
        # registry. but this record usually is not the same as the one
        # saved in database
        # this method retrieves the record from the database
        table = record.__class__
        id = record.id
        db = self.db
        rs = db.query(table).filter_by(id=id).all()
        n = len(rs)
        if n>1: raise RuntimeError
        if n==1: return rs[0]
        return 


    def _saveRecordRecursively(self, object, record):
        db = self.db
        table = self.object2record.object2dbtable(object.__class__)
        
        # the old record in the database
        oldrecord = self._getRecordFromDB(record)

        for descriptor in object.Inventory.getDescriptors():
            type = descriptor.type
            name = descriptor.name
            if type == 'reference':
                value = getattr(object.inventory, name)
                if oldrecord:
                    # convert the new referred object to a db record (not saved yet)
                    record1 = self.object2record(value)
                    # if this referred object is actually owned, more work is needed
                    if descriptor.owned:
                        # find the old referred db record
                        oldrecord1 = getattr(oldrecord, name).dereference(db)
                        # if the old record is the same as the new record,
                        # means the reference has not pointed to a new object,
                        # and we don't need to do extra things. Otherwise,
                        # we need to delete the old record
                        if oldrecord1 is not None and (record1 is None or oldrecord1.id != record1.id):
                            # remove the association
                            setattr(oldrecord, name, None)
                            db.updateRecord(oldrecord)
                            # remove the record
                            self._removeRecordFromDB(oldrecord1)
                self.save(value)
                setattr(record, name, self.object2record(value))
            elif type == 'referenceset':
                if oldrecord and descriptor.owned:
                    ref = getattr(oldrecord, name)
                    for k,v in ref.dereference(db):
                        # remove item from the refset.
                        # must do this otherwise the record cannot be removed
                        ref.delete(v, db)
                        # remove the record
                        self._removeRecordFromDB(v)
                value = getattr(object.inventory, name)
                for elem in value:
                    self.save(elem)
                
            continue
        # debug.log('object: %s, %s; record: %s, %s' % (
        #   id(object), object, id(record), record.id))
        
        if not record.id:
            record.id = self.guid()
            db.insertRow(record)
        else:
            db.updateRecord(record)

        for descriptor in object.Inventory.getDescriptors():
            type = descriptor.type
            if type == 'referenceset':
                # need to establish associations after the record is inserted
                name = descriptor.name
                value = getattr(object.inventory, name)
                refset = getattr(self.object2record(object), name)
                for elem in value:
                    record = self.object2record(elem)
                    refset.add(record, db)
                    continue
        return


    def _removeRecordFromDB(self, record):
        '''remove a record (recursively) from the data base
        This record must have been saved to db using a orm manager.
        Also remove its trace in the registry managed by this orm manager.
        '''
        # clean up the object-record registry 
        registry = self.object2record.registry
        obj = registry.findObject(record)
        if obj:
            registry.remove(obj=obj, rec=registry.getRecord(obj))
        # also need to clean up the database side
        # this can be done by load the object from the db
        # and then destroy it
        obj = self.load(obj.__class__, id=record.id)
        self.destroy(obj)
        return



# version
__id__ = "$Id$"

# End of file 
