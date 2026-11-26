# Receive and prepare card authorization requests (CAFM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk medium

## Introduction

The intake side of real-time card authorization for the card payment network. It takes authorization requests off the queue, splits them into fields, and gathers the card's account, customer and pending-authorization summary so the request can be decided. A missing account or customer must not stop the request, which goes on to be declined. A real read failure must end the task before any reply is sent for that request.

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
2. GIVEN A comma-delimited authorization request message whose amount field holds the text '125.50' WHEN The request message is received THEN Each comma-separated value goes into its own request field, and the transaction amount is the number 125.50, ready for the credit check. (CAFM-C04-AC-15; CAFM-BR-044)

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

## Screens and components

No screens: it runs as online.

## Data models

#### CCPAUERY

File record of COPAUA0C. Source: `app/app-authorization-ims-db2-mq/cpy/CCPAUERY.cpy`.

Record `ERROR-LOG-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ERR-DATE |  | X(06) | text, 6 characters |  |  |  |
| ERR-TIME |  | X(06) | text, 6 characters |  |  |  |
| ERR-APPLICATION |  | X(08) | text, 8 characters |  |  |  |
| ERR-PROGRAM |  | X(08) | text, 8 characters |  |  |  |
| ERR-LOCATION |  | X(04) | text, 4 characters |  |  |  |
| ERR-LEVEL |  | X(01) | text, 1 character |  |  | ERR-LOG = L; ERR-INFO = I; ERR-WARNING = W; ERR-CRITICAL = C |
| ERR-SUBSYSTEM |  | X(01) | text, 1 character |  |  | ERR-APP = A; ERR-CICS = C; ERR-IMS = I; ERR-DB2 = D; ERR-MQ = M; ERR-FILE = F |
| ERR-CODE-1 |  | X(09) | text, 9 characters |  |  |  |
| ERR-CODE-2 |  | X(09) | text, 9 characters |  |  |  |
| ERR-MESSAGE |  | X(50) | text, 50 characters |  |  |  |
| ERR-EVENT-KEY |  | X(20) | text, 20 characters |  |  |  |

#### CCPAURQY

File record of COPAUA0C. Source: `app/app-authorization-ims-db2-mq/cpy/CCPAURQY.cpy`.

Record `PA-RQ-AUTH-DATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-AUTH-DATE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RQ-AUTH-TIME`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-AUTH-TIME |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RQ-CARD-NUM`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |

Record `PA-RQ-AUTH-TYPE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-AUTH-TYPE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-RQ-CARD-EXPIRY-DATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-CARD-EXPIRY-DATE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-RQ-MESSAGE-TYPE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MESSAGE-TYPE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RQ-MESSAGE-SOURCE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MESSAGE-SOURCE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RQ-PROCESSING-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-PROCESSING-CODE |  | 9(06) | unsigned integer, 6 digits (zoned decimal) |  |  |  |

Record `PA-RQ-TRANSACTION-AMT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-TRANSACTION-AMT |  | +9(10).99 | formatted text, 14 characters (a number shown with 12 digits) |  |  |  |

Record `PA-RQ-MERCHANT-CATAGORY-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-CATAGORY-CODE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-RQ-ACQR-COUNTRY-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-ACQR-COUNTRY-CODE |  | X(03) | text, 3 characters |  |  |  |

Record `PA-RQ-POS-ENTRY-MODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-POS-ENTRY-MODE |  | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |

Record `PA-RQ-MERCHANT-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-ID |  | X(15) | text, 15 characters |  |  |  |

Record `PA-RQ-MERCHANT-NAME`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-NAME |  | X(22) | text, 22 characters |  |  |  |

Record `PA-RQ-MERCHANT-CITY`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-CITY |  | X(13) | text, 13 characters |  |  |  |

Record `PA-RQ-MERCHANT-STATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-STATE |  | X(02) | text, 2 characters |  |  |  |

Record `PA-RQ-MERCHANT-ZIP`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-ZIP |  | X(09) | text, 9 characters |  |  |  |

Record `PA-RQ-TRANSACTION-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-TRANSACTION-ID |  | X(15) | text, 15 characters |  |  |  |

#### CVACT01Y

File record of COPAUA0C. Source: `app/cpy/CVACT01Y.cpy`.

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

#### CVACT03Y

File record of COPAUA0C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COPAUA0C. Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

- CCPAURLY (working storage of COPAUA0C): see data-contracts.md.
- CIPAUDTY (working storage of COPAUA0C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUA0C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- CAFM-BR-042: Messages on request queue = 800 → 501 messages are processed, each committed; 299 remain on the queue.
- CAFM-BR-042: Messages on request queue = 20 → All 20 are processed.
- CAFM-BR-043: Queue = empty for 5 seconds after the last message → The processor closes the queue and ends.
- CAFM-BR-045: Cross-reference account id = 00000000011; Account record = exists → The account is marked found and its credit limit and balance are available to the decision.
- CAFM-BR-046: Account record = not found; Pending summary = not found → Warning 'A002' 'ACCT NOT FOUND IN XREF' is logged and the request is declined with reason '3100'.
- CAFM-BR-047: Account file read result = file disabled → Critical error 'C002' 'FAILED TO READ ACCT FILE' is logged and the task ends with no reply for this request.
- CAFM-BR-048: Card cross-reference customer id = 000000050; Customer record = exists → The customer is marked found and processing continues.
- CAFM-BR-049: Customer record = not found → Warning 'A003' 'CUST NOT FOUND IN XREF' is logged; if the request is declined its reason is '3100'.
- CAFM-BR-050: Customer file read result = file not open → Critical error 'C003' 'FAILED TO READ CUST FILE' is logged and the task ends with no reply for this request.
- CAFM-BR-051: IMS status = ' ' → The summary is found and its credit limit and balance are used for the decision.
- CAFM-BR-051: IMS status = 'GE' → The summary is not found; the decision uses the account master and a new summary is inserted later.
- CAFM-BR-052: IMS status = 'AI' → Critical error 'I002' 'IMS GET SUMMARY FAILED' is logged and the task ends.
- CAFM-BR-053: Current date (YYDDD) = 25330; Current time = 143015; Milliseconds = 250 → Key date = 99999 - 25330 = 74669; key time = 999999999 - 143015250 = 856984749.
- CAFM-BR-053: Current date (YYDDD) = 25001; Current time = 000000; Milliseconds = 0 → Key date = 74998; key time = 999999999, so newer authorizations sort first.

## Decision tables

#### Master record lookup outcome

| Master file read | Read result | Lookup handling | Rule |
|---|---|---|---|
| Account master (ACCTDAT) | Found | Mark account found | CAFM-BR-045 |
| Account master (ACCTDAT) | Not found | Mark not found, log warning 'A002', continue | CAFM-BR-046 |
| Account master (ACCTDAT) | Other failure | Log critical error 'C002', end task with no reply | CAFM-BR-047 |
| Customer master (CUSTDAT) | Found | Mark customer found | CAFM-BR-048 |
| Customer master (CUSTDAT) | Not found | Mark not found, log warning 'A003', continue | CAFM-BR-049 |
| Customer master (CUSTDAT) | Other failure | Log critical error 'C003', end task with no reply | CAFM-BR-050 |


## Design notes

- CAFM-BR-042: Consume authorization requests from the request queue one at a time, committing after each. Stop after 501 messages in one activation (the limit is 500, checked as 'more than') and leave the rest for the next activation. Make the limit a configuration value.
- CAFM-BR-043: Wait up to 5 seconds for each next request, and end the consumer cleanly when none arrives.
- CAFM-BR-044: Read the request as comma-separated text in this field order: auth date, auth time, card number, auth type, card expiry, message type, message source, processing code, amount, merchant category code, acquirer country code, POS entry mode, merchant id, merchant name, merchant city, merchant state, merchant zip, transaction id. Convert the amount text to a decimal number.
- CAFM-BR-045: Once the card is found, look up the account by the account id from the card cross-reference (a keyed lookup by account id) and record whether it was found.
- CAFM-BR-048: Once the card is found, look up the customer by the customer id from the card cross-reference (a keyed lookup by customer id) and record whether it was found.
- CAFM-BR-051: Look up the pending-authorization summary by the card's account id. Keep three outcomes apart: found, not found (a valid state, after which a new summary is created) and read failure (critical error 'I002').
- CAFM-BR-053: Authorization details must list newest first under their account. The legacy key does this with an inverted date (99999 minus YYDDD) and an inverted time (999999999 minus time×1000+milliseconds). A modern store can order by a full timestamp descending instead, but the purge's age calculation and the paging keys must use the same date.

## Open questions

- SME-131: The authorization reply expiry is given as 50 with no unit. What unit and timeout should the new messaging platform use? (Integration team) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- SME-132: In the pending authorization summary, an approval sets the cash balance to zero instead of adding to it, and the declined-amount total may not use the current request's amount. Is each of these intended, or is it a defect? (Card authorization product owner) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- SME-133: Decline reasons 4200 (card not active), 4300 (account closed), 5100 (card fraud) and 5200 (merchant fraud) are defined, but nothing triggers them. Should these checks be implemented, and what data should drive them? (Card authorization product owner / fraud management team) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- SME-134: The authorization summary is saved before the authorization detail is recorded, so if recording the detail fails, the totals already include it. Must the summary update and the detail record succeed or fail together? (Card authorization business owner) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- SME-135: When a lookup during authorization logs a critical error (C001, C002, C003, I002), should the decision, reply and recording still go ahead for that request? (Card authorization business owner) On CAFM-BR-044, CAFM-BR-053, CAFM-BR-050, CAFM-BR-052, CAFM-BR-047.
- DEF-138: Is this intended? The summary found/not-found flag is never reset per message, so when a later request's card is not in the cross-reference (lookup skipped) the decision reuses the previous request's summary credit limit and balance and can approve an unknown card. (Subject-matter expert) On CAFM-BR-052.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).
