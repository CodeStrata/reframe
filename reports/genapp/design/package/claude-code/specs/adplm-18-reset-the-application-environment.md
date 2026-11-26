# Reset the application environment (ADPLM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Lets an operator reset the application to a clean state that matches the restored customer database. The reset sets the customer number range (low 0000000001, high 0000000011 unless the operator gives another high number), seeds the next-customer-number counter, zeroes all 36 transaction statistics counters and clears the operational logs. It must always leave the control record and the next-customer counter in agreement, so that new customers do not collide with restored ones.

**User story:** As an operator, I want to run the setup transaction to reset the customer number range, statistics counters and operational queues, so that the application matches the restored customer database and starts from a clean state.

## Requirements

### Requirement 1: ADPLM-REQ-F-112 (business rule)

#### Acceptance criteria

1. When the setup transaction runs, the system shall delete the next-customer-number counter 'GENACUSTNUM' in pool 'GENA' and redefine it with the high customer number (11 unless the operator supplies one), so that the next customer added receives that number. (rules ADPLM-BR-121)
2. GIVEN GENACUSTNUM before: 532; terminal input: LGSE WHEN the setup transaction runs THEN GENACUSTNUM is redefined at 11 and the next customer added is given number 11 (ADPLM-C18-AC-01; ADPLM-BR-121)
3. GIVEN terminal input: LGSE 250 WHEN the setup transaction runs THEN GENACUSTNUM is redefined at 250 (ADPLM-C18-AC-02; ADPLM-BR-121)

### Requirement 2: ADPLM-REQ-F-113 (business rule)

#### Acceptance criteria

1. When the operator types more than the 5 characters of the transaction code and separator (for example 'LGSE 250'), the system shall use the characters that follow as the high customer number, writing it to the control queue and seeding the next-customer-number counter with it. (rules ADPLM-BR-122)
2. GIVEN The operator enters 'LGSE 250' WHEN The setup transaction runs THEN The control queue holds 'HIGH CUSTOMER=0000000250' and the next-customer-number counter 'GENACUSTNUM' is seeded with 250 (ADPLM-C18-AC-06; ADPLM-BR-122)

### Requirement 3: ADPLM-REQ-F-114 (business rule)

#### Acceptance criteria

1. The system shall always set the low customer number to 0000000001 and, unless the operator supplies a number, the high customer number to 0000000011, matching the restored customer database. (rules ADPLM-BR-123)
2. GIVEN The operator enters 'LGSE' with no number WHEN The setup transaction runs THEN The low customer number is 0000000001 and the high customer number is 0000000011 (ADPLM-C18-AC-07; ADPLM-BR-123)

### Requirement 4: ADPLM-REQ-F-115 (side effect)

#### Acceptance criteria

1. When the setup transaction runs, the system shall delete and recreate at zero all 36 transaction statistics counters in pool 'GENA', a success '00' and a failure '99' counter for each of 18 request types (such as 'GENA01IMOT00' and 'GENA01IMOT99'). (rules ADPLM-BR-124)
2. GIVEN GENA01IMOT00: 1240; GENA01IMOT99: 7 WHEN the setup transaction runs THEN both counters are recreated with value 0, as are the other 34 GENA01 counters (ADPLM-C18-AC-03; ADPLM-BR-124)

### Requirement 5: ADPLM-REQ-F-116 (design note)

#### Acceptance criteria

1. When the setup transaction runs, the system shall delete the error log queue 'GENAERRS', the start-time queue 'GENASTRT', the statistics queue 'GENASTAT' and the control queue 'GENACNTL', and recreate only 'GENACNTL'; the other queues are rebuilt when the application next writes to them. (rules ADPLM-BR-125)
2. GIVEN GENAERRS: 25 error records WHEN the setup transaction runs THEN GENAERRS is deleted and stays absent until the next error is logged (ADPLM-C18-AC-04; ADPLM-BR-125)

### Requirement 6: ADPLM-REQ-F-117 (design note)

#### Acceptance criteria

1. When the operator runs the setup transaction (LGSE), the system shall rewrite the control queue 'GENACNTL' as three entries in order: '**** GENAPP CNTL', 'LOW CUSTOMER=' followed by the 10-digit lowest customer number, and 'HIGH CUSTOMER=' followed by the 10-digit highest customer number. (rules ADPLM-BR-126)
2. GIVEN The control queue 'GENACNTL' holds old entries and the operator enters 'LGSE' WHEN The setup transaction runs THEN 'GENACNTL' holds exactly three entries in this order: '**** GENAPP CNTL', 'LOW CUSTOMER=0000000001', 'HIGH CUSTOMER=0000000011' (ADPLM-C18-AC-08; ADPLM-BR-126)

### Requirement 7: ADPLM-REQ-N-003 (design note)

#### Acceptance criteria

1. The system shall write the three control entries with lengths of 20, 23 and 24 characters without waiting if queue space is short, recording each outcome in a response code that is not checked. (rules ADPLM-BR-127)
2. GIVEN queue write outcome: NOSPACE WHEN setup program runs THEN the program carries on with the counter resets and still shows the completion line (ADPLM-C18-AC-05; ADPLM-BR-127)

### Requirement 8: ADPLM-REQ-F-118 (formatting)

#### Acceptance criteria

1. When the setup has finished, the system shall clear the terminal screen, show the high-customer entry (for example 'HIGH CUSTOMER=0000000011') and end the transaction. (rules ADPLM-BR-128)
2. GIVEN The operator enters 'LGSE' with no number WHEN The setup has finished THEN The terminal screen is cleared and shows 'HIGH CUSTOMER=0000000011', and the transaction ends (ADPLM-C18-AC-09; ADPLM-BR-128)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-121 | Next-customer-number counter reseeded to last customer number | business rule | WHEN the setup transaction runs, THE setup program SHALL delete the next-customer-number counter 'GENACUSTNUM' in pool 'GENA' and redefine it with the high customer number (11 unless the operator supplies one), so the next customer added receives that number. | medium | base/src/lgsetup.cbl:53-55, base/src/lgsetup.cbl:179-187, base/src/lgacdb01.cbl:200-210 |
| ADPLM-BR-122 | Operator override of last customer number from terminal input | business rule | WHEN the operator types more than the 5 characters of the transaction code and separator (for example 'LGSE 250'), THE setup program SHALL use the characters that follow as the high customer number, writing it to the control queue and seeding the next-customer-number counter with it. | medium | base/src/lgsetup.cbl:25-28, base/src/lgsetup.cbl:128-135, base/src/lgsetup.cbl:155, base/src/lgsetup.cbl:183-187 |
| ADPLM-BR-123 | Customer number range reset to match restored database | business rule | THE setup program SHALL always set the low customer number to 0000000001 and, unless the operator supplies a number, the high customer number to 0000000011, matching the restored customer database. | high | base/src/lgsetup.cbl:43-53, base/src/lgsetup.cbl:150-176, base/src/lgsetup.cbl:520-528 |
| ADPLM-BR-124 | Transaction statistics counters reset to zero | side effect | WHEN the setup transaction runs, THE setup program SHALL delete and recreate at zero all 36 transaction statistics counters in pool 'GENA' (a success '00' and a failure '99' counter for each of 18 request types, such as 'GENA01IMOT00' and 'GENA01IMOT99'). | medium | base/src/lgsetup.cbl:59-94, base/src/lgsetup.cbl:189-516, base/src/lgastat1.cbl:121-133 |
| ADPLM-BR-125 | Operational log and status queues purged on reset | design note | WHEN the setup transaction runs, THE setup program SHALL delete the error log queue 'GENAERRS', the start-time queue 'GENASTRT', the statistics queue 'GENASTAT' and the control queue 'GENACNTL', recreating only 'GENACNTL' itself; the others are rebuilt when the application next writes to them. | medium | base/src/lgsetup.cbl:137-152, base/src/lgastat1.cbl:101-117, base/src/lgstsq.cbl:82 |
| ADPLM-BR-126 | Write control header and customer range entries | design note | WHEN the operator runs the setup transaction (LGSE), THE setup program SHALL delete the application control queue 'GENACNTL' and rewrite it as three entries in order: '**** GENAPP CNTL', 'LOW CUSTOMER=' followed by the 10-digit lowest customer number, and 'HIGH CUSTOMER=' followed by the 10-digit highest customer number. | high | base/src/lgsetup.cbl:43-53, base/src/lgsetup.cbl:150-176, base/src/lgsetup.cbl:520-528 |
| ADPLM-BR-127 | Write control header and customer range entries | design note | THE setup program SHALL write the three control entries with lengths 20, 23 and 24 characters, without waiting if queue space is short (NOSUSPEND), recording each outcome in a response code that is never checked. | high | base/src/lgsetup.cbl:43-53, base/src/lgsetup.cbl:150-176, base/src/lgsetup.cbl:520-528 |
| ADPLM-BR-128 | Customer number range reset to match restored database | formatting | WHEN the setup has finished, THE setup program SHALL clear the terminal screen and show the high-customer entry, for example 'HIGH CUSTOMER=0000000011', then end the transaction. | high | base/src/lgsetup.cbl:43-53, base/src/lgsetup.cbl:150-176, base/src/lgsetup.cbl:520-528 |

### Worked examples

- ADPLM-BR-121: GENACUSTNUM before = 532; terminal input = LGSE → GENACUSTNUM is redefined at 11 and the next customer added is given number 11
- ADPLM-BR-121: terminal input = LGSE 250 → GENACUSTNUM is redefined at 250
- ADPLM-BR-124: GENA01IMOT00 = 1240; GENA01IMOT99 = 7 → both counters are recreated with value 0, as are the other 34 GENA01 counters
- ADPLM-BR-125: GENAERRS = 25 error records → GENAERRS is deleted and stays absent until the next error is logged
- ADPLM-BR-127: queue write outcome = NOSPACE → the program carries on with the counter resets and still shows the completion line

## Decision tables

None.

## Design notes

- ADPLM-BR-125: Reset is an admin operation. It clears the error log, the start-time records and the statistics records, and it rewrites the control record. Only the control record is recreated straight away; the other stores fill again as the application writes to them.
- ADPLM-BR-126: Replace the control record as a whole in one transaction with the header '**** GENAPP CNTL', the 10-digit low customer number and the 10-digit high customer number, so that no reader sees a partly rewritten record.
- ADPLM-BR-127: The legacy writes do not wait for space and never check the result. The new reset should check the write of the control record and report a failure to the operator; the fixed lengths of 20, 23 and 24 characters only matter where the old text format is kept.

## Open questions

- SME-070: During the setup that resets the customer number range, if writing the control entries fails (for example for lack of space), should the setup stop, report the failure, or carry on? (Application owner) On ADPLM-BR-127.
- SME-071: During setup, which customer numbers should be recorded as the low and high customer in the control entries, and where should those values come from? (Application owner) On ADPLM-BR-127.
- SME-072: Should clearing the existing control entries be a stated requirement of the setup, and what should happen if clearing them fails? (Application owner) On ADPLM-BR-127.
- SME-073: When an operator types a last customer number at setup, should it be checked first (digits only, positive, at most 8 or 10 digits, not below 1) before it resets the customer range and counter, and what should happen if it is invalid? (Operations supervisor) On ADPLM-BR-122.
- SME-074: Setup resets the customer number range to match a restored database (low 1, high 11 by default, or the operator's value). Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Application owner) On ADPLM-BR-128.
- SME-075: After setup, the first new customer is given number 11, the same as the recorded high customer number. Does the restored database already contain customer 11 (which would cause a duplicate), or is 11 meant to be the first free number? (Customer data owner) On ADPLM-BR-121.
- DEF-018: Is this intended? Every queue and counter command records a response code that is never tested, so the program shows the 'HIGH CUSTOMER=' completion line even when the control queue write or a counter reset failed. (Subject-matter expert) On ADPLM-BR-127, ADPLM-BR-128.
- DEF-057: Is this intended? The override is not checked: non-digit characters or more than 8 digits are moved straight into the 8-digit number, giving an unpredictable or truncated high customer number and counter value. (Subject-matter expert) On ADPLM-BR-122.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).
