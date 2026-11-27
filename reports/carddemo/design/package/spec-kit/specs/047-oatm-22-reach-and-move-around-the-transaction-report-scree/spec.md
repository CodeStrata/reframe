# Feature specification: Reach and move around the transaction report screen

**Feature:** OATM-C22 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C22)

As a signed-on user, I want to open the transaction report screen, leave it, and be told when I press a key it does not support, so that I can ask for reports only within a valid session.

Controls access to the transaction report screen and movement on it. Only a signed-on user may reach it, and a request without a session is sent to sign-on. PF3 returns to the main menu, Enter processes the request, and any other key is rejected with 'Invalid key pressed. Please see below...'. A report must never be requested outside a valid session.

**Acceptance scenarios:**

1. **Given** Session data: none, **when** the transaction report program (CR00) starts with no session data, **then** User is transferred to sign-on program COSGN00C (OATM-C22-AC-01)
2. **Given** Arriving from: Main menu option 9 'Transaction Reports', **when** the user first arrives at the transaction report screen from another screen, **then** Empty report screen shown, cursor on Monthly (OATM-C22-AC-02)
3. **Given** Key pressed: PF3, **when** the user presses PF3 on the transaction report screen, **then** Main menu COMEN01C is shown (OATM-C22-AC-03)
4. **Given** Key pressed: Enter; Monthly: X, **when** the user presses Enter on the transaction report screen, **then** Monthly report request is processed (OATM-C22-AC-04)
5. **Given** Key pressed: PF5, **when** the user presses any key other than Enter or PF3, **then** Message 'Invalid key pressed. Please see below...' shown (OATM-C22-AC-05)

## Requirements

### Functional requirements

- **OATM-REQ-N-007** (business rule): When the transaction report program (CR00) starts with no session data, the system shall send the user to the sign-on screen (COSGN00C). Rules: OATM-BR-181.
- **OATM-REQ-F-173** (formatting): When the user first arrives at the transaction report screen from another screen, the system shall show an empty report screen with the cursor on Monthly. Rules: OATM-BR-182.
- **OATM-REQ-F-174** (formatting): When the user presses PF3 on the transaction report screen, the system shall return to the main menu (COMEN01C). Rules: OATM-BR-183.
- **OATM-REQ-F-175** (business rule): When the user presses Enter on the transaction report screen, the system shall process the report request. Rules: OATM-BR-184.
- **OATM-REQ-F-176** (business rule): If the user presses any key other than Enter or PF3 on the transaction report screen, then the system shall show 'Invalid key pressed. Please see below...' with the cursor on Monthly. Rules: OATM-BR-185.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-181 | Report screen navigation and session guard | business rule | WHEN the transaction report program (CR00) starts with no session data, THE transaction report screen SHALL send the user to the sign-on screen (COSGN00C). | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-182 | Report screen navigation and session guard | formatting | WHEN the user first arrives at the transaction report screen from another screen, THE transaction report screen SHALL show an empty report screen with the cursor on Monthly. | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-183 | Report screen navigation and session guard | formatting | WHEN the user presses PF3 on the transaction report screen, THE transaction report screen SHALL return to the main menu (COMEN01C). | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-184 | Report screen navigation and session guard | business rule | WHEN the user presses Enter on the transaction report screen, THE transaction report screen SHALL process the report request. | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-185 | Report screen navigation and session guard | business rule | WHEN the user presses any key other than Enter or PF3, THE transaction report screen SHALL show 'Invalid key pressed. Please see below...' with the cursor on Monthly. | medium | app/cbl/CORPT00C.cbl:172-197, app/cbl/CORPT00C.cbl:540-551, app/cpy/CSMSG01Y.cpy:20-21 |

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CVTRA05Y (working storage)

### Needs clarification

None.

### Decision table gaps

None.
