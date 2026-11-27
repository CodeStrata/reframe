# Tasks: Consolidate transactions into the transaction master (DTPR-C09)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C09-T1 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-N-003. Rules: DTPR-BR-067.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C09-T2 [api] Build the scheduled job. Requirements: DTPR-REQ-F-062, DTPR-REQ-F-063. Rules: DTPR-BR-066, DTPR-BR-068. After: DTPR-C09-T1.
  - DTPR-BR-066: Build a sorted extract that merges the latest transaction backup with the latest system-transaction batch, ordered ascending by the 16-character transaction ID, and publish it as a new version. Make it a scheduled step that depends on the backup and interest jobs, and discard its output if it fails.
  - DTPR-BR-068: Load every record of the combined, sorted set into the transaction store keyed by transaction ID, as a bulk load or upsert in one step. Decide explicitly what to do with duplicate transaction IDs.
- [ ] DTPR-C09-T3 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-062, DTPR-REQ-N-003, DTPR-REQ-F-063. Criteria: DTPR-C09-AC-01, DTPR-C09-AC-02, DTPR-C09-AC-03. After: DTPR-C09-T1, DTPR-C09-T2.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C09-T4 [compliance] Review the handling of money. Requirements: DTPR-REQ-F-062, DTPR-REQ-N-003, DTPR-REQ-F-063. After: DTPR-C09-T1, DTPR-C09-T2.
  - Check storage, logs, screens and audit against the rules.
