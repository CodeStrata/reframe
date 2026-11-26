# Feature specification: Publish policy number lookup as a web service

**Feature:** WSIG-C05 · Web Service Interface Generation · Web Service Interface Generation

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (WSIG-C05)

As an integration developer, I want the policy number program published as a web service, so that other applications can call policy number lookup as a web service.

Publishes policy number lookup as a single web service at the address GENAPP/LGIPVS01, so that other applications can look up policy numbers without the screens. It serves integration developers. It must never mix up its separate request and response layouts, and it must never move the service address that callers depend on.

**Acceptance scenarios:**

1. **Given** program (PGMNAME): 'LGIPVS01'; request copybook (REQMEM): 'SOAVPII'; response copybook (RESPMEM): 'SOAVPIO', **when** policy number web service set-up job runs, **then** The program that obtains a policy number from the VSAM file is published as a web service at 'GENAPP/LGIPVS01'. (WSIG-C05-AC-01)
2. **Given** the policy number web service generation for program LGIPVS01 is run with ZFSHOME set to the installation home directory, **when** the generation step completes, **then** the binding file '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGIPVS01.LOG' all exist, at exactly those paths (WSIG-C05-AC-02)
3. **Given** the policy number generation step for LGIPVS01 is configured, **when** the step's generator settings are inspected before it runs, **then** it uses Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS' (WSIG-C05-AC-03)

## Requirements

### Functional requirements

- **WSIG-REQ-F-026** (design note): The system shall generate the policy number web service for program 'LGIPVS01' with the CICS web service generation procedure (DFHLS2WS), using COBOL request copybook 'SOAVPII' and response copybook 'SOAVPIO' from the source library, service address 'GENAPP/LGIPVS01', COMMAREA data passing and proxy 'PROXY.HURSLEY.IBM.COM:80'. Rules: WSIG-BR-029.
- **WSIG-REQ-F-027** (design note): The system shall write the policy number binding file '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGIPVS01.LOG'. Rules: WSIG-BR-030.
- **WSIG-REQ-N-006** (design note): The system shall run the policy number generation with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS'. Rules: WSIG-BR-030.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| WSIG-BR-029 | Generate web service binding and WSDL | design note | THE policy number web service set-up job SHALL run the CICS web service generation procedure (DFHLS2WS) for program 'LGIPVS01', using COBOL request copybook 'SOAVPII' and response copybook 'SOAVPIO' from the source library, service address 'GENAPP/LGIPVS01', COMMAREA data passing and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsavp01.jcl:11-31 |
| WSIG-BR-030 | Generate web service binding and WSDL | design note | THE policy number web service set-up job SHALL write the binding file '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGIPVS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGIPVS01.LOG', running with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS'. | medium | base/cntl/wsavp01.jcl:11-31 |

### Key entities

None found in the source.

### Needs clarification

- SME-120: When the step that generates the web service definition (binding and WSDL) runs, what counts as success and what counts as failure? For example: what should happen if the request or response layout is invalid or incomplete, or if the output cannot be written, and may partial output be left behind after a failure? This applies to both the customer and the policy web service generation jobs. (Integration team) On WSIG-BR-030.
- SME-122: Environment settings used to generate the web services are currently fixed: the network proxy (PROXY.HURSLEY.IBM.COM:80), the Java runtime directory, the CICS install directory, and the source and output locations. Should these stay fixed or become configurable settings in the new system? (Platform operations team) On WSIG-BR-030.
- SME-124: Today request and response data are passed to the target program through a shared memory block (COMMAREA). What interface should the new service use to pass this data to the program that handles it? (Application architecture team) On WSIG-BR-030.

### Decision table gaps

None.
