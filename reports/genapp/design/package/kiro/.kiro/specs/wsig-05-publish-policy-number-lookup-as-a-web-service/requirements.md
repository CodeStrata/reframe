# Requirements: Publish policy number lookup as a web service (WSIG-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Web Service Interface Generation · Web Service Interface Generation · runs as scheduled job · risk low

## Introduction

Publishes policy number lookup as a single web service at the address GENAPP/LGIPVS01, so that other applications can look up policy numbers without the screens. It serves integration developers. It must never mix up its separate request and response layouts, and it must never move the service address that callers depend on.

**User story:** As an integration developer, I want the policy number program published as a web service, so that other applications can call policy number lookup as a web service.

## Requirements

### Requirement 1: WSIG-REQ-F-026 (design note)

#### Acceptance criteria

1. The system shall generate the policy number web service for program 'LGIPVS01' with the CICS web service generation procedure (DFHLS2WS), using COBOL request copybook 'SOAVPII' and response copybook 'SOAVPIO' from the source library, service address 'GENAPP/LGIPVS01', COMMAREA data passing and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-029)
2. GIVEN program (PGMNAME): 'LGIPVS01'; request copybook (REQMEM): 'SOAVPII'; response copybook (RESPMEM): 'SOAVPIO' WHEN policy number web service set-up job runs THEN The program that obtains a policy number from the VSAM file is published as a web service at 'GENAPP/LGIPVS01'. (WSIG-C05-AC-01; WSIG-BR-029)

### Requirement 2: WSIG-REQ-F-027 (design note)

#### Acceptance criteria

1. The system shall write the policy number binding file '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGIPVS01.LOG'. (rules WSIG-BR-030)
2. GIVEN the policy number web service generation for program LGIPVS01 is run with ZFSHOME set to the installation home directory WHEN the generation step completes THEN the binding file '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGIPVS01.LOG' all exist, at exactly those paths (WSIG-C05-AC-02; WSIG-BR-030)

### Requirement 3: WSIG-REQ-N-006 (design note)

#### Acceptance criteria

1. The system shall run the policy number generation with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS'. (rules WSIG-BR-030)
2. GIVEN the policy number generation step for LGIPVS01 is configured WHEN the step's generator settings are inspected before it runs THEN it uses Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS' (WSIG-C05-AC-03; WSIG-BR-030)
