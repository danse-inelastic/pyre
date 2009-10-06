from pyre.tests.inventory import inventory
from pyre.tests.inventory import component
from pyre.tests.inventory import trait
from pyre.tests.inventory import odb
from pyre.tests.inventory import bool
from pyre.tests.util import expand

def runTests():
    expand.test()
    inventory.test()
    component.test()
    trait.test()
    odb.test()
    bool.test()

if __name__ == "__main__":
    runTests()
