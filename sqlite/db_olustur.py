import sqlite3


#database'i global bir degisken olarak tanimladık. boylelikle eger bir degisiklik olacaksa burada yapabiliriz
DATABASE = "todo.db" 

def db_olustur():
    conn = db_baglan(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS todo(id INTEGER PRIMARY KEY AUTOINCREMENT, icerik TEXT NOT NULL, yapildimi INTEGER NOT NULL DEFAULT 0)')

    conn.commit()

    #burada tek tek yapsak da, bunları bir dictionary icerisine yazarak for loop ile de eklemek mumkun
    c.execute('INSERT INTO todo(icerik, yapildimi) values (?,?)', ("ekmek al", 0))
    c.execute('INSERT INTO todo(icerik, yapildimi) values (?,?)', ("icecek al", 0))

    conn.commit()
    conn.close()

def db_oku():
    conn = db_baglan(DATABASE)
    c = conn.cursor()
    c.execute('select * from todo')
    rows = c.fetchall()
    conn.close()
    print(rows)

def db_baglan(db_adi):
    conn = sqlite3.connect(db_adi)
    return conn
    
if __name__ == "__main__":
    db_olustur()
    db_oku()
