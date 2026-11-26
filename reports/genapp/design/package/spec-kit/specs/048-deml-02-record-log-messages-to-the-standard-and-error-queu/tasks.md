# Tasks: Record log messages to the standard and error queues (DEML-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DEML-C02-T1 [business-rules] Implement the business rules. Requirements: DEML-REQ-F-006, DEML-REQ-F-007, DEML-REQ-F-005, DEML-REQ-F-008. Rules: DEML-BR-005, DEML-BR-006, DEML-BR-007, DEML-BR-008.
  - Keep each business rule exactly as specified.
- [ ] DEML-C02-T2 [business-rules] Implement error handling and messages. Requirements: DEML-REQ-N-001. Rules: DEML-BR-009.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DEML-C02-T3 [api] Build the service. Requirements: DEML-REQ-F-005, DEML-REQ-F-006, DEML-REQ-F-007, DEML-REQ-F-008, DEML-REQ-N-001. Rules: DEML-BR-005, DEML-BR-006, DEML-BR-007, DEML-BR-008, DEML-BR-009. After: DEML-C02-T1, DEML-C02-T2.
  - Expose the rules as the service the screens call.
- [ ] DEML-C02-T4 [test-generation] Write a test for every acceptance criterion. Requirements: DEML-REQ-F-005, DEML-REQ-F-006, DEML-REQ-F-007, DEML-REQ-F-008, DEML-REQ-N-001. Criteria: DEML-C02-AC-01, DEML-C02-AC-02, DEML-C02-AC-03, DEML-C02-AC-04, DEML-C02-AC-05, DEML-C02-AC-06. After: DEML-C02-T1, DEML-C02-T2, DEML-C02-T3.
  - 6 acceptance criteria, each a test named by its ID.
- [ ] DEML-C02-T5 [compliance] Review the handling of audit. Requirements: DEML-REQ-F-005, DEML-REQ-F-006, DEML-REQ-F-007, DEML-REQ-F-008, DEML-REQ-N-001. After: DEML-C02-T1, DEML-C02-T2, DEML-C02-T3.
  - Check storage, logs, screens and audit against the rules.
