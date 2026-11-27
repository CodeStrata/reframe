# Feature specification: Update account details with validation and confirmation

**Feature:** OATM-C15 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C15)

As an operator, I want my changes to account details checked and then saved only when I confirm them with PF5, so that only validated changes reach the account record and I know whether the save succeeded.

Lets an operator change an account's and its customer's details. Every changed value is checked, and a save happens only after the operator explicitly confirms with PF5. Changes that fail a check, or that are not confirmed, must never be saved. The operator must always be told whether there was nothing to change, whether the changes were validated, or whether the save was committed or failed.

**Acceptance scenarios:**

1. **Given** credit limit: changed from 5000.00 to 7000.00; all other fields: valid, **when** details are shown and the operator changes one or more values, **then** State 'N'; message 'Changes validated.Press F5 to save' (OATM-C15-AC-01)
2. **Given** account status: changed to 'X', **when** details are shown and the operator changes one or more values, **then** State 'E'; an error message is shown and nothing can be saved (OATM-C15-AC-02)
3. **Given** update state: 'S'; screen values: same as fetched, **when** details are shown and the operator submits without changing any value, **then** State stays 'S'; message 'No change detected with respect to values fetched.' (OATM-C15-AC-03)
4. **Given** update state: 'N'; key: Enter, **when** the state is changes not OK ('E'), or validated changes ('N') are submitted without PF5, **then** Nothing saved; state stays 'N' with 'Changes validated.Press F5 to save' (OATM-C15-AC-04)
5. **Given** update state: 'N'; key: PF5; record: unchanged by others, lock and update succeed, **when** validated changes ('N') are confirmed with PF5, **then** State 'C' (OATM-C15-AC-05)
6. **Given** update state: 'N'; key: PF5; record: changed by another user since it was read, **when** validated changes ('N') are confirmed with PF5, **then** State 'S'; the details are shown again (OATM-C15-AC-06)
7. **Given** save outcome: success, **when** a save completes ('C'), **then** Message 'Changes committed to database' (OATM-C15-AC-07)

## Requirements

### Functional requirements

- **OATM-REQ-F-118** (business rule): While details are shown, when the operator changes one or more values, the system shall check every field and set the state to 'N' with the message 'Changes validated.Press F5 to save' if no check fails, or to 'E' (changes not OK) if any check fails. Rules: OATM-BR-121.
- **OATM-REQ-F-119** (business rule): While details are shown, when the operator submits without changing any value, the system shall keep the details shown (state 'S') and report 'No change detected with respect to values fetched.'. Rules: OATM-BR-122.
- **OATM-REQ-F-120** (business rule): When the state is changes not OK ('E'), or validated changes ('N') are submitted without PF5, the system shall save nothing and show the details again for correction or confirmation. Rules: OATM-BR-123.
- **OATM-REQ-F-121** (business rule): When validated changes ('N') are confirmed with PF5, the system shall save them and set the state to 'L' if the account cannot be locked, 'F' if the locked update fails, 'S' (details shown again) if someone else changed the record since it was read, or 'C' otherwise. Rules: OATM-BR-124.
- **OATM-REQ-F-122** (formatting): When a save completes ('C'), the system shall show the message 'Changes committed to database'. Rules: OATM-BR-125.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-121 | Cross-check state and ZIP, set verdict | business rule | WHEN details are shown and the operator changes one or more values, THE account update screen SHALL check every field and SHALL set the state to 'N' with the message 'Changes validated.Press F5 to save' if no check fails, or to 'E' (changes not OK) if any check fails. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-122 | Request confirmation for valid changes | business rule | WHEN details are shown and the operator submits without changing any value, THE account update screen SHALL keep the details shown (state 'S') and report 'No change detected with respect to values fetched.'. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-123 | Redisplay when edits fail or confirmation pending | business rule | WHEN the state is changes not OK ('E'), or validated changes ('N') are submitted without PF5, THE account update screen SHALL save nothing and show the details again for correction or confirmation. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-124 | Save confirmed changes and record outcome | business rule | WHEN validated changes ('N') are confirmed with PF5, THE account update screen SHALL save them and set the state to 'L' if the account cannot be locked, 'F' if the locked update fails, 'S' (details shown again) if someone else changed the record since it was read, or 'C' otherwise. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-125 | Confirm successful update commit | formatting | WHEN a save completes ('C'), THE account update screen SHALL show the message 'Changes committed to database'. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

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

- SME-054: When saving an account update, a failure to lock the customer record is reported as a successful save. Is that intended, or should it be reported as a lock error? (Account servicing business owner) On OATM-BR-122, OATM-BR-123, OATM-BR-124.
- SME-062: What should the account update screen do in each of these cases: exit (PF3), first entry before any details are fetched, arriving from the menu, a completed save, a failed save, cancel (PF12), details shown, and answering 'N' to confirmation (PF5)? (Business analyst) On OATM-BR-123.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-121, OATM-BR-122, OATM-BR-123, OATM-BR-124, OATM-BR-125.

### Decision table gaps

- Account update outcome by state, key and save result: No rule says what happens on the next submission after a failed lock ('L'), failed update ('F') or completed save ('C').
