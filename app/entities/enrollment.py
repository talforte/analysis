class Enrollment:
    def __init__(self, status: str, enrollment_date: str, student_id: int, course_id: int):
        self.status = status
        self.enrollment_date = enrollment_date
        self.student_id = student_id
        self.course_id = course_id
    
    def isActive(self):
        if self.status == "active":
            return True
        return False
    
    def cancel(self):
        pass  # Logic to cancel the enrollment

    def getEnrollmentStaatus(self):
        return self.status
    
    def activate(self):
        self.status = "active"
    
    