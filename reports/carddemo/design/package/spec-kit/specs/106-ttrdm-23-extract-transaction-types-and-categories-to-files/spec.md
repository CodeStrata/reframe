# Feature specification: Extract transaction types and categories to files

**Feature:** TTRDM-C23 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C23)

As an operations user, I want to back up the current transaction type and category files and unload fresh copies from the database, so that downstream processing such as the transaction report has current reference data.

Backs up the current transaction type and category files, then produces fresh copies from the database for downstream use such as the transaction report. Types are written in type code order and categories in type then category order, as fixed 60-character records. A failed unload must never leave a partial file behind.

**Acceptance scenarios:**

1. **Given** Transaction type file: AWS.M2.CARDDEMO.TRANTYPE.PS from the previous run, **when** transaction type extract job (TRANEXTR) runs, **then** A new generation of AWS.M2.CARDDEMO.TRANTYPE.BKUP holds a copy of it. (TTRDM-C23-AC-01)
2. **Given** Return code of the transaction type backup step: 0, **when** every earlier step of the transaction type extract job (TRANEXTR) ended with return code 0, **then** The current category file is copied into a new backup generation. (TTRDM-C23-AC-02)
3. **Given** Return code of the transaction type backup step: 12, **when** any earlier step of the transaction type extract job ended with a return code other than 0, **then** No new category backup generation is created. (TTRDM-C23-AC-03)
4. **Given** Earlier step return codes: all 0; Transaction types in the table: '02', '01', **when** every earlier step of the transaction type extract job ended with return code 0, **then** The new file holds type '01' then type '02'. (TTRDM-C23-AC-04)
5. **Given** Earlier step return codes: one step ended 8, **when** every earlier step of the transaction type extract job ended with return code 0, **then** The unload is skipped and no new transaction type file is written. (TTRDM-C23-AC-05)
6. **Given** Unload step: abends, **when** the transaction type unload fails, **then** AWS.M2.CARDDEMO.TRANTYPE.PS is deleted, not cataloged. (TTRDM-C23-AC-06)
7. **Given** Highest earlier step return code: 4, **when** no earlier step of the transaction type extract job ended with a return code above 4, **then** The category unload still runs. (TTRDM-C23-AC-07)
8. **Given** Highest earlier step return code: 8, **when** no earlier step of the transaction type extract job ended with a return code above 4, **then** The category unload is skipped. (TTRDM-C23-AC-08)
9. **Given** Unload step: abends, **when** the transaction category unload fails, **then** AWS.M2.CARDDEMO.TRANCATG.PS is deleted, not cataloged. (TTRDM-C23-AC-09)
10. **Given** The transaction type table holds type code '01' with description 'Purchase', **when** The transaction type extract runs, **then** The extract file holds a 60-character record made of '01', then 'Purchase' padded with spaces to 50 characters, then '00000000' (TTRDM-C23-AC-10)
11. **Given** The transaction type category table holds a category for type code '01' with category description 'Regular Sales Draft', **when** The transaction category extract runs, **then** The extract file holds one 60-character record for it, made of the type code '01', then the category code, then 'Regular Sales Draft' padded with spaces to 50 characters, then '0000' (TTRDM-C23-AC-11)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-151** (design note): The system shall first copy the current transaction type file (AWS.M2.CARDDEMO.TRANTYPE.PS) into a new cataloged generation of the transaction type backup (AWS.M2.CARDDEMO.TRANTYPE.BKUP) of fixed 60-byte records. Rules: TTRDM-BR-163.
- **TTRDM-REQ-F-152** (design note): When every earlier step of the transaction type extract job (TRANEXTR) ended with return code 0, the system shall copy the current transaction category file (AWS.M2.CARDDEMO.TRANCATG.PS) into a new cataloged generation of the category backup (AWS.M2.CARDDEMO.TRANCATG.PS.BKUP) of fixed 60-byte records. Rules: TTRDM-BR-164.
- **TTRDM-REQ-F-153** (error handling): If any earlier step of the transaction type extract job ended with a return code other than 0, then the system shall skip the transaction category backup. Rules: TTRDM-BR-165.
- **TTRDM-REQ-F-154** (side effect): When every earlier step of the transaction type extract job ended with return code 0, the system shall unload all transaction types from the Db2 table CARDDEMO.TRANSACTION_TYPE, in type code order, to a new transaction type file (AWS.M2.CARDDEMO.TRANTYPE.PS) for the transaction report. Rules: TTRDM-BR-166.
- **TTRDM-REQ-F-155** (design note): The system shall write each extracted transaction type as one 60-character record: the type code, the description padded to 50 characters, then eight '0' characters. Rules: TTRDM-BR-167.
- **TTRDM-REQ-F-156** (error handling): If the transaction type unload fails, then the system shall delete the new transaction type file instead of keeping it. Rules: TTRDM-BR-168.
- **TTRDM-REQ-F-157** (side effect): When no earlier step of the transaction type extract job ended with a return code above 4, the system shall unload all transaction categories from the Db2 table CARDDEMO.TRANSACTION_TYPE_CATEGORY, in type code then category order, to a new transaction category file (AWS.M2.CARDDEMO.TRANCATG.PS). Rules: TTRDM-BR-169.
- **TTRDM-REQ-F-158** (design note): The system shall write each extracted category as one 60-character record: the type code, the category code, the category description padded to 50 characters, then four '0' characters. Rules: TTRDM-BR-170.
- **TTRDM-REQ-F-159** (error handling): If the transaction category unload fails, then the system shall delete the new transaction category file instead of keeping it. Rules: TTRDM-BR-171.

### Business rules

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

### Key entities

None found in the source.

### Needs clarification

- SME-288: The transaction category unload runs if earlier steps ended with return code 4 or lower, while the other steps in the job need return code 0. Is the looser threshold intended, or should every step require return code 0? (Batch operations / application owner) On TTRDM-BR-165, TTRDM-BR-163, TTRDM-BR-168, TTRDM-BR-171.
- SME-289: The extract job removes the existing transaction type and category files between backup and rebuild. Should the modernized flow guarantee that a file is never removed unless its backup succeeded? (Batch operations / data owner) On TTRDM-BR-165, TTRDM-BR-163, TTRDM-BR-168, TTRDM-BR-171.
- SME-290: Who uses the transaction type and category extracts, and must the modernized extracts keep the exact fixed-length layout, including padding and trailing '0' characters? (Integration team) On TTRDM-BR-165, TTRDM-BR-163, TTRDM-BR-168, TTRDM-BR-171.
- DEF-136: Is this intended? Unlike every other step, the category unload runs when an earlier step ended with return code 4, so a warning in the transaction type unload still produces a category file while the earlier steps would have been skipped; the step's comment is also copied from the transaction type step. (Subject-matter expert) On TTRDM-BR-171.

### Decision table gaps

- Extract job steps by earlier return codes: No rule states what happens to the transaction type unload when an earlier step ended with a non-zero return code.
- Extract job steps by earlier return codes: No rule states explicitly that the transaction category unload is skipped when an earlier step ended above 4.
