# Implementation plan: Read-only statement data access (ASGD-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ASGD-C07-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-035_
  - _Rules: ASGD-BR-035_
- [ ] 2. ASGD-C07-T2 [api] Build the scheduled job
  - ASGD-BR-033: Look up a customer directly by primary key (customer ID) and return the record, or a 'not found' result that the caller can tell apart from other failures. The legacy program passes the key length in from the caller. The new application should use a typed customer ID instead.
  - ASGD-BR-034: Look up an account directly by its 11-digit account ID (primary key) and return the record or a clear 'not found' result. Validate the ID as 11 digits rather than relying on a key length the caller supplies.
  - ASGD-BR-008: Every data source the statement job uses follows the lifecycle open, read one or more times, close. Use scoped resources that are always released, including when the run fails.
  - ASGD-BR-036: Transactions must be readable in order of (card number, transaction ID), and the card cross-reference in card-number order. These are ordered sequential reads, such as streams or cursors over a sorted query, with a clear end-of-data signal.
  - ASGD-BR-037: Customers and accounts are needed only for keyed point lookups. No scans or ordered reads are needed for them.
  - ASGD-BR-038: The statement job's data access must be read-only. Use read-only connections or a read replica with credentials that cannot write. Expose no write or update operations, even though the legacy routine defines 'W' and 'Z' operation codes.
  - _Requirements: ASGD-REQ-F-033, ASGD-REQ-F-034, ASGD-REQ-F-036, ASGD-REQ-F-037, ASGD-REQ-F-038, ASGD-REQ-N-002_
  - _Rules: ASGD-BR-008, ASGD-BR-033, ASGD-BR-034, ASGD-BR-036, ASGD-BR-037, ASGD-BR-038_
  - _After: ASGD-C07-T1_
- [ ] 3. ASGD-C07-T3 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-033, ASGD-REQ-F-034, ASGD-REQ-F-035, ASGD-REQ-F-036, ASGD-REQ-F-037, ASGD-REQ-F-038, ASGD-REQ-N-002_
  - _Criteria: ASGD-C07-AC-01, ASGD-C07-AC-02, ASGD-C07-AC-03, ASGD-C07-AC-04, ASGD-C07-AC-05, ASGD-C07-AC-06, ASGD-C07-AC-07, ASGD-C07-AC-08_
  - _After: ASGD-C07-T1, ASGD-C07-T2_
- [ ] 4. ASGD-C07-T4 [compliance] Review the handling of card data, money, personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-033, ASGD-REQ-F-034, ASGD-REQ-F-035, ASGD-REQ-F-036, ASGD-REQ-F-037, ASGD-REQ-F-038, ASGD-REQ-N-002_
  - _After: ASGD-C07-T1, ASGD-C07-T2_
