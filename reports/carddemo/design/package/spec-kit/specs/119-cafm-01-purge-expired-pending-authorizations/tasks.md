# Tasks: Purge expired pending authorizations (CAFM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C01-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-002, CAFM-REQ-F-003, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-008, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013.
  - File records: CIPAUSMY (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY.
- [ ] CAFM-C01-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-002, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013. Rules: CAFM-BR-003, CAFM-BR-005, CAFM-BR-006, CAFM-BR-007, CAFM-BR-009, CAFM-BR-010, CAFM-BR-011, CAFM-BR-012. After: CAFM-C01-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C01-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-008. Rules: CAFM-BR-008. After: CAFM-C01-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C01-T4 [api] Build the scheduled job. Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-003. Rules: CAFM-BR-001, CAFM-BR-002, CAFM-BR-004. After: CAFM-C01-T1, CAFM-C01-T2, CAFM-C01-T3.
  - CAFM-BR-001: At start-up the job takes the run date from the system clock and reads two run parameters. Expiry days is used when numeric and defaults to 5 otherwise. Checkpoint frequency defaults to 5 when it is blank, zero or missing. Check both values before any data is touched.
  - CAFM-BR-002: Run the purge as a scheduled batch job that has update access to the pending authorization store, both summaries and details. It runs alongside the online authorization service, so it must commit in small batches (see the checkpoint frequency) rather than locking the whole store.
  - CAFM-BR-004: Read every account summary in turn and, for each one, all of its authorization details. Delete the details that qualify, then decide whether the summary goes too, before moving to the next account. A parent-child query or keyset cursor over summaries with their details is enough. Commit every checkpoint-frequency summaries so a restart can resume from the last committed account.
- [ ] CAFM-C01-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-002, CAFM-REQ-F-003, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-008, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013. Criteria: CAFM-C01-AC-01, CAFM-C01-AC-02, CAFM-C01-AC-03, CAFM-C01-AC-04, CAFM-C01-AC-05, CAFM-C01-AC-06, CAFM-C01-AC-07, CAFM-C01-AC-08, CAFM-C01-AC-09, CAFM-C01-AC-10, CAFM-C01-AC-11, CAFM-C01-AC-12, CAFM-C01-AC-13, CAFM-C01-AC-14, CAFM-C01-AC-15, CAFM-C01-AC-16, CAFM-C01-AC-17, CAFM-C01-AC-18. After: CAFM-C01-T1, CAFM-C01-T2, CAFM-C01-T3, CAFM-C01-T4.
  - 18 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C01-T6 [compliance] Review the handling of money. Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-002, CAFM-REQ-F-003, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-008, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013. After: CAFM-C01-T1, CAFM-C01-T2, CAFM-C01-T3, CAFM-C01-T4.
  - Check storage, logs, screens and audit against the rules.
