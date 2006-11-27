#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2006  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component


class Greeter(Component):

    class Inventory(Component.Inventory):
        import pyre.inventory
        intro = pyre.inventory.str('intro',default="My name is")
        intro.meta['tip'] = 'an introductory string to introduce myself'
        
    def greet(self, friend):
        return "%s %s: %s %s!" % (self.intro, self.name, self.greeting, friend)


    def __init__(self, name):
        Component.__init__(self, name, facility='greeter')
        self.intro = ""
        self.greeting = ""
        return

    def _configure(self):
        Component._configure(self)
        self.intro = self.inventory.intro
        return


# version
__id__ = "$Id: Greeter.py,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $"

# End of file 
