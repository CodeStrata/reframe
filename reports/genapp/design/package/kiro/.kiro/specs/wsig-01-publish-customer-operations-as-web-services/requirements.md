# Requirements: Publish customer operations as web services (WSIG-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Web Service Interface Generation · Web Service Interface Generation · runs as scheduled job · risk medium

## Introduction

Publishes the four customer operations (add customer, customer inquiry, customer update and customer number lookup) as callable web services, each at its own fixed address with a published service description, so that other applications can work with customers without going through the screens. It serves integration developers and the systems they connect. It must never publish a service whose request or response layout differs from the layout the customer program actually uses, and it must never move a service address (GENAPP/LGACUS01, GENAPP/LGICUS01, GENAPP/LGUCUS01, GENAPP/LGICVS01) that callers depend on.

**User story:** As an integration developer, I want the customer add, customer inquiry, customer update and customer number programs published as web services with their binding files and service descriptions, so that other applications can call customer operations as web services.

## Requirements

### Requirement 1: WSIG-REQ-F-001 (design note)

#### Acceptance criteria

1. The system shall expose the add-customer program LGACUS01 as a web service at relative address GENAPP/LGACUS01, passing data by COMMAREA and using the customer request and response layout SOAIC01 from library <SOURCEX>. (rules WSIG-BR-001)
2. GIVEN program (PGMNAME): LGACUS01; request/response layout (REQMEM/RESPMEM): SOAIC01; URI: GENAPP/LGACUS01 WHEN add-customer web service generation job runs THEN A web service for adding a customer is generated, reached at GENAPP/LGACUS01 and calling LGACUS01 through a COMMAREA. (WSIG-C01-AC-01; WSIG-BR-001)

### Requirement 2: WSIG-REQ-F-002 (design note)

#### Acceptance criteria

1. The system shall write the add-customer binding file to <ZFSHOME>/genapp/wsdir/LGACUS01.wsbind, the service description to <ZFSHOME>/genapp/wsdir/LGACUS01.wsdl and the generation log to <ZFSHOME>/genapp/logs/LS2WS_LGACUS01.LOG. (rules WSIG-BR-002)
2. GIVEN ZFSHOME: /u/genapp WHEN add-customer web service generation job runs THEN Files /u/genapp/genapp/wsdir/LGACUS01.wsbind and LGACUS01.wsdl and log /u/genapp/genapp/logs/LS2WS_LGACUS01.LOG are produced. (WSIG-C01-AC-02; WSIG-BR-002)

### Requirement 3: WSIG-REQ-F-003 (design note)

#### Acceptance criteria

1. The system shall expose the customer inquiry program LGICUS01 as a web service at relative address GENAPP/LGICUS01, passing data by COMMAREA and using the customer request and response layout SOAIC01 from library <SOURCEX>. (rules WSIG-BR-003)
2. GIVEN program (PGMNAME): LGICUS01; request/response layout (REQMEM/RESPMEM): SOAIC01; URI: GENAPP/LGICUS01 WHEN customer inquiry web service generation job runs THEN A web service for inquiring on a customer is generated, reached at GENAPP/LGICUS01 and calling LGICUS01 through a COMMAREA. (WSIG-C01-AC-03; WSIG-BR-003)

### Requirement 4: WSIG-REQ-F-004 (design note)

#### Acceptance criteria

1. The system shall write the customer inquiry binding file to <ZFSHOME>/genapp/wsdir/LGICUS01.wsbind, the service description to <ZFSHOME>/genapp/wsdir/LGICUS01.wsdl and the generation log to <ZFSHOME>/genapp/logs/LS2WS_LGICUS01.LOG. (rules WSIG-BR-004)
2. GIVEN ZFSHOME: /u/genapp WHEN customer inquiry web service generation job runs THEN Files /u/genapp/genapp/wsdir/LGICUS01.wsbind and LGICUS01.wsdl and log /u/genapp/genapp/logs/LS2WS_LGICUS01.LOG are produced. (WSIG-C01-AC-04; WSIG-BR-004)

### Requirement 5: WSIG-REQ-F-005 (design note)

#### Acceptance criteria

1. The system shall generate the customer update web service for program 'LGUCUS01' with the CICS web service generation procedure (DFHLS2WS), using the COBOL copybook 'SOAIC01' for both request and response, service address 'GENAPP/LGUCUS01', COMMAREA data passing and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-005)
2. GIVEN program (PGMNAME): 'LGUCUS01'; request and response copybook (REQMEM, RESPMEM): 'SOAIC01'; service address (URI): 'GENAPP/LGUCUS01' WHEN customer update web service set-up job runs THEN The customer update program is published as a web service at 'GENAPP/LGUCUS01' that passes its data through the COMMAREA. (WSIG-C01-AC-05; WSIG-BR-005)

### Requirement 6: WSIG-REQ-F-006 (design note)

#### Acceptance criteria

1. The system shall write the customer update binding file '<ZFSHOME>/genapp/wsdir/LGUCUS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGUCUS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGUCUS01.LOG'. (rules WSIG-BR-006)
2. GIVEN the customer update web service generation for program LGUCUS01 is run with ZFSHOME set to the installation home directory WHEN the generation step completes THEN the binding file '<ZFSHOME>/genapp/wsdir/LGUCUS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGUCUS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGUCUS01.LOG' all exist, at exactly those paths (WSIG-C01-AC-09; WSIG-BR-006)

### Requirement 7: WSIG-REQ-F-007 (design note)

#### Acceptance criteria

1. The system shall generate the customer number web service for program 'LGICVS01' with the CICS web service generation procedure (DFHLS2WS), using COBOL request copybook 'SOAVCII' and response copybook 'SOAVCIO' from the source library, service address 'GENAPP/LGICVS01', COMMAREA data passing and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-007)
2. GIVEN program (PGMNAME): 'LGICVS01'; request copybook (REQMEM): 'SOAVCII'; response copybook (RESPMEM): 'SOAVCIO' WHEN customer number web service set-up job runs THEN The program that obtains a customer number from the VSAM file is published as a web service at 'GENAPP/LGICVS01'. (WSIG-C01-AC-06; WSIG-BR-007)

### Requirement 8: WSIG-REQ-F-008 (design note)

#### Acceptance criteria

1. The system shall write the customer number binding file '<ZFSHOME>/genapp/wsdir/LGICVS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGICVS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGICVS01.LOG'. (rules WSIG-BR-008)
2. GIVEN the customer number web service generation for program LGICVS01 is run with ZFSHOME set to the installation home directory WHEN the generation step completes THEN the binding file '<ZFSHOME>/genapp/wsdir/LGICVS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGICVS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGICVS01.LOG' all exist, at exactly those paths (WSIG-C01-AC-10; WSIG-BR-008)

### Requirement 9: WSIG-REQ-N-001 (design note)

#### Acceptance criteria

1. The system shall run the add-customer and customer inquiry generation with the CICS language-structure-to-WSDL procedure (DFHLS2WS), Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp', temporary file 'LS2WS' and HTTP proxy PROXY.HURSLEY.IBM.COM:80. (rules WSIG-BR-009, WSIG-BR-010)
2. GIVEN JAVADIR: 'java601_bit64_ga/J6.0.1_64'; HTTPPROXY: PROXY.HURSLEY.IBM.COM:80 WHEN add-customer web service generation job runs THEN The generation runs with that Java runtime and reaches external resources through the Hursley proxy. (WSIG-C01-AC-07; WSIG-BR-009)
3. GIVEN TMPDIR: '/tmp'; TMPFILE: 'LS2WS' WHEN customer inquiry web service generation job runs THEN The generation uses /tmp for its temporary files named with prefix LS2WS. (WSIG-C01-AC-08; WSIG-BR-010)

### Requirement 10: WSIG-REQ-N-002 (design note)

#### Acceptance criteria

1. The system shall run the customer update and customer number generation with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS'. (rules WSIG-BR-006, WSIG-BR-008)
2. GIVEN the customer update generation step for LGUCUS01 is configured WHEN the step's generator settings are inspected before it runs THEN it uses Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS' (WSIG-C01-AC-11; WSIG-BR-006)
3. GIVEN the customer number generation step for LGICVS01 is configured WHEN the step's generator settings are inspected before it runs THEN it uses Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS' (WSIG-C01-AC-12; WSIG-BR-008)
