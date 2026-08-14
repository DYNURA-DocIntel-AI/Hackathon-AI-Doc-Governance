# Project Documentation

## 1. Drift Analysis

### Drift Status

**NO SIGNIFICANT DRIFT** — The previously documented `testpayment.py` business logic, components, and data flow remain unchanged and unaffected by this PR. All prior documentation describing `PaymentValidator` and `PaymentProcessor` continues to accurately reflect the current implementation.

This PR introduces an entirely new, independent file, `order_service.py`, which was not previously documented. Its addition is new functionality rather than a modification of previously documented behavior.

### Minor Drift

* The newly added `order_service.py` contains an inline code comment stating *"Orders below ₹50,000 are automatically approved,"* but the implemented `AUTO_APPROVAL_LIMIT = 25_000` class attribute and the `if order.amount < self.AUTO_APPROVAL_LIMIT` check enforce a ₹25,000 threshold, not ₹50,000. This is an internal code-comment-vs-implementation inconsistency introduced within the same new file. The documentation below treats the **current implemented threshold (₹25,000)** as authoritative, consistent with the PR title and description ("update order approval threshold," "from ₹50,000 to ₹25,000").
* The PR description frames this as an update ("change ... from ₹50,000 to ₹25,000"), but the supplied diff shows `order_service.py` as a wholly new file addition (+61/-0) with no prior tracked version. There is no prior implementation evidenced in this repository to compare against; the ₹50,000 reference exists only in the PR description and the code's own comment, not in any prior documented or tracked code state.

## 2. Overview

This repository, in its current supplied state, contains three notable files:

- `test.txt` — a plain text file with sample content, unrelated to application logic.
- `testpayment.py` — a small Python script implementing basic payment validation and processing logic, including fee calculation and an approval threshold check.
- `order_service.py` — a small standalone Python script implementing basic order creation and an automatic approval/manual-review decision based on an order amount threshold.

There is no evidence of a web framework, server, database, or shared API layer connecting these files in the supplied code. The repository appears to be at an early/prototype stage, containing two independent, self-contained business-logic modules: one for payment processing (`testpayment.py`) and one for order processing (`order_service.py`). The two modules are not evidenced to import from or depend on each other.

## 3. Architecture

The supplied code consists of two standalone Python scripts with no external framework integration, no persistence layer, and no networking code.

**Payment module (`testpayment.py`)** — a simple procedural/object-oriented script composed of two classes:

- `PaymentValidator` — static validation utility.
- `PaymentProcessor` — orchestrates validation and fee/total calculation, returning a result dictionary.

The script executes top-level code that instantiates `PaymentProcessor` and calls `process()` directly when run, printing the result to stdout.

**Order module (`order_service.py`)** — a separate, independent standalone script composed of:

- `Order` — a `@dataclass` representing an order (`order_id`, `customer_name`, `amount`, `status` defaulting to `"CREATED"`).
- `OrderService` — a class with a class attribute `AUTO_APPROVAL_LIMIT = 25_000` and a `create_order(order)` method that prints order details, applies the approval threshold rule, mutates `order.status`, and returns a result dictionary.
- `main()` — a module-level function that instantiates `OrderService`, builds two sample `Order` instances (`ORD-001` at ₹25,000 and `ORD-002` at ₹75,000), calls `create_order()` for each, and prints each result.
- A `if __name__ == "__main__": main()` guard controls script execution.

Both modules are structurally similar (standalone script with classes and top-level/main execution) but are functionally independent — there is no evidence of shared imports, shared state, or cross-module calls.

## 4. APIs

No HTTP APIs, endpoints, or web routes are evidenced in the supplied code. Both modules expose only in-process Python classes/methods (not network-accessible):

- `PaymentValidator.validate(amount)` — static method, not an HTTP API.
- `PaymentProcessor.process(amount)` — instance method, not an HTTP API.
- `OrderService.create_order(order)` — instance method, not an HTTP API. Accepts an `Order` instance and returns a dictionary describing the outcome.

No API documentation applies to either module.

## 5. Business Logic

### 5.1 Payment Processing (`testpayment.py`)

The core business logic implemented in `testpayment.py`:

- **Validation rule**: A payment `amount` must be strictly greater than zero. If `amount <= 0`, a `ValueError` is raised with the message `"Amount must be greater than zero"`.
- **Fee calculation**: A processing fee is computed as `amount * 0.0222` (i.e., 2.22% of the amount).
- **Total amount**: `total_amount = amount + fee`.
- **Approval threshold rule**: If `amount > 1000000`, the payment is not immediately approved — the result status is `"pending"` with the message `"Manager approval required"`.
- **Default approval**: If the amount is within the valid range and does not exceed the threshold, the result status is `"approved"`.

#### Processing Flow

1. `PaymentProcessor.process(amount)` is called with a numeric amount.
2. `PaymentValidator.validate(amount)` checks that `amount > 0`; raises `ValueError` otherwise.
3. Fee and total amount are computed using the fee rate `0.0222`.
4. If `amount > 1000000`, return a `pending` result requiring manager approval.
5. Otherwise, return an `approved` result.

### 5.2 Order Processing (`order_service.py`)

The core business logic implemented in `order_service.py`:

- **Auto-approval threshold rule**: `OrderService.AUTO_APPROVAL_LIMIT = 25_000` (₹25,000). If `order.amount < AUTO_APPROVAL_LIMIT`, the order is automatically approved: `order.status` is set to `"APPROVED"` and the returned message is `"Order automatically approved"`.
- **Manual review rule**: If `order.amount >= AUTO_APPROVAL_LIMIT` (i.e., ₹25,000 or more), `order.status` is set to `"MANUAL_REVIEW"` and the returned message is `"Order requires manual review"`.
- **No amount validation**: There is no check for negative, zero, or non-numeric `amount` values in `create_order` — any such value flows directly into the threshold comparison without raising an error.
- **Status field default**: A newly constructed `Order` defaults to `status = "CREATED"` until `create_order` mutates it to either `"APPROVED"` or `"MANUAL_REVIEW"`.

> **Note (see Drift Analysis):** An inline code comment states the threshold as "below ₹50,000," but the enforced constant and comparison use ₹25,000. The ₹25,000 value is the authoritative, currently implemented behavior.

#### Processing Flow

1. `OrderService.create_order(order)` is called with an `Order` instance.
2. The order ID, customer name, and amount are printed to stdout.
3. If `order.amount < 25_000`, set `order.status = "APPROVED"` and `message = "Order automatically approved"`.
4. Otherwise (`order.amount >= 25_000`), set `order.status = "MANUAL_REVI