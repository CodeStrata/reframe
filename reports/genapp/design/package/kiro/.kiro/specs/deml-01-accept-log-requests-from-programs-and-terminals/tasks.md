# Implementation plan: Accept log requests from programs and terminals (DEML-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. DEML-C01-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DEML-REQ-F-003_
  - _Rules: DEML-BR-003_
- [ ] 2. DEML-C01-T2 [api] Build the scheduled job
  - DEML-BR-001: Expose the logger as a callable service (in-process API or endpoint) that takes a message of up to 90 characters. The service prefixes the identifier of the producing system/instance and one space, and records the length as message length plus 5. Keep the 90-character limit and the 'system-id space text' layout so existing log readers still work.
  - DEML-BR-002: Give operators a separate entry point (a console command or simple form) for typing a message by hand. When the input still carries a 5-character command/transaction prefix, strip it and keep at most the next 74 characters as the message. Then pass it through the same record-building path, with length computed as input length minus 5, plus 5.
  - DEML-BR-004: A program-call submission must return straight to the caller with no user-facing output and no result the caller has to handle. Make it a fire-and-forget call that does not change the caller's flow.
  - _Requirements: DEML-REQ-F-001, DEML-REQ-F-002, DEML-REQ-F-004_
  - _Rules: DEML-BR-001, DEML-BR-002, DEML-BR-004_
  - _After: DEML-C01-T1_
- [ ] 3. DEML-C01-T3 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: DEML-REQ-F-001, DEML-REQ-F-002, DEML-REQ-F-003, DEML-REQ-F-004_
  - _Criteria: DEML-C01-AC-01, DEML-C01-AC-02, DEML-C01-AC-03, DEML-C01-AC-04, DEML-C01-AC-05, DEML-C01-AC-06_
  - _After: DEML-C01-T1, DEML-C01-T2_
- [ ] 4. DEML-C01-T4 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DEML-REQ-F-001, DEML-REQ-F-002, DEML-REQ-F-003, DEML-REQ-F-004_
  - _After: DEML-C01-T1, DEML-C01-T2_
