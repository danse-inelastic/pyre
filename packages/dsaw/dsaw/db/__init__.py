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


from pyre.db import *

def connect(**kwds):
    from DBManager import DBManager
    return DBManager(**kwds)


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


# version
__id__ = "$Id$"

# End of file 
