# Implementation plan: Reach and move around the transaction report screen (OATM-C22)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

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


## Data model

- COCOM01Y (working storage of CORPT00C): see data-contracts.md.
- COTTL01Y (working storage of CORPT00C): see data-contracts.md.
- CSDAT01Y (working storage of CORPT00C): see data-contracts.md.
- CSMSG01Y (working storage of CORPT00C): see data-contracts.md.
- CVTRA05Y (working storage of CORPT00C): see data-contracts.md.

## Design notes

None.

## Decision tables

#### Transaction report screen key handling

| Key pressed | Screen action | Rule |
|---|---|---|
| PF3 | Return to the main menu (COMEN01C) | OATM-BR-183 |
| Enter | Process the report request | OATM-BR-184 |
| Any other key | Show 'Invalid key pressed. Please see below...' with the cursor on Monthly | OATM-BR-185 |

