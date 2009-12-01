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

'''
convert an object type to a db table type.
'''

class Object2DBTable(object):

    rules = {
        'str': {
          'max-length': 64,
        },
        }

    def __init__(self, registry=None, rules=None, object_inventory_generator=None):
        if not registry:
            registry = Registry()
        self.registry = registry

        if not object_inventory_generator:
            from InventoryGenerator import InventoryGenerator
            object_inventory_generator = InventoryGenerator()
        self.object_inventory_generator = object_inventory_generator

        if rules: self.rules = rules
        return


    def mapped(self, object):
        return bool(self.registry.getTable(object))


    def __call__(self, object, rules=None):
        t = self.registry.getTable(object)
        if t: return t
        return self.createTable(object, rules=rules)
        

    def createTable(self, obj, rules=None):
        if 'Inventory' not in obj.__dict__:
            try:
                Inventory = self.object_inventory_generator(obj)
            except:
                import traceback
                raise RuntimeError, "object type %s not translatable. Please manually add an inventory class to it.\n%s" %  (obj.__name__, traceback.format_exc())

            obj.Inventory = Inventory
        if not rules: rules = self.rules
        else:
            r = self.rules.copy(); r.update(rules); rules = r
        
        Inventory = obj.Inventory

        cols = [self._createColumn(descriptor, rules)
                for descriptor in Inventory.getDescriptors()]
            
        # create a table class
        table = self._createTable(obj, cols, rules)

        self.registry.register(obj, table)
        return table


    def _createColumn(self, descriptor, rules):
        type = descriptor.type
        handler = '_on'+type.capitalize()
        handler = getattr(self, handler)
        return handler(descriptor, rules)


    def _createTable(self, object, cols, rules):
        tname = object.__name__.lower()
        from dsaw.db.WithID import WithID
        from dsaw.db.GloballyReferrable import GloballyReferrable
        class _(WithID, GloballyReferrable):
            name = tname

            for col in cols:
                exec '%s=col' % col.name
                continue

            try:
                del col
            except:
                pass
            
        return _


    def _onStr(self, descriptor, rules):
        if hasattr(descriptor, 'max_length'):
            length = descriptor.max_length
        else:
            length = rules['str']['max-length']
        return dsaw.db.varchar(name=descriptor.name, length=length, default=descriptor.default)


    def _onFloat(self, descriptor, rules):
        return dsaw.db.real(name=descriptor.name, default=descriptor.default)


    def _onInt(self, descriptor, rules):
        return dsaw.db.integer(name=descriptor.name, default=descriptor.default)
    

    def _onBool(self, descriptor, rules):
        return dsaw.db.boolean(name=descriptor.name, default=descriptor.default)


    def _onArray(self, descriptor, rules):
        elementtype = descriptor.elementtype
        handler = '_on%sArray' % elementtype.capitalize()
        if not handler in self.__class__.__dict__:
            raise NotImplementedError
        handler = getattr(self, handler)
        return handler(descriptor, rules)


    def _onFloatArray(self, descriptor, rules):
        return dsaw.db.doubleArray(
            name=descriptor.name, default=descriptor.default,
            shape = descriptor.shape
            )


    def _onIntArray(self, descriptor, rules):
        return dsaw.db.doubleArray(
            name=descriptor.name, default=descriptor.default,
            shape = descriptor.shape
            )


    def _onStrArray(self, descriptor, rules):
        if hasattr(descriptor, 'string_max_length'):
            length = descriptor.string_max_length
        else:
            length = rules['str']['max-length']
        return dsaw.db.varcharArray(
            name=descriptor.name, default=descriptor.default,
            shape=descriptor.shape, length=length,
            )
    

    def _onBoolArray(self, descriptor, rules):
        return dsaw.db.booleanArray(
            name=descriptor.name, default=descriptor.default,
            shape=descriptor.shape
            )
    

    def _onBoolArray(self, descriptor, rules):
        return dsaw.db.booleanArray(
            name=descriptor.name, default=descriptor.default,
            shape=descriptor.shape
            )
    

    def _onReference(self, descriptor, rules):
        targettype = descriptor.targettype
        if descriptor.isPolymorphic():
            return self._onPolymorphicReference(descriptor, rules)

        table = self(targettype)
        return dsaw.db.reference(name=descriptor.name, table=table)


    def _onPolymorphicReference(self, descriptor, rules):
        return dsaw.db.versatileReference(name=descriptor.name)


    def _onReferenceset(self, descriptor, rules):
        return dsaw.db.referenceSet(name=descriptor.name)


            
import dsaw.db



class Registry(object):

    def __init__(self):
        self._object2table = {}
        self._table2object = {}
        self._name2object = {}
        return


    def iterTables(self):
        return self._table2object.iterkeys()


    def getObjectFromName(self, name):
        return self._name2object.get(name)


    def getTable(self, object):
        return self._object2table.get(object)


    def getObject(self, table):
        return self._table2object.get(table)


    def register(self, object, table):
        self._object2table[object] = table
        self._table2object[table] = object
        self._name2object[object.__name__] = object
        return
    

# version
__id__ = "$Id$"

# End of file 
