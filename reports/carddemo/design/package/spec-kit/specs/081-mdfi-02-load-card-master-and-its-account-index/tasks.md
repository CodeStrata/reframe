# Tasks: Load card master and its account index (MDFI-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] MDFI-C02-T1 [api] Build the scheduled job. Requirements: MDFI-REQ-F-003, MDFI-REQ-F-004, MDFI-REQ-F-005. Rules: MDFI-BR-003, MDFI-BR-004, MDFI-BR-005.
  - MDFI-BR-003: A scheduled bulk import that copies every record of the card extract file into the card store, keyed on card number. The shared access in the old job means the load must not lock out other readers of the source file. Row counts should be reconciled against the input.
  - MDFI-BR-004: Add a non-unique secondary index on the card's 11-character account ID column, which sits right after the card number in the legacy record (position 17). The database must keep this index up to date automatically on every insert, update and delete, and it must be queryable as 'cards for account X'.
  - MDFI-BR-005: Build or refresh the account-ID index only after the card load has finished, either as the last step of the load job or by creating the index after the bulk insert. That way, lookups by account show every loaded card.
- [ ] MDFI-C02-T2 [test-generation] Write a test for every acceptance criterion. Requirements: MDFI-REQ-F-003, MDFI-REQ-F-004, MDFI-REQ-F-005. Criteria: MDFI-C02-AC-01, MDFI-C02-AC-02, MDFI-C02-AC-03. After: MDFI-C02-T1.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] MDFI-C02-T3 [compliance] Review the handling of card data. Requirements: MDFI-REQ-F-003, MDFI-REQ-F-004, MDFI-REQ-F-005. After: MDFI-C02-T1.
  - Check storage, logs, screens and audit against the rules.
