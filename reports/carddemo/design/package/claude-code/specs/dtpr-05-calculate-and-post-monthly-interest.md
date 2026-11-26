# Calculate and post monthly interest (DTPR-C05)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

#### CVACT01Y

File record of CBACT04C. Source: `app/cpy/CVACT01Y.cpy`.

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

File record of CBACT04C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA01Y

File record of CBACT04C. Source: `app/cpy/CVTRA01Y.cpy`.

Record `TRAN-CAT-BAL-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-CAT-KEY |  |  | group |  |  |  |
| TRANCAT-ACCT-ID | TRAN-CAT-KEY | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| TRANCAT-TYPE-CD | TRAN-CAT-KEY | X(02) | text, 2 characters |  |  |  |
| TRANCAT-CD | TRAN-CAT-KEY | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-CAT-BAL |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| FILLER |  | X(22) | text, 22 characters |  |  |  |

#### CVTRA02Y

File record of CBACT04C. Source: `app/cpy/CVTRA02Y.cpy`.

Record `DIS-GROUP-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| DIS-GROUP-KEY |  |  | group |  |  |  |
| DIS-ACCT-GROUP-ID | DIS-GROUP-KEY | X(10) | text, 10 characters |  |  |  |
| DIS-TRAN-TYPE-CD | DIS-GROUP-KEY | X(02) | text, 2 characters |  |  |  |
| DIS-TRAN-CAT-CD | DIS-GROUP-KEY | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| DIS-INT-RATE |  | S9(04)V99 | signed decimal, 4 integer and 2 fraction digits (zoned decimal) |  |  |  |
| FILLER |  | X(28) | text, 28 characters |  |  |  |

#### CVTRA05Y

File record of CBACT04C. Source: `app/cpy/CVTRA05Y.cpy`.

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


## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-044 | Iterate category balances and post final account | design note | THE interest batch SHALL read the category balance file in order, one record at a time, processing each record until the end of the file is reached. | medium | app/cbl/CBACT04C.cbl:188-222, app/cbl/CBACT04C.cbl:325-348 |
| DTPR-BR-045 | Handle account change between balances | business rule | WHEN a category balance belongs to a different account from the previous one, THE interest batch SHALL post the previous account's accumulated interest (except for the first account of the run), reset the interest total to 0, and read the new account and its card cross-reference. | high | app/cbl/CBACT04C.cbl:194-206, app/cbl/CBACT04C.cbl:372-413, app/cbl/CBACT04C.cbl:628-632 |
| DTPR-BR-046 | Look up rate and gate interest | business rule | WHEN the interest batch processes a category balance, THE interest batch SHALL look up the interest rate in the disclosure group file using the account's group, the balance's transaction type and its transaction category. | high | app/cbl/CBACT04C.cbl:210-217, app/cbl/CBACT04C.cbl:415-440, app/cbl/CBACT04C.cbl:462-468 |
| DTPR-BR-047 | Determine group rate with default fallback | business rule | WHEN an interest rate is needed for a category balance, THE Interest Rate Lookup SHALL retrieve the group-specific rate, fall back to the 'DEFAULT' group rate when no group-specific rate exists, and abend on any other lookup failure (physical store: `DISCGRP-FILE`) | medium | app/cbl/CBACT04C.cbl:415-416,422-426,428-430,434-439,443-444,452-454,458-459, app/cbl/CBACT04C.cbl:415-460 |
| DTPR-BR-048 | Compute monthly category interest | business rule | WHEN a category balance has a non-zero interest rate, THE Interest Calculation SHALL compute monthly interest as balance times rate divided by 1200, add it to the account's total interest, and generate an interest transaction | medium | app/cbl/CBACT04C.cbl:462,464-465,467-468, app/cbl/CBACT04C.cbl:462-470 |
| DTPR-BR-049 | Write system interest transaction | side effect | WHEN monthly interest has been computed for a category balance, THE Interest Transaction Generation SHALL write a transaction with id run-date plus sequence suffix, type '01', category '05', source 'System', description 'Int. for a/c ' plus account id, the interest amount, the card number and the current timestamp, abending if the write fails (physical store: `TRANSACT-FILE`) | medium | app/cbl/CBACT04C.cbl:473-474,476-480,482-498,500,507-509,513-514, app/cbl/CBACT04C.cbl:473-515 |
| DTPR-BR-050 | Look up rate and gate interest | business rule | WHEN the rate found for a category balance is 0, THE interest batch SHALL calculate no interest for that balance, write no interest transaction for it and add nothing to the account's interest total. | high | app/cbl/CBACT04C.cbl:210-217, app/cbl/CBACT04C.cbl:415-440, app/cbl/CBACT04C.cbl:462-468 |
| DTPR-BR-051 | Fee assessment not implemented | historical artifact | WHEN interest is calculated for a category balance, THE interest batch SHALL run a fee step that does nothing, so no fee is calculated or posted (the fee step is marked 'To be implemented'). | medium | app/cbl/CBACT04C.cbl:214-217, app/cbl/CBACT04C.cbl:518-520, app/jcl/INTCALC.jcl:20 |
| DTPR-BR-052 | Post accumulated interest to account | business rule | WHEN the interest batch finishes an account's category balances, THE interest batch SHALL add the account's total interest to its current balance, set its current-cycle credit and current-cycle debit to 0, and rewrite the account record. | high | app/cbl/CBACT04C.cbl:350-370, app/cbl/CBACT04C.cbl:628-632 |
| DTPR-BR-053 | Iterate category balances and post final account | business rule | WHEN the end of the category balance file is reached, THE interest batch SHALL post the last account's accumulated interest to that account before closing its files. | medium | app/cbl/CBACT04C.cbl:188-222, app/cbl/CBACT04C.cbl:325-348 |
| DTPR-BR-054 | Post accumulated interest to account | error handling | WHEN the rewrite of the account record fails, THE interest batch SHALL display 'ERROR RE-WRITING ACCOUNT FILE' with the file status and abend with code 999. | high | app/cbl/CBACT04C.cbl:350-370, app/cbl/CBACT04C.cbl:628-632 |
| DTPR-BR-055 | Account and card cross-reference must exist for every category balance | error handling | WHEN the account of a category balance is not on the account master file, THE interest batch SHALL display 'ACCOUNT NOT FOUND: ' with the account number and 'ERROR READING ACCOUNT FILE' with the file status, and abend with code 999, leaving accounts already rewritten in this run as they are. | high | app/cbl/CBACT04C.cbl:194-206, app/cbl/CBACT04C.cbl:372-413, app/cbl/CBACT04C.cbl:628-632 |
| DTPR-BR-056 | Account and card cross-reference must exist for every category balance | error handling | WHEN no card cross-reference exists for the account of a category balance, THE interest batch SHALL display 'ACCOUNT NOT FOUND: ' with the account number and 'ERROR READING XREF FILE' with the file status, and abend with code 999. | high | app/cbl/CBACT04C.cbl:194-206, app/cbl/CBACT04C.cbl:372-413, app/cbl/CBACT04C.cbl:628-632 |

### Worked examples

- DTPR-BR-044: category balance records = 3 → All 3 records are processed, then the end of file is detected
- DTPR-BR-045: previous account = 00000000001; next balance's account = 00000000002; interest accumulated for 00000000001 = 12.50 → 12.50 is posted to account 00000000001, the total restarts at 0 and account 00000000002 is read
- DTPR-BR-045: first balance of the run, account = 00000000001 → Nothing is posted; account 00000000001 and its cross-reference are read
- DTPR-BR-046: account group = GOLD; transaction type = 01; transaction category = 0001 → The rate is read from the disclosure group record keyed GOLD / 01 / 0001
- DTPR-BR-047: DISCGRP read status = '35' → 'ERROR READING DISCLOSURE GROUP FILE' displayed and the job abends.
- DTPR-BR-048: Category balance = 1200.00; Interest rate = 18.00 → Monthly interest = 1200.00 x 18.00 / 1200 = 18.00, added to the account's total interest and an interest transaction written.
- DTPR-BR-048: Category balance = 500.00; Interest rate = 0 → No interest computed and no transaction written.
- DTPR-BR-049: TRANSACT write status = not '00' → 'ERROR WRITING TRANSACTION RECORD' displayed and the job abends.
- DTPR-BR-050: category balance = 500.00; disclosure group rate = 0.00 → No interest transaction is written and the account's interest total is unchanged
- DTPR-BR-050: category balance = 500.00; disclosure group rate = 18.00 → Interest is calculated for the balance and an interest transaction is written
- DTPR-BR-051: category balance = 500.00; disclosure group rate = 18.00 → Interest is calculated; no fee transaction is written and no fee is added to the account
- DTPR-BR-052: current balance = 1,000.00; total interest = 15.00; current-cycle credit = 300.00; current-cycle debit = 1,200.00 → Current balance 1,015.00, current-cycle credit 0.00, current-cycle debit 0.00, record rewritten
- DTPR-BR-052: current balance = 200.00; total interest = 0.00 (all rates zero); current-cycle debit = 50.00 → Current balance stays 200.00 and current-cycle debit is set to 0.00
- DTPR-BR-053: last account in the file = 00000000050; accumulated interest = 8.25 → 8.25 is added to account 00000000050's current balance and the account is rewritten
- DTPR-BR-054: account rewrite file status = 23 → 'ERROR RE-WRITING ACCOUNT FILE' is displayed with the status and the run abends with code 999

## Decision tables

#### Interest rate lookup and interest outcome

| Rate lookup result | Rate found | Interest action | Rule |
|---|---|---|---|
| Group-specific rate found | Non-zero | Compute balance × rate / 1200, add to account total, write interest transaction | DTPR-BR-048 |
| No group-specific rate | - | Use the 'DEFAULT' group rate | DTPR-BR-047 |
| Other lookup failure | - | Abend | DTPR-BR-047 |
| Rate found | 0 | No interest, no interest transaction, nothing added to account total | DTPR-BR-050 |
| No group-specific rate and no 'DEFAULT' group rate | - | **Gap:** Rules do not say explicitly whether a missing 'DEFAULT' group rate counts as 'any other lookup failure' and abends. | |


## Design notes

- DTPR-BR-044: Read all category balances in key order (account ID, then type, then category) as one sorted stream, so each account's balances come together. The per-account interest total and the account rewrite depend on that grouping.

## Open questions

- SME-012: Interest transaction IDs are made from the run date plus a sequence number. What type and length must the ID and the sequence part have, and what should happen if the sequence runs out of digits? (Data architecture team) On DTPR-BR-047, DTPR-BR-049, DTPR-BR-048, DTPR-BR-053, DTPR-BR-050, DTPR-BR-045, DTPR-BR-054.
- SME-013: If the interest run fails, the interest transactions are discarded but accounts already updated with interest are not rolled back. Should account updates and interest transactions be saved together as one unit, and how should a restart avoid charging interest twice? (Batch operations) On DTPR-BR-047, DTPR-BR-049, DTPR-BR-048, DTPR-BR-053, DTPR-BR-050, DTPR-BR-045, DTPR-BR-054.
- SME-015: Is the interest run the official cycle-close event that resets each account's cycle credit and debit totals, and should accounts with no category balances also have their cycle totals reset? (Card product / finance owner) On DTPR-BR-052.
- DEF-032: Is this intended? An abend part-way through leaves earlier accounts' balances already rewritten with interest, but the job's TRANSACT output is catalogued with abnormal disposition DELETE, so the interest transactions for those accounts are discarded; a rerun would post interest to them again. (Subject-matter expert) On DTPR-BR-045, DTPR-BR-056.
- DEF-103: Is this intended? The final posting at end of file runs even when the category balance file is empty, so no account has been read and the program tries to rewrite an empty account record, which fails and abends the run with 'ERROR RE-WRITING ACCOUNT FILE'. (Subject-matter expert) On DTPR-BR-053.
- DEF-180: Confirm this is deliberate: Fees are never assessed although the job describes itself as computing interest and fees; the fee step is an empty stub. (Subject-matter expert) On DTPR-BR-051.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (17 in all).
