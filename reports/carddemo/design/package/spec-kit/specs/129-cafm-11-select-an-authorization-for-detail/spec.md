# Feature specification: Select an authorization for detail

**Feature:** CAFM-C11 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C11)

As a customer service operator, I want to mark one listed authorization with 'S' to open its details, so that I can examine a specific authorization.

Lets a customer service operator mark one listed authorization with 'S' (or 's') to open its details on the Authorization details screen. Only the first marked row from the top counts. Any other selection code shows 'Invalid selection. Valid value is S' and the list is redisplayed, never an unintended record.

**Acceptance scenarios:**

1. **Given** Account ID: 00000000001; Row 3 selection: S; Row 5 selection: S, **when** Enter is pressed with a numeric account number, **then** Row 3's code and authorization key are recorded (CAFM-C11-AC-01)
2. **Given** Account ID: 00000000001; Row selections: all blank, **when** Enter is pressed with a numeric account number, **then** No selection is recorded and the list is redisplayed (CAFM-C11-AC-02)
3. **Given** Account ID: 00000000001; Row 3 selection: s, **when** the recorded selection code is 'S' or 's' and the row holds an authorization key, **then** The detail screen (COPAUS1C) opens for row 3's authorization (CAFM-C11-AC-03)
4. **Given** Account ID: 00000000001; Row 3 selection: X, **when** the recorded selection code is anything other than 'S' or 's', **then** Message 'Invalid selection. Valid value is S' is shown with the list (CAFM-C11-AC-04)

## Requirements

### Functional requirements

- **CAFM-REQ-F-109** (business rule): When Enter is pressed with a numeric account number, the system shall take the first of the five list rows, from top to bottom, that has a selection code and record that code and the row's authorization key, and if no row is marked shall clear the selection. Rules: CAFM-BR-115.
- **CAFM-REQ-F-110** (business rule): When the recorded selection code is 'S' or 's' and the row holds an authorization key, the system shall pass control to the authorization detail program COPAUS1C with that key, recording COPAUS0C and transaction CPVS as where the user came from. Rules: CAFM-BR-116.
- **CAFM-REQ-F-111** (business rule): If the recorded selection code is anything other than 'S' or 's', then the system shall show 'Invalid selection. Valid value is S' and redisplay the account's authorization list. Rules: CAFM-BR-117.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-115 | Capture selected pending authorization | business rule | WHEN Enter is pressed with a numeric account number, THE Pending Authorization View SHALL take the first of the five list rows, from top to bottom, that has a selection code, and record that code and the row's authorization key; if no row is marked it SHALL clear the selection. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:264-283, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:285-332, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:337, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:33-36 |
| CAFM-BR-116 | Open details for selected authorization | business rule | WHEN the recorded selection code is 'S' or 's' and the row holds an authorization key, THE Pending Authorization View SHALL pass control to the authorization detail program COPAUS1C with that key, recording this program (COPAUS0C) and transaction CPVS as where the user came from. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:264-283, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:285-332, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:337, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:33-36 |
| CAFM-BR-117 | Reject invalid selection code | business rule | WHEN the recorded selection code is anything other than 'S' or 's', THE Pending Authorization View SHALL show 'Invalid selection. Valid value is S' and redisplay the account's authorization list. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:264-283, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:285-332, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:337, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:33-36 |

### Key entities

- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSMSG02Y (working storage)
- CVACT02Y (working storage)

### Needs clarification

- SME-137: On the pending-authorizations list screen, the PF3 (exit) key is accepted but nothing says what it does. Where should PF3 take the user? (Business analyst) On CAFM-BR-115, CAFM-BR-116, CAFM-BR-117.
- SME-138: When an account typed on the pending-authorizations screen has no card cross-reference, account record or customer record, a 'not found' message appears but the inquiry carries on. Should a missing record stop the inquiry so no authorization list is shown, or should the screen still show whatever authorization data exists for that account ID? (Customer service operations lead) On CAFM-BR-115, CAFM-BR-116, CAFM-BR-117.
- SME-139: When a page of pending authorizations is full, the system reads one more record ahead. What rule should decide that there is a next page, so that forward paging (PF8) is allowed? (Business analyst) On CAFM-BR-115, CAFM-BR-116, CAFM-BR-117.
- SME-140: Please confirm: when the card cross-reference lookup succeeds, the account ID and customer ID it returns are the ones used to look up the account and the customer. (Business analyst) On CAFM-BR-115, CAFM-BR-116, CAFM-BR-117.

### Decision table gaps

- Authorization row selection: No rule says what happens when 'S' is entered on a row with no authorization.
- Authorization row selection: Only the first marked row is used; no rule says whether the operator is told other marks were ignored.
