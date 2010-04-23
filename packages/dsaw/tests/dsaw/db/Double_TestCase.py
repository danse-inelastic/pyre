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
        db = connect(db ='postgres:///test') #, echo=True)
        db.autocommit(True)
        return db
    

    def test1(self):
        'dsaw.db.Psycopg2: double type'

        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        class DoubleTest(WithID):
            name = 'doubletest'
            import dsaw.db
            d = dsaw.db.double(name='d')
            r = dsaw.db.real(name='r')

        db.registerTable(DoubleTest)
        db.createAllTables()

        t1 = DoubleTest()
        t1.id = 't1'
        import math
        t1.r = t1.d = math.pi
        db.insertRow(t1)

        self.assertAlmostEqual(t1.r, math.pi, 5)
        self.assertNotAlmostEqual(t1.r, math.pi, 10)
        self.assertAlmostEqual(t1.d, math.pi, 10)
        
        t1.d = math.e
        db.updateRecord(t1)
        
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
