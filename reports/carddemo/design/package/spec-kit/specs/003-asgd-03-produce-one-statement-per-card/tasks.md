# Tasks: Produce one statement per card (ASGD-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ASGD-C03-T1 [data] Model the data the capability reads and writes. Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011.
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
- [ ] ASGD-C03-T2 [business-rules] Implement the business rules. Requirements: ASGD-REQ-F-008. Rules: ASGD-BR-009. After: ASGD-C03-T1.
  - Keep each business rule exactly as specified.
- [ ] ASGD-C03-T3 [business-rules] Implement error handling and messages. Requirements: ASGD-REQ-F-010, ASGD-REQ-F-011. Rules: ASGD-BR-011, ASGD-BR-012. After: ASGD-C03-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ASGD-C03-T4 [api] Build the scheduled job. Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-009. Rules: ASGD-BR-006, ASGD-BR-007, ASGD-BR-008, ASGD-BR-010. After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3.
  - ASGD-BR-006: A scheduled statement job that runs only after the earlier steps succeed. It reads card-ordered transactions, the card cross-reference, accounts and customers, and writes two new outputs per run: a plain-text statement report and an HTML statement report. The 80- and 100-character line widths only matter if the text output must match the legacy layout exactly.
  - ASGD-BR-007: Fixed order for the run: open both outputs, load the card transactions, open the cross-reference, customer and account sources, build every statement, then release all inputs and close the outputs. In the new application, make the transactions available before statement building starts, and finalise the outputs only after every statement is built.
  - ASGD-BR-008: Every data source has the lifecycle open, read one or more times, close. The new application can do this with scoped resources such as connections or readers that are always released, including on failure.
  - ASGD-BR-010: For each cross-reference record, look up the customer by its customer ID and the account by its account ID, then write the header and details, the transactions, the total and the footer. Both lookups use the primary key of their record.
- [ ] ASGD-C03-T5 [test-generation] Write a test for every acceptance criterion. Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011. Criteria: ASGD-C03-AC-01, ASGD-C03-AC-02, ASGD-C03-AC-03, ASGD-C03-AC-04, ASGD-C03-AC-05, ASGD-C03-AC-06, ASGD-C03-AC-07, ASGD-C03-AC-08, ASGD-C03-AC-09. After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3, ASGD-C03-T4.
  - 9 acceptance criteria, each a test named by its ID.
- [ ] ASGD-C03-T6 [compliance] Review the handling of card data, money, personal data. Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011. After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3, ASGD-C03-T4.
  - Check storage, logs, screens and audit against the rules.
