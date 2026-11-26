# Design: Publish policy inquiry as web services (WSIG-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Publishes policy lookup as web services: one inquiry service for each policy type (Motor, Commercial, House and Endowment), plus a mobile lookup that can return several policies in one response. It serves integration developers and mobile clients that need to read policies. It must never return a policy in a layout other than its type's layout, and it must keep the addresses GENAPP/LGIPOLM1, GENAPP/LGIPOLB1, GENAPP/LGIPOLH1, GENAPP/LGIPOLE1 and GENAPP/LGIPOL02 stable.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| WSIG-BR-015 | Generate the policy inquiry service binding and WSDL | design note | THE Policy Inquiry Web Service Publication job (mobile multiple-return step) SHALL generate a web service for program 'IPPROGMB' from COBOL request structure 'POLLOOK' and response structure 'POLLOO2' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOL02', binding '<ZFSHOME>/genapp/wsdir/LGIPOL02.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOL02.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOL02.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsaip01.jcl:1-2, base/cntl/wsaip01.jcl:100-121 |
| WSIG-BR-016 | Generate the policy inquiry web service definition | design note | THE Policy Inquiry Web Service Publication job (Motor Policy step) SHALL generate a web service for program 'LGIPOL01' from COBOL request and response structure 'SOAIPM1' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOLM1', binding '<ZFSHOME>/genapp/wsdir/LGIPOLM1.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOLM1.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOLM1.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsaip01.jcl:11-33 |
| WSIG-BR-017 | Generate commercial policy inquiry web service | design note | THE Policy Inquiry Web Service Publication job (Commercial Policy step) SHALL generate a web service for program 'LGIPOL01' from COBOL request and response structure 'SOAIPB1' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOLB1', binding '<ZFSHOME>/genapp/wsdir/LGIPOLB1.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOLB1.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOLB1.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsaip01.jcl:78-99 |
| WSIG-BR-018 | Generate House Policy inquiry web service | design note | THE Policy Inquiry Web Service Publication job (House Policy step) SHALL generate a web service for program 'LGIPOL01' from COBOL request and response structure 'SOAIPH1' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOLH1', binding '<ZFSHOME>/genapp/wsdir/LGIPOLH1.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOLH1.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOLH1.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsaip01.jcl:34-55 |
| WSIG-BR-019 | Generate endowment policy inquiry web service artifacts | design note | THE Policy Inquiry Web Service Publication job (Endowment Policy step) SHALL generate a web service for program 'LGIPOL01' from COBOL request and response structure 'SOAIPE1' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOLE1', binding '<ZFSHOME>/genapp/wsdir/LGIPOLE1.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOLE1.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOLE1.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80', running with Java 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix and temporary files '/tmp' 'LS2WS'. | medium | base/cntl/wsaip01.jcl:56-77 |
| WSIG-BR-020 | Generate commercial policy inquiry web service | design note | THE Policy Inquiry Web Service Publication job SHALL run each generation step with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS'. | medium | base/cntl/wsaip01.jcl:78-99 |

### Worked examples

- WSIG-BR-015: job = GENASOAP submitted; program = IPPROGMB → A binding 'LGIPOL02.wsbind' and WSDL 'LGIPOL02.wsdl' are written under '<ZFSHOME>/genapp/wsdir', publishing the service at 'GENAPP/LGIPOL02'.
- WSIG-BR-016: job = GENASOAP submitted; policy type = Motor → The motor policy inquiry service is published at 'GENAPP/LGIPOLM1', with 'LGIPOLM1.wsbind' and 'LGIPOLM1.wsdl' written under '<ZFSHOME>/genapp/wsdir'.
- WSIG-BR-017: job = GENASOAP submitted; policy type = Commercial → The commercial policy inquiry service is published at 'GENAPP/LGIPOLB1', with 'LGIPOLB1.wsbind' and 'LGIPOLB1.wsdl' written under '<ZFSHOME>/genapp/wsdir'.
- WSIG-BR-018: job = GENASOAP submitted; policy type = House → The house policy inquiry service is published at 'GENAPP/LGIPOLH1', with 'LGIPOLH1.wsbind' and 'LGIPOLH1.wsdl' written under '<ZFSHOME>/genapp/wsdir'.
- WSIG-BR-019: job = GENASOAP submitted; policy type = Endowment → The endowment policy inquiry service is published at 'GENAPP/LGIPOLE1', with 'LGIPOLE1.wsbind', 'LGIPOLE1.wsdl' and the log 'LS2WS_LGIPOLE1.LOG' written.
- WSIG-BR-020: step = LS2WSB (Commercial Policy) → The generator runs from Java 'java601_bit64_ga/J6.0.1_64' and CICS 'cics660', using '/tmp' with prefix 'LS2WS' for work files.

## Decision tables

#### Policy inquiry web service by step

| Inquiry step | Program, structures, service URI and output files | Rule |
|---|---|---|
| Mobile multiple-return | Program IPPROGMB, request POLLOOK, response POLLOO2, URI GENAPP/LGIPOL02, LGIPOL02.wsbind/.wsdl, log LS2WS_LGIPOL02.LOG | WSIG-BR-015 |
| Motor Policy | Program LGIPOL01, structure SOAIPM1, URI GENAPP/LGIPOLM1, LGIPOLM1.wsbind/.wsdl, log LS2WS_LGIPOLM1.LOG | WSIG-BR-016 |
| Commercial Policy | Program LGIPOL01, structure SOAIPB1, URI GENAPP/LGIPOLB1, LGIPOLB1.wsbind/.wsdl, log LS2WS_LGIPOLB1.LOG | WSIG-BR-017 |
| House Policy | Program LGIPOL01, structure SOAIPH1, URI GENAPP/LGIPOLH1, LGIPOLH1.wsbind/.wsdl, log LS2WS_LGIPOLH1.LOG | WSIG-BR-018 |
| Endowment Policy | Program LGIPOL01, structure SOAIPE1, URI GENAPP/LGIPOLE1, LGIPOLE1.wsbind/.wsdl, log LS2WS_LGIPOLE1.LOG | WSIG-BR-019 |


## Design notes

- WSIG-BR-015: Provide a read-only mobile policy lookup API operation at the stable path GENAPP/LGIPOL02 that can return several policies in one response. Its request contract comes from POLLOOK and its response contract from POLLOO2. Publish its service description, binding and log named LGIPOL02.
- WSIG-BR-016: Provide a read-only Motor policy inquiry API operation at the stable path GENAPP/LGIPOLM1. Its request and response contract comes from the Motor layout SOAIPM1 and it routes to the shared policy inquiry logic. Publish its artifacts named LGIPOLM1.
- WSIG-BR-017: Provide a read-only Commercial policy inquiry API operation at the stable path GENAPP/LGIPOLB1. Its request and response contract comes from the Commercial layout SOAIPB1. Publish its artifacts named LGIPOLB1.
- WSIG-BR-018: Provide a read-only House policy inquiry API operation at the stable path GENAPP/LGIPOLH1. Its request and response contract comes from the House layout SOAIPH1. Publish its artifacts named LGIPOLH1.
- WSIG-BR-019: Provide a read-only Endowment policy inquiry API operation at the stable path GENAPP/LGIPOLE1. Its request and response contract comes from the Endowment layout SOAIPE1. Publish its artifacts named LGIPOLE1.
- WSIG-BR-020: Generate all five policy inquiry contracts in one repeatable build step. The runtime, platform directory, temp location and file-prefix settings it needs are shared build-environment configuration, not per-service code.

## Open questions

- SME-107: When generating web service files fails (for example, a structure member is missing, the output directory can't be written, or the proxy can't be reached), what should happen: should the job fail, retry, or leave partial files behind? And when a job is run again, should it overwrite the existing binding, WSDL and log files or fail because they already exist? (Operations) On WSIG-BR-015, WSIG-BR-016, WSIG-BR-020, WSIG-BR-018, WSIG-BR-019.
- SME-113: Several generated binding files and WSDL files have no exact file names on record: add-policy Commercial, House and Endowment; inquiry House; customer update; update-policy Endowment and Commercial. Some recorded names also look irregular, such as 'HousePolicyWebServiceGenerationParameters' and 'WebServiceGenerationRequest.ws_bind'. What exact names must these files have for downstream consumers? Should they follow one convention, such as <service>.wsbind and <service>.wsdl? (Integration team) On WSIG-BR-015, WSIG-BR-016, WSIG-BR-020, WSIG-BR-018, WSIG-BR-019.
- SME-114: Some policy service variants don't state their runtime settings (Java directory, installation directory, path prefix, temporary directory and temporary file prefix): add-policy Endowment and Motor, the LGIPOLM1 and multiple-return inquiry variants, and update-policy House. Do they use the same settings as the other variants? (Platform engineering) On WSIG-BR-015, WSIG-BR-016, WSIG-BR-020, WSIG-BR-018, WSIG-BR-019.
- SME-116: The commercial, endowment, house and LGIPOLM1 policy inquiry services all point to the same program but use different request and response layouts. Is one program meant to serve all of these policy types, or is the program name a copy error in some of them? (Application architect) On WSIG-BR-015, WSIG-BR-016, WSIG-BR-020, WSIG-BR-018, WSIG-BR-019.
- SME-117: The multiple-return policy inquiry service (POLLOOK/POLLOO2, URI GENAPP/LGIPOL02) is grouped with house policy publication but calls a different program. Does it belong with the other policy inquiry services, and which policy type does it serve? (Application architect) On WSIG-BR-015, WSIG-BR-016, WSIG-BR-020, WSIG-BR-018, WSIG-BR-019.
- SME-118: One job triggers the policy inquiry services, but five service definitions are described. Which of them does that job actually generate, and in what order? (Operations) On WSIG-BR-015, WSIG-BR-016, WSIG-BR-020, WSIG-BR-018, WSIG-BR-019.
- DEF-050: Is this intended? The mobile step reuses the step name LS2WSB already used by the Commercial Policy step, so the job has two steps with the same name; both still run, but any reference to the step by name is ambiguous. (Subject-matter expert) On WSIG-BR-015.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).