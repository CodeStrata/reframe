# Requirements: List card master records (UP-C02)

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
