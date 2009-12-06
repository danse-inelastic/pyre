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


# declare tables
from dsaw.db.GloballyReferrable import GloballyReferrable
from dsaw.db.WithID import WithID
class User(GloballyReferrable, WithID):

    name = "users"

    import dsaw.db

    username = dsaw.db.varchar(name='username', length=30)
    username.meta['tip'] = "the user's name"

    password = dsaw.db.varchar(name="password", length=30)
    password.meta['tip'] = "the user's password"


class Group(GloballyReferrable, WithID):

    name = "groups"

    import dsaw.db

    id = dsaw.db.varchar(name="id", length=30)
    id.constraints = "PRIMARY KEY"

    import dsaw.db
    users = dsaw.db.referenceSet(name = 'users')




import unittest

class TestCase(unittest.TestCase):


    def testMixed(self):
        'dsaw.db.ReferenceSet: mixed'
        db = self.db

        # insert records
        userbob = User()
        userbob.id = userbob.username = 'bobMixed'
        db.insertRow(userbob)
        
        useralice = User()
        useralice.id = useralice.username = 'aliceMixed'
        db.insertRow(useralice)
        db.commit()

        group = Group()
        group.id = 'groupMixed'
        db.insertRow(group)
        db.commit()

        refset = group.users
        print 'referenceset instance: %s' % refset
        users = refset.dereference( db )
        self.assertEqual(len(users), 0)
        print 'users: %s' % (users,)

        print '> add one user' 
        refset.add( userbob, db, name='1' )
        users = refset.dereference( db )
        self.assertEqual(len(users), 1)

        print '> delete one user'
        refset.delete( userbob, db )
        users = refset.dereference( db )
        self.assertEqual(len(users), 0)

        print '> add two users'
        refset.add( userbob, db )
        refset.add( useralice, db )
        users = refset.dereference( db )
        self.assertEqual(len(users), 2)
        ids = [row.id for label, row in users]
        self.assert_('bobMixed' in ids)
        self.assert_('aliceMixed' in ids)

        print '> remove all users'
        refset.clear( db )
        users = refset.dereference( db )
        self.assertEqual(len(users), 0)


        print '> getElement and setElement'
        refset.setElement('1', userbob, db )
        refset.setElement('2', useralice, db )
        self.assertEqual(refset.getElement('1', db).id, userbob.id)
        
        users = refset.dereference( db )
        self.assertEqual(len(users), 2)
        
        ids = [row.id for label, row in users]
        self.assert_('bobMixed' in ids)
        self.assert_('aliceMixed' in ids)

        refset.setElement('2', userbob, db )
        users = refset.dereference( db )
        self.assertEqual(len(users), 2)
        
        ids = [row.id for label, row in users]
        self.assert_('bobMixed' in ids)
        self.assert_('aliceMixed' not in ids)

        print '> delElement'
        deleted = refset.delElement('1', db)
        self.assertEqual(deleted.id, 'bobMixed')
        self.assertEqual(len(refset.dereference(db)), 1)
        self.assertRaises(KeyError, refset.delElement, '1', db)
        
        print '> remove all users'
        refset.clear( db )
        users = refset.dereference( db )
        self.assertEqual(len(users), 0)

        return
    
    
    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db


    def setUp(self):
        db = self.db = self.dbManager()

        tables = [
            User,
            Group,
            ]
        for table in tables:
            db.registerTable(table)

        db.createAllTables()

        return


    def tearDown(self):
        # finish  and clean up
        self.db.destroyAllTables()
        del self.db
        return


    pass # end of TestCase



def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return suite1

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
