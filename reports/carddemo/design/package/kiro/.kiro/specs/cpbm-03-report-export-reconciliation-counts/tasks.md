# Implementation plan: Report export reconciliation counts (CPBM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CPBM-C03-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
- [ ] 2. CPBM-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
  - _Rules: CPBM-BR-012, CPBM-BR-013_
  - _After: CPBM-C03-T1_
- [ ] 3. CPBM-C03-T3 [api] Build the service
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
  - _Rules: CPBM-BR-012, CPBM-BR-013_
  - _After: CPBM-C03-T1, CPBM-C03-T2_
- [ ] 4. CPBM-C03-T4 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
  - _Criteria: CPBM-C03-AC-01, CPBM-C03-AC-02_
  - _After: CPBM-C03-T1, CPBM-C03-T2, CPBM-C03-T3_
- [ ] 5. CPBM-C03-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
  - _After: CPBM-C03-T1, CPBM-C03-T2, CPBM-C03-T3_
