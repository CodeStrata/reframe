# Feature specification: Open and navigate the Add Transaction screen

**Feature:** OATM-C30 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C30)

As a staff user, I want to open the Add Transaction screen, pre-filled from a selected or the most recent transaction where useful, and move between screens with function keys, so that I can enter new transactions quickly within a signed-on session.

Opens the Add Transaction form for a signed-on staff user. The form can be pre-filled with a card number passed from another screen, or with the details of the most recent transaction (PF5). PF3 returns to the caller, PF4 clears the form and other keys get 'Invalid key pressed. Please see below...'. Users without a session are sent to sign-on, and nothing is added until the entries pass the checks and are confirmed.

**Acceptance scenarios:**

1. **Given** Session data length: 0, **when** the transaction add program is started without any session data, **then** Control passes to 'COSGN00C' (OATM-C30-AC-01)
2. **Given** Entered from: Main menu option 8 'Transaction Add', **when** the transaction add screen is entered for the first time (not a re-entry), **then** A blank add-transaction form is shown with the cursor on Account ID (OATM-C30-AC-02)
3. **Given** Selected value passed: 4111111111111111; Other fields: blank, **when** the screen is entered for the first time and the caller passed a selected value (CDEMO-CT02-TRN-SELECTED), **then** Card Number shows 4111111111111111 and the checks run; with the other fields blank the screen shows 'Type CD can NOT be empty...' (OATM-C30-AC-03)
4. **Given** Key: PF3; Calling program: COMEN01C, **when** the user presses PF3, **then** The main menu is shown (OATM-C30-AC-04)
5. **Given** Key: PF3; Calling program: blank, **when** the user presses PF3, **then** Control passes to 'COMEN01C' (OATM-C30-AC-05)
6. **Given** Key: PF4, **when** the user presses Enter, **then** All fields are blanked and the form is shown again (OATM-C30-AC-06)
7. **Given** Key: PF5; Card Number: 4111111111111111, **when** the user presses Enter, **then** Type, category, source, amount, description, dates and merchant details are copied from the last transaction on file and checked (OATM-C30-AC-07)
8. **Given** Account ID: blank; Card Number: blank; Key pressed: PF5, **when** the operator requests to copy data from the last transaction, **then** The message 'Account or Card Number must be entered...' is shown. (OATM-C30-AC-08)
9. **Given** Key: PF7, **when** the user presses any key other than Enter, PF3, PF4 or PF5, **then** The screen shows 'Invalid key pressed. Please see below...' (OATM-C30-AC-09)

## Requirements

### Functional requirements

- **OATM-REQ-N-012** (business rule): If the transaction add program is started without any session data, then the system shall send the user to the sign-on program 'COSGN00C'. Rules: OATM-BR-252.
- **OATM-REQ-F-238** (formatting): When the transaction add screen is entered for the first time (not a re-entry), the system shall clear the message, show a blank form with the cursor on Account ID, and mark the session so the next input counts as a re-entry. Rules: OATM-BR-253.
- **OATM-REQ-F-239** (business rule): When the transaction add screen is entered for the first time and the caller passed a selected value (CDEMO-CT02-TRN-SELECTED), the system shall put that value in Card Number and process it at once as if Enter were pressed. Rules: OATM-BR-254.
- **OATM-REQ-F-240** (business rule): When the user presses PF3 on the transaction add screen, the system shall return to the program that called it, or to the main menu 'COMEN01C' if no caller is recorded. Rules: OATM-BR-255.
- **OATM-REQ-F-241** (business rule): When the user presses Enter on the transaction add screen, the system shall check the entries and add the transaction if confirmed. Rules: OATM-BR-256.
- **OATM-REQ-F-242** (business rule): When the user presses PF4 on the transaction add screen, the system shall clear all fields and redisplay the form. Rules: OATM-BR-256.
- **OATM-REQ-F-243** (business rule): When the operator presses PF5 to copy data from the last transaction, the system shall validate the keys, retrieve the most recent transaction on file, prefill the form's data fields with its details when no error is flagged, and then process them as for Enter. Rules: OATM-BR-257, OATM-BR-256.
- **OATM-REQ-F-244** (business rule): If the user presses any key other than Enter, PF3, PF4 or PF5 on the transaction add screen, then the system shall show 'Invalid key pressed. Please see below...'. Rules: OATM-BR-258.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-252 | Screen entry, pre-selection and navigation | business rule | WHEN the transaction add program is started without any session data, THE transaction add screen SHALL send the user to the sign-on program 'COSGN00C'. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-253 | Start add-transaction on first entry | formatting | WHEN the transaction add screen is entered for the first time (not a re-entry), THE transaction add screen SHALL clear the message, show a blank form with the cursor on Account ID, and mark the session so the next input counts as a re-entry. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-254 | Start add-transaction on first entry | business rule | WHEN the screen is entered for the first time and the caller passed a selected value (CDEMO-CT02-TRN-SELECTED), THE transaction add screen SHALL put that value in Card Number and process it at once as if Enter were pressed. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-255 | Screen entry, pre-selection and navigation | business rule | WHEN the user presses PF3, THE transaction add screen SHALL return to the program that called it, or to the main menu 'COMEN01C' if no caller is recorded. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-256 | Screen entry, pre-selection and navigation | business rule | WHEN the user presses Enter, THE transaction add screen SHALL check the entries and add the transaction if confirmed; WHEN the user presses PF4, it SHALL clear all fields and redisplay the form; WHEN the user presses PF5, it SHALL fill the data fields from the most recent transaction on file and then process them as for Enter. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-257 | Copy last transaction into form | business rule | WHEN the operator requests to copy data from the last transaction, THE Transaction Data Copy SHALL validate the keys, retrieve the most recent transaction, prefill the form with its details when no error is flagged, and process the entry | medium | app/cbl/COTRN02C.cbl:471,473,475-478,480-493,495, app/cbl/COTRN02C.cbl:471-495 |
| OATM-BR-258 | Screen entry, pre-selection and navigation | business rule | WHEN the user presses any key other than Enter, PF3, PF4 or PF5, THE transaction add screen SHALL show 'Invalid key pressed. Please see below...'. | high | app/cbl/COTRN02C.cbl:107-159, app/cbl/COTRN02C.cbl:471-511, app/cbl/COTRN02C.cbl:754-779, app/cpy/CSMSG01Y.cpy:20-21 |

### Key entities

- CVACT03Y (file record)
- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CVACT01Y (working storage)

### Needs clarification

- SME-180: When the add-transaction screen first opens, a pre-selected value is placed in the Card Number field, but the field's name suggests it holds a transaction ID. Is that value meant to be a card number? (Legacy application SME) On OATM-BR-258.
- SME-181: When the operator presses PF5 to copy the last transaction as a template, should it copy the last transaction for the selected card or account instead of the last transaction in the whole file? (Product owner) On OATM-BR-257.
- DEF-080: Is this intended? The pre-fill uses a field named for a selected transaction as a card number, no program in the source sets it, and because the rest of the form is blank, processing it at once always ends with 'Type CD can NOT be empty...'. (Subject-matter expert) On OATM-BR-254, OATM-BR-258.

### Decision table gaps

None.
