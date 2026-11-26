# Tasks: Load card cross-reference master and its account index (MDFI-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] MDFI-C04-T1 [api] Build the scheduled job. Requirements: MDFI-REQ-F-009, MDFI-REQ-F-010, MDFI-REQ-F-011. Rules: MDFI-BR-009, MDFI-BR-010, MDFI-BR-011.
  - MDFI-BR-009: The scheduled job drops or empties the cross-reference store and its by-account index, and it must succeed even if they do not exist yet. It then recreates the store with the 16-character card number as its unique primary key.
  - MDFI-BR-010: A bulk import of every card cross-reference record from the extract file into the new store, keyed on card number. The loaded row count should be reconciled against the input file.
  - MDFI-BR-011: After the load, create a non-unique secondary index on account ID over every cross-reference record. This supports the query 'all cards for account X', which can return many cards for one account. In a relational store, the index itself replaces the separate index and access-path objects of the old job.
- [ ] MDFI-C04-T2 [test-generation] Write a test for every acceptance criterion. Requirements: MDFI-REQ-F-009, MDFI-REQ-F-010, MDFI-REQ-F-011. Criteria: MDFI-C04-AC-01, MDFI-C04-AC-02, MDFI-C04-AC-03. After: MDFI-C04-T1.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] MDFI-C04-T3 [compliance] Review the handling of card data. Requirements: MDFI-REQ-F-009, MDFI-REQ-F-010, MDFI-REQ-F-011. After: MDFI-C04-T1.
  - Check storage, logs, screens and audit against the rules.
