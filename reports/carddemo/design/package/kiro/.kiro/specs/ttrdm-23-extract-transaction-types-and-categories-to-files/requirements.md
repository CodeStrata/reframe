# Requirements: Extract transaction types and categories to files (TTRDM-C23)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

A scheduled job for operations that backs up the current transaction type and category extract files and then writes fresh extracts from the database, for downstream processing such as the transaction report. The extracts must hold exactly the database contents in code order and in a fixed 60-character layout. A failed extract must never leave a partial file behind.

**User story:** As an operations user, I want to back up the current transaction type and category files and unload fresh copies from the database, so that downstream processing such as the transaction report has current reference data.

## Requirements

### Requirement 1: TTRDM-REQ-F-151 (design note)

#### Acceptance criteria

1. The system shall first copy the current transaction type file (AWS.M2.CARDDEMO.TRANTYPE.PS) into a new cataloged generation of the transaction type backup (AWS.M2.CARDDEMO.TRANTYPE.BKUP) of fixed 60-byte records. (rules TTRDM-BR-163)
2. GIVEN Transaction type file: AWS.M2.CARDDEMO.TRANTYPE.PS from the previous run WHEN transaction type extract job (TRANEXTR) runs THEN A new generation of AWS.M2.CARDDEMO.TRANTYPE.BKUP holds a copy of it. (TTRDM-C23-AC-01; TTRDM-BR-163)

### Requirement 2: TTRDM-REQ-F-152 (design note)

#### Acceptance criteria

1. When every earlier step of the transaction type extract job (TRANEXTR) ended with return code 0, the system shall copy the current transaction category file (AWS.M2.CARDDEMO.TRANCATG.PS) into a new cataloged generation of the category backup (AWS.M2.CARDDEMO.TRANCATG.PS.BKUP) of fixed 60-byte records. (rules TTRDM-BR-164)
2. GIVEN Return code of the transaction type backup step: 0 WHEN every earlier step of the transaction type extract job (TRANEXTR) ended with return code 0 THEN The current category file is copied into a new backup generation. (TTRDM-C23-AC-02; TTRDM-BR-164)

### Requirement 3: TTRDM-REQ-F-153 (error handling)

#### Acceptance criteria

1. If any earlier step of the transaction type extract job ended with a return code other than 0, then the system shall skip the transaction category backup. (rules TTRDM-BR-165)
2. GIVEN Return code of the transaction type backup step: 12 WHEN any earlier step of the transaction type extract job ended with a return code other than 0 THEN No new category backup generation is created. (TTRDM-C23-AC-03; TTRDM-BR-165)

### Requirement 4: TTRDM-REQ-F-154 (side effect)

#### Acceptance criteria

1. When every earlier step of the transaction type extract job ended with return code 0, the system shall unload all transaction types from the Db2 table CARDDEMO.TRANSACTION_TYPE, in type code order, to a new transaction type file (AWS.M2.CARDDEMO.TRANTYPE.PS) for the transaction report. (rules TTRDM-BR-166)
2. GIVEN Earlier step return codes: all 0; Transaction types in the table: '02', '01' WHEN every earlier step of the transaction type extract job ended with return code 0 THEN The new file holds type '01' then type '02'. (TTRDM-C23-AC-04; TTRDM-BR-166)
3. GIVEN Earlier step return codes: one step ended 8 WHEN every earlier step of the transaction type extract job ended with return code 0 THEN The unload is skipped and no new transaction type file is written. (TTRDM-C23-AC-05; TTRDM-BR-166)

### Requirement 5: TTRDM-REQ-F-155 (design note)

#### Acceptance criteria

1. The system shall write each extracted transaction type as one 60-character record: the type code, the description padded to 50 characters, then eight '0' characters. (rules TTRDM-BR-167)
2. GIVEN The transaction type table holds type code '01' with description 'Purchase' WHEN The transaction type extract runs THEN The extract contains one 60-character record for it: '01', then 'Purchase' padded with spaces to 50 characters, then '00000000' (TTRDM-C23-AC-10; TTRDM-BR-167)

### Requirement 6: TTRDM-REQ-F-156 (error handling)

#### Acceptance criteria

1. If the transaction type unload fails, then the system shall delete the new transaction type file instead of keeping it. (rules TTRDM-BR-168)
2. GIVEN Unload step: abends WHEN the transaction type unload fails THEN AWS.M2.CARDDEMO.TRANTYPE.PS is deleted, not cataloged. (TTRDM-C23-AC-06; TTRDM-BR-168)

### Requirement 7: TTRDM-REQ-F-157 (side effect)

#### Acceptance criteria

1. When no earlier step of the transaction type extract job ended with a return code above 4, the system shall unload all transaction categories from the Db2 table CARDDEMO.TRANSACTION_TYPE_CATEGORY, in type code then category order, to a new transaction category file (AWS.M2.CARDDEMO.TRANCATG.PS). (rules TTRDM-BR-169)
2. GIVEN Highest earlier step return code: 4 WHEN no earlier step of the transaction type extract job ended with a return code above 4 THEN The category unload still runs. (TTRDM-C23-AC-07; TTRDM-BR-169)
3. GIVEN Highest earlier step return code: 8 WHEN no earlier step of the transaction type extract job ended with a return code above 4 THEN The category unload is skipped. (TTRDM-C23-AC-08; TTRDM-BR-169)

### Requirement 8: TTRDM-REQ-F-158 (design note)

#### Acceptance criteria

1. The system shall write each extracted category as one 60-character record: the type code, the category code, the category description padded to 50 characters, then four '0' characters. (rules TTRDM-BR-170)
2. GIVEN The transaction category table holds type code '01', category code '0001', description 'Regular Sales Draft' WHEN The transaction category extract runs THEN The extract contains one 60-character record for it: '01', then '0001', then 'Regular Sales Draft' padded with spaces to 50 characters, then '0000' (TTRDM-C23-AC-11; TTRDM-BR-170)

### Requirement 9: TTRDM-REQ-F-159 (error handling)

#### Acceptance criteria

1. If the transaction category unload fails, then the system shall delete the new transaction category file instead of keeping it. (rules TTRDM-BR-171)
2. GIVEN Unload step: abends WHEN the transaction category unload fails THEN AWS.M2.CARDDEMO.TRANCATG.PS is deleted, not cataloged. (TTRDM-C23-AC-09; TTRDM-BR-171)
