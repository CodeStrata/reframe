# Tasks: Abort the import on any file failure (CPBM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CPBM-C08-T1 [data] Model the data the capability reads and writes. Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029.
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
- [ ] CPBM-C08-T2 [business-rules] Implement the business rules. Requirements: CPBM-REQ-F-028. Rules: CPBM-BR-020, CPBM-BR-021, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-034. After: CPBM-C08-T1.
  - Keep each business rule exactly as specified.
- [ ] CPBM-C08-T3 [business-rules] Implement error handling and messages. Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-029. Rules: CPBM-BR-017, CPBM-BR-032, CPBM-BR-033, CPBM-BR-035. After: CPBM-C08-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CPBM-C08-T4 [api] Build the scheduled job. Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029. Rules: CPBM-BR-017, CPBM-BR-020, CPBM-BR-021, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-032, CPBM-BR-033, CPBM-BR-034, CPBM-BR-035. After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3.
  - CPBM-BR-021: The account write must report failure to the job, so that a failed write stops the whole import rather than being skipped.
  - CPBM-BR-022: The cross-reference write must report failure to the job, so that a failed write stops the whole import.
  - CPBM-BR-023: The transaction write must report failure to the job, so that a failed write stops the whole import.
  - CPBM-BR-017: Make the import all-or-nothing: write the targets to staging (or inside a transaction) and publish them only when the step succeeds; on an abnormal end, remove the customer, account, cross-reference, transaction and error outputs.
- [ ] CPBM-C08-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029. Criteria: CPBM-C08-AC-01, CPBM-C08-AC-02, CPBM-C08-AC-03, CPBM-C08-AC-04, CPBM-C08-AC-05, CPBM-C08-AC-06, CPBM-C08-AC-07, CPBM-C08-AC-08, CPBM-C08-AC-09, CPBM-C08-AC-10. After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3, CPBM-C08-T4.
  - 10 acceptance criteria, each a test named by its ID.
- [ ] CPBM-C08-T6 [compliance] Review the handling of audit. Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029. After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3, CPBM-C08-T4.
  - Check storage, logs, screens and audit against the rules.
