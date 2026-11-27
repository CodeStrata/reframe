# Tasks: Produce account extracts from the account master (DTPR-C14)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C14-T1 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-073. Rules: DTPR-BR-081.
  - Keep each business rule exactly as specified.
- [ ] DTPR-C14-T2 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-N-009, DTPR-REQ-N-010. Rules: DTPR-BR-082.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C14-T3 [api] Build the scheduled job. Requirements: DTPR-REQ-F-072. Rules: DTPR-BR-080. After: DTPR-C14-T1, DTPR-C14-T2.
  - DTPR-BR-080: The extract job must clear out the previous run's account extract, account array extract and variable-record extract before writing, so each run's outputs are regenerated from scratch and never appended to or merged with older data.
- [ ] DTPR-C14-T4 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-072, DTPR-REQ-F-073, DTPR-REQ-N-009, DTPR-REQ-N-010. Criteria: DTPR-C14-AC-01, DTPR-C14-AC-02, DTPR-C14-AC-03. After: DTPR-C14-T1, DTPR-C14-T2, DTPR-C14-T3.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C14-T5 [compliance] Review the handling of money. Requirements: DTPR-REQ-F-072, DTPR-REQ-F-073, DTPR-REQ-N-009, DTPR-REQ-N-010. After: DTPR-C14-T1, DTPR-C14-T2, DTPR-C14-T3.
  - Check storage, logs, screens and audit against the rules.
