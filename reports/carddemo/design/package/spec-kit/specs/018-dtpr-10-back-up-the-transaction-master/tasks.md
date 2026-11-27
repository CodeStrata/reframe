# Tasks: Back up the transaction master (DTPR-C10)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C10-T1 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-N-004, DTPR-REQ-N-005. Rules: DTPR-BR-069, DTPR-BR-071.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C10-T2 [api] Build the scheduled job. Requirements: DTPR-REQ-F-064. Rules: DTPR-BR-069, DTPR-BR-070. After: DTPR-C10-T1.
  - DTPR-BR-069: Run a scheduled snapshot job that copies every transaction to a new, versioned backup in the 350-byte layout. Publish the new version only on success and discard it on failure, keeping earlier versions available.
  - DTPR-BR-070: Take the snapshot with a consistent, non-blocking read (for example a read-only snapshot or export), so other jobs can still read the transaction master during the backup.
- [ ] DTPR-C10-T3 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-064, DTPR-REQ-N-004, DTPR-REQ-N-005. Criteria: DTPR-C10-AC-01, DTPR-C10-AC-02, DTPR-C10-AC-03, DTPR-C10-AC-04, DTPR-C10-AC-05. After: DTPR-C10-T1, DTPR-C10-T2.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C10-T4 [compliance] Review the handling of money. Requirements: DTPR-REQ-F-064, DTPR-REQ-N-004, DTPR-REQ-N-005. After: DTPR-C10-T1, DTPR-C10-T2.
  - Check storage, logs, screens and audit against the rules.
