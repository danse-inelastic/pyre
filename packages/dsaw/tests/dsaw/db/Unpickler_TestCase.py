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


import dsaw.db
from dsaw.db.Table import Table
from tables import *

import unittest, os, shutil

class TestCase(unittest.TestCase):


    dbname = 'test'
    def removeDB(self):
        dbname = self.dbname
        if os.path.exists(dbname):
            os.remove(dbname)
        return
    

    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='sqlite:///%s' % self.dbname)
        db.autocommit(True)
        return db
    

    def test1(self):
        'dsaw.db.unpickler: basic table'
        self.removeDB()
        db = self.dbManager()
        
        from dsaw.db.Unpickler import Unpickler
        indir = 'unpickle-inputs/test1'
        unpickler = Unpickler(db, indir)
        unpickler.load([User])

        records = db.query(User).all()
        self.assertEqual(len(records), 1)
        user1 = records[0]
        self.assertEqual(user1.id, 1)
        self.assertEqual(user1.username, 'user1')
        return
    
    
    def test2(self):
        'dsaw.db.unpickler: table with a column being reference'
        self.removeDB()
        db = self.dbManager()
        
        from dsaw.db.Unpickler import Unpickler
        indir = 'unpickle-inputs/test2'
        unpickler = Unpickler(db, indir)
        unpickler.load([User, Simulation])
        
        records = db.query(User).all()
        self.assertEqual(len(records), 1)
        user1 = records[0]
        self.assertEqual(user1.id, 1)
        self.assertEqual(user1.username, 'user1')

        records = db.query(Simulation).all()
        self.assertEqual(len(records), 1)
        sim1 = records[0]
        self.assertEqual(sim1.id, 5)
        self.assertEqual(sim1.creator.dereference(db).id, user1.id)
        return
    
    
    def test3(self):
        'dsaw.db.unpickler: table with a column being versatile reference'
        self.removeDB()
        db = self.dbManager()
        
        from dsaw.db.Unpickler import Unpickler
        indir = 'unpickle-inputs/test3'
        unpickler = Unpickler(db, indir)
        unpickler.load([Cylinder, Sample, global_pointer])

        records = db.query(Cylinder).all()
        self.assertEqual(len(records), 1)
        cylinder1 = records[0]
        self.assertEqual(cylinder1.id, 3)

        records = db.query(Sample).all()
        self.assertEqual(len(records), 1)
        sample1 = records[0]
        self.assertEqual(sample1.id, 5)
        shape = sample1.shape.dereference(db)
        self.assertEqual(shape.id, cylinder1.id)
        self.assertEqual(shape.__class__, Cylinder)
        
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
