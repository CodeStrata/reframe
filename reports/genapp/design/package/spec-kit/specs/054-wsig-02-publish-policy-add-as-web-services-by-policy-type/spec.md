# Feature specification: Publish policy add as web services by policy type

**Feature:** WSIG-C02 · Web Service Interface Generation · Web Service Interface Generation

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (WSIG-C02)

As an integration developer, I want the policy add program published as a separate web service for each policy type, so that other applications can add Motor, Endowment, House and Commercial policies as web services.

Publishes adding a policy as four web services, one for each policy type (Motor, Endowment, House and Commercial). All four are served by the same policy add program, but each has its own address and its own policy-type layout. It serves integration developers whose systems create policies. It must never send a request to the wrong policy type's layout, and it must never change the addresses GENAPP/LGAPOLM1, GENAPP/LGAPOLE1, GENAPP/LGAPOLH1 and GENAPP/LGAPOLB1.

**Acceptance scenarios:**

1. **Given** Job step: LS2WS (Motor Policy), **when** web service generation job runs, **then** <ZFSHOME>/genapp/wsdir/LGAPOLM1.wsbind and LGAPOLM1.wsdl are produced for URI GENAPP/LGAPOLM1 (WSIG-C02-AC-01)
2. **Given** Job step: LS2WS (Endowment Policy), **when** web service generation job runs, **then** <ZFSHOME>/genapp/wsdir/LGAPOLE1.wsbind and LGAPOLE1.wsdl are produced for URI GENAPP/LGAPOLE1 (WSIG-C02-AC-02)
3. **Given** Job step: LS2WS (House Policy), **when** web service generation job runs, **then** <ZFSHOME>/genapp/wsdir/LGAPOLH1.wsbind and LGAPOLH1.wsdl are produced for URI GENAPP/LGAPOLH1 (WSIG-C02-AC-03)
4. **Given** Job step: LS2WS (Commercial Policy), **when** web service generation job runs, **then** <ZFSHOME>/genapp/wsdir/LGAPOLB1.wsbind and LGAPOLB1.wsdl are produced for URI GENAPP/LGAPOLB1 (WSIG-C02-AC-04)

## Requirements

### Functional requirements

- **WSIG-REQ-F-009** (design note): The system shall expose the policy add program LGAPOL01 as the Motor Policy web service at URI 'GENAPP/LGAPOLM1', using COBOL copybook member SOAIPM1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLM1.wsbind, LGAPOLM1.wsdl and log LS2WS_LGAPOLM1.LOG. Rules: WSIG-BR-011.
- **WSIG-REQ-F-010** (design note): The system shall expose the policy add program LGAPOL01 as the Endowment Policy web service at URI 'GENAPP/LGAPOLE1', using COBOL copybook member SOAIPE1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLE1.wsbind, LGAPOLE1.wsdl and log LS2WS_LGAPOLE1.LOG. Rules: WSIG-BR-012.
- **WSIG-REQ-F-011** (design note): The system shall expose the policy add program LGAPOL01 as the House Policy web service at URI 'GENAPP/LGAPOLH1', using COBOL copybook member SOAIPH1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLH1.wsbind, LGAPOLH1.wsdl and log LS2WS_LGAPOLH1.LOG. Rules: WSIG-BR-013.
- **WSIG-REQ-F-012** (design note): The system shall expose the policy add program LGAPOL01 as the Commercial Policy web service at URI 'GENAPP/LGAPOLB1', using COBOL copybook member SOAIPB1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLB1.wsbind, LGAPOLB1.wsdl and log LS2WS_LGAPOLB1.LOG. Rules: WSIG-BR-014.
- **WSIG-REQ-N-003** (design note): The system shall generate the House Policy and Commercial Policy add web services with Java 'java601_bit64_ga/J6.0.1_64' and CICS directory 'cics660'. Rules: WSIG-BR-013, WSIG-BR-014.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| WSIG-BR-011 | Generate the Motor Policy add web service artifacts | design note | THE web service generation job SHALL expose the policy add program LGAPOL01 as the Motor Policy web service at URI 'GENAPP/LGAPOLM1', using COBOL copybook member SOAIPM1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLM1.wsbind and LGAPOLM1.wsdl and log LS2WS_LGAPOLM1.LOG. | medium | base/cntl/wsaap01.jcl:12-32 |
| WSIG-BR-012 | Generate the endowment policy web service | design note | THE web service generation job SHALL expose the policy add program LGAPOL01 as the Endowment Policy web service at URI 'GENAPP/LGAPOLE1', using COBOL copybook member SOAIPE1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLE1.wsbind and LGAPOLE1.wsdl and log LS2WS_LGAPOLE1.LOG. | medium | base/cntl/wsaap01.jcl:56-76 |
| WSIG-BR-013 | Generate the endowment policy web service | design note | THE web service generation job SHALL expose the policy add program LGAPOL01 as the House Policy web service at URI 'GENAPP/LGAPOLH1', using COBOL copybook member SOAIPH1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLH1.wsbind, LGAPOLH1.wsdl and log LS2WS_LGAPOLH1.LOG, with Java 'java601_bit64_ga/J6.0.1_64' and CICS directory 'cics660'. | medium | base/cntl/wsaap01.jcl:34-54 |
| WSIG-BR-014 | Generate the endowment policy web service | design note | THE web service generation job SHALL expose the policy add program LGAPOL01 as the Commercial Policy web service at URI 'GENAPP/LGAPOLB1', using COBOL copybook member SOAIPB1 for request and response, COMMAREA passing and proxy PROXY.HURSLEY.IBM.COM:80, writing LGAPOLB1.wsbind, LGAPOLB1.wsdl and log LS2WS_LGAPOLB1.LOG, with Java 'java601_bit64_ga/J6.0.1_64' and CICS directory 'cics660'. | medium | base/cntl/wsaap01.jcl:78-98 |

### Key entities

None found in the source.

### Needs clarification

- SME-108: The web service generation jobs use fixed settings from the legacy installation: Java directory java601_bit64_ga/J6.0.1_64, installation directory cics660, and HTTP proxy PROXY.HURSLEY.IBM.COM:80. Should the new system keep these values, replace them with equivalents, or make them configurable per environment? Is the proxy still needed at all? (Platform engineering) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-109: Output and log paths use the placeholders <ZFSHOME> and <SOURCEX>, and the source library is also a placeholder. What are the real base directory and source library in the target environment, and how should they be supplied to the new system? (Platform engineering) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-111: The add-policy and update-policy web services each call one shared program for all four policy types (Commercial, Endowment, House, Motor), with a different request and response layout for each type. Should the new system keep one shared operation with four type-specific contracts, merge the contracts, or define a separate operation for each type? (Integration architect) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-112: The four policy-type web services for add-policy and for update-policy each have a single trigger, but each is documented as its own single-step job. Should the four be generated together in one job or as independent jobs, and if one fails, what should happen to the others? (Operations) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-113: Several generated binding files and WSDL files have no exact file names on record: add-policy Commercial, House and Endowment; inquiry House; customer update; update-policy Endowment and Commercial. Some recorded names also look irregular, such as 'HousePolicyWebServiceGenerationParameters' and 'WebServiceGenerationRequest.ws_bind'. What exact names must these files have for downstream consumers? Should they follow one convention, such as <service>.wsbind and <service>.wsdl? (Integration team) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-114: Some policy service variants don't state their runtime settings (Java directory, installation directory, path prefix, temporary directory and temporary file prefix): add-policy Endowment and Motor, the LGIPOLM1 and multiple-return inquiry variants, and update-policy House. Do they use the same settings as the other variants? (Platform engineering) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
- SME-115: The Commercial and House add-policy service definitions are labelled 'Generate the endowment policy web service'. Is this label a mistake in the legacy documentation? (Application owner) On WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.

### Decision table gaps

None.
