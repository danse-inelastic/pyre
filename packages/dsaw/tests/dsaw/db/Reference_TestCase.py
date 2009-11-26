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
        'dsaw.db.Reference: '
        import dsaw.db
        
        db = dsaw.db.connect(db='postgres:///test')
        db.autocommit(True)

        print 'declare tables'
        from dsaw.db.WithID import WithID
        class Cylinder(WithID):
            name = 'cylinders'
            radius = dsaw.db.real(name='radius')
            height = dsaw.db.real(name='height')
            
        class Scatterer(WithID):
            name = 'scatterers'
            shape = dsaw.db.reference(name='shape', table=Cylinder)
            
        tables = [
            Cylinder,
            Scatterer,
            ]
        for table in tables:
            db.registerTable(table)
            
        db.createAllTables()
        
        print 'insert records'
        cylinder1 = Cylinder()
        cylinder1.id = 'cylinder1'
        cylinder1.radius = 5
        cylinder1.height = 10
        
        scatterer1 = Scatterer()
        scatterer1.id = 'scatterer1'
        scatterer1.shape = cylinder1
        
        rows = [
            cylinder1,
            scatterer1,
            ]
        for row in rows: db.insertRow(row)
        
        print 'dereference'
        shape1 = scatterer1.shape.dereference(db)
        self.assertEqual( shape1.__class__, Cylinder)
        self.assertEqual(shape1.id, cylinder1.id)
        
        print "make sure we don't create dangling reference"
        self.assertRaises(db.RecordStillReferred, db.deleteRecord, cylinder1)
        
        print 'updateRecord 3: switch to None'
        scatterer1.shape = None
        db.updateRecord(scatterer1)
        shape1 = scatterer1.shape
        self.assertEqual(shape1, None)
        
        print 'remove tables'
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
