# Tasks: Return policy details (UP-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C06-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-030, UP-REQ-F-031, UP-REQ-F-032, UP-REQ-F-033, UP-REQ-F-034, UP-REQ-F-035, UP-REQ-F-036, UP-REQ-F-037, UP-REQ-F-038.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] UP-C06-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-030, UP-REQ-F-031, UP-REQ-F-033, UP-REQ-F-035, UP-REQ-F-036, UP-REQ-F-037. Rules: UP-BR-051, UP-BR-052, UP-BR-055, UP-BR-057, UP-BR-058, UP-BR-059. After: UP-C06-T1.
  - Keep each business rule exactly as specified.
- [ ] UP-C06-T3 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-038. Rules: UP-BR-060. After: UP-C06-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C06-T4 [api] Build the scheduled job. Requirements: UP-REQ-F-032, UP-REQ-F-034. Rules: UP-BR-053, UP-BR-054, UP-BR-056. After: UP-C06-T1, UP-C06-T2, UP-C06-T3.
  - UP-BR-053: Before replying, the inquiry works out the space the reply needs: 33 bytes of header plus the length for the policy type. That is 124 for endowment plus any padding data, 130 for house, 137 for motor and 1174 for commercial. In a message-based API this becomes a check that the reply fits the caller's limit, with '98' when it does not.
  - UP-BR-054: For an endowment policy, the space needed is 33 + 124 bytes plus the length of the policy's free-form padding data when present. The padding length must be read with the policy, so the size check and the reply use the same value.
  - UP-BR-056: An endowment reply ends with the end-of-data marker 'FINAL', written straight after the padding data: at position 1 plus the padding length, or position 1 when there is none. Callers use it to find where the policy data ends. An API with explicit field lengths may not need it, but it must stay while existing callers read it.
- [ ] UP-C06-T5 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-030, UP-REQ-F-031, UP-REQ-F-032, UP-REQ-F-033, UP-REQ-F-034, UP-REQ-F-035, UP-REQ-F-036, UP-REQ-F-037, UP-REQ-F-038. Criteria: UP-C06-AC-01, UP-C06-AC-02, UP-C06-AC-03, UP-C06-AC-04, UP-C06-AC-05, UP-C06-AC-06, UP-C06-AC-07, UP-C06-AC-08, UP-C06-AC-09, UP-C06-AC-10, UP-C06-AC-11, UP-C06-AC-12, UP-C06-AC-13, UP-C06-AC-14, UP-C06-AC-15. After: UP-C06-T1, UP-C06-T2, UP-C06-T3, UP-C06-T4.
  - 15 acceptance criteria, each a test named by its ID.
- [ ] UP-C06-T6 [compliance] Review the handling of money, personal data. Requirements: UP-REQ-F-030, UP-REQ-F-031, UP-REQ-F-032, UP-REQ-F-033, UP-REQ-F-034, UP-REQ-F-035, UP-REQ-F-036, UP-REQ-F-037, UP-REQ-F-038. After: UP-C06-T1, UP-C06-T2, UP-C06-T3, UP-C06-T4.
  - Check storage, logs, screens and audit against the rules.
