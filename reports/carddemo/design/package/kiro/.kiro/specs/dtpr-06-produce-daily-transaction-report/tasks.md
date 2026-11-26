# Implementation plan: Produce daily transaction report (DTPR-C06)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C06-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA03Y, CVTRA04Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: CVTRA07Y.
  - _Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056_
- [ ] 2. DTPR-C06-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-056_
  - _Rules: DTPR-BR-057, DTPR-BR-058, DTPR-BR-060_
  - _After: DTPR-C06-T1_
- [ ] 3. DTPR-C06-T3 [api] Build the services and the scheduled job
  - DTPR-BR-059: For each in-range transaction, look up the card's cross-reference (giving the account) by card number, the type description by type code, and the category description by type and category code. A missing reference record must fail the report run rather than print a blank. The type and category tables are small and can be cached for the run.
  - _Requirements: DTPR-REQ-F-054, DTPR-REQ-F-055_
  - _Rules: DTPR-BR-059_
  - _After: DTPR-C06-T1, DTPR-C06-T2_
- [ ] 4. DTPR-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056_
  - _Criteria: DTPR-C06-AC-01, DTPR-C06-AC-02, DTPR-C06-AC-03, DTPR-C06-AC-04, DTPR-C06-AC-05, DTPR-C06-AC-06, DTPR-C06-AC-07, DTPR-C06-AC-08_
  - _After: DTPR-C06-T1, DTPR-C06-T2, DTPR-C06-T3_
- [ ] 5. DTPR-C06-T5 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056_
  - _After: DTPR-C06-T1, DTPR-C06-T2, DTPR-C06-T3_
