# Tasks: List card cross-reference records (UP-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C03-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012.
  - File records: CVACT03Y (see data-contracts.md).
- [ ] UP-C03-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-012. Rules: UP-BR-014. After: UP-C03-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-014.
- [ ] UP-C03-T3 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-011. Rules: UP-BR-013. After: UP-C03-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C03-T4 [api] Build the scheduled job. Requirements: UP-REQ-F-010. Rules: UP-BR-012. After: UP-C03-T1, UP-C03-T2, UP-C03-T3.
  - UP-BR-012: A report job that reads the full card-to-account/customer link table through a read-only connection, from start to end, and writes every link to the job's report output. It changes nothing.
- [ ] UP-C03-T5 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012. Criteria: UP-C03-AC-01, UP-C03-AC-02, UP-C03-AC-03. After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] UP-C03-T6 [compliance] Review the handling of card data. Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012. After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4.
  - Check storage, logs, screens and audit against the rules.
