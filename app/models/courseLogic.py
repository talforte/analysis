from app.database import connect_db
from datetime import datetime


def is_course_open(course_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM courses WHERE id=?", (course_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def is_student_enrolled(student_id, course_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM enrollments WHERE student_id=? AND course_id=?", (student_id, course_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def register_student_to_course(student_id, course_id):
    if not is_course_open(course_id):
        raise Exception("הקורס לא קיים או סגור לרישום.")

    if is_student_enrolled(student_id, course_id):
        raise Exception("התלמיד כבר רשום לקורס זה.")

    conn = connect_db()
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO enrollments (student_id, course_id, date) VALUES (?, ?, ?)",
                   (student_id, course_id, date))
    enrollment_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return enrollment_id


def does_teacher_teach_course(teacher_id, course_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM schedule
        WHERE teacher_id=? AND course_id=?
    """, (teacher_id, course_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def enroll_student_to_course(student_id, course_id):
    conn = connect_db()
    cursor = conn.cursor()

    # לבדוק אם כבר רשום
    cursor.execute("""
        SELECT COUNT(*) FROM enrollments
        WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id))

    if cursor.fetchone()[0] > 0:
        raise Exception("התלמיד כבר רשום לחוג זה")

    enrollment_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (?, ?, ?)
    """, (student_id, course_id, enrollment_date))

    conn.commit()
    conn.close()

def get_all_courses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            courses.id,
            courses.name,
            courses.time,
            courses.level,
            courses.status,
            teachers.name AS teacher_name
        FROM courses
        JOIN teachers ON courses.teacher_id = teachers.id
    """)
    courses = cursor.fetchall()
    conn.close()
    return courses


def get_student_enrollments(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            enrollments.id AS enrollment_id,
            courses.name,
            courses.time
        FROM enrollments
        JOIN courses ON enrollments.course_id = courses.id
        WHERE enrollments.student_id = ?
    """, (student_id,))
    enrollments = cursor.fetchall()
    conn.close()
    return enrollments



def delete_enrollment(enrollment_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enrollments WHERE id = ?", (enrollment_id,))
    conn.commit()
    conn.close()
