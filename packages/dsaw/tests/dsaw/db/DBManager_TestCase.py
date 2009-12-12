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
        'dsaw.db.Psycopg2: connect'
        from dsaw.db import connect
        db = connect(db = 'postgres:///test')
        return


    def test2(self):
        'dsaw.db.Psycopg2: normal table'
        db = self.dbManager()

        # init system tables
        db.createSystemTables()

        from dsaw.db.WithID import WithID
        class Table1(WithID):
            name = 'table1'
            import dsaw.db
            greeting = dsaw.db.varchar(name='greeting', length=100)
            
        db.createTable(Table1)

        # insert record
        row = Table1()
        row.greeting = 'hello'
        row.id = 'first'
        db.insertRow(row)

        # fetch it
        rows = db.fetchall(Table1, where="id='%s'" % row.id)
        self.assertEqual(len(rows), 1)
        row1 = rows[0]
        self.assertEqual(row1.greeting, row.greeting)
        
        db.dropTable(Table1)

        # remove system tables
        db.destroySystemTables()
        return
    
    
    def test3(self):
        'dsaw.db.Psycopg2: table with reference'
        db = self.dbManager()

        from dsaw.db.WithID import WithID
        class User(WithID):
            name = 'users'
            import dsaw.db
            username = dsaw.db.varchar(name='username', length=100)

        class Greeting(WithID):
            name = 'greetings'
            import dsaw.db
            greeting = dsaw.db.varchar(name='greeting', length=100)
            who = dsaw.db.reference(name='who', table=User)
            
        tables = [User, Greeting]

        # init system tables
        db.createSystemTables()

        #
        for table in tables: db.createTable(table)

        # create a user
        user = User()
        user.username = 'bob'
        user.id = 'bob1'
        db.insertRow(user)
        
        # create a greeting
        greeting = Greeting()
        greeting.who = user
        greeting.greeting = 'hello'
        greeting.id = 'greeting1'
        db.insertRow(greeting)

        #
        tables.reverse()
        for table in tables: db.dropTable(table)

        #
        db.destroySystemTables()
        return
    

    def test3a(self):
        'dsaw.db.Psycopg2: table with reference. catch non-existing reference'
        
        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        class User(WithID):
            name = 'users'
            import dsaw.db
            username = dsaw.db.varchar(name='username', length=100)

        class Greeting(WithID):
            name = 'greetings'
            import dsaw.db
            greeting = dsaw.db.varchar(name='greeting', length=100)
            who = dsaw.db.reference(name='who', table=User)
            
        tables = [User, Greeting]

        # init system tables
        db.createSystemTables()

        #
        for table in tables: db.createTable(table)

        # create a greeting
        greeting = Greeting()
        greeting.id = 'greeting1'
        greeting.who = 'a'
        greeting.greeting = 'hello'
        self.assertRaises(db.IntegrityError, db.insertRow, greeting)

        #
        tables.reverse()
        for table in tables: db.dropTable(table)

        #
        db.destroySystemTables()
        return
    

    def test3b(self):
        'dsaw.db.Psycopg2: table with reference. catch dangling reference'
        
        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        class User(WithID):
            name = 'users'
            import dsaw.db
            username = dsaw.db.varchar(name='username', length=100)

        class Greeting(WithID):
            name = 'greetings'
            import dsaw.db
            greeting = dsaw.db.varchar(name='greeting', length=100)
            who = dsaw.db.reference(name='who', table=User)
            
        tables = [User, Greeting]

        # init system tables
        db.createSystemTables()

        #
        for table in tables: db.createTable(table)

        # create a user
        user = User()
        user.id = user.username = 'bob'
        db.insertRow(user)
        
        # create a greeting
        greeting = Greeting()
        greeting.who = user
        greeting.greeting = 'hello'
        greeting.id = 'greeting1'
        db.insertRow(greeting)

        # delete user would leave a dangling reference
        self.assertRaises(db.RecordStillReferred, db.deleteRecord, user)
        
        #
        tables.reverse()
        for table in tables: db.dropTable(table)

        #
        db.destroySystemTables()
        return
    

    def test3c(self):
        'dsaw.db.Psycopg2: table with reference. updateRecord'

        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        class User(WithID):
            name = 'users'
            import dsaw.db
            username = dsaw.db.varchar(name='username', length=100)

        class Greeting(WithID):
            name = 'greetings'
            import dsaw.db
            greeting = dsaw.db.varchar(name='greeting', length=100)
            who = dsaw.db.reference(name='who', table=User)

        db._tablemap.registerTable(User)
        db._tablemap.TableToObject(User)
            
        tables = [User, Greeting]
        for table in tables: db.registerTable(table)

        db.createAllTables()

        # create two users
        userbob = User()
        userbob.id = userbob.username = 'bob'
        db.insertRow(userbob)
        
        useralice = User()
        useralice.id = useralice.username = 'alice'
        db.insertRow(useralice)
        
        # create a greeting
        greeting = Greeting()
        greeting.who = userbob
        greeting.greeting = 'hello'
        greeting.id = 'greeting1'
        db.insertRow(greeting)

        # update
        greeting.who = useralice
        greeting.greeting = 'aloha'
        db.updateRecord(greeting)
        
        # fetch it
        greeting1 = db.query(Greeting).filter_by(id=greeting.id).one()
        self.assertEqual(greeting1.greeting, 'aloha')
        self.assertEqual(greeting1.who.id, useralice.id)

        db.destroyAllTables()
        return
    

    def test4(self):
        'dsaw.db: DBManager.getUniqueIdentifierStr and DBManager.fetchRecordUsingUniqueIdentifierStr'

        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        class User(WithID):
            name = 'users'
            import dsaw.db
            username = dsaw.db.varchar(name='username', length=100)

        # register and initialize
        tables = [User]
        for table in tables: db.registerTable(table)
        db.createAllTables()

        # insert a record
        bob = User()
        bob.id = bob.username = 'bob'
        db.insertRow(bob)
        
        #
        uidstr = db.getUniqueIdentifierStr(bob)
        bob1 = db.fetchRecordUsingUniqueIdentifierStr(uidstr)
        assert bob1.id == bob.id
        assert bob1.username == bob.username
        
        # destroy
        db.destroyAllTables()
        return
        
    def test5(self):
        'dsaw.db: make sure globalpointer is left blank when a record is created'

        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        from dsaw.db.GloballyReferrable import GloballyReferrable
        class User(WithID, GloballyReferrable):
            name = 'users'
            import dsaw.db
            username = dsaw.db.varchar(name='username', length=100)

        # register and initialize
        tables = [User]
        for table in tables: db.registerTable(table)
        db.createAllTables()

        # insert a record
        bob = User()
        bob.id = bob.username = 'bob'
        db.insertRow(bob)

        # read
        bob1 = db.query(User).filter_by(id=bob.id).one()
        self.assertEqual(bob1.globalpointer, None)
        
        # destroy
        db.destroyAllTables()
        return
        
    pass # end of TestCase


# init system tables
def create_system_tables(db):
    from dsaw.db import systemTables
    system_tables = systemTables()
    for table in system_tables.itertables():
        db.createTable(table)
        continue
    return

# fini system tables
def destroy_system_tables(db):
    from dsaw.db import systemTables
    system_tables = systemTables()
    for table in system_tables.itertables():
        db.dropTable(table)
        continue
    return

    
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
