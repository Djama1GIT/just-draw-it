import datetime
import sqlite3

try:
    con = sqlite3.connect('chats.db')
    cursor = con.cursor()
    create_query = '''CREATE TABLE chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method INTEGER NOT NULL,
    step INTEGER NOT NULL,
    sizes VARCHAR(10) NOT NULL,
    image TEXT NOT NULL
    );'''
    cursor.execute(create_query)
except Exception as e:
    with open('log.txt', 'a') as log:
        err = f'[{datetime.datetime.now()}] DB Error {e} | Arguments: {e.args}\n'
        print(err)
        log.write(err)
finally:
    if con:
        con.close()
