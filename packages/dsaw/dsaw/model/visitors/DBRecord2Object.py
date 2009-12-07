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


class DBRecord2Object(object):


    def __init__(self, object2record, db):
        # this and object2dbrecord is not symmetric since
        # orm starts with object
        self.object2dbtable = object2record.object2dbtable
        self.registry = object2record.registry
        self.db = db
        return


    def __call__(self, record):
        ret = self.registry.getObject(record)
        if not ret:
            kls = self._getObjectType(record)
            ret = self._createObject(record, kls)
            self.registry.register(ret, record)
            return ret
        self._updateObject(ret, record)
        return ret


    def findObject(self, record):
        '''find the object in the registry that corresponds to this record
        This is different from the __call__ method since
        the record might not be in the registry.
        '''
        return self.registry.findObject(record)


    def _createObject(self, record, klass):
        # try creating the instance without any arguments
        try:
            instance = klass()
        except:
            try:
                kwds = self._kwdsFromRecord(record, klass.Inventory)
                return klass(**kwds)
            except:
                raise RuntimeError, 'Cannot create new instance of type %s. Please adapt the constructor of %s class to be able to either take no argument, or arguments in the inventory'
        else:
            self._updateObject(instance, record)
            return instance


    def _createInventoryFromRecord(self, record, klass):
        kwds = self._kwdsFromRecord(record, klass.Inventory)
        inventory = klass.Inventory()
        for descriptor in klass.Inventory.getDescriptors():
            name = descriptor.name
            value = kwds[name]
            setattr(inventory, name, value)
            continue
        return inventory


    def _kwdsFromRecord(self, record, Inventory):
        db = self.db
        kwds = {}
        for descriptor in Inventory.getDescriptors():
            name = descriptor.name
            value = getattr(record, name)
            type = descriptor.type
            if type =='reference':
                if value is not None:
                    record1 = value.dereference(db)
                    value = self(record1)
            elif type == 'referenceset':
                value = [self(v) for k,v in value.dereference(db)]
            kwds[name] = value
            continue
        return kwds
    

    def _getObjectType(self, record):
        return self.object2dbtable.registry.getObject(record.__class__)


    def _updateObject(self, instance, record):
        klass = instance.__class__
        inventory = self._createInventoryFromRecord(record, klass)
        if '__restoreFromInventory__' in klass.__dict__:
            instance.__restoreFromInventory__(inventory)
            return instance
        for descriptor in klass.Inventory.getDescriptors():
            name = descriptor.name
            setattr(instance, name, getattr(inventory, name))
            continue
        return instance


# version
__id__ = "$Id$"

# End of file 
