# Feature specification: Post validated transactions

**Feature:** DTPR-C03 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C03)

As a card issuer, I want each validated daily transaction posted to its category balance, its account and the transaction master file, so that balances and cycle totals reflect the day's activity.

Posts each validated daily transaction: it adds the amount to the matching category balance, updates the account's current balance and cycle credit or debit totals, and writes the posted transaction, stamped with the run time, to the transaction master. It serves the card issuer and keeps balances in line with the day's activity. It must never post in the wrong order (category balance, then account, then transaction), lose an amount, or let a storage failure pass unnoticed; any read or write error on these files stops the run.

**Acceptance scenarios:**

1. **Given** Validation result: passed; Transaction file status on write: '00', **when** a transaction passes validation, **then** Category balance, account and transaction file are all updated (DTPR-C03-AC-01)
2. **Given** validation result: passed, **when** a daily transaction passes validation, **then** Category balance, then account, are updated, and then the transaction record is written. (DTPR-C03-AC-02)
3. **Given** Account: 00000000012; Transaction type: 01; Category: 0001, **when** a transaction passes validation, **then** The batch reads the category balance for account 00000000012, type '01', category 0001 (DTPR-C03-AC-03)
4. **Given** Existing category balance: $500.00; Transaction amount: $25.00, **when** a category balance record already exists for the account, type and category, **then** The category balance becomes $525.00 (DTPR-C03-AC-04)
5. **Given** Existing category balance: $500.00; Transaction amount: -$40.00, **when** a category balance record already exists for the account, type and category, **then** The category balance becomes $460.00 (DTPR-C03-AC-05)
6. **Given** Category balance record: none for account 00000000012, type '01', category 0001; Transaction amount: $25.00, **when** no category balance record exists for the account, type and category, **then** A new category balance record is created with balance $25.00 (DTPR-C03-AC-06)
7. **Given** Category balance file status on read: '35', **when** reading the category balance fails for any reason other than record not found, or creating or saving it fails, **then** 'ERROR READING TRANSACTION BALANCE FILE' is displayed and the batch abends (DTPR-C03-AC-07)
8. **Given** Category balance file status on rewrite: '22', **when** reading the category balance fails for any reason other than record not found, or creating or saving it fails, **then** 'ERROR REWRITING TRANSACTION BALANCE FILE' is displayed and the batch abends (DTPR-C03-AC-08)
9. **Given** current balance: $1,200.00; transaction amount: $75.25, **when** a daily transaction passes validation, **then** Current balance becomes $1,275.25. (DTPR-C03-AC-09)
10. **Given** current balance: $1,275.25; transaction amount: -$100.00, **when** a daily transaction passes validation, **then** Current balance becomes $1,175.25. (DTPR-C03-AC-10)
11. **Given** cycle credit: $300.00; transaction amount: $75.25, **when** a posted transaction amount is zero or positive, **then** Cycle credit becomes $375.25; cycle debit is unchanged. (DTPR-C03-AC-11)
12. **Given** cycle debit: -$50.00; transaction amount: -$100.00, **when** a posted transaction amount is negative, **then** Cycle debit becomes -$150.00; cycle credit is unchanged. (DTPR-C03-AC-12)
13. **Given** transaction amount: $75.25; account: found during validation, **when** account posting runs, **then** The account record is rewritten with the new balance and cycle credit. (DTPR-C03-AC-13)
14. **Given** account rewrite: record not found, **when** the account record cannot be rewritten because it is not found, **then** Reason 109 'ACCOUNT RECORD NOT FOUND' is set in memory only; the transaction is still written, no reject record is written, and the reason is cleared for the next transaction. (DTPR-C03-AC-14)
15. **Given** daily transaction ID: 0000000000001234; original timestamp: 2025-03-01-09.30.00.000000, **when** a daily transaction passes validation, **then** The posted transaction has ID 0000000000001234 and original timestamp 2025-03-01-09.30.00.000000, with all other details copied over. (DTPR-C03-AC-15)
16. **Given** transaction file write status: 22 (duplicate key), **when** writing the posted transaction fails, **then** 'ERROR WRITING TO TRANSACTION FILE' and the status are displayed, and the program abends. (DTPR-C03-AC-16)
17. **Given** a daily transaction that has passed validation, and a posting run whose clock reads 2026-11-25 14:05:09.37, **when** the posted transaction is written, **then** its processed timestamp is '2026-11-25-14.05.09.370000' (YYYY-MM-DD-HH.MM.SS, then hundredths of a second, then '0000') (DTPR-C03-AC-17)

## Requirements

### Functional requirements

- **DTPR-REQ-F-020** (business rule): When a daily transaction passes validation, the system shall first update the category balance, then update the account, and then write the posted transaction to the transaction file. Rules: DTPR-BR-025, DTPR-BR-026.
- **DTPR-REQ-F-021** (design note): When a transaction passes validation, the system shall look up the category balance record for the card's account, the transaction type and the transaction category. Rules: DTPR-BR-027.
- **DTPR-REQ-F-022** (business rule): When a category balance record already exists for the account, type and category, the system shall add the transaction amount to that balance and save the record. Rules: DTPR-BR-028.
- **DTPR-REQ-F-023** (business rule): When no category balance record exists for the account, type and category, the system shall create one with a balance equal to the transaction amount and display 'TCATBAL record not found for key : ... Creating.'. Rules: DTPR-BR-029.
- **DTPR-REQ-F-024** (error handling): If reading the category balance fails for any reason other than record not found, or creating or saving it fails, then the system shall display 'ERROR READING TRANSACTION BALANCE FILE', 'ERROR WRITING TRANSACTION BALANCE FILE' or 'ERROR REWRITING TRANSACTION BALANCE FILE' with the file status and abend. Rules: DTPR-BR-030.
- **DTPR-REQ-F-025** (business rule): When a daily transaction passes validation, the system shall add the transaction amount to the account's current balance. Rules: DTPR-BR-031.
- **DTPR-REQ-F-026** (business rule): When a posted transaction amount is zero or positive, the system shall add it to the account's current billing-cycle credit total. Rules: DTPR-BR-032.
- **DTPR-REQ-F-027** (business rule): When a posted transaction amount is negative, the system shall add it as a negative value to the account's current billing-cycle debit total. Rules: DTPR-BR-033.
- **DTPR-REQ-F-028** (design note): The system shall save the updated balance and cycle totals back to the account record before the transaction itself is written. Rules: DTPR-BR-034.
- **DTPR-REQ-F-029** (historical artifact): If the account record cannot be rewritten because it is not found, then the system shall set reason 109 'ACCOUNT RECORD NOT FOUND' and still write the transaction to the transaction file without rejecting it or counting it as rejected. Rules: DTPR-BR-035.
- **DTPR-REQ-F-030** (design note): When a daily transaction passes validation, the system shall build the posted transaction from the daily transaction's ID, type, category, source, description, amount, merchant ID, name, city and ZIP, card number and original timestamp. Rules: DTPR-BR-036.
- **DTPR-REQ-F-031** (design note): The system shall stamp each posted transaction with the run's current date and time in the form YYYY-MM-DD-HH.MM.SS.hh0000. Rules: DTPR-BR-037.
- **DTPR-REQ-F-032** (error handling): If writing the posted transaction fails, then the system shall display 'ERROR WRITING TO TRANSACTION FILE' with the file status and abend the run. Rules: DTPR-BR-025, DTPR-BR-038.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-025 | Post transaction and maintain category balance | error handling | WHEN a transaction passes validation, THE daily posting batch SHALL update the category balance, then the account balances, then write the posted transaction, abending with 'ERROR WRITING TO TRANSACTION FILE' if the transaction write fails. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-026 | Assemble posted transaction record | business rule | WHEN a daily transaction passes validation, THE transaction posting SHALL first update the category balance, then update the account, and then write the posted transaction to the transaction file (TRANSACT-FILE). | high | app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:562-579, app/cbl/CBTRN02C.cbl:692-705, app/cbl/CBTRN02C.cbl:150-177 |
| DTPR-BR-027 | Locate category balance for transaction | design note | WHEN a transaction passes validation, THE daily posting batch SHALL look up the category balance record for the card's account, the transaction type and the transaction category. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-028 | Update existing category balance record | business rule | WHEN a category balance record already exists for the account, type and category, THE daily posting batch SHALL add the transaction amount to that balance and save the record. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-029 | Locate category balance for transaction | business rule | WHEN no category balance record exists for the account, type and category, THE daily posting batch SHALL create one with a balance equal to the transaction amount and display 'TCATBAL record not found for key : ... Creating.'. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-030 | Create or update category balance | error handling | WHEN reading the category balance fails for any reason other than record not found, or creating or saving it fails, THE daily posting batch SHALL display 'ERROR READING TRANSACTION BALANCE FILE', 'ERROR WRITING TRANSACTION BALANCE FILE' or 'ERROR REWRITING TRANSACTION BALANCE FILE' with the file status and abend. | high | app/cbl/CBTRN02C.cbl:467-501, app/cbl/CBTRN02C.cbl:503-524, app/cbl/CBTRN02C.cbl:526-542, app/cbl/CBTRN02C.cbl:424-444 |
| DTPR-BR-031 | Post transaction to account balances | business rule | WHEN a daily transaction passes validation, THE account posting SHALL add the transaction amount to the account's current balance. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-032 | Post transaction to account balances | business rule | WHEN a posted transaction amount is zero or positive, THE account posting SHALL add it to the account's current billing-cycle credit total. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-033 | Post transaction to account balances | business rule | WHEN a posted transaction amount is negative, THE account posting SHALL add it as a negative value to the account's current billing-cycle debit total, so the debit total grows more negative. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-034 | Post transaction to account balances | design note | THE account posting SHALL save the updated balance and cycle totals back to the account record (ACCOUNT-FILE) before the transaction itself is written. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-035 | Update account balances for posted transaction | historical artifact | WHEN the account record cannot be rewritten because it is not found, THE account posting SHALL set reason 109 'ACCOUNT RECORD NOT FOUND', but the transaction is still written to the transaction file and is neither rejected nor counted as rejected. | high | app/cbl/CBTRN02C.cbl:545-560, app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:206-216, app/cpy/CVACT01Y.cpy:7-14 |
| DTPR-BR-036 | Assemble posted transaction record | design note | WHEN a daily transaction passes validation, THE transaction posting SHALL build the posted transaction from the daily transaction's ID, type, category, source, description, amount, merchant ID, name, city and ZIP, card number and original timestamp. | high | app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:562-579, app/cbl/CBTRN02C.cbl:692-705, app/cbl/CBTRN02C.cbl:150-177 |
| DTPR-BR-037 | Assemble posted transaction record | design note | THE transaction posting SHALL stamp each posted transaction with the run's current date and time in the form YYYY-MM-DD-HH.MM.SS.hh0000 (hundredths of a second followed by '0000'). | high | app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:562-579, app/cbl/CBTRN02C.cbl:692-705, app/cbl/CBTRN02C.cbl:150-177 |
| DTPR-BR-038 | Write posted transaction record | error handling | WHEN writing the posted transaction fails, THE transaction posting SHALL display 'ERROR WRITING TO TRANSACTION FILE' with the file status and abend the run. | high | app/cbl/CBTRN02C.cbl:424-444, app/cbl/CBTRN02C.cbl:562-579, app/cbl/CBTRN02C.cbl:692-705, app/cbl/CBTRN02C.cbl:150-177 |

### Key entities

- CVACT01Y (file record)
- CVACT03Y (file record)
- CVTRA01Y (file record)
- CVTRA05Y (file record)
- CVTRA06Y (file record)

### Needs clarification

- SME-040: When posting a transaction and the account record cannot be saved (failure reason 109), should the run stop, should the transaction go to the daily rejects file, or should the posted transaction still be written? (Card business rules team) On DTPR-BR-034, DTPR-BR-035, DTPR-BR-030, DTPR-BR-037, DTPR-BR-038.
- SME-041: Posting one transaction updates the category balance, then the account, then writes the posted transaction. If a later step fails, must the earlier updates be reversed, so that all three succeed or fail together? (Batch operations team) On DTPR-BR-034, DTPR-BR-035, DTPR-BR-030, DTPR-BR-037, DTPR-BR-038.
- SME-042: Each posting run replaces the contents of the posted-transaction master. Is that intended, or should posted transactions accumulate across days? (Card operations / batch operations owner) On DTPR-BR-037.
- DEF-003: Is this intended? When the account rewrite fails, reason 109 is set after the posting decision has been made. The transaction is still written, nothing goes to the rejects file, the reject count is unchanged, and the run does not abend. Rewrite failures other than INVALID KEY are not checked at all, so the account and transaction files can disagree. (Subject-matter expert) On DTPR-BR-033, DTPR-BR-034, DTPR-BR-035.
- DEF-009: Is this intended? Posting is not all-or-nothing: the category balance is saved before the account update, and if the account rewrite fails (reason 109 'ACCOUNT RECORD NOT FOUND') the batch neither abends nor rejects; it still writes the transaction, leaving the category balance and transaction file out of step with the account. (Subject-matter expert) On DTPR-BR-029, DTPR-BR-030.
- DEF-073: Is this intended? The category balance and the account are updated before the transaction is written. If the write then fails (for example a duplicate transaction ID), the run abends after those updates were already made. (Subject-matter expert) On DTPR-BR-037, DTPR-BR-038.

### Decision table gaps

None.
