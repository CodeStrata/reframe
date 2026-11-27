# Tasks: Post daily transactions and record rejects (DTPR-C07)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C07-T1 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-058, DTPR-REQ-N-001. Rules: DTPR-BR-062.
  - Keep each business rule exactly as specified.
- [ ] DTPR-C07-T2 [api] Build the scheduled job. Requirements: DTPR-REQ-F-057. Rules: DTPR-BR-061. After: DTPR-C07-T1.
  - DTPR-BR-061: Run a scheduled daily job that reads the day's transaction feed and, for each transaction, uses the card cross-reference and posts to the transaction master, account and category balance tables. The job needs read access to the feed and cross-reference, and write access to transactions, accounts and category balances. Schedule it after the daily feed arrives and before any jobs that read the posted data.
- [ ] DTPR-C07-T3 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-057, DTPR-REQ-F-058, DTPR-REQ-N-001. Criteria: DTPR-C07-AC-01, DTPR-C07-AC-02, DTPR-C07-AC-03. After: DTPR-C07-T1, DTPR-C07-T2.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C07-T4 [compliance] Review the handling of card data, money. Requirements: DTPR-REQ-F-057, DTPR-REQ-F-058, DTPR-REQ-N-001. After: DTPR-C07-T1, DTPR-C07-T2.
  - Check storage, logs, screens and audit against the rules.
