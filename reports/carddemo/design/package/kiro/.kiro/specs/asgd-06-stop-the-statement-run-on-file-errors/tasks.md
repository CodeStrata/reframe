# Implementation plan: Stop the statement run on file errors (ASGD-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ASGD-C06-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
- [ ] 2. ASGD-C06-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
  - _Rules: ASGD-BR-012, ASGD-BR-027, ASGD-BR-028, ASGD-BR-029, ASGD-BR-030, ASGD-BR-031, ASGD-BR-032_
  - _After: ASGD-C06-T1_
- [ ] 3. ASGD-C06-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
  - _Rules: ASGD-BR-012, ASGD-BR-027, ASGD-BR-028, ASGD-BR-029, ASGD-BR-030, ASGD-BR-031, ASGD-BR-032_
  - _After: ASGD-C06-T1, ASGD-C06-T2_
- [ ] 4. ASGD-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
  - _Criteria: ASGD-C06-AC-01, ASGD-C06-AC-02, ASGD-C06-AC-03, ASGD-C06-AC-04, ASGD-C06-AC-05, ASGD-C06-AC-06, ASGD-C06-AC-07_
  - _After: ASGD-C06-T1, ASGD-C06-T2, ASGD-C06-T3_
- [ ] 5. ASGD-C06-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
  - _After: ASGD-C06-T1, ASGD-C06-T2, ASGD-C06-T3_
