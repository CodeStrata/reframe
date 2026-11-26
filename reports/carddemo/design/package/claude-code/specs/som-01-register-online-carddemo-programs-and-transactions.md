# Register online CardDemo programs and transactions (SOM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as scheduled job · risk high

## Introduction

Registers the sign-on program and the admin menu program with the online system so that users can start them: sign-on under transaction code CC00, and the admin menu under CCAD and CCDM. This is set up by operations and is not something users see. It must never leave an entry point unregistered or attached to the wrong program, because then users cannot sign on or administrators cannot reach their menu.

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

Sign in to CardDemo with User ID and password; on success the user lands on the home page for their role. Also shows the signed-out confirmation.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

One role-aware home page replacing both the Main Menu and the Admin Menu: each allowed function is a link, grouped by subject, instead of a typed option number. Administrators see Administration; regular users see accounts, cards, transactions and payments.

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

- SOM-BR-001: The sign-on entry point must be set up as part of deployment configuration, such as a route table or service registration. Its legacy code CC00 maps to the sign-on screen, and it must be usable from any node or region (the legacy data location ANY). Keep CC00 as an alias only if outside links or operators still use it.
- SOM-BR-002: Register the admin menu as a deployable entry point (a route or service) that answers to the legacy code CCAD. It must be declared in the same deployment configuration as sign-on (the CARDDEMO group), so the two are always released together.
- SOM-BR-003: A second legacy code, CCDM, must open the same admin menu. Model it as an alias route or redirect to the admin menu entry point, not as a separate screen. No location restriction is needed (ANY).

## Open questions

- SME-016: Two transaction codes both open the same admin menu. Should the new system keep both entry points, or is one redundant? (Application owner) On SOM-BR-001, SOM-BR-002, SOM-BR-003.
- SME-017: Does the mainframe 'data location ANY' storage setting need an equivalent on the target platform, or can it be dropped? (Platform architecture team) On SOM-BR-001, SOM-BR-002, SOM-BR-003.
- DEF-151: Is this intended? The job defines admin menu program COADM00C with transaction codes CCAD and CCDM, but no COADM00C exists in the source; the admin menu program is COADM01C with transaction CA00, which app/csd/CARDDEMO.CSD defines, so these definitions point at a missing program. (Subject-matter expert) On SOM-BR-002.
- DEF-152: Is this intended? Transaction CCDM starts COADM00C, which does not exist in the source; the admin menu is COADM01C under transaction CA00, defined in app/csd/CARDDEMO.CSD. CCDM also differs from the CCAD code given on the program definition. (Subject-matter expert) On SOM-BR-003.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
