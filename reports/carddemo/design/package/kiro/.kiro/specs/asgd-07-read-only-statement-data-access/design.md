# Design: Read-only statement data access (ASGD-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Statement data is read only through a data-access layer that reads files and reports each outcome. Producing statements therefore never changes customer, account, card or transaction records. The layer must never write, change or delete data, and it must report not-found and end-of-data outcomes accurately so the run can stop or continue correctly.

Runs as scheduled job.

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