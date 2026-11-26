# Feature specification: Count transactions by request type and outcome

**Feature:** ADPLM-C13 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C13)

As an operations administrator, I want every transaction counted by request type and outcome, so that I can see how many requests of each kind succeeded or failed.

Counts every insurance transaction by request type and outcome so operations administrators can see how many requests of each kind succeeded or failed. Each event adds one to a single named counter: outcome '00' for return code '00' and '99' for anything else. It must never count an event twice or under the wrong name, and it must count related request types such as '02ACUS' under their shared type.

**Acceptance scenarios:**

1. **Given** event containers: absent; request type: 01ACUS; return code: 00, **when** the event containers cannot be read and request data was passed, **then** Request type '01ACUS' with return code '00' is counted (ADPLM-C13-AC-01)
2. **Given** event containers: absent; request length: 0, **when** the event containers cannot be read and no request data was passed, **then** The program returns and no counter is incremented (ADPLM-C13-AC-02)
3. **Given** request type: 02ACUS, **when** a statistics event arrives with request type '02ACUS', **then** Counted under '01ACUS' (ADPLM-C13-AC-03)
4. **Given** request type: 03ICOM, **when** a statistics event arrives with request type '02ICOM', '03ICOM' or '05ICOM', **then** Counted under '01ICOM' (ADPLM-C13-AC-04)
5. **Given** counter: GENA01ICOM00, **when** transaction statistics counter runs, **then** The value is read back and ignored (ADPLM-C13-AC-05)
6. **Given** A statistics event whose event data holds request type '01IMOT' and whose return-code data holds '00', **when** The statistics counter processes the event, **then** The request type used for counting is '01IMOT' and the return code is '00', both taken from the event data and not from any request passed alongside it (ADPLM-C13-AC-06)
7. **Given** Counter 'GENA01IMOT00' in pool 'GENA' holds 5 and counter 'GENA01IMOT99' holds 2, **when** An event with request type '01IMOT' and return code '00' is counted, followed by an event with request type '01IMOT' and return code '90', **then** 'GENA01IMOT00' holds 6 and 'GENA01IMOT99' holds 3; no other counter changes (ADPLM-C13-AC-07)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-072** (design note): When the statistics program can read the return-code event container (DFHEP.DATA.00002), the system shall take the request type from event container DFHEP.DATA.00001 and the return code from DFHEP.DATA.00002. Rules: ADPLM-BR-076.
- **ADPLM-REQ-F-073** (design note): When the event containers cannot be read and request data was passed, the system shall take the request type and return code from the request. Rules: ADPLM-BR-077.
- **ADPLM-REQ-F-074** (error handling): If the event containers cannot be read and no request data was passed, then the system shall end without counting anything. Rules: ADPLM-BR-078.
- **ADPLM-REQ-F-075** (business rule): When a statistics event arrives with request type '02ACUS', the system shall count it as '01ACUS'. Rules: ADPLM-BR-079.
- **ADPLM-REQ-F-076** (business rule): When a statistics event arrives with request type '02ICOM', '03ICOM' or '05ICOM', the system shall count it as '01ICOM', and shall count every other request type under its own value. Rules: ADPLM-BR-080.
- **ADPLM-REQ-F-077** (side effect): The system shall add one to the counter named 'GENA' + request type + outcome in pool 'GENA', where the outcome is '00' for return code '00' and '99' for any other return code. Rules: ADPLM-BR-081.
- **ADPLM-REQ-N-001** (historical artifact): The system shall fetch the counter's new value after incrementing it but shall not use that value. Rules: ADPLM-BR-082.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-076 | Statistics event source selection and no-input exit | design note | WHEN the statistics program can read the return-code event container (DFHEP.DATA.00002), THE transaction statistics counter SHALL take the request type from event container DFHEP.DATA.00001 and the return code from DFHEP.DATA.00002. | medium | base/src/lgastat1.cbl:26-29, base/src/lgastat1.cbl:79-99 |
| ADPLM-BR-077 | Statistics event source selection and no-input exit | design note | WHEN the event containers cannot be read and request data was passed, THE transaction statistics counter SHALL take the request type and return code from the request. | medium | base/src/lgastat1.cbl:26-29, base/src/lgastat1.cbl:79-99 |
| ADPLM-BR-078 | Statistics event source selection and no-input exit | error handling | WHEN the event containers cannot be read and no request data was passed, THE transaction statistics counter SHALL end without counting anything. | medium | base/src/lgastat1.cbl:26-29, base/src/lgastat1.cbl:79-99 |
| ADPLM-BR-079 | Request type normalisation for statistics | business rule | WHEN a statistics event arrives with request type '02ACUS', THE transaction statistics counter SHALL count it as '01ACUS'. | medium | base/src/lgastat1.cbl:122-126 |
| ADPLM-BR-080 | Request type normalisation for statistics | business rule | WHEN a statistics event arrives with request type '02ICOM', '03ICOM' or '05ICOM', THE transaction statistics counter SHALL count it as '01ICOM'; every other request type is counted under its own value. | medium | base/src/lgastat1.cbl:122-126 |
| ADPLM-BR-081 | Outcome bucket and transaction counter increment | side effect | THE transaction statistics counter SHALL add one to the counter named 'GENA' + request type + outcome in pool 'GENA', where the outcome is '00' for return code '00' and '99' for any other return code. | medium | base/src/lgastat1.cbl:38-43, base/src/lgastat1.cbl:52, base/src/lgastat1.cbl:127-135 |
| ADPLM-BR-082 | Outcome bucket and transaction counter increment | historical artifact | THE transaction statistics counter SHALL fetch the counter's new value but not use it. | medium | base/src/lgastat1.cbl:38-43, base/src/lgastat1.cbl:52, base/src/lgastat1.cbl:127-135 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-043: For the usage statistics, what business transactions do the request codes 02ACUS, 02ICOM, 03ICOM and 05ICOM stand for? Is it intended that 04ICOM is not counted in the same group as 01ICOM? (Business analyst) On ADPLM-BR-080.
- DEF-054: Is this intended? Only the return-code container read is checked; if the request-type container DFHEP.DATA.00001 failed but 00002 succeeded, the counter would be built from an uninitialised request type. (Subject-matter expert) On ADPLM-BR-078.

### Decision table gaps

None.
