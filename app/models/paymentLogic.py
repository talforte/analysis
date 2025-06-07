from app.database import connect_db
from datetime import datetime


def has_paid(enrollment_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM payments WHERE enrollment_id=?", (enrollment_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_payment_details(enrollment_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE enrollment_id=?", (enrollment_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_course_price_by_enrollment(enrollment_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.price
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE e.id = ?
    """, (enrollment_id,))
    result = cursor.fetchone()
    conn.close()
    return result["price"] if result else None


def create_payment(enrollment_id, parent_id, method):
    if has_paid(enrollment_id):
        raise Exception("כבר שולם עבור רישום זה.")

    amount = get_course_price_by_enrollment(enrollment_id)
    if amount is None:
        raise Exception("לא נמצא מחיר לחוג.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "paid"

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO payments (enrollment_id, parent_id, amount, method, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (enrollment_id, parent_id, amount, method, status, timestamp))
    conn.commit()
    conn.close()
    return True
