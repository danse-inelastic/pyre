from dsaw.db import connect
db = connect(db ='postgres:///test')
db.autocommit(True)

# declare tables
from dsaw.db.WithID import WithID
class AttributeTypeAssignmentTest(WithID):
    name = 'attributetypeassignmenttest'
    
    myattribute = 'cake'
    
    def sayhi(self):
        print 'hi'

db.registerTable(AttributeTypeAssignmentTest)
db.createAllTables()

t1 = AttributeTypeAssignmentTest()
t1.id = 't1'
t1.myattribute = 'bigcake'
db.insertRow(t1)

t1.myattribute = 'biggercake'
db.updateRecord(t1)

db.destroyAllTables()