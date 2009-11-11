#note: one must have a postgres database called 'test'
#before running this

from dsaw.db import connect
db = connect(db ='postgres:///test')
db.autocommit(True)
db.createSystemTables()

from dsaw.db.WithID import WithID
class User(WithID):
    name = 'users'
    username = 'bob'

class Greeting(WithID):
    name = 'greetings'
    greeting = 'hi'
    who = User()
    
db.createTable(User)
db.createTable(Greeting)

# create a user
user = User()
user.username = 'billy'
user.id = 'bob1'
db.insertRow(user)

# create a greeting
greeting = Greeting()
greeting.who = user
greeting.greeting = 'hello'
greeting.id = 'greeting1'
db.insertRow(greeting)

# remove tables
db.dropTable(Greeting)
db.dropTable(User)
db.destroySystemTables()

