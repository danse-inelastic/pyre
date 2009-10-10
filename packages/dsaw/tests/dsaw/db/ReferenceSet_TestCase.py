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


    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db


    def test1(self):
        'dsaw.db.ReferenceSet: '
        db = self.dbManager()

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


        tables = [
            User,
            Group,
            ]
        for table in tables:
            db.registerTable(table)

        db.createAllTables()

        # insert records
        userbob = User()
        userbob.id = userbob.username = 'bob'
        db.insertRow(userbob)
        
        useralice = User()
        useralice.id = useralice.username = 'alice'
        db.insertRow(useralice)
        db.commit()

        group = Group()
        group.id = 'group1'
        db.insertRow(group)
        db.commit()

        refset = group.users
        print 'referenceset instance: %s' % refset
        users = refset.dereference( db )
        self.assertEqual(len(users), 0)
        print 'users: %s' % (users,)

        print '> add one user' 
        refset.add( userbob, db )
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
        self.assert_('bob' in ids)
        self.assert_('alice' in ids)

        print '> remove all users'
        refset.clear( db )
        users = refset.dereference( db )
        self.assertEqual(len(users), 0)


        # finish  and clean up
        db.destroyAllTables()
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
