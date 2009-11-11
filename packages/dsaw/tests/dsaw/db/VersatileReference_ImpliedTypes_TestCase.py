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
        'dsaw.db.VersatileReference: '
        import dsaw.db
        
        db = dsaw.db.connect(db='postgres:///test')
        db.autocommit(True)

        print 'declare tables'
        from dsaw.db.WithID import WithID
        from dsaw.db.GloballyReferrable import GloballyReferrable
        class Cylinder(WithID, GloballyReferrable):
            name = 'cylinders'
            radius = 1.0
            height = 2.0
            
        class Sphere(WithID, GloballyReferrable):
            name = 'spheres'
            radius = 1.1
            
        class Scatterer(WithID):
            name = 'scatterers'
            shape = dsaw.db.versatileReference(name='shape')
            
        tables = [
            Sphere, Cylinder,
            Scatterer,
            ]
        for table in tables:
            db.registerTable(table)
            
        db.createAllTables()
        
        print 'insert records'
        sphere1 = Sphere()
        sphere1.id = 'sphere1'
        sphere1.radius = 10.
        
        cylinder1 = Cylinder()
        cylinder1.id = 'cylinder1'
        cylinder1.radius = 5
        cylinder1.height = 10
        
        scatterer1 = Scatterer()
        scatterer1.id = 'scatterer1'
        scatterer1.shape = sphere1
        
        rows = [
            sphere1, cylinder1,
            scatterer1,
            ]
        for row in rows: db.insertRow(row)
        
        print 'dereference'
        shape1 = scatterer1.shape.dereference(db)
        self.assertEqual( shape1.__class__, sphere1.__class__)
        self.assertEqual(shape1.id, sphere1.id)
        
        print 'fetch from db'
        rows = db.fetchall(Scatterer, where="id='%s'" % scatterer1.id)
        self.assertEqual(len(rows), 1)
        scatterer1r = rows[0]
        self.assertEqual(scatterer1r.shape.id, sphere1.globalpointer.id)
        
        print "make sure we don't create dangling reference"
        self.assertRaises(db.RecordStillReferred, db.deleteRecord, sphere1)
        
        print 'updateRecord: switch to a different type of shape'
        scatterer1.shape = cylinder1
        db.updateRecord(scatterer1)
        shape1 = scatterer1.shape.dereference(db)
        self.assertEqual( shape1.__class__, cylinder1.__class__)
        self.assertEqual(shape1.id, cylinder1.id)
        
        print 'updateRecord 2: switch to a different type of shape by using a string'
        scatterer1.shape = 'spheres###sphere1'
        db.updateRecord(scatterer1)
        shape1 = scatterer1.shape.dereference(db)
        self.assertEqual(shape1.__class__, sphere1.__class__)
        self.assertEqual(shape1.id, sphere1.id)
        
        print 'remove tables'
        db.destroyAllTables()
        return
    
    
    def test2(self):
        'dsaw.db.GloballyReferrable: establish global pointer automatically'
        import dsaw.db
        
        db = dsaw.db.connect(db='postgres:///test')
        db.autocommit(True)

        print 'declare tables'
        from dsaw.db.WithID import WithID
        from dsaw.db.GloballyReferrable import GloballyReferrable
        class Cylinder(WithID, GloballyReferrable):
            name = 'cylinders'
            radius = dsaw.db.real(name='radius')
            height = dsaw.db.real(name='height')
            
        tables = [
            Cylinder,
            ]
        for table in tables:
            db.registerTable(table)
            
        db.createAllTables()
        
        print 'insert records'
        cylinder1 = Cylinder()
        cylinder1.id = 'cylinder1'
        cylinder1.radius = 5
        cylinder1.height = 10
        
        rows = [
            cylinder1,
            ]
        for row in rows: db.insertRow(row)

        self.assert_( cylinder1.globalpointer and cylinder1.globalpointer.id )

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
