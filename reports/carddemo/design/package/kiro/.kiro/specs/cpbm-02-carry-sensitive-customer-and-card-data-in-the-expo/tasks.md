# Implementation plan: Carry sensitive customer and card data in the export (CPBM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CPBM-C02-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
- [ ] 2. CPBM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
  - _Rules: CPBM-BR-009, CPBM-BR-010, CPBM-BR-011_
  - _After: CPBM-C02-T1_
- [ ] 3. CPBM-C02-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
  - _Rules: CPBM-BR-009, CPBM-BR-010, CPBM-BR-011_
  - _After: CPBM-C02-T1, CPBM-C02-T2_
- [ ] 4. CPBM-C02-T4 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
  - _Criteria: CPBM-C02-AC-01, CPBM-C02-AC-02, CPBM-C02-AC-03, CPBM-C02-AC-04_
  - _After: CPBM-C02-T1, CPBM-C02-T2, CPBM-C02-T3_
- [ ] 5. CPBM-C02-T5 [compliance] Review the handling of card data, personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
  - _After: CPBM-C02-T1, CPBM-C02-T2, CPBM-C02-T3_
