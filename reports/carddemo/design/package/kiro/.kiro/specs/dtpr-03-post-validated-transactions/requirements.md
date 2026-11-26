# Requirements: Post validated transactions (DTPR-C03)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Posts each validated daily transaction: it adds the amount to the matching category balance, updates the account's current balance and cycle credit or debit totals, and writes the posted transaction, stamped with the run time, to the transaction master. It serves the card issuer and keeps balances in line with the day's activity. It must never post in the wrong order (category balance, then account, then transaction), lose an amount, or let a storage failure pass unnoticed; any read or write error on these files stops the run.

**User story:** As a card issuer, I want each validated daily transaction posted to its category balance, its account and the transaction master file, so that balances and cycle totals reflect the day's activity.

## Requirements

### Requirement 1: DTPR-REQ-F-020 (business rule)

#### Acceptance criteria

1. When a daily transaction passes validation, the system shall first update the category balance, then update the account, and then write the posted transaction to the transaction file. (rules DTPR-BR-025, DTPR-BR-026)
2. GIVEN Validation result: passed; Transaction file status on write: '00' WHEN a transaction passes validation THEN Category balance, account and transaction file are all updated (DTPR-C03-AC-01; DTPR-BR-025)
3. GIVEN validation result: passed WHEN a daily transaction passes validation THEN Category balance, then account, are updated, and then the transaction record is written. (DTPR-C03-AC-02; DTPR-BR-026)

### Requirement 2: DTPR-REQ-F-021 (design note)

#### Acceptance criteria

1. When a transaction passes validation, the system shall look up the category balance record for the card's account, the transaction type and the transaction category. (rules DTPR-BR-027)
2. GIVEN Account: 00000000012; Transaction type: 01; Category: 0001 WHEN a transaction passes validation THEN The batch reads the category balance for account 00000000012, type '01', category 0001 (DTPR-C03-AC-03; DTPR-BR-027)

### Requirement 3: DTPR-REQ-F-022 (business rule)

#### Acceptance criteria

1. When a category balance record already exists for the account, type and category, the system shall add the transaction amount to that balance and save the record. (rules DTPR-BR-028)
2. GIVEN Existing category balance: $500.00; Transaction amount: $25.00 WHEN a category balance record already exists for the account, type and category THEN The category balance becomes $525.00 (DTPR-C03-AC-04; DTPR-BR-028)
3. GIVEN Existing category balance: $500.00; Transaction amount: -$40.00 WHEN a category balance record already exists for the account, type and category THEN The category balance becomes $460.00 (DTPR-C03-AC-05; DTPR-BR-028)

### Requirement 4: DTPR-REQ-F-023 (business rule)

#### Acceptance criteria

1. When no category balance record exists for the account, type and category, the system shall create one with a balance equal to the transaction amount and display 'TCATBAL record not found for key : ... Creating.'. (rules DTPR-BR-029)
2. GIVEN Category balance record: none for account 00000000012, type '01', category 0001; Transaction amount: $25.00 WHEN no category balance record exists for the account, type and category THEN A new category balance record is created with balance $25.00 (DTPR-C03-AC-06; DTPR-BR-029)

### Requirement 5: DTPR-REQ-F-024 (error handling)

#### Acceptance criteria

1. If reading the category balance fails for any reason other than record not found, or creating or saving it fails, then the system shall display 'ERROR READING TRANSACTION BALANCE FILE', 'ERROR WRITING TRANSACTION BALANCE FILE' or 'ERROR REWRITING TRANSACTION BALANCE FILE' with the file status and abend. (rules DTPR-BR-030)
2. GIVEN Category balance file status on read: '35' WHEN reading the category balance fails for any reason other than record not found, or creating or saving it fails THEN 'ERROR READING TRANSACTION BALANCE FILE' is displayed and the batch abends (DTPR-C03-AC-07; DTPR-BR-030)
3. GIVEN Category balance file status on rewrite: '22' WHEN reading the category balance fails for any reason other than record not found, or creating or saving it fails THEN 'ERROR REWRITING TRANSACTION BALANCE FILE' is displayed and the batch abends (DTPR-C03-AC-08; DTPR-BR-030)

### Requirement 6: DTPR-REQ-F-025 (business rule)

#### Acceptance criteria

1. When a daily transaction passes validation, the system shall add the transaction amount to the account's current balance. (rules DTPR-BR-031)
2. GIVEN current balance: $1,200.00; transaction amount: $75.25 WHEN a daily transaction passes validation THEN Current balance becomes $1,275.25. (DTPR-C03-AC-09; DTPR-BR-031)
3. GIVEN current balance: $1,275.25; transaction amount: -$100.00 WHEN a daily transaction passes validation THEN Current balance becomes $1,175.25. (DTPR-C03-AC-10; DTPR-BR-031)

### Requirement 7: DTPR-REQ-F-026 (business rule)

#### Acceptance criteria

1. When a posted transaction amount is zero or positive, the system shall add it to the account's current billing-cycle credit total. (rules DTPR-BR-032)
2. GIVEN cycle credit: $300.00; transaction amount: $75.25 WHEN a posted transaction amount is zero or positive THEN Cycle credit becomes $375.25; cycle debit is unchanged. (DTPR-C03-AC-11; DTPR-BR-032)

### Requirement 8: DTPR-REQ-F-027 (business rule)

#### Acceptance criteria

1. When a posted transaction amount is negative, the system shall add it as a negative value to the account's current billing-cycle debit total. (rules DTPR-BR-033)
2. GIVEN cycle debit: -$50.00; transaction amount: -$100.00 WHEN a posted transaction amount is negative THEN Cycle debit becomes -$150.00; cycle credit is unchanged. (DTPR-C03-AC-12; DTPR-BR-033)

### Requirement 9: DTPR-REQ-F-028 (design note)

#### Acceptance criteria

1. The system shall save the updated balance and cycle totals back to the account record before the transaction itself is written. (rules DTPR-BR-034)
2. GIVEN transaction amount: $75.25; account: found during validation WHEN account posting runs THEN The account record is rewritten with the new balance and cycle credit. (DTPR-C03-AC-13; DTPR-BR-034)

### Requirement 10: DTPR-REQ-F-029 (historical artifact)

#### Acceptance criteria

1. If the account record cannot be rewritten because it is not found, then the system shall set reason 109 'ACCOUNT RECORD NOT FOUND' and still write the transaction to the transaction file without rejecting it or counting it as rejected. (rules DTPR-BR-035)
2. GIVEN account rewrite: record not found WHEN the account record cannot be rewritten because it is not found THEN Reason 109 'ACCOUNT RECORD NOT FOUND' is set in memory only; the transaction is still written, no reject record is written, and the reason is cleared for the next transaction. (DTPR-C03-AC-14; DTPR-BR-035)

### Requirement 11: DTPR-REQ-F-030 (design note)

#### Acceptance criteria

1. When a daily transaction passes validation, the system shall build the posted transaction from the daily transaction's ID, type, category, source, description, amount, merchant ID, name, city and ZIP, card number and original timestamp. (rules DTPR-BR-036)
2. GIVEN daily transaction ID: 0000000000001234; original timestamp: 2025-03-01-09.30.00.000000 WHEN a daily transaction passes validation THEN The posted transaction has ID 0000000000001234 and original timestamp 2025-03-01-09.30.00.000000, with all other details copied over. (DTPR-C03-AC-15; DTPR-BR-036)

### Requirement 12: DTPR-REQ-F-031 (design note)

#### Acceptance criteria

1. The system shall stamp each posted transaction with the run's current date and time in the form YYYY-MM-DD-HH.MM.SS.hh0000. (rules DTPR-BR-037)
2. GIVEN a daily transaction that has passed validation, and a posting run whose clock reads 2026-11-25 14:05:09.37 WHEN the posted transaction is written THEN its processed timestamp is '2026-11-25-14.05.09.370000' (YYYY-MM-DD-HH.MM.SS, then hundredths of a second, then '0000') (DTPR-C03-AC-17; DTPR-BR-037)

### Requirement 13: DTPR-REQ-F-032 (error handling)

#### Acceptance criteria

1. If writing the posted transaction fails, then the system shall display 'ERROR WRITING TO TRANSACTION FILE' with the file status and abend the run. (rules DTPR-BR-025, DTPR-BR-038)
2. GIVEN Validation result: passed; Transaction file status on write: '00' WHEN a transaction passes validation THEN Category balance, account and transaction file are all updated (DTPR-C03-AC-01; DTPR-BR-025)
3. GIVEN transaction file write status: 22 (duplicate key) WHEN writing the posted transaction fails THEN 'ERROR WRITING TO TRANSACTION FILE' and the status are displayed, and the program abends. (DTPR-C03-AC-16; DTPR-BR-038)
