# Implementation plan: Calculate and post monthly interest (DTPR-C05)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C05-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA02Y, CVTRA05Y (see data-contracts.md).
  - _Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051_
- [ ] 2. DTPR-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: DTPR-BR-051.
  - _Requirements: DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-046_
  - _Rules: DTPR-BR-045, DTPR-BR-046, DTPR-BR-047, DTPR-BR-048, DTPR-BR-049, DTPR-BR-050, DTPR-BR-051, DTPR-BR-052, DTPR-BR-053_
  - _After: DTPR-C05-T1_
- [ ] 3. DTPR-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051_
  - _Rules: DTPR-BR-054, DTPR-BR-055, DTPR-BR-056_
  - _After: DTPR-C05-T1_
- [ ] 4. DTPR-C05-T4 [api] Build the scheduled job
  - DTPR-BR-044: Read all category balances in key order (account ID, then type, then category) as one sorted stream, so each account's balances come together. The per-account interest total and the account rewrite depend on that grouping.
  - _Requirements: DTPR-REQ-F-038_
  - _Rules: DTPR-BR-044_
  - _After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3_
- [ ] 5. DTPR-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 17 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051_
  - _Criteria: DTPR-C05-AC-01, DTPR-C05-AC-02, DTPR-C05-AC-03, DTPR-C05-AC-04, DTPR-C05-AC-05, DTPR-C05-AC-06, DTPR-C05-AC-07, DTPR-C05-AC-08, DTPR-C05-AC-09, DTPR-C05-AC-10, DTPR-C05-AC-11, DTPR-C05-AC-12, DTPR-C05-AC-13, DTPR-C05-AC-14, DTPR-C05-AC-15, DTPR-C05-AC-16, DTPR-C05-AC-17_
  - _After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3, DTPR-C05-T4_
- [ ] 6. DTPR-C05-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051_
  - _After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3, DTPR-C05-T4_
