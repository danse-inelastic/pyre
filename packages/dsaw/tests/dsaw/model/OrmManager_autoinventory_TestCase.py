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


import dataobjects

import unittest

class TestCase(unittest.TestCase):


    def test1(self):
        Dummy = dataobjects.Dummy
        
        # create a data object instance
        dummy = Dummy(a='hello', x=2., i=2, b=False)

        # orm manager
        orm = self.ormManager()
        orm.save(dummy)

        #
        db = orm.db
        db.destroyAllTables()
        return
    

    def test1a(self):
        Dummy = dataobjects.Dummy
        
        # create a data object instance
        dummy = Dummy(a='hello', x=2., i=2, b=False, vec=range(10), mat=range(12))
        
        # orm manager
        orm = self.ormManager()
        # save
        orm.save(dummy)
        
        # new orm
        orm2 = self.ormManager()
        # load
        orm2.registerObjectType(Dummy)
        id = orm.object2record(dummy).id
        #id = '1'
        dummy2 = orm2.load(Dummy, id)
        #self.assertEqual(dummy2.a, 'hello')
        self.assertEqual(dummy2.a, dummy.a)
        self.assertEqual(type(dummy2.a), str)
        self.assertEqual(dummy2.x, dummy.x)
        self.assertEqual(type(dummy2.x), float)
        self.assertEqual(dummy2.i, dummy.i)
        self.assertEqual(type(dummy2.i), int)
        self.assertEqual(dummy2.b, dummy.b)
        self.assertEqual(type(dummy2.b), bool)

        vec = dummy2.vec
        for i in range(10):
            self.assertEqual(vec[i],i)

        mat = dummy2.mat
        self.assertEqual(mat[0,0], 0)
        self.assertEqual(mat[2,3], 11)
        #
        orm2.db.destroyAllTables()
        orm.db.destroyAllTables()
        return
    

    def test1b(self):
        'destroy'
        Dummy = dataobjects.Dummy
        
        # create a data object instance
        dummy = Dummy(a='hello', x=2., i=2, b=False)

        # orm manager
        orm = self.ormManager()
        orm.save(dummy)

        # db record id
        r = orm.object2record(dummy)
        rid = r.id
        
        # try load it
        self.assertEqual(
            orm.db.query(orm.object2record.object2dbtable(Dummy)).filter_by(id=rid).count(),
            1)
        
        # destroy
        orm.destroy(dummy)

        # try load it
        self.assertEqual(
            orm.db.query(orm.object2record.object2dbtable(Dummy)).filter_by(id=rid).count(),
            0)
        
        #
        db = orm.db
        db.destroyAllTables()
        return
    

    def test2(self):
        Computation = dataobjects.Computation
        Job = dataobjects.Job
        
        # create data objects
        computation = Computation('what?')
        job = Job('a.b.c', computation)

        # orm manager
        orm = self.ormManager()

        # save to db
        orm.save(job)

        # load from db and compare
        db = orm.db
        r = orm.object2record(computation)
        id = r.id
        r = db.query(r.__class__).filter_by(id=id).one()
        self.assertEqual(r.about, computation.about)

        # update and save
        computation.about = 'hey'
        orm.save(computation)
        r = db.query(r.__class__).filter_by(id=id).one()
        self.assertEqual(r.about, computation.about)
        
        #
        db.destroyAllTables()
        return


    def test2a(self):
        Computation = dataobjects.Computation
        Job = dataobjects.Job
        
        # create data objects
        computation = Computation('what?')
        job = Job('a.b.c', computation)

        # orm manager
        orm = self.ormManager()

        # save to db
        orm.save(job)

        # 
        # new orm
        orm2 = self.ormManager()
        # load
        orm2.registerObjectType(Computation)
        orm2.registerObjectType(Job)
        id = orm.object2record(job).id
        #id = '1'
        job2 = orm2.load(Job, id)
        self.assertEqual(job.server, job2.server)

        computation2 = job2.computation
        self.assertEqual(computation2.about, computation.about)
        self.assertEqual(computation2.__class__, computation.__class__)
        
        #
        orm2.db.destroyAllTables()
        #
        orm.db.destroyAllTables()
        return


    def test2b(self):
        'destroy object with reference'
        Job = dataobjects.Job
        Computation = dataobjects.Computation
        
        # create a data object instance
        job = Job(server='server', computation=Computation(about='weather'))

        # orm manager
        orm = self.ormManager()
        orm.save(job)

        # db record id
        jobid = orm.object2record(job).id
        computationid = orm.object2record(job.computation).id
        
        # tables
        JobTable = orm.object2record.object2dbtable(Job)
        ComputationTable = orm.object2record.object2dbtable(Computation)
        
        self.assertEqual(
            orm.db.query(JobTable).filter_by(id=jobid).count(),
            1)
        self.assertEqual(
            orm.db.query(ComputationTable).filter_by(id=computationid).count(),
            1)
        
        # destroy
        orm.destroy(job)

        # 
        self.assertEqual(
            orm.db.query(JobTable).filter_by(id=jobid).count(),
            0)
        self.assertEqual(
            orm.db.query(ComputationTable).filter_by(id=computationid).count(),
            0)
        
        #
        db = orm.db
        db.destroyAllTables()
        return


    def test3(self):
        'object with reference set'
        import dataobjects as do
        struct = do.Structure(shape=do.Cylinder(r=3,h=10), atoms=[do.Atom(), do.Atom('C')])

        # orm manager
        orm = self.ormManager()
        orm.save(struct)

        # load from db and compare
        db = orm.db
        r = orm.object2record(struct)
        id = r.id
        r = db.query(r.__class__).filter_by(id=id).one()
        shape = r.shape.dereference(db)
        self.assertEqual(shape.r, struct.shape.r)
        self.assertEqual(shape.h, struct.shape.h)

        # reference to "None" 
        struct1 = do.Structure(shape=None, atoms=[do.Atom(), do.Atom('C')])
        orm.save(struct1)

        # load from db and compare
        r1 = orm.object2record(struct1)
        self.assertEqual(r1.shape and r1.shape.id, None)
        
        #
        db = orm.db
        db.destroyAllTables()
        return


    def test3a(self):
        'object with reference set: update'
        import dataobjects as do
        struct = do.Structure(shape=do.Cylinder(r=3,h=10), atoms=[do.Atom(), do.Atom('C')])

        # orm manager
        orm = self.ormManager()
        orm.save(struct)

        # load from db and check
        db = orm.db
        AtomTable = orm.object2record.object2dbtable(do.Atom)
        rs = db.query(AtomTable).all()
        symbols = [r.symbol for r in rs]
        self.assertEqual(len(symbols), 2)
        self.assert_('H' in symbols)
        self.assert_('C' in symbols)

        #
        struct.atoms[0].symbol = 'C'
        orm.save(struct)

        # load from db and compare
        db = orm.db
        AtomTable = orm.object2record.object2dbtable(do.Atom)
        rs = db.query(AtomTable).all()
        symbols = [r.symbol for r in rs]
        self.assertEqual(symbols, ['C', 'C'])

        #
        db = orm.db
        db.destroyAllTables()
        return

    
    def test3aa(self):
        'object with reference set: update reference and referenceset'
        import dataobjects as do
        struct = do.Structure(shape=do.Cylinder(r=3,h=10), atoms=[do.Atom(), do.Atom('C')])

        # orm manager
        orm = self.ormManager()
        orm.save(struct)

        #
        struct.shape = do.Box(x=1, y=1, z=1)
        struct.atoms[0] = do.Atom('C')
        orm.save(struct)

        # load from db and compare
        db = orm.db
        AtomTable = orm.object2record.object2dbtable(do.Atom)
        rs = db.query(AtomTable).all()
        symbols = [r.symbol for r in rs]
        self.assertEqual(symbols, ['C', 'C'])

        CylinderTable = orm.object2record.object2dbtable(do.Cylinder)
        self.assertEqual(db.query(CylinderTable).count(), 0)
        BoxTable = orm.object2record.object2dbtable(do.Box)
        self.assertEqual(db.query(BoxTable).count(), 1)

        # None for reference
        struct.shape = None
        orm.save(struct)
        
        #
        db = orm.db
        db.destroyAllTables()
        return

    
    def test3b(self):
        'object with reference set: destroy'
        import dataobjects as do
        struct = do.Structure(shape=do.Cylinder(r=3,h=10), atoms=[do.Atom(), do.Atom('C')])

        # orm manager
        orm = self.ormManager()
        orm.save(struct)

        # load from db and compare
        db = orm.db
        r = orm.object2record(struct)
        id = r.id
        r = db.query(r.__class__).filter_by(id=id).one()
        shape = r.shape.dereference(db)
        self.assertEqual(shape.r, struct.shape.r)
        self.assertEqual(shape.h, struct.shape.h)

        # destroy
        orm.destroy(struct)

        # 
        self.assertEqual(db.query(r.__class__).filter_by(id=id).count(), 0)
        object2dbtable = orm.object2record.object2dbtable
        self.assertEqual(db.query(object2dbtable(do.Atom)).count(), 0)
        self.assertEqual(db.query(object2dbtable(do.Cylinder)).count(), 0)

        #
        db = orm.db
        db.destroyAllTables()
        return


    def test4(self):
        '__establishInventory__ and __restoreFromInventory__'
        import dataobjects as do
        pos = do.Position()
        pos.setX(10.)

        # orm manager
        orm = self.ormManager()
        orm.save(pos)

        #
        posrec = orm.object2record(pos)
        id = posrec.id
        pos1 = orm.load(do.Position, id)
        self.assertEqual(pos1.getX(), 10.)

        pos.setX(0)
        self.assertEqual(pos1.getX(), 10.)
        
        #
        db = orm.db
        db.destroyAllTables()
        return
        

    
    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db


    def ormManager(self):
        from dsaw.model.visitors.OrmManager import OrmManager
        return OrmManager(self.dbManager(), guid)


    pass # end of TestCase


# helpers
_id = 0
def guid():
    global _id
    _id += 1
    return str(_id)


def pysuite():
    import journal
    journal.debug('dsaw.model').activate()
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
