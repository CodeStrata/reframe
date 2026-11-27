# Implementation plan: Stop the export on any file error (CPBM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CPBM-C04-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
- [ ] 2. CPBM-C04-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
  - _Rules: CPBM-BR-014, CPBM-BR-015, CPBM-BR-016_
  - _After: CPBM-C04-T1_
- [ ] 3. CPBM-C04-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
  - _Rules: CPBM-BR-014, CPBM-BR-015, CPBM-BR-016_
  - _After: CPBM-C04-T1, CPBM-C04-T2_
- [ ] 4. CPBM-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
  - _Criteria: CPBM-C04-AC-01, CPBM-C04-AC-02, CPBM-C04-AC-03, CPBM-C04-AC-04, CPBM-C04-AC-05, CPBM-C04-AC-06_
  - _After: CPBM-C04-T1, CPBM-C04-T2, CPBM-C04-T3_
- [ ] 5. CPBM-C04-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
  - _After: CPBM-C04-T1, CPBM-C04-T2, CPBM-C04-T3_
