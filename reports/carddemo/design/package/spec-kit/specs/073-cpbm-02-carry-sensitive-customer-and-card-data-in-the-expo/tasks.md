# Tasks: Carry sensitive customer and card data in the export (CPBM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CPBM-C02-T1 [data] Model the data the capability reads and writes. Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003.
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
- [ ] CPBM-C02-T2 [business-rules] Implement the business rules. Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003. Rules: CPBM-BR-009, CPBM-BR-010, CPBM-BR-011. After: CPBM-C02-T1.
  - Keep each business rule exactly as specified.
- [ ] CPBM-C02-T3 [api] Build the scheduled job. Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003. Rules: CPBM-BR-009, CPBM-BR-010, CPBM-BR-011. After: CPBM-C02-T1, CPBM-C02-T2.
  - Expose the rules as the service the screens call.
- [ ] CPBM-C02-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003. Criteria: CPBM-C02-AC-01, CPBM-C02-AC-02, CPBM-C02-AC-03, CPBM-C02-AC-04. After: CPBM-C02-T1, CPBM-C02-T2, CPBM-C02-T3.
  - 4 acceptance criteria, each a test named by its ID.
- [ ] CPBM-C02-T5 [compliance] Review the handling of card data, personal data, security. Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003. After: CPBM-C02-T1, CPBM-C02-T2, CPBM-C02-T3.
  - Check storage, logs, screens and audit against the rules.
