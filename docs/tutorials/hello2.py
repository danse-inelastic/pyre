#!/usr/bin/env python

from pyre.applications.Script import Script as base

class HelloApp(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        
        name = pyre.inventory.str(name='name', default='World')
        

    def main(self):
        print "Hello " + self.name + "!"
        return


    def _configure(self):
        super(HelloApp, self)._configure()
        self.name = self.inventory.name
        return
    
    
    def __init__(self, name='hello2'):
        super(HelloApp, self).__init__(name=name)
        return

    
# main
if __name__ == "__main__":
    app = HelloApp()
    app.run()
    
# End of file
