# Implementation plan: Accept and check a policy update request (ADPLM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C19-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA.
  - _Requirements: ADPLM-REQ-F-119, ADPLM-REQ-F-120, ADPLM-REQ-F-121, ADPLM-REQ-F-122, ADPLM-REQ-F-123, ADPLM-REQ-F-124, ADPLM-REQ-F-125_
- [ ] 2. ADPLM-C19-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-121, ADPLM-REQ-F-122, ADPLM-REQ-F-123, ADPLM-REQ-F-124_
  - _Rules: ADPLM-BR-131, ADPLM-BR-132, ADPLM-BR-133, ADPLM-BR-134_
  - _After: ADPLM-C19-T1_
- [ ] 3. ADPLM-C19-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ADPLM-REQ-F-119_
  - _Rules: ADPLM-BR-129_
  - _After: ADPLM-C19-T1_
- [ ] 4. ADPLM-C19-T4 [api] Build the scheduled job
  - ADPLM-BR-130: Set the response code to '00' as soon as a request with data is accepted, before the length and type checks run.
  - ADPLM-BR-135: Call the policy database update in-process with the whole validated request, and return its outcome code ('00', '01', '02' or '90') to the caller as the final result.
  - _Requirements: ADPLM-REQ-F-120, ADPLM-REQ-F-125_
  - _Rules: ADPLM-BR-130, ADPLM-BR-135_
  - _After: ADPLM-C19-T1, ADPLM-C19-T2, ADPLM-C19-T3_
- [ ] 5. ADPLM-C19-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-119, ADPLM-REQ-F-120, ADPLM-REQ-F-121, ADPLM-REQ-F-122, ADPLM-REQ-F-123, ADPLM-REQ-F-124, ADPLM-REQ-F-125_
  - _Criteria: ADPLM-C19-AC-01, ADPLM-C19-AC-02, ADPLM-C19-AC-03, ADPLM-C19-AC-04, ADPLM-C19-AC-05, ADPLM-C19-AC-06, ADPLM-C19-AC-07, ADPLM-C19-AC-08, ADPLM-C19-AC-09, ADPLM-C19-AC-10_
  - _After: ADPLM-C19-T1, ADPLM-C19-T2, ADPLM-C19-T3, ADPLM-C19-T4_
- [ ] 6. ADPLM-C19-T6 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-119, ADPLM-REQ-F-120, ADPLM-REQ-F-121, ADPLM-REQ-F-122, ADPLM-REQ-F-123, ADPLM-REQ-F-124, ADPLM-REQ-F-125_
  - _After: ADPLM-C19-T1, ADPLM-C19-T2, ADPLM-C19-T3, ADPLM-C19-T4_
