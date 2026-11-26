# Feature specification: Log unknown record types during import

**Feature:** CPBM-C06 · Customer Profile Branch Migration · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CPBM-C06)

As a branch migration operator, I want export records of an unknown type logged to an error report, so that I can see which records were not imported.

Logs every migration record whose type is not 'C', 'A', 'X', 'T' or 'D' to an error report so the operator can see which records were not imported. Each entry holds the timestamp, the record type, the export sequence number and 'Unknown record type encountered', separated by '\|'. An unknown record must never be imported into any target file, and a failure to write the error entry does not stop the import.

**Acceptance scenarios:**

1. **Given** Export record type: 'Z'; Sequence number: 000000123, **when** an export record's type is not `'C'`, `'A'`, `'X'`, `'T'` or `'D'`, **then** An error line with the current timestamp, type 'Z', sequence 000000123 and 'Unknown record type encountered' is written to the error report, and the unknown-type and errors-written counts each go up by 1 (CPBM-C06-AC-01)
2. **Given** Export record type: 'A', **when** an export record's type is not `'C'`, `'A'`, `'X'`, `'T'` or `'D'`, **then** The record is imported as an account record; no error line is written (CPBM-C06-AC-02)
3. **Given** record type: 'Z'; export sequence number: 57, **when** an export record has any record type other than 'C', 'A', 'X', 'T' or 'D', **then** An error record with type 'Z', sequence 0000057 and 'Unknown record type encountered' is written to the import error file; nothing goes to the master import files. (CPBM-C06-AC-03)
4. **Given** error file write status: '37', **when** the error record cannot be written, **then** The message is displayed, the run continues and the errors-written count still goes up by 1. (CPBM-C06-AC-04)

## Requirements

### Functional requirements

- **CPBM-REQ-F-022** (error handling): If an export record's type is not 'C', 'A', 'X', 'T' or 'D', then the system shall count it as an unknown record type and write an error entry to the error report file (ERROR-OUTPUT) holding the current timestamp, the record type, the export sequence number and the message 'Unknown record type encountered', separated by '\|'. Rules: CPBM-BR-026, CPBM-BR-027.
- **CPBM-REQ-F-023** (error handling): If the error record cannot be written, then the system shall display 'ERROR: Writing error record, Status: ' with the file status and carry on importing, still counting the error as written. Rules: CPBM-BR-028.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CPBM-BR-026 | Log unknown record type to error report | error handling | WHEN an export record's type is not `'C'`, `'A'`, `'X'`, `'T'` or `'D'`, THE Import Error Reporting SHALL write an error entry to the error report file (`ERROR-OUTPUT`) containing the current timestamp, the record type, the sequence number and the message 'Unknown record type encountered' | low | app/cbl/CBIMPORT.cbl:283-284,425,429-432,434,437,439, app/jcl/CBIMPORT.jcl:283-284,425,429-432,434,437,439, app/cbl/CBIMPORT.cbl:425-446 |
| CPBM-BR-027 | Route each export record to its target master file by record type | error handling | WHEN an export record has any record type other than 'C', 'A', 'X', 'T' or 'D', THE import batch SHALL count it as an unknown record type and write an error record holding the current timestamp, the record type, the export sequence number and the message 'Unknown record type encountered', separated by '\|'. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |
| CPBM-BR-028 | Route each export record to its target master file by record type | error handling | WHEN the error record cannot be written, THE import batch SHALL display 'ERROR: Writing error record, Status: ' with the file status and carry on importing, still counting the error as written. | high | app/cbl/CBIMPORT.cbl:37-41, app/cbl/CBIMPORT.cbl:248-285, app/cbl/CBIMPORT.cbl:351-446, app/cbl/CBIMPORT.cbl:152-160 |

### Key entities

- CVACT01Y (file record)
- CVACT02Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CVEXPORT (file record)
- CVTRA05Y (file record)

### Needs clarification

- SME-023: Imported card records go to a separate card output that is not listed among the import job's outputs. Where should imported card records be stored, and are they deleted on failure like the other import files? (Migration architecture team) On CPBM-BR-026.
- SME-024: After an export record with an unknown type is logged as an error, should the import carry on with the next record or stop? (Migration business analyst) On CPBM-BR-026.
- SME-025: If the import cannot write an entry to its error file, should the run stop? (Migration business analyst) On CPBM-BR-026.
- SME-027: How important is the rule that sends each import record to its target master file by record type (customer, account, cross-reference, transaction, card; anything else to the error log)? Is it core to the system, or a rule that would be costly to get wrong? (Data migration lead) On CPBM-BR-028.
- DEF-089: Is this intended? The job (CBIMPORT.jcl) has no CARDOUT DD, so opening the card output is likely to fail and abend the run before any record is read; if the runtime allocates it dynamically, the card records go to a temporary file that is not kept. Also, a failed error-file write is still counted as written, and the 9-digit export sequence number is cut to 7 digits in the error record. (Subject-matter expert) On CPBM-BR-028.

### Decision table gaps

None.
