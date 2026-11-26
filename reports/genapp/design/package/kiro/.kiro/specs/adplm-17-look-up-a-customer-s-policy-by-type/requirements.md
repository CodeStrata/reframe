# Requirements: Look up a customer's policy by type (ADPLM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk medium

## Introduction

Finds a customer's policy of a given type in the policy file. It returns either 'Policy Key=' with the full 21-character policy key or a clear 'Policy Bad=' answer. Testers and calling programs use it to get a real policy key. It must never return a policy of a different type from the one asked for.

**User story:** As a tester or calling program, I want to find a customer's policy of a given type in the policy file, so that I get its full policy key or a clear bad-policy answer.

## Requirements

### Requirement 1: ADPLM-REQ-F-105 (design note)

#### Acceptance criteria

1. When the request was not started by a distributed link and has no calling program, the system shall read the request typed at the terminal as a 5-character transaction code and space, then the policy type, then the customer number, whose length is the input length minus 6. (rules ADPLM-BR-112)
2. GIVEN terminal input: LGPF M0001000010 WHEN the request was not started by a distributed link and has no calling program THEN Policy type 'M' and customer number 0001000010 are used for the lookup. (ADPLM-C17-AC-01; ADPLM-BR-112)
3. GIVEN terminal input: LGPF C1000010 WHEN the request was not started by a distributed link and has no calling program THEN Policy type 'C' and customer number 0001000010 (right-aligned, zero-filled) are used. (ADPLM-C17-AC-02; ADPLM-BR-112)

### Requirement 2: ADPLM-REQ-F-106 (design note)

#### Acceptance criteria

1. When the request was started by a distributed link (start code beginning 'D') or by a calling program, the system shall take the policy type from the first character of the caller's data and the customer number from the next 10 characters. (rules ADPLM-BR-113)
2. GIVEN start code: D; caller data: M0001000010 WHEN the request was started by a distributed link (start code beginning 'D') or by a calling program THEN Policy type 'M' and customer number 0001000010 are used and the answer goes back in the caller's data area. (ADPLM-C17-AC-03; ADPLM-BR-113)
3. GIVEN calling program: web service pipeline; caller data: H0001000020 WHEN the request was started by a distributed link (start code beginning 'D') or by a calling program THEN Policy type 'H' and customer number 0001000020 are used. (ADPLM-C17-AC-04; ADPLM-BR-113)

### Requirement 3: ADPLM-REQ-N-002 (historical artifact)

#### Acceptance criteria

1. The system shall copy the caller's data length into its working length and then immediately replace it with a fixed length, so that the length the caller passed is never used. (rules ADPLM-BR-114)
2. GIVEN caller data length: 90 WHEN policy inquiry runs THEN The program still reads exactly 1 type character and 10 customer-number characters. (ADPLM-C17-AC-05; ADPLM-BR-114)

### Requirement 4: ADPLM-REQ-F-107 (business rule)

#### Acceptance criteria

1. The system shall read the policy file (KSDSPOLY) for the first policy whose key is at or after the requested policy type followed by the 10-digit customer number, matching on those first 11 characters only (generic read, greater-or-equal) and taking a 64-byte record. (rules ADPLM-BR-115)
2. GIVEN policy type: M; customer number: 0001000010; first policy file key at or after M0001000010: M00010000100000000003 WHEN policy inquiry runs THEN The policy record with key M / 0001000010 / 0000000003 is retrieved. (ADPLM-C17-AC-06; ADPLM-BR-115)
3. GIVEN policy type: M; customer number: 0001000010; first policy file key at or after M0001000010: M00010000150000000007 WHEN policy inquiry runs THEN The policy of customer 0001000015 is retrieved, because the read takes the next key when there is no exact match. (ADPLM-C17-AC-07; ADPLM-BR-115)

### Requirement 5: ADPLM-REQ-F-108 (business rule)

#### Acceptance criteria

1. When the read succeeds and the retrieved policy has the requested policy type, the system shall answer 'Policy Key=' followed by the retrieved 21-character key (policy type, customer number, policy number). (rules ADPLM-BR-116)
2. GIVEN The policy file holds a record with key 'M00000000010000000003' and no earlier key for type 'M' and customer 0000000001 WHEN A lookup is made for policy type 'M' and customer number 0000000001 THEN The answer is 'Policy Key=M00000000010000000003' (ADPLM-C17-AC-10; ADPLM-BR-116)

### Requirement 6: ADPLM-REQ-F-109 (error handling)

#### Acceptance criteria

1. If the read fails or the retrieved policy has a different policy type from the one requested, then the system shall answer 'Policy Bad=' followed by type 'X', customer number 0000000013 and policy number 0000000013. (rules ADPLM-BR-117, ADPLM-BR-118)
2. GIVEN Requested policy type: 'M'; Requested number: 0000000001; First KSDSPOLY record at or after key: type 'H' WHEN the retrieved policy type differs from the requested type or the policy lookup fails THEN Message shows 'Policy Bad=' with customer number 0000000013 and policy number 0000000013 (ADPLM-C17-AC-08; ADPLM-BR-117)
3. GIVEN Requested policy type: 'E'; KSDSPOLY read: not found (response not NORMAL) WHEN the retrieved policy type differs from the requested type or the policy lookup fails THEN Message shows 'Policy Bad=' with customer number 0000000013 and policy number 0000000013 (ADPLM-C17-AC-09; ADPLM-BR-117)

### Requirement 7: ADPLM-REQ-F-110 (design note)

#### Acceptance criteria

1. When the request came from a calling program or service rather than a terminal, the system shall clear the caller's data area and return in it the result label ('Policy Key=' or 'Policy Bad=') followed by the 21-character policy key. (rules ADPLM-BR-119)
2. GIVEN A calling program sends a request whose data area holds old content, for policy type 'H' and customer 0000000001, and has no house policy at or after that key WHEN The lookup is made THEN The caller's data area is cleared and holds only 'Policy Bad=' followed by the 21-character key 'X00000000130000000013' (ADPLM-C17-AC-11; ADPLM-BR-119)

### Requirement 8: ADPLM-REQ-F-111 (formatting)

#### Acceptance criteria

1. When the request was typed at a terminal, the system shall clear the screen, show the 80-character answer ('Policy Key=' or 'Policy Bad=' followed by the policy key), and unlock the keyboard. (rules ADPLM-BR-120)
2. GIVEN A request is typed at a terminal for a policy type and customer that has a matching policy with key 'E00000000010000000001' WHEN The lookup finishes THEN The screen is cleared, shows the 80-character answer 'Policy Key=E00000000010000000001' padded with spaces, and the keyboard is unlocked (ADPLM-C17-AC-12; ADPLM-BR-120)
