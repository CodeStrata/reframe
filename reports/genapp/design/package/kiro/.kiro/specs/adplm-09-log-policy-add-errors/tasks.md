# Implementation plan: Log policy add errors (ADPLM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C09-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: ADPLM-REQ-F-055_
- [ ] 2. ADPLM-C09-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-055_
  - _Rules: ADPLM-BR-060_
  - _After: ADPLM-C09-T1_
- [ ] 3. ADPLM-C09-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: ADPLM-REQ-F-055_
  - _Rules: ADPLM-BR-060_
  - _After: ADPLM-C09-T1, ADPLM-C09-T2_
- [ ] 4. ADPLM-C09-T4 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-055_
  - _Criteria: ADPLM-C09-AC-01, ADPLM-C09-AC-02_
  - _After: ADPLM-C09-T1, ADPLM-C09-T2, ADPLM-C09-T3_
- [ ] 5. ADPLM-C09-T5 [compliance] Review the handling of audit, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-055_
  - _After: ADPLM-C09-T1, ADPLM-C09-T2, ADPLM-C09-T3_
