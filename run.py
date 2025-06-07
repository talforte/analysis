from flask import Flask, render_template, request, redirect, session, url_for, flash
from datetime import timedelta,datetime
from app.database import init_db, connect_db
from app.models import authenticate, studentRegistrationLogic, courseLogic
from app.models.courseLogic import enroll_student_to_course, get_all_courses, get_student_enrollments, delete_enrollment
from app.models.studentRegistrationLogic import get_students_by_parent
from app.models.teacherLogic import teacher_login, get_teacher_attendance
app = Flask(__name__)
app.secret_key = "your_secret_key"  # החלף לסיסמה אמיתית
app.permanent_session_lifetime = timedelta(minutes=30)

# ---------- דף התחברות ----------
@app.route("/")
def home():
    return redirect(url_for("select_user_type"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = authenticate.login(email, password)

        if user:
            session["parent_id"] = user["id"]
            session["parent_name"] = user["name"]
            return redirect(url_for("dashboard"))
        else:
            flash("פרטי התחברות שגויים")
            return redirect(url_for("login"))

    return render_template("login.html")


# ---------- דשבורד לאחר התחברות ----------

@app.route("/dashboard")
def dashboard():
    if "parent_id" not in session:
        return redirect(url_for("login"))

    parent_id = session["parent_id"]
    conn = connect_db()
    cursor = conn.cursor()

    # שליפת שם ההורה
    cursor.execute("SELECT name FROM parents WHERE id = ?", (parent_id,))
    parent = cursor.fetchone()
    parent_name = parent["name"] if parent else "הורה"

    # שליפת התלמידים
    cursor.execute("""
        SELECT id, name, birth_date, enrollment_date, gender
        FROM students
        WHERE parent_id = ?
    """, (parent_id,))
    students = cursor.fetchall()

    # המרה ל־dict והוספת חוגים
    students_dicts = []
    for student in students:
        student_dict = dict(student)
        cursor.execute("""
            SELECT courses.name, courses.time, courses.date, courses.level, courses.status, teachers.name AS teacher_name
            FROM enrollments
            JOIN courses ON enrollments.course_id = courses.id
            JOIN teachers ON courses.teacher_id = teachers.id
            WHERE enrollments.student_id = ?
        """, (student["id"],))
        courses = cursor.fetchall()
        student_dict["courses"] = [dict(course) for course in courses]
        students_dicts.append(student_dict)

    conn.close()

    return render_template("dashboard.html", parent_name=parent_name, students=students_dicts)




# ---------- רישום תלמיד חדש ----------
@app.route("/register_student", methods=["GET", "POST"])
def register_student():
    if "parent_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name")
        birth_date = request.form.get("birth_date")
        gender = request.form.get("gender")  # ⬅️ הכנס כאן
        parent_id = session["parent_id"]
        enrollment_date = datetime.today().strftime("%Y-%m-%d")

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students (name, birth_date, gender, parent_id, enrollment_date)
            VALUES (?, ?, ?, ?, ?)
        """, (name, birth_date, gender, parent_id, enrollment_date))

        conn.commit()
        conn.close()

        flash("התלמיד נרשם בהצלחה!")
        return redirect(url_for("dashboard"))

    return render_template("register_student.html")


# ---------- התנתקות ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/enroll/<int:student_id>", methods=["GET", "POST"])
def enroll(student_id):
    if "parent_id" not in session:
        return redirect(url_for("login"))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        flash("התלמיד לא נמצא")
        return redirect(url_for("dashboard"))

    student_name = student["name"]

    if request.method == "POST":
        course_id = request.form["course_id"]

        try:
            enroll_student_to_course(student_id, course_id)
            flash(f"התלמיד {student_name} נרשם בהצלחה לחוג!")
        except Exception as e:
            flash(str(e))

        

    courses = get_all_courses()
    enrollments = get_student_enrollments(student_id)
    return render_template("enroll_course.html", student_id=student_id, student_name=student_name,
                       courses=courses, enrollments=enrollments)

@app.route("/unenroll/<int:enrollment_id>/<int:student_id>",methods=["POST"])
def unenroll(enrollment_id, student_id):
    if "parent_id" not in session:
        return redirect(url_for("login"))

    delete_enrollment(enrollment_id)
    flash("ההרשמה לחוג הוסרה בהצלחה.")
    return redirect(url_for("enroll", student_id=student_id))

@app.route("/teacher_login", methods=["GET", "POST"])
def teacher_login_route():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM teachers WHERE email = ? AND password = ?", (email, password))
        teacher = cursor.fetchone()
        conn.close()

        if teacher:
            session["teacher_id"] = teacher["id"]
            session["teacher_name"] = teacher["name"]
            return redirect(url_for("teacher_dashboard"))
        else:
            flash("פרטי התחברות שגויים")

    return render_template("teacher_login.html")


@app.route("/teacher_dashboard")
def teacher_dashboard():
    if "teacher_id" not in session:
        return redirect(url_for("teacher_login_route"))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, level, time, date FROM courses WHERE teacher_id = ?", (session["teacher_id"],))
    courses = cursor.fetchall()
    conn.close()

    return render_template("teacher_dashboard.html", teacher_name=session["teacher_name"], courses=courses)

@app.route("/select_user_type")
def select_user_type():
    return render_template("select_user_type.html")

@app.route("/teacher/course/<int:course_id>")
def teacher_course_view(course_id):
    if "teacher_id" not in session:
        return redirect(url_for("teacher_login_route"))

    conn = connect_db()
    cursor = conn.cursor()

    # בדיקה אם הקורס שייך למורה
    cursor.execute("SELECT name FROM courses WHERE id = ? AND teacher_id = ?", (course_id, session["teacher_id"]))
    course = cursor.fetchone()

    if not course:
        flash("הקורס לא נמצא או שאינך מלמד בו.")
        return redirect(url_for("teacher_dashboard"))

    # שליפת התלמידים הרשומים
    cursor.execute("""
        SELECT s.id, s.name, s.birth_date, s.enrollment_date, e.id AS enrollment_id
        FROM enrollments e
        JOIN students s ON e.student_id = s.id
        WHERE e.course_id = ?
    """, (course_id,))
    students = cursor.fetchall()
    conn.close()

    return render_template("teacher_course_view.html",
                           course_name=course["name"],
                           students=students,
                           course_id=course_id)
@app.route("/teacher/attendance_history")
def teacher_attendance_history():
    if "teacher_id" not in session:
        return redirect(url_for("login"))

    teacher_id = session["teacher_id"]
    student_name = request.args.get("student_name", "")
    parent_name = request.args.get("parent_name", "")
    course_name = request.args.get("course_name", "")
    teacher_name = request.args.get("teacher_name", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    conn = connect_db()
    cursor = conn.cursor()

    query = """
        SELECT 
            students.name AS student_name,
            parents.name AS parent_name,
            attendance.date,
            attendance.status,
            courses.name AS course_name,
            teachers.name AS teacher_name
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        JOIN enrollments ON enrollments.student_id = students.id
        JOIN parents ON students.parent_id = parents.id
        JOIN courses ON attendance.course_id = courses.id
        JOIN teachers ON courses.teacher_id = teachers.id
        WHERE courses.teacher_id = ?
    """
    params = [teacher_id]

    if student_name:
        query += " AND students.name = ?"
        params.append(student_name)
    if parent_name:
        query += " AND parents.name = ?"
        params.append(parent_name)
    if course_name:
        query += " AND courses.name = ?"
        params.append(course_name)
    if teacher_name:
        query += " AND teachers.name = ?"
        params.append(teacher_name)
    if start_date:
        query += " AND attendance.date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND attendance.date <= ?"
        params.append(end_date)

    query += " ORDER BY attendance.date DESC"
    cursor.execute(query, params)
    attendance = cursor.fetchall()
    conn.close()

    return render_template(
        "teacher_attendance_history.html",
        attendance=attendance
    )






@app.route("/teacher/unenroll/<int:enrollment_id>/<int:course_id>")
def teacher_unenroll(enrollment_id, course_id):
    if "teacher_id" not in session:
        return redirect(url_for("teacher_login_route"))

    delete_enrollment(enrollment_id)
    flash("התלמיד הוסר מהקורס בהצלחה.")
    return redirect(url_for("teacher_course_view", course_id=course_id))
@app.route("/teacher/course/<int:course_id>/attendance", methods=["GET", "POST"])
def take_attendance(course_id):
    if "teacher_id" not in session:
        return redirect(url_for("teacher_login_route"))

    conn = connect_db()
    cursor = conn.cursor()

    # בדיקת קורס שייך למורה
    cursor.execute("SELECT name FROM courses WHERE id = ? AND teacher_id = ?", (course_id, session["teacher_id"]))
    course = cursor.fetchone()
    if not course:
        flash("אין גישה לקורס הזה.")
        return redirect(url_for("teacher_dashboard"))

    # טופס שליחה
    if request.method == "POST":
        date = request.form["date"]
        for key in request.form:
            if key.startswith("status_"):
                student_id = int(key.replace("status_", ""))
                status = request.form[key]
                cursor.execute("""
                    INSERT INTO attendance (student_id, course_id, date, status)
                    VALUES (?, ?, ?, ?)
                """, (student_id, course_id, date, status))
        conn.commit()
        conn.close()
        flash("הנוכחות נשמרה בהצלחה!")
        return redirect(url_for("teacher_course_view", course_id=course_id))

    # טופס הצגה
    cursor.execute("""
        SELECT s.id, s.name
        FROM enrollments e
        JOIN students s ON e.student_id = s.id
        WHERE e.course_id = ?
    """, (course_id,))
    students = cursor.fetchall()
    conn.close()

    return render_template("take_attendance.html", course_name=course["name"], course_id=course_id, students=students)
@app.route("/mark_attendance/<int:course_id>", methods=["POST"])
def mark_attendance(course_id):
    if "teacher_id" not in session:
        return redirect(url_for("login"))

    # קבלת תאריך מהטופס
    attendance_date = request.form.get("date")
    if not attendance_date:
        flash("יש לבחור תאריך נוכחות.")
        return redirect(url_for("take_attendance", course_id=course_id))

    conn = connect_db()
    cursor = conn.cursor()

    # שליפת כל התלמידים של הקורס
    cursor.execute("""
        SELECT students.id
        FROM students
        JOIN enrollments ON students.id = enrollments.student_id
        WHERE enrollments.course_id = ?
    """, (course_id,))
    students = cursor.fetchall()

    for student in students:
        student_id = student["id"]
        status = request.form.get(f"status_{student_id}")

        if status:
            # בדיקה אם קיימת כבר נוכחות לאותו תאריך
            cursor.execute("""
                SELECT * FROM attendance
                WHERE student_id = ? AND course_id = ? AND date = ?
            """, (student_id, course_id, attendance_date))
            existing = cursor.fetchone()

            if not existing:
                cursor.execute("""
                    INSERT INTO attendance (student_id, course_id, date, status)
                    VALUES (?, ?, ?, ?)
                """, (student_id, course_id, attendance_date, status))

    conn.commit()
    conn.close()

    flash("הנוכחות נשמרה בהצלחה.")
    return redirect(url_for("teacher_course_view", course_id=course_id))

@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    if "parent_id" not in session:
        return redirect(url_for("login"))

    conn = connect_db()
    cursor = conn.cursor()

    # מחיקת התלמיד (אפשר להוסיף מחיקת הרשמות אם תרצה)
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    flash("התלמיד נמחק בהצלחה.")
    return redirect(url_for("dashboard"))

# ---------- הפעלת השרת ----------
if __name__ == "__main__":
    init_db()  # פונקציה לאתחול בסיס הנתונים אם יש צורך
    app.run(debug=True)
