# Implementation plan: Abort the import on any file failure (CPBM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CPBM-C08-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029_
- [ ] 2. CPBM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-F-028_
  - _Rules: CPBM-BR-020, CPBM-BR-021, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-034_
  - _After: CPBM-C08-T1_
- [ ] 3. CPBM-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-029_
  - _Rules: CPBM-BR-017, CPBM-BR-032, CPBM-BR-033, CPBM-BR-035_
  - _After: CPBM-C08-T1_
- [ ] 4. CPBM-C08-T4 [api] Build the scheduled job
  - CPBM-BR-021: The account write must report failure to the job, so that a failed write stops the whole import rather than being skipped.
  - CPBM-BR-022: The cross-reference write must report failure to the job, so that a failed write stops the whole import.
  - CPBM-BR-023: The transaction write must report failure to the job, so that a failed write stops the whole import.
  - CPBM-BR-017: Make the import all-or-nothing: write the targets to staging (or inside a transaction) and publish them only when the step succeeds; on an abnormal end, remove the customer, account, cross-reference, transaction and error outputs.
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029_
  - _Rules: CPBM-BR-017, CPBM-BR-020, CPBM-BR-021, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-032, CPBM-BR-033, CPBM-BR-034, CPBM-BR-035_
  - _After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3_
- [ ] 5. CPBM-C08-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029_
  - _Criteria: CPBM-C08-AC-01, CPBM-C08-AC-02, CPBM-C08-AC-03, CPBM-C08-AC-04, CPBM-C08-AC-05, CPBM-C08-AC-06, CPBM-C08-AC-07, CPBM-C08-AC-08, CPBM-C08-AC-09, CPBM-C08-AC-10_
  - _After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3, CPBM-C08-T4_
- [ ] 6. CPBM-C08-T6 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029_
  - _After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3, CPBM-C08-T4_
