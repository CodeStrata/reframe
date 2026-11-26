# Design: Publish customer operations as web services (WSIG-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Publishes the four customer operations (add customer, customer inquiry, customer update and customer number lookup) as callable web services, each at its own fixed address with a published service description, so that other applications can work with customers without going through the screens. It serves integration developers and the systems they connect. It must never publish a service whose request or response layout differs from the layout the customer program actually uses, and it must never move a service address (GENAPP/LGACUS01, GENAPP/LGICUS01, GENAPP/LGUCUS01, GENAPP/LGICVS01) that callers depend on.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| WSIG-BR-001 | Generate customer add web service artifacts | design note | THE add-customer web service generation job SHALL expose the COBOL add-customer program LGACUS01 as a web service at relative address GENAPP/LGACUS01, passing data by COMMAREA and using the customer request and response layout SOAIC01 from library <SOURCEX>. | medium | base/cntl/wsaac01.jcl:11-31 |
| WSIG-BR-002 | Generate customer add web service artifacts | design note | THE add-customer web service generation job SHALL write the binding file to <ZFSHOME>/genapp/wsdir/LGACUS01.wsbind, the service description to <ZFSHOME>/genapp/wsdir/LGACUS01.wsdl and the generation log to <ZFSHOME>/genapp/logs/LS2WS_LGACUS01.LOG. | medium | base/cntl/wsaac01.jcl:11-31 |
| WSIG-BR-003 | Generate customer inquiry web service artifacts | design note | THE customer inquiry web service generation job SHALL expose the COBOL customer inquiry program LGICUS01 as a web service at relative address GENAPP/LGICUS01, passing data by COMMAREA and using the customer request and response layout SOAIC01 from library <SOURCEX>. | medium | base/cntl/wsaic01.jcl:11-31 |
| WSIG-BR-004 | Generate customer inquiry web service artifacts | design note | THE customer inquiry web service generation job SHALL write the binding file to <ZFSHOME>/genapp/wsdir/LGICUS01.wsbind, the service description to <ZFSHOME>/genapp/wsdir/LGICUS01.wsdl and the generation log to <ZFSHOME>/genapp/logs/LS2WS_LGICUS01.LOG. | medium | base/cntl/wsaic01.jcl:11-31 |
| WSIG-BR-005 | Generate customer update web service artifacts | design note | THE customer update web service set-up job SHALL run the CICS web service generation procedure (DFHLS2WS) for program 'LGUCUS01', using the COBOL copybook 'SOAIC01' for both request and response, service address 'GENAPP/LGUCUS01', COMMAREA data passing and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsauc01.jcl:11-31 |
| WSIG-BR-006 | Generate customer update web service artifacts | design note | THE customer update web service set-up job SHALL write the binding file '<ZFSHOME>/genapp/wsdir/LGUCUS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGUCUS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGUCUS01.LOG', running with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS'. | medium | base/cntl/wsauc01.jcl:11-31 |
| WSIG-BR-007 | Generate web service binding and WSDL | design note | THE customer number web service set-up job SHALL run the CICS web service generation procedure (DFHLS2WS) for program 'LGICVS01', using COBOL request copybook 'SOAVCII' and response copybook 'SOAVCIO' from the source library, service address 'GENAPP/LGICVS01', COMMAREA data passing and proxy 'PROXY.HURSLEY.IBM.COM:80'. | medium | base/cntl/wsavc01.jcl:11-31 |
| WSIG-BR-008 | Generate web service binding and WSDL | design note | THE customer number web service set-up job SHALL write the binding file '<ZFSHOME>/genapp/wsdir/LGICVS01.wsbind', the WSDL '<ZFSHOME>/genapp/wsdir/LGICVS01.wsdl' and the log '<ZFSHOME>/genapp/logs/LS2WS_LGICVS01.LOG', running with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS'. | medium | base/cntl/wsavc01.jcl:11-31 |
| WSIG-BR-009 | Generate customer add web service artifacts | design note | THE add-customer web service generation job SHALL run the CICS language-structure-to-WSDL procedure (DFHLS2WS) with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp', temporary file 'LS2WS' and HTTP proxy PROXY.HURSLEY.IBM.COM:80. | medium | base/cntl/wsaac01.jcl:11-31 |
| WSIG-BR-010 | Generate customer inquiry web service artifacts | design note | THE customer inquiry web service generation job SHALL run the CICS language-structure-to-WSDL procedure (DFHLS2WS) with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp', temporary file 'LS2WS' and HTTP proxy PROXY.HURSLEY.IBM.COM:80. | medium | base/cntl/wsaic01.jcl:11-31 |

### Worked examples

- WSIG-BR-001: program (PGMNAME) = LGACUS01; request/response layout (REQMEM/RESPMEM) = SOAIC01; URI = GENAPP/LGACUS01 → A web service for adding a customer is generated, reached at GENAPP/LGACUS01 and calling LGACUS01 through a COMMAREA.
- WSIG-BR-002: ZFSHOME = /u/genapp → Files /u/genapp/genapp/wsdir/LGACUS01.wsbind and LGACUS01.wsdl and log /u/genapp/genapp/logs/LS2WS_LGACUS01.LOG are produced.
- WSIG-BR-003: program (PGMNAME) = LGICUS01; request/response layout (REQMEM/RESPMEM) = SOAIC01; URI = GENAPP/LGICUS01 → A web service for inquiring on a customer is generated, reached at GENAPP/LGICUS01 and calling LGICUS01 through a COMMAREA.
- WSIG-BR-004: ZFSHOME = /u/genapp → Files /u/genapp/genapp/wsdir/LGICUS01.wsbind and LGICUS01.wsdl and log /u/genapp/genapp/logs/LS2WS_LGICUS01.LOG are produced.
- WSIG-BR-005: program (PGMNAME) = 'LGUCUS01'; request and response copybook (REQMEM, RESPMEM) = 'SOAIC01'; service address (URI) = 'GENAPP/LGUCUS01' → The customer update program is published as a web service at 'GENAPP/LGUCUS01' that passes its data through the COMMAREA.
- WSIG-BR-007: program (PGMNAME) = 'LGICVS01'; request copybook (REQMEM) = 'SOAVCII'; response copybook (RESPMEM) = 'SOAVCIO' → The program that obtains a customer number from the VSAM file is published as a web service at 'GENAPP/LGICVS01'.
- WSIG-BR-009: JAVADIR = 'java601_bit64_ga/J6.0.1_64'; HTTPPROXY = PROXY.HURSLEY.IBM.COM:80 → The generation runs with that Java runtime and reaches external resources through the Hursley proxy.
- WSIG-BR-010: TMPDIR = '/tmp'; TMPFILE = 'LS2WS' → The generation uses /tmp for its temporary files named with prefix LS2WS.

## Decision tables

#### Customer web service by operation

| Customer operation | Program, service address and request/response layout | Rule |
|---|---|---|
| Add customer | Program LGACUS01 at GENAPP/LGACUS01 using SOAIC01 for request and response | WSIG-BR-001 |
| Customer inquiry | Program LGICUS01 at GENAPP/LGICUS01 using SOAIC01 for request and response | WSIG-BR-003 |
| Customer update | Program LGUCUS01 at GENAPP/LGUCUS01 using SOAIC01 for request and response | WSIG-BR-005 |
| Customer number | Program LGICVS01 at GENAPP/LGICVS01 using request SOAVCII and response SOAVCIO | WSIG-BR-007 |


## Design notes

- WSIG-BR-001: Expose add customer as an API operation at the stable path GENAPP/LGACUS01. Its request and response contract comes from the one shared customer layout (SOAIC01), the same layout that inquiry and update use. Generate the contract from that layout so the two cannot drift apart.
- WSIG-BR-002: Publish the add-customer service description, any runtime binding, and a generation log as build artifacts named after the service (LGACUS01). Put them where the deployment step and callers can find them under the installation home. Generation failures must show up in that log.
- WSIG-BR-003: Expose customer inquiry as a read-only API operation at the stable path GENAPP/LGICUS01. It uses the shared customer layout SOAIC01 for both request and response.
- WSIG-BR-004: Publish the customer inquiry service description, binding and generation log as build artifacts named LGICUS01, in the same published-services and logs locations as the other customer services.
- WSIG-BR-005: Expose customer update as an API operation at the stable path GENAPP/LGUCUS01, with the shared customer layout SOAIC01 for both request and response. The legacy generator reached the network through PROXY.HURSLEY.IBM.COM:80. Make the build's outbound proxy a configuration setting, not a fixed value.
- WSIG-BR-006: Publish the customer update service description, binding and log as build artifacts named LGUCUS01. The legacy toolchain settings (Java 'java601_bit64_ga/J6.0.1_64', 'cics660', '/tmp', 'LS2WS') belong in build-environment configuration. They are not product behaviour.
- WSIG-BR-007: Expose customer number lookup as an API operation at the stable path GENAPP/LGICVS01. Unlike the other customer services, it has its own request layout (SOAVCII) and its own response layout (SOAVCIO), and the contract must keep those two shapes separate.
- WSIG-BR-008: Publish the customer number service description, binding and log as build artifacts named LGICVS01. The toolchain directories and temp-file settings go in build configuration.
- WSIG-BR-009: Contract generation for add customer runs as a repeatable build or pipeline step from the source layouts. The Java runtime, platform directory, temp location and HTTP proxy it needs become build-environment settings.
- WSIG-BR-010: Contract generation for customer inquiry runs in the same repeatable build step as add customer, with the same configurable runtime, temp location and proxy settings.

## Open questions

- SME-107: When generating web service files fails (for example, a structure member is missing, the output directory can't be written, or the proxy can't be reached), what should happen: should the job fail, retry, or leave partial files behind? And when a job is run again, should it overwrite the existing binding, WSDL and log files or fail because they already exist? (Operations) On WSIG-BR-010, WSIG-BR-009, WSIG-BR-006.
- SME-108: The web service generation jobs use fixed settings from the legacy installation: Java directory java601_bit64_ga/J6.0.1_64, installation directory cics660, and HTTP proxy PROXY.HURSLEY.IBM.COM:80. Should the new system keep these values, replace them with equivalents, or make them configurable per environment? Is the proxy still needed at all? (Platform engineering) On WSIG-BR-010, WSIG-BR-009, WSIG-BR-006.
- SME-109: Output and log paths use the placeholders <ZFSHOME> and <SOURCEX>, and the source library is also a placeholder. What are the real base directory and source library in the target environment, and how should they be supplied to the new system? (Platform engineering) On WSIG-BR-010, WSIG-BR-009.
- SME-110: Once the binding file and service description have been generated, how are they deployed? Is deployment part of this business function or a separate process? (Integration team) On WSIG-BR-009.
- SME-113: Several generated binding files and WSDL files have no exact file names on record: add-policy Commercial, House and Endowment; inquiry House; customer update; update-policy Endowment and Commercial. Some recorded names also look irregular, such as 'HousePolicyWebServiceGenerationParameters' and 'WebServiceGenerationRequest.ws_bind'. What exact names must these files have for downstream consumers? Should they follow one convention, such as <service>.wsbind and <service>.wsdl? (Integration team) On WSIG-BR-006.
- SME-119: The customer update web service has an empty path prefix. Is that deliberate, or is it a placeholder that each environment should fill in? (Platform engineering) On WSIG-BR-006.
- SME-120: When the step that generates the web service definition (binding and WSDL) runs, what counts as success and what counts as failure? For example: what should happen if the request or response layout is invalid or incomplete, or if the output cannot be written, and may partial output be left behind after a failure? This applies to both the customer and the policy web service generation jobs. (Integration team) On WSIG-BR-008.
- SME-121: Where exactly should the new system read the source layouts from and write the generated web service files to? Today these locations are unfilled placeholders (<SOURCEX> and <ZFSHOME>). (Platform/infrastructure team) On WSIG-BR-008.
- SME-122: Environment settings used to generate the web services are currently fixed: the network proxy (PROXY.HURSLEY.IBM.COM:80), the Java runtime directory, the CICS install directory, and the source and output locations. Should these stay fixed or become configurable settings in the new system? (Platform operations team) On WSIG-BR-008.
- SME-123: The customer number web service takes a request (SOAVCII) and returns a response (SOAVCIO). What business information does each of these carry, that is, what does the published service actually expose to callers? (Business analyst) On WSIG-BR-008.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).