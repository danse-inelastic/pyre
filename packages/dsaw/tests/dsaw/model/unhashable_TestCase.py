#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

class Structure(list):

    def __init__(self, atoms):
        for a in atoms: self.append(a)

    # helpers for make it ormable
    def __establishInventory__(self, inventory):
        inventory.atoms = self
        return

class Atom: pass


# add inventory
from dsaw.model.Inventory import Inventory as base
class Inventory(base):

    atoms = base.descriptors.referenceSet(name='atoms', targettype=Atom, owned=1)

Structure.Inventory = Inventory



import unittest

class TestCase(unittest.TestCase):


    def test1(self):
        'data object that is unhashable'

        # create a data object instance
        atom1 = Atom(); atom2 = Atom()
        atoms = [ atom1, atom2 ]
        struct = Structure(atoms)

        # convert struct to a db record
        from dsaw.model.visitors.Object2DBRecord import Object2DBRecord
        o2r = Object2DBRecord()
        record = o2r(struct)
        
        self.orm.save(struct)
        self.structid = self.orm(struct).id

        self.orm2.registerObjectType(Atom)
        struct2 = self.orm2.load(Structure, self.structid)
        self.assertEqual(len(struct2), 2)
        for atom in struct2:
            self.assertEqual(atom.__class__, Atom)

        self.orm.destroy(struct)
        return
    
    

    def setUp(self):
        self.orm = self._ormManager()
        self.orm2 = self._ormManager()


    def tearDown(self):
        del self.orm2
        
        db = self.orm.db
        db.destroyAllTables()
        return
        

    def _dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db


    def _ormManager(self):
        from dsaw.model.visitors.OrmManager import OrmManager
        return OrmManager(self._dbManager(), guid)


    pass # end of TestCase


# helpers
_id = 0
def guid():
    global _id
    _id += 1
    return str(_id)



def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
