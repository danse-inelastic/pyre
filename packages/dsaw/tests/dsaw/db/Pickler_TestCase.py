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
        self.removeDB()
        
        from dsaw.db.Table import Table
        class User(Table):

            name = 'users'
            
            import dsaw.db
            username = dsaw.db.varchar(name='username', length=32)

            id = dsaw.db.integer(name='id')
            id.constraints = 'PRIMARY KEY'

        user1 = User(); user1.id = 1; user1.username = 'user1'

        db = self.dbManager()
        db.createTable(User)
        db.insertRow(user1)
        db.commit()
        del db

        from dsaw.db.Pickler import Pickler
        outdir = 'pickle-test1-out'
        if os.path.exists(outdir):
           shutil.rmtree(outdir)
        db = self.dbManager()
        pickler = Pickler(db, outdir)
        pickler.dump(User)

        import pickle
        pkl = os.path.join(outdir, User.getTableName())
        tablename, fields, records = pickle.load(open(pkl))

        self.assertEqual(tablename, User.getTableName())
        self.assertEqual(fields, tuple(user1.getColumnNames()))
        self.assertEqual(records[0][0], user1.getColumnValue(user1.getColumnNames()[0]))
        
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
