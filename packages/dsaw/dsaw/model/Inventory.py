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

from pyre.inventory.Inventory import Inventory as base


class Inventory(base):

    import descriptors
    d = descriptors
    v = descriptors.validators


    def __init__(self, name=None):
        super(Inventory, self).__init__(name)
        return


    # help methods for visitors. not for users to use
    def getDescriptors(cls):
        # return a list of descriptors
        return cls._traitRegistry.values()
    getDescriptors = classmethod(getDescriptors)

    pass



def restoreObjectFromInventory(obj, inventory):
    if hasattr(obj, '__restoreFromInventory__'):
        obj.__restoreFromInventory__(inventory)
        return obj

    for descriptor in inventory.getDescriptors():
        name = descriptor.name
        setattr(obj, name, getattr(inventory, name))
        continue
    
    return obj


def establishInventoryFromObject(inventory, obj):
    # if the object has the facility to do the conversion, just do that
    if hasattr(obj, '__establishInventory__'):
        obj.__establishInventory__(inventory)
        return inventory

    # otherwise, try to introspect the inventory and assume the
    # attributes are public attributes of the object and copy the
    # values into the inventory.
    for descriptor in obj.Inventory.getDescriptors():
        name = descriptor.name
        value = getattr(obj,name)
        type = descriptor.type
        try:
            setattr(inventory, name, value)
        except:
            import traceback as tb
            raise RuntimeError, 'unable to set %s of type %s to %s\n%s' % (
                name, type, value, tb.format_exc())
        continue
    return inventory


# version
__id__ = "$Id$"

# End of file 
