# Read-only statement data access (ASGD-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Account Self-Service · Account Statement Generation and Delivery · runs as scheduled job · risk high

## Introduction

Statement data is read only through a data-access layer that reads files and reports each outcome. Producing statements therefore never changes customer, account, card or transaction records. The layer must never write, change or delete data, and it must report not-found and end-of-data outcomes accurately so the run can stop or continue correctly.

**User story:** As a statement operations team, I want statement data read through a routine that only reads files and returns each file outcome, so that producing statements never changes customer, account, card or transaction records.

## Requirements

### Requirement 1: ASGD-REQ-F-033 (design note)

#### Acceptance criteria

1. When the statement program asks for a customer record by key, the system shall take the given number of key characters as the customer id and read that customer directly, returning the record and status '00' when found and status '23' when not found. (rules ASGD-BR-033)
2. GIVEN A customer record exists for the given customer ID, and no record exists for a second ID WHEN The statement program asks for each customer by key THEN The first lookup returns that customer's record with status '00', and the second returns status '23' (ASGD-C07-AC-06; ASGD-BR-033)

### Requirement 2: ASGD-REQ-F-034 (design note)

#### Acceptance criteria

1. When the statement program asks for an account record by key, the system shall take the given number of key characters as the 11-digit account id and read that account directly, returning the record and status '00' when found and status '23' when not found. (rules ASGD-BR-034)
2. GIVEN An account record exists for the 11-digit account ID 00000000001, and no record exists for 00000000099 WHEN The statement program asks for each account by key THEN The lookup for 00000000001 returns the account record with status '00', and the lookup for 00000000099 returns status '23' (ASGD-C07-AC-07; ASGD-BR-034)

### Requirement 3: ASGD-REQ-F-035 (error handling)

#### Acceptance criteria

1. The system shall return the file status of every open, read or close to the calling program as the outcome code, for example '00' for success, '10' for end of file on a sequential read and '23' for a key not found. (rules ASGD-BR-035)
2. GIVEN File: 'TRNXFILE'; Operation: 'R'; Transactions left: none WHEN statement file routine (CBSTM03B) runs THEN Outcome code '10' is returned. (ASGD-C07-AC-01; ASGD-BR-035)
3. GIVEN File: 'XREFFILE'; Operation: 'O' WHEN statement file routine (CBSTM03B) runs THEN Outcome code '00' is returned when the file opens. (ASGD-C07-AC-02; ASGD-BR-035)

### Requirement 4: ASGD-REQ-F-036 (design note)

#### Acceptance criteria

1. The system shall drive each statement file in the order open, read one or more times, then close. (rules ASGD-BR-008)
2. GIVEN File: 'ACCTFILE' WHEN statement program (CBSTM03A) runs THEN It is opened, read by key for each card, and closed at the end. (ASGD-C07-AC-03; ASGD-BR-008)

### Requirement 5: ASGD-REQ-F-037 (design note)

#### Acceptance criteria

1. The system shall let the transaction file (TRNXFILE) and card cross-reference file (XREFFILE) be opened, read in key order (card number and transaction id for transactions, card number for the cross-reference) and closed. (rules ASGD-BR-036)
2. GIVEN File: 'TRNXFILE'; Operation: 'R' WHEN statement file routine (CBSTM03B) runs THEN The next transaction in card number and transaction id order is returned in the 1000-byte data area. (ASGD-C07-AC-04; ASGD-BR-036)

### Requirement 6: ASGD-REQ-F-038 (design note)

#### Acceptance criteria

1. The system shall let the customer file (CUSTFILE) and account file (ACCTFILE) be opened, read by key and closed. (rules ASGD-BR-037)
2. GIVEN The customer file and the account file WHEN The statement program opens each one, reads by key and closes it THEN Each operation is allowed and returns its file status. Reading by key is the only read the statement program uses on these files. (ASGD-C07-AC-08; ASGD-BR-037)

### Requirement 7: ASGD-REQ-N-002 (design note)

#### Acceptance criteria

1. The system shall open all four statement files for input only, so it never adds, changes or deletes records, even though write ('W') and rewrite ('Z') operation codes are defined. (rules ASGD-BR-038)
2. GIVEN File: 'CUSTFILE'; Operation: 'W' WHEN statement file routine (CBSTM03B) runs THEN Nothing is written; the customer file is unchanged. (ASGD-C07-AC-05; ASGD-BR-038)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-033 | Keyed customer/account lookup uses caller-supplied key length | design note | WHEN the statement program asks for a customer record by key, THE statement file routine (CBSTM03B) SHALL take the given number of key characters as the customer id and read that customer directly, returning the record and status '00' when found and status '23' when not found. | medium | app/cbl/CBSTM03B.CBL:43-53, app/cbl/CBSTM03B.CBL:188-201, app/cbl/CBSTM03B.CBL:213-226, app/cbl/CBSTM03A.CBL:366-382 |
| ASGD-BR-034 | Keyed customer/account lookup uses caller-supplied key length | design note | WHEN the statement program asks for an account record by key, THE statement file routine (CBSTM03B) SHALL take the given number of key characters as the 11-digit account id and read that account directly, returning the record and status '00' when found and status '23' when not found. | medium | app/cbl/CBSTM03B.CBL:43-53, app/cbl/CBSTM03B.CBL:188-201, app/cbl/CBSTM03B.CBL:213-226, app/cbl/CBSTM03A.CBL:366-382 |
| ASGD-BR-035 | File status passed back to the caller as the outcome code | error handling | THE statement file routine (CBSTM03B) SHALL return the file status of every open, read or close it performs to the calling program as the outcome code, for example '00' for success, '10' for end of file on a sequential read and '23' for a key not found. | medium | app/cbl/CBSTM03B.CBL:151-152, app/cbl/CBSTM03B.CBL:175-176, app/cbl/CBSTM03B.CBL:200-201, app/cbl/CBSTM03B.CBL:225-226 |
| ASGD-BR-008 | File status passed back to the caller as the outcome code | design note | THE statement program (CBSTM03A) SHALL drive each file through the routine in the order open, read one or more times, then close. | medium | app/cbl/CBSTM03B.CBL:151-152, app/cbl/CBSTM03B.CBL:175-176, app/cbl/CBSTM03B.CBL:200-201, app/cbl/CBSTM03B.CBL:225-226 |
| ASGD-BR-036 | Statement data access: allowed operations per file | design note | THE statement file routine (CBSTM03B) SHALL let the transaction file (TRNXFILE) and card cross-reference file (XREFFILE) be opened, read in key order (card number and transaction id for transactions, card number for the cross-reference) and closed. | medium | app/cbl/CBSTM03B.CBL:31-53, app/cbl/CBSTM03B.CBL:100-112, app/cbl/CBSTM03B.CBL:114-229 |
| ASGD-BR-037 | Statement data access: allowed operations per file | design note | THE statement file routine (CBSTM03B) SHALL let the customer file (CUSTFILE) and account file (ACCTFILE) be opened, read by key and closed. | medium | app/cbl/CBSTM03B.CBL:31-53, app/cbl/CBSTM03B.CBL:100-112, app/cbl/CBSTM03B.CBL:114-229 |
| ASGD-BR-038 | Statement data access: allowed operations per file | design note | THE statement file routine (CBSTM03B) SHALL open all four files for input only, so it never adds, changes or deletes records, even though write ('W') and rewrite ('Z') operation codes are defined. | medium | app/cbl/CBSTM03B.CBL:31-53, app/cbl/CBSTM03B.CBL:100-112, app/cbl/CBSTM03B.CBL:114-229 |

### Worked examples

- ASGD-BR-035: File = 'TRNXFILE'; Operation = 'R'; Transactions left = none → Outcome code '10' is returned.
- ASGD-BR-035: File = 'XREFFILE'; Operation = 'O' → Outcome code '00' is returned when the file opens.
- ASGD-BR-008: File = 'ACCTFILE' → It is opened, read by key for each card, and closed at the end.
- ASGD-BR-036: File = 'TRNXFILE'; Operation = 'R' → The next transaction in card number and transaction id order is returned in the 1000-byte data area.
- ASGD-BR-038: File = 'CUSTFILE'; Operation = 'W' → Nothing is written; the customer file is unchanged.

## Decision tables

None.

## Design notes

- ASGD-BR-033: Look up a customer directly by primary key (customer ID) and return the record, or a 'not found' result that the caller can tell apart from other failures. The legacy program passes the key length in from the caller. The new application should use a typed customer ID instead.
- ASGD-BR-034: Look up an account directly by its 11-digit account ID (primary key) and return the record or a clear 'not found' result. Validate the ID as 11 digits rather than relying on a key length the caller supplies.
- ASGD-BR-008: Every data source the statement job uses follows the lifecycle open, read one or more times, close. Use scoped resources that are always released, including when the run fails.
- ASGD-BR-036: Transactions must be readable in order of (card number, transaction ID), and the card cross-reference in card-number order. These are ordered sequential reads, such as streams or cursors over a sorted query, with a clear end-of-data signal.
- ASGD-BR-037: Customers and accounts are needed only for keyed point lookups. No scans or ordered reads are needed for them.
- ASGD-BR-038: The statement job's data access must be read-only. Use read-only connections or a read replica with credentials that cannot write. Expose no write or update operations, even though the legacy routine defines 'W' and 'Z' operation codes.

## Open questions

- SME-035: Does the caller always pass a key length of 9 for customer lookups and 11 for account lookups? Should the new system check the key length, and check that the account key is numeric, before looking it up? (Application architect) On ASGD-BR-034.
- DEF-175: Is this intended? An operation a file does not support (for example 'R' on CUSTFILE, or 'W' or 'Z' on any file) does nothing but still returns that file's last status, often '00', so the caller would take it as success; an unknown file name returns without setting any outcome code. (Subject-matter expert) On ASGD-BR-038.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
