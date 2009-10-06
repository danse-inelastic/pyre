import psycopg2 as ps2
db = ps2.connect("dbname='vnf' user='jbk'")
cursor = db.cursor()
cursor.execute('SELECT * FROM samples')
print cursor.fetchall()