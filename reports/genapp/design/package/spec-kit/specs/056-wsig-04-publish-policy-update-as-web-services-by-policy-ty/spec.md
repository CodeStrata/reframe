# Feature specification: Publish policy update as web services by policy type

**Feature:** WSIG-C04 · Web Service Interface Generation · Web Service Interface Generation

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (WSIG-C04)

As an integration developer, I want the policy update program published as a separate web service for each policy type, so that other applications can update Motor, Commercial, Endowment and House policies as web services.

Publishes updating a policy as four web services, one for each policy type (Motor, Commercial, Endowment and House). All four are served by the same policy update program, but each has its own address and its own policy-type layout. It serves integration developers whose systems change existing policies. It must never accept an update in another policy type's layout, and it must keep the addresses GENAPP/LGUPOLM1, GENAPP/LGUPOLB1, GENAPP/LGUPOLE1 and GENAPP/LGUPOLH1 stable.

**Acceptance scenarios:**

1. **Given** Policy type: Motor; Program: LGUPOL01; Layout (REQMEM/RESPMEM): SOAIPM1, **when** policy web service build job runs, **then** A web service is published at 'GENAPP/LGUPOLM1' that passes the SOAIPM1 layout to LGUPOL01 through its COMMAREA. (WSIG-C04-AC-01)
2. **Given** Service: LGUPOLM1, **when** policy web service build job runs, **then** Files 'LGUPOLM1.wsbind' and 'LGUPOLM1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLM1.LOG' in genapp/logs. (WSIG-C04-AC-02)
3. **Given** Policy type: Commercial; Program: LGUPOL01; Layout (REQMEM/RESPMEM): SOAIPB1, **when** policy web service build job runs, **then** A web service is published at 'GENAPP/LGUPOLB1' that passes the SOAIPB1 layout to LGUPOL01 through its COMMAREA. (WSIG-C04-AC-03)
4. **Given** Service: LGUPOLB1, **when** policy web service build job runs, **then** Files 'LGUPOLB1.wsbind' and 'LGUPOLB1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLB1.LOG' in genapp/logs. (WSIG-C04-AC-04)
5. **Given** Policy type: Endowment; Program: LGUPOL01; Layout (REQMEM/RESPMEM): SOAIPE1, **when** policy web service build job runs, **then** A web service is published at 'GENAPP/LGUPOLE1' that passes the SOAIPE1 layout to LGUPOL01 through its COMMAREA. (WSIG-C04-AC-05)
6. **Given** Service: LGUPOLE1, **when** policy web service build job runs, **then** Files 'LGUPOLE1.wsbind' and 'LGUPOLE1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLE1.LOG' in genapp/logs. (WSIG-C04-AC-06)
7. **Given** Policy type: House; Program: LGUPOL01; Layout (REQMEM/RESPMEM): SOAIPH1, **when** policy web service build job runs, **then** A web service is published at 'GENAPP/LGUPOLH1' that passes the SOAIPH1 layout to LGUPOL01 through its COMMAREA. (WSIG-C04-AC-07)
8. **Given** Service: LGUPOLH1, **when** policy web service build job runs, **then** Files 'LGUPOLH1.wsbind' and 'LGUPOLH1.wsdl' appear in genapp/wsdir and 'LS2WS_LGUPOLH1.LOG' in genapp/logs. (WSIG-C04-AC-08)

## Requirements

### Functional requirements

- **WSIG-REQ-F-018** (design note): The system shall generate the Motor policy update web service for program LGUPOL01, using request and response layout SOAIPM1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLM1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. Rules: WSIG-BR-021.
- **WSIG-REQ-F-019** (design note): The system shall write the Motor service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLM1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLM1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLM1.LOG'. Rules: WSIG-BR-022.
- **WSIG-REQ-F-020** (design note): The system shall generate the Commercial policy update web service for program LGUPOL01, using request and response layout SOAIPB1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLB1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. Rules: WSIG-BR-023.
- **WSIG-REQ-F-021** (design note): The system shall write the Commercial service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLB1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLB1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLB1.LOG'. Rules: WSIG-BR-024.
- **WSIG-REQ-F-022** (design note): The system shall generate the Endowment policy update web service for program LGUPOL01, using request and response layout SOAIPE1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLE1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. Rules: WSIG-BR-025.
- **WSIG-REQ-F-023** (design note): The system shall write the Endowment service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLE1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLE1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLE1.LOG'. Rules: WSIG-BR-026.
- **WSIG-REQ-F-024** (design note): The system shall generate the House policy update web service for program LGUPOL01, using request and response layout SOAIPH1 from the source library, a COMMAREA interface, URI 'GENAPP/LGUPOLH1' and proxy 'PROXY.HURSLEY.IBM.COM:80'. Rules: WSIG-BR-027.
- **WSIG-REQ-F-025** (design note): The system shall write the House service binding to '<ZFSHOME>/genapp/wsdir/LGUPOLH1.wsbind', its service description to '<ZFSHOME>/genapp/wsdir/LGUPOLH1.wsdl' and its log to '<ZFSHOME>/genapp/logs/LS2WS_LGUPOLH1.LOG'. Rules: WSIG-BR-028.
- **WSIG-REQ-N-005** (design note): The system shall run each policy update generation with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', empty path prefix and temporary file 'LS2WS' in '/tmp'. Rules: WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.

### Business rules

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

### Key entities

None found in the source.

### Needs clarification

- SME-111: The add-policy and update-policy web services each call one shared program for all four policy types (Commercial, Endowment, House, Motor), with a different request and response layout for each type. Should the new system keep one shared operation with four type-specific contracts, merge the contracts, or define a separate operation for each type? (Integration architect) On WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.
- SME-112: The four policy-type web services for add-policy and for update-policy each have a single trigger, but each is documented as its own single-step job. Should the four be generated together in one job or as independent jobs, and if one fails, what should happen to the others? (Operations) On WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.
- SME-113: Several generated binding files and WSDL files have no exact file names on record: add-policy Commercial, House and Endowment; inquiry House; customer update; update-policy Endowment and Commercial. Some recorded names also look irregular, such as 'HousePolicyWebServiceGenerationParameters' and 'WebServiceGenerationRequest.ws_bind'. What exact names must these files have for downstream consumers? Should they follow one convention, such as <service>.wsbind and <service>.wsdl? (Integration team) On WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.
- SME-114: Some policy service variants don't state their runtime settings (Java directory, installation directory, path prefix, temporary directory and temporary file prefix): add-policy Endowment and Motor, the LGIPOLM1 and multiple-return inquiry variants, and update-policy House. Do they use the same settings as the other variants? (Platform engineering) On WSIG-BR-022, WSIG-BR-024, WSIG-BR-026, WSIG-BR-028.

### Decision table gaps

None.
