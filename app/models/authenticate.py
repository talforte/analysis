import sqlite3
DB_PATH = 'db/database.db'


def connect_db():
    return sqlite3.connect(DB_PATH)

def login(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM parents WHERE email=? AND password=?", (email, password))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"id": row[0], "name": row[1]}
    return None

def user_exists(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM parents WHERE email=?", (email,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def register_new_parent(name, email, password):
    if user_exists(email):
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO parents (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()
    return True