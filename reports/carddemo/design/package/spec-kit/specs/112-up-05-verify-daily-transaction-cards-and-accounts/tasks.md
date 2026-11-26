# Tasks: Verify daily transaction cards and accounts (UP-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C05-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024.
  - File records: CVACT01Y, CVACT03Y, CVTRA06Y (see data-contracts.md).
  - Working records it passes or builds: CVACT02Y, CVCUS01Y, CVTRA05Y.
- [ ] UP-C05-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-017, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-023. Rules: UP-BR-019, UP-BR-021, UP-BR-022, UP-BR-025. After: UP-C05-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-025.
- [ ] UP-C05-T3 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-016, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-018, UP-REQ-F-024. Rules: UP-BR-018, UP-BR-020, UP-BR-023, UP-BR-024, UP-BR-026. After: UP-C05-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C05-T4 [api] Build the service. Requirements: UP-REQ-F-015. Rules: UP-BR-017. After: UP-C05-T1, UP-C05-T2, UP-C05-T3.
  - UP-BR-017: A batch job that streams the day's transaction feed in file order, one record at a time. It logs each record and runs card verification on it, and it finishes when the feed is used up. End of feed is the normal way to finish.
- [ ] UP-C05-T5 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024. Criteria: UP-C05-AC-01, UP-C05-AC-02, UP-C05-AC-03, UP-C05-AC-04, UP-C05-AC-05, UP-C05-AC-06, UP-C05-AC-07, UP-C05-AC-08, UP-C05-AC-09, UP-C05-AC-10, UP-C05-AC-11. After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4.
  - 11 acceptance criteria, each a test named by its ID.
- [ ] UP-C05-T6 [compliance] Review the handling of card data, personal data. Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024. After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4.
  - Check storage, logs, screens and audit against the rules.
