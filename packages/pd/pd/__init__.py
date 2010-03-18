#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""proposed changes:
1) change _reference to ReferredEntity?
2)  

"""

from pyre.db import *


def reference(**kwds):
    from Reference import Reference
    return Reference(**kwds)


def versatileReference(**kwds):
    from VersatileReference import VersatileReference
    return VersatileReference(**kwds)


def referenceSet(**kwds):
    from ReferenceSet import ReferenceSet
    return ReferenceSet(**kwds)


def time(**kwds):
    from Time import Time
    return Time(**kwds)


from TableRegistry import tableRegistry

# End of file 
