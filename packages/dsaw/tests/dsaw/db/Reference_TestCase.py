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
        
        print greeting.who
        print greeting.who.dereference(db)

        #
        tables.reverse()
        for table in tables: db.dropTable(table)

        #
        db.destroySystemTables()
        return
    

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
