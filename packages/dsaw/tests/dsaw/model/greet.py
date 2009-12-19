#!/usr/bin/env python
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


from pyre.applications.Script import Script
from dsaw.model.Inventory import Inventory as DsawInventory

class GreetApp(Script):


    class Inventory(DsawInventory, Script.Inventory):

        name = DsawInventory.d.str(name='name', default='world')
        name.meta['tip'] = 'the entity to greet'


    def main(self, *args, **kwds):
        print 'Hello %s!' % self.friend
        return


    def __establishInventory__(self, inventory):
        return


    def __restoreFromInventory__(self, inventory):
        return


    def __init__(self):
        Script.__init__(self, 'greet')
        self.friend = ''
        return


    def _defaults(self):
        Script._defaults(self)
        return


    def _configure(self):
        Script._configure(self)
        self.friend = self.inventory.name
        return


    def _init(self):
        Script._init(self)
        return



def main():
    app = GreetApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
