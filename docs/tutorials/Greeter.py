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


from pyre.components.Component import Component


class Greeter(Component):


    class Inventory(Component.Inventory):

        import pyre.inventory

        greetings = pyre.inventory.str('greetings', default='Hello')


    def greet(self, name):
        print self.greetings + ' ' + name + '!'
        return


    def __init__(self, name='greeter'):
        Component.__init__(self, name, facility='greeter')
        return


    def _configure(self):
        super(Greeter, self)._configure()
        self.greetings = self.inventory.greetings
        return


# version
__id__ = "$Id$"

# End of file 
