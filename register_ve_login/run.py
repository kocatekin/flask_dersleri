from flask import Flask, render_template, request
import hashlib
import secrets
import sqlite3

app = Flask(__name__)

DATABASE = "user.db"

def tuz_olustur(uzunluk=12):
    return secrets.token_hex(uzunluk // 2)

def db_baglan(db):
    conn = sqlite3.connect(db)
    return conn

def hash_olustur(sifre,tuz):
    return hashlib.sha256((sifre+tuz).encode('utf-8')).hexdigest()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/girisyap')
def girisyap():
    return render_template("girisyap.html")

@app.route('/kayitol')
def kayitol():
    return render_template("kayitol.html")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    sifre = request.form['sifre']
    tuz = tuz_olustur()
    digest = hashlib.sha256((sifre+tuz).encode('utf-8')).hexdigest()
    conn = db_baglan(DATABASE)
    c = conn.cursor()
    c.execute("insert into user(username, sifre, tuz) values (?,?,?)", (username, digest, tuz))
    conn.commit()
    conn.close()
    return "kullanici eklendi"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    sifre = request.form['sifre']
    conn = db_baglan(DATABASE)
    c = conn.cursor()
    c.execute("select tuz,sifre from user where username=?", [username])
    row = c.fetchone()
    tuz = row[0]
    donen_sifre = row[1]
    if(hash_olustur(sifre,tuz) == donen_sifre):
        return "dogru kullanici"
    else:
        return "yanlis k.adi ya da sifre"


if __name__ == "__main__":
    app.run(port=5001, debug=True)
