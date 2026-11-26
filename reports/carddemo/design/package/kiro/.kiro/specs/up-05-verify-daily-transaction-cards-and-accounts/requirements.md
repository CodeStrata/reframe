# Requirements: Verify daily transaction cards and accounts (UP-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as service · risk medium

## Introduction

A batch check of the day's transactions. For each one it looks up the card on the card cross-reference and then looks up the linked account, reporting cards and accounts that cannot be found. Operations staff use it to see bad transactions before posting. It must never quietly pass an unknown card, and it must stop the whole run at once if any file cannot be opened, read or closed.

**User story:** As an operations user, I want each daily transaction's card checked against the card cross-reference and its account looked up, so that transactions with unknown cards or accounts are reported.

## Requirements

### Requirement 1: UP-REQ-F-015 (design note)

#### Acceptance criteria

1. The system shall read the daily transaction file one record at a time from the start, show each record read, and verify its card, stopping when the file reports end of file (status '10'). (rules UP-BR-017)
2. GIVEN Daily transaction file: 3 records WHEN daily transaction verification batch runs THEN Each of the 3 records is shown and its card looked up; the 4th read returns status '10' and the loop ends, after which the files are closed and 'END OF EXECUTION OF PROGRAM CBTRN01C' is shown. (UP-C05-AC-01; UP-BR-017)

### Requirement 2: UP-REQ-F-016 (error handling)

#### Acceptance criteria

1. If reading the daily transaction file returns a status other than '00' or '10', then the system shall show 'ERROR READING DAILY TRANSACTION FILE' and the file status ('FILE STATUS IS: NNNN' followed by the code), then abend with code 999. (rules UP-BR-018)
2. GIVEN The verification run is reading the daily transaction file WHEN A read returns a status other than '00' or '10' THEN The run shows 'ERROR READING DAILY TRANSACTION FILE' and 'FILE STATUS IS: NNNN' followed by the status code, ends abnormally with code 999, and verifies no more transactions. (UP-C05-AC-06; UP-BR-018)

### Requirement 3: UP-REQ-F-017 (business rule)

#### Acceptance criteria

1. When a daily transaction has been read, the system shall look up the transaction's card number, by exact match, in the card cross-reference file to find the linked account and customer. (rules UP-BR-019)
2. GIVEN Transaction ID: T000000000000001; Card number: 4111111111111111 WHEN a daily transaction has been read THEN The batch looks up card 4111111111111111 in the card cross-reference file. (UP-C05-AC-02; UP-BR-019)

### Requirement 4: UP-REQ-F-018 (formatting)

#### Acceptance criteria

1. When the card number is found in the cross-reference, the system shall show 'SUCCESSFUL READ OF XREF' with the card number, account ID and customer ID, and then look up the linked account on the account master. (rules UP-BR-020)
2. GIVEN A daily transaction whose card number exists in the card cross-reference, linked to an account ID and a customer ID WHEN The transaction is verified THEN The run shows 'SUCCESSFUL READ OF XREF' with that card number, account ID and customer ID, and then looks up that account ID on the account master. (UP-C05-AC-07; UP-BR-020)

### Requirement 5: UP-REQ-F-019 (business rule)

#### Acceptance criteria

1. If the card number is not in the cross-reference, then the system shall show 'INVALID CARD NUMBER FOR XREF' and 'CARD NUMBER <card> COULD NOT BE VERIFIED. SKIPPING TRANSACTION ID-<transaction ID>', and shall not look up any account for that transaction. (rules UP-BR-021)
2. GIVEN A daily transaction with ID T1 whose card number C1 is not in the card cross-reference WHEN The transaction is verified THEN The run shows 'INVALID CARD NUMBER FOR XREF' and 'CARD NUMBER C1 COULD NOT BE VERIFIED. SKIPPING TRANSACTION ID-T1'. It looks up no account for that transaction and goes on to the next transaction. (UP-C05-AC-08; UP-BR-021)

### Requirement 6: UP-REQ-F-020 (business rule)

#### Acceptance criteria

1. While the transaction card was found in the card cross-reference, when the account lookup for the cross-referenced account id in the account store fails (not found), the system shall display 'ACCOUNT <account id> NOT FOUND'. (rules UP-BR-022)
2. GIVEN Transaction card number: 4111111111111111 (found in cross-reference); Cross-referenced account id: 00000000042 (in account file) WHEN the transaction card was found in the card cross-reference (`WS-XREF-READ-STATUS` = 0), WHEN the account lookup for the cross-referenced account id fails (account read status `WS-ACCT-READ-STATUS` is not 0, set to 4 when not found) THEN The job log shows 'SUCCESSFUL READ OF ACCOUNT FILE' and no not-found message (UP-C05-AC-03; UP-BR-022)

### Requirement 7: UP-REQ-F-021 (error handling)

#### Acceptance criteria

1. If any of the six files fails to open (status not '00'), then the system shall show the open error for that file ('ERROR OPENING DAILY TRANSACTION FILE', 'ERROR OPENING CUSTOMER FILE', 'ERROR OPENING CROSS REF FILE', 'ERROR OPENING CARD FILE', 'ERROR OPENING ACCOUNT FILE' or 'ERROR OPENING TRANSACTION FILE') and the file status, then abend with code 999 before processing any transaction. (rules UP-BR-023)
2. GIVEN The cross-reference file cannot be opened (open status is not '00'), and the other files open normally WHEN The verification run starts THEN The run shows 'ERROR OPENING CROSS REF FILE' and the file status, and ends abnormally with code 999 before any transaction is processed. A failure on any of the other files gives that file's own message in the same way: 'ERROR OPENING DAILY TRANSACTION FILE', 'ERROR OPENING CUSTOMER FILE', 'ERROR OPENING CARD FILE', 'ERROR OPENING ACCOUNT FILE' or 'ERROR OPENING TRANSACTION FILE'. (UP-C05-AC-09; UP-BR-023)

### Requirement 8: UP-REQ-F-022 (error handling)

#### Acceptance criteria

1. If any file fails to close at the end of the run (status not '00'), then the system shall show the close error for that file and its file status, then abend with code 999. (rules UP-BR-024)
2. GIVEN Cross-reference file close status: '92' WHEN any file fails to close at the end of the run (status not '00') THEN The log shows 'ERROR CLOSING CROSS REF FILE' and the file status, then 'ABENDING PROGRAM'; the job abends with code 999. (UP-C05-AC-04; UP-BR-024)

### Requirement 9: UP-REQ-F-023 (historical artifact)

#### Acceptance criteria

1. The system shall open the customer, card and transaction files at start and close them at end even though it never reads or writes them, so that a missing customer, card or transaction file still stops the job. (rules UP-BR-025)
2. GIVEN Card file: not available (open status '35') WHEN daily transaction verification batch runs THEN The log shows 'ERROR OPENING CARD FILE' and the job abends with code 999, although no card record would have been used. (UP-C05-AC-05; UP-BR-025)

### Requirement 10: UP-REQ-F-024 (formatting)

#### Acceptance criteria

1. When a file status is not numeric or starts with '9', the system shall show it as 'FILE STATUS IS: NNNN' followed by the first character and the binary value of the second character as three digits, and otherwise shall show 'FILE STATUS IS: NNNN00' followed by the two-digit status. (rules UP-BR-026)
2. GIVEN A file operation in the verification run fails with the numeric status '35' WHEN The run shows the file status THEN It shows 'FILE STATUS IS: NNNN0035', that is, 'NNNN00' followed by the two-digit status. (UP-C05-AC-10; UP-BR-026)
3. GIVEN A file operation fails with a status whose first character is '9' (or that is not numeric) WHEN The run shows the file status THEN It shows 'FILE STATUS IS: NNNN' followed by the first status character and then the binary value of the second status character as three digits. (UP-C05-AC-11; UP-BR-026)
