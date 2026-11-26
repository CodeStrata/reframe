# Decide and reply to card authorization requests (CAFM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

The decision and reply step for card authorizations. It approves or declines each request against available credit (credit limit minus balance, taken from the pending summary when there is one, or else from the account) and sends the reply to the payment network in real time. It must never approve an amount strictly greater than the available credit, and a decline always carries response '05' with approved amount 0.

**User story:** As a card payment network, I want each authorization request approved or declined against the account's available credit and answered on my reply queue, so that the merchant transaction can proceed or be refused in real time.

## Requirements

### Requirement 1: CAFM-REQ-F-052 (business rule)

#### Acceptance criteria

1. When the account has a pending-authorization summary, the system shall compute available credit as the summary credit limit minus the summary credit balance and shall decline for insufficient funds when the requested amount is strictly greater than that available credit. (rules CAFM-BR-054)
2. GIVEN summary credit limit: 5000.00; summary credit balance: 4800.00; amount: 250.00 WHEN the account has a pending-authorization summary THEN Declined: response '05', reason '4100' (insufficient funds) (CAFM-C05-AC-01; CAFM-BR-054)
3. GIVEN summary credit limit: 5000.00; summary credit balance: 4800.00; amount: 200.00 WHEN the account has a pending-authorization summary THEN Approved: response '00', approved amount 200.00 (CAFM-C05-AC-02; CAFM-BR-054)

### Requirement 2: CAFM-REQ-F-053 (business rule)

#### Acceptance criteria

1. When the account has no pending-authorization summary but the account record was found, the system shall compute available credit as the account credit limit minus the account current balance and shall decline for insufficient funds when the amount is strictly greater. (rules CAFM-BR-055)
2. GIVEN summary: none; account credit limit: 3000.00; account current balance: 2900.00; amount: 150.00 WHEN the account has no pending-authorization summary but the account record was found THEN Declined: response '05', reason '4100' (CAFM-C05-AC-03; CAFM-BR-055)

### Requirement 3: CAFM-REQ-F-054 (business rule)

#### Acceptance criteria

1. When neither a pending-authorization summary nor the account record is found, the system shall decline the request without an insufficient-funds reason, the reply then carrying reason '3100' because the account is not found. (rules CAFM-BR-056)
2. GIVEN summary: none; account record: not found; amount: 10.00 WHEN neither a pending-authorization summary nor the account record is found THEN Declined: response '05', reason '3100', approved amount 0.00 (CAFM-C05-AC-04; CAFM-BR-056)

### Requirement 4: CAFM-REQ-F-055 (business rule)

#### Acceptance criteria

1. When the authorization decision is decline ('D'), the system shall set response code '05' with approved amount 0, and default the reason to '0000'. (rules CAFM-BR-057)
2. GIVEN Credit limit: 1000.00; Balance: 900.00; Transaction amount: 200.00 WHEN the authorization decision is decline ('D') or approve THEN Declined: response code '05', approved amount 0 (reason then set to '4100'). (CAFM-C05-AC-05; CAFM-BR-057)
3. GIVEN Credit limit: 1000.00; Balance: 100.00; Transaction amount: 200.00 WHEN the authorization decision is decline ('D') or approve THEN Approved: response code '00', approved amount 200.00, reason '0000'. (CAFM-C05-AC-06; CAFM-BR-057)

### Requirement 5: CAFM-REQ-F-056 (business rule)

#### Acceptance criteria

1. When the authorization decision is approve, the system shall set response code '00' with the full transaction amount as the approved amount, and default the reason to '0000'. (rules CAFM-BR-057)
2. GIVEN Credit limit: 1000.00; Balance: 900.00; Transaction amount: 200.00 WHEN the authorization decision is decline ('D') or approve THEN Declined: response code '05', approved amount 0 (reason then set to '4100'). (CAFM-C05-AC-05; CAFM-BR-057)
3. GIVEN Credit limit: 1000.00; Balance: 100.00; Transaction amount: 200.00 WHEN the authorization decision is decline ('D') or approve THEN Approved: response code '00', approved amount 200.00, reason '0000'. (CAFM-C05-AC-06; CAFM-BR-057)

### Requirement 6: CAFM-REQ-F-057 (business rule)

#### Acceptance criteria

1. The system shall carry the request's card number and transaction id in the authorization reply and shall use the request's authorization time as the authorization id code. (rules CAFM-BR-058)
2. GIVEN Card number: 4111111111111111; Transaction id: TX0001; Request auth time: 143015 WHEN authorization reply runs THEN The reply carries card 4111111111111111, transaction TX0001 and authorization id 143015. (CAFM-C05-AC-07; CAFM-BR-058)

### Requirement 7: CAFM-REQ-F-058 (formatting)

#### Acceptance criteria

1. The system shall format the authorization reply as comma-delimited text of card number, transaction id, authorization id, response code, reason code and approved amount (signed, two decimals), each followed by a comma. (rules CAFM-BR-059)
2. GIVEN An authorization decided for card number 4111111111111111, transaction id TXN0001 and authorization id 143005, with response code '00', reason code '0000' and approved amount 125.50 WHEN The authorization reply is formatted THEN The reply text is the card number, transaction id, authorization id, response code '00', reason code '0000' and the approved amount 125.50 written signed with two decimals, in that order, each followed by a comma (the message ends with a comma) (CAFM-C05-AC-09; CAFM-BR-059)

### Requirement 8: CAFM-REQ-F-059 (design note)

#### Acceptance criteria

1. When an authorization decision has been made, the system shall send the non-persistent reply with expiry 50 and the original correlation id through MQPUT1 to the requester's reply queue. (rules CAFM-BR-060)
2. GIVEN MQPUT1 completion code: not MQCC-OK WHEN an authorization decision has been made THEN Critical error logged at location 'M004' with message 'FAILED TO PUT ON REPLY MQ' to queue 'CSSL'; the program ends. (CAFM-C05-AC-08; CAFM-BR-060)

### Requirement 9: CAFM-REQ-F-060 (design note)

#### Acceptance criteria

1. If putting the authorization reply fails, then the system shall log critical error 'M004'. (rules CAFM-BR-060)
2. GIVEN MQPUT1 completion code: not MQCC-OK WHEN an authorization decision has been made THEN Critical error logged at location 'M004' with message 'FAILED TO PUT ON REPLY MQ' to queue 'CSSL'; the program ends. (CAFM-C05-AC-08; CAFM-BR-060)

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
| CAFM-BR-054 | Check available credit for authorization | business rule | WHEN the account has a pending-authorization summary, THE authorization decision SHALL compute available credit as the summary credit limit minus the summary credit balance, and SHALL decline for insufficient funds when the requested amount is strictly greater than that available credit. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:664-696, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-706 |
| CAFM-BR-055 | Check available credit for authorization | business rule | WHEN the account has no pending-authorization summary but the account record was found, THE authorization decision SHALL compute available credit as the account credit limit minus the account current balance, and SHALL decline for insufficient funds when the amount is strictly greater. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:664-696, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-706 |
| CAFM-BR-056 | Check available credit for authorization | business rule | WHEN neither a pending-authorization summary nor the account record is found, THE authorization decision SHALL decline the request without an insufficient-funds reason (the reply then carries reason '3100' because the account is not found). | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:664-696, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-706 |
| CAFM-BR-057 | Set approve or decline response | business rule | WHEN the authorization decision is decline ('D') or approve, THE Authorization Credit Decision SHALL set response code '05' with approved amount 0 for a decline, or '00' with the full transaction amount for an approval, and default the reason to '0000' | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:685-686,688-696,698, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:685-696 |
| CAFM-BR-058 | Assemble comma-delimited reply content | business rule | THE authorization reply SHALL carry the request's card number and transaction id, and SHALL use the request's authorization time as the authorization id code. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:657-662, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:720-731, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:66, app/app-authorization-ims-db2-mq/cpy/CCPAURLY.cpy:21 |
| CAFM-BR-059 | Assemble comma-delimited reply content | formatting | THE authorization reply SHALL be comma-delimited text of card number, transaction id, authorization id, response code, reason code and approved amount (signed, two decimals), each followed by a comma. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:657-662, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:720-731, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:66, app/app-authorization-ims-db2-mq/cpy/CCPAURLY.cpy:21 |
| CAFM-BR-060 | Send authorization reply message | design note | WHEN an authorization decision has been made, THE Authorization Reply SHALL send the non-persistent reply with expiry 50 and the original correlation id through MQPUT1 to the requester's reply queue, logging critical error 'M004' if the put fails | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:738,741-742,744-751,753-754,756,758-779, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:738-766 |

### Worked examples

- CAFM-BR-054: summary credit limit = 5000.00; summary credit balance = 4800.00; amount = 250.00 → Declined: response '05', reason '4100' (insufficient funds)
- CAFM-BR-054: summary credit limit = 5000.00; summary credit balance = 4800.00; amount = 200.00 → Approved: response '00', approved amount 200.00
- CAFM-BR-055: summary = none; account credit limit = 3000.00; account current balance = 2900.00; amount = 150.00 → Declined: response '05', reason '4100'
- CAFM-BR-056: summary = none; account record = not found; amount = 10.00 → Declined: response '05', reason '3100', approved amount 0.00
- CAFM-BR-057: Credit limit = 1000.00; Balance = 900.00; Transaction amount = 200.00 → Declined: response code '05', approved amount 0 (reason then set to '4100').
- CAFM-BR-057: Credit limit = 1000.00; Balance = 100.00; Transaction amount = 200.00 → Approved: response code '00', approved amount 200.00, reason '0000'.
- CAFM-BR-058: Card number = 4111111111111111; Transaction id = TX0001; Request auth time = 143015 → The reply carries card 4111111111111111, transaction TX0001 and authorization id 143015.
- CAFM-BR-060: MQPUT1 completion code = not MQCC-OK → Critical error logged at location 'M004' with message 'FAILED TO PUT ON REPLY MQ' to queue 'CSSL'; the program ends.

## Decision tables

#### Available credit check

| Pending-authorization summary found | Account record found | Amount strictly greater than available credit | Credit decision | Rule |
|---|---|---|---|---|
| Yes | Any | Yes | Decline for insufficient funds (available credit = summary credit limit - summary credit balance) | CAFM-BR-054 |
| Yes | Any | No | Not declined for insufficient funds | CAFM-BR-054 |
| No | Yes | Yes | Decline for insufficient funds (available credit = account credit limit - account current balance) | CAFM-BR-055 |
| No | Yes | No | Not declined for insufficient funds | CAFM-BR-055 |
| No | No | Any | Decline without insufficient-funds reason; reply carries reason '3100' | CAFM-BR-056 |
| Yes | No | Any | **Gap:** R58 decides on the summary alone; the rules do not say whether reason '3100' (account not found) also applies when the summary is found but the account record is not. | |


## Design notes

- CAFM-BR-060: Send each reply as a one-off, non-persistent message to the reply address named in the request, with the request's correlation id and a short time-to-live (expiry 50, which is 5 seconds in MQ's tenths of a second). This way stale replies expire instead of piling up. If the send fails, log critical error 'M004'.

## Open questions

- SME-131: The authorization reply expiry is given as 50 with no unit. What unit and timeout should the new messaging platform use? (Integration team) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- SME-132: In the pending authorization summary, an approval sets the cash balance to zero instead of adding to it, and the declined-amount total may not use the current request's amount. Is each of these intended, or is it a defect? (Card authorization product owner) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- SME-133: Decline reasons 4200 (card not active), 4300 (account closed), 5100 (card fraud) and 5200 (merchant fraud) are defined, but nothing triggers them. Should these checks be implemented, and what data should drive them? (Card authorization product owner / fraud management team) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- SME-134: The authorization summary is saved before the authorization detail is recorded, so if recording the detail fails, the totals already include it. Must the summary update and the detail record succeed or fail together? (Card authorization business owner) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- SME-135: When a lookup during authorization logs a critical error (C001, C002, C003, I002), should the decision, reply and recording still go ahead for that request? (Card authorization business owner) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- DEF-001: Is this intended? The summary-found flag and the decline-reason flag are never reset between messages. When the summary read fails with an IMS error (I002), or the card is unknown, the check uses the summary flag and the limit and balance left over from the previous request in the same run. (Subject-matter expert) On CAFM-BR-055, CAFM-BR-056.
- DEF-139: Is this intended? The STRING pointer for the reply (WS-RESP-LENGTH) starts at 1 and is never reset between messages, so from the second request in a task each reply is appended after the previous replies in the 200-byte buffer and sent with them; after about three replies the buffer overflows. The sent length is also one byte longer than the text. (Subject-matter expert) On CAFM-BR-059.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).
