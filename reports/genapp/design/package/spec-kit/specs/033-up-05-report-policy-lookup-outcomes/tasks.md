# Tasks: Report policy lookup outcomes (UP-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C05-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028, UP-REQ-F-029.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] UP-C05-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-028. Rules: UP-BR-049. After: UP-C05-T1.
  - Keep each business rule exactly as specified.
- [ ] UP-C05-T3 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-029. Rules: UP-BR-045, UP-BR-046, UP-BR-047, UP-BR-048, UP-BR-050. After: UP-C05-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C05-T4 [api] Build the scheduled job. Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028, UP-REQ-F-029. Rules: UP-BR-045, UP-BR-046, UP-BR-047, UP-BR-048, UP-BR-049, UP-BR-050. After: UP-C05-T1, UP-C05-T2, UP-C05-T3.
  - Expose the rules as the service the screens call.
- [ ] UP-C05-T5 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028, UP-REQ-F-029. Criteria: UP-C05-AC-01, UP-C05-AC-02, UP-C05-AC-03, UP-C05-AC-04, UP-C05-AC-05, UP-C05-AC-06, UP-C05-AC-07, UP-C05-AC-08. After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] UP-C05-T6 [compliance] Review the handling of audit, personal data. Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028, UP-REQ-F-029. After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4.
  - Check storage, logs, screens and audit against the rules.
