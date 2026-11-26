# Requirements: Count transactions by request type and outcome (ADPLM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk low

## Introduction

Counts every insurance transaction by request type and outcome so operations administrators can see how many requests of each kind succeeded or failed. Each event adds one to a single named counter: outcome '00' for return code '00' and '99' for anything else. It must never count an event twice or under the wrong name, and it must count related request types such as '02ACUS' under their shared type.

**User story:** As an operations administrator, I want every transaction counted by request type and outcome, so that I can see how many requests of each kind succeeded or failed.

## Requirements

### Requirement 1: ADPLM-REQ-F-072 (design note)

#### Acceptance criteria

1. When the statistics program can read the return-code event container (DFHEP.DATA.00002), the system shall take the request type from event container DFHEP.DATA.00001 and the return code from DFHEP.DATA.00002. (rules ADPLM-BR-076)
2. GIVEN A statistics event whose event data holds request type '01IMOT' and whose return-code data holds '00' WHEN The statistics counter processes the event THEN The request type used for counting is '01IMOT' and the return code is '00', both taken from the event data and not from any request passed alongside it (ADPLM-C13-AC-06; ADPLM-BR-076)

### Requirement 2: ADPLM-REQ-F-073 (design note)

#### Acceptance criteria

1. When the event containers cannot be read and request data was passed, the system shall take the request type and return code from the request. (rules ADPLM-BR-077)
2. GIVEN event containers: absent; request type: 01ACUS; return code: 00 WHEN the event containers cannot be read and request data was passed THEN Request type '01ACUS' with return code '00' is counted (ADPLM-C13-AC-01; ADPLM-BR-077)

### Requirement 3: ADPLM-REQ-F-074 (error handling)

#### Acceptance criteria

1. If the event containers cannot be read and no request data was passed, then the system shall end without counting anything. (rules ADPLM-BR-078)
2. GIVEN event containers: absent; request length: 0 WHEN the event containers cannot be read and no request data was passed THEN The program returns and no counter is incremented (ADPLM-C13-AC-02; ADPLM-BR-078)

### Requirement 4: ADPLM-REQ-F-075 (business rule)

#### Acceptance criteria

1. When a statistics event arrives with request type '02ACUS', the system shall count it as '01ACUS'. (rules ADPLM-BR-079)
2. GIVEN request type: 02ACUS WHEN a statistics event arrives with request type '02ACUS' THEN Counted under '01ACUS' (ADPLM-C13-AC-03; ADPLM-BR-079)

### Requirement 5: ADPLM-REQ-F-076 (business rule)

#### Acceptance criteria

1. When a statistics event arrives with request type '02ICOM', '03ICOM' or '05ICOM', the system shall count it as '01ICOM', and shall count every other request type under its own value. (rules ADPLM-BR-080)
2. GIVEN request type: 03ICOM WHEN a statistics event arrives with request type '02ICOM', '03ICOM' or '05ICOM' THEN Counted under '01ICOM' (ADPLM-C13-AC-04; ADPLM-BR-080)

### Requirement 6: ADPLM-REQ-F-077 (side effect)

#### Acceptance criteria

1. The system shall add one to the counter named 'GENA' + request type + outcome in pool 'GENA', where the outcome is '00' for return code '00' and '99' for any other return code. (rules ADPLM-BR-081)
2. GIVEN Counter 'GENA01IMOT00' in pool 'GENA' holds 5 and counter 'GENA01IMOT99' holds 2 WHEN An event with request type '01IMOT' and return code '00' is counted, followed by an event with request type '01IMOT' and return code '90' THEN 'GENA01IMOT00' holds 6 and 'GENA01IMOT99' holds 3; no other counter changes (ADPLM-C13-AC-07; ADPLM-BR-081)

### Requirement 7: ADPLM-REQ-N-001 (historical artifact)

#### Acceptance criteria

1. The system shall fetch the counter's new value after incrementing it but shall not use that value. (rules ADPLM-BR-082)
2. GIVEN counter: GENA01ICOM00 WHEN transaction statistics counter runs THEN The value is read back and ignored (ADPLM-C13-AC-05; ADPLM-BR-082)
