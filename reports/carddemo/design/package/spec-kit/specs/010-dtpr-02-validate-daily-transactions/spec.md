# Feature specification: Validate daily transactions

**Feature:** DTPR-C02 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C02)

As a card issuer, I want each daily transaction checked against the card cross-reference and the linked account, so that only transactions for known cards on valid, in-limit, unexpired accounts are posted.

Checks each daily card transaction before it is posted. The card must be on the card cross-reference, its account must exist, the account must not go over its credit limit, and the transaction must not be dated after the account expires. It serves the card issuer and decides which transactions are posted and which are rejected. It must never post a transaction for an unknown card, a missing account, an over-limit cycle or an expired account, and it must assign the correct reason code (100, 101, 102 or 103), with expiry (103) taking precedence over over-limit (102).

**Acceptance scenarios:**

1. **Given** Card number: 4111000011112222 (not in cross-reference), **when** daily posting batch runs, **then** Rejected with reason 100 'INVALID CARD NUMBER FOUND'; the account is not looked up (DTPR-C02-AC-01)
2. **Given** Card number: 4111000011112222 (in cross-reference, account 00000000012), **when** daily posting batch runs, **then** Account 00000000012 is looked up (DTPR-C02-AC-02)
3. **Given** DALYTRAN-CARD-NUM: 4000000000000002; Card in cross-reference: no, **when** the transaction's card number is not found in the card cross-reference, **then** WS-VALIDATION-FAIL-REASON is 100; the account lookup, credit limit and expiration checks are not made (DTPR-C02-AC-03)
4. **Given** DALYTRAN-CARD-NUM: 4000000000000002; Card in cross-reference: yes; XREF-ACCT-ID: 00000000011, **when** the transaction's card number is not found in the card cross-reference, **then** Reason stays 0 and account 00000000011 is looked up for the credit limit and expiration checks (DTPR-C02-AC-04)
5. **Given** DALYTRAN-CARD-NUM: 5500000000000004; Card in cross-reference: no, **when** the transaction's card number is not found in the card cross-reference, **then** Reject record trailer holds reason 100 and 'INVALID CARD NUMBER FOUND'; reject count goes up by 1 and the job ends with return code 4 (DTPR-C02-AC-05)
6. **Given** DALYTRAN-CARD-NUM: 5500000000000004; Card in cross-reference: yes, **when** the transaction's card number is not found in the card cross-reference, **then** Reason stays 0 and the account lookup is made (DTPR-C02-AC-06)
7. **Given** DALYTRAN-CARD-NUM: 4111111111111111; Card in cross-reference: no, **when** the transaction's card number is not found in the card cross-reference, **then** Failure reason is 100 (card not found); the transaction is written to the daily rejects file (DTPR-C02-AC-07)
8. **Given** DALYTRAN-CARD-NUM: 4111111111111111; Card in cross-reference: yes, **when** the transaction's card number is not found in the card cross-reference, **then** Failure reason stays 0 and validation goes on to the account checks (DTPR-C02-AC-08)
9. **Given** Card number: 4111000011112222; Linked account: 00000000099 (not on account master), **when** the account linked to the card is not on the account master, **then** Transaction rejected with reason 0101 'ACCOUNT RECORD NOT FOUND' and written to the daily rejects file (DTPR-C02-AC-09)
10. **Given** credit limit: $5,000.00; cycle credit: $4,800.00; cycle debit: $0.00; transaction amount: $250.00, **when** the card's account is found and its credit limit is less than the cycle credit total minus the cycle debit total plus the transaction amount, **then** The projection is $5,050.00, which is over the limit, so the transaction is rejected with 102 'OVERLIMIT TRANSACTION'. (DTPR-C02-AC-10)
11. **Given** credit limit: $5,000.00; cycle credit: $4,800.00; cycle debit: $0.00; transaction amount: $200.00, **when** the card's account is found and its credit limit is less than the cycle credit total minus the cycle debit total plus the transaction amount, **then** The projection is exactly $5,000.00, so the transaction passes the limit check. (DTPR-C02-AC-11)
12. **Given** current balance: $4,900.00; credit limit: $5,000.00; cycle credit: $100.00; cycle debit: $0.00; transaction amount: $300.00, **when** transaction validation runs, **then** The projection is $400.00, so the transaction passes even though balance plus amount would be $5,200.00. (DTPR-C02-AC-12)
13. **Given** Card found in cross-reference: yes; Account found: yes; ACCT-EXPIRAION-DATE: 2024-12-31; DALYTRAN-ORIG-TS (date part): 2025-01-02, **when** the account linked to the card is found, WHEN the account expiration date is earlier than the transaction date, **then** Failure reason is 103 (transaction after account expiration); the transaction is rejected (DTPR-C02-AC-13)
14. **Given** Account found: yes; ACCT-EXPIRAION-DATE: 2027-12-31; DALYTRAN-ORIG-TS (date part): 2025-01-02, **when** the account linked to the card is found, WHEN the account expiration date is earlier than the transaction date, **then** Failure reason is not set to 103; if no other check fails the transaction is posted (DTPR-C02-AC-14)
15. **Given** Account found: no, **when** the account linked to the card is found, WHEN the account expiration date is earlier than the transaction date, **then** The expiration check is not made; failure reason is 101 'ACCOUNT RECORD NOT FOUND' (DTPR-C02-AC-15)
16. **Given** Account found: yes; ACCT-EXPIRAION-DATE: 2025-03-31; DALYTRAN-ORIG-TS: 2025-04-01-10.15.00.000000, **when** the linked account was found, WHEN the account expiration date is earlier than the transaction's original date, **then** Failure reason 103 with description 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION' is written in the reject record's trailer (DTPR-C02-AC-16)
17. **Given** Account found: yes; Balance after transaction: over credit limit; ACCT-EXPIRAION-DATE: 2025-03-31; DALYTRAN-ORIG-TS: 2025-04-01-10.15.00.000000, **when** the linked account was found, WHEN the account expiration date is earlier than the transaction's original date, **then** The reason 102 'OVERLIMIT TRANSACTION' is replaced, and the reject shows 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION' (DTPR-C02-AC-17)
18. **Given** ACCT-EXPIRAION-DATE: 2025-06-30; DALYTRAN-ORIG-TS (date part): 2025-07-15, **when** the account is found and its expiration date is earlier than the transaction date, **then** WS-VALIDATION-FAIL-REASON is set to 103; the transaction is written to the daily rejects file and not posted (DTPR-C02-AC-18)
19. **Given** ACCT-EXPIRAION-DATE: 2025-06-30; DALYTRAN-ORIG-TS (date part): 2025-06-30, **when** the account is found and its expiration date is earlier than the transaction date, **then** No failure reason 103 is set (an expiry date equal to the transaction date is accepted) (DTPR-C02-AC-19)
20. **Given** projection: over the credit limit; transaction date: after account expiration, **when** a transaction is both over the limit and dated after the account's expiration date, **then** The reject record carries 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION', not 102. (DTPR-C02-AC-20)

## Requirements

### Functional requirements

- **DTPR-REQ-F-013** (business rule): The system shall look up the transaction's card in the card cross-reference first and shall look up the linked account only when the card was found. Rules: DTPR-BR-014, DTPR-BR-015, DTPR-BR-016.
- **DTPR-REQ-F-014** (business rule): If the transaction's card number is not found in the card cross-reference, then the system shall record failure reason 100 'INVALID CARD NUMBER FOUND' and skip the account checks. Rules: DTPR-BR-015, DTPR-BR-016, DTPR-BR-017.
- **DTPR-REQ-F-015** (business rule): If the account linked to the card is not on the account master, then the system shall reject the transaction with reason 101 'ACCOUNT RECORD NOT FOUND' and shall not evaluate the credit-limit or expiration checks. Rules: DTPR-BR-018.
- **DTPR-REQ-F-016** (business rule): If the card's account is found and its credit limit is less than the cycle credit total minus the cycle debit total plus the transaction amount, then the system shall reject the transaction with reason 102 'OVERLIMIT TRANSACTION', passing a projection equal to the limit. Rules: DTPR-BR-019.
- **DTPR-REQ-F-017** (business rule): The system shall base the credit-limit check on the current billing cycle's credit and debit totals plus the new transaction, not on the account's current balance. Rules: DTPR-BR-020.
- **DTPR-REQ-F-018** (business rule): While the account linked to the card is found, when the account expiration date is earlier than the transaction's original date, the system shall record failure reason 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION'. Rules: DTPR-BR-021, DTPR-BR-022, DTPR-BR-023.
- **DTPR-REQ-F-019** (business rule): When a transaction is both over the credit limit and dated after the account's expiration date, the system shall record only reason 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION'. Rules: DTPR-BR-024.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-014 | Sequence card and account validation | business rule | THE daily posting batch SHALL look up the card in the card cross-reference first and SHALL look up the linked account only when the card was found. | high | app/cbl/CBTRN02C.cbl:370-378, app/cbl/CBTRN02C.cbl:380-392, app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:211-216 |
| DTPR-BR-015 | Reject transaction for unknown card | business rule | IF the transaction's card number is not found in the card cross-reference, THEN THE Transaction Validation SHALL set the failure reason (`WS-VALIDATION-FAIL-REASON`) to 100 and skip the account checks; when the card is found and the reason is 0, proceed to the account lookup (physical store: `XREF-FILE`) | medium | app/cbl/CBTRN02C.cbl:370-376,380,382-385,391, app/cbl/CBTRN02C.cbl:370-392 |
| DTPR-BR-016 | Reject transaction with unknown card | business rule | IF the transaction's card number is not found in the card cross-reference, THEN THE Transaction Validation SHALL record (`XREF-FILE`) failure reason `100` with description `'INVALID CARD NUMBER FOUND'` and skip the account checks; proceed to the account lookup only when the reason is still `0` | medium | app/cbl/CBTRN02C.cbl:370-376,380,382-387,391, app/cbl/CBTRN02C.cbl:370-392 |
| DTPR-BR-017 | Reject unknown card number | business rule | IF the transaction's card number is not found in the card cross-reference, THEN THE Transaction Validation SHALL set the validation failure reason to 100 (card not found) (physical store: `XREF-FILE`) | medium | app/cbl/CBTRN02C.cbl:380,382-385,391, app/cbl/CBTRN02C.cbl:370-392 |
| DTPR-BR-018 | Reject transaction for unknown account | business rule | WHEN the account linked to the card is not on the account master, THE daily posting batch SHALL reject the transaction with reason 101 'ACCOUNT RECORD NOT FOUND' and SHALL NOT evaluate the credit-limit or expiration checks. | high | app/cbl/CBTRN02C.cbl:370-378, app/cbl/CBTRN02C.cbl:380-392, app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:211-216 |
| DTPR-BR-019 | Reject transaction exceeding credit limit | business rule | WHEN the card's account is found and its credit limit is less than the cycle credit total minus the cycle debit total plus the transaction amount, THE transaction validation SHALL reject the transaction with reason 102 'OVERLIMIT TRANSACTION'; a projection equal to the limit passes. | high | app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:545-552, app/cbl/CBTRN02C.cbl:208-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-020 | Over-credit-limit rejection | business rule | THE transaction validation SHALL base the limit check on the current billing cycle's credit and debit totals plus the new transaction, not on the account's current balance. | high | app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:545-552, app/cbl/CBTRN02C.cbl:208-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-021 | Reject transaction after account expiration | business rule | WHILE the account linked to the card is found, WHEN the account expiration date is earlier than the transaction date, THE Transaction Validation SHALL set the validation failure reason to 103 (transaction after account expiration) | medium | app/cbl/CBTRN02C.cbl:414-417,420-421, app/cbl/CBTRN02C.cbl:414-420 |
| DTPR-BR-022 | Reject transaction after account expiration | business rule | WHILE the linked account was found, WHEN the account expiration date is earlier than the transaction's original date, THE Transaction Validation SHALL record failure reason `103` with description `'TRANSACTION RECEIVED AFTER ACCT EXPIRATION'` | medium | app/cbl/CBTRN02C.cbl:414-421, app/cbl/CBTRN02C.cbl:414-420 |
| DTPR-BR-023 | Reject transaction after account expiration | business rule | WHEN the account is found and its expiration date is earlier than the transaction date, THE Transaction Validation SHALL set the failure reason (`WS-VALIDATION-FAIL-REASON`) to 103 | medium | app/cbl/CBTRN02C.cbl:414-417,420, app/cbl/CBTRN02C.cbl:414-420 |
| DTPR-BR-024 | Over-credit-limit rejection | business rule | WHEN a transaction is both over the limit and dated after the account's expiration date, THE transaction validation SHALL record only reason 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION', because the expiration check runs after the limit check and overwrites reason 102. | high | app/cbl/CBTRN02C.cbl:393-422, app/cbl/CBTRN02C.cbl:545-552, app/cbl/CBTRN02C.cbl:208-216, app/cpy/CVACT01Y.cpy:7-14 |

### Key entities

- CVACT01Y (file record)
- CVACT03Y (file record)
- CVTRA01Y (file record)
- CVTRA05Y (file record)
- CVTRA06Y (file record)

### Needs clarification

- SME-039: How should the over-credit-limit check measure exposure? Today it uses cycle credits minus cycle debits plus the transaction amount, and because debits are stored as negative amounts this effectively adds payments. Is that intended, or should the check use the current balance plus the transaction amount? Should cash transactions also be checked against the cash credit limit? (Credit risk / card product owner) On DTPR-BR-021, DTPR-BR-022, DTPR-BR-015, DTPR-BR-016, DTPR-BR-017, DTPR-BR-023, DTPR-BR-019, DTPR-BR-024, DTPR-BR-014, DTPR-BR-018.
- DEF-018: Is this intended? Negative amounts are stored in the cycle debit total as negative values (2800-UPDATE-ACCOUNT-REC), so 'credit minus debit' adds their magnitude back and raises the projection instead of lowering it. The check also ignores the current balance and any earlier cycles, and reason 103 silently overwrites reason 102. (Subject-matter expert) On DTPR-BR-019, DTPR-BR-024.

### Decision table gaps

None.
