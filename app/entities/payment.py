class Payment:
    def __init__(self, payment_id: int, parent_id: int, amount: float, payment_date: str, status: str, enrollment_id: int):
        self.payment_id = payment_id
        self.parent_id = parent_id
        self.amount = amount
        self.payment_date = payment_date
        self.status = status
        self.enrollment_id = enrollment_id

    def processPayment(self):
        # Logic to process payment
        pass
    def getPaymentStatus(self):
        # Logic to get payment status
        return self.status
    
    def sendReceipt(self):
        # Logic to send payment receipt
        pass

    def notifyFailure(self):
        # Logic to notify payment failure
        pass

    def retry(self):
        # Logic to retry payment
        pass

    def waitForPayment(self):
        # Logic to wait for payment confirmation
        pass
    
class PaymentMethod:
    CREDIT = "credit"
    DIRECT_DEBIT = "direct_debit"
    INSTALLMENTS = "installments"