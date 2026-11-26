# Requirements: Publish policy add as web services by policy type (WSIG-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Web Service Interface Generation · Web Service Interface Generation · runs as scheduled job · risk medium

## Introduction

Publishes adding a policy as four web services, one for each policy type (Motor, Endowment, House and Commercial). All four are served by the same policy add program, but each has its own address and its own policy-type layout. It serves integration developers whose systems create policies. It must never send a request to the wrong policy type's layout, and it must never change the addresses GENAPP/LGAPOLM1, GENAPP/LGAPOLE1, GENAPP/LGAPOLH1 and GENAPP/LGAPOLB1.

**User story:** As an integration developer, I want the policy add program published as a separate web service for each policy type, so that other applications can add Motor, Endowment, House and Commercial policies as web services.

## Requirements

### Requirement 1: WSIG-REQ-F-009 (design note)

#### Acceptance criteria

1. The system shall expose the policy add program LGAPOL01 as the Motor Policy web service at URI 'GENAPP/LGAPOLM1', using COBOL copybook member SOAIPM1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLM1.wsbind, LGAPOLM1.wsdl and log LS2WS_LGAPOLM1.LOG. (rules WSIG-BR-011)
2. GIVEN Job step: LS2WS (Motor Policy) WHEN web service generation job runs THEN <ZFSHOME>/genapp/wsdir/LGAPOLM1.wsbind and LGAPOLM1.wsdl are produced for URI GENAPP/LGAPOLM1 (WSIG-C02-AC-01; WSIG-BR-011)

### Requirement 2: WSIG-REQ-F-010 (design note)

#### Acceptance criteria

1. The system shall expose the policy add program LGAPOL01 as the Endowment Policy web service at URI 'GENAPP/LGAPOLE1', using COBOL copybook member SOAIPE1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLE1.wsbind, LGAPOLE1.wsdl and log LS2WS_LGAPOLE1.LOG. (rules WSIG-BR-012)
2. GIVEN Job step: LS2WS (Endowment Policy) WHEN web service generation job runs THEN <ZFSHOME>/genapp/wsdir/LGAPOLE1.wsbind and LGAPOLE1.wsdl are produced for URI GENAPP/LGAPOLE1 (WSIG-C02-AC-02; WSIG-BR-012)

### Requirement 3: WSIG-REQ-F-011 (design note)

#### Acceptance criteria

1. The system shall expose the policy add program LGAPOL01 as the House Policy web service at URI 'GENAPP/LGAPOLH1', using COBOL copybook member SOAIPH1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLH1.wsbind, LGAPOLH1.wsdl and log LS2WS_LGAPOLH1.LOG. (rules WSIG-BR-013)
2. GIVEN Job step: LS2WS (House Policy) WHEN web service generation job runs THEN <ZFSHOME>/genapp/wsdir/LGAPOLH1.wsbind and LGAPOLH1.wsdl are produced for URI GENAPP/LGAPOLH1 (WSIG-C02-AC-03; WSIG-BR-013)

### Requirement 4: WSIG-REQ-F-012 (design note)

#### Acceptance criteria

1. The system shall expose the policy add program LGAPOL01 as the Commercial Policy web service at URI 'GENAPP/LGAPOLB1', using COBOL copybook member SOAIPB1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLB1.wsbind, LGAPOLB1.wsdl and log LS2WS_LGAPOLB1.LOG. (rules WSIG-BR-014)
2. GIVEN Job step: LS2WS (Commercial Policy) WHEN web service generation job runs THEN <ZFSHOME>/genapp/wsdir/LGAPOLB1.wsbind and LGAPOLB1.wsdl are produced for URI GENAPP/LGAPOLB1 (WSIG-C02-AC-04; WSIG-BR-014)

### Requirement 5: WSIG-REQ-N-003 (design note)

#### Acceptance criteria

1. The system shall generate the House Policy and Commercial Policy add web services with Java 'java601_bit64_ga/J6.0.1_64' and CICS directory 'cics660'. (rules WSIG-BR-013, WSIG-BR-014)
2. GIVEN Job step: LS2WS (House Policy) WHEN web service generation job runs THEN <ZFSHOME>/genapp/wsdir/LGAPOLH1.wsbind and LGAPOLH1.wsdl are produced for URI GENAPP/LGAPOLH1 (WSIG-C02-AC-03; WSIG-BR-013)
3. GIVEN Job step: LS2WS (Commercial Policy) WHEN web service generation job runs THEN <ZFSHOME>/genapp/wsdir/LGAPOLB1.wsbind and LGAPOLB1.wsdl are produced for URI GENAPP/LGAPOLB1 (WSIG-C02-AC-04; WSIG-BR-014)
