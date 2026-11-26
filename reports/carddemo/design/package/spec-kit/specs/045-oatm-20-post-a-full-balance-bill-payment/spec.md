# Feature specification: Post a full-balance bill payment

**Feature:** OATM-C20 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C20)

As a cardholder, I want my confirmed payment recorded as a transaction for the full balance and my account balance cleared, so that my account is paid off and I get a transaction ID as proof.

Posts a confirmed online bill payment. It records a type '02', category 2 transaction for the full current balance under the next transaction ID, clears the account balance to zero and gives the cardholder the transaction ID as proof. It must never charge a different amount than the balance or reuse a transaction ID. Note that the legacy system clears the balance even when the payment record cannot be written, so the team must decide whether to keep that or make the two steps all-or-nothing.

**Acceptance scenarios:**

1. **Given** Confirm: Y; Highest transaction ID on file: 0000000000001234, **when** the user confirms a bill payment with 'Y' or 'y' and the account has a balance to pay, **then** The payment transaction is given ID 0000000000001235. (OATM-C20-AC-01)
2. **Given** Highest transaction ID on file: 0000000000001234; Confirm: Y, **when** a confirmed bill payment needs a new transaction number, **then** The latest existing transaction ID is taken as 0000000000001234. (OATM-C20-AC-02)
3. **Given** Transaction file: empty; Confirm: Y, **when** reading back from the end of the transaction file finds no transaction (end of file), **then** The new payment transaction is numbered 0000000000000001. (OATM-C20-AC-03)
4. **Given** Account ID: 00000000011; Confirm: Y; Card link for account: missing, **when** a confirmed payment looks up the card linked to the account, **then** 'Account ID NOT found...' is shown (but see defect: posting still continues). (OATM-C20-AC-04)
5. **Given** Confirm: Y; ACCT-CURR-BAL: 150.00; last TRAN-ID: 0000000000000041, **when** a confirmed bill payment is posted, **then** Transaction 0000000000000042 written with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', amount 150.00, merchant 999999999 'BILL PAYMENT' 'N/A' 'N/A', current timestamp; balance then becomes 0.00 (OATM-C20-AC-05)
6. **Given** Confirm: (blank); ACCT-CURR-BAL: 150.00, **when** a confirmed bill payment is posted, **then** No transaction written; screen shows 'Confirm to make a bill payment...' (OATM-C20-AC-06)
7. **Given** Account: 00000000011; Current balance: $1,250.75; Confirm: Y, **when** the user confirms a bill payment, **then** A payment transaction of $1,250.75 is written and the account balance becomes $0.00. (OATM-C20-AC-07)
8. **Given** Account card number: 4111111111111111; Payment time: 2026-11-25 10:15:00, **when** Bill Payment screen runs, **then** The transaction has type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE' and timestamps 2026-11-25 10:15:00. (OATM-C20-AC-08)
9. **Given** Current balance: $300.00; Confirm: Y, **when** a confirmed payment is posted, **then** A transaction of $300.00 is written and the balance becomes $0.00. (OATM-C20-AC-09)
10. **Given** Balance before: $1,250.75; Payment: $1,250.75, **when** the payment transaction has been written, **then** The account is saved with current balance $0.00. (OATM-C20-AC-10)
11. **Given** Write result: duplicate key, **when** the payment transaction ID already exists, **then** The message 'Tran ID already exist...' is shown. (OATM-C20-AC-11)
12. **Given** Current balance: $300.00; Confirm: Y; Transaction write: duplicate key, **when** the payment transaction cannot be written (message 'Tran ID already exist...' or 'Unable to Add Bill pay Transaction...') or the card lookup fails, **then** 'Tran ID already exist...' is shown, yet the balance is saved as $0.00 with no payment transaction. (OATM-C20-AC-12)
13. **Given** Account save result: not found, **when** saving the updated account fails, **then** The message 'Account ID NOT found...' is shown. (OATM-C20-AC-13)
14. **Given** Account save result: other error, **when** saving the updated account fails, **then** The message 'Unable to Update Account...' is shown. (OATM-C20-AC-14)
15. **Given** A cardholder confirmed with 'Y' a payment on an account with a balance above zero, and the highest existing transaction ID is 0000000000000041, **when** The payment transaction 0000000000000042 is written successfully, **then** The account ID, balance and confirmation fields are cleared and the message 'Payment successful. Your Transaction ID is 0000000000000042.' is shown in green (OATM-C20-AC-15)

## Requirements

### Functional requirements

- **OATM-REQ-F-160** (business rule): When the user confirms a bill payment with 'Y' or 'y' and the account has a balance to pay, the system shall look up the card linked to the account and number the new payment transaction as the highest existing transaction ID plus 1. Rules: OATM-BR-166.
- **OATM-REQ-F-161** (design note): When a confirmed bill payment needs a new transaction number, the system shall position at the end of the transaction file, read the last transaction record and take its transaction ID as the latest existing number. Rules: OATM-BR-167.
- **OATM-REQ-F-162** (business rule): When reading back from the end of the transaction file finds no transaction, the system shall treat the latest transaction ID as zero, so the payment is given transaction ID 1. Rules: OATM-BR-168.
- **OATM-REQ-F-163** (error handling): If a confirmed payment's lookup of the card linked to the account finds no card link, then the system shall show 'Account ID NOT found...', or 'Unable to lookup XREF AIX file...' on any other failure. Rules: OATM-BR-169.
- **OATM-REQ-F-164** (business rule): When the user confirms a bill payment, the system shall record a payment for the full current account balance and reduce the account's current balance by that amount, leaving it at zero. Rules: OATM-BR-170, OATM-BR-171.
- **OATM-REQ-F-165** (business rule): The system shall record each online payment with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', merchant ID 999999999, merchant name 'BILL PAYMENT', merchant city and ZIP 'N/A', the account's card number, and the current date and time as both origin and processing time. Rules: OATM-BR-170, OATM-BR-172.
- **OATM-REQ-F-166** (business rule): When a confirmed payment is posted, the system shall write a payment transaction for the full current balance, then subtract that amount from the account balance and save the account. Rules: OATM-BR-173, OATM-BR-174.
- **OATM-REQ-F-167** (formatting): When the bill payment transaction is written successfully, the system shall clear the account ID, balance and confirmation fields and show in green 'Payment successful. Your Transaction ID is <new ID>.'. Rules: OATM-BR-175.
- **OATM-REQ-F-168** (error handling): If the payment transaction ID already exists, then the system shall show 'Tran ID already exist...', and for any other write failure 'Unable to Add Bill pay Transaction...'. Rules: OATM-BR-176.
- **OATM-REQ-F-169** (error handling): If the payment transaction cannot be written or the card lookup fails, then the system shall still subtract the payment from the balance and save the account, so the balance is cleared without a payment on file. Rules: OATM-BR-177.
- **OATM-REQ-F-170** (error handling): If saving the updated account fails, then the system shall show 'Account ID NOT found...' if the account is not found, or 'Unable to Update Account...' for any other failure, with the cursor on the account ID. Rules: OATM-BR-178.

### Business rules

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

### Key entities

- CVACT01Y (file record)
- CVACT03Y (file record)
- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

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

### Decision table gaps

- Bill payment posting outcome: No rule says whether the written payment transaction is kept or reversed when the account save fails, leaving a payment on file without a reduced balance.
