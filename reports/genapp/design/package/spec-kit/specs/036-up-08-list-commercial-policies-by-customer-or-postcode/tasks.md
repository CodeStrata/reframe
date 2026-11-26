# Tasks: List commercial policies by customer or postcode (UP-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C08-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-048, UP-REQ-F-049, UP-REQ-F-050.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] UP-C08-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-050. Rules: UP-BR-067, UP-BR-068, UP-BR-069, UP-BR-072. After: UP-C08-T1.
  - Keep each business rule exactly as specified.
- [ ] UP-C08-T3 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-048, UP-REQ-F-049. Rules: UP-BR-070, UP-BR-071. After: UP-C08-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C08-T4 [api] Build the scheduled job. Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-048, UP-REQ-F-049, UP-REQ-F-050. Rules: UP-BR-067, UP-BR-068, UP-BR-069, UP-BR-070, UP-BR-071, UP-BR-072. After: UP-C08-T1, UP-C08-T2, UP-C08-T3.
  - Expose the rules as the service the screens call.
- [ ] UP-C08-T5 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-048, UP-REQ-F-049, UP-REQ-F-050. Criteria: UP-C08-AC-01, UP-C08-AC-02, UP-C08-AC-03, UP-C08-AC-04, UP-C08-AC-05, UP-C08-AC-06, UP-C08-AC-07. After: UP-C08-T1, UP-C08-T2, UP-C08-T3, UP-C08-T4.
  - 7 acceptance criteria, each a test named by its ID.
- [ ] UP-C08-T6 [compliance] Review the handling of money, personal data. Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-048, UP-REQ-F-049, UP-REQ-F-050. After: UP-C08-T1, UP-C08-T2, UP-C08-T3, UP-C08-T4.
  - Check storage, logs, screens and audit against the rules.
