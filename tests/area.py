#!/usr/bin/env python
#


from pyre.applications.Script import Script
import pyre.units
parser = pyre.units.parser()


class AreaApp(Script):

    class Inventory(Script.Inventory):

        import pyre.inventory
        width = pyre.inventory.dimensional('width', default=parser.parse('1*cm'))
        height = pyre.inventory.dimensional('height', default=parser.parse('1*inch'))

    def main(self, *args, **kwds):
        self.area = self.width * self.height
        print('Area={}'.format(self.area))
        return

    def __init__(self):
        Script.__init__(self, 'area')
        return

    def _configure(self):
        Script._configure(self)
        self.width = self.inventory.width
        self.height = self.inventory.height
        return

def main():
    app = AreaApp()
    return app.run()

# main
if __name__ == '__main__':
    main()

# End of file 
