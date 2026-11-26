# Tasks: Stop the export on any file error (CPBM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CPBM-C04-T1 [data] Model the data the capability reads and writes. Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012.
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
- [ ] CPBM-C04-T2 [business-rules] Implement error handling and messages. Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012. Rules: CPBM-BR-014, CPBM-BR-015, CPBM-BR-016. After: CPBM-C04-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CPBM-C04-T3 [api] Build the scheduled job. Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012. Rules: CPBM-BR-014, CPBM-BR-015, CPBM-BR-016. After: CPBM-C04-T1, CPBM-C04-T2.
  - Expose the rules as the service the screens call.
- [ ] CPBM-C04-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012. Criteria: CPBM-C04-AC-01, CPBM-C04-AC-02, CPBM-C04-AC-03, CPBM-C04-AC-04, CPBM-C04-AC-05, CPBM-C04-AC-06. After: CPBM-C04-T1, CPBM-C04-T2, CPBM-C04-T3.
  - 6 acceptance criteria, each a test named by its ID.
- [ ] CPBM-C04-T5 [compliance] Review the handling of audit. Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012. After: CPBM-C04-T1, CPBM-C04-T2, CPBM-C04-T3.
  - Check storage, logs, screens and audit against the rules.
