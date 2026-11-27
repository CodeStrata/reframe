# Implementation plan: Publish statements as PDF (ASGD-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ASGD-C08-T1 [api] Build the scheduled job
  - ASGD-BR-039: A scheduled follow-on step that starts when statement creation completes. It renders the plain-text statement report to PDF and stores the result as the published statement document (legacy name AWS.M2.CARDDEMO.STATEMNT.PS.PDF), for example in document storage. Any text-to-PDF renderer works. The legacy job uses the TXT2PDF utility with BROWSE Y.
  - _Requirements: ASGD-REQ-F-039_
  - _Rules: ASGD-BR-039_
- [ ] 2. ASGD-C08-T2 [test-generation] Write a test for every acceptance criterion
  - 1 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-039_
  - _Criteria: ASGD-C08-AC-01_
  - _After: ASGD-C08-T1_
- [ ] 3. ASGD-C08-T3 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-039_
  - _After: ASGD-C08-T1_
