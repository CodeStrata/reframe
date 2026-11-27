# Feature specification: Select a user to update or delete

**Feature:** USPM-C03 · User Security Profile Management · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (USPM-C03)

As an administrator, I want to mark a user on the list with an action code, so that I am taken to the update or delete screen for that user.

Lets an administrator mark one user on the list with 'U' to open the update screen or 'D' to open the delete screen for that user. Only the first marked row counts, and any other code is rejected with a message. It must never open an update or delete screen for a user the administrator did not mark, or for a code other than U/D.

**Acceptance scenarios:**

1. **Given** Row 3 selection: 'd'; Row 3 user ID: USER0003, **when** the operator presses Enter on the user list and one or more of the 10 rows has a selection code entered, **then** The pending selection is 'd' for user USER0003 (USPM-C03-AC-01)
2. **Given** Row 2 selection: 'U'; Row 2 user ID: USER0002; Row 7 selection: 'D'; Row 7 user ID: USER0007, **when** the operator presses Enter on the user list and one or more of the 10 rows has a selection code entered, **then** Only row 2 is used: the pending selection is 'U' for USER0002 and the row 7 mark is ignored (USPM-C03-AC-02)
3. **Given** Selection in rows 1-10: all blank, **when** the user list is submitted with no selection code in any of the ten rows, **then** No user screen is opened; the list is shown again from the search user ID (USPM-C03-AC-03)
4. **Given** Rows 1-10 selection: blank, **when** the operator presses Enter and no row has a selection code entered, **then** The pending selection and selected user are cleared to blanks, and no transfer takes place (USPM-C03-AC-04)
5. **Given** Selection code: 'u'; Selected user ID: USER0005, **when** the pending selection code is 'U' or 'u' and a user ID was selected, **then** The Update User screen (COUSR02C) opens for USER0005, with the list recorded as 'CU00'/'COUSR00C' to return to (USPM-C03-AC-05)
6. **Given** Selection code: 'd'; Selected user ID: USER0003, **when** the pending selection code is 'D' or 'd' and a user ID was selected, **then** The Delete User screen (COUSR03C) opens for USER0003, with the list recorded as 'CU00'/'COUSR00C' to return to (USPM-C03-AC-06)
7. **Given** Row 3 selection: X; Row 3 user ID: USER0003, **when** a row with a user ID is selected with an action code other than 'U', 'u', 'D' or 'd', **then** Message 'Invalid selection. Valid values are U and D' is shown and the list is redisplayed (USPM-C03-AC-07)
8. **Given** Row 1 selection: u; Row 1 user ID: USER0001, **when** a row with a user ID is selected with an action code other than 'U', 'u', 'D' or 'd', **then** The update user screen (COUSR02C) is opened for USER0001 (USPM-C03-AC-08)

## Requirements

### Functional requirements

- **USPM-REQ-F-034** (business rule): When the operator presses Enter on the user list and one or more of the 10 rows has a selection code entered, the system shall take only the first marked row from the top, saving its selection code and user ID as the pending selection, and ignore marks on later rows. Rules: USPM-BR-038.
- **USPM-REQ-F-035** (design note): When the operator presses Enter and no row has a selection code entered, the system shall clear the pending selection code and selected user ID to blanks so that no update or delete screen is opened, and shall just refresh the list. Rules: USPM-BR-039, USPM-BR-040.
- **USPM-REQ-F-036** (business rule): When the pending selection code is 'U' or 'u' and a user ID was selected, the system shall transfer to the Update User program (COUSR02C), passing the selected user ID with from-transaction 'CU00', from-program 'COUSR00C' and context 0. Rules: USPM-BR-041.
- **USPM-REQ-F-037** (business rule): When the pending selection code is 'D' or 'd' and a user ID was selected, the system shall transfer to the Delete User program (COUSR03C), passing the selected user ID with from-transaction 'CU00', from-program 'COUSR00C' and context 0. Rules: USPM-BR-042.
- **USPM-REQ-F-038** (business rule): If a row with a user ID is selected with an action code other than 'U', 'u', 'D' or 'd', then the system shall not open any user screen, shall show the message 'Invalid selection. Valid values are U and D', and shall place the cursor on the user ID search field. Rules: USPM-BR-043.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-038 | Capture selection from first list row | business rule | WHEN the operator presses Enter on the user list and one or more of the 10 rows has a selection code entered, THE User List SHALL take only the first marked row from the top, saving its selection code and user ID as the pending selection (CDEMO-CU00-USR-SEL-FLG, CDEMO-CU00-USR-SELECTED), and ignore marks on later rows. | high | app/cbl/COUSR00C.cbl:36-37, app/cbl/COUSR00C.cbl:147-185, app/cbl/COUSR00C.cbl:187-210 |
| USPM-BR-039 | Clear selection when no row marked | design note | WHEN the user list is submitted with no selection code in any of the ten rows, THE user list SHALL clear any pending selected action and user (CDEMO-CU00-USR-SEL-FLG, CDEMO-CU00-USR-SELECTED) so that no update or delete screen is opened, and SHALL just refresh the list. | medium | app/cbl/COUSR00C.cbl:152-185, app/cbl/COUSR00C.cbl:187-189, app/cbl/COUSR00C.cbl:218-229 |
| USPM-BR-040 | Row selection action routes to update or delete user | design note | WHEN the operator presses Enter and no row has a selection code entered, THE User List SHALL clear the pending selection code and selected user ID to blanks. | high | app/cbl/COUSR00C.cbl:36-37, app/cbl/COUSR00C.cbl:147-185, app/cbl/COUSR00C.cbl:187-210 |
| USPM-BR-041 | Transfer selected user for update or delete | business rule | WHEN the pending selection code is 'U' or 'u' and a user ID was selected, THE User List SHALL transfer to the Update User program (COUSR02C), passing the selected user ID with from-transaction 'CU00', from-program 'COUSR00C' and context 0. | high | app/cbl/COUSR00C.cbl:36-37, app/cbl/COUSR00C.cbl:147-185, app/cbl/COUSR00C.cbl:187-210 |
| USPM-BR-042 | Transfer selected user for update or delete | business rule | WHEN the pending selection code is 'D' or 'd' and a user ID was selected, THE User List SHALL transfer to the Delete User program (COUSR03C), passing the selected user ID with from-transaction 'CU00', from-program 'COUSR00C' and context 0. | high | app/cbl/COUSR00C.cbl:36-37, app/cbl/COUSR00C.cbl:147-185, app/cbl/COUSR00C.cbl:187-210 |
| USPM-BR-043 | Reject invalid selection action | business rule | WHEN a row with a user ID is selected with an action code other than 'U', 'u', 'D' or 'd', THE user list SHALL not open any user screen, SHALL show the message 'Invalid selection. Valid values are U and D', and SHALL place the cursor on the user ID search field. | medium | app/cbl/COUSR00C.cbl:188-216, app/cbl/COUSR00C.cbl:526 |

### Key entities

- CSUSR01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-209: On the user list, selecting 'U' (update) or 'D' (delete) against a row currently goes to the same place. Which function should handle update requests, and which should handle delete requests? (Business analyst (user security)) On USPM-BR-043, USPM-BR-039, USPM-BR-038, USPM-BR-042.
- SME-210: After paging back through the user list, what page number should be shown? Should it reset to 1 when there is no next page, or only when it cannot go back any further? (Business analyst (user security)) On USPM-BR-043, USPM-BR-039, USPM-BR-038, USPM-BR-042.
- SME-211: What should happen when the operator presses PF3 on the user list? (Business analyst (user security)) On USPM-BR-043, USPM-BR-039, USPM-BR-038, USPM-BR-042.
- SME-212: What should happen when the user list is opened directly, without coming from another screen? (Business analyst (user security)) On USPM-BR-043, USPM-BR-039, USPM-BR-038, USPM-BR-042.
- SME-215: Should the rule that a row selection on the user list routes to update or delete user be treated as top priority (P0)? (Product owner) On USPM-BR-042.
- DEF-155: Is this intended? A selection code typed on an empty row (no user ID) is silently ignored, with no message. (Subject-matter expert) On USPM-BR-043.

### Decision table gaps

- Action on the first marked row: No rule says what happens when a selection code is entered on a row that shows no user ID.
