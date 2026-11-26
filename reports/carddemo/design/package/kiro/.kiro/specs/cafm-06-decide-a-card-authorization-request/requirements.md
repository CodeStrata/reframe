# Requirements: Decide a card authorization request (CAFM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

The rules that decide each card authorization for the card issuer: look up the card, then its account, customer and pending summary, and approve or decline with a clear reason code. Only known cards may be approved. A card, account or customer that is not found always declines with reason '3100', which takes precedence over insufficient funds ('4100'). Every request gets a reply, even when the card is unknown.

**User story:** As a card issuer, I want each incoming card authorization request approved or declined against the card, account and customer records, so that only transactions for known cards are approved and every request gets a reply with a clear reason.

## Requirements

### Requirement 1: CAFM-REQ-F-061 (business rule)

#### Acceptance criteria

1. When an authorization request is processed, the system shall start from an approve decision and look up the card in the card cross-reference, and only when the card is found shall it read the account, the customer and the account's pending-authorization summary before deciding. (rules CAFM-BR-061)
2. GIVEN card number: 4000000000000002 (in cross-reference) WHEN an authorization request is processed THEN Account, customer and summary are read, then the decision is made (CAFM-C06-AC-01; CAFM-BR-061)
3. GIVEN card number: 4000000000000099 (not in cross-reference) WHEN an authorization request is processed THEN No account, customer or summary is read; the decision is made directly (CAFM-C06-AC-02; CAFM-BR-061)

### Requirement 2: CAFM-REQ-F-062 (business rule)

#### Acceptance criteria

1. When the request is declined, the system shall reply with response code '05' and approved amount 0, and otherwise shall reply '00' with the full requested amount approved. (rules CAFM-BR-062)
2. GIVEN decision: declined; amount: 250.00 WHEN the request is declined THEN Response '05', approved amount 0.00 (CAFM-C06-AC-03; CAFM-BR-062)
3. GIVEN decision: approved; amount: 75.00 WHEN the request is declined THEN Response '00', approved amount 75.00 (CAFM-C06-AC-04; CAFM-BR-062)

### Requirement 3: CAFM-REQ-F-063 (business rule)

#### Acceptance criteria

1. When the card is not in the card cross-reference, the system shall treat the card and its account as not found and decline the request with response '05', reason '3100' and approved amount 0. (rules CAFM-BR-063)
2. GIVEN card number: 4000000000000099 (not in cross-reference); amount: 50.00 WHEN the card is not in the card cross-reference THEN Reply has response '05', reason '3100', approved amount 0.00 (CAFM-C06-AC-05; CAFM-BR-063)

### Requirement 4: CAFM-REQ-F-064 (business rule)

#### Acceptance criteria

1. When the card is not in the card cross-reference, the system shall still decide and send a reply but shall not update the pending-authorization summary or record an authorization detail. (rules CAFM-BR-064)
2. GIVEN card number: 4000000000000099 (not in cross-reference) WHEN the card is not in the card cross-reference THEN A reply is sent; nothing is written to the pending-authorization database (CAFM-C06-AC-06; CAFM-BR-064)

### Requirement 5: CAFM-REQ-F-065 (side effect)

#### Acceptance criteria

1. When the card is not in the card cross-reference, the system shall log a warning at location 'A001' with message 'CARD NOT FOUND IN XREF' and the card number as the key. (rules CAFM-BR-065)
2. GIVEN card number: 4000000000000099 (not in cross-reference) WHEN the card is not in the card cross-reference THEN Warning 'A001' 'CARD NOT FOUND IN XREF' logged with key 4000000000000099 (CAFM-C06-AC-07; CAFM-BR-065)

### Requirement 6: CAFM-REQ-F-066 (error handling)

#### Acceptance criteria

1. If reading the card cross-reference fails for any reason other than not found, then the system shall log a critical error at location 'C001' with message 'FAILED TO READ XREF FILE' and the response codes, and carry on processing the request as if the card had been found. (rules CAFM-BR-066)
2. GIVEN cross-reference file: unavailable WHEN reading the card cross-reference fails for any reason other than not found THEN Critical error 'C001' 'FAILED TO READ XREF FILE' logged; account, customer and summary reads are still attempted and the authorization is recorded (CAFM-C06-AC-08; CAFM-BR-066)

### Requirement 7: CAFM-REQ-F-067 (business rule)

#### Acceptance criteria

1. When an authorization is approved, the system shall reply with reason code '0000'. (rules CAFM-BR-067)
2. GIVEN decision: approved WHEN an authorization is approved THEN Reason '0000' (CAFM-C06-AC-09; CAFM-BR-067)

### Requirement 8: CAFM-REQ-F-068 (business rule)

#### Acceptance criteria

1. When an authorization is declined and the card, the account or the customer was not found, the system shall reply with reason code '3100', taking precedence over every other reason. (rules CAFM-BR-068)
2. GIVEN card in cross-reference: no; decision: declined WHEN an authorization is declined and the card THEN Reason '3100' (CAFM-C06-AC-10; CAFM-BR-068)
3. GIVEN customer record: not found; decision: declined for insufficient funds WHEN an authorization is declined and the card THEN Reason '3100', not '4100' (CAFM-C06-AC-11; CAFM-BR-068)

### Requirement 9: CAFM-REQ-F-069 (business rule)

#### Acceptance criteria

1. When an authorization is declined for insufficient funds and the card, account and customer were all found, the system shall reply with reason code '4100'. (rules CAFM-BR-069)
2. GIVEN available credit: 200.00; amount: 250.00 WHEN an authorization is declined for insufficient funds and the card, account and customer were all found THEN Response '05', reason '4100' (CAFM-C06-AC-12; CAFM-BR-069)

### Requirement 10: CAFM-REQ-F-070 (historical artifact)

#### Acceptance criteria

1. Where a decline is for card not active, account closed, card fraud, merchant fraud or any other cause, the system shall assign reason '4200', '4300', '5100', '5200' or '9000' respectively, although nothing sets these conditions today so these codes are not produced. (rules CAFM-BR-070)
2. GIVEN card status: inactive WHEN reason assignment runs THEN No '4200' decline is produced; the card is decided on credit only (CAFM-C06-AC-13; CAFM-BR-070)
