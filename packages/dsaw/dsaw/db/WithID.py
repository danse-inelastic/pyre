# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Table import Table as base


class WithID(base):
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"
    
    def __init__(self, id = None):
        base.__init__(self)
        self.id = id




# version
__id__ = "$Id$"

# End of file 
