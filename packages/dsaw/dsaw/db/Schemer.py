#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# Modified from pyre.db.Schemer
# 


from Column import Column
import weakref


from pyre.db.Schemer import Schemer as base

class Schemer(base):


    def __init__(cls, name, bases, dict):
        base.__init__(cls, name, bases, dict)

        # scan the class record for columns
        for name, item in cls.__dict__.iteritems():

            # disregard entries that do not derive from Column
            if not isinstance(item, Column):
                continue

            # XXX: Jiao Lin:
            # added so that the column descriptor knows
            # the table it belongs to
            item.parent_table = weakref.ref(cls)

        return


# version
__id__ = "$Id$"

# End of file 
