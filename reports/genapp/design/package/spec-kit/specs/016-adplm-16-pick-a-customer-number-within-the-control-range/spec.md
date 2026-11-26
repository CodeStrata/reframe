# Feature specification: Pick a customer number within the control range

**Feature:** ADPLM-C16 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C16)

As a tester or calling program, I want a customer number chosen at random within the customer range held in the control queue, so that I can work with an existing customer without knowing one in advance.

Picks an existing customer number at random from within the low and high customer range held in the application control record. Testers and calling programs use it to work with a real customer without knowing one in advance. It must read the range correctly, repair missing control entries with the documented defaults, and never pick a number outside the range unless no customer exists at or above the candidate.

**Acceptance scenarios:**

1. **Given** invoking program: LGTESTC1, **when** the customer inquiry program was started by another program (the start code begins with 'D' or a calling program name is present), **then** The run is program-called ('C') and the result goes back in the communication area (ADPLM-C16-AC-01)
2. **Given** control queue GENACNTL: does not exist, **when** customer inquiry program runs, **then** The range used is low 1000001 to high 1000001 (ADPLM-C16-AC-02)
3. **Given** control queue GENACNTL: does not exist, **when** the first entry of the control queue 'GENACNTL' can be read, **then** Header, low customer and high customer entries are all treated as missing (ADPLM-C16-AC-03)
4. **Given** control queue GENACNTL: does not exist, **when** the control queue has no header entry, **then** The entry '**** GENAPP CNTL' is written to GENACNTL (ADPLM-C16-AC-04)
5. **Given** range: 1000001 to 1000101; random fraction: 0.4567; KSDSCUST: 1000046 absent, 1000047 present, **when** customer inquiry program runs, **then** The candidate is 1000046 and customer 1000047 is returned (ADPLM-C16-AC-05)
6. **Given** candidate: 1000090; KSDSCUST: highest customer 1000080, **when** no customer in 'KSDSCUST' has a number equal to or greater than the candidate, or the read fails, **then** 1000090 is returned although no such customer exists (ADPLM-C16-AC-06)
7. **Given** run mode: 'C' (program-called); chosen customer: 0001000047, **when** the customer inquiry was called by another program, **then** The communication area holds 'HIGH CUSTOMER=' followed by 0001000047 (ADPLM-C16-AC-07)
8. **Given** The control queue 'GENACNTL' holds '**** GENAPP CNTL', then 'LOW CUSTOMER=0000000005', then 'HIGH CUSTOMER=0000000011', **when** The customer inquiry runs, **then** The low end of the range used is 5, and no 'LOW CUSTOMER=' entry is added to the queue (ADPLM-C16-AC-08)
9. **Given** The control queue 'GENACNTL' holds '**** GENAPP CNTL', then 'LOW CUSTOMER=0000000001', then 'HIGH CUSTOMER=0000000250', **when** The customer inquiry runs, **then** The high end of the range used is 250, and no 'HIGH CUSTOMER=' entry is added to the queue (ADPLM-C16-AC-09)
10. **Given** The control queue 'GENACNTL' holds '**** GENAPP CNTL' and 'HIGH CUSTOMER=0000000011' but no low customer entry, **when** The customer inquiry runs, **then** The 23-character entry 'LOW CUSTOMER=0001000001' is added to 'GENACNTL' (ADPLM-C16-AC-10)
11. **Given** The control queue 'GENACNTL' holds '**** GENAPP CNTL' and 'LOW CUSTOMER=0001000001' but no high customer entry, **when** The customer inquiry runs, **then** The 24-character entry 'HIGH CUSTOMER=0001000001' is added to 'GENACNTL' (ADPLM-C16-AC-11)
12. **Given** The customer inquiry is started from a terminal and the chosen customer number is 0000000007, **when** The inquiry finishes, **then** The screen is cleared, it shows 'HIGH CUSTOMER=' followed by 0000000007, and the keyboard is unlocked (ADPLM-C16-AC-12)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-092** (design note): When the customer inquiry program was started by another program (the start code begins with 'D' or a calling program name is present), the system shall treat the run as program-called and return its result in the communication area, and otherwise shall receive the terminal input and treat the run as terminal-started. Rules: ADPLM-BR-100.
- **ADPLM-REQ-F-093** (design note): The system shall start with a customer number range of 1000001 to 1000001, lock the control queue 'GENACNTL' while it reads and repairs it, and release the lock before choosing a customer. Rules: ADPLM-BR-101.
- **ADPLM-REQ-F-094** (design note): When the first entry of the control queue 'GENACNTL' can be read, the system shall treat the header entry as present and read every later entry until no more are returned. Rules: ADPLM-BR-102.
- **ADPLM-REQ-F-095** (design note): If the first entry of the control queue 'GENACNTL' cannot be read, then the system shall treat the header, low customer and high customer entries as all missing. Rules: ADPLM-BR-102.
- **ADPLM-REQ-F-096** (business rule): When an entry after the first one in the control queue begins with 'LOW CUSTOMER', the system shall take the 10-digit number that follows 'LOW CUSTOMER=' as the low end of the customer range and treat the low customer entry as present. Rules: ADPLM-BR-103.
- **ADPLM-REQ-F-097** (business rule): When an entry after the first one in the control queue begins with 'HIGH CUSTOMER', the system shall take the 10-digit number that follows 'HIGH CUSTOMER=' as the high end of the customer range and treat the high customer entry as present. Rules: ADPLM-BR-104.
- **ADPLM-REQ-F-098** (design note): While the control queue has no header entry, the system shall add the 20-character header entry '**** GENAPP CNTL' to the control queue 'GENACNTL'. Rules: ADPLM-BR-105.
- **ADPLM-REQ-F-099** (design note): While no low customer entry was found, the system shall add a 23-character entry, 'LOW CUSTOMER=' followed by the 10-digit low end of the range in use (0001000001 by default), to the control queue 'GENACNTL'. Rules: ADPLM-BR-106.
- **ADPLM-REQ-F-100** (design note): While no high customer entry was found, the system shall add a 24-character entry, 'HIGH CUSTOMER=' followed by the 10-digit high end of the range in use (0001000001 by default), to the control queue 'GENACNTL'. Rules: ADPLM-BR-107.
- **ADPLM-REQ-F-101** (business rule): The system shall calculate a candidate customer number as the whole-number part of a random fraction (seeded with the CICS task number) times (high minus low) plus low, and return the first customer in file 'KSDSCUST' whose number is equal to or greater than it. Rules: ADPLM-BR-108.
- **ADPLM-REQ-F-102** (error handling): If no customer in 'KSDSCUST' has a number equal to or greater than the candidate, or the read fails, then the system shall return the candidate number itself. Rules: ADPLM-BR-109.
- **ADPLM-REQ-F-103** (formatting): When the customer inquiry was started from a terminal, the system shall clear the screen, show 'HIGH CUSTOMER=' followed by the chosen customer number, and unlock the keyboard. Rules: ADPLM-BR-110.
- **ADPLM-REQ-F-104** (design note): When the customer inquiry was called by another program, the system shall clear the communication area and return 'HIGH CUSTOMER=' and the chosen customer number in it. Rules: ADPLM-BR-111.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-100 | Determine invocation mode of the run | design note | WHEN the customer inquiry program was started by another program (the start code begins with 'D' or a calling program name is present), THE program SHALL treat the run as program-called and return its result in the communication area; otherwise it SHALL receive the terminal input and treat the run as terminal-started. | medium | base/src/lgicvs01.cbl:101-121 |
| ADPLM-BR-101 | Customer number range is held in a shared control queue and self-initialised | design note | THE customer inquiry program SHALL start with a customer number range of 1000001 to 1000001, lock the control queue 'GENACNTL' while it reads and repairs it, and release the lock before choosing a customer. | high | base/src/lgicvs01.cbl:123-191, base/src/lgicvs01.cbl:40-47, base/src/lgicvs01.cbl:54-61 |
| ADPLM-BR-102 | Detect existing control queue | design note | WHEN the first entry of the control queue 'GENACNTL' can be read, THE customer inquiry program SHALL treat the header entry as present and read every later entry until no more are returned; WHEN the first entry cannot be read, it SHALL treat the header, low customer and high customer entries as all missing. | high | base/src/lgicvs01.cbl:123-191, base/src/lgicvs01.cbl:40-47, base/src/lgicvs01.cbl:54-61 |
| ADPLM-BR-103 | Recognise low customer entry | business rule | WHEN an entry after the first one in the control queue begins with 'LOW CUSTOMER', THE customer inquiry program SHALL take the 10-digit number that follows 'LOW CUSTOMER=' as the low end of the customer range and treat the low customer entry as present. | high | base/src/lgicvs01.cbl:123-191, base/src/lgicvs01.cbl:40-47, base/src/lgicvs01.cbl:54-61 |
| ADPLM-BR-104 | Recognise high customer entry | business rule | WHEN an entry after the first one in the control queue begins with 'HIGH CUSTOMER', THE customer inquiry program SHALL take the 10-digit number that follows 'HIGH CUSTOMER=' as the high end of the customer range and treat the high customer entry as present. | high | base/src/lgicvs01.cbl:123-191, base/src/lgicvs01.cbl:40-47, base/src/lgicvs01.cbl:54-61 |
| ADPLM-BR-105 | Write missing header entry | design note | WHEN the control queue has no header entry, THE customer inquiry program SHALL add the 20-character header entry '**** GENAPP CNTL' to the control queue 'GENACNTL'. | high | base/src/lgicvs01.cbl:123-191, base/src/lgicvs01.cbl:40-47, base/src/lgicvs01.cbl:54-61 |
| ADPLM-BR-106 | Write missing low customer entry | design note | WHEN no low customer entry was found, THE customer inquiry program SHALL add a 23-character entry, 'LOW CUSTOMER=' followed by the 10-digit low end of the range in use (0001000001 by default), to the control queue 'GENACNTL'. | high | base/src/lgicvs01.cbl:123-191, base/src/lgicvs01.cbl:40-47, base/src/lgicvs01.cbl:54-61 |
| ADPLM-BR-107 | Write missing high customer entry | design note | WHEN no high customer entry was found, THE customer inquiry program SHALL add a 24-character entry, 'HIGH CUSTOMER=' followed by the 10-digit high end of the range in use (0001000001 by default), to the control queue 'GENACNTL'. | high | base/src/lgicvs01.cbl:123-191, base/src/lgicvs01.cbl:40-47, base/src/lgicvs01.cbl:54-61 |
| ADPLM-BR-108 | Random customer number selection within the control range | business rule | THE customer inquiry program SHALL calculate a candidate customer number as the whole-number part of a random fraction (seeded with the CICS task number) times (high minus low) plus low, and return the first customer in file 'KSDSCUST' whose number is equal to or greater than it. | medium | base/src/lgicvs01.cbl:193-209 |
| ADPLM-BR-109 | Random customer number selection within the control range | error handling | WHEN no customer in 'KSDSCUST' has a number equal to or greater than the candidate, or the read fails, THE customer inquiry program SHALL return the candidate number itself. | medium | base/src/lgicvs01.cbl:193-209 |
| ADPLM-BR-110 | Display high customer message on terminal | formatting | WHEN the customer inquiry was started from a terminal, THE customer inquiry program SHALL clear the screen, show 'HIGH CUSTOMER=' followed by the chosen customer number, and unlock the keyboard. | medium | base/src/lgicvs01.cbl:197-222 |
| ADPLM-BR-111 | Display high customer message on terminal | design note | WHEN the customer inquiry was called by another program, THE customer inquiry program SHALL clear the communication area and return 'HIGH CUSTOMER=' and the chosen customer number in it. | medium | base/src/lgicvs01.cbl:197-222 |

### Key entities

None found in the source.

### Needs clarification

- SME-051: When the control list is first set up, what starting values should be written after 'LOW CUSTOMER=' and 'HIGH CUSTOMER='? (Application business owner) On ADPLM-BR-102, ADPLM-BR-103, ADPLM-BR-104, ADPLM-BR-105, ADPLM-BR-106, ADPLM-BR-107.
- SME-052: When the control list is checked, a read error is treated the same as reaching the end of the list. Should a read error be handled differently, for example so that duplicate low or high customer entries are not written? (Application architecture team) On ADPLM-BR-102, ADPLM-BR-103, ADPLM-BR-104, ADPLM-BR-105, ADPLM-BR-106, ADPLM-BR-107.
- SME-053: The control list is treated as having its header whenever its first entry can be read, even if that entry is not '**** GENAPP CNTL'. Should the new system check the header text? (Application architecture team) On ADPLM-BR-102, ADPLM-BR-103, ADPLM-BR-104, ADPLM-BR-105, ADPLM-BR-106, ADPLM-BR-107.
- SME-054: If writing an entry to the control list fails because storage is unavailable, should the failure be reported, retried or ignored? (Operations team) On ADPLM-BR-102, ADPLM-BR-103, ADPLM-BR-104, ADPLM-BR-105, ADPLM-BR-106, ADPLM-BR-107.
- SME-055: Two runs at the same time could both find a control-list entry missing and both add it. Must runs be made to take turns to prevent duplicates? (Application architecture team) On ADPLM-BR-102, ADPLM-BR-103, ADPLM-BR-104, ADPLM-BR-105, ADPLM-BR-106, ADPLM-BR-107.
- SME-056: The high-customer message shown on the terminal is longer than its 'HIGH CUSTOMER=' label. What should follow the label in that message? (Business analyst for policy lifecycle management) On ADPLM-BR-100, ADPLM-BR-111.
- SME-057: When this function is called by another program instead of run from a terminal, what output should it produce, and who should receive it? (Application architecture team) On ADPLM-BR-100, ADPLM-BR-111.
- SME-058: This flow is called 'Random Customer Number Retrieval', but no rule says how the customer number is chosen or where it is read from. How should that work? (Business analyst for policy lifecycle management) On ADPLM-BR-100, ADPLM-BR-111.
- DEF-016: Is this intended? Only the entries after the first one are checked for 'LOW CUSTOMER' and 'HIGH CUSTOMER', and the first entry is always taken to be the header without checking its text. If the queue exists but the low or high entry is missing, the default 1000001 is written for that end, which can make the low end higher than the high end. (Subject-matter expert) On ADPLM-BR-102, ADPLM-BR-103, ADPLM-BR-104, ADPLM-BR-105, ADPLM-BR-106, ADPLM-BR-107.
- DEF-038: Confirm this is deliberate: The chosen random customer number is shown under the label 'HIGH CUSTOMER=', because the program reuses the high customer field to hold its result. (Subject-matter expert) On ADPLM-BR-111.
- DEF-051: Is this intended? When the greater-or-equal read finds no customer, the program returns the candidate number, which is not an existing customer, although its header says it returns a customer that is in the file. (Subject-matter expert) On ADPLM-BR-109.

### Decision table gaps

None.
