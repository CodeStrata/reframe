# Requirements: Register online CardDemo programs and transactions (SOM-C01)

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
