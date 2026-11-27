# Implementation plan: Validate and look up an account for viewing (OATM-C16)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

### Account (S-ACCOUNT-VIEW)

Look up an account by account number or card number and show its status, balances, limits and dates beside the customer profile on one screen, while the caller waits. Tab order: search, the cards, then Update account.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account or card number | **lookup field** | 11-digit account number or 16-digit card number (spaces and dashes ignored); a card number is resolved to its account through the card cross-reference | Blank: 'No input received' - enter an account number (11 digits) or a card number (16 digits). Not digits, wrong length or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number' (or a 16-digit card number). Not in the card cross-reference: 'Account:<number> not found in Cross ref file.' - check the number with the caller. The error shows under the field. |  | OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-130, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-133, OATM-REQ-F-134, OATM-REQ-F-135, OATM-REQ-F-136 |

### Application header and navigation (S-APP-SHELL)

New, shared by every screen: the header and navigation shown once, replacing the transaction, program, date, time and title lines every 3270 screen repeated and the numbered main-menu options. A sign-in is required; with no session the user is sent to sign-in. The navigation carries the account in context, so going from an account to Pay balance, Update account or Add transaction keeps it. Tab order: account search, navigation, then the page.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Find account (account or card number) | **lookup field** | 11-digit account number or 16-digit card number | Same checks as the account search on S-ACCOUNT-VIEW; an empty search says 'No input received' - enter an account number (11 digits) or a card number (16 digits). | S-ACCOUNT-VIEW | OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126 |


## Data model

#### CSMSG02Y

File record of COACTVWC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT01Y

File record of COACTVWC. Source: `app/cpy/CVACT01Y.cpy`.

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

File record of COACTVWC. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COACTVWC. Source: `app/cpy/CVCUS01Y.cpy`.

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

- COCOM01Y (working storage of COACTVWC): see data-contracts.md.
- COTTL01Y (working storage of COACTVWC): see data-contracts.md.
- CSDAT01Y (working storage of COACTVWC): see data-contracts.md.
- CSMSG01Y (working storage of COACTVWC): see data-contracts.md.
- CSSTRPFY (working storage of COACTVWC): see data-contracts.md.
- CSUSR01Y (working storage of COACTVWC): see data-contracts.md.
- CVACT02Y (working storage of COACTVWC): see data-contracts.md.
- CVCRD01Y (working storage of COACTVWC): see data-contracts.md.

## Design notes

- OATM-BR-130: Needs a lookup of the card-to-account link by account number (a secondary index or query on account ID). When a link is found, the customer number and card number it holds are kept in the user's session for the rest of the interaction and used by the later customer lookup.
- OATM-BR-133: Needs a read of the account by its 11-digit account number, which is the primary key. A successful read sets an 'account found' flag that tells the view to show the account's financial details.
- OATM-BR-136: Needs a read of the customer by the customer number taken from the card-to-account link, not from anything the user typed. A successful read sets a 'customer found' flag that tells the view to show the customer details.

## Decision tables

#### Account number validation

| Account number entered | Result | Rule |
|---|---|---|
| '*' or blank | Not supplied: input error, no file read, session account zero, 'No input received', field shown as '*' in red | OATM-BR-127 |
| Not all digits (including shorter than 11 digits) | Input error, no file read, session account zero, field in red, 'Account Filter must be a non-zero 11 digit number' | OATM-BR-128 |
| All zeros | Input error, no file read, session account zero, field in red, 'Account Filter must be a non-zero 11 digit number' | OATM-BR-128 |
| 11 digits, not all zeros | Accepted as session account; go on to account lookup | OATM-BR-129 |

#### Account and customer lookup outcome

| Card cross-reference read | Account master read | Customer master read | Result | Rule |
|---|---|---|---|---|
| Not found | — | — | Stop; input error; account number in red; 'Account:<account number> not found in Cross ref file. Resp:<code> Reas:<code>' | OATM-BR-131 |
| Other failure | — | — | Stop; input error; 'File Error: READ on CXACAIX returned RESP <code>,RESP2 <code>' | OATM-BR-132 |
| Found | Found | — | Account marked found; details displayed | OATM-BR-133 |
| Found | Not found | — | Input error; account number in red; 'Account:<account number> not found in Acct Master file.Resp:<code> Reas:<code>'; customer master still read | OATM-BR-134 |
| Found | Other failure | — | 'File Error: READ on ACCTDAT returned RESP <code>,RESP2 <code>'; customer master still read | OATM-BR-135 |
| Found | Any | Found | Customer marked found; customer details displayed | OATM-BR-136 |
| Found | Any | Not found | Input error; 'CustId:<customer number> not found in customer master.Resp: <code> REAS:<code>' unless an earlier message is already set | OATM-BR-137 |
| Found | Any | Other failure | Input error; 'File Error: READ on CUSTDAT returned RESP <code>,RESP2 <code>', replacing any earlier message | OATM-BR-138 |
| Found | Not found or other failure | Any | **Gap:** R26 says lookup stops at the first not found, but R17 says the customer master is still read after an account master failure; which behaviour the business wants is not settled. | |

