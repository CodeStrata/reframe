# Design: Decide a card authorization request (CAFM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The rules that decide each card authorization for the card issuer: look up the card, then its account, customer and pending summary, and approve or decline with a clear reason code. Only known cards may be approved. A card, account or customer that is not found always declines with reason '3100', which takes precedence over insufficient funds ('4100'). Every request gets a reply, even when the card is unknown.

Runs as online.

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
| CAFM-BR-061 | Orchestrate single authorization request | business rule | WHEN an authorization request is processed, THE authorization processor SHALL start from an approve decision and look up the card in the card cross-reference; only when the card is found SHALL it read the account, the customer and the account's pending-authorization summary before deciding. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-062 | Available credit check (insufficient funds decline) | business rule | WHEN the request is declined, THE authorization decision SHALL reply with response code '05' and approved amount 0; otherwise it SHALL reply '00' with the full requested amount approved. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:664-696, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-706 |
| CAFM-BR-063 | Look up card in cross-reference | business rule | WHEN the card is not in the card cross-reference, THE authorization processor SHALL treat the card and its account as not found, so the request is declined with response '05', reason '3100' and approved amount 0. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-064 | Orchestrate single authorization request | business rule | WHEN the card is not in the card cross-reference, THE authorization processor SHALL still decide and send a reply, but SHALL NOT update the pending-authorization summary or record an authorization detail. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-065 | Look up card in cross-reference | side effect | WHEN the card is not in the card cross-reference, THE authorization processor SHALL log a warning at location 'A001' with message 'CARD NOT FOUND IN XREF' and the card number as the key. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-066 | Look up card in cross-reference | error handling | WHEN reading the card cross-reference fails for any reason other than not found, THE authorization processor SHALL log a critical error at location 'C001' with message 'FAILED TO READ XREF FILE' and the response codes, and carry on processing the request as if the card had been found. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-067 | Assign decline reason code | business rule | WHEN an authorization is approved, THE authorization reply SHALL carry reason code '0000'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-718, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:140-145, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:665-683 |
| CAFM-BR-068 | Assign decline reason code | business rule | WHEN an authorization is declined and the card, the account or the customer was not found, THE authorization reply SHALL carry reason code '3100'; this takes precedence over every other reason. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-718, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:140-145, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:665-683 |
| CAFM-BR-069 | Assign decline reason code | business rule | WHEN an authorization is declined for insufficient funds and the card, account and customer were all found, THE authorization reply SHALL carry reason code '4100'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-718, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:140-145, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:665-683 |
| CAFM-BR-070 | Assign decline reason code | historical artifact | THE reason assignment SHALL map card not active to '4200', account closed to '4300', card fraud to '5100', merchant fraud to '5200' and any other decline to '9000', but nothing in the program ever sets these conditions, so these codes are not produced today. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-718, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:140-145, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:665-683 |

### Worked examples

- CAFM-BR-061: card number = 4000000000000002 (in cross-reference) → Account, customer and summary are read, then the decision is made
- CAFM-BR-061: card number = 4000000000000099 (not in cross-reference) → No account, customer or summary is read; the decision is made directly
- CAFM-BR-062: decision = declined; amount = 250.00 → Response '05', approved amount 0.00
- CAFM-BR-062: decision = approved; amount = 75.00 → Response '00', approved amount 75.00
- CAFM-BR-063: card number = 4000000000000099 (not in cross-reference); amount = 50.00 → Reply has response '05', reason '3100', approved amount 0.00
- CAFM-BR-064: card number = 4000000000000099 (not in cross-reference) → A reply is sent; nothing is written to the pending-authorization database
- CAFM-BR-065: card number = 4000000000000099 (not in cross-reference) → Warning 'A001' 'CARD NOT FOUND IN XREF' logged with key 4000000000000099
- CAFM-BR-066: cross-reference file = unavailable → Critical error 'C001' 'FAILED TO READ XREF FILE' logged; account, customer and summary reads are still attempted and the authorization is recorded
- CAFM-BR-067: decision = approved → Reason '0000'
- CAFM-BR-068: card in cross-reference = no; decision = declined → Reason '3100'
- CAFM-BR-068: customer record = not found; decision = declined for insufficient funds → Reason '3100', not '4100'
- CAFM-BR-069: available credit = 200.00; amount = 250.00 → Response '05', reason '4100'
- CAFM-BR-070: card status = inactive → No '4200' decline is produced; the card is decided on credit only

## Decision tables

#### Authorization response and reason code

| Decision | Card, account and customer found | Decline cause | Response code, reason code and approved amount | Rule |
|---|---|---|---|---|
| Approved | All found | - | Response '00', full requested amount approved | CAFM-BR-062 |
| Approved | All found | - | Reason '0000' | CAFM-BR-067 |
| Declined | Card not in cross-reference | - | Response '05', reason '3100', approved amount 0 | CAFM-BR-063 |
| Declined | Card, account or customer not found | Any | Reason '3100' (takes precedence) | CAFM-BR-068 |
| Declined | All found | Insufficient funds | Response '05', reason '4100', approved amount 0 | CAFM-BR-069 |
| Declined | All found | Card not active | Reason '4200' (not produced today) | CAFM-BR-070 |
| Declined | All found | Account closed | Reason '4300' (not produced today) | CAFM-BR-070 |
| Declined | All found | Card fraud | Reason '5100' (not produced today) | CAFM-BR-070 |
| Declined | All found | Merchant fraud | Reason '5200' (not produced today) | CAFM-BR-070 |
| Declined | All found | Any other | Reason '9000' (not produced today) | CAFM-BR-070 |
| Declined | All found | Insufficient funds | **Gap:** The rules name an available credit check but do not state how insufficient funds is determined (which balance and limit are compared). | |
| Approved | Cross-reference read failed (not 'not found') | - | **Gap:** R11 carries on as if the card were found, but no rule says what decision or reason results when the account and customer data were not actually read. | |


## Design notes

None.

## Open questions

- SME-131: The authorization reply expiry is given as 50 with no unit. What unit and timeout should the new messaging platform use? (Integration team) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-070.
- SME-132: In the pending authorization summary, an approval sets the cash balance to zero instead of adding to it, and the declined-amount total may not use the current request's amount. Is each of these intended, or is it a defect? (Card authorization product owner) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-070.
- SME-133: Decline reasons 4200 (card not active), 4300 (account closed), 5100 (card fraud) and 5200 (merchant fraud) are defined, but nothing triggers them. Should these checks be implemented, and what data should drive them? (Card authorization product owner / fraud management team) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-068, CAFM-BR-070.
- SME-134: The authorization summary is saved before the authorization detail is recorded, so if recording the detail fails, the totals already include it. Must the summary update and the detail record succeed or fail together? (Card authorization business owner) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-070.
- SME-135: When a lookup during authorization logs a critical error (C001, C002, C003, I002), should the decision, reply and recording still go ahead for that request? (Card authorization business owner) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-070.
- DEF-001: Is this intended? The summary-found flag and the decline-reason flag are never reset between messages. When the summary read fails with an IMS error (I002), or the card is unknown, the check uses the summary flag and the limit and balance left over from the previous request in the same run. (Subject-matter expert) On CAFM-BR-062.
- DEF-022: Is this intended? The summary-found flag is not reset for each message. For an unknown card, the decision uses the summary-found flag and the limit and balance left over from an earlier request in the same run of up to 500 messages, so an unknown card can be approved. A cross-reference read error (C001) also leaves the card marked as found, and processing goes on with whatever cross-reference data is in memory. (Subject-matter expert) On CAFM-BR-064, CAFM-BR-065, CAFM-BR-066.
- DEF-023: Is this intended? A missing customer record does not cause a decline, but it takes precedence over the reason. A request declined for insufficient funds on an account whose customer is missing is reported as '3100' instead of '4100'. The flags are also never reset between messages. (Subject-matter expert) On CAFM-BR-068, CAFM-BR-070.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).