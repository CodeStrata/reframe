# Design: Batch maintenance of transaction types (TTRDM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A scheduled batch job lets reference data administrators add, update and delete transaction types from an input file. Each line holds a one-character action (A, U, D, or * for a comment), a two-character type code and a 50-character description. The job must never stop because one line is rejected: it reports each rejected line, keeps going, and ends with return code 4 if any line failed and 0 if none did.

Runs as scheduled job.

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