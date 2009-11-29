#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
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
        'attribute type assignment test'

        db = self.dbManager()
        # declare tables
        from dsaw.db.WithID import WithID
        class AttributeTypeAssignmentTest(WithID):
            name = 'attributetypeassignmenttest'
            
            myattribute = 'cake'
            
            def sayhi(self):
                print 'hi'

        db.registerTable(AttributeTypeAssignmentTest)
        db.createAllTables()

        t1 = AttributeTypeAssignmentTest()
        t1.id = 't1'
        t1.myattribute = 'bigcake'
        db.insertRow(t1)

        t1.myattribute = 'biggercake'
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
