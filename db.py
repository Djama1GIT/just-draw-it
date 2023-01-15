import datetime
import sqlite3

try:
    con = sqlite3.connect('chats.db')
    cursor = con.cursor()
except Exception as e:
    with open('log.txt', 'a') as log:
        err = f'[{datetime.datetime.now()}] DB Error {e} | Arguments: {e.args}\n'
        print(err)
        log.write(err)
finally:
    if con:
        con.close()
