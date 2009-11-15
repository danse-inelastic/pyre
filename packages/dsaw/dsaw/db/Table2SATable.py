# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Table2SATable(object):

    _cache = {}

    def render(self, table, metadata=None):
        if table in self._cache:
            return self._cache[table]

        self._metadata = metadata
        
        self._table = table
        self._props = {}
        class _(object): pass
        self._Object = _
        
        sacols = []
        for colname, descriptor in table._columnRegistry.iteritems():
            sacol = self.dispatch(descriptor)
            sacols.append(sacol)
            continue

        name = table.getTableName()

        satable = sqlalchemy.Table(name, metadata, *sacols)

        from sqlalchemy.orm import mapper
        mapper(self._Object, satable, properties=self._props)

        table._SAObject = self._Object
        
        return satable, self._Object


    def dispatch(self, descriptor):
        name = descriptor.__class__.__name__
        handler = 'on'+name
        handler = getattr(self, handler)
        return handler(descriptor)


    def onReference(self, col):
        name = col.name
        table = col.referred_table
        
        
        tablename = table.getTableName()
        if not hasattr(table, 'primary_key_col'):
            self._cache[table] = Table2SATable().render(table, self._metadata)
            
        pkcol = table.primary_key_col

        from pyre.db.Integer import Integer
        from pyre.db.VarChar import VarChar
        coltypemap = {
            Integer: sqlalchemy.Integer,
            VarChar: sqlalchemy.String,
            }
        coltype = coltypemap[pkcol.__class__]
        
        col = sqlalchemy.Column(
            name, coltype, sqlalchemy.ForeignKey('%s.%s' % (tablename, pkcol.name)))
        return col
    

    def onVersatileReference(self, col):
        name = col.name
        coltype = sqlalchemy.Integer
        from VersatileReference import global_pointer
        tablename = global_pointer.name
        col = sqlalchemy.Column(
            name, coltype, sqlalchemy.ForeignKey('%s.%s' % (tablename, 'id')))
        return col
    

    def onVarChar(self, col):
        name = col.name
        length = col.length
        primary_key = self._isPrimaryKey(col)
        return sqlalchemy.Column(name, sqlalchemy.String(length=length), primary_key=primary_key)


    def onInteger(self, col):
        name = col.name
        primary_key = self._isPrimaryKey(col)
        return sqlalchemy.Column(name, sqlalchemy.Integer, primary_key=primary_key)


    def onReal(self, col):
        name = col.name
        return sqlalchemy.Column(name, sqlalchemy.Float)
    

    def onDate(self, col):
        name = col.name
        return sqlalchemy.Column(name, sqlalchemy.Date)
    

    def onTime(self, col):
        name = col.name
        tz = col.tz
        return sqlalchemy.Column(name, sqlalchemy.DateTime(timezone=tz))
    

    def onBoolean(self, col):
        name = col.name
        return sqlalchemy.Column(name, sqlalchemy.Boolean)


    def onChar(self, col):
        name = col.name
        return sqlalchemy.Column(name, sqlalchemy.CHAR)


    def onTimestamp(self, col):
        name = col.name
        return sqlalchemy.Column(name, sqlalchemy.TIMESTAMP)


    # specific to postgres
    def onDoubleArray(self, col):
        name = col.name
        from sqlalchemy.databases import postgres
        return sqlalchemy.Column(name, postgres.PGArray(postgres.PGFloat))
    

    def onIntegerArray(self, col):
        name = col.name
        from sqlalchemy.databases import postgres 
        return sqlalchemy.Column(name, postgres.PGArray(postgres.PGInteger))
    

    def onVarCharArray(self, col):
        name = col.name
        length = col.length
        from sqlalchemy.databases import postgres 
        return sqlalchemy.Column(name, postgres.PGArray(postgres.PGString(length=length)))
    

    def _isPrimaryKey(self, col):
        if col.constraints and col.constraints.lower().find('primary key')!=-1:
            primary_key = True
        else:
            primary_key = False
        col.primary_key = primary_key
        if primary_key:
            self._table.primary_key_col = col
        return primary_key


import sqlalchemy

def test1():
    from pyre.db.Table import Table
    class User(Table):
        name = 'users'

        import pyre.db
        username = pyre.db.varchar(name='username', length=64)
        username.constraints = 'PRIMARY KEY'
        password = pyre.db.varchar(name='password', length=64)
        
    metadata = sqlalchemy.MetaData()
    satable, saUser = Table2SATable().render(User, metadata)
    return


def test2():
    from pyre.db.Table import Table
    class Job(Table):
        name = 'jobs'

        import pyre.db
        username = pyre.db.varchar(name='username', length=64)

        id = pyre.db.integer(name='id')
        id.constraints = 'PRIMARY KEY'

        runtime = pyre.db.real(name='runtime')

        date_started = pyre.db.date(name='date_started')

        time_started = pyre.db.time(name='time_started')

        active = pyre.db.boolean(name='active')

    metadata = sqlalchemy.MetaData()
    satable, saJob = Table2SATable().render(Job, metadata)
    return


def test3():
    from pyre.db.Table import Table
    import pyre.db, dsaw.db

    class Computation(Table):

        name = 'computations'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        
    class Job(Table):
        
        name = 'jobs'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        computation = dsaw.db.reference(name='computation', table=Computation)

    metadata = sqlalchemy.MetaData()
    
    saComputationTable, saComputation = Table2SATable().render(Computation, metadata)
    saJobTable, saJob = Table2SATable().render(Job, metadata)
    return


def main():
    test1()
    test2()
    test3()
    return

if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
