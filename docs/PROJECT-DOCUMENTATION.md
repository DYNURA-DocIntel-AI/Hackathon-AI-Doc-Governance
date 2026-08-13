# Project Documentation

## 1. Overview

This repository, in its current supplied state, contains the following files relevant to application logic:

- `test.txt` — a plain text file with sample content, unrelated to application logic.
- `payment.py` — a small Python script implementing payment validation and processing logic, including payment-method-aware fee calculation, an approval threshold check, and payment-method validation via an `Enum`. (Note: earlier documentation referred to this script as `testpayment.py`; the currently supplied change set modifies a file named `payment.py` with the same `PaymentValidator`/`PaymentProcessor` structure. This appears to be the same module evolved/renamed; the rename itself is not explicitly evidenced in the supplied diff, so it is noted here as inferred.)

There is no evidence of a web framework, server, database, or API layer in the supplied code. The repository appears to be at an early/prototype stage, with `payment.py` demonstrating payment-processing business logic that now supports multiple payment methods with differentiated fee rates.

## 2. Architecture

The supplied code consists of a single standalone Python script with no external framework integration, no persistence layer, and no networking code. The architecture is a simple procedural/object-oriented script composed of:

- `PaymentMethod` — an `Enum` defining the supported payment methods (`UPI`, `CARD`, `BANK_TRANSFER`).
- `PaymentValidator` — static validation utility, now validating both the amount and the payment method.
- `PaymentProcessor` — orchestrates validation, computes a payment-method-specific fee via `calculate_fee`, computes the total amount, and returns a result dictionary including status, message, and payment method.

The script executes top-level code that instantiates `PaymentProcessor` and calls `process()` directly when run, passing an amount and a `PaymentMethod` value, and printing the result to stdout.

## 3. APIs

No HTTP APIs, endpoints, or web routes are evidenced in the supplied code. `payment.py` exposes only in-process Python classes/methods (not network-accessible):

- `PaymentValidator.validate(amount, payment_method)` — static method, not an HTTP API.
- `PaymentProcessor.calculate_fee(amount, payment_method)` — instance method, not an HTTP API.
- `PaymentProcessor.process(amount, payment_method)` — instance method, not an HTTP API.

No API documentation applies.

## 4. Business Logic

The core business logic is implemented in `payment.py`:

- **Payment methods**: Supported payment methods are defined by the `PaymentMethod` enum: `UPI`, `CARD`, and `BANK_TRANSFER`.
- **Validation rule (amount)**: A payment `amount` must be strictly greater than zero. If `amount <= 0`, a `ValueError` is raised with the message `"Amount must be greater than zero"`.
- **Validation rule (payment method)**: The `payment_method` argument must be an instance of the `PaymentMethod` enum. If it is not, a `ValueError` is raised with the message `"Invalid payment method"`.
- **Fee calculation (payment-method-specific)**: The processing fee is computed based on the payment method via `PaymentProcessor.FEE_RATES`:
  - `UPI`: `1%` (`0.01`)
  - `CARD`: `2%` (`0.02`)
  - `BANK_TRANSFER`: `0.5%` (`0.005`)

  The fee is computed as `round(amount * rate, 2)`, where `rate` is looked up from `FEE_RATES` using the given `payment_method`.
- **Total amount**: `total_amount = amount + fee`.
- **Approval threshold rule**: If `amount > 1,000,000`, the payment is not immediately approved — the result status is `"pending"` with the message `"Manager approval required"`.
- **Default approval**: If the amount is within the valid range and does not exceed the threshold, the result status is `"approved"` with the message `"Payment processed successfully"`.
- **Result payload**: Regardless of status, the result now includes the resolved `payment_method` (as its string `.value`), in addition to `status`, `message`, `amount`, `fee`, and `total_amount`.

### Processing Flow

1. `PaymentProcessor.process(amount, payment_method)` is called with a numeric amount and a `PaymentMethod` enum member.
2. `PaymentValidator.validate(amount, payment_method)` checks:
   - `amount > 0`; raises `ValueError("Amount must be greater than zero")` otherwise.
   - `payment_method` is a `PaymentMethod` instance; raises `ValueError("Invalid payment method")` otherwise.
3. `PaymentProcessor.calculate_fee(amount, payment_method)` looks up the fee rate for the given payment method from `FEE_RATES` and computes `fee = round(amount * rate, 2)`.
4. `total_amount = amount + fee` is computed.
5. If `amount > 1,000,000`, `status = "pending"` and `message = "Manager approval required"`.
6. Otherwise, `status = "approved"` and `message = "Payment processed successfully"`.
7. A result dictionary is returned containing `status`, `message`, `payment_method` (string value), `amount`, `fee`, and `total_amount`.

## 5. Components

### `PaymentMethod`
- **Type**: `Enum`.
- **Members**: `UPI = "UPI"`, `CARD = "CARD"`, `BANK_TRANSFER = "BANK_TRANSFER"`.
- **Purpose**: Restricts the set of valid payment methods accepted by `PaymentValidator` and `PaymentProcessor`.

### `PaymentValidator`
- **Type**: Class with a single static method.
- **Method**: `validate(amount, payment_method)` — raises `ValueError` if `amount <= 0` (`"Amount must be greater than zero"`), and raises `ValueError` if `payment_method` is not an instance of `PaymentMethod` (`"Invalid payment method"`). Otherwise performs no action (implicitly valid).

### `PaymentProcessor`
- **Type**: Class encapsulating payment processing.
- **Class attribute**: `FEE_RATES` — a dict mapping each `PaymentMethod` to its fee rate (`UPI`: `0.01`, `CARD`: `0.02`, `BANK_TRANSFER`: `0.005`).
- **Method**: `calculate_fee(self, amount, payment_method)` — looks up the rate for `payment_method` in `FEE_RATES` and returns `round(amount * rate, 2)`.
- **Method**: `process(self, amount, payment_method)`:
  - Validates the amount and payment method via `PaymentValidator.validate`.
  - Calculates `fee` via `calculate_fee` and computes `total_amount`.
  - Determines `status` and `message` based on the approval threshold (`amount > 1,000,000`).
  - Returns a dictionary describing the outcome (`status`, `message`, `payment_method` (string value), `amount`, `fee`, `total_amount`).

### Script-level execution
- Instantiates `processor = PaymentProcessor()`.
- Calls `processor.process(60000, PaymentMethod.UPI)`.
- Prints the resulting dictionary to standard output.

### `test.txt`
- A non-code text file containing two lines: `test` and `check 1 -1`. No functional role evidenced; appears to be a test/placeholder artifact.

## 6. Data Flow

```
amount, payment_method (input)
   │
   ▼
PaymentValidator.validate(amount, payment_method)
   ├── amount <= 0            ──▶ raises ValueError("Amount must be greater than zero")
   └── not a PaymentMethod    ──▶ raises ValueError("Invalid payment method")
   ▼
PaymentProcessor.calculate_fee(amount, payment_method)
   │   rate = FEE_RATES[payment_method]   (UPI=0.01, CARD=0.02, BANK_TRANSFER=0.005)
   │   fee = round(amount * rate, 2)
   ▼
total_amount = amount + fee
   │
   ▼
amount > 1,000,000 ?
   ├── Yes ──▶ {status: "pending",  message: "Manager approval required",       payment_method, amount, fee, total_amount}
   └── No  ──▶ {status: "approved", message: "Payment processed successfully",  payment_method, amount, fee, total_amount}
```

Data flows entirely in-memory within a single process execution; there is no external I/O, persistence, or network transmission evidenced.

## 7. Configuration

No configuration files, environment variables, or settings are evidenced in the supplied code.

- The per-method fee rates (`UPI`: `0.01`, `CARD`: `0.02`, `BANK_TRANSFER`: `0.005`) are hard-coded as a class-level dictionary (`PaymentProcessor.FEE_RATES`), not externalized as configuration.
- The approval threshold (`1,000,000`) is a hard-coded literal within `PaymentProcessor.process`, not externalized as configuration.

## 8. Error Handling

- `PaymentValidator.validate(amount, payment_method)` raises a `ValueError` with message `"Amount must be greater than zero"` when `amount <= 0`.
- `PaymentValidator.validate(amount, payment_method)` raises a `ValueError` with message `"Invalid payment method"` when `payment_method` is not an instance of the `PaymentMethod` enum.
- Both exceptions propagate uncaught from `PaymentProcessor.process`, meaning callers must handle them themselves (no try/except is present in the supplied script).
- `PaymentProcessor.calculate_fee` will raise a `KeyError` if called with a `payment_method` not present in `FEE_RATES`; however, since `validate` is called before `calculate_fee` in `process` and rejects non-`PaymentMethod` values, this scenario is not reachable through the normal `process` flow given the currently defined enum members.
- No other error handling (e.g., type validation for non-numeric amounts) is present in the supplied code.

## 9. Dependencies

`payment.py` now imports `Enum` from the Python standard library (`enum` module) to define `PaymentMethod`. No third-party libraries, frameworks, or external services are used or evidenced.

## 10. Usage

The script is intended to be run directly (e.g., `python payment.py`). On execution it:

1. Instantiates a `PaymentProcessor`.
2. Calls `processor.process(60000, PaymentMethod.UPI)`.
3. Prints the resulting dictionary (containing `status`, `message`, `payment_method`, `amount`, `fee`, `total_amount`) to standard output.

To process a different payment, callers should import `PaymentMethod` and `PaymentProcessor`, then call:

```python
processor = PaymentProcessor()
result = processor.process(amount, PaymentMethod.CARD)  # or .UPI / .BANK_TRANSFER
```

Callers must be prepared to catch `ValueError` for invalid amounts or invalid payment methods, since `process` does not handle these internally.

## 11. Architecture Diagram

```mermaid
flowchart TD
    A[Script entry point] --> B[PaymentProcessor.process(amount, payment_method)]
    B --> C[PaymentValidator.validate(amount, payment_method)]
    C -->|amount <= 0| D[raise ValueError: Amount must be greater than zero]
    C -->|not a PaymentMethod| E[raise ValueError: Invalid payment method]
    C -->|valid| F[PaymentProcessor.calculate_fee(amount, payment_method)]
    F --> G[Lookup rate in FEE_RATES by payment_method]
    G --> H[fee = round(amount * rate, 2)]
    H --> I[total_amount = amount + fee]
    I --> J{amount > 1,000,000?}
    J -->|Yes| K[status = pending, message = Manager approval required]
    J -->|No| L[status = approved, message = Payment processed successfully]
    K --> M[Return result dict: status, message, payment_method, amount, fee, total_amount]
    L --> M
    M --> N[print(result)]
```

## 12. Change Summary

### What Changed

- Introduced a `PaymentMethod` `Enum` with members `UPI`, `CARD`, and `BANK_TRANSFER`.
- `PaymentValidator.validate` now accepts and validates a `payment_method` argument in addition to `amount`, raising `ValueError("Invalid payment method")` if it is not a `PaymentMethod` instance.
- `PaymentProcessor` gained a `FEE_RATES` class attribute mapping each `PaymentMethod` to a distinct fee rate (`UPI`: `0.01`, `CARD`: `0.02`, `BANK_TRANSFER`: `0.005`), replacing the previous flat `0.02` (2%) fee applied to all payments.
- Added `PaymentProcessor.calculate_fee(amount, payment_method)`, which looks up the applicable rate and returns `round(amount * rate, 2)`.
- `PaymentProcessor.process` now requires a `payment_method` argument, delegates fee calculation to `calculate_fee`, and refactors the approval-threshold branching into local `status`/`message` variables before constructing a single return statement (removing the previous early-return duplicate dictionary construction).
- The returned result dictionary now includes a `payment_method` key (the enum member's string `.value`) in both the "pending" and "approved" outcomes.
- The approval threshold literal changed from `1000000` to the equivalent `1_000_000` (numeric underscore formatting only; value unchanged).
- The script-level example call changed from `processor.process(50000)` to `processor.process(60000, PaymentMethod.UPI)`.
- A trailing newline was added after the final `print(result)` statement.

### Why It Changed

Not evidenced in supplied context. (PR description was not provided; changes are inferred solely from the code diff to support multiple payment methods with differentiated processing fees.)

### Impacted Modules

- `payment.py`
  - `PaymentMethod` (new `Enum`)
  - `PaymentValidator` (`validate` method signature and logic changed)
  - `PaymentProcessor` (`FEE_RATES` class attribute added, `calculate_fee` method added, `process` method signature and logic changed)
  - Script-level execution block (updated example call)

### API / Interface Changes

- `PaymentValidator.validate(amount)` → `PaymentValidator.validate(amount, payment_method)`. Callers must now pass a `PaymentMethod` enum member; omitting it or passing an invalid type raises `ValueError("Invalid payment method")`.
- `PaymentProcessor.process(amount)` → `PaymentProcessor.process(amount, payment_method)`. This is a breaking signature change — the `payment_method` parameter is required.
- New method: `PaymentProcessor.calculate_fee(self, amount, payment_method)`.
- Return value of `PaymentProcessor.process` gained a new key: `payment_method` (string), present in both `"approved"` and `"pending"` outcomes.

### Configuration Changes

None evidenced. The new fee rates and payment methods remain hard-coded in `PaymentProcessor.FEE_RATES` and the `PaymentMethod` enum, not externalized as configuration.

### Expected Behavior

- Observed from code: Calling `process` without a `payment_method` argument will now raise a `TypeError` (missing required positional argument), since the parameter has no default. Calling `process(amount, payment_method)` with a valid `PaymentMethod` member computes a fee based on that method's specific rate rather than a flat 2%, and returns a result dictionary that additionally reports the payment method used.
- Observed from code: The approval threshold logic (`amount > 1,000,000` triggers `"pending"`) is unchanged in effect, only refactored in implementation.
- Inferred: This change is intended to support differentiated fee pricing across payment channels (e.g., cheaper bank transfers vs. more expensive card payments).

### Backward Compatibility

- **Breaking change**: Any existing caller invoking `PaymentProcessor.process(amount)` or