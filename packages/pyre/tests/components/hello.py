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


from pyre.applications.Script import Script


class HelloApp(Script):


    class Inventory(Script.Inventory):

        import greeters
        import pyre.inventory

        name = pyre.inventory.str('name', default='world')
        name.meta['tip'] = 'the entity to greet'


        greeter1 = pyre.inventory.facility(
            name="greeter1",
            family="greeter",
            factory=greeters.hello, args=["default1"])
        greeter1.meta['tip'] = 'the component responsible for generating the greeting'

        greeter2 = pyre.inventory.facility(
            name="greeter2",
            family="greeter",
            factory=greeters.hello, args=["default2"])
        greeter2.meta['tip'] = 'another component responsible for generating a greeting'


    def main(self, *args, **kwds):
        print self.greeter1.greet(self.friend)
        print self.greeter2.greet(self.friend)
        return


    def __init__(self):
        Script.__init__(self, 'hello')
        self.friend = ''
        self.greeter1 = None
        self.greeter2 = None
        return


    def _configure(self):
        Script._configure(self)
        self.friend = self.inventory.name
        self.greeter1 = self.inventory.greeter1
        self.greeter2 = self.inventory.greeter2
        return




# main
if __name__ == '__main__':
    app = HelloApp()
    app.run()


# version
__id__ = "$Id: hello.py,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $"

# End of file 
