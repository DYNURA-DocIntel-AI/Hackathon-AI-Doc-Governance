class PaymentValidator:
    @staticmethod
    def validate(amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")


class PaymentProcessor:

    def calculate_fee(self, amount):
        """Calculate a 2% processing fee."""
        return amount * 0.02

    def process(self):
        amount = 50000
        PaymentValidator.validate(amount)

        fee = self.calculate_fee(amount)
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
result = processor.process()

print(result)
