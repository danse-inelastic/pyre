import pyre.inventory
from pyre.applications.Script import Script as base

class Greet(base):

    class Inventory(base.Inventory):

        greeting = pyre.inventory.str('greeting', default='hello')
        to = pyre.inventory.str('to', default='world')

    def main(self):
        msg = "{} {}".format(self.inventory.greeting, self.inventory.to)
        self._debug.log(msg)
        print(msg)
        return

if __name__ == '__main__':
    app = Greet('greet')
    app.run()
