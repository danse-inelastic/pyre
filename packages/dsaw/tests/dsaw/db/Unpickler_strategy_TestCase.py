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


    def dbManager(self, dbname):
        from dsaw.db import connect
        db = connect(db ='sqlite:///%s' % dbname)
        db.autocommit(True)
        return db


    def preparedb(self, newdbname):
        cmd = 'cp db-inputs/test %s' % newdbname
        import os
        os.system(cmd)
        return
    

    def test1(self):
        'dsaw.db.unpickler: overwrite'
        dbname = 'test1'
        self.preparedb(dbname)
        db = self.dbManager(dbname)
        
        from dsaw.db.Unpickler import Unpickler
        indir = 'unpickle-inputs/test1a'
        unpickler = Unpickler(db, indir)
        unpickler.load([User], strategy = 'overwrite')
        
        records = db.query(User).all()
        self.assertEqual(len(records), 1)
        user1 = records[0]
        self.assertEqual(user1.id, 1)
        self.assertEqual(user1.username, 'user1a')
        
        return
    
    
    def test2(self):
        'dsaw.db.unpickler: skip'
        dbname = 'test2'
        self.preparedb(dbname)
        db = self.dbManager(dbname)
        
        from dsaw.db.Unpickler import Unpickler
        indir = 'unpickle-inputs/test1a'
        unpickler = Unpickler(db, indir)
        unpickler.load([User], strategy = 'skip')
        
        records = db.query(User).all()
        self.assertEqual(len(records), 1)
        user1 = records[0]
        self.assertEqual(user1.id, 1)
        self.assertEqual(user1.username, 'user1')
        
        return
    
    
    def test3(self):
        'dsaw.db.unpickler: prompt'
        dbname = 'test2'
        self.preparedb(dbname)
        db = self.dbManager(dbname)
        
        from dsaw.db.Unpickler import Unpickler
        indir = 'unpickle-inputs/test1a'
        unpickler = Unpickler(db, indir)
        unpickler.load([User], strategy = 'prompt')
        
        records = db.query(User).all()
        for r in records:
            print r
        
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
