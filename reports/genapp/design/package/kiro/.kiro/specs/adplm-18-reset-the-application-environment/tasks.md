# Implementation plan: Reset the application environment (ADPLM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C18-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-112, ADPLM-REQ-F-113, ADPLM-REQ-F-114, ADPLM-REQ-F-115_
  - _Rules: ADPLM-BR-121, ADPLM-BR-122, ADPLM-BR-123, ADPLM-BR-124_
- [ ] 2. ADPLM-C18-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ADPLM-REQ-F-118_
  - _Rules: ADPLM-BR-128_
- [ ] 3. ADPLM-C18-T3 [api] Build the scheduled job
  - ADPLM-BR-125: Reset is an admin operation. It clears the error log, the start-time records and the statistics records, and it rewrites the control record. Only the control record is recreated straight away; the other stores fill again as the application writes to them.
  - ADPLM-BR-126: Replace the control record as a whole in one transaction with the header '**** GENAPP CNTL', the 10-digit low customer number and the 10-digit high customer number, so that no reader sees a partly rewritten record.
  - ADPLM-BR-127: The legacy writes do not wait for space and never check the result. The new reset should check the write of the control record and report a failure to the operator; the fixed lengths of 20, 23 and 24 characters only matter where the old text format is kept.
  - _Requirements: ADPLM-REQ-F-116, ADPLM-REQ-F-117, ADPLM-REQ-N-003_
  - _Rules: ADPLM-BR-125, ADPLM-BR-126, ADPLM-BR-127_
  - _After: ADPLM-C18-T1, ADPLM-C18-T2_
- [ ] 4. ADPLM-C18-T4 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-112, ADPLM-REQ-F-113, ADPLM-REQ-F-114, ADPLM-REQ-F-115, ADPLM-REQ-F-116, ADPLM-REQ-F-117, ADPLM-REQ-N-003, ADPLM-REQ-F-118_
  - _Criteria: ADPLM-C18-AC-01, ADPLM-C18-AC-02, ADPLM-C18-AC-03, ADPLM-C18-AC-04, ADPLM-C18-AC-05, ADPLM-C18-AC-06, ADPLM-C18-AC-07, ADPLM-C18-AC-08, ADPLM-C18-AC-09_
  - _After: ADPLM-C18-T1, ADPLM-C18-T2, ADPLM-C18-T3_
- [ ] 5. ADPLM-C18-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-112, ADPLM-REQ-F-113, ADPLM-REQ-F-114, ADPLM-REQ-F-115, ADPLM-REQ-F-116, ADPLM-REQ-F-117, ADPLM-REQ-N-003, ADPLM-REQ-F-118_
  - _After: ADPLM-C18-T1, ADPLM-C18-T2, ADPLM-C18-T3_
