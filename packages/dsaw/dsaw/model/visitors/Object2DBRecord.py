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


    def __init__(self, object2dbtable=None, registry=None):
        if object2dbtable is None:
            from Object2DBTable import Object2DBTable
            object2dbtable = Object2DBTable()
        self.object2dbtable = object2dbtable

        if not registry:
            registry = Registry()
        self.registry = registry
        
        return


    def __call__(self, obj):
        if obj is None: return
        ret = self.registry.getRecord(obj)
        if not ret: 
            table = self._getTable(obj)
            ret = table()
            self.registry.register(obj, ret)
        self._updateRecord(obj, ret)
        return ret


    def _getTable(self, obj):
        return self.object2dbtable(obj.__class__)


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
                for element in value:
                    elementrecord = self(element)
                continue
                
            setattr(record, name, value)
            continue

        return record


    def _createInventory(self, obj):
        '''create the inventory instance for the given object'''
        i = obj.Inventory()

        # if the object has the facility to do the conversion, just do that
        if '__establishInventory__' in obj.__class__.__dict__:
            obj.__establishInventory__(i)
            return i

        # otherwise, try to introspect the inventory and assume the
        # attributes are public attributes of the object and copy the
        # values into the inventory.
        for descriptor in obj.Inventory.getDescriptors():
            name = descriptor.name
            value = getattr(obj,name)
            type = descriptor.type
            try:
                setattr(i, name, value)
            except:
                import traceback as tb
                raise RuntimeError, 'unable to set %s to %s: %s' % (
                    name, value, tb.format_exc())
            continue

        return i
        
        


class Registry(object):

    def __init__(self):
        self._obj2rec = {}
        self._rec2obj = {}


    def getRecord(self, obj):
        return self._obj2rec.get(obj)


    def getObject(self, rec):
        return self._rec2obj.get(rec)


    def findObject(self, rec):
        # find the object give a record. this record might not
        # be registered. but we can find the corresponding object by
        # using the type and id of the record
        for record in self._rec2obj.iterkeys():
            if record.name == rec.name and record.id == rec.id:
                return self._rec2obj[record]
            continue
        return
    

    def register(self, obj, rec):
        self._obj2rec[obj] = rec
        self._rec2obj[rec] = obj
        return


    def remove(self, obj=None, rec=None):
        if obj is None and rec is None: raise RuntimeError, 'neither object nor record is supplied'
        if obj is not None and rec is not None:
            assert self._obj2rec[obj] is rec, "object %s and record %s does not match" % (
                obj, rec)

        if obj:
            del self._obj2rec[obj]
            
        if rec:
            del self._rec2obj[rec]

        return
    

# version
__id__ = "$Id$"

# End of file 
