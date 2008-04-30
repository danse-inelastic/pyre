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


def main():


    from pyre.applications.Script import Script


    class ListApp(Script):


        class Inventory(Script.Inventory):

            import pyre.inventory

            items = pyre.inventory.list('items')
            items.meta['tip'] = 'the list of items'

            floats = pyre.inventory.list('floats')
            floats.meta['tip'] = 'the list of floats inventory item'


        def main(self, *args, **kwds):
            print "registry:", self.registry.render()
            print "items:", self.inventory.items
            return


        def __init__(self):
            Script.__init__(self, 'list')
            return


    app = ListApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
