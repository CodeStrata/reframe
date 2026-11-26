# Implementation plan: Look up house and motor policy details (UP-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C09-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: UP-REQ-F-051, UP-REQ-F-052, UP-REQ-F-053, UP-REQ-F-054_
- [ ] 2. UP-C09-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: UP-REQ-F-051, UP-REQ-F-052_
  - _Rules: UP-BR-073, UP-BR-074_
  - _After: UP-C09-T1_
- [ ] 3. UP-C09-T3 [api] Build the scheduled job
  - UP-BR-075: A house reply ends with 'FINAL' in the first 5 positions of the free space straight after the house details. Callers use it to find where the policy data ends.
  - UP-BR-076: A motor reply ends with 'FINAL' in the first 5 positions of the free space straight after the motor details, after the accidents count. Callers use it to find where the policy data ends.
  - _Requirements: UP-REQ-F-053, UP-REQ-F-054_
  - _Rules: UP-BR-075, UP-BR-076_
  - _After: UP-C09-T1, UP-C09-T2_
- [ ] 4. UP-C09-T4 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-051, UP-REQ-F-052, UP-REQ-F-053, UP-REQ-F-054_
  - _Criteria: UP-C09-AC-01, UP-C09-AC-02, UP-C09-AC-03, UP-C09-AC-04, UP-C09-AC-05, UP-C09-AC-06_
  - _After: UP-C09-T1, UP-C09-T2, UP-C09-T3_
- [ ] 5. UP-C09-T5 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-051, UP-REQ-F-052, UP-REQ-F-053, UP-REQ-F-054_
  - _After: UP-C09-T1, UP-C09-T2, UP-C09-T3_
