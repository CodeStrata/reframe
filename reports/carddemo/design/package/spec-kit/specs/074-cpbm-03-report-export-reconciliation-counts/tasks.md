# Tasks: Report export reconciliation counts (CPBM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CPBM-C03-T1 [data] Model the data the capability reads and writes. Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009.
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
- [ ] CPBM-C03-T2 [business-rules] Implement the business rules. Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009. Rules: CPBM-BR-012, CPBM-BR-013. After: CPBM-C03-T1.
  - Keep each business rule exactly as specified.
- [ ] CPBM-C03-T3 [api] Build the service. Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009. Rules: CPBM-BR-012, CPBM-BR-013. After: CPBM-C03-T1, CPBM-C03-T2.
  - Expose the rules as the service the screens call.
- [ ] CPBM-C03-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009. Criteria: CPBM-C03-AC-01, CPBM-C03-AC-02. After: CPBM-C03-T1, CPBM-C03-T2, CPBM-C03-T3.
  - 2 acceptance criteria, each a test named by its ID.
- [ ] CPBM-C03-T5 [compliance] Review the handling of audit. Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009. After: CPBM-C03-T1, CPBM-C03-T2, CPBM-C03-T3.
  - Check storage, logs, screens and audit against the rules.
