class Secretary:
    def __init__(self,secretary_id: int, name: str, email: str, phone: str, hire_date: str):
        self.secretary_id = secretary_id
        self.name = name
        self.email = email
        self.phone = phone
        self.hire_date = hire_date

    def manageCourses(self, course_id: int, action: str):
        # Logic to manage courses (open/close)
        if action == "open":
            # Open course logic
            pass
        elif action == "close":
            # Close course logic
            pass
    
    def sendReminderToParent(self, parent_id: int, message: str):
        # Logic to send reminders to parents
        pass

    def manageSchedule(self, student_id: int, action: str):
        # Logic to manage student schedules
        if action == "view":
            # View schedule logic
            pass
        elif action == "update":
            # Update schedule logic
            pass
    
    def generatePaymentReports(self, payment_id: int):
        # Logic to generate payment reports
        pass