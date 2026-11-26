# Tasks: Extract account data to output files (DTPR-C01)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C01-T1 [data] Model the data the capability reads and writes. Requirements: DTPR-REQ-F-001, DTPR-REQ-F-002, DTPR-REQ-F-003, DTPR-REQ-F-004, DTPR-REQ-F-005, DTPR-REQ-F-006, DTPR-REQ-F-007, DTPR-REQ-F-008, DTPR-REQ-F-009, DTPR-REQ-F-010, DTPR-REQ-F-011, DTPR-REQ-F-012.
  - File records: CVACT01Y (see data-contracts.md).
  - Working records it passes or builds: CODATECN.
- [ ] DTPR-C01-T2 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-003, DTPR-REQ-F-004, DTPR-REQ-F-005. Rules: DTPR-BR-004, DTPR-BR-005, DTPR-BR-006. After: DTPR-C01-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: DTPR-BR-006.
- [ ] DTPR-C01-T3 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-F-009, DTPR-REQ-F-010, DTPR-REQ-F-012. Rules: DTPR-BR-010, DTPR-BR-011, DTPR-BR-013. After: DTPR-C01-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C01-T4 [api] Build the scheduled job. Requirements: DTPR-REQ-F-001, DTPR-REQ-F-002, DTPR-REQ-F-006, DTPR-REQ-F-007, DTPR-REQ-F-008, DTPR-REQ-F-011. Rules: DTPR-BR-001, DTPR-BR-002, DTPR-BR-003, DTPR-BR-007, DTPR-BR-008, DTPR-BR-009, DTPR-BR-012. After: DTPR-C01-T1, DTPR-C01-T2, DTPR-C01-T3.
  - DTPR-BR-001: Map each account straight onto the flat account extract record: ID, active status, current balance, credit limit, cash credit limit, open date, expiration date, current cycle credit and group ID, with no changes to the values. Define the extract layout as a versioned contract that its downstream consumers agree to.
  - DTPR-BR-002: Parse the reissue date once from its stored YYYY-MM-DD form. Use it both for the YYYYMMDD output date and for the four-digit reissue year in the financial record, so the two can never disagree.
  - DTPR-BR-003: Use a standard date library to reformat the reissue date from YYYY-MM-DD to YYYYMMDD instead of a separate shared date-conversion routine. Decide and test how an invalid or blank reissue date is handled.
  - DTPR-BR-007: Produce a fixed 12-character status record per account: the account ID zero-padded to 11 digits, then the one-character active status. Downstream readers depend on the exact width.
  - DTPR-BR-008: After each account's status record, produce a 39-byte financial record (account ID, current balance, credit limit, reissue year) in the same output stream. Keep the order status-then-financial for each account, and give the numeric fields an agreed fixed encoding.
  - DTPR-BR-009: Process accounts as a sequential stream over the whole account master. Each account produces exactly one account record, one balance array record and two variable-length records, so the record counts can be reconciled (N, N, 2N) at the end of the run.
  - DTPR-BR-012: Treat running out of accounts as normal completion: close the source and log the completion message 'END OF EXECUTION OF PROGRAM CBACT01C' (or an agreed equivalent) with a success exit status for the scheduler.
- [ ] DTPR-C01-T5 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-001, DTPR-REQ-F-002, DTPR-REQ-F-003, DTPR-REQ-F-004, DTPR-REQ-F-005, DTPR-REQ-F-006, DTPR-REQ-F-007, DTPR-REQ-F-008, DTPR-REQ-F-009, DTPR-REQ-F-010, DTPR-REQ-F-011, DTPR-REQ-F-012. Criteria: DTPR-C01-AC-01, DTPR-C01-AC-02, DTPR-C01-AC-03, DTPR-C01-AC-04, DTPR-C01-AC-05, DTPR-C01-AC-06, DTPR-C01-AC-07, DTPR-C01-AC-08, DTPR-C01-AC-09, DTPR-C01-AC-10, DTPR-C01-AC-11, DTPR-C01-AC-12, DTPR-C01-AC-13, DTPR-C01-AC-14, DTPR-C01-AC-15. After: DTPR-C01-T1, DTPR-C01-T2, DTPR-C01-T3, DTPR-C01-T4.
  - 15 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C01-T6 [compliance] Review the handling of money. Requirements: DTPR-REQ-F-001, DTPR-REQ-F-002, DTPR-REQ-F-003, DTPR-REQ-F-004, DTPR-REQ-F-005, DTPR-REQ-F-006, DTPR-REQ-F-007, DTPR-REQ-F-008, DTPR-REQ-F-009, DTPR-REQ-F-010, DTPR-REQ-F-011, DTPR-REQ-F-012. After: DTPR-C01-T1, DTPR-C01-T2, DTPR-C01-T3, DTPR-C01-T4.
  - Check storage, logs, screens and audit against the rules.
