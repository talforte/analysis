class Teacher:
    def __init__(self, teacher_id: int, name: str, email: str, phone: str, specialization: str, hire_date: str):
        self.teacher_id = teacher_id
        self.name = name
        self.email = email
        self.phone = phone
        self.specialization = specialization
        self.hire_date = hire_date
    
    def markAttendance(self, student_id: int, lesson_id: int):
        # Logic to mark attendance for a student in a lesson
        pass
    def reviewFeedback(self, feedback_id: int):
        # Logic to review feedback from students or parents
        pass
    def updateCourseDetails(self, course_id: int, name: str, description: str, level: str):
        # Logic to update course details
        pass

    def notifyParents(self, parent_id: int, message: str):
        # Logic to notify parents about student progress or issues
        pass

    def cancelAttendance(self, student_id: int, lesson_id: int):
        # Logic to cancel attendance for a student in a lesson
        pass

    def viewStudentList(self, course_id: int):
        # Logic to view the list of students enrolled in a course
        pass

    def openAttendance(self, course_id: int):
        # Logic to open attendance for a course
        pass
