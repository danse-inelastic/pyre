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
warning = journal.warning('dsaw.Inventory')
warning.deactivate()

from pyre.inventory.Facility import Facility
from pyre.inventory.Inventory import Inventory as base

class Inventory(base):

    import descriptors
    d = descriptors
    v = descriptors.validators

    def __init__(self, name=None):
        super(Inventory, self).__init__(name)

    # help methods for visitors. not for users to use
    @classmethod
    def getDescriptors(cls):
        # return a list of descriptors

        # don't want to deal with descriptor with charactor '-'
        # also don't want to deal with facility 
        candidates = cls._traitRegistry.values()
        ret = []
        for c in candidates:
            if c.name.find('-')!=-1:
                warning.log('descriptor name contains "-": %s. skip' % c.name)
                continue
            if isinstance(c, Facility):
                warning.log('descriptor is a facility: %s. skip' % c.name)
                continue
            ret.append(c)
        return ret


    @classmethod
    def getDescriptor(cls, name):
        return cls._traitRegistry.get(name)
    

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
        value = getattr(obj, name)
#        try:
#            value = getattr(obj, name)
#        except:
#            value = None
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
