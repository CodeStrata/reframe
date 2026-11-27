# List card master records (UP-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk medium

## Introduction

A read-only batch listing of every card on the card master, in card-number order. Operations staff use it to review card records. It must never change a card, must print each card exactly once with nothing after the last one, and must stop with a clear error rather than produce a partial listing when the file cannot be opened, read or closed.

**User story:** As an operations user, I want a listing of every card on the card master file, so that I can review card records without changing them.

## Requirements

### Requirement 1: UP-REQ-F-003 (design note)

#### Acceptance criteria

1. When the READCARD job runs, the system shall run the card master reader program (CBACT02C) with shared read access to the card master file AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS (CARDFILE), sending its messages and printed output to the job output listing (SYSOUT, SYSPRINT). (rules UP-BR-003)
2. GIVEN job submitted: READCARD; card master file: AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS WHEN the READCARD job runs THEN Step STEP05 runs CBACT02C, reading the card master file in shared mode, and its output appears in the job listing. (UP-C02-AC-01; UP-BR-003)

### Requirement 2: UP-REQ-F-004 (formatting)

#### Acceptance criteria

1. When the card listing job (READCARD) runs, the system shall print 'START OF EXECUTION OF PROGRAM CBACT02C', then each card record from the card master file once, in ascending card-number order, then 'END OF EXECUTION OF PROGRAM CBACT02C', opening the file for reading only so that no card is changed. (rules UP-BR-004, UP-BR-005)
2. GIVEN card master file: 3 cards: 4000000000000001, 4000000000000002, 4000000000000003 WHEN the card listing job (READCARD) runs THEN 'START OF EXECUTION OF PROGRAM CBACT02C', the three card records in that order, then 'END OF EXECUTION OF PROGRAM CBACT02C'; the file is unchanged (UP-C02-AC-02; UP-BR-004)
3. GIVEN customer records: 5 WHEN Customer Listing (CBCUS01C) runs THEN The customer listing has 10 record lines. (UP-C02-AC-03; UP-BR-005)
4. GIVEN card records: 5 WHEN Customer Listing (CBCUS01C) runs THEN The card listing has 5 record lines. (UP-C02-AC-04; UP-BR-005)

### Requirement 3: UP-REQ-F-005 (design note)

#### Acceptance criteria

1. When a read of the card master file returns status '00', the system shall treat the read as successful and print the record. (rules UP-BR-006)
2. GIVEN read file status: 00 WHEN a read of the card master file returns status '00' THEN The card record is printed (UP-C02-AC-05; UP-BR-006)

### Requirement 4: UP-REQ-F-006 (design note)

#### Acceptance criteria

1. When a read of the card master file returns status '10' (end of file), the system shall stop reading, print nothing for that read and end the listing normally, so that no blank or repeated record appears after the last card. (rules UP-BR-007, UP-BR-008)
2. GIVEN read file status: 10 WHEN a read of the card master file returns status '10' (end of file) THEN The loop ends, the file is closed and 'END OF EXECUTION OF PROGRAM CBACT02C' is printed (UP-C02-AC-06; UP-BR-007)
3. GIVEN card master file: empty WHEN a read reaches the end of the card master file THEN Only the start and end banners are printed (UP-C02-AC-07; UP-BR-008)

### Requirement 5: UP-REQ-F-007 (error handling)

#### Acceptance criteria

1. If a read of the card master file returns any status other than '00' or '10', then the system shall print 'ERROR READING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. (rules UP-BR-009)
2. GIVEN The card listing job has opened the card master and printed some cards WHEN A read of the card master returns status '23' (any status other than '00' or '10') THEN The job prints 'ERROR READING CARDFILE', then 'FILE STATUS IS: NNNN' followed by the 4-digit status, then 'ABENDING PROGRAM'. It ends abnormally with code 999 and prints no more cards. (UP-C02-AC-08; UP-BR-009)

### Requirement 6: UP-REQ-F-008 (error handling)

#### Acceptance criteria

1. If the card master file cannot be opened (any file status other than '00', for example '35' when the file is missing), then the system shall print 'ERROR OPENING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. (rules UP-BR-010)
2. GIVEN The card master file is missing, so opening it returns status '35' WHEN The card listing job starts THEN The job prints 'ERROR OPENING CARDFILE', then 'FILE STATUS IS: NNNN' followed by the 4-digit status, then 'ABENDING PROGRAM'. It ends abnormally with code 999 and prints no card records. (UP-C02-AC-09; UP-BR-010)

### Requirement 7: UP-REQ-F-009 (error handling)

#### Acceptance criteria

1. If closing the card master file returns any file status other than '00', then the system shall print 'ERROR CLOSING CARDFILE', 'FILE STATUS IS: NNNN' followed by the 4-digit status, and 'ABENDING PROGRAM', then abend with code 999. (rules UP-BR-011)
2. GIVEN The card listing job has printed every card and reached end of file WHEN Closing the card master returns a status other than '00' THEN The job prints 'ERROR CLOSING CARDFILE', then 'FILE STATUS IS: NNNN' followed by the 4-digit status, then 'ABENDING PROGRAM', and ends abnormally with code 999. (UP-C02-AC-10; UP-BR-011)

## Screens and components

No screens: it runs as scheduled job.

## Data models

#### CVACT02Y

File record of CBACT02C. Source: `app/cpy/CVACT02Y.cpy`.

Record `CARD-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| CARD-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| CARD-CVV-CD |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| CARD-EMBOSSED-NAME |  | X(50) | text, 50 characters |  |  |  |
| CARD-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| CARD-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| FILLER |  | X(59) | text, 59 characters |  |  |  |

#### CVACT03Y

File record of CBACT03C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |


## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- UP-BR-003: job submitted = READCARD; card master file = AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS → Step STEP05 runs CBACT02C, reading the card master file in shared mode, and its output appears in the job listing.
- UP-BR-004: card master file = 3 cards: 4000000000000001, 4000000000000002, 4000000000000003 → 'START OF EXECUTION OF PROGRAM CBACT02C', the three card records in that order, then 'END OF EXECUTION OF PROGRAM CBACT02C'; the file is unchanged
- UP-BR-005: customer records = 5 → The customer listing has 10 record lines.
- UP-BR-005: card records = 5 → The card listing has 5 record lines.
- UP-BR-006: read file status = 00 → The card record is printed
- UP-BR-007: read file status = 10 → The loop ends, the file is closed and 'END OF EXECUTION OF PROGRAM CBACT02C' is printed
- UP-BR-008: card master file = empty → Only the start and end banners are printed

## Decision tables

#### Card master read outcome

| Card master read file status | Card Listing action | Rule |
|---|---|---|
| '00' | Treat read as successful and print the record | UP-BR-006 |
| '10' (end of file) | Stop reading, print nothing for that read, end the listing normally | UP-BR-007 |
| any other status | Print 'ERROR READING CARDFILE', file status and 'ABENDING PROGRAM', abend with code 999 | UP-BR-009 |


## Design notes

- UP-BR-003: A scheduled or on-demand report job that reads the card store through a read-only connection, so it can run while online users are working. Its progress messages and the listing go to the job's log or report output.
- UP-BR-006: Each successful fetch of the next card in the ordered read is written to the report. The new application needs a sequential read of all cards, ordered by card number.
- UP-BR-007: When the cursor or stream runs out of cards, the job ends normally. End of data is the normal way to finish, not an error.
- UP-BR-008: Iterate until there are no more rows and write nothing for the empty fetch, so no blank or repeated line appears after the last card.

## Open questions

- SME-010: The cross-reference and customer listings print every record twice. Does anything rely on that, or should each record be printed once? (Batch operations) On UP-BR-005.
- DEF-097: Is this intended? Each record is displayed twice, once in the read paragraph and once in the main loop; CBACT02C has the same read-paragraph display commented out, suggesting the duplicate is debug output left in by mistake. (Subject-matter expert) On UP-BR-005.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).
