class Course:
    def __init__(self, course_id: int, teacher_id: int, name: str, description: str, level: str, time: str, status: str):
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.name = name
        self.description = description
        self.level = level
        self.time = time
        self.status = status
    
    def openCourse(self):
        # Logic to open the course for enrollment
        self.status = "open"
    def closeCourse(self):
        # Logic to close the course for enrollment
        self.status = "closed"
    