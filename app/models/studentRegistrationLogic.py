from app.database import connect_db
from datetime import datetime

MAX_STUDENTS_PER_PARENT = 5  # אם יש מגבלה כזו


def parent_can_add_student(parent_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students WHERE parent_id=?", (parent_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count < MAX_STUDENTS_PER_PARENT


def is_student_name_duplicate(parent_id, student_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE parent_id=? AND name=?", (parent_id, student_name))
    exists = cursor.fetchone()
    conn.close()
    return exists is not None


def register_new_student(name, birth_date, parent_id):
    enrollment_date = datetime.now().strftime("%Y-%m-%d")  # תאריך רישום אוטומטי
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students WHERE parent_id=? AND name=?", (parent_id, name))
    if cursor.fetchone()[0] > 0:
        raise Exception("תלמיד בשם זה כבר קיים להורה")

    cursor.execute("""
        INSERT INTO students (name, birth_date, enrollment_date, parent_id)
        VALUES (?, ?, ?, ?)
    """, (name, birth_date, enrollment_date, parent_id))

    student_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return student_id
def get_students_by_parent(parent_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, birth_date, enrollment_date
        FROM students
        WHERE parent_id = ?
    """, (parent_id,))
    students = cursor.fetchall()
    conn.close()
    return students
