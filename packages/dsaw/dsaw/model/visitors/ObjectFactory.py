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


class ObjectFactory(object):

    '''component to create an instance of a data object
    '''

    def __init__(self, inventoryGenerator):
        self.inventoryGenerator = inventoryGenerator
        self._defaults_store = {}
        return
    

    def __call__(self, Object):
        Inventory = self._getInventory(Object)
        defaults = self._getDefaultsForInventory(Inventory)
        try:
            instance = Object()
        except:
            try:
                return Object(**defaults)
            except:
                raise RuntimeError, 'Cannot create new instance of type %s. Please adapt the constructor of %s class to be able to either take no argument, or arguments in the inventory'
            
        inventory = Inventory()
        from dsaw.model.Inventory import restoreObjectFromInventory
        return restoreObjectFromInventory(instance, inventory)


    def _getDefaultsForInventory(self, Inventory):
        if Inventory not in self._defaults_store:
            self._defaults_store[Inventory] = self._createDefaultsFromInventory(Inventory)
        return self._defaults_store[Inventory]
    

    def _createDefaultsFromInventory(self, Inventory):
        defaults = {}
        i = Inventory()
        for descriptor in Inventory.getDescriptors():
            name = descriptor.name
            value = getattr(i, name)
            defaults[name] = value
        return defaults


    def _getInventory(self, Object):
        # has to be in the __dict__. inherited Inventory does not count
        if 'Inventory' in Object.__dict__: return Object.Inventory
        # auto generation
        Inventory = self.inventoryGenerator(Object)
        return Inventory
    

# version
__id__ = "$Id$"

# End of file 
