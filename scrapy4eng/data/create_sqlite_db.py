import sqlite3
import os

sqlite3DbDir = os.path.dirname(__file__) + '/words.db'

conn = sqlite3.connect(sqlite3DbDir)
print "Opened database successfully";
c = conn.cursor()
c.execute('''CREATE TABLE if NOT EXISTS words
       (id INTEGER PRIMARY KEY     AUTOINCREMENT NOT NULL ,
       word          TEXT     unique NOT NULL ,
       add_time       datetime NOT NULL,
       update_time    datetime NOT NULL,
       view_count     int,
       add_result     int);''')
print "Table created successfully";
conn.commit()
conn.close()