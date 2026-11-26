# Requirements: Pick a customer number within the control range (ADPLM-C16)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk medium

## Introduction

Picks an existing customer number at random from within the low and high customer range held in the application control record. Testers and calling programs use it to work with a real customer without knowing one in advance. It must read the range correctly, repair missing control entries with the documented defaults, and never pick a number outside the range unless no customer exists at or above the candidate.

**User story:** As a tester or calling program, I want a customer number chosen at random within the customer range held in the control queue, so that I can work with an existing customer without knowing one in advance.

## Requirements

### Requirement 1: ADPLM-REQ-F-092 (design note)

#### Acceptance criteria

1. When the customer inquiry program was started by another program (the start code begins with 'D' or a calling program name is present), the system shall treat the run as program-called and return its result in the communication area, and otherwise shall receive the terminal input and treat the run as terminal-started. (rules ADPLM-BR-100)
2. GIVEN invoking program: LGTESTC1 WHEN the customer inquiry program was started by another program (the start code begins with 'D' or a calling program name is present) THEN The run is program-called ('C') and the result goes back in the communication area (ADPLM-C16-AC-01; ADPLM-BR-100)

### Requirement 2: ADPLM-REQ-F-093 (design note)

#### Acceptance criteria

1. The system shall start with a customer number range of 1000001 to 1000001, lock the control queue 'GENACNTL' while it reads and repairs it, and release the lock before choosing a customer. (rules ADPLM-BR-101)
2. GIVEN control queue GENACNTL: does not exist WHEN customer inquiry program runs THEN The range used is low 1000001 to high 1000001 (ADPLM-C16-AC-02; ADPLM-BR-101)

### Requirement 3: ADPLM-REQ-F-094 (design note)

#### Acceptance criteria

1. When the first entry of the control queue 'GENACNTL' can be read, the system shall treat the header entry as present and read every later entry until no more are returned. (rules ADPLM-BR-102)
2. GIVEN control queue GENACNTL: does not exist WHEN the first entry of the control queue 'GENACNTL' can be read THEN Header, low customer and high customer entries are all treated as missing (ADPLM-C16-AC-03; ADPLM-BR-102)

### Requirement 4: ADPLM-REQ-F-095 (design note)

#### Acceptance criteria

1. If the first entry of the control queue 'GENACNTL' cannot be read, then the system shall treat the header, low customer and high customer entries as all missing. (rules ADPLM-BR-102)
2. GIVEN control queue GENACNTL: does not exist WHEN the first entry of the control queue 'GENACNTL' can be read THEN Header, low customer and high customer entries are all treated as missing (ADPLM-C16-AC-03; ADPLM-BR-102)

### Requirement 5: ADPLM-REQ-F-096 (business rule)

#### Acceptance criteria

1. When an entry after the first one in the control queue begins with 'LOW CUSTOMER', the system shall take the 10-digit number that follows 'LOW CUSTOMER=' as the low end of the customer range and treat the low customer entry as present. (rules ADPLM-BR-103)
2. GIVEN The control queue 'GENACNTL' holds '**** GENAPP CNTL', then 'LOW CUSTOMER=0000000005', then 'HIGH CUSTOMER=0000000011' WHEN The customer inquiry runs THEN The low end of the range used is 5, and no 'LOW CUSTOMER=' entry is added to the queue (ADPLM-C16-AC-08; ADPLM-BR-103)

### Requirement 6: ADPLM-REQ-F-097 (business rule)

#### Acceptance criteria

1. When an entry after the first one in the control queue begins with 'HIGH CUSTOMER', the system shall take the 10-digit number that follows 'HIGH CUSTOMER=' as the high end of the customer range and treat the high customer entry as present. (rules ADPLM-BR-104)
2. GIVEN The control queue 'GENACNTL' holds '**** GENAPP CNTL', then 'LOW CUSTOMER=0000000001', then 'HIGH CUSTOMER=0000000250' WHEN The customer inquiry runs THEN The high end of the range used is 250, and no 'HIGH CUSTOMER=' entry is added to the queue (ADPLM-C16-AC-09; ADPLM-BR-104)

### Requirement 7: ADPLM-REQ-F-098 (design note)

#### Acceptance criteria

1. While the control queue has no header entry, the system shall add the 20-character header entry '**** GENAPP CNTL' to the control queue 'GENACNTL'. (rules ADPLM-BR-105)
2. GIVEN control queue GENACNTL: does not exist WHEN the control queue has no header entry THEN The entry '**** GENAPP CNTL' is written to GENACNTL (ADPLM-C16-AC-04; ADPLM-BR-105)

### Requirement 8: ADPLM-REQ-F-099 (design note)

#### Acceptance criteria

1. While no low customer entry was found, the system shall add a 23-character entry, 'LOW CUSTOMER=' followed by the 10-digit low end of the range in use (0001000001 by default), to the control queue 'GENACNTL'. (rules ADPLM-BR-106)
2. GIVEN The control queue 'GENACNTL' holds '**** GENAPP CNTL' and 'HIGH CUSTOMER=0000000011' but no low customer entry WHEN The customer inquiry runs THEN The 23-character entry 'LOW CUSTOMER=0001000001' is added to 'GENACNTL' (ADPLM-C16-AC-10; ADPLM-BR-106)

### Requirement 9: ADPLM-REQ-F-100 (design note)

#### Acceptance criteria

1. While no high customer entry was found, the system shall add a 24-character entry, 'HIGH CUSTOMER=' followed by the 10-digit high end of the range in use (0001000001 by default), to the control queue 'GENACNTL'. (rules ADPLM-BR-107)
2. GIVEN The control queue 'GENACNTL' holds '**** GENAPP CNTL' and 'LOW CUSTOMER=0001000001' but no high customer entry WHEN The customer inquiry runs THEN The 24-character entry 'HIGH CUSTOMER=0001000001' is added to 'GENACNTL' (ADPLM-C16-AC-11; ADPLM-BR-107)

### Requirement 10: ADPLM-REQ-F-101 (business rule)

#### Acceptance criteria

1. The system shall calculate a candidate customer number as the whole-number part of a random fraction (seeded with the CICS task number) times (high minus low) plus low, and return the first customer in file 'KSDSCUST' whose number is equal to or greater than it. (rules ADPLM-BR-108)
2. GIVEN range: 1000001 to 1000101; random fraction: 0.4567; KSDSCUST: 1000046 absent, 1000047 present WHEN customer inquiry program runs THEN The candidate is 1000046 and customer 1000047 is returned (ADPLM-C16-AC-05; ADPLM-BR-108)

### Requirement 11: ADPLM-REQ-F-102 (error handling)

#### Acceptance criteria

1. If no customer in 'KSDSCUST' has a number equal to or greater than the candidate, or the read fails, then the system shall return the candidate number itself. (rules ADPLM-BR-109)
2. GIVEN candidate: 1000090; KSDSCUST: highest customer 1000080 WHEN no customer in 'KSDSCUST' has a number equal to or greater than the candidate, or the read fails THEN 1000090 is returned although no such customer exists (ADPLM-C16-AC-06; ADPLM-BR-109)

### Requirement 12: ADPLM-REQ-F-103 (formatting)

#### Acceptance criteria

1. When the customer inquiry was started from a terminal, the system shall clear the screen, show 'HIGH CUSTOMER=' followed by the chosen customer number, and unlock the keyboard. (rules ADPLM-BR-110)
2. GIVEN The customer inquiry is started from a terminal and the chosen customer number is 0000000007 WHEN The inquiry finishes THEN The screen is cleared, it shows 'HIGH CUSTOMER=' followed by 0000000007, and the keyboard is unlocked (ADPLM-C16-AC-12; ADPLM-BR-110)

### Requirement 13: ADPLM-REQ-F-104 (design note)

#### Acceptance criteria

1. When the customer inquiry was called by another program, the system shall clear the communication area and return 'HIGH CUSTOMER=' and the chosen customer number in it. (rules ADPLM-BR-111)
2. GIVEN run mode: 'C' (program-called); chosen customer: 0001000047 WHEN the customer inquiry was called by another program THEN The communication area holds 'HIGH CUSTOMER=' followed by 0001000047 (ADPLM-C16-AC-07; ADPLM-BR-111)
