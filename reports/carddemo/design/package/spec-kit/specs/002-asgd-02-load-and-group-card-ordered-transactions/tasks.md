# Tasks: Load and group card-ordered transactions (ASGD-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ASGD-C02-T1 [data] Model the data the capability reads and writes. Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001.
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
- [ ] ASGD-C02-T2 [api] Build the scheduled job. Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001. Rules: ASGD-BR-003, ASGD-BR-004, ASGD-BR-005. After: ASGD-C02-T1.
  - ASGD-BR-003: Make card-ordered transactions available by the composite key (card number, transaction ID). An indexed table or a keyed staging store works. Load it only after every earlier step of the statement job has succeeded. Copy every record, and run the load as a gated step in the scheduled job.
  - ASGD-BR-004: Group the sorted transactions by card number: a control break opens a new group with a count of 1 when the card number changes and adds to the current group while it stays the same. In the new application this is a group-by on card number that keeps transaction-ID order within each card.
  - ASGD-BR-005: The legacy program holds at most 51 cards and 10 transactions per card in memory and does not check either limit. The new application should not have these fixed limits. It can stream or query per card, or size its collections dynamically. If a limit has to stay, exceeding it must be reported, not ignored. The business has to confirm whether to keep the legacy truncation.
- [ ] ASGD-C02-T3 [test-generation] Write a test for every acceptance criterion. Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001. Criteria: ASGD-C02-AC-01, ASGD-C02-AC-02, ASGD-C02-AC-03, ASGD-C02-AC-04, ASGD-C02-AC-05. After: ASGD-C02-T1, ASGD-C02-T2.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] ASGD-C02-T4 [compliance] Review the handling of card data, money. Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001. After: ASGD-C02-T1, ASGD-C02-T2.
  - Check storage, logs, screens and audit against the rules.
