# Tasks: Log unknown record types during import (CPBM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CPBM-C06-T1 [data] Model the data the capability reads and writes. Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023.
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
- [ ] CPBM-C06-T2 [business-rules] Implement error handling and messages. Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023. Rules: CPBM-BR-026, CPBM-BR-027, CPBM-BR-028. After: CPBM-C06-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CPBM-C06-T3 [api] Build the scheduled job. Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023. Rules: CPBM-BR-026, CPBM-BR-027, CPBM-BR-028. After: CPBM-C06-T1, CPBM-C06-T2.
  - Expose the rules as the service the screens call.
- [ ] CPBM-C06-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023. Criteria: CPBM-C06-AC-01, CPBM-C06-AC-02, CPBM-C06-AC-03, CPBM-C06-AC-04. After: CPBM-C06-T1, CPBM-C06-T2, CPBM-C06-T3.
  - 4 acceptance criteria, each a test named by its ID.
- [ ] CPBM-C06-T5 [compliance] Review the handling of audit. Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023. After: CPBM-C06-T1, CPBM-C06-T2, CPBM-C06-T3.
  - Check storage, logs, screens and audit against the rules.
