# Design: Navigate the account view screen (OATM-C18)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Controls how a user moves on and off the Account View screen. Arriving from the main menu starts a fresh view. Enter, and any unsupported key, runs the lookup. PF3 (or PF15) returns the user to where they came from, or to the main menu if no caller is known. The view must never carry data over from a previous visit, and an unexpected session state must stop processing rather than guess.

Runs as online. Journeys: J01.

## Screens and components

### Account (S-ACCOUNT-VIEW)

Look up an account by account number or card number and show its status, balances, limits and dates beside the customer profile on one screen, while the caller waits. Tab order: search, the cards, then Update account.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account or card number | **lookup field** | 11-digit account number or 16-digit card number (spaces and dashes ignored); a card number is resolved to its account through the card cross-reference | Blank: 'No input received' - enter an account number (11 digits) or a card number (16 digits). Not digits, wrong length or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number' (or a 16-digit card number). Not in the card cross-reference: 'Account:<number> not found in Cross ref file.' - check the number with the caller. The error shows under the field. |  | OATM-REQ-F-143, OATM-REQ-F-146 |

### Application header and navigation (S-APP-SHELL)

New, shared by every screen: the header and navigation shown once, replacing the transaction, program, date, time and title lines every 3270 screen repeated and the numbered main-menu options. A sign-in is required; with no session the user is sent to sign-in. The navigation carries the account in context, so going from an account to Pay balance, Update account or Add transaction keeps it. Tab order: account search, navigation, then the page.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account | **primary button** |  |  | S-ACCOUNT-VIEW | OATM-REQ-F-144, OATM-REQ-F-145 |


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
| OATM-BR-148 | Only Enter and PF3 are valid actions; other keys treated as Enter | business rule | WHEN the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1, THE Account View Navigation SHALL treat it as Enter. | high | app/cbl/COACTVWC.cbl:299-314, app/cbl/COACTVWC.cbl:323-352, app/cpy/CSSTRPFY.cpy:34-35, app/cpy/CSSTRPFY.cpy:58-59 |
| OATM-BR-149 | Exit to destination program on PF3 | business rule | WHEN the user presses PF3, THE Account View Navigation SHALL transfer control, with the session data and the program context reset to first entry, to the calling program and transaction, or to the main menu ('COMEN01C', transaction 'CM00') when no caller is recorded. | high | app/cbl/COACTVWC.cbl:299-314, app/cbl/COACTVWC.cbl:323-352, app/cpy/CSSTRPFY.cpy:34-35, app/cpy/CSSTRPFY.cpy:58-59 |
| OATM-BR-150 | Screen conversation state: first entry vs re-entry | design note | WHEN the program starts with no session data, or is entered from the main menu ('COMEN01C') other than as a re-entry, THE Account View Screen Flow SHALL start a fresh session context, discarding any passed data. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |
| OATM-BR-151 | Show account screen on first entry | business rule | WHEN PF3 was not pressed and the program context is first entry (0), THE Account View Screen Flow SHALL show the empty account search screen and wait for input. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |
| OATM-BR-152 | Screen conversation state: first entry vs re-entry | design note | WHENEVER the account view screen is sent, THE Account View Screen Flow SHALL set the program context to re-entry (1) and end the task, keeping the session data, so that the next input from the user starts transaction 'CAVW'. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |
| OATM-BR-153 | Screen conversation state: first entry vs re-entry | error handling | WHEN the program context is neither first entry nor re-entry, THE Account View Screen Flow SHALL send the plain text 'UNEXPECTED DATA SCENARIO' and end. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |

### Worked examples

- OATM-BR-148: key pressed = PF7 → Processed as Enter: the account number is validated and looked up
- OATM-BR-148: key pressed = PF15 → Treated as PF3: exit
- OATM-BR-149: key pressed = PF3; calling program = COMEN01C → Control returns to COMEN01C
- OATM-BR-149: key pressed = PF3; calling program = (blank) → Control goes to main menu COMEN01C under transaction CM00
- OATM-BR-150: calling program = COMEN01C; program context = 0 (first entry) → Session data is cleared and the flow starts fresh
- OATM-BR-151: key = Enter; program context = 0 → Empty account view screen shown
- OATM-BR-152: screen sent = yes → Context becomes 1 and the next input starts transaction CAVW
- OATM-BR-153: program context = 5 → Plain text 'UNEXPECTED DATA SCENARIO' shown, task ends

## Decision tables

None.

## Design notes

- OATM-BR-150: When the view is opened with no session state, or opened from the main menu as a new visit, the application must create a new, empty view state and discard any data handed over by the previous screen. Only an explicit re-entry from the same view may reuse existing state.
- OATM-BR-152: The view is a request/response interaction that keeps its state between requests. Every time the screen is returned, the session must be marked as 're-entry' and the entered account number and lookup results kept, so that the user's next submission is handled as a continuation of the same Account View interaction.

## Open questions

- SME-067: When an account number is entered on the account view screen and the account is not found, or the file cannot be read, should the lookup stop at that point? (Currently it stops only on one exact message, 'Did not find this account in account master file', and the real not-found path produces a different message.) (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-068: On the account view screen, if the account number is left blank, which message should the operator see: 'Account number not provided' or 'No input received'? (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-069: On the account view screen, the error message says the account number must be 'a non-zero 11 digit number', but only 'numeric and non-zero' is checked. Should exactly 11 digits be required? Should the message keep its current double space? (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-070: On the account view screen, if the customer record is found but the account record is not, should the account's financial details still be shown? After a successful lookup, should the screen show a success message ('Displaying details of given Account') instead of the input prompt? (Customer service operations lead) On OATM-BR-149, OATM-BR-151.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).