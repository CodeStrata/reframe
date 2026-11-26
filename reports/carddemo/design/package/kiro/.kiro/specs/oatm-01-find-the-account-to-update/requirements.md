# Requirements: Find the account to update (OATM-C01)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Lets an operator enter an account id and fetches the linked card cross-reference, account and customer records so the details can be reviewed and updated. It records what was fetched as the original snapshot that later change detection and the concurrency check compare against. It must never present or update details for an account or customer that was not actually found, and must stop at the first missing record with the right message.

**User story:** As an operator, I want to enter an account id and have the system fetch the linked card, account and customer records, so that I can review and update the right account and customer details.

## Requirements

### Requirement 1: OATM-REQ-F-001 (formatting)

#### Acceptance criteria

1. When the account update screen is shown on first entry to the function, the system shall set the information message to 'Enter or update id of account to update'. (rules OATM-BR-001)
2. GIVEN entry: first entry from the main menu WHEN the account update screen is shown on first entry to the function THEN Message 'Enter or update id of account to update' (OATM-C01-AC-01; OATM-BR-001)

### Requirement 2: OATM-REQ-F-002 (formatting)

#### Acceptance criteria

1. When the account update screen is shown, it is not a first entry, and no account details have been fetched yet, the system shall set the information message to 'Enter or update id of account to update'. (rules OATM-BR-002)
2. GIVEN account id entered: 00000000099 (not found); update stage: not fetched WHEN the account update screen is shown, it is not a first entry, and no account details have been fetched yet THEN Message 'Enter or update id of account to update' (OATM-C01-AC-02; OATM-BR-002)

### Requirement 3: OATM-REQ-F-003 (historical artifact)

#### Acceptance criteria

1. If no update stage matches and the information message is blank, then the system shall default the information message to 'Enter or update id of account to update'. (rules OATM-BR-003)
2. GIVEN update stage: unrecognised value; information message: blank WHEN no update stage matches and the information message is blank THEN Message 'Enter or update id of account to update' (OATM-C01-AC-03; OATM-BR-003)

### Requirement 4: OATM-REQ-F-004 (design note)

#### Acceptance criteria

1. When the account is found in the card cross-reference by account ID, the system shall take the customer ID and card number from it for the session and go on to read the account and customer. (rules OATM-BR-004)
2. GIVEN Account ID: 00000000011; Cross-reference: found, customer 000000011 WHEN the account is found in the card cross-reference (by account ID) THEN Customer 000000011 and its card number become the session customer and card. (OATM-C01-AC-04; OATM-BR-004)

### Requirement 5: OATM-REQ-F-005 (business rule)

#### Acceptance criteria

1. If the account is not in the card cross-reference, then the system shall flag the account as invalid, stop the lookup and show 'Account:<account> not found in Cross ref file. Resp:<resp> Reas:<reason>'. (rules OATM-BR-005)
2. GIVEN an operator has entered account id 00000000099 and no card cross-reference entry exists for that account WHEN the account lookup runs THEN the account is flagged invalid, the account and customer are not read, and the message 'Account:00000000099 not found in Cross ref file. Resp:<resp> Reas:<reason>' is shown with the returned response and reason codes (OATM-C01-AC-09; OATM-BR-005)

### Requirement 6: OATM-REQ-F-006 (error handling)

#### Acceptance criteria

1. If the card cross-reference read fails for any other reason, then the system shall flag the account as invalid, stop the lookup and show 'File Error: READ on CXACAIX returned RESP <resp>,RESP2 <reason>'. (rules OATM-BR-006)
2. GIVEN an operator has entered a valid account id and the card cross-reference read fails for a reason other than record not found WHEN the account lookup runs THEN the account is flagged invalid, the lookup stops before the account and customer reads, and the message 'File Error: READ on CXACAIX returned RESP <resp>,RESP2 <reason>' is shown with the returned codes (OATM-C01-AC-10; OATM-BR-006)

### Requirement 7: OATM-REQ-F-007 (design note)

#### Acceptance criteria

1. When the account master read succeeds, the system shall mark the account as found. (rules OATM-BR-007)
2. GIVEN account id: 00000000001; account master: record exists WHEN the account master read (ACCTDAT) succeeds THEN Account marked found (OATM-C01-AC-05; OATM-BR-007)

### Requirement 8: OATM-REQ-F-008 (error handling)

#### Acceptance criteria

1. If the account is not on the account master, then the system shall flag an input error, mark the account search invalid and, if no message is already set, report 'Account:<id> not found in Acct Master file.Resp:<resp> Reas:<reason>'. (rules OATM-BR-008)
2. GIVEN account 00000000011 is in the card cross-reference but not on the account master, and no message has been set yet WHEN the account master is read THEN an input error is flagged, the account search is marked invalid and the message 'Account:00000000011 not found in Acct Master file.Resp:<resp> Reas:<reason>' is shown (OATM-C01-AC-11; OATM-BR-008)
3. GIVEN the account is not on the account master and an error message is already set WHEN the account master is read THEN an input error is flagged and the account search is marked invalid, but the existing message is kept unchanged (OATM-C01-AC-12; OATM-BR-008)

### Requirement 9: OATM-REQ-F-009 (error handling)

#### Acceptance criteria

1. If the account master read fails for any other reason, then the system shall flag an input error, mark the account search invalid and report 'File Error: READ on ACCTDAT returned RESP <resp>...'. (rules OATM-BR-009)
2. GIVEN the account is in the card cross-reference and the account master read fails for a reason other than record not found WHEN the account master is read THEN an input error is flagged, the account search is marked invalid and the message beginning 'File Error: READ on ACCTDAT returned RESP <resp>' is shown with the returned codes (OATM-C01-AC-13; OATM-BR-009)

### Requirement 10: OATM-REQ-F-010 (design note)

#### Acceptance criteria

1. When the customer master read for the account's customer succeeds, the system shall mark the customer as found. (rules OATM-BR-010)
2. GIVEN customer id from cross-reference: 000000001; customer master: record exists WHEN the customer master read (CUSTDAT) for the account's customer succeeds THEN Customer marked found (OATM-C01-AC-06; OATM-BR-010)

### Requirement 11: OATM-REQ-F-011 (error handling)

#### Acceptance criteria

1. If the customer is not on the customer master, then the system shall flag an input error, mark the customer search invalid and, if no message is already set, report 'CustId:<id> not found in customer master.Resp: <resp> REAS:<reason>'. (rules OATM-BR-011)
2. GIVEN the account is found but its customer id 000000123 is not on the customer master, and no message has been set yet WHEN the customer master is read THEN an input error is flagged, the customer search is marked invalid and the message 'CustId:000000123 not found in customer master.Resp: <resp> REAS:<reason>' is shown (OATM-C01-AC-14; OATM-BR-011)

### Requirement 12: OATM-REQ-F-012 (error handling)

#### Acceptance criteria

1. If the customer master read fails for any other reason, then the system shall flag an input error, mark the customer search invalid and report 'File Error: READ on CUSTDAT returned RESP <resp>...'. (rules OATM-BR-012)
2. GIVEN the account is found and the customer master read fails for a reason other than record not found WHEN the customer master is read THEN an input error is flagged, the customer search is marked invalid and the message beginning 'File Error: READ on CUSTDAT returned RESP <resp>' is shown with the returned codes (OATM-C01-AC-15; OATM-BR-012)

### Requirement 13: OATM-REQ-F-013 (design note)

#### Acceptance criteria

1. When the account is found in the card cross-reference, the system shall save the account id, customer id, customer names, account status and card number as the session context. (rules OATM-BR-013)
2. GIVEN account id: 00000000001; cross-reference: found WHEN the account is found in the card cross-reference THEN The session context holds the account, customer and card number for later screens (OATM-C01-AC-07; OATM-BR-013)

### Requirement 14: OATM-REQ-F-014 (design note)

#### Acceptance criteria

1. When the account is found in the card cross-reference, the system shall copy the fetched account and customer values into the original snapshot, splitting the open, expiry, reissue and birth dates (YYYY-MM-DD) into year, month and day. (rules OATM-BR-014)
2. GIVEN stored expiry date: 2027-08-31 WHEN the account is found in the card cross-reference THEN Snapshot expiry year 2027, month 08, day 31 (OATM-C01-AC-08; OATM-BR-014)
