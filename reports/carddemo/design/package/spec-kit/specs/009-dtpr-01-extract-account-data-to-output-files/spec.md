# Feature specification: Extract account data to output files

**Feature:** DTPR-C01 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C01)

As an operations analyst, I want each account on the account master file extracted to the account output, balance array and variable-length files, so that downstream processes receive the account details in the formats they expect.

A scheduled extract that reads every account on the account master and writes it out in four formats for downstream processes: a flat account record, a balance array record, and two variable-length records (one with status, one with financial details). It serves operations analysts and the systems that consume these extracts. It must never skip or duplicate an account, so N accounts always give N, N and 2N records. It must also stop the run on any read or write error rather than produce a partial extract.

**Acceptance scenarios:**

1. **Given** ACCT-CURR-CYC-DEBIT: 0.00, **when** the account's current cycle debit equals zero, **then** The output record's cycle debit (OUT-ACCT-CURR-CYC-DEBIT) is 2525.00. (DTPR-C01-AC-01)
2. **Given** ACCT-CURR-CYC-DEBIT: 150.00, **when** the account's current cycle debit equals zero, **then** The output cycle debit is not set to 2525.00 (the code does not copy 150.00 into it either). (DTPR-C01-AC-02)
3. **Given** Current cycle debit: 0.00, **when** the account's current cycle debit is zero, **then** Output cycle debit 2525.00 (DTPR-C01-AC-03)
4. **Given** Current cycle debit: 310.50, **when** the account's current cycle debit is zero, **then** Output cycle debit is not set from the account (310.50 is not written) (DTPR-C01-AC-04)
5. **Given** ACCT-ID: 00000000001; ACCT-CURR-BAL: 1940.00, **when** an account has been read successfully, **then** The array record holds account 00000000001 with slot 1 balance 1940.00 / cycle debit 1005.00, slot 2 balance 1940.00 / cycle debit 1525.00, slot 3 balance -1025.00 / cycle debit -2500.00. (DTPR-C01-AC-05)
6. **Given** ACCT-ID: 00000000002; ACCT-CURR-BAL: 0.00, **when** an account has been read successfully, **then** Slots 1 and 2 hold balance 0.00 with cycle debits 1005.00 and 1525.00; slot 3 is still -1025.00 / -2500.00 whatever the account holds. (DTPR-C01-AC-06)
7. **Given** Accounts on the account master file: 3, **when** an account is read successfully from the account master file, **then** 3 records on OUTFILE, 3 on ARRYFILE, 6 on VBRCFILE (DTPR-C01-AC-07)
8. **Given** File: balance array file (ARRYFILE); Write status: '10', **when** a write to any of the three output files returns file status '00' or '10', **then** No error; processing continues (DTPR-C01-AC-08)
9. **Given** File: account output file (OUTFILE); Write status: '00', **when** a write to the account output file, **then** Processing continues with the next write (DTPR-C01-AC-09)
10. **Given** Read status: '10', **when** reading the account master file returns status '10', **then** Loop ends; 'END OF EXECUTION OF PROGRAM CBACT01C' displayed (DTPR-C01-AC-10)
11. **Given** an account on the account master with ID 00000000001, active status 'Y', current balance 1500.00, credit limit 5000.00, cash credit limit 1000.00, open date 2015-01-10, expiration date 2027-01-10, current cycle credit 200.00 and group ID 'A000000000', **when** the extract reads the account successfully, **then** the account output record holds account ID 00000000001, active status 'Y', current balance 1500.00, credit limit 5000.00, cash credit limit 1000.00, open date 2015-01-10, expiration date 2027-01-10, current cycle credit 200.00 and group ID 'A000000000', unchanged from the master (DTPR-C01-AC-11)
12. **Given** an account whose reissue date is '2025-03-15' (YYYY-MM-DD), **when** the extract reads the account successfully, **then** the account output record's reissue date is '20250315' (YYYYMMDD) (DTPR-C01-AC-12)
13. **Given** an account with ID 00000000001 and active status 'Y', **when** the extract reads the account successfully, **then** a 12-byte variable-length status record '00000000001Y' is written: the 11-digit account ID followed by the active status (DTPR-C01-AC-13)
14. **Given** an account with ID 00000000001, current balance 1500.00, credit limit 5000.00 and reissue date '2025-03-15', **when** the extract reads the account successfully and has written the status record, **then** a 39-byte variable-length financial record is written next, holding account ID 00000000001, current balance 1500.00, credit limit 5000.00 and reissue year '2025' (DTPR-C01-AC-14)
15. **Given** an extract run in progress, **when** reading the account master returns a file status other than '00' or '10' (for example '30'), **then** the run displays 'ERROR READING ACCOUNT FILE' with status '30' and abends with code 999, and does not end normally (DTPR-C01-AC-15)

## Requirements

### Functional requirements

- **DTPR-REQ-F-001** (design note): When an account record is read successfully, the system shall copy the account ID, active status, current balance, credit limit, cash credit limit, open date, expiration date, current cycle credit and group ID to the account output record. Rules: DTPR-BR-001.
- **DTPR-REQ-F-002** (design note): When an account record is read successfully, the system shall convert the account reissue date from YYYY-MM-DD to YYYYMMDD and write it as the output reissue date. Rules: DTPR-BR-002, DTPR-BR-003.
- **DTPR-REQ-F-003** (business rule): When the account's current cycle debit equals zero, the system shall set the output current cycle debit to 2525.00. Rules: DTPR-BR-004, DTPR-BR-005.
- **DTPR-REQ-F-004** (business rule): The system shall not copy a non-zero current cycle debit to the account output record. Rules: DTPR-BR-005.
- **DTPR-REQ-F-005** (historical artifact): When an account record is read successfully, the system shall write a balance array record holding the account identifier and the current balance in cycle slots 1 and 2 with cycle debits 1005.00 and 1525.00, and slot 3 with balance -1025.00 and cycle debit -2500.00. Rules: DTPR-BR-006.
- **DTPR-REQ-F-006** (design note): When an account record is read successfully, the system shall write a 12-byte variable-length status record holding the 11-digit account ID followed by the account active status. Rules: DTPR-BR-007.
- **DTPR-REQ-F-007** (design note): When an account record is read successfully, the system shall then write a 39-byte variable-length financial record holding the account ID, current balance, credit limit and the four-digit year of the reissue date. Rules: DTPR-BR-002, DTPR-BR-008.
- **DTPR-REQ-F-008** (design note): When an account is read successfully from the account master file, the system shall write one account output record, one balance array record and two variable-length records and then read the next account, so that N accounts give N, N and 2N records. Rules: DTPR-BR-009.
- **DTPR-REQ-F-009** (error handling): When a write to any of the three output files returns file status '00' or '10', the system shall treat the write as successful and continue processing. Rules: DTPR-BR-010.
- **DTPR-REQ-F-010** (error handling): If a write to the account output file, the balance array file or either variable-length record write returns a file status other than '00' or '10', then the system shall display 'ACCOUNT FILE WRITE STATUS IS:' with the status, 'FILE STATUS IS: NNNN' with the four-digit status and 'ABENDING PROGRAM', and abend with code 999. Rules: DTPR-BR-011.
- **DTPR-REQ-F-011** (design note): When reading the account master file returns status '10', the system shall treat it as end of file, stop reading, close the account file and end normally with 'END OF EXECUTION OF PROGRAM CBACT01C'. Rules: DTPR-BR-012.
- **DTPR-REQ-F-012** (error handling): If reading the account master file returns a status other than '00' or '10', then the system shall display 'ERROR READING ACCOUNT FILE' with the file status and abend with code 999. Rules: DTPR-BR-013.

### Business rules

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

### Key entities

- CVACT01Y (file record)
- CODATECN (working storage)

### Needs clarification

- SME-006: The account extract replaces a zero cycle debit with 2,525.00, and the balance array record is filled with fixed amounts (cycle debits 1,005.00, 1,525.00 and -2,500.00; a balance of -1,025.00). Are these real business values or test data to be replaced? And when an account has a non-zero cycle debit, should its own value be carried through to the extract? (Business analyst) On DTPR-BR-004, DTPR-BR-006, DTPR-BR-002, DTPR-BR-005, DTPR-BR-008, DTPR-BR-011, DTPR-BR-009.
- SME-007: The extract accepts a write result of '10' as well as '00' as success. Should accepting '10' be kept in the new system? (Technical lead) On DTPR-BR-004, DTPR-BR-006, DTPR-BR-002, DTPR-BR-005, DTPR-BR-008, DTPR-BR-011, DTPR-BR-009.
- SME-008: Do downstream consumers depend on the exact fixed record layouts of the account extracts (including the different status and financial record lengths), so they must be kept? (Integration team) On DTPR-BR-004, DTPR-BR-006, DTPR-BR-002, DTPR-BR-005, DTPR-BR-008, DTPR-BR-011, DTPR-BR-009.
- SME-009: Does anything downstream use the balance array file, or is it a demo/test file that can be dropped or replaced with real data? (Downstream data owner) On DTPR-BR-006.
- DEF-031: Is this intended? Every write failure, including those on the array and variable-record files, is reported with the same text 'ACCOUNT FILE WRITE STATUS IS:', so the message does not say which file failed; status '10' (end of file) is also accepted on a write, where it has no meaning. (Subject-matter expert) On DTPR-BR-011.
- DEF-070: Is this intended? At the end of the run only the account master file is closed; the three output files are never explicitly closed and rely on the runtime closing them at GOBACK. (Subject-matter expert) On DTPR-BR-009, DTPR-BR-013.
- DEF-108: Is this intended? The current cycle debit is only set (to the fixed 2525.00) when the account's value is zero; a non-zero cycle debit is never copied, so the output carries whatever was left in the record area. COBDATFT's 'INVALID INPUT' error result is also never checked. (Subject-matter expert) On DTPR-BR-005.

### Decision table gaps

None.
