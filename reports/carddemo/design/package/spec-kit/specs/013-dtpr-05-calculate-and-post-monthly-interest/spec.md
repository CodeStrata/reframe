# Feature specification: Calculate and post monthly interest

**Feature:** DTPR-C05 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C05)

As a card issuer, I want monthly interest calculated on each category balance at the account group's rate and posted to the account, so that customers are charged the correct interest.

Calculates monthly interest on each category balance (balance × rate ÷ 1200) at the rate for the account's disclosure group, falling back to the 'DEFAULT' group's rate when the group has none. It writes each interest charge as a system transaction, then adds the account's total interest to its balance and resets its cycle totals to zero. It serves the card issuer, who must charge customers the right interest. It must never use the wrong rate, charge interest at a rate of 0, or carry on when an account or card cross-reference is missing.

**Acceptance scenarios:**

1. **Given** category balance records: 3, **when** interest batch runs, **then** All 3 records are processed, then the end of file is detected (DTPR-C05-AC-01)
2. **Given** previous account: 00000000001; next balance's account: 00000000002; interest accumulated for 00000000001: 12.50, **when** a category balance belongs to a different account from the previous one, **then** 12.50 is posted to account 00000000001, the total restarts at 0 and account 00000000002 is read (DTPR-C05-AC-02)
3. **Given** first balance of the run, account: 00000000001, **when** a category balance belongs to a different account from the previous one, **then** Nothing is posted; account 00000000001 and its cross-reference are read (DTPR-C05-AC-03)
4. **Given** account group: GOLD; transaction type: 01; transaction category: 0001, **when** the interest batch processes a category balance, **then** The rate is read from the disclosure group record keyed GOLD / 01 / 0001 (DTPR-C05-AC-04)
5. **Given** DISCGRP read status: '35', **when** an interest rate is needed for a category balance, **then** 'ERROR READING DISCLOSURE GROUP FILE' displayed and the job abends. (DTPR-C05-AC-05)
6. **Given** Category balance: 1200.00; Interest rate: 18.00, **when** a category balance has a non-zero interest rate, **then** Monthly interest = 1200.00 x 18.00 / 1200 = 18.00, added to the account's total interest and an interest transaction written. (DTPR-C05-AC-06)
7. **Given** Category balance: 500.00; Interest rate: 0, **when** a category balance has a non-zero interest rate, **then** No interest computed and no transaction written. (DTPR-C05-AC-07)
8. **Given** TRANSACT write status: not '00', **when** monthly interest has been computed for a category balance, **then** 'ERROR WRITING TRANSACTION RECORD' displayed and the job abends. (DTPR-C05-AC-08)
9. **Given** category balance: 500.00; disclosure group rate: 0.00, **when** the rate found for a category balance is 0, **then** No interest transaction is written and the account's interest total is unchanged (DTPR-C05-AC-09)
10. **Given** category balance: 500.00; disclosure group rate: 18.00, **when** the rate found for a category balance is 0, **then** Interest is calculated for the balance and an interest transaction is written (DTPR-C05-AC-10)
11. **Given** category balance: 500.00; disclosure group rate: 18.00, **when** interest is calculated for a category balance, **then** Interest is calculated; no fee transaction is written and no fee is added to the account (DTPR-C05-AC-11)
12. **Given** current balance: 1,000.00; total interest: 15.00; current-cycle credit: 300.00; current-cycle debit: 1,200.00, **when** the interest batch finishes an account's category balances, **then** Current balance 1,015.00, current-cycle credit 0.00, current-cycle debit 0.00, record rewritten (DTPR-C05-AC-12)
13. **Given** current balance: 200.00; total interest: 0.00 (all rates zero); current-cycle debit: 50.00, **when** the interest batch finishes an account's category balances, **then** Current balance stays 200.00 and current-cycle debit is set to 0.00 (DTPR-C05-AC-13)
14. **Given** last account in the file: 00000000050; accumulated interest: 8.25, **when** the end of the category balance file is reached, **then** 8.25 is added to account 00000000050's current balance and the account is rewritten (DTPR-C05-AC-14)
15. **Given** account rewrite file status: 23, **when** the rewrite of the account record fails, **then** 'ERROR RE-WRITING ACCOUNT FILE' is displayed with the status and the run abends with code 999 (DTPR-C05-AC-15)
16. **Given** an interest run in which account 00000000001 has already been rewritten with its interest, and the next category balance belongs to account 00000000099, which is not on the account master, **when** the run reaches that category balance and looks up account 00000000099, **then** it displays 'ACCOUNT NOT FOUND: ' with 00000000099 and 'ERROR READING ACCOUNT FILE' with the file status, abends with code 999, and account 00000000001 keeps the interest already posted to it (DTPR-C05-AC-16)
17. **Given** a category balance for account 00000000099, which has no card cross-reference, **when** the run looks up the card cross-reference for account 00000000099, **then** it displays 'ACCOUNT NOT FOUND: ' with 00000000099 and 'ERROR READING XREF FILE' with the file status, and abends with code 999 (DTPR-C05-AC-17)

## Requirements

### Functional requirements

- **DTPR-REQ-F-038** (design note): The system shall read the category balance file in order, one record at a time, processing each record until the end of the file is reached. Rules: DTPR-BR-044.
- **DTPR-REQ-F-039** (business rule): When a category balance belongs to a different account from the previous one, the system shall post the previous account's accumulated interest (except for the first account of the run), reset the interest total to 0, and read the new account and its card cross-reference. Rules: DTPR-BR-045.
- **DTPR-REQ-F-040** (business rule): When the system processes a category balance, the system shall look up the interest rate in the disclosure group file using the account's group, the balance's transaction type and its transaction category. Rules: DTPR-BR-046.
- **DTPR-REQ-F-041** (business rule): When no group-specific rate exists for a category balance, the system shall use the 'DEFAULT' group rate. Rules: DTPR-BR-047.
- **DTPR-REQ-F-042** (business rule): If the interest rate lookup fails for any reason other than no group-specific rate existing, then the system shall abend. Rules: DTPR-BR-047.
- **DTPR-REQ-F-043** (business rule): When a category balance has a non-zero interest rate, the system shall compute monthly interest as balance times rate divided by 1200 and add it to the account's total interest. Rules: DTPR-BR-048.
- **DTPR-REQ-F-044** (business rule): When monthly interest has been computed for a category balance, the system shall write a transaction with id run-date plus sequence suffix, type '01', category '05', source 'System', description 'Int. for a/c ' plus account id, the interest amount, the card number and the current timestamp, abending if the write fails. Rules: DTPR-BR-049, DTPR-BR-048.
- **DTPR-REQ-F-045** (business rule): When the rate found for a category balance is 0, the system shall calculate no interest for that balance, write no interest transaction for it and add nothing to the account's interest total. Rules: DTPR-BR-050.
- **DTPR-REQ-F-046** (historical artifact): When interest is calculated for a category balance, the system shall calculate and post no fee, as the fee step is marked 'To be implemented'. Rules: DTPR-BR-051.
- **DTPR-REQ-F-047** (business rule): When the system finishes an account's category balances, the system shall add the account's total interest to its current balance, set its current-cycle credit and current-cycle debit to 0, and rewrite the account record. Rules: DTPR-BR-052.
- **DTPR-REQ-F-048** (business rule): When the end of the category balance file is reached, the system shall post the last account's accumulated interest to that account before closing its files. Rules: DTPR-BR-053.
- **DTPR-REQ-F-049** (error handling): If the rewrite of the account record fails, then the system shall display 'ERROR RE-WRITING ACCOUNT FILE' with the file status and abend with code 999. Rules: DTPR-BR-054.
- **DTPR-REQ-F-050** (error handling): If the account of a category balance is not on the account master file, then the system shall display 'ACCOUNT NOT FOUND: ' with the account number and 'ERROR READING ACCOUNT FILE' with the file status, and abend with code 999, leaving accounts already rewritten in this run as they are. Rules: DTPR-BR-055.
- **DTPR-REQ-F-051** (error handling): If no card cross-reference exists for the account of a category balance, then the system shall display 'ACCOUNT NOT FOUND: ' with the account number and 'ERROR READING XREF FILE' with the file status, and abend with code 999. Rules: DTPR-BR-056.

### Business rules

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

### Key entities

- CVACT01Y (file record)
- CVACT03Y (file record)
- CVTRA01Y (file record)
- CVTRA02Y (file record)
- CVTRA05Y (file record)

### Needs clarification

- SME-012: Interest transaction IDs are made from the run date plus a sequence number. What type and length must the ID and the sequence part have, and what should happen if the sequence runs out of digits? (Data architecture team) On DTPR-BR-047, DTPR-BR-049, DTPR-BR-048, DTPR-BR-053, DTPR-BR-050, DTPR-BR-045, DTPR-BR-054.
- SME-013: If the interest run fails, the interest transactions are discarded but accounts already updated with interest are not rolled back. Should account updates and interest transactions be saved together as one unit, and how should a restart avoid charging interest twice? (Batch operations) On DTPR-BR-047, DTPR-BR-049, DTPR-BR-048, DTPR-BR-053, DTPR-BR-050, DTPR-BR-045, DTPR-BR-054.
- SME-015: Is the interest run the official cycle-close event that resets each account's cycle credit and debit totals, and should accounts with no category balances also have their cycle totals reset? (Card product / finance owner) On DTPR-BR-052.
- DEF-032: Is this intended? An abend part-way through leaves earlier accounts' balances already rewritten with interest, but the job's TRANSACT output is catalogued with abnormal disposition DELETE, so the interest transactions for those accounts are discarded; a rerun would post interest to them again. (Subject-matter expert) On DTPR-BR-045, DTPR-BR-056.
- DEF-103: Is this intended? The final posting at end of file runs even when the category balance file is empty, so no account has been read and the program tries to rewrite an empty account record, which fails and abends the run with 'ERROR RE-WRITING ACCOUNT FILE'. (Subject-matter expert) On DTPR-BR-053.
- DEF-180: Confirm this is deliberate: Fees are never assessed although the job describes itself as computing interest and fees; the fee step is an empty stub. (Subject-matter expert) On DTPR-BR-051.

### Decision table gaps

- Interest rate lookup and interest outcome: Rules do not say explicitly whether a missing 'DEFAULT' group rate counts as 'any other lookup failure' and abends.
