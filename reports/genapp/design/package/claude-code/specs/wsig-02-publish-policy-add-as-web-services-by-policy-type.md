# Publish policy add as web services by policy type (WSIG-C02)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| WSIG-BR-011 | Generate the Motor Policy add web service artifacts | design note | THE web service generation job SHALL expose the policy add program LGAPOL01 as the Motor Policy web service at URI 'GENAPP/LGAPOLM1', using COBOL copybook member SOAIPM1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLM1.wsbind and LGAPOLM1.wsdl and log LS2WS_LGAPOLM1.LOG. | medium | base/cntl/wsaap01.jcl:12-32 |
| WSIG-BR-012 | Generate the endowment policy web service | design note | THE web service generation job SHALL expose the policy add program LGAPOL01 as the Endowment Policy web service at URI 'GENAPP/LGAPOLE1', using COBOL copybook member SOAIPE1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLE1.wsbind and LGAPOLE1.wsdl and log LS2WS_LGAPOLE1.LOG. | medium | base/cntl/wsaap01.jcl:56-76 |
| WSIG-BR-013 | Generate the endowment policy web service | design note | THE web service generation job SHALL expose the policy add program LGAPOL01 as the House Policy web service at URI 'GENAPP/LGAPOLH1', using COBOL copybook member SOAIPH1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLH1.wsbind, LGAPOLH1.wsdl and log LS2WS_LGAPOLH1.LOG, with Java 'java601_bit64_ga/J6.0.1_64' and CICS directory 'cics660'. | medium | base/cntl/wsaap01.jcl:34-54 |
| WSIG-BR-014 | Generate the endowment policy web service | design note | THE web service generation job SHALL expose the policy add program LGAPOL01 as the Commercial Policy web service at URI 'GENAPP/LGAPOLB1', using COBOL copybook member SOAIPB1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLB1.wsbind, LGAPOLB1.wsdl and log LS2WS_LGAPOLB1.LOG, with Java 'java601_bit64_ga/J6.0.1_64' and CICS directory 'cics660'. | medium | base/cntl/wsaap01.jcl:78-98 |

### Worked examples

- WSIG-BR-011: Job step = LS2WS (Motor Policy) → <ZFSHOME>/genapp/wsdir/LGAPOLM1.wsbind and LGAPOLM1.wsdl are produced for URI GENAPP/LGAPOLM1
- WSIG-BR-012: Job step = LS2WS (Endowment Policy) → <ZFSHOME>/genapp/wsdir/LGAPOLE1.wsbind and LGAPOLE1.wsdl are produced for URI GENAPP/LGAPOLE1
- WSIG-BR-013: Job step = LS2WS (House Policy) → <ZFSHOME>/genapp/wsdir/LGAPOLH1.wsbind and LGAPOLH1.wsdl are produced for URI GENAPP/LGAPOLH1
- WSIG-BR-014: Job step = LS2WS (Commercial Policy) → <ZFSHOME>/genapp/wsdir/LGAPOLB1.wsbind and LGAPOLB1.wsdl are produced for URI GENAPP/LGAPOLB1

## Decision tables

#### Policy add web service by policy type

| Policy type | Service URI, copybook and output files for program LGAPOL01 | Rule |
|---|---|---|
| Motor | URI GENAPP/LGAPOLM1, copybook SOAIPM1, LGAPOLM1.wsbind, LGAPOLM1.wsdl, log LS2WS_LGAPOLM1.LOG | WSIG-BR-011 |
| Endowment | URI GENAPP/LGAPOLE1, copybook SOAIPE1, LGAPOLE1.wsbind, LGAPOLE1.wsdl, log LS2WS_LGAPOLE1.LOG | WSIG-BR-012 |
| House | URI GENAPP/LGAPOLH1, copybook SOAIPH1, LGAPOLH1.wsbind, LGAPOLH1.wsdl, log LS2WS_LGAPOLH1.LOG | WSIG-BR-013 |
| Commercial | URI GENAPP/LGAPOLB1, copybook SOAIPB1, LGAPOLB1.wsbind, LGAPOLB1.wsdl, log LS2WS_LGAPOLB1.LOG | WSIG-BR-014 |


## Design notes

- WSIG-BR-011: Provide an add-Motor-policy API operation at the stable path GENAPP/LGAPOLM1. Its contract comes from the Motor policy layout SOAIPM1 and it routes to the shared policy add logic. Publish its service description, binding and log named LGAPOLM1. The outbound proxy is build configuration.
- WSIG-BR-012: Provide an add-Endowment-policy API operation at the stable path GENAPP/LGAPOLE1. Its contract comes from the Endowment layout SOAIPE1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLE1.
- WSIG-BR-013: Provide an add-House-policy API operation at the stable path GENAPP/LGAPOLH1. Its contract comes from the House layout SOAIPH1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLH1. The Java and platform directory settings are build-environment configuration.
- WSIG-BR-014: Provide an add-Commercial-policy API operation at the stable path GENAPP/LGAPOLB1. Its contract comes from the Commercial layout SOAIPB1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLB1. Toolchain settings are build configuration.

## Open questions

- SME-108: The web service generation jobs use fixed settings from the legacy installation: Java directory java601_bit64_ga/J6.0.1_64, installation directory cics660, and HTTP proxy PROXY.HURSLEY.IBM.COM:80. Should the new system keep these values, replace them with equivalents, or make them configurable per environment? Is the proxy still needed at all? (Platform engineering) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-109: Output and log paths use the placeholders <ZFSHOME> and <SOURCEX>, and the source library is also a placeholder. What are the real base directory and source library in the target environment, and how should they be supplied to the new system? (Platform engineering) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-111: The add-policy and update-policy web services each call one shared program for all four policy types (Commercial, Endowment, House, Motor), with a different request and response layout for each type. Should the new system keep one shared operation with four type-specific contracts, merge the contracts, or define a separate operation for each type? (Integration architect) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-112: The four policy-type web services for add-policy and for update-policy each have a single trigger, but each is documented as its own single-step job. Should the four be generated together in one job or as independent jobs, and if one fails, what should happen to the others? (Operations) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-113: Several generated binding files and WSDL files have no exact file names on record: add-policy Commercial, House and Endowment; inquiry House; customer update; update-policy Endowment and Commercial. Some recorded names also look irregular, such as 'HousePolicyWebServiceGenerationParameters' and 'WebServiceGenerationRequest.ws_bind'. What exact names must these files have for downstream consumers? Should they follow one convention, such as <service>.wsbind and <service>.wsdl? (Integration team) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-114: Some policy service variants don't state their runtime settings (Java directory, installation directory, path prefix, temporary directory and temporary file prefix): add-policy Endowment and Motor, the LGIPOLM1 and multiple-return inquiry variants, and update-policy House. Do they use the same settings as the other variants? (Platform engineering) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-115: The Commercial and House add-policy service definitions are labelled 'Generate the endowment policy web service'. Is this label a mistake in the legacy documentation? (Application owner) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).
