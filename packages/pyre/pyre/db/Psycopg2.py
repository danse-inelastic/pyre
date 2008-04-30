#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import psycopg2
from DBManager import DBManager


class Psycopg2(DBManager):


    # exceptions
    ProgrammingError = psycopg2.ProgrammingError


    # interface
    def connect(self, **kwds):
        return psycopg2.connect(**kwds)


# version
__id__ = "$Id: Psycopg2.py,v 1.1 2008-04-04 08:36:46 aivazis Exp $"

# End of file 
