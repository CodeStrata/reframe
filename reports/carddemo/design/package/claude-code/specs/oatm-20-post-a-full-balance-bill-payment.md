# Post a full-balance bill payment (OATM-C20)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Posts a confirmed bill payment as a new transaction for the full current balance, clears the account balance to zero, and gives the cardholder the new transaction ID as proof. The payment is numbered one above the highest existing transaction ID. As the legacy system behaves, the balance is still cleared even when the payment transaction could not be written, so the build team must decide explicitly whether to keep that.

**User story:** As a cardholder, I want my confirmed payment recorded as a transaction for the full balance and my account balance cleared, so that my account is paid off and I get a transaction ID as proof.

## Requirements

### Requirement 1: OATM-REQ-F-160 (business rule)

#### Acceptance criteria

1. When the user confirms a bill payment with 'Y' or 'y' and the account has a balance to pay, the system shall look up the card linked to the account and number the new payment transaction as the highest existing transaction ID plus 1. (rules OATM-BR-166)
2. GIVEN Confirm: Y; Highest transaction ID on file: 0000000000001234 WHEN the user confirms a bill payment with 'Y' or 'y' and the account has a balance to pay THEN The payment transaction is given ID 0000000000001235. (OATM-C20-AC-01; OATM-BR-166)

### Requirement 2: OATM-REQ-F-161 (design note)

#### Acceptance criteria

1. When a confirmed bill payment needs a new transaction number, the system shall position at the end of the transaction file, read the last transaction record and take its transaction ID as the latest existing number. (rules OATM-BR-167)
2. GIVEN Highest transaction ID on file: 0000000000001234; Confirm: Y WHEN a confirmed bill payment needs a new transaction number THEN The latest existing transaction ID is taken as 0000000000001234. (OATM-C20-AC-02; OATM-BR-167)

### Requirement 3: OATM-REQ-F-162 (business rule)

#### Acceptance criteria

1. When reading back from the end of the transaction file finds no transaction, the system shall treat the latest transaction ID as zero, so the payment is given transaction ID 1. (rules OATM-BR-168)
2. GIVEN Transaction file: empty; Confirm: Y WHEN reading back from the end of the transaction file finds no transaction (end of file) THEN The new payment transaction is numbered 0000000000000001. (OATM-C20-AC-03; OATM-BR-168)

### Requirement 4: OATM-REQ-F-163 (error handling)

#### Acceptance criteria

1. If a confirmed payment's lookup of the card linked to the account finds no card link, then the system shall show 'Account ID NOT found...', or 'Unable to lookup XREF AIX file...' on any other failure. (rules OATM-BR-169)
2. GIVEN Account ID: 00000000011; Confirm: Y; Card link for account: missing WHEN a confirmed payment looks up the card linked to the account THEN 'Account ID NOT found...' is shown (but see defect: posting still continues). (OATM-C20-AC-04; OATM-BR-169)

### Requirement 5: OATM-REQ-F-164 (business rule)

#### Acceptance criteria

1. When the user confirms a bill payment, the system shall record a payment for the full current account balance and reduce the account's current balance by that amount, leaving it at zero. (rules OATM-BR-170, OATM-BR-171)
2. GIVEN Confirm: Y; ACCT-CURR-BAL: 150.00; last TRAN-ID: 0000000000000041 WHEN a confirmed bill payment is posted THEN Transaction 0000000000000042 written with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', amount 150.00, merchant 999999999 'BILL PAYMENT' 'N/A' 'N/A', current timestamp; balance then becomes 0.00 (OATM-C20-AC-05; OATM-BR-170)
3. GIVEN Confirm: (blank); ACCT-CURR-BAL: 150.00 WHEN a confirmed bill payment is posted THEN No transaction written; screen shows 'Confirm to make a bill payment...' (OATM-C20-AC-06; OATM-BR-170)
4. GIVEN Account: 00000000011; Current balance: $1,250.75; Confirm: Y WHEN the user confirms a bill payment THEN A payment transaction of $1,250.75 is written and the account balance becomes $0.00. (OATM-C20-AC-07; OATM-BR-171)

### Requirement 6: OATM-REQ-F-165 (business rule)

#### Acceptance criteria

1. The system shall record each online payment with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', merchant ID 999999999, merchant name 'BILL PAYMENT', merchant city and ZIP 'N/A', the account's card number, and the current date and time as both origin and processing time. (rules OATM-BR-170, OATM-BR-172)
2. GIVEN Confirm: Y; ACCT-CURR-BAL: 150.00; last TRAN-ID: 0000000000000041 WHEN a confirmed bill payment is posted THEN Transaction 0000000000000042 written with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', amount 150.00, merchant 999999999 'BILL PAYMENT' 'N/A' 'N/A', current timestamp; balance then becomes 0.00 (OATM-C20-AC-05; OATM-BR-170)
3. GIVEN Confirm: (blank); ACCT-CURR-BAL: 150.00 WHEN a confirmed bill payment is posted THEN No transaction written; screen shows 'Confirm to make a bill payment...' (OATM-C20-AC-06; OATM-BR-170)
4. GIVEN Account card number: 4111111111111111; Payment time: 2026-11-25 10:15:00 WHEN Bill Payment screen runs THEN The transaction has type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE' and timestamps 2026-11-25 10:15:00. (OATM-C20-AC-08; OATM-BR-172)

### Requirement 7: OATM-REQ-F-166 (business rule)

#### Acceptance criteria

1. When a confirmed payment is posted, the system shall write a payment transaction for the full current balance, then subtract that amount from the account balance and save the account. (rules OATM-BR-173, OATM-BR-174)
2. GIVEN Current balance: $300.00; Confirm: Y WHEN a confirmed payment is posted THEN A transaction of $300.00 is written and the balance becomes $0.00. (OATM-C20-AC-09; OATM-BR-173)
3. GIVEN Balance before: $1,250.75; Payment: $1,250.75 WHEN the payment transaction has been written THEN The account is saved with current balance $0.00. (OATM-C20-AC-10; OATM-BR-174)

### Requirement 8: OATM-REQ-F-167 (formatting)

#### Acceptance criteria

1. When the bill payment transaction is written successfully, the system shall clear the account ID, balance and confirmation fields and show in green 'Payment successful. Your Transaction ID is <new ID>.'. (rules OATM-BR-175)
2. GIVEN A cardholder has confirmed a bill payment with 'Y' on account 00000000001 and the new payment transaction 0000000000000124 is written successfully WHEN The Bill Payment screen is shown again THEN The account ID, balance and confirmation fields are empty and the message 'Payment successful. Your Transaction ID is 0000000000000124.' is shown in green (OATM-C20-AC-15; OATM-BR-175)

### Requirement 9: OATM-REQ-F-168 (error handling)

#### Acceptance criteria

1. If the payment transaction ID already exists, then the system shall show 'Tran ID already exist...', and for any other write failure 'Unable to Add Bill pay Transaction...'. (rules OATM-BR-176)
2. GIVEN Write result: duplicate key WHEN the payment transaction ID already exists THEN The message 'Tran ID already exist...' is shown. (OATM-C20-AC-11; OATM-BR-176)

### Requirement 10: OATM-REQ-F-169 (error handling)

#### Acceptance criteria

1. If the payment transaction cannot be written or the card lookup fails, then the system shall still subtract the payment from the balance and save the account, so the balance is cleared without a payment on file. (rules OATM-BR-177)
2. GIVEN Current balance: $300.00; Confirm: Y; Transaction write: duplicate key WHEN the payment transaction cannot be written (message 'Tran ID already exist...' or 'Unable to Add Bill pay Transaction...') or the card lookup fails THEN 'Tran ID already exist...' is shown, yet the balance is saved as $0.00 with no payment transaction. (OATM-C20-AC-12; OATM-BR-177)

### Requirement 11: OATM-REQ-F-170 (error handling)

#### Acceptance criteria

1. If saving the updated account fails, then the system shall show 'Account ID NOT found...' if the account is not found, or 'Unable to Update Account...' for any other failure, with the cursor on the account ID. (rules OATM-BR-178)
2. GIVEN Account save result: not found WHEN saving the updated account fails THEN The message 'Account ID NOT found...' is shown. (OATM-C20-AC-13; OATM-BR-178)
3. GIVEN Account save result: other error WHEN saving the updated account fails THEN The message 'Unable to Update Account...' is shown. (OATM-C20-AC-14; OATM-BR-178)

## Screens and components

### Pay balance (S-BILL-PAY)

See the balance owed on an account and pay it in full after confirming.

Prototype: `ui-reference/index.html#/S-BILL-PAY`. Replaces the legacy screens COBIL0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Pay full balance | button | Opens the confirmation; offered only when a balance is owed |  |  | OATM-REQ-F-164, OATM-REQ-F-165 |
| Payment result | message | Success: 'Payment successful. Your Transaction ID is <id>.' and the form clears; failures: 'Tran ID already exist...', 'Unable to Add Bill pay Transaction...', 'Unable to Update Account...' |  |  | OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-169 |


## Data models

#### CVACT01Y

File record of COBIL00C. Source: `app/cpy/CVACT01Y.cpy`.

Record `ACCOUNT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| ACCT-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| ACCT-CURR-BAL |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CASH-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-OPEN-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-REISSUE-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-CURR-CYC-CREDIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CURR-CYC-DEBIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| ACCT-GROUP-ID |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(178) | text, 178 characters |  |  |  |

#### CVACT03Y

File record of COBIL00C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA05Y

File record of COBIL00C. Source: `app/cpy/CVTRA05Y.cpy`.

Record `TRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| TRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| TRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| TRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| TRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| TRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| TRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

- COCOM01Y (working storage of COBIL00C): see data-contracts.md.
- COTTL01Y (working storage of COBIL00C): see data-contracts.md.
- CSDAT01Y (working storage of COBIL00C): see data-contracts.md.
- CSMSG01Y (working storage of COBIL00C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-166 | Assign next payment transaction ID | business rule | WHEN the user confirms a bill payment with 'Y' or 'y' and the account has a balance to pay, THE Bill Payment screen SHALL look up the card linked to the account and number the new payment transaction as the highest existing transaction ID plus 1. | medium | app/cbl/COBIL00C.cbl:173-177, app/cbl/COBIL00C.cbl:197-219, app/cbl/COBIL00C.cbl:408-418 |
| OATM-BR-167 | Retrieve latest existing transaction | design note | WHEN a confirmed bill payment needs a new transaction number, THE Bill Payment screen SHALL position at the end of the transaction file, read the last transaction record and take its transaction ID as the latest existing number. | medium | app/cbl/COBIL00C.cbl:212-216, app/cbl/COBIL00C.cbl:441-449, app/cbl/COBIL00C.cbl:472-486 |
| OATM-BR-168 | Default identifier when no transactions exist | business rule | WHEN reading back from the end of the transaction file finds no transaction (end of file), THE Bill Payment screen SHALL treat the latest transaction ID as zero, so the payment is given transaction ID 1. | medium | app/cbl/COBIL00C.cbl:487-488, app/cbl/COBIL00C.cbl:216-219 |
| OATM-BR-169 | Retrieve card linked to account | error handling | WHEN a confirmed payment looks up the card linked to the account, THE Bill Payment screen SHALL show 'Account ID NOT found...' if no card link exists, or 'Unable to lookup XREF AIX file...' on any other failure (card cross-reference by account). | high | app/cbl/COBIL00C.cbl:158-167, app/cbl/COBIL00C.cbl:173-184, app/cbl/COBIL00C.cbl:343-372, app/cbl/COBIL00C.cbl:208-235 |
| OATM-BR-170 | Build bill payment transaction record | business rule | WHEN a confirmed bill payment is posted, THE Bill Payment Posting SHALL create a type '02', category 2 transaction for the full current balance with the fixed bill-payment merchant values and the current timestamp, and write it | medium | app/cbl/COBIL00C.cbl:218-233, app/cbl/COBIL00C.cbl:218-232 |
| OATM-BR-171 | Bill payment pays the full current account balance | business rule | WHEN the user confirms a bill payment, THE Bill Payment screen SHALL record a payment for the full current account balance and reduce the account's current balance by that amount, leaving it at zero. | medium | app/cbl/COBIL00C.cbl:218-235, app/cbl/COBIL00C.cbl:249-267 |
| OATM-BR-172 | Bill payment pays the full current account balance | business rule | THE Bill Payment screen SHALL record each online payment with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', merchant ID 999999999, merchant name 'BILL PAYMENT', merchant city and ZIP 'N/A', the account's card number, and the current date and time as both origin and processing time. | medium | app/cbl/COBIL00C.cbl:218-235, app/cbl/COBIL00C.cbl:249-267 |
| OATM-BR-173 | Reduce account balance by payment | business rule | WHEN a confirmed payment is posted, THE Bill Payment screen SHALL write a payment transaction for the full current balance, then subtract that amount from the account balance and save the account. | high | app/cbl/COBIL00C.cbl:210-235, app/cbl/COBIL00C.cbl:510-547, app/cbl/COBIL00C.cbl:377-403 |
| OATM-BR-174 | Save updated account balance | design note | WHEN the payment transaction has been written, THE Bill Payment screen SHALL save the account with its reduced current balance. | medium | app/cbl/COBIL00C.cbl:233-235, app/cbl/COBIL00C.cbl:377-403 |
| OATM-BR-175 | Confirm successful payment to operator | formatting | WHEN the bill payment transaction is written successfully, THE Bill Payment screen SHALL clear the account ID, balance and confirmation fields and show in green 'Payment successful. Your Transaction ID is <new ID>.' | medium | app/cbl/COBIL00C.cbl:510-547, app/cbl/COBIL00C.cbl:560-566 |
| OATM-BR-176 | Confirm successful payment to operator | error handling | WHEN the payment transaction ID already exists, THE Bill Payment screen SHALL show 'Tran ID already exist...', and for any other write failure 'Unable to Add Bill pay Transaction...'. | medium | app/cbl/COBIL00C.cbl:510-547, app/cbl/COBIL00C.cbl:560-566 |
| OATM-BR-177 | Payment posting is not atomic: balance is cleared even if transaction write fails | error handling | WHEN the payment transaction cannot be written (message 'Tran ID already exist...' or 'Unable to Add Bill pay Transaction...') or the card lookup fails, THE Bill Payment screen SHALL still subtract the payment from the balance and save the account, so the balance is cleared without a payment on file. | high | app/cbl/COBIL00C.cbl:210-235, app/cbl/COBIL00C.cbl:510-547, app/cbl/COBIL00C.cbl:377-403 |
| OATM-BR-178 | Save updated account balance | error handling | WHEN saving the updated account fails, THE Bill Payment screen SHALL show 'Account ID NOT found...' if the account is not found, or 'Unable to Update Account...' for any other failure, with the cursor on the account ID. | medium | app/cbl/COBIL00C.cbl:233-235, app/cbl/COBIL00C.cbl:377-403 |

### Worked examples

- OATM-BR-166: Confirm = Y; Highest transaction ID on file = 0000000000001234 → The payment transaction is given ID 0000000000001235.
- OATM-BR-167: Highest transaction ID on file = 0000000000001234; Confirm = Y → The latest existing transaction ID is taken as 0000000000001234.
- OATM-BR-168: Transaction file = empty; Confirm = Y → The new payment transaction is numbered 0000000000000001.
- OATM-BR-169: Account ID = 00000000011; Confirm = Y; Card link for account = missing → 'Account ID NOT found...' is shown (but see defect: posting still continues).
- OATM-BR-170: Confirm = Y; ACCT-CURR-BAL = 150.00; last TRAN-ID = 0000000000000041 → Transaction 0000000000000042 written with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', amount 150.00, merchant 999999999 'BILL PAYMENT' 'N/A' 'N/A', current timestamp; balance then becomes 0.00
- OATM-BR-170: Confirm = (blank); ACCT-CURR-BAL = 150.00 → No transaction written; screen shows 'Confirm to make a bill payment...'
- OATM-BR-171: Account = 00000000011; Current balance = $1,250.75; Confirm = Y → A payment transaction of $1,250.75 is written and the account balance becomes $0.00.
- OATM-BR-172: Account card number = 4111111111111111; Payment time = 2026-11-25 10:15:00 → The transaction has type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE' and timestamps 2026-11-25 10:15:00.
- OATM-BR-173: Current balance = $300.00; Confirm = Y → A transaction of $300.00 is written and the balance becomes $0.00.
- OATM-BR-174: Balance before = $1,250.75; Payment = $1,250.75 → The account is saved with current balance $0.00.
- OATM-BR-176: Write result = duplicate key → The message 'Tran ID already exist...' is shown.
- OATM-BR-177: Current balance = $300.00; Confirm = Y; Transaction write = duplicate key → 'Tran ID already exist...' is shown, yet the balance is saved as $0.00 with no payment transaction.
- OATM-BR-178: Account save result = not found → The message 'Account ID NOT found...' is shown.
- OATM-BR-178: Account save result = other error → The message 'Unable to Update Account...' is shown.

## Decision tables

#### Bill payment posting outcome

| Card lookup | Transaction write | Account save | Result | Rule |
|---|---|---|---|---|
| Found | Written | Saved | Balance reduced to zero; fields cleared; green 'Payment successful. Your Transaction ID is <new ID>.' | OATM-BR-175 |
| Found | Transaction ID already exists | Saved | 'Tran ID already exist...'; balance still cleared without a payment on file | OATM-BR-177 |
| Found | Other write failure | Saved | 'Unable to Add Bill pay Transaction...'; balance still cleared without a payment on file | OATM-BR-177 |
| No card link | — | Saved | 'Account ID NOT found...'; balance still cleared without a payment on file | OATM-BR-177 |
| Other failure | — | Saved | 'Unable to lookup XREF AIX file...'; balance still cleared without a payment on file | OATM-BR-177 |
| Any | Any | Account not found | 'Account ID NOT found...', cursor on account ID | OATM-BR-178 |
| Any | Any | Other failure | 'Unable to Update Account...', cursor on account ID | OATM-BR-178 |
| Found | Written | Account not found or other failure | **Gap:** No rule says whether the written payment transaction is kept or reversed when the account save fails, leaving a payment on file without a reduced balance. | |


## Design notes

- OATM-BR-167: Needs the highest existing transaction ID (a 'max ID' query or a descending keyed read of the last record). When there are no transactions it returns zero. Because 'highest plus 1' can race between concurrent payments, the new application should use a database sequence or an atomic ID generator, with the unique key as a safety net.
- OATM-BR-174: After the payment transaction is written, the account read for update earlier is saved with its reduced current balance. This should be an update on the same locked or version-checked account row. Ideally it runs in the same database transaction as the payment insert, so the balance and the payment record cannot disagree (subject to the decision on the non-atomic legacy behaviour).

## Open questions

- SME-080: What should the bill payment screen do when it is opened without any information from the screen that called it? (Business analyst) On OATM-BR-170, OATM-BR-167, OATM-BR-168, OATM-BR-166, OATM-BR-178, OATM-BR-176, OATM-BR-169, OATM-BR-173.
- SME-081: What format and length must a new bill payment transaction ID have? It is currently the last ID plus 1. (Data architect) On OATM-BR-170, OATM-BR-167, OATM-BR-168, OATM-BR-166, OATM-BR-178, OATM-BR-176, OATM-BR-169, OATM-BR-173.
- SME-082: The bill payment transaction is saved before the account balance is reduced. If the account update then fails, what should happen to the saved transaction? Should the two be one all-or-nothing step? (Business analyst / architecture team) On OATM-BR-170, OATM-BR-167, OATM-BR-168, OATM-BR-166, OATM-BR-178, OATM-BR-176, OATM-BR-169, OATM-BR-173.
- SME-083: How must the system make sure that two bill payments made at the same time never get the same transaction ID? (Architecture team) On OATM-BR-170, OATM-BR-167, OATM-BR-168, OATM-BR-166, OATM-BR-178, OATM-BR-176, OATM-BR-169, OATM-BR-173.
- SME-084: If saving the bill payment transaction fails, what message should the user see and how should the failure be handled? (Business analyst) On OATM-BR-170, OATM-BR-167, OATM-BR-168, OATM-BR-166, OATM-BR-178, OATM-BR-176, OATM-BR-169, OATM-BR-173.
- SME-085: During a bill payment, should a failed card cross-reference lookup or a failed account update stop the remaining payment steps? (Business analyst) On OATM-BR-170, OATM-BR-167, OATM-BR-168, OATM-BR-166, OATM-BR-178, OATM-BR-176, OATM-BR-169, OATM-BR-173.
- SME-086: Please confirm the full rule for checking the account ID on bill payment: it is required, it must exist, and which error message goes with each case. (Legacy application SME) On OATM-BR-169.
- SME-088: Online bill payments are recorded as type '02', category 2. Does that match the payment type and category in the transaction-type reference data? Should payment amounts be stored as positive or negative compared with purchases? (Payments business owner) On OATM-BR-170.
- DEF-046: Is this intended? A failed card cross-reference lookup sets an error message but does not stop the posting: the transaction is still written (with whatever card number is in the cross-reference record) and the balance is still reduced and saved. (Subject-matter expert) On OATM-BR-169.
- DEF-058: Is this intended? The balance reduction and account rewrite are not conditional on the transaction write (or card lookup) succeeding, so a failed write leaves the account balance cleared with no payment transaction recorded. (Subject-matter expert) On OATM-BR-173, OATM-BR-177.
- DEF-111: Is this intended? After each step of the payment (card cross-reference lookup, transaction browse, transaction write) the error flag is set on failure but never checked before the next step, so a failed lookup still leads to writing a transaction, and a failed transaction write still reduces and rewrites the account balance. (Subject-matter expert) On OATM-BR-167.
- DEF-115: Is this intended? Errors from the card cross-reference lookup or the transaction browse set the error flag but the payment steps continue anyway, so a transaction can be written with no card number. (Subject-matter expert) On OATM-BR-166.
- DEF-118: Is this intended? The account is rewritten even when the payment transaction write failed, and a failed account rewrite does not undo the transaction already written, so the transaction file and account balance can disagree. (Subject-matter expert) On OATM-BR-178.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).
