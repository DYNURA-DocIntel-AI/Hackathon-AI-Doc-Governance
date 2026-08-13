class PaymentValidator:
    @staticmethod
    def validate(amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")


class PaymentProcessor:
    def process(self, amount):
        PaymentValidator.validate(amount)

        # NEW: Apply a 2% transaction fee
        fee = amount * 0.02
        total_amount = amount + fee

        if amount > 100000:
            return self._pending(
                amount,
                fee,
                total_amount,
            )

        return self._approved(
            amount,
            fee,
            total_amount,
        )

    def _pending(self, amount, fee, total_amount):
        return {
            "status": "pending",
            "message": "Manager approval required",
            "amount": amount,
            "fee": fee,
            "total_amount": total_amount,
        }
        

    def _approved(self, amount, fee, total_amount):
        return {
            "status": "approved",
            "amount": amount,
            "fee": fee,
            "total_amount": total_amount,
        }


processor = PaymentProcessor()

result = processor.process(50000)
print(result)