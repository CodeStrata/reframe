# Implementation plan: Run the unload jobs and manage unload files (CAFM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C21-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
  - _Requirements: CAFM-REQ-N-004, CAFM-REQ-N-005, CAFM-REQ-N-006, CAFM-REQ-F-180, CAFM-REQ-F-181, CAFM-REQ-F-182, CAFM-REQ-F-183_
- [ ] 2. CAFM-C21-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-182, CAFM-REQ-F-183_
  - _Rules: CAFM-BR-199, CAFM-BR-200_
  - _After: CAFM-C21-T1_
- [ ] 3. CAFM-C21-T3 [api] Build the scheduled job
  - CAFM-BR-194: Needs a scheduled batch job running the summary-and-detail unload (DBUNLDGS in the legacy) with read-only, shared access to the pending authorization data and its index, so online use is not blocked while it runs.
  - CAFM-BR-195: This job writes to two existing output files, the summary file (AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM) and the detail file (AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM). No other process may write to them during the run, and they are kept whether the job succeeds or fails, so downstream steps must check the job status before using them.
  - CAFM-BR-196: Needs a second scheduled export job (PAUDBUNL in the legacy) that reads the pending authorization data and its index with shared, read-only access and writes summaries to the first output file and details to the second.
  - CAFM-BR-197: The job creates a new summary export file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) of fixed 100-byte records. It is published or registered only when the job succeeds and is deleted when the job fails, for example by writing to a temporary location and renaming it on success.
  - CAFM-BR-198: The job creates a new detail export file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) of fixed 206-byte records. It is published only when the job succeeds and deleted when the job fails, the same way as the summary file.
  - _Requirements: CAFM-REQ-N-004, CAFM-REQ-N-005, CAFM-REQ-N-006, CAFM-REQ-F-180, CAFM-REQ-F-181_
  - _Rules: CAFM-BR-194, CAFM-BR-195, CAFM-BR-196, CAFM-BR-197, CAFM-BR-198_
  - _After: CAFM-C21-T1, CAFM-C21-T2_
- [ ] 4. CAFM-C21-T4 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-N-004, CAFM-REQ-N-005, CAFM-REQ-N-006, CAFM-REQ-F-180, CAFM-REQ-F-181, CAFM-REQ-F-182, CAFM-REQ-F-183_
  - _Criteria: CAFM-C21-AC-01, CAFM-C21-AC-02, CAFM-C21-AC-03, CAFM-C21-AC-04, CAFM-C21-AC-05, CAFM-C21-AC-06, CAFM-C21-AC-07, CAFM-C21-AC-08, CAFM-C21-AC-09, CAFM-C21-AC-10_
  - _After: CAFM-C21-T1, CAFM-C21-T2, CAFM-C21-T3_
- [ ] 5. CAFM-C21-T5 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-N-004, CAFM-REQ-N-005, CAFM-REQ-N-006, CAFM-REQ-F-180, CAFM-REQ-F-181, CAFM-REQ-F-182, CAFM-REQ-F-183_
  - _After: CAFM-C21-T1, CAFM-C21-T2, CAFM-C21-T3_
