# Implementation plan: Accept and route policy inquiries (UP-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C10-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: UP-REQ-F-055, UP-REQ-F-056_
- [ ] 2. UP-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: UP-REQ-F-055, UP-REQ-F-056_
  - _Rules: UP-BR-077, UP-BR-078_
  - _After: UP-C10-T1_
- [ ] 3. UP-C10-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: UP-REQ-F-055, UP-REQ-F-056_
  - _Rules: UP-BR-077, UP-BR-078_
  - _After: UP-C10-T1, UP-C10-T2_
- [ ] 4. UP-C10-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-055, UP-REQ-F-056_
  - _Criteria: UP-C10-AC-01, UP-C10-AC-02, UP-C10-AC-03_
  - _After: UP-C10-T1, UP-C10-T2, UP-C10-T3_
