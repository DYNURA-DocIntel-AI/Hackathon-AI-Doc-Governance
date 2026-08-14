from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    customer_name: str
    amount: float
    status: str = "CREATED"


class OrderService:

    # DRIFT CHANGE #1:
    # Old documented rule: ₹25,000
    # New business rule: ₹50,000
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

        # DRIFT CHANGE #2:
        # New business rule:
        # Orders above ₹100,000 require executive review.
        elif order.amount > 100_000:
            order.status = "EXECUTIVE_REVIEW"
            message = "Order requires executive review"

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
        - Orders from ₹10,000 to ₹50,000 receive 10%.
        - Orders above ₹50,000 receive 10%.

        Note:
        The implementation intentionally differs from the existing
        documentation for drift detection.
        """

        if order.amount < 10_000:
            discount_rate = 0

        elif order.amount <= 50_000:
            # DRIFT CHANGE #3:
            # Old documented rule: 5%
            # Current implementation: 10%
            discount_rate = 0.10

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
    def calculate_shipping_fee(self, order: Order):
    # Old docs: free shipping above ₹25,000
    # Current rule: free shipping above ₹50,000
        return 0 if order.amount >= 50_000 else 500


    def is_priority_order(self, order: Order):
    # Old docs: priority above ₹100,000
    # Current rule: priority above ₹75,000
        return order.amount > 75_000

def main():

    service = OrderService()

    orders = [
        # Below approval threshold
        Order(
            order_id="ORD-001",
            customer_name="Rahul",
            amount=25_000,
        ),

        # Manual review
        Order(
            order_id="ORD-002",
            customer_name="Priya",
            amount=75_000,
        ),

        # Executive review
        Order(
            order_id="ORD-003",
            customer_name="Amit",
            amount=15_000,
        ),
    ]

    for order in orders:

        result = service.create_order(order)
        print(result)

        discount = service.calculate_discount(order)
        print(discount)
        shipping = service.calculate_shipping_fee(order)
        priority = service.is_priority_order(order)

        print({
            "order_id": order.order_id,
            "shipping_fee": shipping,
            "priority": priority,
        })

if __name__ == "__main__":
    main()