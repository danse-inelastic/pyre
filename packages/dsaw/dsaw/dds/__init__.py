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


# distributed data store


def dds(*args, **kwds):
    from DistributedDataStore import DistributedDataStore
    return DistributedDataStore(*args, **kwds)


def filemirror(*args, **kwds):
    from FileMirror import FileMirror
    return FileMirror(*args, **kwds)


def node(*args, **kwds):
    from Node import Node
    return Node(*args, **kwds)


# version
__id__ = "$Id$"

# End of file 
