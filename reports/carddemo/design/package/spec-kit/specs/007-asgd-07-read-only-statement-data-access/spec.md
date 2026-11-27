# Feature specification: Read-only statement data access

**Feature:** ASGD-C07 · Account Statement Generation and Delivery · Customer Account Self-Service

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ASGD-C07)

As a statement operations team, I want statement data read through a routine that only reads files and returns each file outcome, so that producing statements never changes customer, account, card or transaction records.

Statement data is read only through a data-access layer that reads files and reports each outcome. Producing statements therefore never changes customer, account, card or transaction records. The layer must never write, change or delete data, and it must report not-found and end-of-data outcomes accurately so the run can stop or continue correctly.

**Acceptance scenarios:**

1. **Given** File: 'TRNXFILE'; Operation: 'R'; Transactions left: none, **when** statement file routine (CBSTM03B) runs, **then** Outcome code '10' is returned. (ASGD-C07-AC-01)
2. **Given** File: 'XREFFILE'; Operation: 'O', **when** statement file routine (CBSTM03B) runs, **then** Outcome code '00' is returned when the file opens. (ASGD-C07-AC-02)
3. **Given** File: 'ACCTFILE', **when** statement program (CBSTM03A) runs, **then** It is opened, read by key for each card, and closed at the end. (ASGD-C07-AC-03)
4. **Given** File: 'TRNXFILE'; Operation: 'R', **when** statement file routine (CBSTM03B) runs, **then** The next transaction in card number and transaction id order is returned in the 1000-byte data area. (ASGD-C07-AC-04)
5. **Given** File: 'CUSTFILE'; Operation: 'W', **when** statement file routine (CBSTM03B) runs, **then** Nothing is written; the customer file is unchanged. (ASGD-C07-AC-05)
6. **Given** A customer record exists for the given customer ID, and no record exists for a second ID, **when** The statement program asks for each customer by key, **then** The first lookup returns that customer's record with status '00', and the second returns status '23' (ASGD-C07-AC-06)
7. **Given** An account record exists for the 11-digit account ID 00000000001, and no record exists for 00000000099, **when** The statement program asks for each account by key, **then** The lookup for 00000000001 returns the account record with status '00', and the lookup for 00000000099 returns status '23' (ASGD-C07-AC-07)
8. **Given** The customer file and the account file, **when** The statement program opens each one, reads by key and closes it, **then** Each operation is allowed and returns its file status. Reading by key is the only read the statement program uses on these files. (ASGD-C07-AC-08)

## Requirements

### Functional requirements

- **ASGD-REQ-F-033** (design note): When the statement program asks for a customer record by key, the system shall take the given number of key characters as the customer id and read that customer directly, returning the record and status '00' when found and status '23' when not found. Rules: ASGD-BR-033.
- **ASGD-REQ-F-034** (design note): When the statement program asks for an account record by key, the system shall take the given number of key characters as the 11-digit account id and read that account directly, returning the record and status '00' when found and status '23' when not found. Rules: ASGD-BR-034.
- **ASGD-REQ-F-035** (error handling): The system shall return the file status of every open, read or close to the calling program as the outcome code, for example '00' for success, '10' for end of file on a sequential read and '23' for a key not found. Rules: ASGD-BR-035.
- **ASGD-REQ-F-036** (design note): The system shall drive each statement file in the order open, read one or more times, then close. Rules: ASGD-BR-008.
- **ASGD-REQ-F-037** (design note): The system shall let the transaction file (TRNXFILE) and card cross-reference file (XREFFILE) be opened, read in key order (card number and transaction id for transactions, card number for the cross-reference) and closed. Rules: ASGD-BR-036.
- **ASGD-REQ-F-038** (design note): The system shall let the customer file (CUSTFILE) and account file (ACCTFILE) be opened, read by key and closed. Rules: ASGD-BR-037.
- **ASGD-REQ-N-002** (design note): The system shall open all four statement files for input only, so it never adds, changes or deletes records, even though write ('W') and rewrite ('Z') operation codes are defined. Rules: ASGD-BR-038.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-033 | Keyed customer/account lookup uses caller-supplied key length | design note | WHEN the statement program asks for a customer record by key, THE statement file routine (CBSTM03B) SHALL take the given number of key characters as the customer id and read that customer directly, returning the record and status '00' when found and status '23' when not found. | medium | app/cbl/CBSTM03B.CBL:43-53, app/cbl/CBSTM03B.CBL:188-201, app/cbl/CBSTM03B.CBL:213-226, app/cbl/CBSTM03A.CBL:366-382 |
| ASGD-BR-034 | Keyed customer/account lookup uses caller-supplied key length | design note | WHEN the statement program asks for an account record by key, THE statement file routine (CBSTM03B) SHALL take the given number of key characters as the 11-digit account id and read that account directly, returning the record and status '00' when found and status '23' when not found. | medium | app/cbl/CBSTM03B.CBL:43-53, app/cbl/CBSTM03B.CBL:188-201, app/cbl/CBSTM03B.CBL:213-226, app/cbl/CBSTM03A.CBL:366-382 |
| ASGD-BR-035 | File status passed back to the caller as the outcome code | error handling | THE statement file routine (CBSTM03B) SHALL return the file status of every open, read or close it performs to the calling program as the outcome code, for example '00' for success, '10' for end of file on a sequential read and '23' for a key not found. | medium | app/cbl/CBSTM03B.CBL:151-152, app/cbl/CBSTM03B.CBL:175-176, app/cbl/CBSTM03B.CBL:200-201, app/cbl/CBSTM03B.CBL:225-226 |
| ASGD-BR-008 | File status passed back to the caller as the outcome code | design note | THE statement program (CBSTM03A) SHALL drive each file through the routine in the order open, read one or more times, then close. | medium | app/cbl/CBSTM03B.CBL:151-152, app/cbl/CBSTM03B.CBL:175-176, app/cbl/CBSTM03B.CBL:200-201, app/cbl/CBSTM03B.CBL:225-226 |
| ASGD-BR-036 | Statement data access: allowed operations per file | design note | THE statement file routine (CBSTM03B) SHALL let the transaction file (TRNXFILE) and card cross-reference file (XREFFILE) be opened, read in key order (card number and transaction id for transactions, card number for the cross-reference) and closed. | medium | app/cbl/CBSTM03B.CBL:31-53, app/cbl/CBSTM03B.CBL:100-112, app/cbl/CBSTM03B.CBL:114-229 |
| ASGD-BR-037 | Statement data access: allowed operations per file | design note | THE statement file routine (CBSTM03B) SHALL let the customer file (CUSTFILE) and account file (ACCTFILE) be opened, read by key and closed. | medium | app/cbl/CBSTM03B.CBL:31-53, app/cbl/CBSTM03B.CBL:100-112, app/cbl/CBSTM03B.CBL:114-229 |
| ASGD-BR-038 | Statement data access: allowed operations per file | design note | THE statement file routine (CBSTM03B) SHALL open all four files for input only, so it never adds, changes or deletes records, even though write ('W') and rewrite ('Z') operation codes are defined. | medium | app/cbl/CBSTM03B.CBL:31-53, app/cbl/CBSTM03B.CBL:100-112, app/cbl/CBSTM03B.CBL:114-229 |

### Key entities

None found in the source.

### Needs clarification

- SME-035: Does the caller always pass a key length of 9 for customer lookups and 11 for account lookups? Should the new system check the key length, and check that the account key is numeric, before looking it up? (Application architect) On ASGD-BR-034.
- DEF-175: Is this intended? An operation a file does not support (for example 'R' on CUSTFILE, or 'W' or 'Z' on any file) does nothing but still returns that file's last status, often '00', so the caller would take it as success; an unknown file name returns without setting any outcome code. (Subject-matter expert) On ASGD-BR-038.

### Decision table gaps

None.
