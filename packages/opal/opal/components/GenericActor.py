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


class GenericActor(Actor):


    def perform(self, app, routine=None):
        self.routine = routine
        page = self.createPage(app)
        return page


    def createPage(self, app):
        page = app.retrievePage(self.name)
        return page


    def __init__(self, name):
        Actor.__init__(self, name)
        return


# version
__id__ = "$Id: GenericActor.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
