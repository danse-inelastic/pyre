#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import dsaw.db
from dsaw.db.Table import Table
class User(Table):

    name = 'users'

    id = dsaw.db.integer(name='id')
    id.constraints = 'PRIMARY KEY'

    username = dsaw.db.varchar(name='username', length=32)


class Simulation(Table):

    name = 'simulations'

    id = dsaw.db.integer(name='id')
    id.constraints = 'PRIMARY KEY'

    creator = dsaw.db.reference(name='creator', table=User)


from dsaw.db.GloballyReferrable import GloballyReferrable, global_pointer
class Cylinder(GloballyReferrable):

    name = 'cylinders'

    id = dsaw.db.integer(name='id')
    id.constraints = 'PRIMARY KEY'


class Sample(Table):

    name = 'samples'

    id = dsaw.db.integer(name='id')
    id.constraints = 'PRIMARY KEY'

    shape = dsaw.db.versatileReference(name='shape')
    

# version
__id__ = "$Id$"

# End of file 
