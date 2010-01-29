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


# helpers

#
_id = 0
def guid():
    global _id
    _id += 1
    return str(_id)


import dataobjects_with_inventory as dataobjects

import unittest

class TestCase(unittest.TestCase):


    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db


    def ormManager(self):
        from dsaw.model.visitors.OrmManager import OrmManager
        return OrmManager(self.dbManager(), guid)


    def test1(self):
        Dummy = dataobjects.Dummy
        
        # create a data object instance
        dummy = Dummy('hello')

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
        dummy = Dummy('hello')
        
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
        
        #
        orm2.db.destroyAllTables()
        orm.db.destroyAllTables()
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
        orm.save(computation)
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


    pass # end of TestCase


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
