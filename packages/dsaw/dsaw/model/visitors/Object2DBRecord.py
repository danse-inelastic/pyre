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


class Object2DBRecord(object):


    def __init__(self, object2dbtable=None, registry=None, rules=None):
        if object2dbtable is None:
            from Object2DBTable import Object2DBTable
            object2dbtable = Object2DBTable(rules=rules)
        self.object2dbtable = object2dbtable

        if not registry:
            registry = Registry()
        self.registry = registry
        
        return


    def __call__(self, obj, rules=None):
        if obj is None: return
        ret = self.registry.getRecord(obj)
        if not ret: 
            table = self._getTable(obj, rules=rules)
            ret = table()
            self.registry.register(obj, ret)
        self._updateRecord(obj, ret)
        return ret


    def _getTable(self, obj, rules=None):
        return self.object2dbtable(obj.__class__, rules=rules)


    def _updateRecord(self, obj, record):
        '''update the db record from the object'''
        inventory = obj.inventory = self._createInventory(obj)
        
        for descriptor in obj.Inventory.getDescriptors():
            name = descriptor.name
            type = descriptor.type
            value = descriptor.__get__(inventory)
            if type == 'reference':
                if value:
                    value = self(value)
            elif type == 'referenceset':
                if value:
                    for element in value:
                        elementrecord = self(element)
                continue
                
            setattr(record, name, value)
            continue

        return record


    def _createInventory(self, obj):
        '''create the inventory instance for the given object'''
        i = obj.Inventory()
        
        from dsaw.model.Inventory import establishInventoryFromObject
        return establishInventoryFromObject(i, obj)
        
        


class Registry(object):

    def __init__(self):
        self._obj2rec = {}
        self._rec2obj = {}
        self._objid2rec = {}
        return


    def getRecord(self, obj):
        if not self.isRegistered(obj): return
        objid = id(obj)
        if objid in self._objid2rec:
            return self._objid2rec[objid]
        return self._obj2rec[obj]


    def isRegistered(self, obj):
        objid = id(obj)
        if objid in self._objid2rec: return True
        try: return obj in self._obj2rec
        except TypeError, e:
            if str(e).find('unhashable')!=-1: return False
            raise
        raise RuntimeError, "should not reach here"


    def getObject(self, rec):
        return self._rec2obj.get(rec)


    def findObject(self, rec):
        # find the object give a record. this record might not
        # be registered. but we can find the corresponding object by
        # using the type and id of the record
        tablename = rec.getTableName()
        for record in self._rec2obj.iterkeys():
            if record.getTableName() == tablename and record.id == rec.id:
                return self._rec2obj[record]
            continue
        return
    

    def register(self, obj, rec):
        try:
            self._obj2rec[obj] = rec
        except TypeError, err:
            if str(err).find('unhashable') != -1:
                self._objid2rec[id(obj)] = rec
            else:
                raise
        self._rec2obj[rec] = obj
        return


    def remove(self, obj=None, rec=None):
        if obj is None and rec is None: raise RuntimeError, 'neither object nor record is supplied'
        if obj is not None and rec is not None:
            record = self.getRecord(obj)
            assert record is rec, \
                   "object %s and record %s does not match" % (obj, rec)

        if obj:
            objid = id(obj)
            if objid in self._objid2rec:
                del self._objid2rec[objid]
            else:
                del self._obj2rec[obj]
            
        if rec:
            del self._rec2obj[rec]

        return
    

# version
__id__ = "$Id$"

# End of file 
