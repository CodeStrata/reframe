# Implementation plan: Validate daily transactions (DTPR-C02)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C02-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA05Y, CVTRA06Y (see data-contracts.md).
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
- [ ] 2. DTPR-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
  - _Rules: DTPR-BR-014, DTPR-BR-015, DTPR-BR-016, DTPR-BR-017, DTPR-BR-018, DTPR-BR-019, DTPR-BR-020, DTPR-BR-021, DTPR-BR-022, DTPR-BR-023, DTPR-BR-024_
  - _After: DTPR-C02-T1_
- [ ] 3. DTPR-C02-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
  - _Rules: DTPR-BR-014, DTPR-BR-015, DTPR-BR-016, DTPR-BR-017, DTPR-BR-018, DTPR-BR-019, DTPR-BR-020, DTPR-BR-021, DTPR-BR-022, DTPR-BR-023, DTPR-BR-024_
  - _After: DTPR-C02-T1, DTPR-C02-T2_
- [ ] 4. DTPR-C02-T4 [test-generation] Write a test for every acceptance criterion
  - 20 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
  - _Criteria: DTPR-C02-AC-01, DTPR-C02-AC-02, DTPR-C02-AC-03, DTPR-C02-AC-04, DTPR-C02-AC-05, DTPR-C02-AC-06, DTPR-C02-AC-07, DTPR-C02-AC-08, DTPR-C02-AC-09, DTPR-C02-AC-10, DTPR-C02-AC-11, DTPR-C02-AC-12, DTPR-C02-AC-13, DTPR-C02-AC-14, DTPR-C02-AC-15, DTPR-C02-AC-16, DTPR-C02-AC-17, DTPR-C02-AC-18, DTPR-C02-AC-19, DTPR-C02-AC-20_
  - _After: DTPR-C02-T1, DTPR-C02-T2, DTPR-C02-T3_
- [ ] 5. DTPR-C02-T5 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
  - _After: DTPR-C02-T1, DTPR-C02-T2, DTPR-C02-T3_
