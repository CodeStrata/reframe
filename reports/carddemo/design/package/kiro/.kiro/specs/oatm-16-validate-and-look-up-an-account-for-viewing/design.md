# Design: Validate and look up an account for viewing (OATM-C16)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Checks the 11-digit account number a user enters on the Account View screen. It then finds the account's linked card and customer, the account itself and the customer's profile. It must never show details for an invalid or unknown number, and every lookup that fails must give a clear message naming which record could not be found or read.

Runs as online. Journeys: J01.

## Screens and components

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


## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-126 | Treat asterisk or blank account as unsupplied | business rule | WHEN the account number entered on the Account View screen is '*' or blank, THE account view SHALL treat the account number as not supplied. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |
| OATM-BR-127 | Reject missing account number | business rule | WHEN no account number is supplied, THE account view SHALL reject the request as an input error without reading any file, set the session account to zero, show 'No input received', and redisplay the account field as '*' in red. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |
| OATM-BR-128 | Validate account number is non-zero numeric | business rule | WHEN the account number supplied is not all digits (including one shorter than 11 digits) or is all zeros, THE account view SHALL reject it as an input error without reading any file, set the session account to zero, show the account field in red and show 'Account Filter must be a non-zero 11 digit number'. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |
| OATM-BR-129 | Validate account number is non-zero numeric | business rule | WHEN the account number is 11 digits and not all zeros, THE account view SHALL accept it as the session account and go on to the account lookup. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |
| OATM-BR-130 | Orchestrate account and customer retrieval | design note | WHEN an account number passes validation on the Account View screen, THE account view SHALL look the account up in the card cross-reference by account number (CXACAIX) and, when it is found, keep that account's customer number and card number for the rest of the session. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-131 | Look up customer via card cross-reference | business rule | WHEN the account is not in the card cross-reference, THE account view SHALL stop the lookup, treat it as an input error, show the account number in red and show 'Account:<account number> not found in Cross ref file. Resp:<code> Reas:<code>'. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-132 | Look up customer via card cross-reference | error handling | WHEN reading the card cross-reference fails for any reason other than 'not found', THE account view SHALL stop the lookup, treat it as an input error and show 'File Error: READ on CXACAIX returned RESP <code>,RESP2 <code>'. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-133 | Orchestrate account and customer retrieval | design note | WHEN the account is found in the cross-reference, THE account view SHALL read the account master (ACCTDAT) by account number and, on success, mark the account as found so that its details are displayed. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-134 | Read account master record | error handling | WHEN the account is not in the account master, THE account view SHALL treat it as an input error, show the account number in red and show 'Account:<account number> not found in Acct Master file.Resp:<code> Reas:<code>'; any other read failure SHALL show 'File Error: READ on ACCTDAT returned RESP <code>,RESP2 <code>'. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-135 | Orchestrate account and customer retrieval | error handling | WHEN reading the account master does not succeed, THE account view SHALL still go on to read the customer master, because the stop check after the account read never triggers (the 'not found' flag is never set). | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-136 | Orchestrate account and customer retrieval | design note | THE account view SHALL read the customer master (CUSTDAT) using the customer number taken from the card cross-reference and, on success, mark the customer as found so that the customer details are displayed. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-137 | Read customer master record | error handling | WHEN the customer is not in the customer master, THE account view SHALL treat it as an input error and show 'CustId:<customer number> not found in customer master.Resp: <code> REAS:<code>', unless an earlier message is already set. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-138 | Read customer master record | error handling | WHEN reading the customer master fails for any reason other than 'not found', THE account view SHALL treat it as an input error and show 'File Error: READ on CUSTDAT returned RESP <code>,RESP2 <code>', replacing any earlier message. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-139 | Process entered account on re-entry | business rule | WHEN PF3 was not pressed and the program context is re-entry (1), THE Account View Screen Flow SHALL read and validate the entered account number; on an input error it SHALL redisplay the screen with the error, otherwise it SHALL look up the card cross-reference, account master and customer master in turn (stopping at the first not found) and display the screen. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |

### Worked examples

- OATM-BR-126: Account number = '*' → Handled exactly like a blank account number
- OATM-BR-127: Account number = blank → Message 'No input received'; the account field shows '*' in red; no file is read
- OATM-BR-128: Account number = ABC12345678 → Message 'Account Filter must be a non-zero 11 digit number'
- OATM-BR-128: Account number = 00000000000 → Message 'Account Filter must be a non-zero 11 digit number'
- OATM-BR-129: Account number = 00000012345 → Accepted; the card cross-reference is read for account 00000012345
- OATM-BR-130: Account number = 00000012345; Cross-reference entry = customer 000000123, card 4111111111111111 → Customer 000000123 and card 4111111111111111 are kept for the session and the account master is read next
- OATM-BR-133: Account number = 00000012345; Account master = record exists → The account is marked as found and its status, balances, limits and dates are displayed
- OATM-BR-135: Account master = no record for 00000012345; Customer master = customer 000000123 exists → The customer is still read and shown, the account fields are shown from an empty record, and the account 'not found' message is still shown
- OATM-BR-136: Cross-reference customer = 000000123; Customer master = record exists → The customer's name, address, phones, SSN and FICO score are displayed
- OATM-BR-139: program context = 1; account number = 00000000000 → Screen redisplayed with 'Account number must be a non zero 11 digit number'
- OATM-BR-139: program context = 1; account number = 00000012345; cross-reference, account, customer = all found → Screen shows account and customer details

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


## Design notes

- OATM-BR-130: Needs a lookup of the card-to-account link by account number (a secondary index or query on account ID). When a link is found, the customer number and card number it holds are kept in the user's session for the rest of the interaction and used by the later customer lookup.
- OATM-BR-133: Needs a read of the account by its 11-digit account number, which is the primary key. A successful read sets an 'account found' flag that tells the view to show the account's financial details.
- OATM-BR-136: Needs a read of the customer by the customer number taken from the card-to-account link, not from anything the user typed. A successful read sets a 'customer found' flag that tells the view to show the customer details.

## Open questions

- SME-067: When an account number is entered on the account view screen and the account is not found, or the file cannot be read, should the lookup stop at that point? (Currently it stops only on one exact message, 'Did not find this account in account master file', and the real not-found path produces a different message.) (Business analyst) On OATM-BR-127, OATM-BR-129, OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138, OATM-BR-139.
- SME-068: On the account view screen, if the account number is left blank, which message should the operator see: 'Account number not provided' or 'No input received'? (Business analyst) On OATM-BR-127, OATM-BR-129, OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138, OATM-BR-139.
- SME-069: On the account view screen, the error message says the account number must be 'a non-zero 11 digit number', but only 'numeric and non-zero' is checked. Should exactly 11 digits be required? Should the message keep its current double space? (Business analyst) On OATM-BR-127, OATM-BR-129, OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138, OATM-BR-139.
- SME-070: On the account view screen, if the customer record is found but the account record is not, should the account's financial details still be shown? After a successful lookup, should the screen show a success message ('Displaying details of given Account') instead of the input prompt? (Customer service operations lead) On OATM-BR-127, OATM-BR-129, OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138, OATM-BR-139.
- SME-071: Please confirm the priority of the account view lookup chain (card cross-reference, then account master, then customer master). Is it critical to the system's core purpose, or a rule that would be costly if it were wrong? (Account servicing subject-matter expert) On OATM-BR-138.
- DEF-044: Is this intended? A blank account number first sets the message 'Account number not provided', which is then replaced at once with 'No input received', so the more specific message can never be shown. The 'only if no message yet' guard in front of it has no effect. (Subject-matter expert) On OATM-BR-127, OATM-BR-129.
- DEF-045: Is this intended? When the account is missing from the account master, or the read fails, the lookup does not stop: the stop check tests a message flag that is never set, so the customer master is still read. If the customer is found, the account fields are filled from an empty account record next to the account 'not found' message. (Subject-matter expert) On OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (18 in all).