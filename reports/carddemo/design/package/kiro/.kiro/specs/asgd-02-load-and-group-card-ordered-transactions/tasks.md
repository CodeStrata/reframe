# Implementation plan: Load and group card-ordered transactions (ASGD-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ASGD-C02-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001_
- [ ] 2. ASGD-C02-T2 [api] Build the scheduled job
  - ASGD-BR-003: Make card-ordered transactions available by the composite key (card number, transaction ID). An indexed table or a keyed staging store works. Load it only after every earlier step of the statement job has succeeded. Copy every record, and run the load as a gated step in the scheduled job.
  - ASGD-BR-004: Group the sorted transactions by card number: a control break opens a new group with a count of 1 when the card number changes and adds to the current group while it stays the same. In the new application this is a group-by on card number that keeps transaction-ID order within each card.
  - ASGD-BR-005: The legacy program holds at most 51 cards and 10 transactions per card in memory and does not check either limit. The new application should not have these fixed limits. It can stream or query per card, or size its collections dynamically. If a limit has to stay, exceeding it must be reported, not ignored. The business has to confirm whether to keep the legacy truncation.
  - _Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001_
  - _Rules: ASGD-BR-003, ASGD-BR-004, ASGD-BR-005_
  - _After: ASGD-C02-T1_
- [ ] 3. ASGD-C02-T3 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001_
  - _Criteria: ASGD-C02-AC-01, ASGD-C02-AC-02, ASGD-C02-AC-03, ASGD-C02-AC-04, ASGD-C02-AC-05_
  - _After: ASGD-C02-T1, ASGD-C02-T2_
- [ ] 4. ASGD-C02-T4 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001_
  - _After: ASGD-C02-T1, ASGD-C02-T2_
