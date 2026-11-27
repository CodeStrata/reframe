# Tasks: Load pending authorization summaries (CAFM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C19-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169.
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
- [ ] CAFM-C19-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167. Rules: CAFM-BR-181. After: CAFM-C19-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C19-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-168, CAFM-REQ-F-169. Rules: CAFM-BR-182, CAFM-BR-183. After: CAFM-C19-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C19-T4 [api] Build the scheduled job. Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169. Rules: CAFM-BR-181, CAFM-BR-182, CAFM-BR-183. After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3.
  - Expose the rules as the service the screens call.
- [ ] CAFM-C19-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169. Criteria: CAFM-C19-AC-01, CAFM-C19-AC-02, CAFM-C19-AC-03. After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3, CAFM-C19-T4.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C19-T6 [compliance] Review the handling of card data. Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169. After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3, CAFM-C19-T4.
  - Check storage, logs, screens and audit against the rules.
