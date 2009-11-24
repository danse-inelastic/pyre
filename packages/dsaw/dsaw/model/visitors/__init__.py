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

def getDataObjectClassInventory(kls, **kwds):
    if 'Inventory' in kls.__dict__: return getattr(kls, 'Inventory')
    from InventoryGenerator import InventoryGenerator
    I = InventoryGenerator(**kwds)(kls)
    kls.Inventory = I
    return I
    

# version
__id__ = "$Id$"

# End of file 
