# Requirements: Publish policy update as web services by policy type (WSIG-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Web Service Interface Generation · Web Service Interface Generation · runs as scheduled job · risk medium

## Introduction

Publishes updating a policy as four web services, one for each policy type (Motor, Commercial, Endowment and House). All four are served by the same policy update program, but each has its own address and its own policy-type layout. It serves integration developers whose systems change existing policies. It must never accept an update in another policy type's layout, and it must keep the addresses GENAPP/LGUPOLM1, GENAPP/LGUPOLB1, GENAPP/LGUPOLE1 and GENAPP/LGUPOLH1 stable.

**User story:** As an integration developer, I want the policy update program published as a separate web service for each policy type, so that other applications can update Motor, Commercial, Endowment and House policies as web services.

## Requirements

### Requirement 1: WSIG-REQ-F-018 (design note)

#### Acceptance criteria

1. The system shall generate the Motor policy update web service for program LGUPOL01, using request and response layout SOAIPM1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLM1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-021)
2. GIVEN Policy type: Motor; Program: LGUPOL01; Layout (REQMEM/RESPMEM): SOAIPM1 WHEN policy web service build job runs THEN A web service is published at 'GENAPP/LGUPOLM1' that passes the SOAIPM1 layout to LGUPOL01 through its COMMAREA. (WSIG-C04-AC-01; WSIG-BR-021)

### Requirement 2: WSIG-REQ-F-019 (design note)

#### Acceptance criteria

1. The system shall write the Motor service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLM1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLM1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLM1.LOG'. (rules WSIG-BR-022)
2. GIVEN Service: LGUPOLM1 WHEN policy web service build job runs THEN Files 'LGUPOLM1.wsbind' and 'LGUPOLM1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLM1.LOG' in genapp/logs. (WSIG-C04-AC-02; WSIG-BR-022)

### Requirement 3: WSIG-REQ-F-020 (design note)

#### Acceptance criteria

1. The system shall generate the Commercial policy update web service for program LGUPOL01, using request and response layout SOAIPB1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLB1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-023)
2. GIVEN Policy type: Commercial; Program: LGUPOL01; Layout (REQMEM/RESPMEM): SOAIPB1 WHEN policy web service build job runs THEN A web service is published at 'GENAPP/LGUPOLB1' that passes the SOAIPB1 layout to LGUPOL01 through its COMMAREA. (WSIG-C04-AC-03; WSIG-BR-023)

### Requirement 4: WSIG-REQ-F-021 (design note)

#### Acceptance criteria

1. The system shall write the Commercial service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLB1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLB1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLB1.LOG'. (rules WSIG-BR-024)
2. GIVEN Service: LGUPOLB1 WHEN policy web service build job runs THEN Files 'LGUPOLB1.wsbind' and 'LGUPOLB1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLB1.LOG' in genapp/logs. (WSIG-C04-AC-04; WSIG-BR-024)

### Requirement 5: WSIG-REQ-F-022 (design note)

#### Acceptance criteria

1. The system shall generate the Endowment policy update web service for program LGUPOL01, using request and response layout SOAIPE1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLE1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-025)
2. GIVEN Policy type: Endowment; Program: LGUPOL01; Layout (REQMEM/RESPMEM): SOAIPE1 WHEN policy web service build job runs THEN A web service is published at 'GENAPP/LGUPOLE1' that passes the SOAIPE1 layout to LGUPOL01 through its COMMAREA. (WSIG-C04-AC-05; WSIG-BR-025)

### Requirement 6: WSIG-REQ-F-023 (design note)

#### Acceptance criteria

1. The system shall write the Endowment service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLE1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLE1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLE1.LOG'. (rules WSIG-BR-026)
2. GIVEN Service: LGUPOLE1 WHEN policy web service build job runs THEN Files 'LGUPOLE1.wsbind' and 'LGUPOLE1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLE1.LOG' in genapp/logs. (WSIG-C04-AC-06; WSIG-BR-026)

### Requirement 7: WSIG-REQ-F-024 (design note)

#### Acceptance criteria

1. The system shall generate the House policy update web service for program LGUPOL01, using request and response layout SOAIPH1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLH1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-027)
2. GIVEN Policy type: House; Program: LGUPOL01; Layout (REQMEM/RESPMEM): SOAIPH1 WHEN policy web service build job runs THEN A web service is published at 'GENAPP/LGUPOLH1' that passes the SOAIPH1 layout to LGUPOL01 through its COMMAREA. (WSIG-C04-AC-07; WSIG-BR-027)

### Requirement 8: WSIG-REQ-F-025 (design note)

#### Acceptance criteria

1. The system shall write the House service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLH1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLH1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLH1.LOG'. (rules WSIG-BR-028)
2. GIVEN Service: LGUPOLH1 WHEN policy web service build job runs THEN Files 'LGUPOLH1.wsbind' and 'LGUPOLH1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLH1.LOG' in genapp/logs. (WSIG-C04-AC-08; WSIG-BR-028)

### Requirement 9: WSIG-REQ-N-005 (design note)

#### Acceptance criteria

1. The system shall run each policy update generation with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', empty path prefix and temporary file 'LS2WS' in '/tmp'. (rules WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028)
2. GIVEN Service: LGUPOLM1 WHEN policy web service build job runs THEN Files 'LGUPOLM1.wsbind' and 'LGUPOLM1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLM1.LOG' in genapp/logs. (WSIG-C04-AC-02; WSIG-BR-022)
3. GIVEN Service: LGUPOLB1 WHEN policy web service build job runs THEN Files 'LGUPOLB1.wsbind' and 'LGUPOLB1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLB1.LOG' in genapp/logs. (WSIG-C04-AC-04; WSIG-BR-024)
4. GIVEN Service: LGUPOLE1 WHEN policy web service build job runs THEN Files 'LGUPOLE1.wsbind' and 'LGUPOLE1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLE1.LOG' in genapp/logs. (WSIG-C04-AC-06; WSIG-BR-026)
5. GIVEN Service: LGUPOLH1 WHEN policy web service build job runs THEN Files 'LGUPOLH1.wsbind' and 'LGUPOLH1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLH1.LOG' in genapp/logs. (WSIG-C04-AC-08; WSIG-BR-028)
