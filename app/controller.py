import sqlite3
from database import connect_db
DB_PATH = 'db/database.db'

from entities.parent import Parent
from entities.teacher import Teacher
from entities.payment import Payment
from entities.student import Student
from entities.enrollment import Enrollment
from entities.course import Course


from models import courseLogic
from models import studentRegistrationLogic
from models import paymentLogic




def enroll_existing_student(student_id, course_id):
    return courseLogic.register_student_to_course(student_id, course_id)

def check_teacher_course_relation(teacher_id, course_id):
    return courseLogic.does_teacher_teach_course(teacher_id, course_id)

def create_student_for_parent(name, age, parent_id):
    return studentRegistrationLogic.register_new_student(name, age, parent_id)

def pay_for_enrollment(enrollment_id, parent_id, method):
    return paymentLogic.create_payment(enrollment_id, parent_id, method)

def get_payment_info(enrollment_id):
    return paymentLogic.get_payment_details(enrollment_id)
