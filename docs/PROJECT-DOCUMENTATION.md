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
- **Approval threshold rule**: If `amount > 1000000`, the payment is not immediately approved — the result status is `"pending"` with the message `"Manager approval required"`. (The threshold value itself remains `1,000,000`; only its literal representation in code changed from `1_000_000` to `1000000`, a formatting change with no effect on behavior.)
- **Default approval**: If the amount is within the valid range and does not exceed the threshold, the result status is `"approved"` with the message `"Payment processed successfully"`.
- **Result payload**: Regardless of status, the result now includes the resolved `payment_method` (as its string `.value`), in addition to `status`, `message`, `amount`, `fee`, and `total_amount`.

### Processing Flow

1. `PaymentProcessor.process(amount, payment_method)` is called with a numeric amount and a `PaymentMethod` enum member.
2. `PaymentValidator.validate(amount, payment_method)` checks:
   - `amount > 0`; raises `ValueError("Amount must be greater than zero")` otherwise.
   - `payment_method` is a `PaymentMethod` instance; raises `ValueError("Invalid payment method")` otherwise.
3. `PaymentProcessor.calculate_fee(amount, payment_method)` looks up the fee rate for the given payment method from `FEE_RATES` and computes `fee = round(amount * rate, 2)`.
4. `total_amount = amount + fee` is computed.
5. If `amount > 1000000`, `status = "pending"` and `message = "Manager approval required"`.
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
  - Determines `status` and `message` based on the approval threshold (`amount > 1000000`).
  - Returns a dictionary describing the outcome (`status`, `message`, `payment_method` (string value), `amount`, `fee`, `total_amount`).

### Script-level execution
- Instantiates `processor = PaymentProcessor()`.
- Calls `processor.process(30000, PaymentMethod.UPI)`. (Previously `60000`; the example invocation amount was changed but the underlying processing logic and outcome — `"approved"` status, since the amount remains well below the 1,000,000 threshold — are unaffected.)
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
amount > 1000000 ?
   ├── Yes ──▶ {status: "pending",  message: "Manager approval required",       payment_method, amount, fee, total_amount}
   └── No  ──▶ {status: "approved", message: "Payment processed successfully",  payment_method, amount, fee, total_amount}
```

Data flows entirely in-memory within a single process execution; there is no external I/O, persistence, or network transmission evidenced.

## 7. Configuration

No configuration files, environment variables, or settings are evidenced in the supplied code.

- The per-method fee rates (`UPI`: `0.01`, `CARD`: `0.02`, `BANK_TRANSFER`: `0.005`) are hard-coded as a class-level dictionary (`PaymentProcessor.FEE_RATES`), not externalized as configuration.
- The approval threshold (`1000000`) is a hard-coded literal within `PaymentProcessor.process`, not externalized as configuration. Its numeric value is unchanged; only its literal formatting (previously written with an underscore digit separator, `1_000_000`) was updated.

## 8. Error Handling

- `PaymentValidator.validate(amount, payment_method)` raises a `ValueError` with message `"Amount must be greater than zero"` when `amount <= 0`.
- `PaymentValidator.validate(amount, payment_method)` raises a `ValueError` with message `"Invalid payment method"` when `payment_method` is not an instance of the `PaymentMethod` enum.
- Both exceptions propagate uncaught from `PaymentProcessor.process`, meaning callers must handle them themselves (no try/except is present in the supplied script).
- `PaymentProcessor.calculate_fee` will raise a `KeyError` if called with a `payment_method` not present in `FEE_RATES`; however, since `validate` is called before `calculate_fee` in `process` and rejects non-`PaymentMethod` values, this scenario is not reachable through the normal `process` flow given the currently defined enum members.
- No other error handling (e.g., type validation for non-numeric amounts) is present in the supplied code.

## 9. Dependencies

`payment.py` imports `Enum` from the Python standard library (`enum` module) to define `PaymentMethod`. No third-party libraries, frameworks, or external services are evidenced in the supplied code.

## 12. Change Summary

### What Changed

- In `PaymentProcessor.process`, the approval threshold check was rewritten from `if amount > 1_000_000:` to `if amount > 1000000:`. This is a literal formatting change (removal of the underscore digit separator); the numeric threshold value (1,000,000) is unchanged.
- In the script-level example invocation, `processor.process(60000, PaymentMethod.UPI)` was changed to `processor.process(30000, PaymentMethod.UPI)`, altering the sample amount used when the script is run directly.

### Why It Changed

Not evidenced in supplied context. The PR title is "Pyament Process Update" with no description provided.

### Impacted Modules

- `payment.py` — specifically `PaymentProcessor.process` (threshold literal) and the module's top-level script execution block (example invocation amount).

### API / Interface Changes

None evidenced. Method signatures for `PaymentValidator.validate`, `PaymentProcessor.calculate_fee`, and `PaymentProcessor.process` are unchanged.

### Configuration Changes

None evidenced. The approval threshold remains a hard-coded literal (value unchanged at 1,000,000); only its source-code representation changed.

### Expected Behavior

- **Observed from code**: The approval threshold comparison behaves identically before and after the change, since `1_000_000 == 1000000` in Python — no functional difference in when a payment is marked `"pending"` vs. `"approved"`.
- **Observed from code**: Running the script directly now processes a payment of `30000` via `UPI` instead of `60000`. Given the fee rate for `UPI` is `1%`, this changes the printed sample output's `amount`, `fee` (from `600.0` to `300.0`), and `total_amount` (from `60600.0` to `30300.0`), but the `status` remains `"approved"` in both cases since neither amount exceeds the 1,000,000 threshold.
- **Inferred**: This change appears to be a minor code cleanup/example-data adjustment rather than a business rule change.

### Backward Compatibility

No breaking changes are evidenced. The public method signatures, validation rules, fee calculation logic, and approval threshold value are all unchanged. The only differences are a code-style literal change and a sample invocation value, neither of which affects the module's external behavior or contract.

### Testing Requirements

- Verify `PaymentProcessor.process` still returns `status = "approved"` for amounts at and below 1,000,000, and `status = "pending"` for amounts above 1,000,000, confirming the threshold behavior is unaffected by the literal formatting change.
- Verify boundary behavior at `amount == 1000000` (should be `"approved"`, since the condition is strictly `>`).
- Re-run/verify the script's sample output reflects the new example amount (`30000`) with correct `fee` (`300.0`) and `total_amount` (`30300.0`) for `PaymentMethod.UPI`.
- Confirm no regression in existing validation error paths (`amount <= 0`, invalid `payment_method`).