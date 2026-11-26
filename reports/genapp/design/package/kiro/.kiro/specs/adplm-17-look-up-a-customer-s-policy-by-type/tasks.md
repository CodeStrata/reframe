# Implementation plan: Look up a customer's policy by type (ADPLM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C17-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: ADPLM-BR-114.
  - _Requirements: ADPLM-REQ-F-107, ADPLM-REQ-F-108, ADPLM-REQ-N-002_
  - _Rules: ADPLM-BR-114, ADPLM-BR-115, ADPLM-BR-116_
- [ ] 2. ADPLM-C17-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ADPLM-REQ-F-109, ADPLM-REQ-F-111_
  - _Rules: ADPLM-BR-117, ADPLM-BR-118, ADPLM-BR-120_
- [ ] 3. ADPLM-C17-T3 [api] Build the scheduled job
  - ADPLM-BR-112: The interactive entry point takes the policy type and the customer number as separate input fields, instead of splitting a typed line at fixed offsets after a 5-character transaction code and space.
  - ADPLM-BR-113: The service entry point takes a request with a one-character policy type and a 10-digit customer number as named fields.
  - ADPLM-BR-119: Return a fresh response for service callers that holds the result label ('Policy Key=' or 'Policy Bad=') and the 21-character key. Nothing from the caller's request is echoed back.
  - _Requirements: ADPLM-REQ-F-105, ADPLM-REQ-F-106, ADPLM-REQ-F-110_
  - _Rules: ADPLM-BR-112, ADPLM-BR-113, ADPLM-BR-119_
  - _After: ADPLM-C17-T1, ADPLM-C17-T2_
- [ ] 4. ADPLM-C17-T4 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-105, ADPLM-REQ-F-106, ADPLM-REQ-N-002, ADPLM-REQ-F-107, ADPLM-REQ-F-108, ADPLM-REQ-F-109, ADPLM-REQ-F-110, ADPLM-REQ-F-111_
  - _Criteria: ADPLM-C17-AC-01, ADPLM-C17-AC-02, ADPLM-C17-AC-03, ADPLM-C17-AC-04, ADPLM-C17-AC-05, ADPLM-C17-AC-06, ADPLM-C17-AC-07, ADPLM-C17-AC-08, ADPLM-C17-AC-09, ADPLM-C17-AC-10, ADPLM-C17-AC-11, ADPLM-C17-AC-12_
  - _After: ADPLM-C17-T1, ADPLM-C17-T2, ADPLM-C17-T3_
- [ ] 5. ADPLM-C17-T5 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-105, ADPLM-REQ-F-106, ADPLM-REQ-N-002, ADPLM-REQ-F-107, ADPLM-REQ-F-108, ADPLM-REQ-F-109, ADPLM-REQ-F-110, ADPLM-REQ-F-111_
  - _After: ADPLM-C17-T1, ADPLM-C17-T2, ADPLM-C17-T3_
