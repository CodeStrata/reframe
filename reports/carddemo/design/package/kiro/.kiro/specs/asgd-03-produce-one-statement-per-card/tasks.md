# Implementation plan: Produce one statement per card (ASGD-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ASGD-C03-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011_
- [ ] 2. ASGD-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ASGD-REQ-F-008_
  - _Rules: ASGD-BR-009_
  - _After: ASGD-C03-T1_
- [ ] 3. ASGD-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-010, ASGD-REQ-F-011_
  - _Rules: ASGD-BR-011, ASGD-BR-012_
  - _After: ASGD-C03-T1_
- [ ] 4. ASGD-C03-T4 [api] Build the scheduled job
  - ASGD-BR-006: A scheduled statement job that runs only after the earlier steps succeed. It reads card-ordered transactions, the card cross-reference, accounts and customers, and writes two new outputs per run: a plain-text statement report and an HTML statement report. The 80- and 100-character line widths only matter if the text output must match the legacy layout exactly.
  - ASGD-BR-007: Fixed order for the run: open both outputs, load the card transactions, open the cross-reference, customer and account sources, build every statement, then release all inputs and close the outputs. In the new application, make the transactions available before statement building starts, and finalise the outputs only after every statement is built.
  - ASGD-BR-008: Every data source has the lifecycle open, read one or more times, close. The new application can do this with scoped resources such as connections or readers that are always released, including on failure.
  - ASGD-BR-010: For each cross-reference record, look up the customer by its customer ID and the account by its account ID, then write the header and details, the transactions, the total and the footer. Both lookups use the primary key of their record.
  - _Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-009_
  - _Rules: ASGD-BR-006, ASGD-BR-007, ASGD-BR-008, ASGD-BR-010_
  - _After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3_
- [ ] 5. ASGD-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011_
  - _Criteria: ASGD-C03-AC-01, ASGD-C03-AC-02, ASGD-C03-AC-03, ASGD-C03-AC-04, ASGD-C03-AC-05, ASGD-C03-AC-06, ASGD-C03-AC-07, ASGD-C03-AC-08, ASGD-C03-AC-09_
  - _After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3, ASGD-C03-T4_
- [ ] 6. ASGD-C03-T6 [compliance] Review the handling of card data, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011_
  - _After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3, ASGD-C03-T4_
