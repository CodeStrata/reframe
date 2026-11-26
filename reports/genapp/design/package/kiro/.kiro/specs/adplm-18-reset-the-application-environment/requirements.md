# Requirements: Reset the application environment (ADPLM-C18)

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
