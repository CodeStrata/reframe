# Navigate the account view screen (OATM-C18)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk low

## Introduction

Controls how a user enters and leaves the account view screen. It starts fresh on first entry, treats any unsupported key as Enter, and returns to the caller or the main menu on PF3. It must keep track of whether this is a first visit or a return visit and keep the session data between interactions. An unexpected state must end with 'UNEXPECTED DATA SCENARIO' rather than guessing.

**User story:** As a user, I want the account view screen to start fresh, accept my input and return me to where I came from with PF3, so that I can move through the application predictably.

## Requirements

### Requirement 1: OATM-REQ-F-143 (business rule)

#### Acceptance criteria

1. When the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1, the system shall treat it as Enter. (rules OATM-BR-148)
2. GIVEN key pressed: PF7 WHEN the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1 THEN Processed as Enter: the account number is validated and looked up (OATM-C18-AC-01; OATM-BR-148)
3. GIVEN key pressed: PF15 WHEN the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1 THEN Treated as PF3: exit (OATM-C18-AC-02; OATM-BR-148)

### Requirement 2: OATM-REQ-F-144 (business rule)

#### Acceptance criteria

1. When the user presses PF3, the system shall transfer control, with the session data and the program context reset to first entry, to the calling program and transaction, or to the main menu ('COMEN01C', transaction 'CM00') when no caller is recorded. (rules OATM-BR-149)
2. GIVEN key pressed: PF3; calling program: COMEN01C WHEN the user presses PF3 THEN Control returns to COMEN01C (OATM-C18-AC-03; OATM-BR-149)
3. GIVEN key pressed: PF3; calling program: (blank) WHEN the user presses PF3 THEN Control goes to main menu COMEN01C under transaction CM00 (OATM-C18-AC-04; OATM-BR-149)

### Requirement 3: OATM-REQ-F-145 (design note)

#### Acceptance criteria

1. When the program starts with no session data, or is entered from the main menu ('COMEN01C') other than as a re-entry, the system shall start a fresh session context, discarding any passed data. (rules OATM-BR-150)
2. GIVEN calling program: COMEN01C; program context: 0 (first entry) WHEN the program starts with no session data, or is entered from the main menu ('COMEN01C') other than as a re-entry THEN Session data is cleared and the flow starts fresh (OATM-C18-AC-05; OATM-BR-150)

### Requirement 4: OATM-REQ-F-146 (business rule)

#### Acceptance criteria

1. While the program context is first entry (0), when PF3 was not pressed, the system shall show the empty account search screen and wait for input. (rules OATM-BR-151)
2. GIVEN key: Enter; program context: 0 WHEN PF3 was not pressed and the program context is first entry (0) THEN Empty account view screen shown (OATM-C18-AC-06; OATM-BR-151)

### Requirement 5: OATM-REQ-F-147 (design note)

#### Acceptance criteria

1. When the account view screen is sent, the system shall set the program context to re-entry (1) and end the task, keeping the session data, so that the next input from the user starts transaction 'CAVW'. (rules OATM-BR-152)
2. GIVEN screen sent: yes WHEN Screen conversation state: first entry vs re-entry applies THEN Context becomes 1 and the next input starts transaction CAVW (OATM-C18-AC-07; OATM-BR-152)

### Requirement 6: OATM-REQ-F-148 (error handling)

#### Acceptance criteria

1. If the program context is neither first entry nor re-entry, then the system shall send the plain text 'UNEXPECTED DATA SCENARIO' and end. (rules OATM-BR-153)
2. GIVEN program context: 5 WHEN the program context is neither first entry nor re-entry THEN Plain text 'UNEXPECTED DATA SCENARIO' shown, task ends (OATM-C18-AC-08; OATM-BR-153)

## Screens and components

### Account (S-ACCOUNT-VIEW)

Find an account by number and review its status, dates, balances and limits together with the cardholder's profile, address and contacts, with direct links (new) to update it or pay its balance.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| View account | button |  |  |  | OATM-REQ-F-146, OATM-REQ-F-147 |
| Account lookup error | message | Error naming what to fix, such as 'Account:<number> not found in Cross ref file', 'Account:<number> not found in Acct Master file', 'CustId:<number> not found in customer master', or a file error; the account number field is marked in error |  |  |  |
| Back | link |  |  | S-APP-SHELL | OATM-REQ-F-143, OATM-REQ-F-144, OATM-REQ-F-145 |


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

- OATM-BR-150: The screen needs a per-user conversation state with a 'first entry' marker. When there is no session, or the user arrives fresh from the main menu, the server creates new screen state and ignores any data passed in. Only a return visit to the same screen reuses its state.
- OATM-BR-152: Each time the account view is rendered, store its session state server-side (or in a signed client token) marked as 're-entry'. The next request from the user then resumes the same account view conversation. No process stays waiting between requests: the flow is stateless request handling with persisted session state.

## Open questions

- SME-067: When an account number is entered on the account view screen and the account is not found, or the file cannot be read, should the lookup stop at that point? (Currently it stops only on one exact message, 'Did not find this account in account master file', and the real not-found path produces a different message.) (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-068: On the account view screen, if the account number is left blank, which message should the operator see: 'Account number not provided' or 'No input received'? (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-069: On the account view screen, the error message says the account number must be 'a non-zero 11 digit number', but only 'numeric and non-zero' is checked. Should exactly 11 digits be required? Should the message keep its current double space? (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-070: On the account view screen, if the customer record is found but the account record is not, should the account's financial details still be shown? After a successful lookup, should the screen show a success message ('Displaying details of given Account') instead of the input prompt? (Customer service operations lead) On OATM-BR-149, OATM-BR-151.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
