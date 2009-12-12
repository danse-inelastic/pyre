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
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db
    

    def test1(self):
        'dsaw.db.Psycopg2: varchar array type'

        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        class VarCharArrayTest(WithID):
            name = 'varchararraytest'
            import dsaw.db
            arr = dsaw.db.varcharArray(name='arr', length=10)

        db.registerTable(VarCharArrayTest)
        db.createAllTables()

        t1 = VarCharArrayTest()
        t1.id = 't1'
        t1.arr = ['a', 'b', 'c']
        db.insertRow(t1)

        t1.arr = ['hello', 'world']
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
