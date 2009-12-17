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
