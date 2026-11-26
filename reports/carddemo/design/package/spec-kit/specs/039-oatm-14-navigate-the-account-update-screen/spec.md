# Feature specification: Navigate the account update screen

**Feature:** OATM-C14 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C14)

As an operator, I want the account update screen to respond predictably to my keys and to start afresh when appropriate, so that I always know which step of the update I am in.

Controls how the account update screen moves between its steps: a blank search on first arrival, checking entries on each submit, and a fresh start after a save has completed or failed. It is for operators maintaining accounts. It must never act on PF5 unless validated changes are waiting for confirmation, and never on PF12 unless account details have been fetched.

**Acceptance scenarios:**

1. **Given** previous program: COMEN01C; first arrival: yes, **when** the operator arrives with no saved context, or comes from the main menu ('COMEN01C') for the first time, **then** Empty account update screen with 'Enter or update id of account to update' (OATM-C14-AC-01)
2. **Given** update state: 'C'; key: Enter, **when** the operator submits the screen with any key other than PF3 after a committed ('C') or failed ('L', 'F') save, **then** Screen cleared; prompt 'Enter or update id of account to update' (OATM-C14-AC-02)
3. **Given** update state: 'F'; key: Enter, **when** the operator submits the screen with any key other than PF3 after a committed ('C') or failed ('L', 'F') save, **then** Screen cleared; a new account number must be entered (OATM-C14-AC-03)
4. **Given** key: Enter; update state: 'S' (details shown), **when** the operator submits the screen with any key other than PF3, and it is not a first arrival and not the interaction after a committed or failed save, **then** Entries are checked and the screen is shown again with the outcome (OATM-C14-AC-04)
5. **Given** key: PF5; update state: 'S', **when** account update screen runs, **then** Treated as Enter; nothing is saved (OATM-C14-AC-05)
6. **Given** key: PF12; update state: not fetched, **when** account update screen runs, **then** Treated as Enter (OATM-C14-AC-06)

## Requirements

### Functional requirements

- **OATM-REQ-F-114** (formatting): When the operator arrives with no saved context, or comes from the main menu ('COMEN01C') for the first time, the system shall clear any previous update data and show an empty screen asking 'Enter or update id of account to update'. Rules: OATM-BR-117.
- **OATM-REQ-F-115** (business rule): When the operator submits the screen with any key other than PF3 after a committed ('C') or failed ('L', 'F') save, the system shall clear the update data and account number and show an empty screen asking for a new account number. Rules: OATM-BR-118.
- **OATM-REQ-F-116** (business rule): When the operator submits the screen with any key other than PF3, and it is not a first arrival and not the interaction after a committed or failed save, the system shall read and check the entries, decide the next step from the update state, and show the screen again. Rules: OATM-BR-119.
- **OATM-REQ-F-117** (business rule): The system shall accept PF5 only while validated changes await confirmation ('N') and PF12 only once account details have been fetched, and shall treat any other key, or PF5/PF12 outside those states, as Enter. Rules: OATM-BR-120.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-117 | Show blank search screen on first entry | formatting | WHEN the operator arrives with no saved context, or comes from the main menu ('COMEN01C') for the first time, THE account update screen SHALL clear any previous update data and show an empty screen asking 'Enter or update id of account to update'. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-118 | Restart after completed or failed save | business rule | WHEN the operator submits the screen with any key other than PF3 after a committed ('C') or failed ('L', 'F') save, THE account update screen SHALL clear the update data and account number and show an empty screen asking for a new account number. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-119 | Route other requests to input processing | business rule | WHEN the operator submits the screen with any key other than PF3, and it is not a first arrival and not the interaction after a committed or failed save, THE account update screen SHALL read and check the entries, decide the next step from the update state, and show the screen again. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-120 | Account update screen lifecycle (change-action state machine) | business rule | THE account update screen SHALL accept PF5 only while validated changes await confirmation ('N') and PF12 only once account details have been fetched, and SHALL treat any other key, or PF5/PF12 outside those states, as Enter. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

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

- SME-054: When saving an account update, a failure to lock the customer record is reported as a successful save. Is that intended, or should it be reported as a lock error? (Account servicing business owner) On OATM-BR-117, OATM-BR-118, OATM-BR-119.
- SME-062: What should the account update screen do in each of these cases: exit (PF3), first entry before any details are fetched, arriving from the menu, a completed save, a failed save, cancel (PF12), details shown, and answering 'N' to confirmation (PF5)? (Business analyst) On OATM-BR-119.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-117, OATM-BR-118, OATM-BR-119, OATM-BR-120.

### Decision table gaps

None.
