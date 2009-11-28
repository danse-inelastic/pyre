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




# all data objects used by this test are in the module "dataobjects".
import dataobjects as do

import unittest

class TestCase(unittest.TestCase):


    def test1(self):
        'simple data object'
        orm = self.orm

        dummy = do.Dummy(a='whatever', x=2., i=2, b=False)
        orm.save(dummy)

        dummy.a = 'dsaw'
        orm.save(dummy)

        dummy2 = orm.load(do.Dummy, id=orm.object2record(dummy).id)
        self.assertEqual(dummy2.a, dummy.a)
        return


    def test2(self):
        'data object with reference and referenceset'
        orm = self.orm

        struct = do.Structure(shape=do.Cylinder(r=3,h=10), atoms=[do.Atom(), do.Atom('C')])
        orm.save(struct)

        struct1 = do.Structure(shape=None, atoms=[do.Atom(), do.Atom('C')])
        orm.save(struct1)

        struct2 = orm.load(do.Structure, id=orm.object2record(struct).id)
        struct2.atoms = [do.Atom('He')]
        struct2.shape = None
        orm.save(struct2)

        struct2.shape = do.Box(x=1,y=1,z=1)
        orm.save(struct2)

        sample = do.Sample()
        sample.shape = do.Cylinder(r=1, h=5)
        orm.save(sample)

        # getObjectTypeFromName
        self.assertEqual(orm.getObjectTypeFromName('Sample'), do.Sample)
       
        self.orm2.registerObjectType(do.Cylinder)
        sample2 = self.orm2.load(do.Sample, id=orm.object2record(sample).id)
        self.assertEqual(sample2.shape.__class__, do.Cylinder)
        self.assertEqual(sample2.shape.r, sample.shape.r)
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


#
def pysuite():
    import journal
    journal.debug('dsaw.model').activate()
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
