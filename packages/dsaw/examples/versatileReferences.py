import dsaw.db

db = dsaw.db.connect(db='postgres:///test')
db.autocommit(True)
    
print 'declare tables'
from dsaw.db.WithID import WithID
from dsaw.db.GloballyReferrable import GloballyReferrable
class Cylinder(WithID, GloballyReferrable):
    radius = 1.0
    height = 2.0
    
class Sphere(WithID, GloballyReferrable):
    radius = 1.1
    
class Scatterer(WithID):
    shape = dsaw.db.versatileReference(name='shape')
    
tables = [
    Sphere, Cylinder,
    Scatterer,
    ]
for table in tables:
    db.registerTable(table)
    
db.createAllTables()

print 'insert records'
sphere1 = Sphere()
sphere1.id = 'sphere1'
sphere1.radius = 10.

cylinder1 = Cylinder()
cylinder1.id = 'cylinder1'
cylinder1.radius = 5
cylinder1.height = 10

scatterer1 = Scatterer()
scatterer1.id = 'scatterer1'
scatterer1.shape = sphere1

rows = [
    sphere1, cylinder1,
    scatterer1,
    ]
for row in rows: db.insertRow(row)

def assertEqual(first, second):
    """Fail if the two objects are unequal as determined by the '=='
       operator.
    """
    if not first == second:
        raise Exception, ('%r != %r' % (first, second))

print 'dereference'
shape1 = scatterer1.shape.dereference(db)
assertEqual( shape1.__class__, sphere1.__class__)
assertEqual(shape1.id, sphere1.id)

print 'fetch from db'
rows = db.fetchall(Scatterer, where="id='%s'" % scatterer1.id)
assertEqual(len(rows), 1)
scatterer1r = rows[0]
assertEqual(scatterer1r.shape.id, sphere1.globalpointer.id)

def assertRaises(excClass, callableObj, *args, **kwargs):
    """Fail unless an exception of class excClass is thrown
       by callableObj when invoked with arguments args and keyword
       arguments kwargs. If a different type of exception is
       thrown, it will not be caught, and the test case will be
       deemed to have suffered an error, exactly as for an
       unexpected exception.
    """
    try:
        callableObj(*args, **kwargs)
    except excClass:
        return
    else:
        if hasattr(excClass,'__name__'): excName = excClass.__name__
        else: excName = str(excClass)
        raise Exception, "%s not raised" % excName

print "make sure we don't create dangling reference"
assertRaises(db.RecordStillReferred, db.deleteRecord, sphere1)

print 'updateRecord: switch to a different type of shape'
scatterer1.shape = cylinder1
db.updateRecord(scatterer1)
shape1 = scatterer1.shape.dereference(db)
assertEqual( shape1.__class__, cylinder1.__class__)
assertEqual(shape1.id, cylinder1.id)

print 'updateRecord 2: switch to a different type of shape by using a string'
scatterer1.shape = 'sphere###sphere1'
db.updateRecord(scatterer1)
shape1 = scatterer1.shape.dereference(db)
assertEqual(shape1.__class__, sphere1.__class__)
assertEqual(shape1.id, sphere1.id)

print 'remove tables'
db.destroyAllTables()