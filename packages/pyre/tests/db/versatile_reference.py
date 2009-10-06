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

class Block(Table):
    
    name = "blocks"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=30)
    id.constraints = "PRIMARY KEY"

    width = pyre.db.real(name='width', default=1.)
    height = pyre.db.real(name='height', default=1.)
    thickness = pyre.db.real(name='thickness', default=1.)
    

class Sphere(Table):
    
    name = "spheres"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=30)
    id.constraints = "PRIMARY KEY"

    radius = pyre.db.real(name='radius', default=1.)
    


import pyre.db
tableRegistry = pyre.db.tableRegistry()
tableRegistry.register( Block )
tableRegistry.register( Sphere )

    
class Sample(Table):

    name = "samples"

    import pyre.db

    id = pyre.db.varchar(name="id", length=30)
    id.constraints = "PRIMARY KEY"

    shape = pyre.db.versatileReference(name="shape", tableRegistry=tableRegistry)



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

        tables = [ Block, Sphere, Sample ]
        
        if self.inventory.wipe:
            for table in tables: self.dropTable( table )

        if self.inventory.wipe or self.inventory.create:
            for table in tables: self.createTable( table )

        # create some shapes
        block = Block()
        block.id = 'abc'
        block.width = 3
        block.height = 4
        block.thickness = 5

        sphere = Sphere()
        sphere.id = 'def'
        sphere.radius = 1001

        # store them in the database
        self.save(block)
        self.save(sphere)

        # now extract all records and print them
        self.retrieve(Block)
        self.retrieve(Sphere)

        
        # create a sample record
        sample = Sample()
        sample.shape = Block, 'abc'
        sample.id = 'sample1'

        # store the sample
        self.save( sample )


        # retieve sample
        samples = self.retrieve( Sample )

        assert len(samples) == 1
        sample2 = samples[0]

        shape = sample2.shape.dereference( self.db )
        assert shape.width == block.width
        assert shape.height == block.height
        assert shape.thickness == block.thickness

        # NULL reference
        sample = Sample()
        assert sample.shape is None
        sample.shape = ''
        assert sample.shape is None
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
