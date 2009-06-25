#!/usr/bin/env python

from pyre.applications.Script import Script as base

class GreetApp(base):

    class Inventory(base.Inventory):

        import pyre.inventory

        from Greeter import Greeter
        greeter = pyre.inventory.facility(name='greeter', factory=Greeter)
        name = pyre.inventory.str(name='name', default='World')
        

    def main(self):
        self.greeter.greet(self.name)
        return


    def _configure(self):
        super(GreetApp, self)._configure()
        self.name = self.inventory.name
        self.greeter = self.inventory.greeter
        return
    
    
    def __init__(self, name='greet'):
        super(GreetApp, self).__init__(name=name)
        return

    
# main
if __name__ == "__main__":
    app = GreetApp()
    app.run()
    
# End of file
