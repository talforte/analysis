from app.database import connect_db

def teacher_login(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM teachers WHERE email=? AND password=?", (email, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "name": row[1]}
    return None
def get_teacher_attendance(teacher_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            students.name AS student_name,
            attendance.date,
            attendance.status,
            courses.name AS course_name
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        JOIN courses ON attendance.course_id = courses.id
        WHERE courses.teacher_id = ?
        ORDER BY attendance.date DESC
    """, (teacher_id,))
    results = cursor.fetchall()
    conn.close()
    return results
