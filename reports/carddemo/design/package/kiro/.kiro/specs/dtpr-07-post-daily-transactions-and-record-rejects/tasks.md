# Implementation plan: Post daily transactions and record rejects (DTPR-C07)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C07-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-058, DTPR-REQ-N-001_
  - _Rules: DTPR-BR-062_
- [ ] 2. DTPR-C07-T2 [api] Build the scheduled job
  - DTPR-BR-061: Run a scheduled daily job that reads the day's transaction feed and, for each transaction, uses the card cross-reference and posts to the transaction master, account and category balance tables. The job needs read access to the feed and cross-reference, and write access to transactions, accounts and category balances. Schedule it after the daily feed arrives and before any jobs that read the posted data.
  - _Requirements: DTPR-REQ-F-057_
  - _Rules: DTPR-BR-061_
  - _After: DTPR-C07-T1_
- [ ] 3. DTPR-C07-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-057, DTPR-REQ-F-058, DTPR-REQ-N-001_
  - _Criteria: DTPR-C07-AC-01, DTPR-C07-AC-02, DTPR-C07-AC-03_
  - _After: DTPR-C07-T1, DTPR-C07-T2_
- [ ] 4. DTPR-C07-T4 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-057, DTPR-REQ-F-058, DTPR-REQ-N-001_
  - _After: DTPR-C07-T1, DTPR-C07-T2_
