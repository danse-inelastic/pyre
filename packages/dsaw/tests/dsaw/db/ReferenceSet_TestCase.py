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


    def test1(self):
        'add, delete users'
        db = self.db
        
        # insert records
        userbob = User()
        userbob.id = userbob.username = 'bob1'
        db.insertRow(userbob)
        
        group = Group()
        group.id = 'group1'
        db.insertRow(group)

        refset = group.users
        users = refset.dereference( db )
        self.assertEqual(len(users), 0)

        print '> add one user' 
        refset.add( userbob, db, name='1' )
        users = refset.dereference( db )
        self.assertEqual(len(users), 1)

        print '> delete one user'
        refset.delete( userbob, db )
        users = refset.dereference( db )
        self.assertEqual(len(users), 0)
        return



    def test2(self):
        'add, delete two users'
        db = self.db
        
        # insert records
        userbob = User()
        userbob.id = userbob.username = 'bob2'
        db.insertRow(userbob)
        
        useralice = User()
        useralice.id = useralice.username = 'alice2'
        db.insertRow(useralice)

        group = Group()
        group.id = 'group2'
        db.insertRow(group)
        db.commit()

        refset = group.users
        refset.add(userbob, db)
        refset.add(useralice, db)

        users = refset.dereference(db)
        self.assertEqual(len(users), 2)

        refset.delete(useralice, db)
        refset.delete(userbob, db)
        return



    def test3(self):
        'get, set, delete by key'
        db = self.db
        
        # insert records
        userbob = User()
        userbob.id = userbob.username = 'bob3'
        db.insertRow(userbob)
        
        useralice = User()
        useralice.id = useralice.username = 'alice3'
        db.insertRow(useralice)

        group = Group()
        group.id = 'group3'
        db.insertRow(group)
        db.commit()

        refset = group.users
        refset.setElement(element=userbob, db=db, key='key1')
        refset.setElement(element=useralice, db=db, key='key2')

        user1 = refset.getElement(db=db, key='key1')
        self.assertEqual(user1.id, userbob.id)

        user2 = refset.getElement(db=db, key='key2')
        self.assertEqual(user2.id, useralice.id)

        refset.delElement(db=db, key='key1')
        self.assertEqual(len(refset.dereference(db)), 1)

        user2 = refset.getElement(db=db, key='key2')
        self.assertEqual(user2.id, useralice.id)

        user0 = refset.getElement(db=db, index=0)
        self.assertEqual(user0.id, useralice.id)

        refset.setElement(db=db, key='key1', element=userbob)

        user1 = refset.getElement(db=db, index=1)
        self.assertEqual(user1.id, userbob.id)
        return



    def test4(self):
        'get, set, delete by index'
        db = self.db
        
        # insert records
        userbob = User()
        userbob.id = userbob.username = 'bob4'
        db.insertRow(userbob)
        
        useralice = User()
        useralice.id = useralice.username = 'alice4'
        db.insertRow(useralice)

        group = Group()
        group.id = 'group4'
        db.insertRow(group)
        db.commit()

        refset = group.users

        # bob, alice
        refset.add(userbob, db=db)
        refset.add(useralice, db=db)

        user0 = refset.getElement(db=db, index=0)
        self.assertEqual(user0.id, userbob.id)

        # alice, alice
        refset.setElement(element=useralice, index=0, db=db)
        user0 = refset.getElement(db=db, index=0)
        self.assertEqual(user0.id, useralice.id)

        # alice, bob
        refset.setElement(element=userbob, index=1, db=db)
        user0 = refset.getElement(db=db, index=0)
        self.assertEqual(user0.id, useralice.id)
        user1 = refset.getElement(db=db, index=1)
        self.assertEqual(user1.id, userbob.id)

        # bob
        refset.delElement(index=0, db=db)
        user0 = refset.getElement(db=db, index=0)
        self.assertEqual(user0.id, userbob.id)
        
        return



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
