# Implementation plan: Report import run statistics (CPBM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CPBM-C07-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
- [ ] 2. CPBM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CPBM-BR-030, CPBM-BR-031.
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
  - _Rules: CPBM-BR-029, CPBM-BR-030, CPBM-BR-031_
  - _After: CPBM-C07-T1_
- [ ] 3. CPBM-C07-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
  - _Rules: CPBM-BR-029, CPBM-BR-030, CPBM-BR-031_
  - _After: CPBM-C07-T1, CPBM-C07-T2_
- [ ] 4. CPBM-C07-T4 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
  - _Criteria: CPBM-C07-AC-01, CPBM-C07-AC-02, CPBM-C07-AC-03, CPBM-C07-AC-04, CPBM-C07-AC-05_
  - _After: CPBM-C07-T1, CPBM-C07-T2, CPBM-C07-T3_
- [ ] 5. CPBM-C07-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
  - _After: CPBM-C07-T1, CPBM-C07-T2, CPBM-C07-T3_
