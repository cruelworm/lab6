# -*- coding: utf-8 -*-
import MySQLdb

db = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='1234',
    db='first_db'
)

c = db.cursor()
c.execute('insert into office (named,location)VALUES (%s,%s);', ('Sales office', 'Moskow,Lenina, 15/1'))
db.commit()

c.execute('select * from office;')
entries = c.fetchall()
for e in entries:
    print(e)

c.close()
db.close()
