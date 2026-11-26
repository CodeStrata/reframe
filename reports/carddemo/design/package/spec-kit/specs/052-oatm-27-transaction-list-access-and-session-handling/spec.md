# Feature specification: Transaction list access and session handling

**Feature:** OATM-C27 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C27)

As the business, I want the transaction list reachable only within a signed-on session, with clear key handling and return to the main menu, so that users move safely through the screens.

Governs access to the transaction list. Only signed-on users reach it: anyone without a session goes to sign-on. PF3 returns to the main menu, and unsupported keys get 'Invalid key pressed. Please see below...'. Any signed-on user, regular or admin, sees transactions from every account and card. That is current behaviour and the team must confirm it deliberately rather than change it by accident.

**Acceptance scenarios:**

1. **Given** session data length: 0, **when** the transaction list program (COTRN00C) is started without any session data (no commarea), **then** The user is transferred to sign-on (COSGN00C); no list is shown. (OATM-C27-AC-01)
2. **Given** user type: U (regular); user's account: 00000000001, **when** transaction list runs, **then** The list also includes transactions belonging to other accounts and cards. (OATM-C27-AC-02)
3. **Given** key: PF3, **when** the user presses PF3 on the transaction list, **then** The main menu is displayed. (OATM-C27-AC-03)
4. **Given** key: PF5, **when** the user presses any key other than Enter, PF3, PF7 or PF8, **then** Screen redisplayed with 'Invalid key pressed. Please see below...'. (OATM-C27-AC-04)
5. **Given** key: PF8, **when** transaction list runs, **then** After page 2 is shown, the next key press returns to the transaction list with page 2 remembered. (OATM-C27-AC-05)

## Requirements

### Functional requirements

- **OATM-REQ-N-008** (business rule): When the transaction list program (COTRN00C) is started without any session data (no commarea), the system shall transfer the user to the sign-on program 'COSGN00C'. Rules: OATM-BR-234.
- **OATM-REQ-N-009** (business rule): The system shall show transactions from every account and card in transaction-ID order to any signed-on user, regular or admin, without limiting them to the user's own account or checking user type. Rules: OATM-BR-235.
- **OATM-REQ-F-224** (business rule): When the user presses PF3 on the transaction list, the system shall return the user to the main menu program 'COMEN01C'. Rules: OATM-BR-236.
- **OATM-REQ-F-225** (business rule): If the user presses any key other than Enter, PF3, PF7 or PF8 on the transaction list, then the system shall redisplay the screen with the message 'Invalid key pressed. Please see below...' and the cursor on the transaction ID field. Rules: OATM-BR-237.
- **OATM-REQ-N-010** (design note): The system shall end every transaction list interaction by waiting for the next user input under transaction 'CT00', keeping the session data (page position, selection, user) for the next screen. Rules: OATM-BR-238.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-234 | Transaction list screen navigation and session routing | business rule | WHEN the transaction list program (COTRN00C) is started without any session data (no commarea), THE transaction list SHALL transfer the user to the sign-on program 'COSGN00C'. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-235 | Transaction list visible to any signed-on user (no account scoping) | business rule | THE transaction list SHALL show transactions from every account and card in transaction-ID order to any signed-on user, regular or admin, without limiting them to the user's own account or checking user type. | medium | app/cbl/COTRN00C.cbl:591-600, app/cbl/COTRN00C.cbl:279-325, app/cpy/COMEN02Y.cpy:55-58, app/cbl/COMEN01C.cbl:136-141 |
| OATM-BR-236 | Transaction list screen navigation and session routing | business rule | WHEN the user presses PF3 on the transaction list, THE transaction list SHALL return the user to the main menu program 'COMEN01C'. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-237 | Reject unsupported key | business rule | WHEN the user presses any key other than Enter, PF3, PF7 or PF8, THE transaction list SHALL redisplay the screen with the message 'Invalid key pressed. Please see below...' and the cursor on the transaction ID field. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-238 | Transaction list screen navigation and session routing | design note | THE transaction list SHALL end every interaction by waiting for the next user input under transaction 'CT00', keeping the session data (page position, selection, user) for the next screen. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |

### Key entities

- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-164: When the operator pages back through the transaction list, the page number is reset to 1 "otherwise". Which situation triggers that reset: when the look-back read failed or the page number is already 1 or less, when no next page is flagged as available, or both? (Business analyst) On OATM-BR-237.
- SME-165: The transaction list only describes how transactions are placed in rows 1 and 10. How should transactions be placed in rows 2 through 9? (Business analyst) On OATM-BR-237.
- SME-166: On the transaction list, how is the next screen chosen when the operator selects a transaction, what should PF3 do, and what should happen when the list is opened without any information from a calling screen? (Application owner) On OATM-BR-237.
- SME-167: When the operator presses PF8 (next page) and no last transaction ID is held, the list currently starts after the highest possible key, which probably shows an empty page. Should the new system keep this behaviour? (Business analyst) On OATM-BR-237.
- SME-168: Should any signed-on user, including regular users, be able to list and open every transaction in the system, or should each user see only the transactions for their own account or cards? (Security/compliance officer) On OATM-BR-235.
- DEF-177: Confirm this is deliberate: Any regular user can see all customers' transactions (card-holder data) because the list is not scoped to the user's account. (Subject-matter expert) On OATM-BR-235.

### Decision table gaps

None.
