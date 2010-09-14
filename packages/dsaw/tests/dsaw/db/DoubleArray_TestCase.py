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


import unittest

class TestCase(unittest.TestCase):


    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test-pyre-db') #, echo=True)
        db.autocommit(True)
        return db
    

    def test1(self):
        'dsaw.db.Psycopg2: double array type'

        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        class DoubleArrayTest(WithID):
            name = 'doublearraytest'
            import dsaw.db
            arr = dsaw.db.doubleArray(name='arr')
            m = dsaw.db.doubleArray(name='m', shape=(2,3))

        db.registerTable(DoubleArrayTest)
        db.createAllTables()

        t1 = DoubleArrayTest()
        t1.id = 't1'
        t1.arr = [1.,2.]
        db.insertRow(t1)

        t1.arr = [3.,4.]
        db.updateRecord(t1)

        t1.arr = [5.,6.]
        t1.m = [ [0,1,2], [3,4,5] ]
        self.assertEqual(t1.m.shape, (2,3))
        
        t1.m = [ [0,1./3,2], [3,4,5] ]
        db.updateRecord(t1)
        self.assert_(abs(t1.m[0,1]-1./3)<1e-12)

        t1a = db.query(DoubleArrayTest).filter_by(id='t1').one()
        self.assert_(abs(t1a.m[0,1]-1./3)<1e-12)
        
        db.destroyAllTables()
        return
    

    pass # end of TestCase


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
