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


# data objects

# create a simple data object type
class Dummy:

    def __init__(self, a):
        self.a = a


# one can add inventory after the do is declared
from dsaw.model.Inventory import Inventory as InventoryBase
class Inventory(InventoryBase):
    a = InventoryBase.descriptors.str(name='a')
Dummy.Inventory = Inventory
        


# one can also add the inventory class to the do directly

class Computation:

    def __init__(self, about):
        self.about = about
        return

    class Inventory(InventoryBase):
        about = InventoryBase.descriptors.str(name='about')


class Job:

    def __init__(self, server, computation):
        self.server = server
        self.computation = computation


    class Inventory(InventoryBase):
        server = InventoryBase.descriptors.str(name='server')
        computation = InventoryBase.descriptors.reference(name='computation', targettype=Computation)




# version
__id__ = "$Id$"

# End of file 
