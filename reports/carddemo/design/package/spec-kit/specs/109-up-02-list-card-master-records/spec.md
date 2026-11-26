# Feature specification: List card master records

**Feature:** UP-C02 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C02)

As an operations user, I want a listing of every card on the card master file, so that I can review card records without changing them.

A read-only batch listing of every card on the card master, in card-number order. Operations staff use it to review card records. It must never change a card, must print each card exactly once with nothing after the last one, and must stop with a clear error rather than produce a partial listing when the file cannot be opened, read or closed.

**Acceptance scenarios:**

1. **Given** job submitted: READCARD; card master file: AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS, **when** the READCARD job runs, **then** Step STEP05 runs CBACT02C, reading the card master file in shared mode, and its output appears in the job listing. (UP-C02-AC-01)
2. **Given** card master file: 3 cards: 4000000000000001, 4000000000000002, 4000000000000003, **when** the card listing job (READCARD) runs, **then** 'START OF EXECUTION OF PROGRAM CBACT02C', the three card records in that order, then 'END OF EXECUTION OF PROGRAM CBACT02C'; the file is unchanged (UP-C02-AC-02)
3. **Given** customer records: 5, **when** Customer Listing (CBCUS01C) runs, **then** The customer listing has 10 record lines. (UP-C02-AC-03)
4. **Given** card records: 5, **when** Customer Listing (CBCUS01C) runs, **then** The card listing has 5 record lines. (UP-C02-AC-04)
5. **Given** read file status: 00, **when** a read of the card master file returns status '00', **then** The card record is printed (UP-C02-AC-05)
6. **Given** read file status: 10, **when** a read of the card master file returns status '10' (end of file), **then** The loop ends, the file is closed and 'END OF EXECUTION OF PROGRAM CBACT02C' is printed (UP-C02-AC-06)
7. **Given** card master file: empty, **when** a read reaches the end of the card master file, **then** Only the start and end banners are printed (UP-C02-AC-07)
8. **Given** The card listing job has opened the card master and printed some cards, **when** A read of the card master returns status '23' (any status other than '00' or '10'), **then** The job prints 'ERROR READING CARDFILE', then 'FILE STATUS IS: NNNN' followed by the 4-digit status, then 'ABENDING PROGRAM'. It ends abnormally with code 999 and prints no more cards. (UP-C02-AC-08)
9. **Given** The card master file is missing, so opening it returns status '35', **when** The card listing job starts, **then** The job prints 'ERROR OPENING CARDFILE', then 'FILE STATUS IS: NNNN' followed by the 4-digit status, then 'ABENDING PROGRAM'. It ends abnormally with code 999 and prints no card records. (UP-C02-AC-09)
10. **Given** The card listing job has printed every card and reached end of file, **when** Closing the card master returns a status other than '00', **then** The job prints 'ERROR CLOSING CARDFILE', then 'FILE STATUS IS: NNNN' followed by the 4-digit status, then 'ABENDING PROGRAM', and ends abnormally with code 999. (UP-C02-AC-10)

## Requirements

### Functional requirements

- **UP-REQ-F-003** (design note): When the READCARD job runs, the system shall run the card master reader program (CBACT02C) with shared read access to the card master file AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS (CARDFILE), sending its messages and printed output to the job output listing (SYSOUT, SYSPRINT). Rules: UP-BR-003.
- **UP-REQ-F-004** (formatting): When the card listing job (READCARD) runs, the system shall print 'START OF EXECUTION OF PROGRAM CBACT02C', then each card record from the card master file once, in ascending card-number order, then 'END OF EXECUTION OF PROGRAM CBACT02C', opening the file for reading only so that no card is changed. Rules: UP-BR-004, UP-BR-005.
- **UP-REQ-F-005** (design note): When a read of the card master file returns status '00', the system shall treat the read as successful and print the record. Rules: UP-BR-006.
- **UP-REQ-F-006** (design note): When a read of the card master file returns status '10' (end of file), the system shall stop reading, print nothing for that read and end the listing normally, so that no blank or repeated record appears after the last card. Rules: UP-BR-007, UP-BR-008.
- **UP-REQ-F-007** (error handling): If a read of the card master file returns any status other than '00' or '10', then the system shall print 'ERROR READING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. Rules: UP-BR-009.
- **UP-REQ-F-008** (error handling): If the card master file cannot be opened (any file status other than '00', for example '35' when the file is missing), then the system shall print 'ERROR OPENING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. Rules: UP-BR-010.
- **UP-REQ-F-009** (error handling): If closing the card master file returns any file status other than '00', then the system shall print 'ERROR CLOSING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. Rules: UP-BR-011.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-003 | Run the card master reader | design note | WHEN the READCARD job runs, THE card master read run SHALL run the card master reader program (CBACT02C) with shared read access to the card master file AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS (CARDFILE), sending its messages and printed output to the job output listing (SYSOUT, SYSPRINT). | medium | app/jcl/READCARD.jcl:1-2, app/jcl/READCARD.jcl:20-28 |
| UP-BR-004 | List every card record until exhausted | formatting | WHEN the card listing job (READCARD) runs, THE Card Listing program SHALL print 'START OF EXECUTION OF PROGRAM CBACT02C', then each card record from the card master file once, in ascending card-number order, then 'END OF EXECUTION OF PROGRAM CBACT02C'. It opens the file for reading only, so no card is changed. | high | app/cbl/CBACT02C.cbl:28-33, app/cbl/CBACT02C.cbl:70-87, app/cbl/CBACT02C.cbl:92-116, app/cbl/CBACT02C.cbl:118-120 |
| UP-BR-005 | Each record is printed twice in the cross-reference and customer dumps | historical artifact | THE Customer Listing (CBCUS01C) SHALL likewise print each customer record twice, while the Card Listing (CBACT02C) prints each card record once because its second print is commented out. | high | app/cbl/CBACT03C.cbl:74-81, app/cbl/CBACT03C.cbl:92-96, app/cbl/CBACT03C.cbl:98-108, app/cbl/CBCUS01C.cbl:78 |
| UP-BR-006 | Read outcome classification: success, end of file, or fatal error | design note | WHEN a read of the card master file returns status '00', THE Card Listing program SHALL treat the read as successful and print the record. | medium | app/cbl/CBACT02C.cbl:92-116, app/cbl/CBACT02C.cbl:154-158, app/cbl/CBACT02C.cbl:161-174 |
| UP-BR-007 | Read outcome classification: success, end of file, or fatal error | design note | WHEN a read of the card master file returns status '10' (end of file), THE Card Listing program SHALL end the listing normally. | medium | app/cbl/CBACT02C.cbl:92-116, app/cbl/CBACT02C.cbl:154-158, app/cbl/CBACT02C.cbl:161-174 |
| UP-BR-008 | List every card record until exhausted | design note | WHEN a read reaches the end of the card master file, THE Card Listing program SHALL stop reading and print nothing for that read, so no blank or repeated record appears after the last card. | high | app/cbl/CBACT02C.cbl:28-33, app/cbl/CBACT02C.cbl:70-87, app/cbl/CBACT02C.cbl:92-116, app/cbl/CBACT02C.cbl:118-120 |
| UP-BR-009 | Read outcome classification: success, end of file, or fatal error | error handling | WHEN a read of the card master file returns any status other than '00' or '10', THE Card Listing program SHALL print 'ERROR READING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. | medium | app/cbl/CBACT02C.cbl:92-116, app/cbl/CBACT02C.cbl:154-158, app/cbl/CBACT02C.cbl:161-174 |
| UP-BR-010 | Open and close must succeed or the job abends | error handling | WHEN the card master file cannot be opened (any file status other than '00', for example '35' when the file is missing), THE Card Listing program SHALL print 'ERROR OPENING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. | medium | app/cbl/CBACT02C.cbl:118-152, app/cbl/CBACT02C.cbl:154-158, app/cbl/CBACT02C.cbl:161-174 |
| UP-BR-011 | Open and close must succeed or the job abends | error handling | WHEN closing the card master file returns any file status other than '00', THE Card Listing program SHALL print 'ERROR CLOSING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. | medium | app/cbl/CBACT02C.cbl:118-152, app/cbl/CBACT02C.cbl:154-158, app/cbl/CBACT02C.cbl:161-174 |

### Key entities

- CVACT02Y (file record)
- CVACT03Y (file record)

### Needs clarification

- SME-010: The cross-reference and customer listings print every record twice. Does anything rely on that, or should each record be printed once? (Batch operations) On UP-BR-005.
- DEF-097: Is this intended? Each record is displayed twice, once in the read paragraph and once in the main loop; CBACT02C has the same read-paragraph display commented out, suggesting the duplicate is debug output left in by mistake. (Subject-matter expert) On UP-BR-005.

### Decision table gaps

None.
