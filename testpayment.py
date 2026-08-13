class PaymentValidator:
    @staticmethod
    def validate(amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")


class PaymentProcessor:
    def process(self, amount):
        PaymentValidator.validate(amount)

        # New functionality: calculate processing fee
        fee = amount * 0.02
        total_amount = amount + fee

        if amount > 1000000:
            return {
                "status": "pending",
                "message": "Manager approval required",
                "amount": amount,
                "fee": fee,
                "total_amount": total_amount,
            }

        return {
            "status": "approved",
            "amount": amount,
            "fee": fee,
            "total_amount": total_amount,
        }


processor = PaymentProcessor()

result = processor.process(50000)

print(result)
