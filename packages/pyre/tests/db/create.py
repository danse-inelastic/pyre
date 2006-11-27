#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script


class CreateApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        db = pyre.inventory.str('db', default='testdb')
        db.meta['tip'] = 'the name of the database to build'

        wipe = pyre.inventory.bool("wipe", default=False)
        wipe.meta["tip"] = "delete the database before exiting"


    def main(self, *args, **kwds):
        import psycopg

        # bootstrapping: connect to the template database
        db = psycopg.connect(database='template1')
        db.autocommit(True)
        c = db.cursor()

        # create our database
        print "creating database %r" % self.db
        try:
            c.execute("CREATE DATABASE %s" % self.db)
        except psycopg.ProgrammingError, msg:
            print "error creating databse:", msg

        # get rid of the temporary connection
        c.close()
        db.close()

        # verify we can connect to the new database
        print "connecting to database %r" % self.db
        db = psycopg.connect(database=self.db)
        c = db.cursor()
        # delete our database
        try:
            c.execute("DELETE DATABASE %s" % self.db)
        except psycopg.ProgrammingError, msg:
            print "error deleting databse:", msg

        db.close()

        # drop the database
        if self.inventory.wipe:
            print "deleting database %r" % self.db
            db = psycopg.connect(database='template1')
            db.autocommit(True)
            c = db.cursor()

            try:
                c.execute("DROP DATABASE %s" % self.db)
            except psycopg.ProgrammingError, msg:
                print "error dropping database %r" % self.db
        
        return


    def __init__(self):
        Script.__init__(self, 'create')
        self.db = ''
        return


    def _configure(self):
        Script._configure(self)
        self.db = self.inventory.db
        return


# main
if __name__ == '__main__':
    # invoke the application shell

    app = CreateApp()
    app.run()


# version
__id__ = "$Id: create.py,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $"

# End of file 
