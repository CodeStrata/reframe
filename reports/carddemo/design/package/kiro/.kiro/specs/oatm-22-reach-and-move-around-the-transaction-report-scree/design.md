# Design: Reach and move around the transaction report screen (OATM-C22)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Handles reaching and leaving the transaction report screen for signed-on users. Without a session it sends them to sign-on, PF3 returns to the main menu, Enter processes the request, and any other key gets 'Invalid key pressed. Please see below...'. It must never allow report requests outside a valid signed-on session.

Runs as online. Journeys: J06.

## Screens and components

### Transaction reports (S-REPORT-REQUEST)

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Submit for printing | button | Checks the request, then opens the confirmation |  |  | OATM-REQ-F-173, OATM-REQ-F-175, OATM-REQ-F-176 |
| Back | link |  |  | S-APP-SHELL | OATM-REQ-F-174, OATM-REQ-N-007 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| CardDemo | header | Application name and titles (legacy TITLE01/TITLE02), the signed-on user, and today's date and time (legacy CURDATE/CURTIME); a user with no session is sent to sign-on |  |  | OATM-REQ-N-007 |


## Data models

- COCOM01Y (working storage of CORPT00C): see data-contracts.md.
- COTTL01Y (working storage of CORPT00C): see data-contracts.md.
- CSDAT01Y (working storage of CORPT00C): see data-contracts.md.
- CSMSG01Y (working storage of CORPT00C): see data-contracts.md.
- CVTRA05Y (working storage of CORPT00C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-181 | Report screen navigation and session guard | business rule | WHEN the transaction report program (CR00) starts with no session data, THE transaction report screen SHALL send the user to the sign-on screen (COSGN00C). | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-182 | Report screen navigation and session guard | formatting | WHEN the user first arrives at the transaction report screen from another screen, THE transaction report screen SHALL show an empty report screen with the cursor on Monthly. | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-183 | Report screen navigation and session guard | formatting | WHEN the user presses PF3 on the transaction report screen, THE transaction report screen SHALL return to the main menu (COMEN01C). | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-184 | Report screen navigation and session guard | business rule | WHEN the user presses Enter on the transaction report screen, THE transaction report screen SHALL process the report request. | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-185 | Report screen navigation and session guard | business rule | WHEN the user presses any key other than Enter or PF3, THE transaction report screen SHALL show 'Invalid key pressed. Please see below...' with the cursor on Monthly. | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |

### Worked examples

- OATM-BR-181: Session data = none → User is transferred to sign-on program COSGN00C
- OATM-BR-182: Arriving from = Main menu option 9 'Transaction Reports' → Empty report screen shown, cursor on Monthly
- OATM-BR-183: Key pressed = PF3 → Main menu COMEN01C is shown
- OATM-BR-184: Key pressed = Enter; Monthly = X → Monthly report request is processed
- OATM-BR-185: Key pressed = PF5 → Message 'Invalid key pressed. Please see below...' shown

## Decision tables

#### Transaction report screen key handling

| Key pressed | Screen action | Rule |
|---|---|---|
| PF3 | Return to the main menu (COMEN01C) | OATM-BR-183 |
| Enter | Process the report request | OATM-BR-184 |
| Any other key | Show 'Invalid key pressed. Please see below...' with the cursor on Monthly | OATM-BR-185 |


## Design notes

None.

## Open questions

None.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).