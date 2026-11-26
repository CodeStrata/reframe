# Feature specification: Select a transaction from the list to view its details

**Feature:** OATM-C26 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C26)

As a signed-on user, I want to mark a transaction in the list with 'S' and open its details, so that I can look at one transaction closely.

Lets a signed-on user mark one row of the transaction list with 'S' and open that transaction's details. Only the first marked row, top to bottom, counts. Any code other than 'S' or 's' is rejected with 'Invalid selection. Valid value is S', and no transaction is ever opened when no row is marked.

**Acceptance scenarios:**

1. **Given** Row 3 selection: S; Row 3 transaction ID: 0000000000000042; Rows 1-2 selection: blank, **when** the user presses Enter on the transaction list, **then** Row 3 is taken: selection 'S', transaction 0000000000000042 (OATM-C26-AC-01)
2. **Given** Row 2 selection: S; Row 7 selection: S, **when** the user presses Enter on the transaction list, **then** Only row 2 is taken; row 7 is ignored (OATM-C26-AC-02)
3. **Given** All row selections: blank, **when** the user presses Enter on the transaction list, **then** No selection is recorded; the list is refreshed (OATM-C26-AC-03)
4. **Given** Row 3 selection: s; Row 3 transaction ID: 0000000000000042, **when** the taken row's selection code is 'S' or 's' and the row has a transaction ID, **then** Transaction Detail (COTRN01C) opens for transaction 0000000000000042 (OATM-C26-AC-04)
5. **Given** Row 3 selection: X; Row 3 transaction ID: 0000000000000042, **when** the taken row's selection code is anything other than 'S' or 's', **then** Message 'Invalid selection. Valid value is S'; the list is shown again (OATM-C26-AC-05)
6. **Given** selection column on all rows: blank; key: Enter, **when** Enter is processed and none of the 10 list rows has a selection code, **then** No transaction is opened; the selection is cleared and the list is shown again. (OATM-C26-AC-06)

## Requirements

### Functional requirements

- **OATM-REQ-F-220** (business rule): When the user presses Enter on the transaction list, the system shall take the first of the ten rows, top to bottom, whose selection field is not blank, recording that row's selection code and transaction ID (CDEMO-CT00-TRN-SEL-FLG, CDEMO-CT00-TRN-SELECTED) and ignoring any later marked rows. Rules: OATM-BR-230.
- **OATM-REQ-F-221** (business rule): When the taken row's selection code is 'S' or 's' and the row has a transaction ID, the system shall pass that transaction ID to the Transaction Detail program (COTRN01C) as a fresh entry (context 0), recording the list screen (CT00, COTRN00C) as the caller. Rules: OATM-BR-231.
- **OATM-REQ-F-222** (business rule): If the taken row's selection code is anything other than 'S' or 's', then the system shall show the message 'Invalid selection. Valid value is S', place the cursor on the transaction ID search field and redisplay the list. Rules: OATM-BR-232.
- **OATM-REQ-F-223** (design note): When Enter is processed and none of the 10 list rows has a selection code, the system shall clear any remembered selection code and selected transaction ID, so no transaction is opened and the list is redisplayed. Rules: OATM-BR-233.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-230 | Capture selection from first list row | business rule | WHEN the user presses Enter on the transaction list, THE Transaction List SHALL take the first of the ten rows, top to bottom, whose selection field is not blank, recording that row's selection code and transaction ID (CDEMO-CT00-TRN-SEL-FLG, CDEMO-CT00-TRN-SELECTED) and ignoring any later marked rows. | high | app/cbl/COTRN00C.cbl:146-181, app/cbl/COTRN00C.cbl:182-204, app/cbl/COTRN00C.cbl:221-225, app/cbl/COTRN00C.cbl:36-37 |
| OATM-BR-231 | Open details for selected transaction | business rule | WHEN the taken row's selection code is 'S' or 's' and the row has a transaction ID, THE Transaction List SHALL pass that transaction ID to the Transaction Detail program (COTRN01C) as a fresh entry (context 0), recording the list screen (CT00, COTRN00C) as the caller. | high | app/cbl/COTRN00C.cbl:146-181, app/cbl/COTRN00C.cbl:182-204, app/cbl/COTRN00C.cbl:221-225, app/cbl/COTRN00C.cbl:36-37 |
| OATM-BR-232 | Reject invalid selection code | business rule | WHEN the taken row's selection code is anything other than 'S' or 's', THE Transaction List SHALL show the message 'Invalid selection. Valid value is S', place the cursor on the transaction ID search field and redisplay the list. | high | app/cbl/COTRN00C.cbl:146-181, app/cbl/COTRN00C.cbl:182-204, app/cbl/COTRN00C.cbl:221-225, app/cbl/COTRN00C.cbl:36-37 |
| OATM-BR-233 | Clear selection when no row chosen | design note | WHEN Enter is processed and none of the 10 list rows has a selection code, THE transaction list SHALL clear any remembered selection code and selected transaction ID, so no transaction is opened and the list is redisplayed. | medium | app/cbl/COTRN00C.cbl:146-183, app/cbl/COTRN00C.cbl:184-186 |

### Key entities

- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-164: When the operator pages back through the transaction list, the page number is reset to 1 "otherwise". Which situation triggers that reset: when the look-back read failed or the page number is already 1 or less, when no next page is flagged as available, or both? (Business analyst) On OATM-BR-233, OATM-BR-230, OATM-BR-231, OATM-BR-232.
- SME-165: The transaction list only describes how transactions are placed in rows 1 and 10. How should transactions be placed in rows 2 through 9? (Business analyst) On OATM-BR-233, OATM-BR-230, OATM-BR-231, OATM-BR-232.
- SME-166: On the transaction list, how is the next screen chosen when the operator selects a transaction, what should PF3 do, and what should happen when the list is opened without any information from a calling screen? (Application owner) On OATM-BR-233, OATM-BR-230, OATM-BR-231, OATM-BR-232.
- SME-167: When the operator presses PF8 (next page) and no last transaction ID is held, the list currently starts after the highest possible key, which probably shows an empty page. Should the new system keep this behaviour? (Business analyst) On OATM-BR-233, OATM-BR-230, OATM-BR-231, OATM-BR-232.
- DEF-049: Is this intended? When a selection code is typed on a row with no transaction ID, the selection is silently ignored with no message; and when several rows are marked only the first is acted on, also without a message. (Subject-matter expert) On OATM-BR-230, OATM-BR-231, OATM-BR-232.

### Decision table gaps

- Row selection on Enter: No rule states what happens when 'S' is entered on a row with no transaction ID.
