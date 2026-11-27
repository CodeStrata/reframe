# Feature specification: Access to transaction type maintenance

**Feature:** TTRDM-C06 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C06)

As a security officer, I want to know how access to transaction type update and delete is controlled, so that only authorised users can change reference data.

This records how access to transaction type update and delete works today: when the list is started directly with no sign-on context, the user is treated as an administrator, and update or delete is never checked against the user's type. The new application must not copy this gap silently; who may change transaction type reference data needs an explicit decision and enforcement.

**Acceptance scenarios:**

1. **Given** Start: CTLI typed at a blank terminal; Signed-on user type: none, **when** transaction CTLI is started directly with no carried sign-on context, **then** The full list/update/delete screen is shown and the user is treated as 'A' (TTRDM-C06-AC-01)
2. **Given** Carried user type: 'U'; Action: D on a row, then F10, **when** Transaction Type List screen runs, **then** The delete is carried out; user type is not checked (TTRDM-C06-AC-02)

## Requirements

### Functional requirements

- **TTRDM-REQ-N-002** (business rule): When transaction CTLI is started directly with no carried sign-on context, the system shall mark the user as an administrator (user type 'A') and offer list, update and delete without checking who signed on. Rules: TTRDM-BR-059.
- **TTRDM-REQ-N-003** (business rule): The system shall not check the user type before allowing updates or deletes of transaction types on the Transaction Type List screen. Rules: TTRDM-BR-060.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-059 | Screen assumes admin user type without checking | business rule | WHEN transaction CTLI is started directly with no carried sign-on context, THE Transaction Type List screen SHALL mark the user as an administrator (user type 'A') and offer list, update and delete without checking who signed on. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:515-532, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:611, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:751, app/app-transaction-type-db2/csd/CRDDEMOD.csd:25-26 |
| TTRDM-BR-060 | Screen assumes admin user type without checking | business rule | THE Transaction Type List screen SHALL never check the user type before allowing updates or deletes of transaction types. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:515-532, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:611, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:751, app/app-transaction-type-db2/csd/CRDDEMOD.csd:25-26 |

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSDB2RPY (working storage)
- CSDB2RWY (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVACT02Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-193: Is the transaction-type maintenance screen (transaction CTLI) limited to administrators by system security settings, or should the program itself check that the user is an administrator? (Security officer) On TTRDM-BR-060.
- DEF-169: Confirm this is deliberate: The list/update/delete screen grants administrator status on a direct start of CTLI and never checks the signed-on user type, so any user who can start the transaction can update or delete transaction types. (Subject-matter expert) On TTRDM-BR-060.

### Decision table gaps

None.
