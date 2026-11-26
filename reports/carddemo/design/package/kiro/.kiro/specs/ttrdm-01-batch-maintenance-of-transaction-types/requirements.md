# Requirements: Batch maintenance of transaction types (TTRDM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

A scheduled batch job lets reference data administrators add, update and delete transaction types from an input file, one action per record ('A', 'U', 'D', or '*' for a comment). It must never let one bad record stop the run or go unnoticed: each rejected record leaves the table unchanged, is reported with its message, and makes the job end with return code 4 instead of 0. It must never delete a transaction type that still has categories referring to it.

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
2. GIVEN the transaction type table has no type with code '99' WHEN the batch reads the input record 'A99' followed by the description 'TEST PURCHASE' padded to 50 characters, and the database accepts the add THEN a transaction type with code '99' and description 'TEST PURCHASE' exists and the job shows 'RECORD INSERTED SUCCESSFULLY' (TTRDM-C01-AC-11; TTRDM-BR-004)

### Requirement 5: TTRDM-REQ-F-005 (error handling)

#### Acceptance criteria

1. If the database rejects an add (for example because the type code already exists, DB2 code -803), then the system shall show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue with the next record. (rules TTRDM-BR-005)
2. GIVEN the transaction type table already holds type code '01', and the input file holds 'A01' with a description followed by a valid 'U' record WHEN the batch processes the file and the database rejects the add with code -803 THEN the job shows 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with -803, type '01' keeps its existing description, the following 'U' record is still processed, and the job ends with return code 4 (TTRDM-C01-AC-12; TTRDM-BR-005)

### Requirement 6: TTRDM-REQ-F-006 (business rule)

#### Acceptance criteria

1. When an input record has action 'U' and the transaction type code exists, the system shall replace that type's description with the record's description and show 'RECORD UPDATED SUCCESSFULLY'. (rules TTRDM-BR-006)
2. GIVEN type code '01' exists with description 'Purchase' WHEN the batch reads the record 'U01' with the description 'Retail Purchase' THEN type '01' has the description 'Retail Purchase' and the job shows 'RECORD UPDATED SUCCESSFULLY' (TTRDM-C01-AC-13; TTRDM-BR-006)

### Requirement 7: TTRDM-REQ-F-007 (error handling)

#### Acceptance criteria

1. If an update or a delete names a transaction type code that does not exist, then the system shall show 'No records found.', set the job return code to 4 and continue with the next record. (rules TTRDM-BR-007, TTRDM-BR-008)
2. GIVEN input record: U99New desc; type '99' exists: no WHEN an update names a transaction type code that does not exist THEN 'No records found.' is shown, return code 4, processing continues (TTRDM-C01-AC-06; TTRDM-BR-007)
3. GIVEN input record: D99; type '99' exists: no WHEN a delete names a transaction type code that does not exist THEN 'No records found.' is shown, return code 4 (TTRDM-C01-AC-07; TTRDM-BR-008)

### Requirement 8: TTRDM-REQ-F-008 (error handling)

#### Acceptance criteria

1. If the database returns an error on an update, then the system shall show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue with the next record. (rules TTRDM-BR-009)
2. GIVEN type code '01' exists and the input file holds 'U01' with a new description followed by another record WHEN the database returns an error on the update THEN the job shows 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, the next record is still processed, and the job ends with return code 4 (TTRDM-C01-AC-14; TTRDM-BR-009)

### Requirement 9: TTRDM-REQ-F-009 (business rule)

#### Acceptance criteria

1. When an input record has action 'D' and the transaction type exists with no categories referring to it, the system shall delete the type and show 'RECORD DELETED SUCCESSFULLY'. (rules TTRDM-BR-010)
2. GIVEN input record: D08; type '08' exists: yes; categories for '08': none WHEN an input record has action 'D' and the transaction type exists with no categories referring to it THEN type '08' is removed; 'RECORD DELETED SUCCESSFULLY' (TTRDM-C01-AC-08; TTRDM-BR-010)

### Requirement 10: TTRDM-REQ-F-010 (error handling)

#### Acceptance criteria

1. If a delete names a transaction type that still has transaction type categories, then the system shall refuse the delete, show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, set the job return code to 4 and continue. (rules TTRDM-BR-011)
2. GIVEN type code '01' exists and at least one transaction type category refers to it WHEN the batch reads the record 'D01' THEN type '01' is still in the table, the job shows 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with the database code, processing continues with the next record, and the job ends with return code 4 (TTRDM-C01-AC-15; TTRDM-BR-011)

### Requirement 11: TTRDM-REQ-F-011 (error handling)

#### Acceptance criteria

1. When any input record is rejected (invalid action code, type not found, or database error), the system shall keep processing the remaining records and end the job with return code 4, and otherwise shall end the job with return code 0. (rules TTRDM-BR-012)
2. GIVEN record 1: A08Interest adjustment; record 2: X01Purchase; record 3: U01Retail purchase WHEN any input record is rejected (invalid action code, type not found, or database error) THEN records 1 and 3 are applied, 'ERROR: TYPE NOT VALID' is shown for record 2, the job ends with return code 4 (TTRDM-C01-AC-09; TTRDM-BR-012)
3. GIVEN record 1: U01Retail purchase; type '01' exists: yes WHEN any input record is rejected (invalid action code, type not found, or database error) THEN record applied, job ends with return code 0 (TTRDM-C01-AC-10; TTRDM-BR-012)

### Requirement 12: TTRDM-REQ-N-001 (formatting)

#### Acceptance criteria

1. The system shall show 'PROCESSING' followed by the input record for each record it reads, and 'OPEN FILE OK' or 'OPEN FILE NOT OK' when it opens the input file. (rules TTRDM-BR-013)
2. GIVEN an input file holding the two records 'A99…' and '*comment' WHEN the batch opens the file and processes it THEN the job shows 'OPEN FILE OK', then 'PROCESSING' followed by the first record and 'PROCESSING' followed by the second record; if the file cannot be opened the job shows 'OPEN FILE NOT OK' instead (TTRDM-C01-AC-16; TTRDM-BR-013)
