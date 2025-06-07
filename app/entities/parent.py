class Parent:
    def __init__(self, parent_id:int, name:str, email: str, phone: str, adress: str, registration_date: str):
        self.parent_id = parent_id
        self.name = name
        self.email = email
        self.phone = phone
        self.adress = adress
        self.registration_date = registration_date
    
    def registerStudentToSystem(self, student_id: int):
        # Logic to register a student to the system
        pass

    def processPayment(self, amount: float):
        # Logic to process payment
        pass

    def trackChildProgress(self, student_id: int):
        # Logic to track child's progress
        pass

    def freezeMembership(self):
        # Logic to freeze membership
        pass

    def unfreezeMembership(self):
        # Logic to unfreeze membership
        pass

    def submitFeedback(self, feedback: str):
        # Logic to submit feedback
        pass

    def enrollStudentToCourse(self, student_id: int, course_id: int):
        # Logic to enroll a student to a course
        pass

    def cancelEnrollment(self, student_id: int, course_id: int):
        # Logic to cancel enrollment
        pass

    def confirmPayment(self, payment_id: int):
        # Logic to confirm payment
        pass

    def waitForParentInput(self):
        # Logic to wait for parent input
        pass