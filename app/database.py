import sqlite3
import os

DB_PATH = 'db/database.db'


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if not os.path.exists('db'):
        os.makedirs('db')

    conn = connect_db()
    cursor = conn.cursor()

    # Update the table definitions based on the properties of the classes in entities/
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            registration_date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT,
            birth_date TEXT NOT NULL,
            parent_id INTEGER,
            enrollment_date TEXT NOT NULL,
            FOREIGN KEY(parent_id) REFERENCES parents(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            level TEXT,
            time TEXT,
            date TEXT,
            status TEXT
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO courses (teacher_id, name, description, level, time,date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (1, "בלט קלאסי", "חוג תנועה לילדות", "מתחילים", "17:00","שלישי", "פתוח"),
            (2, "קרב מגע", "הגנה עצמית ואימון", "בינוני", "18:30","רביעי", "פתוח"),
            (3, "ציור חופשי", "אמנות יצירתית", "כל הרמות", "16:00","שישי", "פתוח")
        ])


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            enrollment_date TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_id INTEGER,
            parent_id INTEGER,
            amount REAL,
            method TEXT,
            status TEXT,
            timestamp TEXT,
            FOREIGN KEY(enrollment_id) REFERENCES enrollments(id),
            FOREIGN KEY(parent_id) REFERENCES parents(id)
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM parents")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO parents (id,name, email, password) VALUES (?,?, ?, ?)",
                    (1,"דנה לוי", "dana@example.com", "1234"))

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")
    cursor.execute("SELECT COUNT(*) FROM teachers")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO teachers (id,name, email, password) VALUES (?,?, ?, ?)",
                    (2,"ברכה סביל", "savil@example.com", "1234"))
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(course_id) REFERENCES courses(id)
    )
""")

    conn.commit()
    conn.close()


