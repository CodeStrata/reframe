# Feature specification: Receive and prepare card authorization requests

**Feature:** CAFM-C04 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C04)

As a card payment network, I want authorization request messages taken from the queue, parsed and matched to the card's account, customer and pending authorization summary, so that each request can be decided and answered.

The intake step for card authorization requests from the payment network. It takes each request message, parses it, and looks up the card's account, customer and pending authorization summary so a decision can be made. It must never send a reply based on a failed read of the account, customer or summary data, and it must convert the amount text exactly into the transaction amount.

**Acceptance scenarios:**

1. **Given** Messages on request queue: 800, **when** triggered, **then** 501 messages are processed, each committed; 299 remain on the queue. (CAFM-C04-AC-01)
2. **Given** Messages on request queue: 20, **when** triggered, **then** All 20 are processed. (CAFM-C04-AC-02)
3. **Given** Queue: empty for 5 seconds after the last message, **when** no request message arrives within 5 seconds of a read, **then** The processor closes the queue and ends. (CAFM-C04-AC-03)
4. **Given** Cross-reference account id: 00000000011; Account record: exists, **when** a card is found in the cross-reference, **then** The account is marked found and its credit limit and balance are available to the decision. (CAFM-C04-AC-04)
5. **Given** Account record: not found; Pending summary: not found, **when** the account is not in the account master, **then** Warning 'A002' 'ACCT NOT FOUND IN XREF' is logged and the request is declined with reason '3100'. (CAFM-C04-AC-05)
6. **Given** Account file read result: file disabled, **when** reading the account master fails for any other reason, **then** Critical error 'C002' 'FAILED TO READ ACCT FILE' is logged and the task ends with no reply for this request. (CAFM-C04-AC-06)
7. **Given** Card cross-reference customer id: 000000050; Customer record: exists, **when** a card is found in the cross-reference, **then** The customer is marked found and processing continues. (CAFM-C04-AC-07)
8. **Given** Customer record: not found, **when** the customer is not in the customer master, **then** Warning 'A003' 'CUST NOT FOUND IN XREF' is logged; if the request is declined its reason is '3100'. (CAFM-C04-AC-08)
9. **Given** Customer file read result: file not open, **when** reading the customer master fails for any other reason, **then** Critical error 'C003' 'FAILED TO READ CUST FILE' is logged and the task ends with no reply for this request. (CAFM-C04-AC-09)
10. **Given** IMS status: ' ', **when** a card is found in the cross-reference, **then** The summary is found and its credit limit and balance are used for the decision. (CAFM-C04-AC-10)
11. **Given** IMS status: 'GE', **when** a card is found in the cross-reference, **then** The summary is not found; the decision uses the account master and a new summary is inserted later. (CAFM-C04-AC-11)
12. **Given** IMS status: 'AI', **when** reading the pending authorization summary returns any other IMS status, **then** Critical error 'I002' 'IMS GET SUMMARY FAILED' is logged and the task ends. (CAFM-C04-AC-12)
13. **Given** Current date (YYDDD): 25330; Current time: 143015; Milliseconds: 250, **when** an authorization detail is about to be recorded, **then** Key date = 99999 - 25330 = 74669; key time = 999999999 - 143015250 = 856984749. (CAFM-C04-AC-13)
14. **Given** Current date (YYDDD): 25001; Current time: 000000; Milliseconds: 0, **when** an authorization detail is about to be recorded, **then** Key date = 74998; key time = 999999999, so newer authorizations sort first. (CAFM-C04-AC-14)
15. **Given** A comma-delimited authorization request message whose amount field holds the text '125.50', **when** The request is received and parsed, **then** Each comma-separated value is assigned to its request field in order, and the transaction amount holds the numeric value 125.50 (CAFM-C04-AC-15)

## Requirements

### Functional requirements

- **CAFM-REQ-F-040** (design note): When triggered, the system shall process request messages one at a time, committing after each, and shall stop after 501 messages (the limit 500 is checked as 'more than'), leaving the rest on the queue for a later trigger. Rules: CAFM-BR-042.
- **CAFM-REQ-F-041** (design note): When no request message arrives within 5 seconds of a read, the system shall stop processing and end the task. Rules: CAFM-BR-043.
- **CAFM-REQ-F-042** (design note): When a request message is received, the system shall split the comma-delimited request into its fields and convert the amount text into the numeric transaction amount. Rules: CAFM-BR-044.
- **CAFM-REQ-F-043** (design note): When a card is found in the cross-reference, the system shall read the account master (ACCTDAT) using the account id from the cross-reference and mark the account found when it exists. Rules: CAFM-BR-045.
- **CAFM-REQ-F-044** (error handling): When the account is not in the account master, the system shall mark it not found, log warning 'A002' with message 'ACCT NOT FOUND IN XREF' and continue processing the request. Rules: CAFM-BR-046.
- **CAFM-REQ-F-045** (error handling): If reading the account master fails for any other reason, then the system shall log critical error 'C002' with message 'FAILED TO READ ACCT FILE', ending the task before a reply is sent for that request. Rules: CAFM-BR-047.
- **CAFM-REQ-F-046** (design note): When a card is found in the cross-reference, the system shall read the customer master (CUSTDAT) using the customer id from the cross-reference and mark the customer found when it exists. Rules: CAFM-BR-048.
- **CAFM-REQ-F-047** (error handling): When the customer is not in the customer master, the system shall mark it not found, log warning 'A003' with message 'CUST NOT FOUND IN XREF' and continue processing the request. Rules: CAFM-BR-049.
- **CAFM-REQ-F-048** (error handling): If reading the customer master fails for any other reason, then the system shall log critical error 'C003' with message 'FAILED TO READ CUST FILE', ending the task before a reply is sent for that request. Rules: CAFM-BR-050.
- **CAFM-REQ-F-049** (design note): When a card is found in the cross-reference, the system shall read the pending authorization summary for the card's account and treat IMS status blank or 'FW' as found and 'GE' as not found. Rules: CAFM-BR-051.
- **CAFM-REQ-F-050** (error handling): If reading the pending authorization summary returns any other IMS status, then the system shall log critical error 'I002' with message 'IMS GET SUMMARY FAILED', ending the task before a reply is sent for that request. Rules: CAFM-BR-052.
- **CAFM-REQ-F-051** (design note): When an authorization detail is about to be recorded, the system shall set the key date to 99999 minus the year/day value and the key time to 999999999 minus (time x 1000 + milliseconds). Rules: CAFM-BR-053.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-042 | Per-trigger processing limit and queue wait | design note | WHEN triggered, THE authorization processor SHALL process request messages one at a time, committing after each, and SHALL stop after 501 messages (the limit 500 is checked as 'more than'), leaving the rest on the queue for a later trigger. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:40-42, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:242-246, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:323-345, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:389-417 |
| CAFM-BR-043 | Per-trigger processing limit and queue wait | design note | WHEN no request message arrives within 5 seconds of a read, THE authorization processor SHALL stop processing and end the task. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:40-42, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:242-246, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:323-345, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:389-417 |
| CAFM-BR-044 | Parse comma-delimited authorization request | design note | WHEN a request message is received, THE Authorization Request Parsing SHALL split the comma-delimited request into its fields and convert the amount text into the numeric transaction amount | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:351,354-374,376-377,379-380, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:351-380 |
| CAFM-BR-045 | Look up account master record | design note | WHEN a card is found in the cross-reference, THE account lookup SHALL read the account master (ACCTDAT) using the account id from the cross-reference and mark the account found when it exists. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:450-451, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:520-561, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-682, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:1008-1010 |
| CAFM-BR-046 | Look up account master record | error handling | WHEN the account is not in the account master, THE account lookup SHALL mark it not found and log warning 'A002' with message 'ACCT NOT FOUND IN XREF', and processing of the request SHALL continue. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:450-451, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:520-561, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-682, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:1008-1010 |
| CAFM-BR-047 | Look up account master record | error handling | WHEN reading the account master fails for any other reason, THE account lookup SHALL log critical error 'C002' with message 'FAILED TO READ ACCT FILE', which ends the task before a reply is sent for that request. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:450-451, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:520-561, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-682, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:1008-1010 |
| CAFM-BR-048 | Look up customer master record | design note | WHEN a card is found in the cross-reference, THE customer lookup SHALL read the customer master (CUSTDAT) using the customer id from the cross-reference and mark the customer found when it exists. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:450-452, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:568-609, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-704, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:1008-1010 |
| CAFM-BR-049 | Look up customer master record | error handling | WHEN the customer is not in the customer master, THE customer lookup SHALL mark it not found and log warning 'A003' with message 'CUST NOT FOUND IN XREF', and processing of the request SHALL continue. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:450-452, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:568-609, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-704, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:1008-1010 |
| CAFM-BR-050 | Look up customer master record | error handling | WHEN reading the customer master fails for any other reason, THE customer lookup SHALL log critical error 'C003' with message 'FAILED TO READ CUST FILE', which ends the task before a reply is sent for that request. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:450-452, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:568-609, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-704, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:1008-1010 |
| CAFM-BR-051 | Retrieve pending authorization summary | design note | WHEN a card is found in the cross-reference, THE pending authorization summary lookup SHALL read the summary for the card's account and treat IMS status blank or 'FW' as found and 'GE' as not found. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:86-87, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:616-640, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:1008-1010 |
| CAFM-BR-052 | Retrieve pending authorization summary | error handling | WHEN reading the pending authorization summary returns any other IMS status, THE summary lookup SHALL log critical error 'I002' with message 'IMS GET SUMMARY FAILED', which ends the task before a reply is sent for that request. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:86-87, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:616-640, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:1008-1010 |
| CAFM-BR-053 | Compute inverted authorization timestamp key | design note | WHEN an authorization detail is about to be recorded, THE Authorization Detail Keying SHALL set the key date to 99999 minus the year/day value and the key time to 999999999 minus (time x 1000 + milliseconds) | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854,857-859,861-866,868-869,871-872,874-875, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:857-875 |

### Key entities

- CCPAUERY (file record)
- CCPAURQY (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CCPAURLY (working storage)
- CIPAUDTY (working storage)
- CIPAUSMY (working storage)

### Needs clarification

- SME-131: The authorization reply expiry is given as 50 with no unit. What unit and timeout should the new messaging platform use? (Integration team) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- SME-132: In the pending authorization summary, an approval sets the cash balance to zero instead of adding to it, and the declined-amount total may not use the current request's amount. Is each of these intended, or is it a defect? (Card authorization product owner) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- SME-133: Decline reasons 4200 (card not active), 4300 (account closed), 5100 (card fraud) and 5200 (merchant fraud) are defined, but nothing triggers them. Should these checks be implemented, and what data should drive them? (Card authorization product owner / fraud management team) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- SME-134: The authorization summary is saved before the authorization detail is recorded, so if recording the detail fails, the totals already include it. Must the summary update and the detail record succeed or fail together? (Card authorization business owner) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- SME-135: When a lookup during authorization logs a critical error (C001, C002, C003, I002), should the decision, reply and recording still go ahead for that request? (Card authorization business owner) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- DEF-138: Is this intended? The summary found/not-found flag is never reset per message, so when a later request's card is not in the cross-reference (lookup skipped) the decision reuses the previous request's summary credit limit and balance and can approve an unknown card. (Subject-matter expert) On CAFM-BR-052.

### Decision table gaps

None.
