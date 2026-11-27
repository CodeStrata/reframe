# Tasks: Report import run statistics (CPBM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CPBM-C07-T1 [data] Model the data the capability reads and writes. Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025.
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
- [ ] CPBM-C07-T2 [business-rules] Implement the business rules. Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025. Rules: CPBM-BR-029, CPBM-BR-030, CPBM-BR-031. After: CPBM-C07-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CPBM-BR-030, CPBM-BR-031.
- [ ] CPBM-C07-T3 [api] Build the scheduled job. Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025. Rules: CPBM-BR-029, CPBM-BR-030, CPBM-BR-031. After: CPBM-C07-T1, CPBM-C07-T2.
  - Expose the rules as the service the screens call.
- [ ] CPBM-C07-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025. Criteria: CPBM-C07-AC-01, CPBM-C07-AC-02, CPBM-C07-AC-03, CPBM-C07-AC-04, CPBM-C07-AC-05. After: CPBM-C07-T1, CPBM-C07-T2, CPBM-C07-T3.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] CPBM-C07-T5 [compliance] Review the handling of audit. Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025. After: CPBM-C07-T1, CPBM-C07-T2, CPBM-C07-T3.
  - Check storage, logs, screens and audit against the rules.
