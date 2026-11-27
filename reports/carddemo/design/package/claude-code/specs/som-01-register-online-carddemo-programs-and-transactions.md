# Register online CardDemo programs and transactions (SOM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as scheduled job · risk high

## Introduction

Sets up the entry points users and administrators start from: the sign-on screen and the Admin Menu, each reachable by its own short code. This is set up once per environment by operations staff, not by end users. It must never leave the sign-on or Admin Menu unregistered or linked to the wrong code, because then nobody can sign on or reach administration.

**User story:** As a system administrator, I want the CardDemo sign-on and admin menu programs and their transactions registered in the online system, so that users can start them by transaction code.

## Requirements

### Requirement 1: SOM-REQ-F-001 (design note)

#### Acceptance criteria

1. The system shall define the login program COSGN00C in the CICS group CARDDEMO with data location ANY and transaction code CC00. (rules SOM-BR-001)
2. GIVEN Setup job: CBADMCDJ run against the CICS definitions file WHEN CardDemo online resource setup job (CBADMCDJ) runs THEN Group CARDDEMO holds program COSGN00C, data location ANY, transaction code CC00, description LOGIN. (SOM-C01-AC-01; SOM-BR-001)

### Requirement 2: SOM-REQ-F-002 (design note)

#### Acceptance criteria

1. The system shall define the admin menu program COADM00C in the CICS group CARDDEMO with data location ANY and transaction code CCAD. (rules SOM-BR-002)
2. GIVEN Setup job: CBADMCDJ run against the CICS definitions file WHEN CardDemo online resource setup job (CBADMCDJ) runs THEN Group CARDDEMO holds program COADM00C, data location ANY, transaction code CCAD, description ADMIN MENU. (SOM-C01-AC-02; SOM-BR-002)

### Requirement 3: SOM-REQ-F-003 (design note)

#### Acceptance criteria

1. The system shall define transaction CCDM in the CICS group CARDDEMO to start the admin menu program COADM00C with task data location ANY. (rules SOM-BR-003)
2. GIVEN Setup job: CBADMCDJ run against the CICS definitions file WHEN CardDemo online resource setup job (CBADMCDJ) runs THEN Group CARDDEMO holds transaction CCDM, which starts program COADM00C. (SOM-C01-AC-03; SOM-BR-003)

## Screens and components

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


## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-001 | Register the login program with its transaction | design note | THE CardDemo online resource setup job (CBADMCDJ) SHALL define the login program COSGN00C in the CICS group CARDDEMO with data location ANY and transaction code CC00. | medium | app/jcl/CBADMCDJ.jcl:27-33, app/jcl/CBADMCDJ.jcl:98-99, app/cbl/COSGN00C.cbl:37 |
| SOM-BR-002 | Register the admin menu program with its transaction | design note | THE CardDemo online resource setup job (CBADMCDJ) SHALL define the admin menu program COADM00C in the CICS group CARDDEMO with data location ANY and transaction code CCAD. | medium | app/jcl/CBADMCDJ.jcl:130-132 |
| SOM-BR-003 | Register the admin menu transaction | design note | THE CardDemo online resource setup job (CBADMCDJ) SHALL define transaction CCDM in the CICS group CARDDEMO to start the admin menu program COADM00C with task data location ANY. | medium | app/jcl/CBADMCDJ.jcl:147-148 |

### Worked examples

- SOM-BR-001: Setup job = CBADMCDJ run against the CICS definitions file → Group CARDDEMO holds program COSGN00C, data location ANY, transaction code CC00, description LOGIN.
- SOM-BR-002: Setup job = CBADMCDJ run against the CICS definitions file → Group CARDDEMO holds program COADM00C, data location ANY, transaction code CCAD, description ADMIN MENU.
- SOM-BR-003: Setup job = CBADMCDJ run against the CICS definitions file → Group CARDDEMO holds transaction CCDM, which starts program COADM00C.

## Decision tables

None.

## Design notes

- SOM-BR-001: Register the sign-on screen as a routable entry point (for example a route or deep-link code that matches legacy code CC00) in the application's deployment or route configuration, which is applied when the environment is provisioned. It must be open to any user who has not signed on. No data-location setting is needed.
- SOM-BR-002: Register the Admin Menu as a routable entry point under the code CCAD in the same deployment or route configuration as the sign-on screen, so the configuration is versioned and applied with each release.
- SOM-BR-003: Map a second entry code, CCDM, to the same Admin Menu route, so both CCAD and CCDM open the Admin Menu. Keep it as an alias in the route configuration, not a separate screen.

## Open questions

- SME-016: Two transaction codes both open the same admin menu. Should the new system keep both entry points, or is one redundant? (Application owner) On SOM-BR-001, SOM-BR-002, SOM-BR-003.
- SME-017: Does the mainframe 'data location ANY' storage setting need an equivalent on the target platform, or can it be dropped? (Platform architecture team) On SOM-BR-001, SOM-BR-002, SOM-BR-003.
- DEF-151: Is this intended? The job defines admin menu program COADM00C with transaction codes CCAD and CCDM, but no COADM00C exists in the source; the admin menu program is COADM01C with transaction CA00, which app/csd/CARDDEMO.CSD defines, so these definitions point at a missing program. (Subject-matter expert) On SOM-BR-002.
- DEF-152: Is this intended? Transaction CCDM starts COADM00C, which does not exist in the source; the admin menu is COADM01C under transaction CA00, defined in app/csd/CARDDEMO.CSD. CCDM also differs from the CCAD code given on the program definition. (Subject-matter expert) On SOM-BR-003.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
