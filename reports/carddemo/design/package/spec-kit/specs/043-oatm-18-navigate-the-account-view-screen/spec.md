# Feature specification: Navigate the account view screen

**Feature:** OATM-C18 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C18)

As a user, I want the account view screen to start fresh, accept my input and return me to where I came from with PF3, so that I can move through the application predictably.

Controls how a user moves on and off the Account View screen. Arriving from the main menu starts a fresh view. Enter, and any unsupported key, runs the lookup. PF3 (or PF15) returns the user to where they came from, or to the main menu if no caller is known. The view must never carry data over from a previous visit, and an unexpected session state must stop processing rather than guess.

**Acceptance scenarios:**

1. **Given** key pressed: PF7, **when** the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1, **then** Processed as Enter: the account number is validated and looked up (OATM-C18-AC-01)
2. **Given** key pressed: PF15, **when** the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1, **then** Treated as PF3: exit (OATM-C18-AC-02)
3. **Given** key pressed: PF3; calling program: COMEN01C, **when** the user presses PF3, **then** Control returns to COMEN01C (OATM-C18-AC-03)
4. **Given** key pressed: PF3; calling program: (blank), **when** the user presses PF3, **then** Control goes to main menu COMEN01C under transaction CM00 (OATM-C18-AC-04)
5. **Given** calling program: COMEN01C; program context: 0 (first entry), **when** the program starts with no session data, or is entered from the main menu ('COMEN01C') other than as a re-entry, **then** Session data is cleared and the flow starts fresh (OATM-C18-AC-05)
6. **Given** key: Enter; program context: 0, **when** PF3 was not pressed and the program context is first entry (0), **then** Empty account view screen shown (OATM-C18-AC-06)
7. **Given** screen sent: yes, **when** Screen conversation state: first entry vs re-entry applies, **then** Context becomes 1 and the next input starts transaction CAVW (OATM-C18-AC-07)
8. **Given** program context: 5, **when** the program context is neither first entry nor re-entry, **then** Plain text 'UNEXPECTED DATA SCENARIO' shown, task ends (OATM-C18-AC-08)

## Requirements

### Functional requirements

- **OATM-REQ-F-143** (business rule): When the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1, the system shall treat it as Enter. Rules: OATM-BR-148.
- **OATM-REQ-F-144** (business rule): When the user presses PF3, the system shall transfer control, with the session data and the program context reset to first entry, to the calling program and transaction, or to the main menu ('COMEN01C', transaction 'CM00') when no caller is recorded. Rules: OATM-BR-149.
- **OATM-REQ-F-145** (design note): When the program starts with no session data, or is entered from the main menu ('COMEN01C') other than as a re-entry, the system shall start a fresh session context, discarding any passed data. Rules: OATM-BR-150.
- **OATM-REQ-F-146** (business rule): While the program context is first entry (0), when PF3 was not pressed, the system shall show the empty account search screen and wait for input. Rules: OATM-BR-151.
- **OATM-REQ-F-147** (design note): When the account view screen is sent, the system shall set the program context to re-entry (1) and end the task, keeping the session data, so that the next input from the user starts transaction 'CAVW'. Rules: OATM-BR-152.
- **OATM-REQ-F-148** (error handling): If the program context is neither first entry nor re-entry, then the system shall send the plain text 'UNEXPECTED DATA SCENARIO' and end. Rules: OATM-BR-153.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-148 | Only Enter and PF3 are valid actions; other keys treated as Enter | business rule | WHEN the user presses any key other than Enter or PF3 (PF15 counts as PF3), such as PF7, Clear or PA1, THE Account View Navigation SHALL treat it as Enter. | high | app/cbl/COACTVWC.cbl:299-314, app/cbl/COACTVWC.cbl:323-352, app/cpy/CSSTRPFY.cpy:34-35, app/cpy/CSSTRPFY.cpy:58-59 |
| OATM-BR-149 | Exit to destination program on PF3 | business rule | WHEN the user presses PF3, THE Account View Navigation SHALL transfer control, with the session data and the program context reset to first entry, to the calling program and transaction, or to the main menu ('COMEN01C', transaction 'CM00') when no caller is recorded. | high | app/cbl/COACTVWC.cbl:299-314, app/cbl/COACTVWC.cbl:323-352, app/cpy/CSSTRPFY.cpy:34-35, app/cpy/CSSTRPFY.cpy:58-59 |
| OATM-BR-150 | Screen conversation state: first entry vs re-entry | design note | WHEN the program starts with no session data, or is entered from the main menu ('COMEN01C') other than as a re-entry, THE Account View Screen Flow SHALL start a fresh session context, discarding any passed data. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |
| OATM-BR-151 | Show account screen on first entry | business rule | WHEN PF3 was not pressed and the program context is first entry (0), THE Account View Screen Flow SHALL show the empty account search screen and wait for input. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |
| OATM-BR-152 | Screen conversation state: first entry vs re-entry | design note | WHENEVER the account view screen is sent, THE Account View Screen Flow SHALL set the program context to re-entry (1) and end the task, keeping the session data, so that the next input from the user starts transaction 'CAVW'. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |
| OATM-BR-153 | Screen conversation state: first entry vs re-entry | error handling | WHEN the program context is neither first entry nor re-entry, THE Account View Screen Flow SHALL send the plain text 'UNEXPECTED DATA SCENARIO' and end. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVACT02Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-067: When an account number is entered on the account view screen and the account is not found, or the file cannot be read, should the lookup stop at that point? (Currently it stops only on one exact message, 'Did not find this account in account master file', and the real not-found path produces a different message.) (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-068: On the account view screen, if the account number is left blank, which message should the operator see: 'Account number not provided' or 'No input received'? (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-069: On the account view screen, the error message says the account number must be 'a non-zero 11 digit number', but only 'numeric and non-zero' is checked. Should exactly 11 digits be required? Should the message keep its current double space? (Business analyst) On OATM-BR-149, OATM-BR-151.
- SME-070: On the account view screen, if the customer record is found but the account record is not, should the account's financial details still be shown? After a successful lookup, should the screen show a success message ('Displaying details of given Account') instead of the input prompt? (Customer service operations lead) On OATM-BR-149, OATM-BR-151.

### Decision table gaps

None.
