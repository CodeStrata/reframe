# Requirements: Calculate and post monthly interest (DTPR-C05)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Calculates monthly interest on each category balance (balance × rate ÷ 1200) at the rate for the account's disclosure group, falling back to the 'DEFAULT' group's rate when the group has none. It writes each interest charge as a system transaction, then adds the account's total interest to its balance and resets its cycle totals to zero. It serves the card issuer, who must charge customers the right interest. It must never use the wrong rate, charge interest at a rate of 0, or carry on when an account or card cross-reference is missing.

**User story:** As a card issuer, I want monthly interest calculated on each category balance at the account group's rate and posted to the account, so that customers are charged the correct interest.

## Requirements

### Requirement 1: DTPR-REQ-F-038 (design note)

#### Acceptance criteria

1. The system shall read the category balance file in order, one record at a time, processing each record until the end of the file is reached. (rules DTPR-BR-044)
2. GIVEN category balance records: 3 WHEN interest batch runs THEN All 3 records are processed, then the end of file is detected (DTPR-C05-AC-01; DTPR-BR-044)

### Requirement 2: DTPR-REQ-F-039 (business rule)

#### Acceptance criteria

1. When a category balance belongs to a different account from the previous one, the system shall post the previous account's accumulated interest (except for the first account of the run), reset the interest total to 0, and read the new account and its card cross-reference. (rules DTPR-BR-045)
2. GIVEN previous account: 00000000001; next balance's account: 00000000002; interest accumulated for 00000000001: 12.50 WHEN a category balance belongs to a different account from the previous one THEN 12.50 is posted to account 00000000001, the total restarts at 0 and account 00000000002 is read (DTPR-C05-AC-02; DTPR-BR-045)
3. GIVEN first balance of the run, account: 00000000001 WHEN a category balance belongs to a different account from the previous one THEN Nothing is posted; account 00000000001 and its cross-reference are read (DTPR-C05-AC-03; DTPR-BR-045)

### Requirement 3: DTPR-REQ-F-040 (business rule)

#### Acceptance criteria

1. When the system processes a category balance, the system shall look up the interest rate in the disclosure group file using the account's group, the balance's transaction type and its transaction category. (rules DTPR-BR-046)
2. GIVEN account group: GOLD; transaction type: 01; transaction category: 0001 WHEN the interest batch processes a category balance THEN The rate is read from the disclosure group record keyed GOLD / 01 / 0001 (DTPR-C05-AC-04; DTPR-BR-046)

### Requirement 4: DTPR-REQ-F-041 (business rule)

#### Acceptance criteria

1. When no group-specific rate exists for a category balance, the system shall use the 'DEFAULT' group rate. (rules DTPR-BR-047)
2. GIVEN DISCGRP read status: '35' WHEN an interest rate is needed for a category balance THEN 'ERROR READING DISCLOSURE GROUP FILE' displayed and the job abends. (DTPR-C05-AC-05; DTPR-BR-047)

### Requirement 5: DTPR-REQ-F-042 (business rule)

#### Acceptance criteria

1. If the interest rate lookup fails for any reason other than no group-specific rate existing, then the system shall abend. (rules DTPR-BR-047)
2. GIVEN DISCGRP read status: '35' WHEN an interest rate is needed for a category balance THEN 'ERROR READING DISCLOSURE GROUP FILE' displayed and the job abends. (DTPR-C05-AC-05; DTPR-BR-047)

### Requirement 6: DTPR-REQ-F-043 (business rule)

#### Acceptance criteria

1. When a category balance has a non-zero interest rate, the system shall compute monthly interest as balance times rate divided by 1200 and add it to the account's total interest. (rules DTPR-BR-048)
2. GIVEN Category balance: 1200.00; Interest rate: 18.00 WHEN a category balance has a non-zero interest rate THEN Monthly interest = 1200.00 x 18.00 / 1200 = 18.00, added to the account's total interest and an interest transaction written. (DTPR-C05-AC-06; DTPR-BR-048)
3. GIVEN Category balance: 500.00; Interest rate: 0 WHEN a category balance has a non-zero interest rate THEN No interest computed and no transaction written. (DTPR-C05-AC-07; DTPR-BR-048)

### Requirement 7: DTPR-REQ-F-044 (business rule)

#### Acceptance criteria

1. When monthly interest has been computed for a category balance, the system shall write a transaction with id run-date plus sequence suffix, type '01', category '05', source 'System', description 'Int. for a/c ' plus account id, the interest amount, the card number and the current timestamp, abending if the write fails. (rules DTPR-BR-049, DTPR-BR-048)
2. GIVEN Category balance: 1200.00; Interest rate: 18.00 WHEN a category balance has a non-zero interest rate THEN Monthly interest = 1200.00 x 18.00 / 1200 = 18.00, added to the account's total interest and an interest transaction written. (DTPR-C05-AC-06; DTPR-BR-048)
3. GIVEN Category balance: 500.00; Interest rate: 0 WHEN a category balance has a non-zero interest rate THEN No interest computed and no transaction written. (DTPR-C05-AC-07; DTPR-BR-048)
4. GIVEN TRANSACT write status: not '00' WHEN monthly interest has been computed for a category balance THEN 'ERROR WRITING TRANSACTION RECORD' displayed and the job abends. (DTPR-C05-AC-08; DTPR-BR-049)

### Requirement 8: DTPR-REQ-F-045 (business rule)

#### Acceptance criteria

1. When the rate found for a category balance is 0, the system shall calculate no interest for that balance, write no interest transaction for it and add nothing to the account's interest total. (rules DTPR-BR-050)
2. GIVEN category balance: 500.00; disclosure group rate: 0.00 WHEN the rate found for a category balance is 0 THEN No interest transaction is written and the account's interest total is unchanged (DTPR-C05-AC-09; DTPR-BR-050)
3. GIVEN category balance: 500.00; disclosure group rate: 18.00 WHEN the rate found for a category balance is 0 THEN Interest is calculated for the balance and an interest transaction is written (DTPR-C05-AC-10; DTPR-BR-050)

### Requirement 9: DTPR-REQ-F-046 (historical artifact)

#### Acceptance criteria

1. When interest is calculated for a category balance, the system shall calculate and post no fee, as the fee step is marked 'To be implemented'. (rules DTPR-BR-051)
2. GIVEN category balance: 500.00; disclosure group rate: 18.00 WHEN interest is calculated for a category balance THEN Interest is calculated; no fee transaction is written and no fee is added to the account (DTPR-C05-AC-11; DTPR-BR-051)

### Requirement 10: DTPR-REQ-F-047 (business rule)

#### Acceptance criteria

1. When the system finishes an account's category balances, the system shall add the account's total interest to its current balance, set its current-cycle credit and current-cycle debit to 0, and rewrite the account record. (rules DTPR-BR-052)
2. GIVEN current balance: 1,000.00; total interest: 15.00; current-cycle credit: 300.00; current-cycle debit: 1,200.00 WHEN the interest batch finishes an account's category balances THEN Current balance 1,015.00, current-cycle credit 0.00, current-cycle debit 0.00, record rewritten (DTPR-C05-AC-12; DTPR-BR-052)
3. GIVEN current balance: 200.00; total interest: 0.00 (all rates zero); current-cycle debit: 50.00 WHEN the interest batch finishes an account's category balances THEN Current balance stays 200.00 and current-cycle debit is set to 0.00 (DTPR-C05-AC-13; DTPR-BR-052)

### Requirement 11: DTPR-REQ-F-048 (business rule)

#### Acceptance criteria

1. When the end of the category balance file is reached, the system shall post the last account's accumulated interest to that account before closing its files. (rules DTPR-BR-053)
2. GIVEN last account in the file: 00000000050; accumulated interest: 8.25 WHEN the end of the category balance file is reached THEN 8.25 is added to account 00000000050's current balance and the account is rewritten (DTPR-C05-AC-14; DTPR-BR-053)

### Requirement 12: DTPR-REQ-F-049 (error handling)

#### Acceptance criteria

1. If the rewrite of the account record fails, then the system shall display 'ERROR RE-WRITING ACCOUNT FILE' with the file status and abend with code 999. (rules DTPR-BR-054)
2. GIVEN account rewrite file status: 23 WHEN the rewrite of the account record fails THEN 'ERROR RE-WRITING ACCOUNT FILE' is displayed with the status and the run abends with code 999 (DTPR-C05-AC-15; DTPR-BR-054)

### Requirement 13: DTPR-REQ-F-050 (error handling)

#### Acceptance criteria

1. If the account of a category balance is not on the account master file, then the system shall display 'ACCOUNT NOT FOUND: ' with the account number and 'ERROR READING ACCOUNT FILE' with the file status, and abend with code 999, leaving accounts already rewritten in this run as they are. (rules DTPR-BR-055)
2. GIVEN an interest run in which account 00000000001 has already been rewritten with its interest, and the next category balance belongs to account 00000000099, which is not on the account master WHEN the run reaches that category balance and looks up account 00000000099 THEN it displays 'ACCOUNT NOT FOUND: ' with 00000000099 and 'ERROR READING ACCOUNT FILE' with the file status, abends with code 999, and account 00000000001 keeps the interest already posted to it (DTPR-C05-AC-16; DTPR-BR-055)

### Requirement 14: DTPR-REQ-F-051 (error handling)

#### Acceptance criteria

1. If no card cross-reference exists for the account of a category balance, then the system shall display 'ACCOUNT NOT FOUND: ' with the account number and 'ERROR READING XREF FILE' with the file status, and abend with code 999. (rules DTPR-BR-056)
2. GIVEN a category balance for account 00000000099, which has no card cross-reference WHEN the run looks up the card cross-reference for account 00000000099 THEN it displays 'ACCOUNT NOT FOUND: ' with 00000000099 and 'ERROR READING XREF FILE' with the file status, and abends with code 999 (DTPR-C05-AC-17; DTPR-BR-056)
