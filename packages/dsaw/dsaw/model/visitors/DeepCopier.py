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


class DeepCopier(object):

    """component to create deep copy of a data object
    """


    def __init__(
        self,
        copy_not_owned_reference=False,
        object_inventory_generator=None,
        object_factory = None,
        ):
        
        self.copy_not_owned_reference = copy_not_owned_reference
        
        if not object_inventory_generator:
            from InventoryGenerator import InventoryGenerator
            object_inventory_generator = InventoryGenerator()
        self.object_inventory_generator = object_inventory_generator

        if not object_factory:
            from ObjectFactory import ObjectFactory
            object_factory = ObjectFactory(object_inventory_generator)
        self.object_factory = object_factory
        
        return


    def __call__(self, obj):
        # build an inventory for "obj"
        inventory = self._buildInventory(obj)
        
        # create a new instance
        newinstance = self.object_factory(obj.__class__)

        # build an inventory for the new instance
        newinventory = obj.Inventory()
        
        # go thru new inventory.
        # 1. for each attribute, copy from original instance's inventory
        #    to the new instance's inventory.
        # 2. for reference(set), if it is owned, make a deep copy of the referred
        #    object. if it is not owned, need to check option "copy_not_owned_reference"
        #    put those copies into the new instance's inventory
        for descriptor in obj.Inventory.getDescriptors():
            name = descriptor.name
            value = getattr(inventory, name)
            if descriptor.type == 'reference':
                if descriptor.owned or self.copy_not_owned_reference:
                    newvalue = self(value)
                else:
                    newvalue = value
            elif descriptor.type == 'referenceset':
                if descriptor.owned or self.copy_not_owned_reference:
                    newvalue = map(self, value)
                else:
                    newvalue = value
            else:
                newvalue = value
            #
            setattr(newinventory, name, newvalue)
            continue

        # restore the object from the inventory
        from dsaw.model.Inventory import restoreObjectFromInventory
        restoreObjectFromInventory(newinstance, newinventory)
        
        return newinstance


    def _buildInventory(self, obj):
        Inventory = self._installInventoryClass(obj.__class__)
        inventory = Inventory()
        from dsaw.model.Inventory import establishInventoryFromObject
        return establishInventoryFromObject(inventory, obj)


    def _installInventoryClass(self, Object):
        '''install an Inventory class to a data object class, if necessary'''
        if 'Inventory' not in Object.__dict__:
            try:
                Inventory = self.object_inventory_generator(Object)
            except:
                import traceback
                raise RuntimeError, "object type %s not translatable. Please manually add an inventory class to it.\n%s" %  (Object.__name__, traceback.format_exc())

            Object.Inventory = Inventory
            
        return Object.Inventory
    

# version
__id__ = "$Id$"

# End of file 
