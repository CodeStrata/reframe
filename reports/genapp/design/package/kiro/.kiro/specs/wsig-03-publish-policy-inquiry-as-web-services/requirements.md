# Requirements: Publish policy inquiry as web services (WSIG-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Web Service Interface Generation · Web Service Interface Generation · runs as scheduled job · risk low

## Introduction

Publishes policy lookup as web services: one inquiry service for each policy type (Motor, Commercial, House and Endowment), plus a mobile lookup that can return several policies in one response. It serves integration developers and mobile clients that need to read policies. It must never return a policy in a layout other than its type's layout, and it must keep the addresses GENAPP/LGIPOLM1, GENAPP/LGIPOLB1, GENAPP/LGIPOLH1, GENAPP/LGIPOLE1 and GENAPP/LGIPOL02 stable.

**User story:** As an integration developer, I want the policy inquiry programs published as web services for each policy type and for mobile multiple-return lookup, so that other applications can look up policies as web services.

## Requirements

### Requirement 1: WSIG-REQ-F-013 (design note)

#### Acceptance criteria

1. The system shall generate a web service for program 'IPPROGMB' from COBOL request structure 'POLLOOK' and response structure 'POLLOO2' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOL02', binding '<ZFSHOME>/genapp/wsdir/LGIPOL02.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOL02.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOL02.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-015)
2. GIVEN job: GENASOAP submitted; program: IPPROGMB WHEN Policy Inquiry Web Service Publication job (mobile multiple-return step) runs THEN A binding 'LGIPOL02.wsbind' and WSDL 'LGIPOL02.wsdl' are written under '<ZFSHOME>/genapp/wsdir', publishing the service at 'GENAPP/LGIPOL02'. (WSIG-C03-AC-01; WSIG-BR-015)

### Requirement 2: WSIG-REQ-F-014 (design note)

#### Acceptance criteria

1. The system shall generate the Motor Policy inquiry web service for program 'LGIPOL01' from COBOL request and response structure 'SOAIPM1' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOLM1', binding '<ZFSHOME>/genapp/wsdir/LGIPOLM1.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOLM1.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOLM1.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-016)
2. GIVEN job: GENASOAP submitted; policy type: Motor WHEN Policy Inquiry Web Service Publication job (Motor Policy step) runs THEN The motor policy inquiry service is published at 'GENAPP/LGIPOLM1', with 'LGIPOLM1.wsbind' and 'LGIPOLM1.wsdl' written under '<ZFSHOME>/genapp/wsdir'. (WSIG-C03-AC-02; WSIG-BR-016)

### Requirement 3: WSIG-REQ-F-015 (design note)

#### Acceptance criteria

1. The system shall generate the Commercial Policy inquiry web service for program 'LGIPOL01' from COBOL request and response structure 'SOAIPB1' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOLB1', binding '<ZFSHOME>/genapp/wsdir/LGIPOLB1.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOLB1.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOLB1.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-017)
2. GIVEN job: GENASOAP submitted; policy type: Commercial WHEN Policy Inquiry Web Service Publication job (Commercial Policy step) runs THEN The commercial policy inquiry service is published at 'GENAPP/LGIPOLB1', with 'LGIPOLB1.wsbind' and 'LGIPOLB1.wsdl' written under '<ZFSHOME>/genapp/wsdir'. (WSIG-C03-AC-03; WSIG-BR-017)

### Requirement 4: WSIG-REQ-F-016 (design note)

#### Acceptance criteria

1. The system shall generate the House Policy inquiry web service for program 'LGIPOL01' from COBOL request and response structure 'SOAIPH1' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOLH1', binding '<ZFSHOME>/genapp/wsdir/LGIPOLH1.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOLH1.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOLH1.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-018)
2. GIVEN job: GENASOAP submitted; policy type: House WHEN Policy Inquiry Web Service Publication job (House Policy step) runs THEN The house policy inquiry service is published at 'GENAPP/LGIPOLH1', with 'LGIPOLH1.wsbind' and 'LGIPOLH1.wsdl' written under '<ZFSHOME>/genapp/wsdir'. (WSIG-C03-AC-04; WSIG-BR-018)

### Requirement 5: WSIG-REQ-F-017 (design note)

#### Acceptance criteria

1. The system shall generate the Endowment Policy inquiry web service for program 'LGIPOL01' from COBOL request and response structure 'SOAIPE1' in library '<SOURCEX>', with COMMAREA interface, URI 'GENAPP/LGIPOLE1', binding '<ZFSHOME>/genapp/wsdir/LGIPOLE1.wsbind', WSDL '<ZFSHOME>/genapp/wsdir/LGIPOLE1.wsdl', log '<ZFSHOME>/genapp/logs/LS2WS_LGIPOLE1.LOG' and proxy 'PROXY.HURSLEY.IBM.COM:80'. (rules WSIG-BR-019)
2. GIVEN job: GENASOAP submitted; policy type: Endowment WHEN Policy Inquiry Web Service Publication job (Endowment Policy step) runs THEN The endowment policy inquiry service is published at 'GENAPP/LGIPOLE1', with 'LGIPOLE1.wsbind', 'LGIPOLE1.wsdl' and the log 'LS2WS_LGIPOLE1.LOG' written. (WSIG-C03-AC-05; WSIG-BR-019)

### Requirement 6: WSIG-REQ-N-004 (design note)

#### Acceptance criteria

1. The system shall run each policy inquiry generation step with Java directory 'java601_bit64_ga/J6.0.1_64', CICS directory 'cics660', an empty path prefix, temporary directory '/tmp' and temporary file prefix 'LS2WS'. (rules WSIG-BR-020, WSIG-BR-019)
2. GIVEN job: GENASOAP submitted; policy type: Endowment WHEN Policy Inquiry Web Service Publication job (Endowment Policy step) runs THEN The endowment policy inquiry service is published at 'GENAPP/LGIPOLE1', with 'LGIPOLE1.wsbind', 'LGIPOLE1.wsdl' and the log 'LS2WS_LGIPOLE1.LOG' written. (WSIG-C03-AC-05; WSIG-BR-019)
3. GIVEN step: LS2WSB (Commercial Policy) WHEN Policy Inquiry Web Service Publication job runs THEN The generator runs from Java 'java601_bit64_ga/J6.0.1_64' and CICS 'cics660', using '/tmp' with prefix 'LS2WS' for work files. (WSIG-C03-AC-06; WSIG-BR-020)
