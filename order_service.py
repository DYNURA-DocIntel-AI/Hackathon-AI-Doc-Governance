from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    customer_name: str
    amount: float
    status: str = "CREATED"


class OrderService:

    AUTO_APPROVAL_LIMIT = 50_000

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


if __name__ == "__main__":
    main()