# Tasks: Look up house and motor policy details (UP-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C09-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-051, UP-REQ-F-052, UP-REQ-F-053, UP-REQ-F-054.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] UP-C09-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-051, UP-REQ-F-052. Rules: UP-BR-073, UP-BR-074. After: UP-C09-T1.
  - Keep each business rule exactly as specified.
- [ ] UP-C09-T3 [api] Build the scheduled job. Requirements: UP-REQ-F-053, UP-REQ-F-054. Rules: UP-BR-075, UP-BR-076. After: UP-C09-T1, UP-C09-T2.
  - UP-BR-075: A house reply ends with 'FINAL' in the first 5 positions of the free space straight after the house details. Callers use it to find where the policy data ends.
  - UP-BR-076: A motor reply ends with 'FINAL' in the first 5 positions of the free space straight after the motor details, after the accidents count. Callers use it to find where the policy data ends.
- [ ] UP-C09-T4 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-051, UP-REQ-F-052, UP-REQ-F-053, UP-REQ-F-054. Criteria: UP-C09-AC-01, UP-C09-AC-02, UP-C09-AC-03, UP-C09-AC-04, UP-C09-AC-05, UP-C09-AC-06. After: UP-C09-T1, UP-C09-T2, UP-C09-T3.
  - 6 acceptance criteria, each a test named by its ID.
- [ ] UP-C09-T5 [compliance] Review the handling of money, personal data. Requirements: UP-REQ-F-051, UP-REQ-F-052, UP-REQ-F-053, UP-REQ-F-054. After: UP-C09-T1, UP-C09-T2, UP-C09-T3.
  - Check storage, logs, screens and audit against the rules.
