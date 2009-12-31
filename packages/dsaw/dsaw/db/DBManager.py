#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Table import Table as TableBase


class DBManager(object):


    class IntegrityError(Exception): pass
    class ProgrammingError(Exception): pass

    class RecordStillReferred(Exception): pass


    def getUniqueIdentifierStr(self, record):
        '''return a unique identifier string for a db record which can be used to
        recover the record from database. it will be some sort of combination
        of table name and record id
        '''
        from _reference import reference
        return str(reference(record.id, record.__class__))


    def fetchRecordUsingUniqueIdentifierStr(self, uidstr):
        '''This method is coupled to method "getUniqueIdentifierStr".
        Fetch a record from db using the unique identifier string.
        '''
        from _reference import reference
        name, id = uidstr.split(reference.separator)
        table = self.getTable(name)
        return self.query(table).filter_by(id=id).one()
        
    
    def deleteRecord(self, record):
        import sqlalchemy.exc
        
        from GloballyReferrable import GloballyReferrable
        if isinstance(record, GloballyReferrable):
            # need to delete the global index first
            gptr = record.globalpointer
            gid = gptr and gptr.id
            #
            if gid:
                # there is a global index
                # let us try to remove that reference
                table = record.__class__
                satable = self._tablemap.TableToSATable(table)
                u = satable.update().where("id='%s'" % record.id).values(globalpointer=None)
                conn = self._get_saconnection()
                conn.execute(u)

                from VersatileReference import global_pointer
                try:
                    self.deleteRow(global_pointer, where="id='%s'" % gid)
                except sqlalchemy.exc.IntegrityError:
                    self._sasession.rollback()
                    # bring back the reference
                    u = satable.update().where("id='%s'"%record.id).values(globalpointer=gid)
                    conn.execute(u)
                    raise self.RecordStillReferred, "Unable to delete record %s:%s, it is still referred by someone" % (record.getTableName(), record.id)

        try:
            self.deleteRow(record.__class__, where="id='%s'" % record.id)
        except sqlalchemy.exc.IntegrityError:
            self._sasession.rollback()
            raise self.RecordStillReferred, "Unable to delete record %s:%s, it is still referred by someone" % (record.getTableName(), record.id)

        self.commit()
        return


    def updateRecord(self, record):
        obj = self.recordToObject(record)

        from Reference import Reference
        from VersatileReference import VersatileReference
        from GloballyReferrable import GloballyReferrable

        record_is_globallyreferrable = isinstance(record, GloballyReferrable)
        
        where = None
        assignments = []
        primary_key_col = record.__class__.primary_key_col
        for colname, col in record._columnRegistry.iteritems():

            # globalpointer should not be updatable
            if record_is_globallyreferrable \
               and colname == GloballyReferrable.globalpointer.name: continue

            # if this col is the primary key, then set up "where"
            if col is primary_key_col:
                value = getattr(obj, colname)
                where = "%s='%s'" % (colname, value)
                continue
            value = getattr(obj, colname)
            
            assignment = colname, value
            assignments.append(assignment)
            continue
        self.updateRow(record.__class__, assignments, where=where)
        self.commit()
        return
    

    def insertRow(self, row):
        import sqlalchemy.exc
        try:
            obj = self.recordToObject(row)
            self._sasession.add(obj)
            self._sasession.commit()
            row = self.objectToRecord(obj, record=row)
            self._sasession.commit()
        except sqlalchemy.exc.IntegrityError, e:
            self._sasession.rollback()
            raise self.IntegrityError, str(e)

        # establish global identity if necessary
##         from GloballyReferrable import GloballyReferrable
##         if isinstance(row, GloballyReferrable):
##             gptr = row.globalpointer
##             if not gptr or not gptr.id:
##                 row.establishGlobalPointer(self)
        
        self.commit()
        return row


    def deleteRow(self, table, where=None):
        Object = self._tablemap.TableToObject(table)
        q = self._sasession.query(Object)
        q.filter(where).delete()
        #exec 'q.filter(%s).delete()' % where
        self.commit()
        return


    def updateRow(self, table, assignments, where=None):
        satable = self._tablemap.TableToSATable(table)
        
        opts = {}
        for k,v in assignments:
            opts[k] = v
            continue

        u = satable.update().where(where).values(**opts)
        conn = self._get_saconnection()
        conn.execute(u)

        self.commit()
        return


    def getSystemTables(self):
        from VersatileReference import global_pointer
        import ReferenceSet
        from _system_tables import tables as systables
        return [global_pointer] + list(systables.itertables())


    def createAllTables(self):
        self._sametadata.create_all()
        self.commit()
        #self.createSystemTables()
        #self.createUserTables()
        return


    def createSystemTables(self):
        for table in self.getSystemTables():
            self.createTable(table)
            continue
        return
    

    def createUserTables(self):
        for table in self._tableregistry.itertables():
            self.createTable(table)
            continue
        return
    
        
    def createTable(self, table):
        self.info.log('creating table %s...' % table.getTableName())
        satable = self.convertToSATable(table)

        import sqlalchemy.exc
        try:
            satable.create(bind=self._saengine)
        except sqlalchemy.exc.ProgrammingError, e:
            if str(e).find('already exists') != -1:
                self.info.log('failed to create table %s. Error: %s' % (table.getTableName(), e))
            else:
                raise
        #self._sametadata.create_all(self._saengine)
        self.commit()
        return


    def destroyAllTables(self):
        self.commit()
        self._sametadata.drop_all()
        self.commit()
        # self.destroyUserTables()
        # self.destroySystemTables()
        return


    def destroySystemTables(self):
        import Reference, VersatileReference, ReferenceSet
        from _system_tables import tables as systables
        for table in systables.itertables():
            self.dropTable(table)
            continue

        from VersatileReference import global_pointer
        self.dropTable(global_pointer)
        return


    def destroyUserTables(self):
        for table in self._tableregistry.itertables():
            self.dropTable(table)
            continue
        return        


    def dropTable(self, table):
#        self.commit()
#        try:
#            name = table.name
#        except:
#            name = table.__name__.lower()
        self.info.log('deleting table %s...' % table.getTableName())
        satable = self.convertToSATable(table)
        satable.drop(bind=self._saengine)
        self.commit()
        return


    def iterAllTables(self):
        return self._tableregistry.itertables()


    def getTable(self, name):
        return self._tableregistry.get(name)


    def registerTable(self, table):
        self._tableregistry.register(table)
        self._tablemap.registerTable(table)
        return
        
        
    def commit(self, *args, **kwds):
        return self._sasession.commit()
    

    def fetchall(self, table, where=None):
        if not where:
            return self.query(table).all()
        ret = self.query(table).filter(where).all()
        self.commit()
        return ret


    def query(self, table, **kwds):
        Obj = self._tablemap.TableToObject(table)
        from QueryProxy import QueryProxy
        return QueryProxy(self._sasession.query(Obj,**kwds), self)


    def convertToSATable(self, table):
        return self._tablemap.TableToSATable(table)


    def recordToObject(self, record):
        return self._recordmap.recordToObject(record)
        

    def objectToRecord(self, obj, record=None):
        return self._recordmap.objectToRecord(obj, record=record)
        

    def dereference(self, ref, **kwds):
        return self._deref(ref, **kwds)


    def autocommit(self, autocommit):
        self._sasession.configure(autocommit=autocommit)
        return


    def __init__(self, db='', echo=False, session=None, metadata=None, autocommit=True):
        if not session:
            from sqlalchemy import create_engine
            engine = create_engine(db, echo=echo)
            
            from sqlalchemy.orm import sessionmaker
            Session = sessionmaker(bind=engine)
            session = Session()

        if not metadata:
            from sqlalchemy import MetaData
            metadata = MetaData()

        session.configure(autocommit=autocommit)
        self._sasession = session # instance of sqlalchemy session
        self._saengine = engine
        self._sametadata = metadata
        metadata.bind = engine

        self._tablemap = TableMap(metadata)
        self._recordmap = RecordMap(self._tablemap, self)

        self._deref = DeReferencer(self)
        
        from TableRegistry import TableRegistry
        self._tableregistry = TableRegistry()

        for table in self.getSystemTables():
            self.registerTable(table)
            continue
        
        #
        #import _referenceset
        import journal
        self.info = journal.info('dsaw.db.DBManager')
        self.debug = journal.debug('dsaw.db.DBManager')
        return


    def __del__(self):
        self.commit()
        self._sasession.close()
        return


    def _get_saconnection(self):
        key = '_saconnection'
        if not hasattr(self, key):
            setattr(self, key, self._saengine.connect())
        return getattr(self, key)



from VersatileReference import global_pointer
class DeReferencer(object):


    def __init__(self, db):
        import weakref
        self.db = weakref.ref(db)

        import journal
        self.debug = journal.debug('dsaw.db.DeReferencer')
        return


    def __call__(self, ref, **kwds):
        type = ref.__class__.__name__
        handler = 'on'+type
        return getattr(self, handler)(ref)


    def onstr(self, ref, **kwds):
        from _reference import reference
        tablename, id = ref.split(reference.separator)
        db = self.db()

        try:
            return db.query(db.getTable(tablename)).filter_by(id=id).one()
        except Exception, e:
            self.debug.log(e)
            return


    def onreference(self, ref, **kwds):
        if ref is None: return
        id = ref.id
        if id is None: return

        db = self.db()
        
        table = ref.table
        if isinstance(table, basestring):
            table = db.getTable(table)

        return db.query(table).filter_by(id=id).one()


    def onvreference(self, ref, **kwds):
        id = ref.id
        self.debug.log('onvreference: id=%s'%id)

        if isinstance(id, basestring): return self.onstr(id)
        if id is None: return

        # already a record
        if isinstance(id, TableBase): return id 
        
        # fetch the record in global_pointer table so that
        # we can find out the type of the record this pointer
        # points to
        db = self.db()
        try:
            gptr = db.query(global_pointer).filter_by(id=id).one()
        except:
            raise RuntimeError, 'failed to obtain record (id=%s) in table global_pointers' % id
        
        # type of the record
        type = gptr.type
        # get the table class
        table = db.getTable(type)
        #
        try:
            return db.query(table).filter_by(globalpointer=id).one()
        except:
            import traceback
            raise RuntimeError, 'failed to retrieve record: table %s, globalpointer %s. Traceback:\n%s' % (table.getTableName(), id, traceback.format_exc())


    def onbackref(self, backref, **kwds):
        targetrow = backref.targetrow
        srctable = backref.srctable
        refcolname = backref.refcolname

        opts = {refcolname: targetrow.id}
        opts.update(kwds)

        db = self.db()
        return db.query(srctable).filter_by(**opts).all()


    def onreferenceset(self, rset):
        db = self.db()
        return rset.dereference(db)


    def onNoneType(self, ref):
        assert ref is None
        return None



class RecordMap(object):


    def __init__(self, tablemap, db):
        self._tablemap = tablemap
        self._record2obj_converters = {}
        self._obj2record_converters = {}
        import weakref
        self.db = weakref.ref(db)
        return


    from Table import Table as DBTableBase
    def recordToObject(self, record):
        if isinstance(record, self.DBTableBase):
            converter = self._record2obj_converters.get(record.__class__)
            if not converter: converter = self._createRecord2ObjectConverter(record.__class__)
            return converter(record)
        
        elif self._tablemap.isAMappedObject(record):
            return record
            
        else:
            raise ValueError, '%s(%s)' % (type(record), record)
        
        raise RuntimeError


    def objectToRecord(self, obj, record=None):
        if isinstance(obj, self.DBTableBase):
            return obj

        table = self._tablemap.ObjectToTable(obj.__class__)
        if not record:
            record = table()
                
        for colname, col in table._columnRegistry.iteritems():
            value = getattr(obj, colname)
            col.__set__(record, value)
            continue
            
        return record
    

    class Record2Obj:
        class Skip(Exception):pass
        def __init__(self, Table, Object, db):
            self.converters = {}
            self.Table = Table
            self.Object = Object
            self.db = db
            return
        def setConverter(self, colname, converter):
            self.converters[colname] = converter
            return
        def __call__(self, record):
            assert isinstance(record, self.Table)
            obj = self.Object()
            converters = self.converters
            for name, col in record._columnRegistry.iteritems():
                value = col.__get__(record)
                try:
                    converted = converters[name](value, col, record)
                except self.Skip:
                    continue
                setattr(obj, name, converted) 
                continue

            return obj


        def convertReference(self, ref, col, record):
            if not ref: return
            id = ref.id
            if id is None: return
            return id
        def convertVersatileReference(self, vref, col, record):
            if vref is None: return

            db = self.db()
            
            if isinstance(vref.id, basestring):
                vref.id = db.dereference(vref.id)
                    
            from GloballyReferrable import GloballyReferrable
            if isinstance(vref.id, GloballyReferrable):
                target = vref.id

                # target's globally unique id in global_pointers table
                gptr = target.globalpointer

                # if that id has not been established,
                # establish that
                if gptr is None or not gptr.id:
                    target.establishGlobalPointer(db)
                    gid = target.globalpointer.id
                    col.__set__(record, gid)
                else:
                    gid = gptr.id

                # the value is the gid
                value = gid

            elif isinstance(vref.id, int):
                value = vref.id

            elif vref.id is None:
                return

            else:
                raise ValueError, '%s(%s)' % (vref.__class__.__name__, vref)

            return value
        def convertPrimaryKey(self, value, col, record):
            # if is primary key and user does not assign the primary key any
            # value, skip it
            if not value: raise self.Skip
            return value
        def convertDoubleArray(self, value, col, record):
            if value is None: return
            if col.shape:
                import numpy
                value = numpy.copy(value)
                value.shape = -1,
            return map(float, value)
        def convertIntegerArray(self, value, col, record):
            if col.shape:
                import numpy
                value = numpy.copy(value)
                value.shape = -1,
            return map(int, value)
        def convertVarCharArray(self, value, col, record):
            return map(str, value)

        def convertDefault(self, value, col, record):
            return value
        
                
    def _createRecord2ObjectConverter(self, table):
        from pyre.db.DoubleArray import DoubleArray
        from pyre.db.IntegerArray import IntegerArray
        from pyre.db.VarCharArray import VarCharArray
        from Reference import Reference
        from VersatileReference import VersatileReference, global_pointer
        
        db = self.db
        
        Obj = self._tablemap.TableToObject(table)
        converter = self.Record2Obj(table, Obj, db)

        for name, col in table._columnRegistry.iteritems():
            
            if isinstance(col, VersatileReference):
                converter.setConverter(name, converter.convertVersatileReference)
            elif isinstance(col, Reference):
                converter.setConverter(name, converter.convertReference)
            elif isinstance(col, DoubleArray):
                converter.setConverter(name, converter.convertDoubleArray)
            elif isinstance(col, IntegerArray):
                converter.setConverter(name, converter.convertIntegerArray)
            elif isinstance(col, VarCharArray):
                converter.setConverter(name, converter.convertVarCharArray)
            elif hasattr(col, 'primary_key') and col.primary_key:
                # if is primary key and user does not assign the primary key any
                # value, skip it
                converter.setConverter(name, converter.convertPrimaryKey)
            else:
                converter.setConverter(name, converter.convertDefault)

        self._record2obj_converters[table] = converter
        return converter



class TableMap(object):

    "map pyre db table to sa table, and the other way around"


    def __init__(self, sametadata):
        self.sametadata = sametadata
        
        self._table2sa = {}
        self._sa2table = {}
        self._table2obj = {}
        self._obj2table = {}
        
        from Table2SATable import Table2SATable
        self._table2sa_converter = Table2SATable()
        return


    def registerTable(self, table):
        if table in self._table2sa: return
        
        satable, Object = self._table2sa_converter.render(table, self.sametadata)
        self._table2sa[table] = satable
        self._sa2table[satable] = table
        self._table2obj[table] = Object
        self._obj2table[Object] = table
        return
    

    def TableToSATable(self, table):
        if table not in self._table2sa:
            self.registerTable(table)
        return self._table2sa[table]


    def SATableToTable(self, satable):
        return self._sa2table[satable]


    def TableToObject(self, table):
        if table not in self._table2obj:
            self.registerTable(table)
        return self._table2obj[table]


    def ObjectToTable(self, object):
        return self._obj2table[object]

    
    def isAMappedObject(self, obj):
        for Object in self._table2obj.itervalues():
            if isinstance(obj, Object): return True
            continue
        return False
        

def _getReferences(row):
    ret = []
    for value in row.getValues():
        if isReference(value):
            ret.append(value)
        continue
    return ret


def isReference(candidate):
    from _reference import reference
    return isinstance(candidate, reference)



def testdb():
    return 'postgres:///test-dsawdb'
    return 'sqlite:///test.db'

def test1():
    print 'test1: Create a simple table and test insertRow, deleteRow, fetchall'
    from Table import Table
    class User(Table):
        name = 'users'

        import pyre.db
        username = pyre.db.varchar(name='username', length=64)
        username.constraints = 'PRIMARY KEY'
        password = pyre.db.varchar(name='password', length=64)

    db = DBManager(db=testdb(), echo=False)
    db.createTable(User)

    user = User()
    user.username = 'linjiao'
    user.password = 'xxxx'

    db.insertRow(user)
    
    users = db.fetchall(User)
    user1 = users[0]
    #print user1.username, user1.password
    
    db.deleteRow(User, where="username='linjiao'")

    users = db.fetchall(User)
    assert len(users) == 0

    db.dropTable(User)
    return


def test2():
    print 'test2: simple query'
    from Table import Table
    class Physicist(Table):
        name = 'physicists'

        import pyre.db
        id = pyre.db.integer(name='id')
        id.constraints = 'PRIMARY KEY'

        firstname = pyre.db.varchar(name='firstname', length=64)
        lastname = pyre.db.varchar(name='lastname', length=64)
        

    db = DBManager(db=testdb(), echo=False)
    db.createTable(Physicist)

    mariecurie = Physicist()
    mariecurie.firstname = 'Marie'
    mariecurie.lastname = 'Curie'
    db.insertRow(mariecurie)

    pierrecurie = Physicist()
    pierrecurie.firstname = 'Pierre'
    pierrecurie.lastname = 'Curie'
    db.insertRow(pierrecurie)
    
    alberteinstein = Physicist()
    mariecurie.firstname = 'Albert'
    mariecurie.lastname = 'Einstein'
    db.insertRow(alberteinstein)

    physicists = db.fetchall(Physicist)
    assert len(physicists) == 3
    
    curies = db.query(Physicist).filter_by(lastname='Curie').all()
    assert len(curies) == 2

    db.deleteRow(Physicist, where="lastname='Curie'")
    
    physicists = db.fetchall(Physicist)
    assert len(physicists) == 1

    db.dropTable(Physicist)
    return


def test3():
    print 'test3: reference'
    
    from Table import Table
    import pyre.db, dsaw.db

    class Computation(Table):

        name = 'computations'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        
    class Job(Table):
        
        name = 'jobs'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        from Reference import Reference
        computation = Reference(name='computation', table=Computation, backref="jobs")

    db = DBManager(db=testdb(), echo=False)
    db.createTable(Computation)
    db.createTable(Job)

    computation = Computation()
    computation.id = 'testcomputation'

    job = Job()
    job.id = 'testjob'
    #db.insertRow(job)
    #db.commit()
    
    job.computation = computation

    db.insertRow(computation)
    db.commit()
    
    db.insertRow(job)
    db.commit()

    jobs = db.fetchall(Job)
    job0 = jobs[0]
    computation = job0.computation.dereference(db)
    assert computation.id == 'testcomputation'

    jobs1 = computation.jobs.dereference(db)
    assert jobs1[0].id == 'testjob'

    db.dropTable(Job)
    db.dropTable(Computation)
    return


def test4():
    print 'test4: versatile reference'
    
    from Table import Table
    from GloballyReferrable import GloballyReferrable
    import pyre.db, dsaw.db

    class Comp1(GloballyReferrable):

        name = 'comp1s'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        
    class Comp2(GloballyReferrable):

        name = 'comp2s'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        
    class GJob(Table):
        
        name = 'gjobs'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        from VersatileReference import VersatileReference
        computation = VersatileReference(name='computation')

    tables = [Comp1, Comp2, GJob]
    
    db = DBManager(db=testdb(), echo=False)

    for t in tables: db.registerTable(t)
    db.createAllTables()

    comp1a = Comp1()
    comp1a.id = 'comp1a'
    comp1ac = db.insertRow(comp1a)
    assert comp1ac.id==comp1a.id

    gjob1 = GJob()
    gjob1.id = 'gjob1'
    gjob1.computation = comp1a

    db.insertRow(gjob1)

    gjobs = db.fetchall(GJob)
    gjob0 = gjobs[0]
    computation = gjob0.computation.dereference(db)
    assert computation.id == comp1a.id

    jobs1 = computation.getReferences(db, table=GJob, refname='computation')
    assert jobs1[0].id == gjob1.id

    db.destroyAllTables()
    return


def test5():
    print 'test5: reference set'
    
    from Table import Table
    from GloballyReferrable import GloballyReferrable
    import pyre.db, dsaw.db

    db = DBManager(db=testdb(), echo=False)

    class Instrument(GloballyReferrable):
        name = 'instruments'
        id = dsaw.db.varchar(name='id', length=64)
        id.constraints = 'PRIMARY KEY'

        from ReferenceSet import ReferenceSet
        components = ReferenceSet(name='components')
        
    class Guide(GloballyReferrable):
        name = 'guides'
        id = dsaw.db.varchar(name='id', length=64)
        id.constraints = 'PRIMARY KEY'
        
    class Monitor(GloballyReferrable):
        name = 'monitors'
        id = dsaw.db.varchar(name='id', length=64)
        id.constraints = 'PRIMARY KEY'

    tables = [Instrument, Guide, Monitor]
    for table in tables: db.registerTable(table)
    
    db.createAllTables()

    guide1 = Guide()
    guide1.id = 'guide1'
    
    monitor1 = Monitor()
    monitor1.id = 'monitor1'

    instrument1 = Instrument()
    instrument1.id = 'instrument1'

    db.insertRow(guide1)
    db.insertRow(monitor1)
    db.insertRow(instrument1)
    
    instrument1.components.add(guide1, db)
    instrument1.components.add(monitor1, db)
    db.commit()

    components = instrument1.components.dereference(db)
    (l1,c1), (l2,c2) = components
    assert c1.id == guide1.id
    assert c2.id == monitor1.id

    instrument1.components.clear(db)
    db.commit()
    components = instrument1.components.dereference(db)
    assert len(components)==0

    guide1 = instrument1.components.add(guide1, db)
    monitor1 = instrument1.components.add(monitor1, db)
    db.commit()

    instrument1.components.delete(guide1, db)
    db.commit()
    components = instrument1.components.dereference(db)
    assert len(components)==1
    (l1,c1), = components
    assert c1.id == monitor1.id

    instrument1.components.insert(guide1, before=monitor1, db=db)
    db.commit()
    components = instrument1.components.dereference(db)
    assert len(components)==2
    (l1,c1), (l2,c2) = components
    assert c1.id == guide1.id
    assert c2.id == monitor1.id

    db.destroyAllTables()
    return


def test6():
    print 'test6: versatile reference and deleteRecord'

    from Table import Table
    from GloballyReferrable import GloballyReferrable
    import pyre.db, dsaw.db

    class Comp1(GloballyReferrable):

        name = 'comp1s'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        
    class Comp2(GloballyReferrable):

        name = 'comp2s'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        
    class GJob(Table):
        
        name = 'gjobs'

        id = pyre.db.varchar(name='id', length=100)
        id.constraints = 'PRIMARY KEY'

        from VersatileReference import VersatileReference
        computation = VersatileReference(name='computation')

    
    db = DBManager(db=testdb(), echo=False)

    tables = [Comp1, Comp2, GJob]
    for table in tables:
        db.registerTable(table)
    db.createAllTables()

    comp1a = Comp1()
    comp1a.id = 'comp1a'
    comp1ac = db.insertRow(comp1a)
    assert comp1ac.id==comp1a.id

    gjob1 = GJob()
    gjob1.id = 'gjob1'
    gjob1.computation = comp1a

    db.insertRow(gjob1)

    try:
        db.deleteRecord(comp1a)
    except db.RecordStillReferred:
        # good this throws
        pass
    else:
        raise RuntimeError, "should throw RecordStillReferred"

    db.commit()

    db.deleteRecord(gjob1)
    db.commit()
    db.deleteRecord(comp1a)
    db.commit()

    db.destroyAllTables()
    return




def main():
    import journal
    # journal.debug('dsaw.db.VersatileReference').activate()
    # journal.debug('dsaw.db.DeReferencer').activate()
    # journal.info('dsaw.db.DBManager').activate()
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    return

if __name__ == '__main__': main()

    
# version
__id__ = "$Id$"

# End of file 
