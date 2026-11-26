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
  - CAFM-BR-001: The job needs a parameter setup step at start-up: record today's date as the run date, take expiry days from the job parameters when numeric or else use 5, and set the checkpoint frequency to 5 when it is missing, blank or 0. Expose these as validated job configuration, not as positional text.
  - CAFM-BR-002: Run the purge as a scheduled batch job with write access to the pending authorization store (summaries and their details). The legacy IMS batch program, PSB and DBD library setup becomes the job's scheduler entry and its database credentials and permissions.
  - CAFM-BR-004: The job needs a full pass over all pending authorization summaries, one account at a time, with each summary's child details checked and expired ones deleted before it moves to the next summary. Commit progress at the configured checkpoint frequency so the job can restart after a failure without starting over.
- [ ] CAFM-C01-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-002, CAFM-REQ-F-003, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-008, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013. Criteria: CAFM-C01-AC-01, CAFM-C01-AC-02, CAFM-C01-AC-03, CAFM-C01-AC-04, CAFM-C01-AC-05, CAFM-C01-AC-06, CAFM-C01-AC-07, CAFM-C01-AC-08, CAFM-C01-AC-09, CAFM-C01-AC-10, CAFM-C01-AC-11, CAFM-C01-AC-12, CAFM-C01-AC-13, CAFM-C01-AC-14, CAFM-C01-AC-15, CAFM-C01-AC-16, CAFM-C01-AC-17, CAFM-C01-AC-18. After: CAFM-C01-T1, CAFM-C01-T2, CAFM-C01-T3, CAFM-C01-T4.
  - 18 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C01-T6 [compliance] Review the handling of money. Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-002, CAFM-REQ-F-003, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-008, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013. After: CAFM-C01-T1, CAFM-C01-T2, CAFM-C01-T3, CAFM-C01-T4.
  - Check storage, logs, screens and audit against the rules.
