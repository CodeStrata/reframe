# Implementation plan: Re-sequence transactions by card number (ASGD-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ASGD-C01-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-002, ASGD-REQ-F-003_
  - _Rules: ASGD-BR-002_
- [ ] 2. ASGD-C01-T2 [api] Build the scheduled job
  - ASGD-BR-001: Produce a card-ordered extract of all transactions, sorted ascending by card number (16 characters) and then by transaction ID. Store it as a staging data set or a query or view that later steps read in that order. The new application does not have to copy the card number to the front of each record or use 350-byte fixed records. What matters is the sort order and that every transaction is included.
  - _Requirements: ASGD-REQ-F-001_
  - _Rules: ASGD-BR-001_
  - _After: ASGD-C01-T1_
- [ ] 3. ASGD-C01-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-001, ASGD-REQ-F-002, ASGD-REQ-F-003_
  - _Criteria: ASGD-C01-AC-01, ASGD-C01-AC-02_
  - _After: ASGD-C01-T1, ASGD-C01-T2_
- [ ] 4. ASGD-C01-T4 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-001, ASGD-REQ-F-002, ASGD-REQ-F-003_
  - _After: ASGD-C01-T1, ASGD-C01-T2_
