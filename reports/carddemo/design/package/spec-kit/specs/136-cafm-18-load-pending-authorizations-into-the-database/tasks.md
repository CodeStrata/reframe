# Tasks: Load pending authorizations into the database (CAFM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C18-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165.
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
- [ ] CAFM-C18-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-158, CAFM-REQ-F-159. Rules: CAFM-BR-175, CAFM-BR-176. After: CAFM-C18-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C18-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165. Rules: CAFM-BR-177, CAFM-BR-178, CAFM-BR-179, CAFM-BR-180. After: CAFM-C18-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C18-T4 [api] Build the scheduled job. Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157. Rules: CAFM-BR-172, CAFM-BR-173, CAFM-BR-174. After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3.
  - CAFM-BR-172: A batch load job that takes two input files, a summary file and a detail file, and inserts their records into the pending authorization store while online use continues (it must not need exclusive access to the store).
  - CAFM-BR-173: The load runs in two phases: read the whole summary file and insert every summary, and only then read the detail file. This order guarantees each detail's parent summary already exists when the detail is inserted.
  - CAFM-BR-174: Each detail is attached to its summary by account id: look up the summary by account id (a keyed lookup) and insert the detail under it, for example as a child row with a foreign key to the summary. A detail whose summary cannot be found is skipped, not loaded as an orphan.
- [ ] CAFM-C18-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165. Criteria: CAFM-C18-AC-01, CAFM-C18-AC-02, CAFM-C18-AC-03, CAFM-C18-AC-04, CAFM-C18-AC-05, CAFM-C18-AC-06, CAFM-C18-AC-07, CAFM-C18-AC-08, CAFM-C18-AC-09, CAFM-C18-AC-10, CAFM-C18-AC-11, CAFM-C18-AC-12. After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3, CAFM-C18-T4.
  - 12 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C18-T6 [compliance] Review the handling of card data. Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165. After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3, CAFM-C18-T4.
  - Check storage, logs, screens and audit against the rules.
