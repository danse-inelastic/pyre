#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.db.Table import Table

class User(Table):
    
    name = "users"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=30)
    id.meta['tip'] = "the user's id"
    id.constraints = "PRIMARY KEY"

    username = pyre.db.varchar(name='username', length=30)
    username.meta['tip'] = "the user's name"
    
    password = pyre.db.varchar(name="password", length=30)
    password.meta['tip'] = "the user's password"

    
class Activity(Table):

    name = "activity"

    import pyre.db

    id = pyre.db.varchar(name="id", length=30)
    id.constraints = "PRIMARY KEY"

    theuser = pyre.db.reference(name="theuser", table=User)
    theuser.meta['tip'] = "the user"

    login_times = pyre.db.integer(name="login_times", default=0)
    login_times.meta['tip'] = "how many times has a user log in"



from pyre.applications.Script import Script


class DbApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        db = pyre.inventory.str('db', default='testdb')
        db.meta['tip'] = 'the database to connect to'

        wipe = pyre.inventory.bool('wipe', default=True)
        wipe.meta['tip'] = 'delete the table before inserting data?'

        create = pyre.inventory.bool('create', default=True)
        create.meta['tip'] = 'create the table before inserting data?'

        dbengine = pyre.inventory.str('dbengine', default = 'psycopg2')
        

    def main(self, *args, **kwds):
        print "database:", self.inventory.db
        print "database manager:", self.db

        self.db.autocommit(True)

        if self.inventory.wipe:
            self.dropTable(User)
            self.dropTable(Activity)

        if self.inventory.wipe or self.inventory.create:
            self.createTable(User)
            self.createTable(Activity)

        # create a user record
        user = User()
        user.id = '0'
        user.username = "aivazis"
        user.password = "mga4demo"

        # store it in the database
        self.save(user)

        # now extract all records and print them
        self.retrieve(User)

        
        # create an activity record
        activity = Activity()
        activity.theuser = user.id
        assert activity.theuser.id == user.id
        activity.theuser = user
        assert activity.theuser.id == user.id
        activity.login_times = 333
        activity.id = 1

        # make sure reference works
        theuser = activity.theuser.dereference( self.db )
        assert theuser.username == user.username
        assert theuser.password == user.password

        # store 
        self.save( activity )

        # retieve activities
        activities = self.retrieve( Activity )

        assert len(activities) == 1
        activity2 = activities[0]

        theuser2 = activity2.theuser.dereference( self.db )
        assert theuser2.username == user.username
        assert theuser2.password == user.password

        # null pointer?
        print "test null reference"
        activity3 = Activity()
        assert activity3.theuser is None

        activity3.theuser = ''
        assert activity3.theuser is None

        self.save(activity3)
        return


    def retrieve(self, table):
        print " -- retrieving from table %r" % table.name
        try:
            records = self.db.fetchall(table)
        except self.db.ProgrammingError, msg:
            print "    retrieve failed:", msg
            return
        else:
            print "    success"

        index = 0
        print records
        for record in records:
            index += 1
            columns = record.getColumnNames()
            s = [ '%s=%s' % (col, record.getColumnValue(col)) for col in columns ]
            s = ', '.join( s )
            print "record %d: %s" % (index, s)

        return records


    def save(self, item):
        print " -- saving into table %r" % item.name
        try:
            self.db.insertRow(item)
        except self.db.ProgrammingError, msg:
            print "    insert failed:", msg
        else:
            print "    success"

        return


    def createTable(self, table):
        # create the user table
        print " -- creating table %r" % table.name
        try:
            self.db.createTable(table)
        except self.db.ProgrammingError, msg:
            print "    failed; table exists?"
            print msg
        else:
            print "    success"

        return


    def dropTable(self, table):
        # drop the user table
        print " -- dropping table %r" % table.name
        try:
            self.db.dropTable(table)
        except self.db.ProgrammingError:
            print "    failed; table doesn't exist?"
        else:
            print "    success"

        return


    def __init__(self):
        Script.__init__(self, 'db')
        self.db = None
        return


    def _init(self):
        Script._init(self)

        import pyre.db
        dbname = self.inventory.db
        dbengine = self.inventory.dbengine
        self.db = pyre.db.connect(dbname, wrapper = dbengine)

        return


def main():
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id: db.py,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $"

# End of file 
