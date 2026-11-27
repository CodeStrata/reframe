# Implementation plan: Decide and reply to card authorization requests (CAFM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as online.

## Data model

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

## Design notes

- CAFM-BR-060: Publish each authorization reply once to the reply queue the requester named, carrying the request's correlation id. Send it non-persistent with a short expiry (50, in tenths of a second, so 5 seconds), so stale answers are dropped. If publishing fails, log critical error 'M004'.

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

