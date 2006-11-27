#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from merlin.assets.Project import Project


class Application(Project):


    def builder(self):
        from merlin.agents.CodeBuilder import CodeBuilder
        return CodeBuilder()


    def library(self, name=None):
        if name is None:
            name = self.name

        from merlin.assets.Library import Library
        lib = Library(name)

        self.assets.append(lib)

        return lib
        


    def __init__(self, name):
        Project.__init__(self, name)
        return


# version
__id__ = "$Id: Application.py,v 1.1.1.1 2006-11-27 00:09:43 aivazis Exp $"

# End of file 
