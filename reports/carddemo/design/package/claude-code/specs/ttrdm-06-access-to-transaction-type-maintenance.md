# Access to transaction type maintenance (TTRDM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk high

## Introduction

This records how access to transaction type update and delete works today: when the list is started directly with no sign-on context, the user is treated as an administrator, and update or delete is never checked against the user's type. The new application must not copy this gap silently; who may change transaction type reference data needs an explicit decision and enforcement.

**User story:** As a security officer, I want to know how access to transaction type update and delete is controlled, so that only authorised users can change reference data.

## Requirements

### Requirement 1: TTRDM-REQ-N-002 (business rule)

#### Acceptance criteria

1. When transaction CTLI is started directly with no carried sign-on context, the system shall mark the user as an administrator (user type 'A') and offer list, update and delete without checking who signed on. (rules TTRDM-BR-059)
2. GIVEN Start: CTLI typed at a blank terminal; Signed-on user type: none WHEN transaction CTLI is started directly with no carried sign-on context THEN The full list/update/delete screen is shown and the user is treated as 'A' (TTRDM-C06-AC-01; TTRDM-BR-059)

### Requirement 2: TTRDM-REQ-N-003 (business rule)

#### Acceptance criteria

1. The system shall not check the user type before allowing updates or deletes of transaction types on the Transaction Type List screen. (rules TTRDM-BR-060)
2. GIVEN Carried user type: 'U'; Action: D on a row, then F10 WHEN Transaction Type List screen runs THEN The delete is carried out; user type is not checked (TTRDM-C06-AC-02; TTRDM-BR-060)

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Application header and navigation (S-APP-SHELL)

New, shared by every screen: the header and navigation shown once, replacing the transaction, program, date, time and title lines every 3270 screen repeated and the numbered main-menu options. A sign-in is required; with no session the user is sent to sign-in. The navigation carries the account in context, so going from an account to Pay balance, Update account or Add transaction keeps it. Tab order: account search, navigation, then the page.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Navigation entry for the transaction type list, shown only to administrators; the server checks the administrator role on every list, add, update and delete instead of assuming it |  | S-TRANTYPE-LIST |  |


## Data models

- COCOM01Y (working storage of COTRTLIC): see data-contracts.md.
- COTTL01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RPY (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RWY (working storage of COTRTLIC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTLIC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTLIC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTLIC): see data-contracts.md.
- CVACT02Y (working storage of COTRTLIC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTLIC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-059 | Screen assumes admin user type without checking | business rule | WHEN transaction CTLI is started directly with no carried sign-on context, THE Transaction Type List screen SHALL mark the user as an administrator (user type 'A') and offer list, update and delete without checking who signed on. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:515-532, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:611, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:751, app/app-transaction-type-db2/csd/CRDDEMOD.csd:25-26 |
| TTRDM-BR-060 | Screen assumes admin user type without checking | business rule | THE Transaction Type List screen SHALL never check the user type before allowing updates or deletes of transaction types. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:515-532, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:611, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:751, app/app-transaction-type-db2/csd/CRDDEMOD.csd:25-26 |

### Worked examples

- TTRDM-BR-059: Start = CTLI typed at a blank terminal; Signed-on user type = none → The full list/update/delete screen is shown and the user is treated as 'A'
- TTRDM-BR-060: Carried user type = 'U'; Action = D on a row, then F10 → The delete is carried out; user type is not checked

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-193: Is the transaction-type maintenance screen (transaction CTLI) limited to administrators by system security settings, or should the program itself check that the user is an administrator? (Security officer) On TTRDM-BR-060.
- DEF-169: Confirm this is deliberate: The list/update/delete screen grants administrator status on a direct start of CTLI and never checks the signed-on user type, so any user who can start the transaction can update or delete transaction types. (Subject-matter expert) On TTRDM-BR-060.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
