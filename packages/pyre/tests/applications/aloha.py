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


def greeter():
    return Greeter()


from pyre.components.Component import Component


class Greeter(Component):

    class Inventory(Component.Inventory):

        import pyre.inventory

        greeting = pyre.inventory.str("greeting", default="Aloha")


    def __init__(self):
        Component.__init__(self, name="aloha", facility="greeter")
        return


    def _configure(self):
        self.greeting = self.inventory.greeting
        return


# version
__id__ = "$Id: morning.odb,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $"

# End of file 
