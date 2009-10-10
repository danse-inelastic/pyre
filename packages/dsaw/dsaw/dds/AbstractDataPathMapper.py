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


# abstract class
# map data object to a path
#   object -->  path
# Eg
#   job(id=3AF6C) --> jobs/3AF6C
#
# This mapper maps a data object (uniquely identified by its attribute 'id')
# to a unique path string.


class AbstractDataPathMapper(object):

    def __call__(self, obj):
        raise NotImplementedError
    

# version
__id__ = "$Id$"

# End of file 
