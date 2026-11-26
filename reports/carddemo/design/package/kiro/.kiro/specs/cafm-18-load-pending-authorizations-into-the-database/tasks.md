# Implementation plan: Load pending authorizations into the database (CAFM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C18-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
  - _Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165_
- [ ] 2. CAFM-C18-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-158, CAFM-REQ-F-159_
  - _Rules: CAFM-BR-175, CAFM-BR-176_
  - _After: CAFM-C18-T1_
- [ ] 3. CAFM-C18-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165_
  - _Rules: CAFM-BR-177, CAFM-BR-178, CAFM-BR-179, CAFM-BR-180_
  - _After: CAFM-C18-T1_
- [ ] 4. CAFM-C18-T4 [api] Build the scheduled job
  - CAFM-BR-172: Needs a scheduled load job that takes two input files, the summary file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) and the detail file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO), and inserts their contents into the live pending authorization store while it stays available to other users.
  - CAFM-BR-173: The load runs in two passes: the whole summary file to its end, then the whole detail file to its end. Details are never processed before all summaries are in, so each detail can find its parent.
  - CAFM-BR-174: Same two-pass order: details are attached to their summary by account ID only after every summary has been loaded. In a relational model this is the parent table loaded before the child table, with the account ID as the foreign key.
  - _Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157_
  - _Rules: CAFM-BR-172, CAFM-BR-173, CAFM-BR-174_
  - _After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3_
- [ ] 5. CAFM-C18-T5 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165_
  - _Criteria: CAFM-C18-AC-01, CAFM-C18-AC-02, CAFM-C18-AC-03, CAFM-C18-AC-04, CAFM-C18-AC-05, CAFM-C18-AC-06, CAFM-C18-AC-07, CAFM-C18-AC-08, CAFM-C18-AC-09, CAFM-C18-AC-10, CAFM-C18-AC-11, CAFM-C18-AC-12_
  - _After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3, CAFM-C18-T4_
- [ ] 6. CAFM-C18-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165_
  - _After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3, CAFM-C18-T4_
