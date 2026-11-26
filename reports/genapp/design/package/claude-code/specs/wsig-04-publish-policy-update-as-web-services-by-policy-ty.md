# Publish policy update as web services by policy type (WSIG-C04)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| WSIG-BR-021 | Generate the policy update web service | design note | THE policy web service build job SHALL generate the Motor policy update web service for program LGUPOL01, using request and response layout SOAIPM1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLM1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsaup01.jcl:12-32 |
| WSIG-BR-022 | Generate the policy update web service | design note | THE policy web service build job SHALL write the Motor service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLM1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLM1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLM1.LOG', running the generator with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', empty path prefix and temporary file 'LS2WS' in '/tmp'. | medium | base/cntl/wsaup01.jcl:12-32 |
| WSIG-BR-023 | Generate the policy update web service | design note | THE policy web service build job SHALL generate the Commercial policy update web service for program LGUPOL01, using request and response layout SOAIPB1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLB1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsaup01.jcl:78-98 |
| WSIG-BR-024 | Generate the policy update web service | design note | THE policy web service build job SHALL write the Commercial service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLB1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLB1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLB1.LOG', running the generator with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', empty path prefix and temporary file 'LS2WS' in '/tmp'. | medium | base/cntl/wsaup01.jcl:78-98 |
| WSIG-BR-025 | Generate the policy update web service | design note | THE policy web service build job SHALL generate the Endowment policy update web service for program LGUPOL01, using request and response layout SOAIPE1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLE1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsaup01.jcl:56-76 |
| WSIG-BR-026 | Generate the policy update web service | design note | THE policy web service build job SHALL write the Endowment service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLE1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLE1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLE1.LOG', running the generator with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', empty path prefix and temporary file 'LS2WS' in '/tmp'. | medium | base/cntl/wsaup01.jcl:56-76 |
| WSIG-BR-027 | Define the house policy update service | design note | THE policy web service build job SHALL generate the House policy update web service for program LGUPOL01, using request and response layout SOAIPH1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLH1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsaup01.jcl:34-54 |
| WSIG-BR-028 | Define the house policy update service | design note | THE policy web service build job SHALL write the House service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLH1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLH1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLH1.LOG', running the generator with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', empty path prefix and temporary file 'LS2WS' in '/tmp'. | medium | base/cntl/wsaup01.jcl:34-54 |

### Worked examples

- WSIG-BR-021: Policy type = Motor; Program = LGUPOL01; Layout (REQMEM/RESPMEM) = SOAIPM1 → A web service is published at 'GENAPP/LGUPOLM1' that passes the SOAIPM1 layout to LGUPOL01 through its COMMAREA.
- WSIG-BR-022: Service = LGUPOLM1 → Files 'LGUPOLM1.wsbind' and 'LGUPOLM1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLM1.LOG' in genapp/logs.
- WSIG-BR-023: Policy type = Commercial; Program = LGUPOL01; Layout (REQMEM/RESPMEM) = SOAIPB1 → A web service is published at 'GENAPP/LGUPOLB1' that passes the SOAIPB1 layout to LGUPOL01 through its COMMAREA.
- WSIG-BR-024: Service = LGUPOLB1 → Files 'LGUPOLB1.wsbind' and 'LGUPOLB1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLB1.LOG' in genapp/logs.
- WSIG-BR-025: Policy type = Endowment; Program = LGUPOL01; Layout (REQMEM/RESPMEM) = SOAIPE1 → A web service is published at 'GENAPP/LGUPOLE1' that passes the SOAIPE1 layout to LGUPOL01 through its COMMAREA.
- WSIG-BR-026: Service = LGUPOLE1 → Files 'LGUPOLE1.wsbind' and 'LGUPOLE1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLE1.LOG' in genapp/logs.
- WSIG-BR-027: Policy type = House; Program = LGUPOL01; Layout (REQMEM/RESPMEM) = SOAIPH1 → A web service is published at 'GENAPP/LGUPOLH1' that passes the SOAIPH1 layout to LGUPOL01 through its COMMAREA.
- WSIG-BR-028: Service = LGUPOLH1 → Files 'LGUPOLH1.wsbind' and 'LGUPOLH1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLH1.LOG' in genapp/logs.

## Decision tables

#### Policy update web service by policy type

| Policy type | Layout and service URI for program LGUPOL01 | Rule |
|---|---|---|
| Motor | Layout SOAIPM1, URI GENAPP/LGUPOLM1 | WSIG-BR-021 |
| Commercial | Layout SOAIPB1, URI GENAPP/LGUPOLB1 | WSIG-BR-023 |
| Endowment | Layout SOAIPE1, URI GENAPP/LGUPOLE1 | WSIG-BR-025 |
| House | Layout SOAIPH1, URI GENAPP/LGUPOLH1 | WSIG-BR-027 |


## Design notes

- WSIG-BR-021: Provide an update-Motor-policy API operation at the stable path GENAPP/LGUPOLM1. Its request and response contract comes from the Motor layout SOAIPM1 and it routes to the shared policy update logic. The outbound proxy is build configuration.
- WSIG-BR-022: Publish the Motor update service description, binding and generation log as build artifacts named LGUPOLM1. The toolchain directories and temp settings go in build configuration.
- WSIG-BR-023: Provide an update-Commercial-policy API operation at the stable path GENAPP/LGUPOLB1. Its request and response contract comes from the Commercial layout SOAIPB1 and it routes to the shared policy update logic.
- WSIG-BR-024: Publish the Commercial update service description, binding and generation log as build artifacts named LGUPOLB1. Toolchain settings are build configuration.
- WSIG-BR-025: Provide an update-Endowment-policy API operation at the stable path GENAPP/LGUPOLE1. Its request and response contract comes from the Endowment layout SOAIPE1 and it routes to the shared policy update logic.
- WSIG-BR-026: Publish the Endowment update service description, binding and generation log as build artifacts named LGUPOLE1. Toolchain settings are build configuration.
- WSIG-BR-027: Provide an update-House-policy API operation at the stable path GENAPP/LGUPOLH1. Its request and response contract comes from the House layout SOAIPH1 and it routes to the shared policy update logic.
- WSIG-BR-028: Publish the House update service description, binding and generation log as build artifacts named LGUPOLH1. Toolchain settings are build configuration.

## Open questions

- SME-111: The add-policy and update-policy web services each call one shared program for all four policy types (Commercial, Endowment, House, Motor), with a different request and response layout for each type. Should the new system keep one shared operation with four type-specific contracts, merge the contracts, or define a separate operation for each type? (Integration architect) On WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.
- SME-112: The four policy-type web services for add-policy and for update-policy each have a single trigger, but each is documented as its own single-step job. Should the four be generated together in one job or as independent jobs, and if one fails, what should happen to the others? (Operations) On WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.
- SME-113: Several generated binding files and WSDL files have no exact file names on record: add-policy Commercial, House and Endowment; inquiry House; customer update; update-policy Endowment and Commercial. Some recorded names also look irregular, such as 'HousePolicyWebServiceGenerationParameters' and 'WebServiceGenerationRequest.ws_bind'. What exact names must these files have for downstream consumers? Should they follow one convention, such as <service>.wsbind and <service>.wsdl? (Integration team) On WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.
- SME-114: Some policy service variants don't state their runtime settings (Java directory, installation directory, path prefix, temporary directory and temporary file prefix): add-policy Endowment and Motor, the LGIPOLM1 and multiple-return inquiry variants, and update-policy House. Do they use the same settings as the other variants? (Platform engineering) On WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
