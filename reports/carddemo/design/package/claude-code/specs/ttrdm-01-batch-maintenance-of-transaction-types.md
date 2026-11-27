# Batch maintenance of transaction types (TTRDM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

A scheduled batch job lets reference data administrators add, update and delete transaction types from an input file. Each line holds a one-character action (A, U, D, or * for a comment), a two-character type code and a 50-character description. The job must never stop because one line is rejected: it reports each rejected line, keeps going, and ends with return code 4 if any line failed and 0 if none did.

**User story:** As a reference data administrator, I want to add, update and delete transaction types from a batch input file, so that the transaction type table used to classify credit card transactions stays current.

## Requirements

### Requirement 1: TTRDM-REQ-F-001 (business rule)

#### Acceptance criteria

1. The system shall read each batch input record as a one-character action code (column 1), a two-character transaction type code (columns 2-3) and a 50-character description (columns 4-53), and shall apply 'A' as add, 'U' as update and 'D' as delete. (rules TTRDM-BR-001)
2. GIVEN input record: A08Interest adjustment WHEN transaction type maintenance batch runs THEN 'ADDING RECORD' is shown and type '08' is added (TTRDM-C01-AC-01; TTRDM-BR-001)
3. GIVEN input record: D08 WHEN transaction type maintenance batch runs THEN 'DELETING RECORD' is shown and the delete of type '08' is attempted (TTRDM-C01-AC-02; TTRDM-BR-001)

### Requirement 2: TTRDM-REQ-F-002 (business rule)

#### Acceptance criteria

1. When an input record's action code is '*', the system shall treat the line as a comment, show 'IGNORING COMMENTED LINE' and change nothing. (rules TTRDM-BR-002)
2. GIVEN input record: *01Purchase WHEN an input record's action code is '*' THEN 'IGNORING COMMENTED LINE' is shown; the table is unchanged and the return code is not affected (TTRDM-C01-AC-03; TTRDM-BR-002)

### Requirement 3: TTRDM-REQ-F-003 (business rule)

#### Acceptance criteria

1. If an input record's action code is anything other than 'A', 'U', 'D' or '*', then the system shall show 'ERROR: TYPE NOT VALID', set the job return code to 4, leave the table unchanged and continue with the next record. (rules TTRDM-BR-003)
2. GIVEN input record: X01Purchase WHEN an input record's action code is anything other than 'A', 'U', 'D' or '*' THEN 'ERROR: TYPE NOT VALID' is shown, return code 4, nothing changed, the next record is still processed (TTRDM-C01-AC-04; TTRDM-BR-003)
3. GIVEN input record: a01Purchase WHEN an input record's action code is anything other than 'A', 'U', 'D' or '*' THEN lower-case 'a' is not accepted: 'ERROR: TYPE NOT VALID', return code 4 (TTRDM-C01-AC-05; TTRDM-BR-003)

### Requirement 4: TTRDM-REQ-F-004 (business rule)

#### Acceptance criteria

1. When an input record has action 'A', the system shall add a transaction type with the record's two-character code and its description, and show 'RECORD INSERTED SUCCESSFULLY' when the database accepts it. (rules TTRDM-BR-004)
2. GIVEN Transaction type code '99' does not exist in the transaction type table WHEN The batch processes the input record 'A99NEW TEST TYPE' (action 'A', code '99', description 'NEW TEST TYPE') THEN A transaction type with code '99' and description 'NEW TEST TYPE' exists in the table and the job shows 'RECORD INSERTED SUCCESSFULLY' (TTRDM-C01-AC-11; TTRDM-BR-004)

### Requirement 5: TTRDM-REQ-F-005 (error handling)

#### Acceptance criteria

1. If the database rejects an add (for example because the type code already exists, DB2 code -803), then the system shall show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue with the next record. (rules TTRDM-BR-005)
2. GIVEN Transaction type code '01' already exists in the transaction type table and another valid record follows in the input file WHEN The batch processes an input record with action 'A' and code '01' THEN The database rejects the add (duplicate key, DB2 code -803), the job shows 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' followed by the database code, the existing type '01' is unchanged, the following record is still processed and the job ends with return code 4 (TTRDM-C01-AC-12; TTRDM-BR-005)

### Requirement 6: TTRDM-REQ-F-006 (business rule)

#### Acceptance criteria

1. When an input record has action 'U' and the transaction type code exists, the system shall replace that type's description with the record's description and show 'RECORD UPDATED SUCCESSFULLY'. (rules TTRDM-BR-006)
2. GIVEN Transaction type code '01' exists with description 'Purchase' WHEN The batch processes an input record with action 'U', code '01' and description 'Retail Purchase' THEN The description of type '01' is 'Retail Purchase' and the job shows 'RECORD UPDATED SUCCESSFULLY' (TTRDM-C01-AC-13; TTRDM-BR-006)

### Requirement 7: TTRDM-REQ-F-007 (error handling)

#### Acceptance criteria

1. If an update or a delete names a transaction type code that does not exist, then the system shall show 'No records found.', set the job return code to 4 and continue with the next record. (rules TTRDM-BR-007, TTRDM-BR-008)
2. GIVEN input record: U99New desc; type '99' exists: no WHEN an update names a transaction type code that does not exist THEN 'No records found.' is shown, return code 4, processing continues (TTRDM-C01-AC-06; TTRDM-BR-007)
3. GIVEN input record: D99; type '99' exists: no WHEN a delete names a transaction type code that does not exist THEN 'No records found.' is shown, return code 4 (TTRDM-C01-AC-07; TTRDM-BR-008)

### Requirement 8: TTRDM-REQ-F-008 (error handling)

#### Acceptance criteria

1. If the database returns an error on an update, then the system shall show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue with the next record. (rules TTRDM-BR-009)
2. GIVEN Transaction type code '01' exists, the database returns an error when it is updated, and another record follows in the input file WHEN The batch processes an input record with action 'U' and code '01' THEN The job shows 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' followed by the database code, processes the following record and ends with return code 4 (TTRDM-C01-AC-14; TTRDM-BR-009)

### Requirement 9: TTRDM-REQ-F-009 (business rule)

#### Acceptance criteria

1. When an input record has action 'D' and the transaction type exists with no categories referring to it, the system shall delete the type and show 'RECORD DELETED SUCCESSFULLY'. (rules TTRDM-BR-010)
2. GIVEN input record: D08; type '08' exists: yes; categories for '08': none WHEN an input record has action 'D' and the transaction type exists with no categories referring to it THEN type '08' is removed; 'RECORD DELETED SUCCESSFULLY' (TTRDM-C01-AC-08; TTRDM-BR-010)

### Requirement 10: TTRDM-REQ-F-010 (error handling)

#### Acceptance criteria

1. If a delete names a transaction type that still has transaction type categories, then the system shall refuse the delete, show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue. (rules TTRDM-BR-011)
2. GIVEN Transaction type code '01' exists and at least one transaction type category refers to it WHEN The batch processes an input record with action 'D' and code '01' THEN The database refuses the delete, type '01' still exists, the job shows 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' followed by the database code, continues with the next record and ends with return code 4 (TTRDM-C01-AC-15; TTRDM-BR-011)

### Requirement 11: TTRDM-REQ-F-011 (error handling)

#### Acceptance criteria

1. When any input record is rejected (invalid action code, type not found, or database error), the system shall keep processing the remaining records and end the job with return code 4, and otherwise shall end the job with return code 0. (rules TTRDM-BR-012)
2. GIVEN record 1: A08Interest adjustment; record 2: X01Purchase; record 3: U01Retail purchase WHEN any input record is rejected (invalid action code, type not found, or database error) THEN records 1 and 3 are applied, 'ERROR: TYPE NOT VALID' is shown for record 2, the job ends with return code 4 (TTRDM-C01-AC-09; TTRDM-BR-012)
3. GIVEN record 1: U01Retail purchase; type '01' exists: yes WHEN any input record is rejected (invalid action code, type not found, or database error) THEN record applied, job ends with return code 0 (TTRDM-C01-AC-10; TTRDM-BR-012)

### Requirement 12: TTRDM-REQ-N-001 (formatting)

#### Acceptance criteria

1. The system shall show 'PROCESSING' followed by the input record for each record it reads, and 'OPEN FILE OK' or 'OPEN FILE NOT OK' when it opens the input file. (rules TTRDM-BR-013)
2. GIVEN An input file that can be opened and holds the two records 'A99NEW TEST TYPE' and '*COMMENT' WHEN The batch job runs THEN The job shows 'OPEN FILE OK', then 'PROCESSING' followed by 'A99NEW TEST TYPE', then 'PROCESSING' followed by '*COMMENT'; and when the input file cannot be opened the job shows 'OPEN FILE NOT OK' (TTRDM-C01-AC-16; TTRDM-BR-013)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-001 | Batch maintenance action code dispatch (Add / Update / Delete / Comment) | business rule | THE transaction type maintenance batch SHALL read each input record as a one-character action code (column 1), a two-character transaction type code (columns 2-3) and a 50-character description (columns 4-53), and SHALL apply 'A' as add, 'U' as update and 'D' as delete. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:71-77, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:109-130, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233, app/app-transaction-type-db2/jcl/MNTTRDB2.jcl:8-18 |
| TTRDM-BR-002 | Batch maintenance action code dispatch (Add / Update / Delete / Comment) | business rule | WHEN an input record's action code is '*', THE transaction type maintenance batch SHALL treat the line as a comment, show 'IGNORING COMMENTED LINE' and change nothing. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:71-77, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:109-130, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233, app/app-transaction-type-db2/jcl/MNTTRDB2.jcl:8-18 |
| TTRDM-BR-003 | Reject unrecognized request types | business rule | WHEN an input record's action code is anything other than 'A', 'U', 'D' or '*', THE transaction type maintenance batch SHALL show 'ERROR: TYPE NOT VALID', set the job return code to 4, leave the table unchanged and continue with the next record. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:71-77, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:109-130, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233, app/app-transaction-type-db2/jcl/MNTTRDB2.jcl:8-18 |
| TTRDM-BR-004 | Add a new transaction type | business rule | WHEN an input record has action 'A', THE transaction type maintenance batch SHALL add a transaction type with the record's two-character code and its description, and show 'RECORD INSERTED SUCCESSFULLY' when the database accepts it. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:132-164, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233, app/app-transaction-type-db2/ddl/TRNTYPE.ddl:1-4 |
| TTRDM-BR-005 | Add a new transaction type | error handling | WHEN the database rejects the add (for example because the type code already exists, DB2 code -803), THE transaction type maintenance batch SHALL show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue with the next record. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:132-164, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233, app/app-transaction-type-db2/ddl/TRNTYPE.ddl:1-4 |
| TTRDM-BR-006 | Update a transaction type description | business rule | WHEN an input record has action 'U' and the transaction type code exists, THE transaction type maintenance batch SHALL replace that type's description with the record's description and show 'RECORD UPDATED SUCCESSFULLY'. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:166-195, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233 |
| TTRDM-BR-007 | Update a transaction type description | error handling | WHEN an update names a transaction type code that does not exist, THE transaction type maintenance batch SHALL show 'No records found.', set the job return code to 4 and continue with the next record. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:166-195, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233 |
| TTRDM-BR-008 | Delete a transaction type | error handling | WHEN a delete names a transaction type code that does not exist, THE transaction type maintenance batch SHALL show 'No records found.', set the job return code to 4 and continue with the next record. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:196-226, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233, app/app-transaction-type-db2/ddl/TRNTYCAT.ddl:1-7 |
| TTRDM-BR-009 | Update a transaction type description | error handling | WHEN the database returns an error on an update, THE transaction type maintenance batch SHALL show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue with the next record. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:166-195, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233 |
| TTRDM-BR-010 | Delete a transaction type | business rule | WHEN an input record has action 'D' and the transaction type exists with no categories referring to it, THE transaction type maintenance batch SHALL delete the type and show 'RECORD DELETED SUCCESSFULLY'. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:196-226, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233, app/app-transaction-type-db2/ddl/TRNTYCAT.ddl:1-7 |
| TTRDM-BR-011 | Delete a transaction type | error handling | WHEN a delete names a transaction type that still has transaction type categories, THE database SHALL refuse the delete and THE transaction type maintenance batch SHALL show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue. | high | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:196-226, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-233, app/app-transaction-type-db2/ddl/TRNTYCAT.ddl:1-7 |
| TTRDM-BR-012 | Batch run outcome signalled by return code 4 on any rejected record | error handling | WHEN any input record is rejected (invalid action code, type not found, or database error), THE transaction type maintenance batch SHALL keep processing the remaining records and end the job with return code 4; otherwise the job ends with return code 0. | medium | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:82-107, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-236 |
| TTRDM-BR-013 | Batch run outcome signalled by return code 4 on any rejected record | formatting | THE transaction type maintenance batch SHALL show 'PROCESSING' followed by the input record for each record it reads, and 'OPEN FILE OK' or 'OPEN FILE NOT OK' when it opens the input file. | medium | app/app-transaction-type-db2/cbl/COBTUPDT.cbl:82-107, app/app-transaction-type-db2/cbl/COBTUPDT.cbl:230-236 |

### Worked examples

- TTRDM-BR-001: input record = A08Interest adjustment → 'ADDING RECORD' is shown and type '08' is added
- TTRDM-BR-001: input record = D08 → 'DELETING RECORD' is shown and the delete of type '08' is attempted
- TTRDM-BR-002: input record = *01Purchase → 'IGNORING COMMENTED LINE' is shown; the table is unchanged and the return code is not affected
- TTRDM-BR-003: input record = X01Purchase → 'ERROR: TYPE NOT VALID' is shown, return code 4, nothing changed, the next record is still processed
- TTRDM-BR-003: input record = a01Purchase → lower-case 'a' is not accepted: 'ERROR: TYPE NOT VALID', return code 4
- TTRDM-BR-007: input record = U99New desc; type '99' exists = no → 'No records found.' is shown, return code 4, processing continues
- TTRDM-BR-008: input record = D99; type '99' exists = no → 'No records found.' is shown, return code 4
- TTRDM-BR-010: input record = D08; type '08' exists = yes; categories for '08' = none → type '08' is removed; 'RECORD DELETED SUCCESSFULLY'
- TTRDM-BR-012: record 1 = A08Interest adjustment; record 2 = X01Purchase; record 3 = U01Retail purchase → records 1 and 3 are applied, 'ERROR: TYPE NOT VALID' is shown for record 2, the job ends with return code 4
- TTRDM-BR-012: record 1 = U01Retail purchase; type '01' exists = yes → record applied, job ends with return code 0

## Decision tables

#### Batch record outcome by action code

| Action code | Transaction type code exists | Categories refer to the type | Database accepts the change | Batch result for the record | Rule |
|---|---|---|---|---|---|
| '*' | - | - | - | Show 'IGNORING COMMENTED LINE'; change nothing | TTRDM-BR-002 |
| Other than 'A', 'U', 'D', '*' | - | - | - | Show 'ERROR: TYPE NOT VALID'; return code 4; table unchanged; continue | TTRDM-BR-003 |
| 'A' | - | - | Yes | Add type; show 'RECORD INSERTED SUCCESSFULLY' | TTRDM-BR-004 |
| 'A' | - | - | No (e.g. code already exists, -803) | Show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with code; return code 4; continue | TTRDM-BR-005 |
| 'U' | Yes | - | Yes | Replace description; show 'RECORD UPDATED SUCCESSFULLY' | TTRDM-BR-006 |
| 'U' | No | - | - | Show 'No records found.'; return code 4; continue | TTRDM-BR-007 |
| 'U' | - | - | No (database error) | Show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with code; return code 4; continue | TTRDM-BR-009 |
| 'D' | Yes | No | Yes | Delete type; show 'RECORD DELETED SUCCESSFULLY' | TTRDM-BR-010 |
| 'D' | Yes | Yes | No (refused) | Show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with code; return code 4; continue | TTRDM-BR-011 |
| 'D' | No | - | - | Show 'No records found.'; return code 4; continue | TTRDM-BR-008 |
| 'D' | Yes | No | No (other database error) | **Gap:** R1 says any database error gives return code 4, but no rule states the message shown when a delete fails for a reason other than referring categories. | |


## Design notes

None.

## Open questions

- SME-090: In the transaction type maintenance batch, should comment records (type '*') be skipped without changing the transaction type table? (Business analyst) On TTRDM-BR-003, TTRDM-BR-005, TTRDM-BR-009, TTRDM-BR-011.
- SME-091: In the transaction type maintenance batch, what should be logged or confirmed when a new transaction type is added successfully? (Business analyst) On TTRDM-BR-003, TTRDM-BR-005, TTRDM-BR-009, TTRDM-BR-011.
- SME-092: The transaction type maintenance job is tied to database subsystem DAZ1 and application plan CARDDEMO. Should the new system keep these bindings, or treat them as deployment settings? (Platform team) On TTRDM-BR-003, TTRDM-BR-005, TTRDM-BR-009, TTRDM-BR-011.
- SME-093: When a request in the transaction type maintenance batch is rejected or the job ends abnormally, should the batch carry on and flag the problem (return code 4, earlier changes kept), or stop and roll back the whole batch? Which return code should each outcome give? (Batch operations lead) On TTRDM-BR-013, TTRDM-BR-003, TTRDM-BR-005, TTRDM-BR-009, TTRDM-BR-011.
- SME-094: Please confirm the priority of the batch rule for adding a new transaction type. Is it critical to the system's core purpose, or a rule that would be costly if it were wrong? (Business SME (transaction type reference data)) On TTRDM-BR-005.
- SME-095: Should a transaction type also be protected from deletion while posted transactions still use it? Or is 'no transaction categories refer to it' the only check intended? (Business SME (transaction type reference data)) On TTRDM-BR-011.
- DEF-168: Is this intended? If the input file fails to open, the program only shows 'OPEN FILE NOT OK' and carries on into the read loop; reads on an unopened file never reach end of file, so the job can loop instead of stopping with an error. (Subject-matter expert) On TTRDM-BR-013.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (16 in all).
