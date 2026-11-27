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

Sign in to CardDemo with a user ID and password. Administrators and regular users both land on Home, which shows the functions their role allows.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

Landing page after sign-in. It lists every function the signed-in role may use as links, and replaces the numbered Main Menu, the Admin Menu and the typed option number.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data model

None found in the source.

## Design notes

- SOM-BR-001: Register the sign-on screen as a routable entry point (for example a route or deep-link code that matches legacy code CC00) in the application's deployment or route configuration, which is applied when the environment is provisioned. It must be open to any user who has not signed on. No data-location setting is needed.
- SOM-BR-002: Register the Admin Menu as a routable entry point under the code CCAD in the same deployment or route configuration as the sign-on screen, so the configuration is versioned and applied with each release.
- SOM-BR-003: Map a second entry code, CCDM, to the same Admin Menu route, so both CCAD and CCDM open the Admin Menu. Keep it as an alias in the route configuration, not a separate screen.

## Decision tables

None.
