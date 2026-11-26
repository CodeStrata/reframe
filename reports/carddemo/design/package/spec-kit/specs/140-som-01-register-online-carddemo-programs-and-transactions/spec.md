# Feature specification: Register online CardDemo programs and transactions

**Feature:** SOM-C01 · System Operations and Maintenance · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (SOM-C01)

As a system administrator, I want the CardDemo sign-on and admin menu programs and their transactions registered in the online system, so that users can start them by transaction code.

Sets up the entry points users and administrators start from: the sign-on screen and the Admin Menu, each reachable by its own short code. This is set up once per environment by operations staff, not by end users. It must never leave the sign-on or Admin Menu unregistered or linked to the wrong code, because then nobody can sign on or reach administration.

**Acceptance scenarios:**

1. **Given** Setup job: CBADMCDJ run against the CICS definitions file, **when** CardDemo online resource setup job (CBADMCDJ) runs, **then** Group CARDDEMO holds program COSGN00C, data location ANY, transaction code CC00, description LOGIN. (SOM-C01-AC-01)
2. **Given** Setup job: CBADMCDJ run against the CICS definitions file, **when** CardDemo online resource setup job (CBADMCDJ) runs, **then** Group CARDDEMO holds program COADM00C, data location ANY, transaction code CCAD, description ADMIN MENU. (SOM-C01-AC-02)
3. **Given** Setup job: CBADMCDJ run against the CICS definitions file, **when** CardDemo online resource setup job (CBADMCDJ) runs, **then** Group CARDDEMO holds transaction CCDM, which starts program COADM00C. (SOM-C01-AC-03)

## Requirements

### Functional requirements

- **SOM-REQ-F-001** (design note): The system shall define the login program COSGN00C in the CICS group CARDDEMO with data location ANY and transaction code CC00. Rules: SOM-BR-001.
- **SOM-REQ-F-002** (design note): The system shall define the admin menu program COADM00C in the CICS group CARDDEMO with data location ANY and transaction code CCAD. Rules: SOM-BR-002.
- **SOM-REQ-F-003** (design note): The system shall define transaction CCDM in the CICS group CARDDEMO to start the admin menu program COADM00C with task data location ANY. Rules: SOM-BR-003.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-001 | Register the login program with its transaction | design note | THE CardDemo online resource setup job (CBADMCDJ) SHALL define the login program COSGN00C in the CICS group CARDDEMO with data location ANY and transaction code CC00. | medium | app/jcl/CBADMCDJ.jcl:27-33, app/jcl/CBADMCDJ.jcl:98-99, app/cbl/COSGN00C.cbl:37 |
| SOM-BR-002 | Register the admin menu program with its transaction | design note | THE CardDemo online resource setup job (CBADMCDJ) SHALL define the admin menu program COADM00C in the CICS group CARDDEMO with data location ANY and transaction code CCAD. | medium | app/jcl/CBADMCDJ.jcl:130-132 |
| SOM-BR-003 | Register the admin menu transaction | design note | THE CardDemo online resource setup job (CBADMCDJ) SHALL define transaction CCDM in the CICS group CARDDEMO to start the admin menu program COADM00C with task data location ANY. | medium | app/jcl/CBADMCDJ.jcl:147-148 |

### Key entities

None found in the source.

### Needs clarification

- SME-016: Two transaction codes both open the same admin menu. Should the new system keep both entry points, or is one redundant? (Application owner) On SOM-BR-001, SOM-BR-002, SOM-BR-003.
- SME-017: Does the mainframe 'data location ANY' storage setting need an equivalent on the target platform, or can it be dropped? (Platform architecture team) On SOM-BR-001, SOM-BR-002, SOM-BR-003.
- DEF-151: Is this intended? The job defines admin menu program COADM00C with transaction codes CCAD and CCDM, but no COADM00C exists in the source; the admin menu program is COADM01C with transaction CA00, which app/csd/CARDDEMO.CSD defines, so these definitions point at a missing program. (Subject-matter expert) On SOM-BR-002.
- DEF-152: Is this intended? Transaction CCDM starts COADM00C, which does not exist in the source; the admin menu is COADM01C under transaction CA00, defined in app/csd/CARDDEMO.CSD. CCDM also differs from the CCAD code given on the program definition. (Subject-matter expert) On SOM-BR-003.

### Decision table gaps

None.
