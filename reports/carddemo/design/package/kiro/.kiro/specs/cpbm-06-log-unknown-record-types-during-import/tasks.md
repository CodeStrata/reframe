# Implementation plan: Log unknown record types during import (CPBM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CPBM-C06-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
- [ ] 2. CPBM-C06-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
  - _Rules: CPBM-BR-026, CPBM-BR-027, CPBM-BR-028_
  - _After: CPBM-C06-T1_
- [ ] 3. CPBM-C06-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
  - _Rules: CPBM-BR-026, CPBM-BR-027, CPBM-BR-028_
  - _After: CPBM-C06-T1, CPBM-C06-T2_
- [ ] 4. CPBM-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
  - _Criteria: CPBM-C06-AC-01, CPBM-C06-AC-02, CPBM-C06-AC-03, CPBM-C06-AC-04_
  - _After: CPBM-C06-T1, CPBM-C06-T2, CPBM-C06-T3_
- [ ] 5. CPBM-C06-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
  - _After: CPBM-C06-T1, CPBM-C06-T2, CPBM-C06-T3_
