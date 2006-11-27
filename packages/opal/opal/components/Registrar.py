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


from Actor import Actor


class Registrar(Actor):


    def perform(self, app, routine):
        page = app.retrievePage("registrar-%s" % routine)
        if not page:
            page = app.retrievePage("error")

        return page


    def __init__(self, name=None):
        if name is None:
            name = "registrar"

        Actor.__init__(self, name)

        return


# version
__id__ = "$Id: Registrar.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
