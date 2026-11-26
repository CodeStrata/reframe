# Implementation plan: Register online CardDemo programs and transactions (SOM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

### Sign in (S-SIGN-IN)

Sign in to CardDemo with User ID and password; on success the user lands on the home page for their role. Also shows the signed-out confirmation.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

One role-aware home page replacing both the Main Menu and the Admin Menu: each allowed function is a link, grouped by subject, instead of a typed option number. Administrators see Administration; regular users see accounts, cards, transactions and payments.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data model

None found in the source.

## Design notes

- SOM-BR-001: The sign-on entry point must be set up as part of deployment configuration, such as a route table or service registration. Its legacy code CC00 maps to the sign-on screen, and it must be usable from any node or region (the legacy data location ANY). Keep CC00 as an alias only if outside links or operators still use it.
- SOM-BR-002: Register the admin menu as a deployable entry point (a route or service) that answers to the legacy code CCAD. It must be declared in the same deployment configuration as sign-on (the CARDDEMO group), so the two are always released together.
- SOM-BR-003: A second legacy code, CCDM, must open the same admin menu. Model it as an alias route or redirect to the admin menu entry point, not as a separate screen. No location restriction is needed (ANY).

## Decision tables

None.
