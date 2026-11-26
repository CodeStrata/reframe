# Requirements: Log unknown record types during import (CPBM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as scheduled job · risk high

## Introduction

Logs every migration record whose type is not 'C', 'A', 'X', 'T' or 'D' to an error report so the operator can see which records were not imported. Each entry holds the timestamp, the record type, the export sequence number and 'Unknown record type encountered', separated by '\|'. An unknown record must never be imported into any target file, and a failure to write the error entry does not stop the import.

**User story:** As a branch migration operator, I want export records of an unknown type logged to an error report, so that I can see which records were not imported.

## Requirements

### Requirement 1: CPBM-REQ-F-022 (error handling)

#### Acceptance criteria

1. If an export record's type is not 'C', 'A', 'X', 'T' or 'D', then the system shall count it as an unknown record type and write an error entry to the error report file (ERROR-OUTPUT) holding the current timestamp, the record type, the export sequence number and the message 'Unknown record type encountered', separated by '\|'. (rules CPBM-BR-026, CPBM-BR-027)
2. GIVEN Export record type: 'Z'; Sequence number: 000000123 WHEN an export record's type is not `'C'`, `'A'`, `'X'`, `'T'` or `'D'` THEN An error line with the current timestamp, type 'Z', sequence 000000123 and 'Unknown record type encountered' is written to the error report, and the unknown-type and errors-written counts each go up by 1 (CPBM-C06-AC-01; CPBM-BR-026)
3. GIVEN Export record type: 'A' WHEN an export record's type is not `'C'`, `'A'`, `'X'`, `'T'` or `'D'` THEN The record is imported as an account record; no error line is written (CPBM-C06-AC-02; CPBM-BR-026)
4. GIVEN record type: 'Z'; export sequence number: 57 WHEN an export record has any record type other than 'C', 'A', 'X', 'T' or 'D' THEN An error record with type 'Z', sequence 0000057 and 'Unknown record type encountered' is written to the import error file; nothing goes to the master import files. (CPBM-C06-AC-03; CPBM-BR-027)

### Requirement 2: CPBM-REQ-F-023 (error handling)

#### Acceptance criteria

1. If the error record cannot be written, then the system shall display 'ERROR: Writing error record, Status: ' with the file status and carry on importing, still counting the error as written. (rules CPBM-BR-028)
2. GIVEN error file write status: '37' WHEN the error record cannot be written THEN The message is displayed, the run continues and the errors-written count still goes up by 1. (CPBM-C06-AC-04; CPBM-BR-028)
