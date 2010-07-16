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
        'dsaw.db.pickler: basic table'
        self.removeDB()
        
        user1 = User(); user1.id = 1; user1.username = 'user1'

        db = self.dbManager()
        db.createTable(User)
        db.insertRow(user1)
        db.commit()

        from dsaw.db.Pickler import Pickler
        outdir = 'pickle-test1-out'
        if os.path.exists(outdir):
           shutil.rmtree(outdir)
        pickler = Pickler(db, outdir)
        pickler.dump(User)

        import pickle
        pkl = os.path.join(outdir, User.getTableName())
        tablename, fields, records = pickle.load(open(pkl))

        self.assertEqual(tablename, User.getTableName())
        self.assertEqual(fields, tuple(user1.getColumnNames()))
        self.assertEqual(records[0][0], user1.getColumnValue(user1.getColumnNames()[0]))
        
        # resolve order
        resolve_order = open(os.path.join(outdir, Pickler.resolve_order_filename)).read()
        resolve_order = resolve_order.splitlines()
        self.assertEqual(resolve_order, ['users']) 
        return
    

    def test2(self):
        'dsaw.db.pickler: table with a column being reference'
        self.removeDB()

        tables = [User, Simulation]
        user1 = User(); user1.id = 1; user1.username = 'user1'
        sim1 = Simulation(); sim1.creator = user1; sim1.id = 5
        records = [
            user1,
            sim1,
            ]

        db = self.dbManager()
        for t in tables:
            db.createTable(t)
        for r in records:
            db.insertRow(r)
        db.commit()

        from dsaw.db.Pickler import Pickler
        outdir = 'pickle-test2-out'
        if os.path.exists(outdir):
           shutil.rmtree(outdir)
        pickler = Pickler(db, outdir)
        pickler.dump(Simulation)

        # load and compare
        import pickle
        #  User
        pkl = os.path.join(outdir, User.getTableName())
        tablename, fields, records = pickle.load(open(pkl))

        self.assertEqual(tablename, User.getTableName())
        self.assertEqual(fields, tuple(user1.getColumnNames()))
        self.assertEqual(records[0][0], user1.getColumnValue(user1.getColumnNames()[0]))

        #  Simulation
        pkl = os.path.join(outdir, Simulation.getTableName())
        tablename, fields, records = pickle.load(open(pkl))

        self.assertEqual(tablename, Simulation.getTableName())
        self.assertEqual(fields, tuple(sim1.getColumnNames()))
        self.assertEqual(records[0][0], sim1.id)
        self.assertEqual(records[0][1], user1.id)
        
        # resolve order
        resolve_order = open(os.path.join(outdir, Pickler.resolve_order_filename)).read()
        resolve_order = resolve_order.splitlines()
        self.assertEqual(resolve_order, ['users', 'simulations']) 
        return
    

    def test3(self):
        'dsaw.db.pickler: table with a column being versatile reference'
        self.removeDB()

        # create tables and insert rows
        tables = [global_pointer, Cylinder, Sample]
        cyl1 = Cylinder(); cyl1.id = 3
        sample1 = Sample(); sample1.shape = cyl1; sample1.id = 5
        records = [
            cyl1,
            sample1,
            ]

        db = self.dbManager()
        for t in tables:
            db.createTable(t)
        for r in records:
            db.insertRow(r)
        db.commit()

        # pickle
        from dsaw.db.Pickler import Pickler
        outdir = 'pickle-test3-out'
        if os.path.exists(outdir):
           shutil.rmtree(outdir)
        pickler = Pickler(db, outdir)
        pickler.dump(tables=tables)

        # load and compare
        import pickle
        #  Cylinder
        pkl = os.path.join(outdir, Cylinder.getTableName())
        tablename, fields, records = pickle.load(open(pkl))
        
        self.assertEqual(tablename, Cylinder.getTableName())
        self.assertEqual(fields, tuple(cyl1.getColumnNames()))
        self.assertEqual(records[0][0], cyl1.globalpointer.id)
        
        #  Sample
        pkl = os.path.join(outdir, Sample.getTableName())
        tablename, fields, records = pickle.load(open(pkl))

        self.assertEqual(tablename, Sample.getTableName())
        self.assertEqual(fields, tuple(sample1.getColumnNames()))
        self.assertEqual(records[0][1], sample1.id)
        self.assertEqual(records[0][0], cyl1.globalpointer.id)

        # resolve order
        resolve_order = open(os.path.join(outdir, Pickler.resolve_order_filename)).read()
        resolve_order = resolve_order.splitlines()
        self.assertEqual(resolve_order, ['global_pointers', 'cylinders', 'samples'])
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
