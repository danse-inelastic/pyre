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
        'simple data object'
        orm = self.orm

        from greet import GreetApp
        app = GreetApp()
        app.inventory.name = 'bob'
        orm.save(app)

        app2 = orm.load(GreetApp, orm(app).id)
        self.assertEqual(app2.inventory.name, app.inventory.name)
        
        return


    def setUp(self):
        self.orm = self._ormManager()
        self.orm2 = self._ormManager()


    def tearDown(self):
        del self.orm2
        
        db = self.orm.db
        db.destroyAllTables()
        return
        

    def _dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db


    def _ormManager(self):
        from dsaw.model.visitors.OrmManager import OrmManager
        return OrmManager(self._dbManager(), guid)


    pass # end of TestCase


# helpers
_id = 0
def guid():
    global _id
    _id += 1
    return str(_id)


#
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
