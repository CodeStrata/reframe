# Tasks: Validate daily transactions (DTPR-C02)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C02-T1 [data] Model the data the capability reads and writes. Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019.
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA05Y, CVTRA06Y (see data-contracts.md).
- [ ] DTPR-C02-T2 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019. Rules: DTPR-BR-014, DTPR-BR-015, DTPR-BR-016, DTPR-BR-017, DTPR-BR-018, DTPR-BR-019, DTPR-BR-020, DTPR-BR-021, DTPR-BR-022, DTPR-BR-023, DTPR-BR-024. After: DTPR-C02-T1.
  - Keep each business rule exactly as specified.
- [ ] DTPR-C02-T3 [api] Build the scheduled job. Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019. Rules: DTPR-BR-014, DTPR-BR-015, DTPR-BR-016, DTPR-BR-017, DTPR-BR-018, DTPR-BR-019, DTPR-BR-020, DTPR-BR-021, DTPR-BR-022, DTPR-BR-023, DTPR-BR-024. After: DTPR-C02-T1, DTPR-C02-T2.
  - Expose the rules as the service the screens call.
- [ ] DTPR-C02-T4 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019. Criteria: DTPR-C02-AC-01, DTPR-C02-AC-02, DTPR-C02-AC-03, DTPR-C02-AC-04, DTPR-C02-AC-05, DTPR-C02-AC-06, DTPR-C02-AC-07, DTPR-C02-AC-08, DTPR-C02-AC-09, DTPR-C02-AC-10, DTPR-C02-AC-11, DTPR-C02-AC-12, DTPR-C02-AC-13, DTPR-C02-AC-14, DTPR-C02-AC-15, DTPR-C02-AC-16, DTPR-C02-AC-17, DTPR-C02-AC-18, DTPR-C02-AC-19, DTPR-C02-AC-20. After: DTPR-C02-T1, DTPR-C02-T2, DTPR-C02-T3.
  - 20 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C02-T5 [compliance] Review the handling of card data, money. Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019. After: DTPR-C02-T1, DTPR-C02-T2, DTPR-C02-T3.
  - Check storage, logs, screens and audit against the rules.
