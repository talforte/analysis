class Student:
    def __init__(self, student_id: int, name: str, birthDate: str, parent_id: int, enrollment_date: str):
        self.student_id = student_id
        self.name = name
        self.birthDate = birthDate
        self.parent_id = parent_id
        self.enrollment_date = enrollment_date

    def setLessonReminder(self, lesson_id: int, reminder_time: str):
        # Logic to set a lesson reminder
        pass

    def getNotification(self, notification_id: int):
        # Logic to get a notification
        pass

    def viewSchedule(self):
        # Logic to view schedule
        pass

    def submitFeedback(self, feedback: str):
        # Logic to submit feedback
        pass