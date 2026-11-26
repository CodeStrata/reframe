# Tasks: List card transactions and total (ASGD-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ASGD-C05-T1 [data] Model the data the capability reads and writes. Requirements: ASGD-REQ-F-019, ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-023, ASGD-REQ-F-024, ASGD-REQ-F-025.
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
- [ ] ASGD-C05-T2 [business-rules] Implement the business rules. Requirements: ASGD-REQ-F-019, ASGD-REQ-F-023. Rules: ASGD-BR-020, ASGD-BR-021, ASGD-BR-024. After: ASGD-C05-T1.
  - Keep each business rule exactly as specified.
- [ ] ASGD-C05-T3 [business-rules] Implement error handling and messages. Requirements: ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-024, ASGD-REQ-F-025. Rules: ASGD-BR-021, ASGD-BR-022, ASGD-BR-023, ASGD-BR-025, ASGD-BR-026. After: ASGD-C05-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ASGD-C05-T4 [api] Build the scheduled job. Requirements: ASGD-REQ-F-019, ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-023, ASGD-REQ-F-024, ASGD-REQ-F-025. Rules: ASGD-BR-020, ASGD-BR-021, ASGD-BR-022, ASGD-BR-023, ASGD-BR-024, ASGD-BR-025, ASGD-BR-026. After: ASGD-C05-T1, ASGD-C05-T2, ASGD-C05-T3.
  - Expose the rules as the service the screens call.
- [ ] ASGD-C05-T5 [test-generation] Write a test for every acceptance criterion. Requirements: ASGD-REQ-F-019, ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-023, ASGD-REQ-F-024, ASGD-REQ-F-025. Criteria: ASGD-C05-AC-01, ASGD-C05-AC-02, ASGD-C05-AC-03, ASGD-C05-AC-04, ASGD-C05-AC-05, ASGD-C05-AC-06, ASGD-C05-AC-07, ASGD-C05-AC-08, ASGD-C05-AC-09. After: ASGD-C05-T1, ASGD-C05-T2, ASGD-C05-T3, ASGD-C05-T4.
  - 9 acceptance criteria, each a test named by its ID.
- [ ] ASGD-C05-T6 [compliance] Review the handling of card data, money. Requirements: ASGD-REQ-F-019, ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-023, ASGD-REQ-F-024, ASGD-REQ-F-025. After: ASGD-C05-T1, ASGD-C05-T2, ASGD-C05-T3, ASGD-C05-T4.
  - Check storage, logs, screens and audit against the rules.
