class PaymentValidator:
    @staticmethod
    def validate(amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")


class PaymentProcessor:
    def process(self, amount):
        PaymentValidator.validate(amount)

        if amount > 10000:
            return {
                "status": "pending",
                "message": "Manager approval required",
                "amount": amount,
            }

        return {
            "status": "approved",
            "amount": amount,
        }


processor = PaymentProcessor()

result = processor.process(50000)

print(result)