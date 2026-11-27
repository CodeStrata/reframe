# Record pending authorization summary and detail (CAFM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Records every decided authorization for a known card against the account's pending-authorization summary and as a detail record, so approved and declined counts, totals and balances stay current for matching and fraud review. Approvals add to the approved count, approved total and credit balance. Each detail is stored with match status 'P' or 'D' and a blank fraud flag. A failure to save must be logged as a critical error ('I003' or 'I004').

**User story:** As a card issuer, I want every decided authorization for a known card recorded against the account's pending-authorization summary and as a detail record, so that approved and declined totals and balances are kept current for later matching and review.

## Requirements

### Requirement 1: CAFM-REQ-F-071 (business rule)

#### Acceptance criteria

1. When an authorization for a known card is recorded and the account has no pending-authorization summary yet, the system shall start a new summary with all counts and amounts at zero, carrying the account and customer from the card cross-reference, and add it, and otherwise shall replace the existing summary. (rules CAFM-BR-071, CAFM-BR-072)
2. GIVEN account: 00000000012; existing summary: none; decision: approved 200.00 WHEN an authorization for a known card is recorded and the account has no pending-authorization summary yet THEN A new summary is inserted with approved count 1, approved amount 200.00 and credit balance 200.00 (CAFM-C07-AC-01; CAFM-BR-071)
3. GIVEN Account summary existed: Yes; Decision: approved WHEN a card in the cross-reference has had its authorization decided THEN The existing summary for the account is replaced with the updated totals. (CAFM-C07-AC-02; CAFM-BR-072)
4. GIVEN Account summary existed: No WHEN a card in the cross-reference has had its authorization decided THEN A new summary for the account is inserted. (CAFM-C07-AC-03; CAFM-BR-072)

### Requirement 2: CAFM-REQ-F-072 (business rule)

#### Acceptance criteria

1. When an authorization for a known card is recorded, the system shall set the summary credit limit and cash limit from the account record. (rules CAFM-BR-073)
2. GIVEN account credit limit: 5000.00; account cash credit limit: 1000.00; summary credit limit before: 4000.00 WHEN an authorization for a known card is recorded THEN Summary credit limit becomes 5000.00 and cash limit 1000.00 (CAFM-C07-AC-04; CAFM-BR-073)

### Requirement 3: CAFM-REQ-F-073 (business rule)

#### Acceptance criteria

1. When the authorization is approved, the system shall add 1 to the approved count, add the approved amount to the approved total and to the credit balance, and set the cash balance to 0. (rules CAFM-BR-074)
2. GIVEN credit balance: 1000.00; approved count: 3; approved amount total: 600.00; approved amount: 200.00 WHEN the authorization is approved THEN Approved count 4, approved total 800.00, credit balance 1200.00, cash balance 0 (CAFM-C07-AC-05; CAFM-BR-074)

### Requirement 4: CAFM-REQ-F-074 (business rule)

#### Acceptance criteria

1. When the authorization is declined, the system shall add 1 to the declined count and add to the declined total the transaction amount from the previously recorded authorization detail, not the current request. (rules CAFM-BR-075)
2. GIVEN declined count: 2; declined total: 300.00; current declined amount: 500.00; previous recorded request amount: 40.00 WHEN the authorization is declined THEN Declined count 3, declined total 340.00 (CAFM-C07-AC-06; CAFM-BR-075)

### Requirement 5: CAFM-REQ-F-075 (error handling)

#### Acceptance criteria

1. If adding or replacing the pending authorization summary fails, then the system shall log a critical error at location 'I003' with message 'IMS UPDATE SUMRY FAILED' and the IMS status. (rules CAFM-BR-076, CAFM-BR-077)
2. GIVEN IMS status on summary update: not OK WHEN adding or replacing the summary fails THEN Critical error 'I003' 'IMS UPDATE SUMRY FAILED' logged; the detail insert is still attempted (CAFM-C07-AC-07; CAFM-BR-076)
3. GIVEN IMS status on summary save: II WHEN saving the pending authorization summary fails THEN Error 'I003' 'IMS UPDATE SUMRY FAILED' is logged; no authorization detail is inserted and the task ends. (CAFM-C07-AC-08; CAFM-BR-077)

### Requirement 6: CAFM-REQ-F-076 (design note)

#### Acceptance criteria

1. When an authorization for a known card is recorded, the system shall build an authorization detail from the request (original date and time, card, type, expiry, message type and source, processing code, amount, merchant details, transaction id) and the reply (authorization id code, response code, reason, approved amount), and insert it under the account's summary. (rules CAFM-BR-078)
2. GIVEN account: 00000000012; amount: 75.00; response: '00' WHEN an authorization for a known card is recorded THEN A detail with response '00', reason '0000' and approved amount 75.00 is inserted under the summary for account 00000000012 (CAFM-C07-AC-09; CAFM-BR-078)

### Requirement 7: CAFM-REQ-F-077 (business rule)

#### Acceptance criteria

1. When the authorization detail is recorded, the system shall set match status 'P' (pending) for an approved authorization and 'D' (declined) for a declined one. (rules CAFM-BR-079)
2. GIVEN decision: approved WHEN the authorization detail is recorded THEN Match status 'P' (CAFM-C07-AC-10; CAFM-BR-079)
3. GIVEN decision: declined WHEN the authorization detail is recorded THEN Match status 'D' (CAFM-C07-AC-11; CAFM-BR-079)

### Requirement 8: CAFM-REQ-F-078 (business rule)

#### Acceptance criteria

1. When the authorization detail is recorded, the system shall leave the fraud flag and the fraud report date blank. (rules CAFM-BR-080)
2. GIVEN decision: approved WHEN the authorization detail is recorded THEN Fraud flag ' ', fraud report date blank (CAFM-C07-AC-12; CAFM-BR-080)

### Requirement 9: CAFM-REQ-F-079 (error handling)

#### Acceptance criteria

1. If inserting the authorization detail fails, then the system shall log a critical error at location 'I004' with message 'IMS INSERT DETL FAILED' and the IMS status. (rules CAFM-BR-081)
2. GIVEN IMS status on detail insert: not OK WHEN inserting the authorization detail fails THEN Critical error 'I004' 'IMS INSERT DETL FAILED' logged; the reply already sent is unchanged (CAFM-C07-AC-13; CAFM-BR-081)

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
| CAFM-BR-071 | Accumulate pending authorization summary totals | business rule | WHEN an authorization for a known card is recorded and the account has no pending-authorization summary yet, THE summary maintenance SHALL start a new summary with all counts and amounts at zero, carrying the account and customer from the card cross-reference, and add it; otherwise it SHALL replace the existing summary. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-072 | Save pending authorization summary | design note | WHEN a card in the cross-reference has had its authorization decided, THE pending authorization summary maintenance SHALL replace the account's existing summary if one was found, or insert a new summary if none existed (physical store PAUTSUM0). | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:824-847, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:940-977, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:983-1023 |
| CAFM-BR-073 | Accumulate pending authorization summary totals | business rule | WHEN an authorization for a known card is recorded, THE summary maintenance SHALL set the summary credit limit and cash limit from the account record. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-074 | Accumulate pending authorization summary totals | business rule | WHEN the authorization is approved, THE summary maintenance SHALL add 1 to the approved count, add the approved amount to the approved total and to the credit balance, and set the cash balance to 0. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-075 | Accumulate pending authorization summary totals | business rule | WHEN the authorization is declined, THE summary maintenance SHALL add 1 to the declined count and add a transaction amount to the declined total, but the amount it adds is the one from the previously recorded authorization detail, not the current request. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-076 | Accumulate pending authorization summary totals | error handling | WHEN adding or replacing the summary fails, THE summary maintenance SHALL log a critical error at location 'I003' with message 'IMS UPDATE SUMRY FAILED' and the IMS status, and continue on to record the detail. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-077 | Save pending authorization summary | error handling | WHEN saving the pending authorization summary fails, THE authorization processor SHALL log critical error 'I003' with message 'IMS UPDATE SUMRY FAILED' and the IMS status, and SHALL not record the authorization detail for that request. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:824-847, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:940-977, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:983-1023 |
| CAFM-BR-078 | Insert pending authorization detail record | design note | WHEN an authorization for a known card is recorded, THE detail recording SHALL build an authorization detail from the request (original date and time, card, type, expiry, message type and source, processing code, amount, merchant details, transaction id) and the reply (authorization id code, response code, reason, approved amount), and insert it under the account's summary. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:877-932, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:45-53 |
| CAFM-BR-079 | Insert pending authorization detail record | business rule | WHEN the authorization detail is recorded, THE detail recording SHALL set match status 'P' (pending) for an approved authorization and 'D' (declined) for a declined one. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:877-932, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:45-53 |
| CAFM-BR-080 | Insert pending authorization detail record | business rule | WHEN the authorization detail is recorded, THE detail recording SHALL leave the fraud flag and the fraud report date blank. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:877-932, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:45-53 |
| CAFM-BR-081 | Insert pending authorization detail record | error handling | WHEN inserting the authorization detail fails, THE detail recording SHALL log a critical error at location 'I004' with message 'IMS INSERT DETL FAILED' and the IMS status; the insert is attempted even if the summary update just failed. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:877-932, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:45-53 |

### Worked examples

- CAFM-BR-071: account = 00000000012; existing summary = none; decision = approved 200.00 → A new summary is inserted with approved count 1, approved amount 200.00 and credit balance 200.00
- CAFM-BR-072: Account summary existed = Yes; Decision = approved → The existing summary for the account is replaced with the updated totals.
- CAFM-BR-072: Account summary existed = No → A new summary for the account is inserted.
- CAFM-BR-073: account credit limit = 5000.00; account cash credit limit = 1000.00; summary credit limit before = 4000.00 → Summary credit limit becomes 5000.00 and cash limit 1000.00
- CAFM-BR-074: credit balance = 1000.00; approved count = 3; approved amount total = 600.00; approved amount = 200.00 → Approved count 4, approved total 800.00, credit balance 1200.00, cash balance 0
- CAFM-BR-075: declined count = 2; declined total = 300.00; current declined amount = 500.00; previous recorded request amount = 40.00 → Declined count 3, declined total 340.00
- CAFM-BR-076: IMS status on summary update = not OK → Critical error 'I003' 'IMS UPDATE SUMRY FAILED' logged; the detail insert is still attempted
- CAFM-BR-077: IMS status on summary save = II → Error 'I003' 'IMS UPDATE SUMRY FAILED' is logged; no authorization detail is inserted and the task ends.
- CAFM-BR-078: account = 00000000012; amount = 75.00; response = '00' → A detail with response '00', reason '0000' and approved amount 75.00 is inserted under the summary for account 00000000012
- CAFM-BR-079: decision = approved → Match status 'P'
- CAFM-BR-079: decision = declined → Match status 'D'
- CAFM-BR-080: decision = approved → Fraud flag ' ', fraud report date blank
- CAFM-BR-081: IMS status on detail insert = not OK → Critical error 'I004' 'IMS INSERT DETL FAILED' logged; the reply already sent is unchanged

## Decision tables

#### Pending authorization summary update

| Card in cross-reference | Summary exists for account | Decision | Summary and detail update | Rule |
|---|---|---|---|---|
| No | - | Any | No summary update and no detail recorded |  |
| Yes | No | Any | New summary started at zero with account and customer from cross-reference, then added | CAFM-BR-071 |
| Yes | Yes | Any | Existing summary replaced | CAFM-BR-072 |
| Yes | Any | Approved | Approved count +1, approved amount added to approved total and credit balance, cash balance set to 0; detail match status 'P' | CAFM-BR-074 |
| Yes | Any | Declined | Declined count +1, previously recorded detail amount added to declined total; detail match status 'D' | CAFM-BR-075 |
| Yes | Any | Summary save failed | **Gap:** Rules disagree: R6 and R19 say the detail insert is still attempted, R21 says the detail is not recorded, and R22 says any critical error ends the task. Confirm whether the detail is recorded after a failed summary save. | |
| Yes | No | Declined | **Gap:** R5 adds the amount from the previously recorded authorization detail; no rule says which amount is used when there is no previous detail for a new summary. | |


## Design notes

- CAFM-BR-072: Save the account's summary as an upsert keyed by account id: update it if one was found, insert it if not. Do the save in the same transaction as the detail insert, so the summary and its details cannot drift apart.
- CAFM-BR-078: Insert the authorization detail as a child of the account's summary (a foreign key to the account summary). It holds the request fields and the reply's authorization id, response code, reason and approved amount, and is keyed newest first for paging and purge.

## Open questions

- SME-131: The authorization reply expiry is given as 50 with no unit. What unit and timeout should the new messaging platform use? (Integration team) On CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-132: In the pending authorization summary, an approval sets the cash balance to zero instead of adding to it, and the declined-amount total may not use the current request's amount. Is each of these intended, or is it a defect? (Card authorization product owner) On CAFM-BR-074, CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-133: Decline reasons 4200 (card not active), 4300 (account closed), 5100 (card fraud) and 5200 (merchant fraud) are defined, but nothing triggers them. Should these checks be implemented, and what data should drive them? (Card authorization product owner / fraud management team) On CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-134: The authorization summary is saved before the authorization detail is recorded, so if recording the detail fails, the totals already include it. Must the summary update and the detail record succeed or fail together? (Card authorization business owner) On CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-135: When a lookup during authorization logs a critical error (C001, C002, C003, I002), should the decision, reply and recording still go ahead for that request? (Card authorization business owner) On CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-136: If the database fails after an authorization request has been taken off the queue and answered, the request is lost. Is that acceptable, or must such authorizations be reconciled? (Card authorization operations lead) On CAFM-BR-077.
- DEF-002: Is this intended? The declined total adds the transaction amount from the detail segment buffer. That buffer is filled for the current request only later, in 8500-INSERT-AUTH, so it adds the previous recorded request's amount (or zero or garbage for the first one). Also, every approval resets the summary cash balance to 0. (Subject-matter expert) On CAFM-BR-074, CAFM-BR-076.
- DEF-061: Is this intended? Summary and detail failures are only logged. The reply has already been sent, the detail insert goes ahead even after the summary update fails, and the SYNCPOINT at the end of each message commits whatever succeeded, so the summary and its details can fall out of step. (Subject-matter expert) On CAFM-BR-080, CAFM-BR-081.
- DEF-084: Is this intended? The reply to the merchant is sent (without syncpoint) before the summary and detail are written, so when the summary save fails with I003 the merchant has already received the decision (possibly an approval) while no pending authorization summary or detail is recorded for it. (Subject-matter expert) On CAFM-BR-077.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).
