from dsaw.db import connect
db = connect(db ='postgres:///test')
db.autocommit(True)

# declare tables
from dsaw.db.WithID import WithID
class SomeClass(WithID):
    
    myattribute = 'cake'
    
    def sayhi(self):
        print 'hi'

db.registerTable(SomeClass)
db.createAllTables()

t1 = SomeClass()
t1.id = 't1'
t1.myattribute = 'bigcake'
db.insertRow(t1)

t1.myattribute = 'biggercake'
db.updateRecord(t1)

db.destroyAllTables()