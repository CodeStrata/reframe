# Tasks: Total transaction counters by outcome and type (TSM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TSM-C02-T1 [business-rules] Implement the business rules. Requirements: TSM-REQ-F-005, TSM-REQ-F-006, TSM-REQ-F-007, TSM-REQ-F-008, TSM-REQ-F-009, TSM-REQ-F-010. Rules: TSM-BR-003, TSM-BR-004, TSM-BR-005, TSM-BR-006, TSM-BR-007, TSM-BR-008.
  - Keep each business rule exactly as specified.
- [ ] TSM-C02-T2 [api] Build the scheduled job. Requirements: TSM-REQ-F-005, TSM-REQ-F-006, TSM-REQ-F-007, TSM-REQ-F-008, TSM-REQ-F-009, TSM-REQ-F-010. Rules: TSM-BR-003, TSM-BR-004, TSM-BR-005, TSM-BR-006, TSM-BR-007, TSM-BR-008. After: TSM-C02-T1.
  - Expose the rules as the service the screens call.
- [ ] TSM-C02-T3 [test-generation] Write a test for every acceptance criterion. Requirements: TSM-REQ-F-005, TSM-REQ-F-006, TSM-REQ-F-007, TSM-REQ-F-008, TSM-REQ-F-009, TSM-REQ-F-010. Criteria: TSM-C02-AC-01, TSM-C02-AC-02, TSM-C02-AC-03, TSM-C02-AC-04, TSM-C02-AC-05, TSM-C02-AC-06. After: TSM-C02-T1, TSM-C02-T2.
  - 6 acceptance criteria, each a test named by its ID.
