# Design: Extract account data to output files (DTPR-C01)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Overview

A scheduled extract that reads every account on the account master and writes it out in four formats for downstream processes: a flat account record, a balance array record, and two variable-length records (one with status, one with financial details). It serves operations analysts and the systems that consume these extracts. It must never skip or duplicate an account, so N accounts always give N, N and 2N records. It must also stop the run on any read or write error rather than produce a partial extract.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

#### CVACT01Y

File record of CBACT01C. Source: `app/cpy/CVACT01Y.cpy`.

Record `ACCOUNT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| ACCT-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| ACCT-CURR-BAL |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CASH-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-OPEN-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-REISSUE-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-CURR-CYC-CREDIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CURR-CYC-DEBIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| ACCT-GROUP-ID |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(178) | text, 178 characters |  |  |  |

- CODATECN (working storage of CBACT01C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-001 | Build account output record with reformatted reissue date | design note | WHEN an account is read successfully, THE account extract job SHALL copy the account ID, active status, current balance, credit limit, cash credit limit, open date, expiration date, current cycle credit and group ID to the account output record. | medium | app/cbl/CBACT01C.cbl:215-240, app/asm/COBDATFT.asm:46-54, app/cpy/CODATECN.cpy:17-39 |
| DTPR-BR-002 | Stage account reissue date | design note | WHEN an account record is read successfully, THE account extract job SHALL copy the account reissue date (YYYY-MM-DD) both to the date-conversion input and to a working date whose first four characters give the reissue year used in the financial variable-length record. | medium | app/cbl/CBACT01C.cbl:131-137, app/cbl/CBACT01C.cbl:223-224, app/cbl/CBACT01C.cbl:282 |
| DTPR-BR-003 | Build account output record with reformatted reissue date | design note | WHEN an account is read successfully, THE account extract job SHALL convert the reissue date from YYYY-MM-DD to YYYYMMDD by calling the date routine (COBDATFT, input and output type '2') and write it as the output reissue date. | medium | app/cbl/CBACT01C.cbl:215-240, app/asm/COBDATFT.asm:46-54, app/cpy/CODATECN.cpy:17-39 |
| DTPR-BR-004 | Default zero cycle debit to fixed amount | business rule | WHEN the account's current cycle debit equals zero, THE Account Output Record Builder SHALL set the output cycle debit to 2525.00 | medium | app/cbl/CBACT01C.cbl:236-238, app/cbl/CBACT01C.cbl:236-238 |
| DTPR-BR-005 | Build account output record with reformatted reissue date | business rule | WHEN the account's current cycle debit is zero, THE account extract job SHALL set the output current cycle debit to 2525.00; a non-zero cycle debit is not copied to the output record. | medium | app/cbl/CBACT01C.cbl:215-240, app/asm/COBDATFT.asm:46-54, app/cpy/CODATECN.cpy:17-39 |
| DTPR-BR-006 | Populate account balance array record | historical artifact | WHEN an account has been read successfully, THE Balance Array Builder SHALL copy the account identifier and the current balance into cycle slots 1 and 2 with cycle debits `1005.00` and `1525.00`, and set slot 3 to balance `-1025.00` and cycle debit `-2500.00` | medium | app/cbl/CBACT01C.cbl:253-260, app/cbl/CBACT01C.cbl:253-261 |
| DTPR-BR-007 | Populate account status and financial records | design note | WHEN an account record is read successfully, THE account extract job SHALL write a 12-byte variable-length status record holding the 11-digit account ID followed by the account active status. | high | app/cbl/CBACT01C.cbl:123-130, app/cbl/CBACT01C.cbl:276-285, app/cbl/CBACT01C.cbl:287-290, app/cbl/CBACT01C.cbl:302-305 |
| DTPR-BR-008 | Populate account status and financial records | design note | WHEN an account record is read successfully, THE account extract job SHALL then write a 39-byte variable-length financial record holding the account ID, current balance, credit limit and the four-digit year of the reissue date. | high | app/cbl/CBACT01C.cbl:123-130, app/cbl/CBACT01C.cbl:276-285, app/cbl/CBACT01C.cbl:287-290, app/cbl/CBACT01C.cbl:302-305 |
| DTPR-BR-009 | Process successfully read account | design note | WHEN an account is read successfully from the account master file, THE account extract job SHALL write one record to the account output file, one record to the balance array file and two records to the variable-length file, then read the next account, so N accounts give N, N and 2N records. | high | app/cbl/CBACT01C.cbl:141-160, app/cbl/CBACT01C.cbl:165-198, app/cbl/CBACT01C.cbl:388-410 |
| DTPR-BR-010 | Write 12-byte account status record | error handling | WHEN a write to any of the three output files returns file status '00' or '10', THE account extract job SHALL treat the write as successful and continue processing. | high | app/cbl/CBACT01C.cbl:242-251, app/cbl/CBACT01C.cbl:263-274, app/cbl/CBACT01C.cbl:287-300, app/cbl/CBACT01C.cbl:302-315 |
| DTPR-BR-011 | Write 12-byte account status record | error handling | WHEN a write to the account output file, the balance array file, or either variable-length record write (12-byte status, 39-byte financial) returns a file status other than '00' or '10', THE account extract job SHALL display 'ACCOUNT FILE WRITE STATUS IS:' with the status, display 'FILE STATUS IS: NNNN' with the four-digit status, display 'ABENDING PROGRAM' and abend with code 999. | high | app/cbl/CBACT01C.cbl:242-251, app/cbl/CBACT01C.cbl:263-274, app/cbl/CBACT01C.cbl:287-300, app/cbl/CBACT01C.cbl:302-315 |
| DTPR-BR-012 | Sequential extract run lifecycle and end-of-file handling | design note | WHEN reading the account master file returns status '10', THE account extract job SHALL treat it as end of file, stop the loop, close the account file and end normally with 'END OF EXECUTION OF PROGRAM CBACT01C'. | high | app/cbl/CBACT01C.cbl:141-160, app/cbl/CBACT01C.cbl:165-198, app/cbl/CBACT01C.cbl:388-410 |
| DTPR-BR-013 | Sequential extract run lifecycle and end-of-file handling | error handling | WHEN reading the account master file returns a status other than '00' or '10', THE account extract job SHALL display 'ERROR READING ACCOUNT FILE' and the file status, and abend with code 999. | high | app/cbl/CBACT01C.cbl:141-160, app/cbl/CBACT01C.cbl:165-198, app/cbl/CBACT01C.cbl:388-410 |

### Worked examples

- DTPR-BR-004: ACCT-CURR-CYC-DEBIT = 0.00 → The output record's cycle debit (OUT-ACCT-CURR-CYC-DEBIT) is 2525.00.
- DTPR-BR-004: ACCT-CURR-CYC-DEBIT = 150.00 → The output cycle debit is not set to 2525.00 (the code does not copy 150.00 into it either).
- DTPR-BR-005: Current cycle debit = 0.00 → Output cycle debit 2525.00
- DTPR-BR-005: Current cycle debit = 310.50 → Output cycle debit is not set from the account (310.50 is not written)
- DTPR-BR-006: ACCT-ID = 00000000001; ACCT-CURR-BAL = 1940.00 → The array record holds account 00000000001 with slot 1 balance 1940.00 / cycle debit 1005.00, slot 2 balance 1940.00 / cycle debit 1525.00, slot 3 balance -1025.00 / cycle debit -2500.00.
- DTPR-BR-006: ACCT-ID = 00000000002; ACCT-CURR-BAL = 0.00 → Slots 1 and 2 hold balance 0.00 with cycle debits 1005.00 and 1525.00; slot 3 is still -1025.00 / -2500.00 whatever the account holds.
- DTPR-BR-009: Accounts on the account master file = 3 → 3 records on OUTFILE, 3 on ARRYFILE, 6 on VBRCFILE
- DTPR-BR-010: File = balance array file (ARRYFILE); Write status = '10' → No error; processing continues
- DTPR-BR-011: File = account output file (OUTFILE); Write status = '00' → Processing continues with the next write
- DTPR-BR-012: Read status = '10' → Loop ends; 'END OF EXECUTION OF PROGRAM CBACT01C' displayed

## Decision tables

#### Account master read outcome

| Account master read status | Extract action | Rule |
|---|---|---|
| '00' (read successfully) | Write one account output, one balance array and two variable-length records, then read the next account | DTPR-BR-009 |
| '10' | End of file: stop, close the account file and end normally | DTPR-BR-012 |
| Other than '00' or '10' | Display 'ERROR READING ACCOUNT FILE' with status and abend with code 999 | DTPR-BR-013 |


## Design notes

- DTPR-BR-001: Map each account straight onto the flat account extract record: ID, active status, current balance, credit limit, cash credit limit, open date, expiration date, current cycle credit and group ID, with no changes to the values. Define the extract layout as a versioned contract that its downstream consumers agree to.
- DTPR-BR-002: Parse the reissue date once from its stored YYYY-MM-DD form. Use it both for the YYYYMMDD output date and for the four-digit reissue year in the financial record, so the two can never disagree.
- DTPR-BR-003: Use a standard date library to reformat the reissue date from YYYY-MM-DD to YYYYMMDD instead of a separate shared date-conversion routine. Decide and test how an invalid or blank reissue date is handled.
- DTPR-BR-007: Produce a fixed 12-character status record per account: the account ID zero-padded to 11 digits, then the one-character active status. Downstream readers depend on the exact width.
- DTPR-BR-008: After each account's status record, produce a 39-byte financial record (account ID, current balance, credit limit, reissue year) in the same output stream. Keep the order status-then-financial for each account, and give the numeric fields an agreed fixed encoding.
- DTPR-BR-009: Process accounts as a sequential stream over the whole account master. Each account produces exactly one account record, one balance array record and two variable-length records, so the record counts can be reconciled (N, N, 2N) at the end of the run.
- DTPR-BR-012: Treat running out of accounts as normal completion: close the source and log the completion message 'END OF EXECUTION OF PROGRAM CBACT01C' (or an agreed equivalent) with a success exit status for the scheduler.

## Open questions

- SME-006: The account extract replaces a zero cycle debit with 2,525.00, and the balance array record is filled with fixed amounts (cycle debits 1,005.00, 1,525.00 and -2,500.00; a balance of -1,025.00). Are these real business values or test data to be replaced? And when an account has a non-zero cycle debit, should its own value be carried through to the extract? (Business analyst) On DTPR-BR-004, DTPR-BR-006, DTPR-BR-002, DTPR-BR-005, DTPR-BR-008, DTPR-BR-011, DTPR-BR-009.
- SME-007: The extract accepts a write result of '10' as well as '00' as success. Should accepting '10' be kept in the new system? (Technical lead) On DTPR-BR-004, DTPR-BR-006, DTPR-BR-002, DTPR-BR-005, DTPR-BR-008, DTPR-BR-011, DTPR-BR-009.
- SME-008: Do downstream consumers depend on the exact fixed record layouts of the account extracts (including the different status and financial record lengths), so they must be kept? (Integration team) On DTPR-BR-004, DTPR-BR-006, DTPR-BR-002, DTPR-BR-005, DTPR-BR-008, DTPR-BR-011, DTPR-BR-009.
- SME-009: Does anything downstream use the balance array file, or is it a demo/test file that can be dropped or replaced with real data? (Downstream data owner) On DTPR-BR-006.
- DEF-031: Is this intended? Every write failure, including those on the array and variable-record files, is reported with the same text 'ACCOUNT FILE WRITE STATUS IS:', so the message does not say which file failed; status '10' (end of file) is also accepted on a write, where it has no meaning. (Subject-matter expert) On DTPR-BR-011.
- DEF-070: Is this intended? At the end of the run only the account master file is closed; the three output files are never explicitly closed and rely on the runtime closing them at GOBACK. (Subject-matter expert) On DTPR-BR-009, DTPR-BR-013.
- DEF-108: Is this intended? The current cycle debit is only set (to the fixed 2525.00) when the account's value is zero; a non-zero cycle debit is never copied, so the output carries whatever was left in the record area. COBDATFT's 'INVALID INPUT' error result is also never checked. (Subject-matter expert) On DTPR-BR-005.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).