from enum import Enum


class PaymentMethod(Enum):
    UPI = "UPI"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"


class PaymentValidator:

    @staticmethod
    def validate(amount, payment_method):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        if not isinstance(payment_method, PaymentMethod):
            raise ValueError("Invalid payment method")


class PaymentProcessor:

    FEE_RATES = {
        PaymentMethod.UPI: 0.01,
        PaymentMethod.CARD: 0.02,
        PaymentMethod.BANK_TRANSFER: 0.005,
    }

    def calculate_fee(self, amount, payment_method):
        rate = self.FEE_RATES[payment_method]
        return round(amount * rate, 2)

    def process(self, amount, payment_method):
        PaymentValidator.validate(amount, payment_method)

        fee = self.calculate_fee(amount, payment_method)
        total_amount = amount + fee

        if amount > 1000000:
            status = "pending"
            message = "Manager approval required"
        else:
            status = "approved"
            message = "Payment processed successfully"

        return {
            "status": status,
            "message": message,
            "payment_method": payment_method.value,
            "amount": amount,
            "fee": fee,
            "total_amount": total_amount,
        }


processor = PaymentProcessor()

result = processor.process(
    30000,
    PaymentMethod.UPI
)

print(result)
