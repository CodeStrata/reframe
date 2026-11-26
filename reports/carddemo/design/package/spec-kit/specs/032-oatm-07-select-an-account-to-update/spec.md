# Feature specification: Select an account to update

**Feature:** OATM-C07 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C07)

As an operator, I want to enter an account number and see the account and customer details, so that I can review and update them.

Lets the operator enter an 11-digit account number to start an update; until an account is fetched only that number is checked. A valid number triggers the cross-reference, account and customer lookups, and details are shown only when all three are found. A blank, non-numeric or all-zero number must never lead to a lookup.

**Acceptance scenarios:**

1. **Given** Account number entered: '*', **when** the operator submits the account update screen, **then** The account number is treated as not supplied (OATM-C07-AC-01)
2. **Given** Account number entered: 00000012345, **when** the operator submits the account update screen, **then** 00000012345 is used as the account to search for (OATM-C07-AC-02)
3. **Given** Account details fetched: No; Account number entered: 00000012345; Active status entered: X, **when** no account details have been fetched yet, **then** Only the account number is checked; the active status is not checked (OATM-C07-AC-03)
4. **Given** Account number entered: (blank), **when** no account details have been fetched yet and the account number is blank or '*', **then** Error 'No input received' is shown and no account is read (OATM-C07-AC-04)
5. **Given** Account number entered: '*', **when** no account details have been fetched yet and the account number is blank or '*', **then** Error 'No input received' is shown and no account is read (OATM-C07-AC-05)
6. **Given** Account number entered: 00000012345, **when** no account details have been fetched yet and the account number is an 11-digit non-zero number, **then** 00000012345 becomes the current account and its details are looked up (OATM-C07-AC-06)
7. **Given** account number: 00000000001; cross-reference, account and customer: all exist, **when** account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, **then** Details are shown and state becomes 'S' (OATM-C07-AC-07)
8. **Given** account number: 00000000099; account master record: missing, **when** account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, **then** Lookup stops with 'Did not find this account in account master file'; details are not shown (OATM-C07-AC-08)
9. **Given** key: PF12; update state: 'E', **when** account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, **then** Account is re-read, pending edits are discarded and state returns to 'S' (OATM-C07-AC-09)
10. **Given** no account details have been fetched yet and the operator enters account number '1234ABC5678', **when** the screen is submitted, **then** the message 'Account Number if supplied must be a 11 digit Non-Zero Number' is shown, the current account number is set to zeros and no account is read (OATM-C07-AC-10)
11. **Given** no account details have been fetched yet and the operator enters account number '00000000000', **when** the screen is submitted, **then** the message 'Account Number if supplied must be a 11 digit Non-Zero Number' is shown, the current account number is set to zeros and no account is read (OATM-C07-AC-11)

## Requirements

### Functional requirements

- **OATM-REQ-F-062** (design note): When the operator submits the account update screen, the system shall treat an account number of '*' or blank as not supplied and otherwise take the entered value as the account to search for. Rules: OATM-BR-061.
- **OATM-REQ-F-063** (business rule): While no account details have been fetched yet, the system shall check only the account number and ignore every other field on the screen. Rules: OATM-BR-062.
- **OATM-REQ-F-064** (business rule): If no account details have been fetched yet and the account number is blank or '*', then the system shall show the error 'No input received', set the current account number to zeros and read no account. Rules: OATM-BR-063.
- **OATM-REQ-F-065** (business rule): If no account details have been fetched yet and the account number supplied is not numeric or is all zeros, then the system shall show 'Account Number if supplied must be a 11 digit Non-Zero Number', set the current account number to zeros and read no account. Rules: OATM-BR-064.
- **OATM-REQ-F-066** (business rule): While no account details have been fetched yet, when the account number is an 11-digit non-zero number, the system shall accept it as the current account and go on to look the account up. Rules: OATM-BR-065.
- **OATM-REQ-F-067** (business rule): When account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, the system shall look up the card cross-reference, then the account, then the customer, stopping at the first one not found, and shall show the details (state 'S') only when all three are found. Rules: OATM-BR-066.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-061 | Capture account id entry | design note | WHEN the operator submits the account update screen, THE account update screen SHALL treat an account number of '*' or blank as not supplied and otherwise take the entered value as the account to search for. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-062 | Skip edits when details not fetched | business rule | WHEN no account details have been fetched yet, THE account update screen SHALL check only the account number and ignore every other field on the screen. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-063 | Reject missing account number | business rule | WHEN no account details have been fetched yet and the account number is blank or '*', THE account update screen SHALL show the error 'No input received', set the current account number to zeros and read no account. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-064 | Require 11-digit non-zero account number | business rule | WHEN no account details have been fetched yet and the account number supplied is not numeric or is all zeros, THE account update screen SHALL show 'Account Number if supplied must be a 11 digit Non-Zero Number', set the current account number to zeros and read no account. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-065 | Require 11-digit non-zero account number | business rule | WHEN no account details have been fetched yet and the account number is an 11-digit non-zero number, THE account update screen SHALL accept it as the current account and go on to look the account up. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-066 | Retrieve account and customer details for update | business rule | WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, THE account update screen SHALL look up the card cross-reference, then the account, then the customer, stopping at the first one not found, and SHALL show the details (state 'S') only when all three are found. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSLKPCDY (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDPY (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-054: When saving an account update, a failure to lock the customer record is reported as a successful save. Is that intended, or should it be reported as a lock error? (Account servicing business owner) On OATM-BR-066.
- SME-055: When the customer for an account cannot be found during account update, a 'not found' message is shown but the customer is not marked as not found. Should the new system explicitly mark the customer as not found? (Account servicing business owner) On OATM-BR-062, OATM-BR-063, OATM-BR-065, OATM-BR-066.
- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-062.
- DEF-040: Is this intended? For a blank account number, the 'Account number not provided' message set in 1210-EDIT-ACCOUNT is always overwritten by 'No input received' in 1200-EDIT-MAP-INPUTS, so the more specific message is never shown on this path. (Subject-matter expert) On OATM-BR-062, OATM-BR-063, OATM-BR-065.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-066.

### Decision table gaps

- Account number check before details are fetched: No rule states whether a shorter numeric entry is accepted (e.g. padded) or rejected with the 11-digit message.
