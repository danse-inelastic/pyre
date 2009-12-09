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


    def test1(self):
        'dsaw.db.ReferenceSet: '

        # create table
        from dsaw.db.WithID import WithID
        class Test(WithID):

            name = "test"
            import dsaw.db

        # add more columns 
        import dsaw.db
        address = dsaw.db.varchar(name='address', length=16)
        Test.addColumn(address)

        # 
        db = self.db

        # create table
        db.registerTable(Test)
        db.createAllTables()

        # create new record
        t = Test()
        t.id = '111'
        t.address = 'abc'
        db.insertRow(t)

        # load from db and compare
        t1 = db.query(Test).filter_by(id=t.id).one()
        self.assertEqual(t.address, t1.address)
        
        return


    def setUp(self):
        self.db = self.dbManager()
        return


    def tearDown(self):
        self.db.destroyAllTables()
        return
    
    
    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db


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
