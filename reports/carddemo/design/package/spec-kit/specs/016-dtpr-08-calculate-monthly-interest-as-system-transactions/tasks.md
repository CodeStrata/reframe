# Tasks: Calculate monthly interest as system transactions (DTPR-C08)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C08-T1 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-061. Rules: DTPR-BR-065.
  - Keep each business rule exactly as specified.
- [ ] DTPR-C08-T2 [api] Build the scheduled job. Requirements: DTPR-REQ-F-059, DTPR-REQ-F-060, DTPR-REQ-N-002. Rules: DTPR-BR-063, DTPR-BR-064. After: DTPR-C08-T1.
  - DTPR-BR-063: Run a scheduled monthly job that takes the processing date as a run parameter (the delivered job used '2022071800') rather than the system clock, so a run can be repeated or backdated. It reads category balances, the card cross-reference by card and by account, accounts and disclosure groups without locking out other readers.
  - DTPR-BR-064: Write the generated interest transactions as one new, versioned batch output (a new file version or a batch-tagged table load) in the 350-byte transaction layout. Publish it only if the job succeeds and discard it on failure, so the combine step never picks up a partial batch.
- [ ] DTPR-C08-T3 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-059, DTPR-REQ-F-060, DTPR-REQ-N-002, DTPR-REQ-F-061. Criteria: DTPR-C08-AC-01, DTPR-C08-AC-02, DTPR-C08-AC-03, DTPR-C08-AC-04. After: DTPR-C08-T1, DTPR-C08-T2.
  - 4 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C08-T4 [compliance] Review the handling of card data, money. Requirements: DTPR-REQ-F-059, DTPR-REQ-F-060, DTPR-REQ-N-002, DTPR-REQ-F-061. After: DTPR-C08-T1, DTPR-C08-T2.
  - Check storage, logs, screens and audit against the rules.
