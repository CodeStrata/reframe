# Tasks: Publish statements as PDF (ASGD-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ASGD-C08-T1 [api] Build the scheduled job. Requirements: ASGD-REQ-F-039. Rules: ASGD-BR-039.
  - ASGD-BR-039: A scheduled follow-on step that starts when statement creation completes. It renders the plain-text statement report to PDF and stores the result as the published statement document (legacy name AWS.M2.CARDDEMO.STATEMNT.PS.PDF), for example in document storage. Any text-to-PDF renderer works. The legacy job uses the TXT2PDF utility with BROWSE Y.
- [ ] ASGD-C08-T2 [test-generation] Write a test for every acceptance criterion. Requirements: ASGD-REQ-F-039. Criteria: ASGD-C08-AC-01. After: ASGD-C08-T1.
  - 1 acceptance criteria, each a test named by its ID.
- [ ] ASGD-C08-T3 [compliance] Review the handling of money, personal data. Requirements: ASGD-REQ-F-039. After: ASGD-C08-T1.
  - Check storage, logs, screens and audit against the rules.
