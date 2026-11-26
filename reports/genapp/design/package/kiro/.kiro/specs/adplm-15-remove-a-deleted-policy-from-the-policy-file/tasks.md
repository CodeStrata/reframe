# Implementation plan: Remove a deleted policy from the policy file (ADPLM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C15-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA.
  - _Requirements: ADPLM-REQ-F-088, ADPLM-REQ-F-089, ADPLM-REQ-F-090, ADPLM-REQ-F-091_
- [ ] 2. ADPLM-C15-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-090, ADPLM-REQ-F-091_
  - _Rules: ADPLM-BR-098, ADPLM-BR-099_
  - _After: ADPLM-C15-T1_
- [ ] 3. ADPLM-C15-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ADPLM-REQ-F-089_
  - _Rules: ADPLM-BR-097_
  - _After: ADPLM-C15-T1_
- [ ] 4. ADPLM-C15-T4 [api] Build the scheduled job
  - ADPLM-BR-096: The policy file is a keyed store. Its 21-character key is the policy type letter (the fourth character of the request identifier), then the 10-digit customer number, then the 10-digit policy number. Deletion is a single delete by that exact key.
  - _Requirements: ADPLM-REQ-F-088_
  - _Rules: ADPLM-BR-096_
  - _After: ADPLM-C15-T1, ADPLM-C15-T2, ADPLM-C15-T3_
- [ ] 5. ADPLM-C15-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-088, ADPLM-REQ-F-089, ADPLM-REQ-F-090, ADPLM-REQ-F-091_
  - _Criteria: ADPLM-C15-AC-01, ADPLM-C15-AC-02, ADPLM-C15-AC-03, ADPLM-C15-AC-04, ADPLM-C15-AC-05, ADPLM-C15-AC-06, ADPLM-C15-AC-07, ADPLM-C15-AC-08_
  - _After: ADPLM-C15-T1, ADPLM-C15-T2, ADPLM-C15-T3, ADPLM-C15-T4_
- [ ] 6. ADPLM-C15-T6 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-088, ADPLM-REQ-F-089, ADPLM-REQ-F-090, ADPLM-REQ-F-091_
  - _After: ADPLM-C15-T1, ADPLM-C15-T2, ADPLM-C15-T3, ADPLM-C15-T4_
