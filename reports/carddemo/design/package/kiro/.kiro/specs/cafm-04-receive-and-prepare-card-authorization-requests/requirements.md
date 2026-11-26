# Requirements: Receive and prepare card authorization requests (CAFM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk medium

## Introduction

The intake step for card authorization requests from the payment network. It takes each request message, parses it, and looks up the card's account, customer and pending authorization summary so a decision can be made. It must never send a reply based on a failed read of the account, customer or summary data, and it must convert the amount text exactly into the transaction amount.

**User story:** As a card payment network, I want authorization request messages taken from the queue, parsed and matched to the card's account, customer and pending authorization summary, so that each request can be decided and answered.

## Requirements

### Requirement 1: CAFM-REQ-F-040 (design note)

#### Acceptance criteria

1. When triggered, the system shall process request messages one at a time, committing after each, and shall stop after 501 messages (the limit 500 is checked as 'more than'), leaving the rest on the queue for a later trigger. (rules CAFM-BR-042)
2. GIVEN Messages on request queue: 800 WHEN triggered THEN 501 messages are processed, each committed; 299 remain on the queue. (CAFM-C04-AC-01; CAFM-BR-042)
3. GIVEN Messages on request queue: 20 WHEN triggered THEN All 20 are processed. (CAFM-C04-AC-02; CAFM-BR-042)

### Requirement 2: CAFM-REQ-F-041 (design note)

#### Acceptance criteria

1. When no request message arrives within 5 seconds of a read, the system shall stop processing and end the task. (rules CAFM-BR-043)
2. GIVEN Queue: empty for 5 seconds after the last message WHEN no request message arrives within 5 seconds of a read THEN The processor closes the queue and ends. (CAFM-C04-AC-03; CAFM-BR-043)

### Requirement 3: CAFM-REQ-F-042 (design note)

#### Acceptance criteria

1. When a request message is received, the system shall split the comma-delimited request into its fields and convert the amount text into the numeric transaction amount. (rules CAFM-BR-044)
2. GIVEN A comma-delimited authorization request message whose amount field holds the text '125.50' WHEN The request is received and parsed THEN Each comma-separated value is assigned to its request field in order, and the transaction amount holds the numeric value 125.50 (CAFM-C04-AC-15; CAFM-BR-044)

### Requirement 4: CAFM-REQ-F-043 (design note)

#### Acceptance criteria

1. When a card is found in the cross-reference, the system shall read the account master (ACCTDAT) using the account id from the cross-reference and mark the account found when it exists. (rules CAFM-BR-045)
2. GIVEN Cross-reference account id: 00000000011; Account record: exists WHEN a card is found in the cross-reference THEN The account is marked found and its credit limit and balance are available to the decision. (CAFM-C04-AC-04; CAFM-BR-045)

### Requirement 5: CAFM-REQ-F-044 (error handling)

#### Acceptance criteria

1. When the account is not in the account master, the system shall mark it not found, log warning 'A002' with message 'ACCT NOT FOUND IN XREF' and continue processing the request. (rules CAFM-BR-046)
2. GIVEN Account record: not found; Pending summary: not found WHEN the account is not in the account master THEN Warning 'A002' 'ACCT NOT FOUND IN XREF' is logged and the request is declined with reason '3100'. (CAFM-C04-AC-05; CAFM-BR-046)

### Requirement 6: CAFM-REQ-F-045 (error handling)

#### Acceptance criteria

1. If reading the account master fails for any other reason, then the system shall log critical error 'C002' with message 'FAILED TO READ ACCT FILE', ending the task before a reply is sent for that request. (rules CAFM-BR-047)
2. GIVEN Account file read result: file disabled WHEN reading the account master fails for any other reason THEN Critical error 'C002' 'FAILED TO READ ACCT FILE' is logged and the task ends with no reply for this request. (CAFM-C04-AC-06; CAFM-BR-047)

### Requirement 7: CAFM-REQ-F-046 (design note)

#### Acceptance criteria

1. When a card is found in the cross-reference, the system shall read the customer master (CUSTDAT) using the customer id from the cross-reference and mark the customer found when it exists. (rules CAFM-BR-048)
2. GIVEN Card cross-reference customer id: 000000050; Customer record: exists WHEN a card is found in the cross-reference THEN The customer is marked found and processing continues. (CAFM-C04-AC-07; CAFM-BR-048)

### Requirement 8: CAFM-REQ-F-047 (error handling)

#### Acceptance criteria

1. When the customer is not in the customer master, the system shall mark it not found, log warning 'A003' with message 'CUST NOT FOUND IN XREF' and continue processing the request. (rules CAFM-BR-049)
2. GIVEN Customer record: not found WHEN the customer is not in the customer master THEN Warning 'A003' 'CUST NOT FOUND IN XREF' is logged; if the request is declined its reason is '3100'. (CAFM-C04-AC-08; CAFM-BR-049)

### Requirement 9: CAFM-REQ-F-048 (error handling)

#### Acceptance criteria

1. If reading the customer master fails for any other reason, then the system shall log critical error 'C003' with message 'FAILED TO READ CUST FILE', ending the task before a reply is sent for that request. (rules CAFM-BR-050)
2. GIVEN Customer file read result: file not open WHEN reading the customer master fails for any other reason THEN Critical error 'C003' 'FAILED TO READ CUST FILE' is logged and the task ends with no reply for this request. (CAFM-C04-AC-09; CAFM-BR-050)

### Requirement 10: CAFM-REQ-F-049 (design note)

#### Acceptance criteria

1. When a card is found in the cross-reference, the system shall read the pending authorization summary for the card's account and treat IMS status blank or 'FW' as found and 'GE' as not found. (rules CAFM-BR-051)
2. GIVEN IMS status: ' ' WHEN a card is found in the cross-reference THEN The summary is found and its credit limit and balance are used for the decision. (CAFM-C04-AC-10; CAFM-BR-051)
3. GIVEN IMS status: 'GE' WHEN a card is found in the cross-reference THEN The summary is not found; the decision uses the account master and a new summary is inserted later. (CAFM-C04-AC-11; CAFM-BR-051)

### Requirement 11: CAFM-REQ-F-050 (error handling)

#### Acceptance criteria

1. If reading the pending authorization summary returns any other IMS status, then the system shall log critical error 'I002' with message 'IMS GET SUMMARY FAILED', ending the task before a reply is sent for that request. (rules CAFM-BR-052)
2. GIVEN IMS status: 'AI' WHEN reading the pending authorization summary returns any other IMS status THEN Critical error 'I002' 'IMS GET SUMMARY FAILED' is logged and the task ends. (CAFM-C04-AC-12; CAFM-BR-052)

### Requirement 12: CAFM-REQ-F-051 (design note)

#### Acceptance criteria

1. When an authorization detail is about to be recorded, the system shall set the key date to 99999 minus the year/day value and the key time to 999999999 minus (time x 1000 + milliseconds). (rules CAFM-BR-053)
2. GIVEN Current date (YYDDD): 25330; Current time: 143015; Milliseconds: 250 WHEN an authorization detail is about to be recorded THEN Key date = 99999 - 25330 = 74669; key time = 999999999 - 143015250 = 856984749. (CAFM-C04-AC-13; CAFM-BR-053)
3. GIVEN Current date (YYDDD): 25001; Current time: 000000; Milliseconds: 0 WHEN an authorization detail is about to be recorded THEN Key date = 74998; key time = 999999999, so newer authorizations sort first. (CAFM-C04-AC-14; CAFM-BR-053)
