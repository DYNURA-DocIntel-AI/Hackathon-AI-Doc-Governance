from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    customer_name: str
    amount: float
    status: str = "CREATED"


class OrderService:

    AUTO_APPROVAL_LIMIT = 25_000

    def create_order(self, order: Order):
        print(f"\nCreating order {order.order_id}")
        print(f"Customer: {order.customer_name}")
        print(f"Amount: ₹{order.amount}")

        # Business Rule:
        # Orders below ₹50,000 are automatically approved.
        if order.amount < self.AUTO_APPROVAL_LIMIT:
            order.status = "APPROVED"
            message = "Order automatically approved"

        else:
            order.status = "MANUAL_REVIEW"
            message = "Order requires manual review"

        return {
            "order_id": order.order_id,
            "amount": order.amount,
            "status": order.status,
            "message": message,
        }

    def calculate_discount(self, order: Order):
        """
        Calculate discount based on order amount.

        Business Rules:
        - Orders below ₹10,000 receive no discount.
        - Orders from ₹10,000 to ₹50,000 receive 5%.
        - Orders above ₹50,000 receive 10%.
        """

        if order.amount < 10_000:
            discount_rate = 0

        elif order.amount <= 50_000:
            discount_rate = 0.07

        else:
            discount_rate = 0.10

        discount_amount = order.amount * discount_rate
        final_amount = order.amount - discount_amount

        return {
            "order_id": order.order_id,
            "original_amount": order.amount,
            "discount_rate": discount_rate,
            "discount_amount": discount_amount,
            "final_amount": final_amount,
        }


def main():
    service = OrderService()

    orders = [
        Order(
            order_id="ORD-001",
            customer_name="Rahul",
            amount=25_000,
        ),
        Order(
            order_id="ORD-002",
            customer_name="Priya",
            amount=75_000,
        ),
    ]

    for order in orders:

        result = service.create_order(order)
        print(result)

        discount = service.calculate_discount(order)
        print(discount)


if __name__ == "__main__":
    main()