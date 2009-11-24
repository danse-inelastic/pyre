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


# version
__id__ = "$Id$"

# End of file 
