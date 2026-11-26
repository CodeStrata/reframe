# Implementation plan: Record the first application start (ADPLM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C12-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA.
  - _Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071_
- [ ] 2. ADPLM-C12-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071_
  - _Rules: ADPLM-BR-075_
  - _After: ADPLM-C12-T1_
- [ ] 3. ADPLM-C12-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071_
  - _Rules: ADPLM-BR-075_
  - _After: ADPLM-C12-T1, ADPLM-C12-T2_
- [ ] 4. ADPLM-C12-T4 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071_
  - _Criteria: ADPLM-C12-AC-01, ADPLM-C12-AC-02_
  - _After: ADPLM-C12-T1, ADPLM-C12-T2, ADPLM-C12-T3_
- [ ] 5. ADPLM-C12-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071_
  - _After: ADPLM-C12-T1, ADPLM-C12-T2, ADPLM-C12-T3_
