#!/usr/bin/env python


'''
Try the following in your command line:

  $ python property1.py 
  $ python property1.py --energy=30*meV
  $ python property1.py --energy=1.5*eV   # this will throw an exception
'''


from pyre.applications.Script import Script as base

class App(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        import pyre.units.energy
        energy = pyre.inventory.dimensional(name='energy', default=50*pyre.units.energy.meV, validator=pyre.inventory.less(1*pyre.units.energy.eV))
        

    def main(self):
        print self.inventory.energy
        return
    
    def __init__(self, name='property1'):
        super(App, self).__init__(name=name)
        return
    
# main
if __name__ == "__main__":
    app = App()
    app.run()
    
# End of file
