# Extract transaction types and categories to files (TTRDM-C23)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

Backs up the current transaction type and category files, then produces fresh copies from the database for downstream use such as the transaction report. Types are written in type code order and categories in type then category order, as fixed 60-character records. A failed unload must never leave a partial file behind.

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
2. GIVEN The transaction type table holds type code '01' with description 'Purchase' WHEN The transaction type extract runs THEN The extract file holds a 60-character record made of '01', then 'Purchase' padded with spaces to 50 characters, then '00000000' (TTRDM-C23-AC-10; TTRDM-BR-167)

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
2. GIVEN The transaction type category table holds a category for type code '01' with category description 'Regular Sales Draft' WHEN The transaction category extract runs THEN The extract file holds one 60-character record for it, made of the type code '01', then the category code, then 'Regular Sales Draft' padded with spaces to 50 characters, then '0000' (TTRDM-C23-AC-11; TTRDM-BR-170)

### Requirement 9: TTRDM-REQ-F-159 (error handling)

#### Acceptance criteria

1. If the transaction category unload fails, then the system shall delete the new transaction category file instead of keeping it. (rules TTRDM-BR-171)
2. GIVEN Unload step: abends WHEN the transaction category unload fails THEN AWS.M2.CARDDEMO.TRANCATG.PS is deleted, not cataloged. (TTRDM-C23-AC-09; TTRDM-BR-171)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-163 | Back up previous transaction type file | design note | THE transaction type extract job (TRANEXTR) SHALL first copy the current transaction type file (AWS.M2.CARDDEMO.TRANTYPE.PS) into a new cataloged generation of the transaction type backup (AWS.M2.CARDDEMO.TRANTYPE.BKUP) of fixed 60-byte records. | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:29-38 |
| TTRDM-BR-164 | Back up previous transaction category file | design note | WHEN every earlier step of the transaction type extract job (TRANEXTR) ended with return code 0, THE job SHALL copy the current transaction category file (AWS.M2.CARDDEMO.TRANCATG.PS) into a new cataloged generation of the category backup (AWS.M2.CARDDEMO.TRANCATG.PS.BKUP) of fixed 60-byte records. | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:42-49 |
| TTRDM-BR-165 | Back up previous transaction category file | error handling | WHEN any earlier step of the transaction type extract job ended with a return code other than 0, THE job SHALL skip the transaction category backup. | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:42-49 |
| TTRDM-BR-166 | Unload transaction types to flat file | side effect | WHEN every earlier step of the transaction type extract job ended with return code 0, THE job SHALL unload all transaction types from the Db2 table CARDDEMO.TRANSACTION_TYPE, in type code order, to a new transaction type file (AWS.M2.CARDDEMO.TRANTYPE.PS) for the transaction report. | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:65-91, app/app-transaction-type-db2/jcl/TRANEXTR.jcl:19-21 |
| TTRDM-BR-167 | Unload transaction types to flat file | design note | THE transaction type extract SHALL write each type as one 60-character record: the type code, the description padded to 50 characters, then eight '0' characters. | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:65-91, app/app-transaction-type-db2/jcl/TRANEXTR.jcl:19-21 |
| TTRDM-BR-168 | Unload transaction types to flat file | error handling | WHEN the transaction type unload fails, THE job SHALL delete the new transaction type file instead of keeping it. | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:65-91, app/app-transaction-type-db2/jcl/TRANEXTR.jcl:19-21 |
| TTRDM-BR-169 | Unload transaction categories to flat file | side effect | WHEN no earlier step of the transaction type extract job ended with a return code above 4, THE job SHALL unload all transaction categories from the Db2 table CARDDEMO.TRANSACTION_TYPE_CATEGORY, in type code then category order, to a new transaction category file (AWS.M2.CARDDEMO.TRANCATG.PS). | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:95-122 |
| TTRDM-BR-170 | Unload transaction categories to flat file | design note | THE transaction category extract SHALL write each category as one 60-character record: the type code, the category code, the category description padded to 50 characters, then four '0' characters. | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:95-122 |
| TTRDM-BR-171 | Unload transaction categories to flat file | error handling | WHEN the transaction category unload fails, THE job SHALL delete the new transaction category file instead of keeping it. | medium | app/app-transaction-type-db2/jcl/TRANEXTR.jcl:95-122 |

### Worked examples

- TTRDM-BR-163: Transaction type file = AWS.M2.CARDDEMO.TRANTYPE.PS from the previous run → A new generation of AWS.M2.CARDDEMO.TRANTYPE.BKUP holds a copy of it.
- TTRDM-BR-164: Return code of the transaction type backup step = 0 → The current category file is copied into a new backup generation.
- TTRDM-BR-165: Return code of the transaction type backup step = 12 → No new category backup generation is created.
- TTRDM-BR-166: Earlier step return codes = all 0; Transaction types in the table = '02', '01' → The new file holds type '01' then type '02'.
- TTRDM-BR-166: Earlier step return codes = one step ended 8 → The unload is skipped and no new transaction type file is written.
- TTRDM-BR-168: Unload step = abends → AWS.M2.CARDDEMO.TRANTYPE.PS is deleted, not cataloged.
- TTRDM-BR-169: Highest earlier step return code = 4 → The category unload still runs.
- TTRDM-BR-169: Highest earlier step return code = 8 → The category unload is skipped.
- TTRDM-BR-171: Unload step = abends → AWS.M2.CARDDEMO.TRANCATG.PS is deleted, not cataloged.

## Decision tables

#### Extract job steps by earlier return codes

| Highest return code of earlier steps | Step action | Rule |
|---|---|---|
| 0 | Back up transaction category file | TTRDM-BR-164 |
| 0 | Unload transaction types to new file | TTRDM-BR-166 |
| 0 to 4 | Unload transaction categories to new file | TTRDM-BR-169 |
| Other than 0 | Skip transaction category backup | TTRDM-BR-165 |
| Other than 0 | **Gap:** No rule states what happens to the transaction type unload when an earlier step ended with a non-zero return code. | |
| Above 4 | **Gap:** No rule states explicitly that the transaction category unload is skipped when an earlier step ended above 4. | |


## Design notes

- TTRDM-BR-163: The first step of the scheduled extract job copies the current transaction type file to a new backup version, under the retention policy set up for these backups, before any new file is produced.
- TTRDM-BR-164: This step runs only if every earlier step of the job succeeded. It copies the current transaction category file to a new backup version. The job needs step-level success tracking so this step can be skipped.
- TTRDM-BR-167: This is a sorted extract of the transaction type table in a fixed-width layout. Each record is the 2-character type code, the description padded to 50 characters, and eight '0' filler characters, 60 characters in total. Downstream readers depend on this exact layout.
- TTRDM-BR-170: This is a sorted extract of the transaction category table in a fixed-width layout. Each record is the type code, the category code, the category description padded to 50 characters, and four '0' filler characters, 60 characters in total.

## Open questions

- SME-288: The transaction category unload runs if earlier steps ended with return code 4 or lower, while the other steps in the job need return code 0. Is the looser threshold intended, or should every step require return code 0? (Batch operations / application owner) On TTRDM-BR-165, TTRDM-BR-163, TTRDM-BR-168, TTRDM-BR-171.
- SME-289: The extract job removes the existing transaction type and category files between backup and rebuild. Should the modernized flow guarantee that a file is never removed unless its backup succeeded? (Batch operations / data owner) On TTRDM-BR-165, TTRDM-BR-163, TTRDM-BR-168, TTRDM-BR-171.
- SME-290: Who uses the transaction type and category extracts, and must the modernized extracts keep the exact fixed-length layout, including padding and trailing '0' characters? (Integration team) On TTRDM-BR-165, TTRDM-BR-163, TTRDM-BR-168, TTRDM-BR-171.
- DEF-136: Is this intended? Unlike every other step, the category unload runs when an earlier step ended with return code 4, so a warning in the transaction type unload still produces a category file while the earlier steps would have been skipped; the step's comment is also copied from the transaction type step. (Subject-matter expert) On TTRDM-BR-171.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (11 in all).
