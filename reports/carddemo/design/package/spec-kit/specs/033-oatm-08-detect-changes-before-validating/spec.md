# Feature specification: Detect changes before validating

**Feature:** OATM-C08 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C08)

As an operator, I want the system to check my entries only when I have actually changed something, so that unchanged details are not re-validated or saved.

Compares what the operator entered against the values fetched and runs field checks only when something has actually changed and the update is not already awaiting confirmation or saved. Text is compared ignoring case and surrounding spaces; numbers, dates and codes exactly. It must never re-validate or save unchanged details, and shows 'No change detected with respect to values fetched.' instead.

**Acceptance scenarios:**

1. **Given** Fetched last name: SMITH; Entered last name: smith, **when** the operator presses Enter on an account already shown, **then** No change is counted (OATM-C08-AC-01)
2. **Given** Fetched last name: SMITH; Entered last name: SMYTH, **when** the operator presses Enter on an account already shown, **then** A change is counted (OATM-C08-AC-02)
3. **Given** Fetched credit limit: 5000.00; Entered credit limit: 5500.00, **when** the operator presses Enter on an account already shown, **then** A change is counted (OATM-C08-AC-03)
4. **Given** Fetched status: Y; Entered status: y; Other fields: unchanged, **when** no entered value differs from the fetched values, **then** Message 'No change detected with respect to values fetched.'; nothing validated or saved (OATM-C08-AC-04)
5. **Given** Change detected: yes; Update state: details shown ('S'); All fields valid: yes, **when** a change is detected and the update is neither awaiting confirmation ('N') nor completed ('C'), **then** State becomes 'N' and the operator is asked to confirm (OATM-C08-AC-05)
6. **Given** Change detected: yes; Update state: details shown ('S'); FICO entered: 900, **when** a change is detected and the update is neither awaiting confirmation ('N') nor completed ('C'), **then** State stays 'E' and the field error is shown (OATM-C08-AC-06)
7. **Given** Changes made: none, **when** several fields fail validation, **then** No Y/N check is made (OATM-C08-AC-07)
8. **Given** Update state: 'N' (awaiting confirmation); Key pressed: Enter, **when** no change is detected, or the update is awaiting confirmation ('N') or completed ('C'), **then** No field is re-checked and no field is highlighted as in error (OATM-C08-AC-08)

## Requirements

### Functional requirements

- **OATM-REQ-F-068** (business rule): When the operator presses Enter on an account already shown, the system shall compare every entered value with the value fetched, ignoring upper/lower case and surrounding spaces for text fields (status, group, names, address, state, country, ZIP, government ID, primary-holder flag) and comparing amounts, dates, phone parts, SSN, EFT account and FICO exactly, counting any difference as a change. Rules: OATM-BR-067.
- **OATM-REQ-F-069** (business rule): When no entered value differs from the fetched values, the system shall show 'No change detected with respect to values fetched.', run no field checks, save nothing and leave the details on screen without asking for confirmation. Rules: OATM-BR-068.
- **OATM-REQ-F-070** (business rule): While the update is neither awaiting confirmation ('N') nor completed ('C'), when a change is detected, the system shall mark the changes as not yet accepted ('E'), run every field check, and move the update to awaiting confirmation ('N') if all checks pass. Rules: OATM-BR-069, OATM-BR-070, OATM-BR-071.
- **OATM-REQ-F-071** (design note): When no change is detected, or the update is awaiting confirmation ('N') or completed ('C'), the system shall clear all field error flags and skip every field check, including the date checks. Rules: OATM-BR-072.
- **OATM-REQ-F-072** (business rule): When several fields fail validation, the system shall flag every invalid field but show only the message of the first failing field. Rules: OATM-BR-070, OATM-BR-071, OATM-BR-073.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-067 | Detect changes between old and new details | business rule | WHEN the operator presses Enter on an account already shown, THE account update SHALL compare every entered value with the value fetched, ignoring upper/lower case and surrounding spaces for text fields (status, group, names, address, state, country, ZIP, government ID, primary-holder flag) and comparing amounts, dates, phone parts, SSN, EFT account and FICO exactly; any difference counts as a change. | high | app/cbl/COACTUPC.cbl:1429-1470, app/cbl/COACTUPC.cbl:1670-1675, app/cbl/COACTUPC.cbl:1681-1779, app/cbl/COACTUPC.cbl:165-170 |
| OATM-BR-068 | Detect changes against fetched values | business rule | WHEN no entered value differs from the fetched values, THE account update SHALL show 'No change detected with respect to values fetched.', run no field checks, save nothing and leave the details on screen without asking for confirmation. | high | app/cbl/COACTUPC.cbl:1429-1470, app/cbl/COACTUPC.cbl:1670-1675, app/cbl/COACTUPC.cbl:1681-1779, app/cbl/COACTUPC.cbl:165-170 |
| OATM-BR-069 | Gate validation on detected changes | business rule | WHEN a change is detected and the update is neither awaiting confirmation ('N') nor completed ('C'), THE account update SHALL mark the changes as not yet accepted ('E') and run every field check; if all checks pass it SHALL move the update to awaiting confirmation ('N'). | high | app/cbl/COACTUPC.cbl:1429-1470, app/cbl/COACTUPC.cbl:1670-1675, app/cbl/COACTUPC.cbl:1681-1779, app/cbl/COACTUPC.cbl:165-170 |
| OATM-BR-070 | Require mandatory text present | business rule | WHEN the account update checks the operator's changes, THE account update SHALL show only the first error message found, while still flagging every invalid field, and it SHALL run these checks only when the operator has changed something that is not yet awaiting confirmation. | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-071 | Yes/No flags: account active status and primary cardholder | business rule | WHEN several fields fail validation, THE Account Update screen SHALL show only the message of the first failing field, and SHALL run these Y/N checks only after the account has been fetched and the operator has changed at least one value. | high | app/cbl/COACTUPC.cbl:1064-1070, app/cbl/COACTUPC.cbl:1419-1424, app/cbl/COACTUPC.cbl:1458-1476, app/cbl/COACTUPC.cbl:1657-1662 |
| OATM-BR-072 | Skip edits when nothing changed | design note | WHEN no change is detected, or the update is awaiting confirmation ('N') or completed ('C'), THE account update SHALL clear all field error flags and skip every field check, including the date checks. | high | app/cbl/COACTUPC.cbl:1429-1470, app/cbl/COACTUPC.cbl:1670-1675, app/cbl/COACTUPC.cbl:1681-1779, app/cbl/COACTUPC.cbl:165-170 |
| OATM-BR-073 | Validate phone area code | formatting | WHEN more than one phone number part fails its checks, THE Account Update SHALL flag every failing part in error but show only the first message raised on the screen (no later message replaces one already set). | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |

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

- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-070, OATM-BR-073.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-070, OATM-BR-073.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-070, OATM-BR-073.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-070.
- DEF-039: Confirm this is deliberate: Text fields are compared ignoring case and surrounding spaces, so a correction that only changes capitalisation (for example 'smith' to 'Smith') counts as no change and cannot be saved. (Subject-matter expert) On OATM-BR-067, OATM-BR-068, OATM-BR-069, OATM-BR-072.
- DEF-041: Is this intended? The 'phone not supplied' test checks the area code twice and never checks that the line number is blank-spaces (third condition tests area code = spaces OR line number = low-values). Because the screen input turns blanks into low-values first, this has no visible effect today, but a number arriving with a spaces area code and prefix would be accepted as omitted even with a line number entered. (Subject-matter expert) On OATM-BR-073.

### Decision table gaps

None.
