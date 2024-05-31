import sqlite3

conn = sqlite3.connect("user.db")
c = conn.cursor()
c.execute('CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, sifre TEXT NOT NULL, tuz TEXT NOT NULL)')
conn.commit()
conn.close()

          
