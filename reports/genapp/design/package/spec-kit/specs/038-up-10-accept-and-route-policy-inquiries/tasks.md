# Tasks: Accept and route policy inquiries (UP-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C10-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-055, UP-REQ-F-056.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] UP-C10-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-055, UP-REQ-F-056. Rules: UP-BR-077, UP-BR-078. After: UP-C10-T1.
  - Keep each business rule exactly as specified.
- [ ] UP-C10-T3 [api] Build the scheduled job. Requirements: UP-REQ-F-055, UP-REQ-F-056. Rules: UP-BR-077, UP-BR-078. After: UP-C10-T1, UP-C10-T2.
  - Expose the rules as the service the screens call.
- [ ] UP-C10-T4 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-055, UP-REQ-F-056. Criteria: UP-C10-AC-01, UP-C10-AC-02, UP-C10-AC-03. After: UP-C10-T1, UP-C10-T2, UP-C10-T3.
  - 3 acceptance criteria, each a test named by its ID.
