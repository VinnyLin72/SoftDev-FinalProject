from flask import flash
import sqlite3

from passlib.hash import md5_crypt

DB_FILE = "app.db"

# create table called users
def create_table():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE if not exists users (name TEXT, email TEXT, password TEXT, security_question TEXT, security_answer TEXT)")
    c.execute("CREATE TABLE if not exists events (name TEXT, user TEXT, date TEXT, location TEXT, description TEXT, tags TEXT, people TEXT)")
    db.commit()
    db.close()

# populate tables with example data
def populate_tables():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    hardcoded_vals = [('clara', 'm'), ('jared', 'a'), ('vincet', 'l')]
    for i in hardcoded_vals:
        c.execute("INSERT INTO users VALUES(?, ?)", i)
        print(i)
    params = ("topher", "m")
    c.execute("INSERT INTO users VALUES(?, ?)", params)

    val = ('birthday', 'clara', '02-18-2019', 'nyc', 'my birthday', 'birthday', 'none')
    c.execute("INSERT INTO events VALUES(?, ?, ?, ?, ?, ?, ?)", val)

    db.commit()
    db.close()

# check if username and password combination is valid
def validate_user(email, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    users = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
    if len(users) == 0 or not md5_crypt.verify(password, users[0][2]):
        flash("Username or password incorrect")
        db.close()
        return False
    db.close()
    return True

# returns the user with the given email, None if no user exists
def get_user_by_email(email):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    users = c.fetchall()
    user = None if len(users) == 0 else users[0]
    db.close()
    return user

# add user to database
def add_user(name, email, password, security_question, security_answer):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    password = md5_crypt.hash(password)
    params = (name, email, password, security_question, security_answer)
    c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)", params)
    db.commit()
    db.close()

# get events for certain username
def get_events_by_user(email):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM events WHERE user = ? ORDER BY datetime(date) DESC", (email,)).fetchall()
    db.close()
    return data

def add_event(user, name, desc, date, location, tags, people):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    params = (name, user, date, location, desc, tags, people)
    c.execute("INSERT INTO events VALUES(?, ?, ?, ?, ?, ?, ?)", params)
    db.commit()
    db.close()