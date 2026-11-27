# Tasks

Build final capabilities first. Each task names its role and the IDs it implements.

## ASGD-C01 Re-sequence transactions by card number (draft)

- [ ] ASGD-C01-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-002, ASGD-REQ-F-003_
  - _Rules: ASGD-BR-002_
- [ ] ASGD-C01-T2 [api] Build the scheduled job
  - ASGD-BR-001: Produce a card-ordered extract of all transactions, sorted ascending by card number (16 characters) and then by transaction ID. Store it as a staging data set or a query or view that later steps read in that order. The new application does not have to copy the card number to the front of each record or use 350-byte fixed records. What matters is the sort order and that every transaction is included.
  - _Requirements: ASGD-REQ-F-001_
  - _Rules: ASGD-BR-001_
  - _After: ASGD-C01-T1_
- [ ] ASGD-C01-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-001, ASGD-REQ-F-002, ASGD-REQ-F-003_
  - _Criteria: ASGD-C01-AC-01, ASGD-C01-AC-02_
  - _After: ASGD-C01-T1, ASGD-C01-T2_
- [ ] ASGD-C01-T4 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-001, ASGD-REQ-F-002, ASGD-REQ-F-003_
  - _After: ASGD-C01-T1, ASGD-C01-T2_

## ASGD-C02 Load and group card-ordered transactions (draft)

- [ ] ASGD-C02-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001_
- [ ] ASGD-C02-T2 [api] Build the scheduled job
  - ASGD-BR-003: Make card-ordered transactions available by the composite key (card number, transaction ID). An indexed table or a keyed staging store works. Load it only after every earlier step of the statement job has succeeded. Copy every record, and run the load as a gated step in the scheduled job.
  - ASGD-BR-004: Group the sorted transactions by card number: a control break opens a new group with a count of 1 when the card number changes and adds to the current group while it stays the same. In the new application this is a group-by on card number that keeps transaction-ID order within each card.
  - ASGD-BR-005: The legacy program holds at most 51 cards and 10 transactions per card in memory and does not check either limit. The new application should not have these fixed limits. It can stream or query per card, or size its collections dynamically. If a limit has to stay, exceeding it must be reported, not ignored. The business has to confirm whether to keep the legacy truncation.
  - _Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001_
  - _Rules: ASGD-BR-003, ASGD-BR-004, ASGD-BR-005_
  - _After: ASGD-C02-T1_
- [ ] ASGD-C02-T3 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001_
  - _Criteria: ASGD-C02-AC-01, ASGD-C02-AC-02, ASGD-C02-AC-03, ASGD-C02-AC-04, ASGD-C02-AC-05_
  - _After: ASGD-C02-T1, ASGD-C02-T2_
- [ ] ASGD-C02-T4 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-004, ASGD-REQ-F-005, ASGD-REQ-N-001_
  - _After: ASGD-C02-T1, ASGD-C02-T2_

## ASGD-C03 Produce one statement per card (draft)

- [ ] ASGD-C03-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011_
- [ ] ASGD-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ASGD-REQ-F-008_
  - _Rules: ASGD-BR-009_
  - _After: ASGD-C03-T1_
- [ ] ASGD-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-010, ASGD-REQ-F-011_
  - _Rules: ASGD-BR-011, ASGD-BR-012_
  - _After: ASGD-C03-T1_
- [ ] ASGD-C03-T4 [api] Build the scheduled job
  - ASGD-BR-006: A scheduled statement job that runs only after the earlier steps succeed. It reads card-ordered transactions, the card cross-reference, accounts and customers, and writes two new outputs per run: a plain-text statement report and an HTML statement report. The 80- and 100-character line widths only matter if the text output must match the legacy layout exactly.
  - ASGD-BR-007: Fixed order for the run: open both outputs, load the card transactions, open the cross-reference, customer and account sources, build every statement, then release all inputs and close the outputs. In the new application, make the transactions available before statement building starts, and finalise the outputs only after every statement is built.
  - ASGD-BR-008: Every data source has the lifecycle open, read one or more times, close. The new application can do this with scoped resources such as connections or readers that are always released, including on failure.
  - ASGD-BR-010: For each cross-reference record, look up the customer by its customer ID and the account by its account ID, then write the header and details, the transactions, the total and the footer. Both lookups use the primary key of their record.
  - _Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-009_
  - _Rules: ASGD-BR-006, ASGD-BR-007, ASGD-BR-008, ASGD-BR-010_
  - _After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3_
- [ ] ASGD-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011_
  - _Criteria: ASGD-C03-AC-01, ASGD-C03-AC-02, ASGD-C03-AC-03, ASGD-C03-AC-04, ASGD-C03-AC-05, ASGD-C03-AC-06, ASGD-C03-AC-07, ASGD-C03-AC-08, ASGD-C03-AC-09_
  - _After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3, ASGD-C03-T4_
- [ ] ASGD-C03-T6 [compliance] Review the handling of card data, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-006, ASGD-REQ-F-007, ASGD-REQ-F-008, ASGD-REQ-F-009, ASGD-REQ-F-010, ASGD-REQ-F-011_
  - _After: ASGD-C03-T1, ASGD-C03-T2, ASGD-C03-T3, ASGD-C03-T4_

## ASGD-C04 Show statement header and holder details (draft)

- [ ] ASGD-C04-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
- [ ] ASGD-C04-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
  - _Rules: ASGD-BR-013, ASGD-BR-014, ASGD-BR-015, ASGD-BR-016, ASGD-BR-017, ASGD-BR-018, ASGD-BR-019_
  - _After: ASGD-C04-T1_
- [ ] ASGD-C04-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
  - _Rules: ASGD-BR-013, ASGD-BR-014, ASGD-BR-015, ASGD-BR-016, ASGD-BR-017, ASGD-BR-018, ASGD-BR-019_
  - _After: ASGD-C04-T1, ASGD-C04-T2_
- [ ] ASGD-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
  - _Criteria: ASGD-C04-AC-01, ASGD-C04-AC-02, ASGD-C04-AC-03, ASGD-C04-AC-04, ASGD-C04-AC-05, ASGD-C04-AC-06_
  - _After: ASGD-C04-T1, ASGD-C04-T2, ASGD-C04-T3_
- [ ] ASGD-C04-T5 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-012, ASGD-REQ-F-013, ASGD-REQ-F-014, ASGD-REQ-F-015, ASGD-REQ-F-016, ASGD-REQ-F-017, ASGD-REQ-F-018_
  - _After: ASGD-C04-T1, ASGD-C04-T2, ASGD-C04-T3_

## ASGD-C05 List card transactions and total (draft)

- [ ] ASGD-C05-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-019, ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-023, ASGD-REQ-F-024, ASGD-REQ-F-025_
- [ ] ASGD-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ASGD-REQ-F-019, ASGD-REQ-F-023_
  - _Rules: ASGD-BR-020, ASGD-BR-021, ASGD-BR-024_
  - _After: ASGD-C05-T1_
- [ ] ASGD-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-024, ASGD-REQ-F-025_
  - _Rules: ASGD-BR-021, ASGD-BR-022, ASGD-BR-023, ASGD-BR-025, ASGD-BR-026_
  - _After: ASGD-C05-T1_
- [ ] ASGD-C05-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: ASGD-REQ-F-019, ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-023, ASGD-REQ-F-024, ASGD-REQ-F-025_
  - _Rules: ASGD-BR-020, ASGD-BR-021, ASGD-BR-022, ASGD-BR-023, ASGD-BR-024, ASGD-BR-025, ASGD-BR-026_
  - _After: ASGD-C05-T1, ASGD-C05-T2, ASGD-C05-T3_
- [ ] ASGD-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-019, ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-023, ASGD-REQ-F-024, ASGD-REQ-F-025_
  - _Criteria: ASGD-C05-AC-01, ASGD-C05-AC-02, ASGD-C05-AC-03, ASGD-C05-AC-04, ASGD-C05-AC-05, ASGD-C05-AC-06, ASGD-C05-AC-07, ASGD-C05-AC-08, ASGD-C05-AC-09_
  - _After: ASGD-C05-T1, ASGD-C05-T2, ASGD-C05-T3, ASGD-C05-T4_
- [ ] ASGD-C05-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-019, ASGD-REQ-F-020, ASGD-REQ-F-021, ASGD-REQ-F-022, ASGD-REQ-F-023, ASGD-REQ-F-024, ASGD-REQ-F-025_
  - _After: ASGD-C05-T1, ASGD-C05-T2, ASGD-C05-T3, ASGD-C05-T4_

## ASGD-C06 Stop the statement run on file errors (draft)

- [ ] ASGD-C06-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COSTM01, CUSTREC, CVACT01Y, CVACT03Y.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
- [ ] ASGD-C06-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
  - _Rules: ASGD-BR-012, ASGD-BR-027, ASGD-BR-028, ASGD-BR-029, ASGD-BR-030, ASGD-BR-031, ASGD-BR-032_
  - _After: ASGD-C06-T1_
- [ ] ASGD-C06-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
  - _Rules: ASGD-BR-012, ASGD-BR-027, ASGD-BR-028, ASGD-BR-029, ASGD-BR-030, ASGD-BR-031, ASGD-BR-032_
  - _After: ASGD-C06-T1, ASGD-C06-T2_
- [ ] ASGD-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
  - _Criteria: ASGD-C06-AC-01, ASGD-C06-AC-02, ASGD-C06-AC-03, ASGD-C06-AC-04, ASGD-C06-AC-05, ASGD-C06-AC-06, ASGD-C06-AC-07_
  - _After: ASGD-C06-T1, ASGD-C06-T2, ASGD-C06-T3_
- [ ] ASGD-C06-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-026, ASGD-REQ-F-027, ASGD-REQ-F-028, ASGD-REQ-F-029, ASGD-REQ-F-030, ASGD-REQ-F-031, ASGD-REQ-F-032_
  - _After: ASGD-C06-T1, ASGD-C06-T2, ASGD-C06-T3_

## ASGD-C07 Read-only statement data access (draft)

- [ ] ASGD-C07-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ASGD-REQ-F-035_
  - _Rules: ASGD-BR-035_
- [ ] ASGD-C07-T2 [api] Build the scheduled job
  - ASGD-BR-033: Look up a customer directly by primary key (customer ID) and return the record, or a 'not found' result that the caller can tell apart from other failures. The legacy program passes the key length in from the caller. The new application should use a typed customer ID instead.
  - ASGD-BR-034: Look up an account directly by its 11-digit account ID (primary key) and return the record or a clear 'not found' result. Validate the ID as 11 digits rather than relying on a key length the caller supplies.
  - ASGD-BR-008: Every data source the statement job uses follows the lifecycle open, read one or more times, close. Use scoped resources that are always released, including when the run fails.
  - ASGD-BR-036: Transactions must be readable in order of (card number, transaction ID), and the card cross-reference in card-number order. These are ordered sequential reads, such as streams or cursors over a sorted query, with a clear end-of-data signal.
  - ASGD-BR-037: Customers and accounts are needed only for keyed point lookups. No scans or ordered reads are needed for them.
  - ASGD-BR-038: The statement job's data access must be read-only. Use read-only connections or a read replica with credentials that cannot write. Expose no write or update operations, even though the legacy routine defines 'W' and 'Z' operation codes.
  - _Requirements: ASGD-REQ-F-033, ASGD-REQ-F-034, ASGD-REQ-F-036, ASGD-REQ-F-037, ASGD-REQ-F-038, ASGD-REQ-N-002_
  - _Rules: ASGD-BR-008, ASGD-BR-033, ASGD-BR-034, ASGD-BR-036, ASGD-BR-037, ASGD-BR-038_
  - _After: ASGD-C07-T1_
- [ ] ASGD-C07-T3 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-033, ASGD-REQ-F-034, ASGD-REQ-F-035, ASGD-REQ-F-036, ASGD-REQ-F-037, ASGD-REQ-F-038, ASGD-REQ-N-002_
  - _Criteria: ASGD-C07-AC-01, ASGD-C07-AC-02, ASGD-C07-AC-03, ASGD-C07-AC-04, ASGD-C07-AC-05, ASGD-C07-AC-06, ASGD-C07-AC-07, ASGD-C07-AC-08_
  - _After: ASGD-C07-T1, ASGD-C07-T2_
- [ ] ASGD-C07-T4 [compliance] Review the handling of card data, money, personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-033, ASGD-REQ-F-034, ASGD-REQ-F-035, ASGD-REQ-F-036, ASGD-REQ-F-037, ASGD-REQ-F-038, ASGD-REQ-N-002_
  - _After: ASGD-C07-T1, ASGD-C07-T2_

## ASGD-C08 Publish statements as PDF (draft)

- [ ] ASGD-C08-T1 [api] Build the scheduled job
  - ASGD-BR-039: A scheduled follow-on step that starts when statement creation completes. It renders the plain-text statement report to PDF and stores the result as the published statement document (legacy name AWS.M2.CARDDEMO.STATEMNT.PS.PDF), for example in document storage. Any text-to-PDF renderer works. The legacy job uses the TXT2PDF utility with BROWSE Y.
  - _Requirements: ASGD-REQ-F-039_
  - _Rules: ASGD-BR-039_
- [ ] ASGD-C08-T2 [test-generation] Write a test for every acceptance criterion
  - 1 acceptance criteria, each a test named by its ID.
  - _Requirements: ASGD-REQ-F-039_
  - _Criteria: ASGD-C08-AC-01_
  - _After: ASGD-C08-T1_
- [ ] ASGD-C08-T3 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ASGD-REQ-F-039_
  - _After: ASGD-C08-T1_

## DTPR-C01 Extract account data to output files (final)

- [ ] DTPR-C01-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y (see data-contracts.md).
  - Working records it passes or builds: CODATECN.
  - _Requirements: DTPR-REQ-F-001, DTPR-REQ-F-002, DTPR-REQ-F-003, DTPR-REQ-F-004, DTPR-REQ-F-005, DTPR-REQ-F-006, DTPR-REQ-F-007, DTPR-REQ-F-008, DTPR-REQ-F-009, DTPR-REQ-F-010, DTPR-REQ-F-011, DTPR-REQ-F-012_
- [ ] DTPR-C01-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: DTPR-BR-006.
  - _Requirements: DTPR-REQ-F-003, DTPR-REQ-F-004, DTPR-REQ-F-005_
  - _Rules: DTPR-BR-004, DTPR-BR-005, DTPR-BR-006_
  - _After: DTPR-C01-T1_
- [ ] DTPR-C01-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-009, DTPR-REQ-F-010, DTPR-REQ-F-012_
  - _Rules: DTPR-BR-010, DTPR-BR-011, DTPR-BR-013_
  - _After: DTPR-C01-T1_
- [ ] DTPR-C01-T4 [api] Build the scheduled job
  - DTPR-BR-001: Map each account straight onto the flat account extract record: ID, active status, current balance, credit limit, cash credit limit, open date, expiration date, current cycle credit and group ID, with no changes to the values. Define the extract layout as a versioned contract that its downstream consumers agree to.
  - DTPR-BR-002: Parse the reissue date once from its stored YYYY-MM-DD form. Use it both for the YYYYMMDD output date and for the four-digit reissue year in the financial record, so the two can never disagree.
  - DTPR-BR-003: Use a standard date library to reformat the reissue date from YYYY-MM-DD to YYYYMMDD instead of a separate shared date-conversion routine. Decide and test how an invalid or blank reissue date is handled.
  - DTPR-BR-007: Produce a fixed 12-character status record per account: the account ID zero-padded to 11 digits, then the one-character active status. Downstream readers depend on the exact width.
  - DTPR-BR-008: After each account's status record, produce a 39-byte financial record (account ID, current balance, credit limit, reissue year) in the same output stream. Keep the order status-then-financial for each account, and give the numeric fields an agreed fixed encoding.
  - DTPR-BR-009: Process accounts as a sequential stream over the whole account master. Each account produces exactly one account record, one balance array record and two variable-length records, so the record counts can be reconciled (N, N, 2N) at the end of the run.
  - DTPR-BR-012: Treat running out of accounts as normal completion: close the source and log the completion message 'END OF EXECUTION OF PROGRAM CBACT01C' (or an agreed equivalent) with a success exit status for the scheduler.
  - _Requirements: DTPR-REQ-F-001, DTPR-REQ-F-002, DTPR-REQ-F-006, DTPR-REQ-F-007, DTPR-REQ-F-008, DTPR-REQ-F-011_
  - _Rules: DTPR-BR-001, DTPR-BR-002, DTPR-BR-003, DTPR-BR-007, DTPR-BR-008, DTPR-BR-009, DTPR-BR-012_
  - _After: DTPR-C01-T1, DTPR-C01-T2, DTPR-C01-T3_
- [ ] DTPR-C01-T5 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-001, DTPR-REQ-F-002, DTPR-REQ-F-003, DTPR-REQ-F-004, DTPR-REQ-F-005, DTPR-REQ-F-006, DTPR-REQ-F-007, DTPR-REQ-F-008, DTPR-REQ-F-009, DTPR-REQ-F-010, DTPR-REQ-F-011, DTPR-REQ-F-012_
  - _Criteria: DTPR-C01-AC-01, DTPR-C01-AC-02, DTPR-C01-AC-03, DTPR-C01-AC-04, DTPR-C01-AC-05, DTPR-C01-AC-06, DTPR-C01-AC-07, DTPR-C01-AC-08, DTPR-C01-AC-09, DTPR-C01-AC-10, DTPR-C01-AC-11, DTPR-C01-AC-12, DTPR-C01-AC-13, DTPR-C01-AC-14, DTPR-C01-AC-15_
  - _After: DTPR-C01-T1, DTPR-C01-T2, DTPR-C01-T3, DTPR-C01-T4_
- [ ] DTPR-C01-T6 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-001, DTPR-REQ-F-002, DTPR-REQ-F-003, DTPR-REQ-F-004, DTPR-REQ-F-005, DTPR-REQ-F-006, DTPR-REQ-F-007, DTPR-REQ-F-008, DTPR-REQ-F-009, DTPR-REQ-F-010, DTPR-REQ-F-011, DTPR-REQ-F-012_
  - _After: DTPR-C01-T1, DTPR-C01-T2, DTPR-C01-T3, DTPR-C01-T4_

## DTPR-C02 Validate daily transactions (final)

- [ ] DTPR-C02-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA05Y, CVTRA06Y (see data-contracts.md).
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
- [ ] DTPR-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
  - _Rules: DTPR-BR-014, DTPR-BR-015, DTPR-BR-016, DTPR-BR-017, DTPR-BR-018, DTPR-BR-019, DTPR-BR-020, DTPR-BR-021, DTPR-BR-022, DTPR-BR-023, DTPR-BR-024_
  - _After: DTPR-C02-T1_
- [ ] DTPR-C02-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
  - _Rules: DTPR-BR-014, DTPR-BR-015, DTPR-BR-016, DTPR-BR-017, DTPR-BR-018, DTPR-BR-019, DTPR-BR-020, DTPR-BR-021, DTPR-BR-022, DTPR-BR-023, DTPR-BR-024_
  - _After: DTPR-C02-T1, DTPR-C02-T2_
- [ ] DTPR-C02-T4 [test-generation] Write a test for every acceptance criterion
  - 20 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
  - _Criteria: DTPR-C02-AC-01, DTPR-C02-AC-02, DTPR-C02-AC-03, DTPR-C02-AC-04, DTPR-C02-AC-05, DTPR-C02-AC-06, DTPR-C02-AC-07, DTPR-C02-AC-08, DTPR-C02-AC-09, DTPR-C02-AC-10, DTPR-C02-AC-11, DTPR-C02-AC-12, DTPR-C02-AC-13, DTPR-C02-AC-14, DTPR-C02-AC-15, DTPR-C02-AC-16, DTPR-C02-AC-17, DTPR-C02-AC-18, DTPR-C02-AC-19, DTPR-C02-AC-20_
  - _After: DTPR-C02-T1, DTPR-C02-T2, DTPR-C02-T3_
- [ ] DTPR-C02-T5 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-013, DTPR-REQ-F-014, DTPR-REQ-F-015, DTPR-REQ-F-016, DTPR-REQ-F-017, DTPR-REQ-F-018, DTPR-REQ-F-019_
  - _After: DTPR-C02-T1, DTPR-C02-T2, DTPR-C02-T3_

## DTPR-C03 Post validated transactions (final)

- [ ] DTPR-C03-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA05Y, CVTRA06Y (see data-contracts.md).
  - _Requirements: DTPR-REQ-F-020, DTPR-REQ-F-021, DTPR-REQ-F-022, DTPR-REQ-F-023, DTPR-REQ-F-024, DTPR-REQ-F-025, DTPR-REQ-F-026, DTPR-REQ-F-027, DTPR-REQ-F-028, DTPR-REQ-F-029, DTPR-REQ-F-030, DTPR-REQ-F-031, DTPR-REQ-F-032_
- [ ] DTPR-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: DTPR-BR-035.
  - _Requirements: DTPR-REQ-F-020, DTPR-REQ-F-022, DTPR-REQ-F-023, DTPR-REQ-F-025, DTPR-REQ-F-026, DTPR-REQ-F-027, DTPR-REQ-F-029_
  - _Rules: DTPR-BR-025, DTPR-BR-026, DTPR-BR-028, DTPR-BR-029, DTPR-BR-031, DTPR-BR-032, DTPR-BR-033, DTPR-BR-035_
  - _After: DTPR-C03-T1_
- [ ] DTPR-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-024, DTPR-REQ-F-032_
  - _Rules: DTPR-BR-025, DTPR-BR-030, DTPR-BR-038_
  - _After: DTPR-C03-T1_
- [ ] DTPR-C03-T4 [api] Build the scheduled job
  - DTPR-BR-027: Look up the category balance by a composite key of account ID, transaction type and transaction category; a unique key or index on these three columns. 'Not found' must be told apart from other errors, because 'not found' leads to creating the record.
  - DTPR-BR-034: Save the account's new balance and cycle totals before writing the posted transaction. Ideally both happen in one database transaction, so an account is never updated without its transaction record, or the reverse.
  - DTPR-BR-036: Map the posted transaction field for field from the daily transaction: ID, type, category, source, description, amount, merchant ID, name, city, ZIP, card number and original timestamp. Only the processed timestamp is added by posting.
  - DTPR-BR-037: Take the processed timestamp from the run's clock and store it as a proper timestamp. Where it is exported or compared with legacy data, render it as YYYY-MM-DD-HH.MM.SS.hh0000 (hundredths of a second followed by '0000').
  - _Requirements: DTPR-REQ-F-021, DTPR-REQ-F-028, DTPR-REQ-F-030, DTPR-REQ-F-031_
  - _Rules: DTPR-BR-027, DTPR-BR-034, DTPR-BR-036, DTPR-BR-037_
  - _After: DTPR-C03-T1, DTPR-C03-T2, DTPR-C03-T3_
- [ ] DTPR-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 17 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-020, DTPR-REQ-F-021, DTPR-REQ-F-022, DTPR-REQ-F-023, DTPR-REQ-F-024, DTPR-REQ-F-025, DTPR-REQ-F-026, DTPR-REQ-F-027, DTPR-REQ-F-028, DTPR-REQ-F-029, DTPR-REQ-F-030, DTPR-REQ-F-031, DTPR-REQ-F-032_
  - _Criteria: DTPR-C03-AC-01, DTPR-C03-AC-02, DTPR-C03-AC-03, DTPR-C03-AC-04, DTPR-C03-AC-05, DTPR-C03-AC-06, DTPR-C03-AC-07, DTPR-C03-AC-08, DTPR-C03-AC-09, DTPR-C03-AC-10, DTPR-C03-AC-11, DTPR-C03-AC-12, DTPR-C03-AC-13, DTPR-C03-AC-14, DTPR-C03-AC-15, DTPR-C03-AC-16, DTPR-C03-AC-17_
  - _After: DTPR-C03-T1, DTPR-C03-T2, DTPR-C03-T3, DTPR-C03-T4_
- [ ] DTPR-C03-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-020, DTPR-REQ-F-021, DTPR-REQ-F-022, DTPR-REQ-F-023, DTPR-REQ-F-024, DTPR-REQ-F-025, DTPR-REQ-F-026, DTPR-REQ-F-027, DTPR-REQ-F-028, DTPR-REQ-F-029, DTPR-REQ-F-030, DTPR-REQ-F-031, DTPR-REQ-F-032_
  - _After: DTPR-C03-T1, DTPR-C03-T2, DTPR-C03-T3, DTPR-C03-T4_

## DTPR-C04 Run daily posting and handle rejects (final)

- [ ] DTPR-C04-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA05Y, CVTRA06Y (see data-contracts.md).
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037_
- [ ] DTPR-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034_
  - _Rules: DTPR-BR-039, DTPR-BR-040_
  - _After: DTPR-C04-T1_
- [ ] DTPR-C04-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-035, DTPR-REQ-F-037, DTPR-REQ-F-036_
  - _Rules: DTPR-BR-041, DTPR-BR-042, DTPR-BR-043_
  - _After: DTPR-C04-T1_
- [ ] DTPR-C04-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037_
  - _Rules: DTPR-BR-039, DTPR-BR-040, DTPR-BR-041, DTPR-BR-042, DTPR-BR-043_
  - _After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3_
- [ ] DTPR-C04-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037_
  - _Criteria: DTPR-C04-AC-01, DTPR-C04-AC-02, DTPR-C04-AC-03, DTPR-C04-AC-04, DTPR-C04-AC-05, DTPR-C04-AC-06, DTPR-C04-AC-07_
  - _After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3, DTPR-C04-T4_
- [ ] DTPR-C04-T6 [compliance] Review the handling of audit, card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037_
  - _After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3, DTPR-C04-T4_

## DTPR-C05 Calculate and post monthly interest (final)

- [ ] DTPR-C05-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA02Y, CVTRA05Y (see data-contracts.md).
  - _Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051_
- [ ] DTPR-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: DTPR-BR-051.
  - _Requirements: DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-046_
  - _Rules: DTPR-BR-045, DTPR-BR-046, DTPR-BR-047, DTPR-BR-048, DTPR-BR-049, DTPR-BR-050, DTPR-BR-051, DTPR-BR-052, DTPR-BR-053_
  - _After: DTPR-C05-T1_
- [ ] DTPR-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051_
  - _Rules: DTPR-BR-054, DTPR-BR-055, DTPR-BR-056_
  - _After: DTPR-C05-T1_
- [ ] DTPR-C05-T4 [api] Build the scheduled job
  - DTPR-BR-044: Read all category balances in key order (account ID, then type, then category) as one sorted stream, so each account's balances come together. The per-account interest total and the account rewrite depend on that grouping.
  - _Requirements: DTPR-REQ-F-038_
  - _Rules: DTPR-BR-044_
  - _After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3_
- [ ] DTPR-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 17 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051_
  - _Criteria: DTPR-C05-AC-01, DTPR-C05-AC-02, DTPR-C05-AC-03, DTPR-C05-AC-04, DTPR-C05-AC-05, DTPR-C05-AC-06, DTPR-C05-AC-07, DTPR-C05-AC-08, DTPR-C05-AC-09, DTPR-C05-AC-10, DTPR-C05-AC-11, DTPR-C05-AC-12, DTPR-C05-AC-13, DTPR-C05-AC-14, DTPR-C05-AC-15, DTPR-C05-AC-16, DTPR-C05-AC-17_
  - _After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3, DTPR-C05-T4_
- [ ] DTPR-C05-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051_
  - _After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3, DTPR-C05-T4_

## DTPR-C06 Produce daily transaction report (final)

- [ ] DTPR-C06-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA03Y, CVTRA04Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: CVTRA07Y.
  - _Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056_
- [ ] DTPR-C06-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-056_
  - _Rules: DTPR-BR-057, DTPR-BR-058, DTPR-BR-060_
  - _After: DTPR-C06-T1_
- [ ] DTPR-C06-T3 [api] Build the services and the scheduled job
  - DTPR-BR-059: For each in-range transaction, look up the card's cross-reference (giving the account) by card number, the type description by type code, and the category description by type and category code. A missing reference record must fail the report run rather than print a blank. The type and category tables are small and can be cached for the run.
  - _Requirements: DTPR-REQ-F-054, DTPR-REQ-F-055_
  - _Rules: DTPR-BR-059_
  - _After: DTPR-C06-T1, DTPR-C06-T2_
- [ ] DTPR-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056_
  - _Criteria: DTPR-C06-AC-01, DTPR-C06-AC-02, DTPR-C06-AC-03, DTPR-C06-AC-04, DTPR-C06-AC-05, DTPR-C06-AC-06, DTPR-C06-AC-07, DTPR-C06-AC-08_
  - _After: DTPR-C06-T1, DTPR-C06-T2, DTPR-C06-T3_
- [ ] DTPR-C06-T5 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056_
  - _After: DTPR-C06-T1, DTPR-C06-T2, DTPR-C06-T3_

## DTPR-C07 Post daily transactions and record rejects (final)

- [ ] DTPR-C07-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-058, DTPR-REQ-N-001_
  - _Rules: DTPR-BR-062_
- [ ] DTPR-C07-T2 [api] Build the scheduled job
  - DTPR-BR-061: Run a scheduled daily job that reads the day's transaction feed and, for each transaction, uses the card cross-reference and posts to the transaction master, account and category balance tables. The job needs read access to the feed and cross-reference, and write access to transactions, accounts and category balances. Schedule it after the daily feed arrives and before any jobs that read the posted data.
  - _Requirements: DTPR-REQ-F-057_
  - _Rules: DTPR-BR-061_
  - _After: DTPR-C07-T1_
- [ ] DTPR-C07-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-057, DTPR-REQ-F-058, DTPR-REQ-N-001_
  - _Criteria: DTPR-C07-AC-01, DTPR-C07-AC-02, DTPR-C07-AC-03_
  - _After: DTPR-C07-T1, DTPR-C07-T2_
- [ ] DTPR-C07-T4 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-057, DTPR-REQ-F-058, DTPR-REQ-N-001_
  - _After: DTPR-C07-T1, DTPR-C07-T2_

## DTPR-C08 Calculate monthly interest as system transactions (final)

- [ ] DTPR-C08-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-061_
  - _Rules: DTPR-BR-065_
- [ ] DTPR-C08-T2 [api] Build the scheduled job
  - DTPR-BR-063: Run a scheduled monthly job that takes the processing date as a run parameter (the delivered job used '2022071800') rather than the system clock, so a run can be repeated or backdated. It reads category balances, the card cross-reference by card and by account, accounts and disclosure groups without locking out other readers.
  - DTPR-BR-064: Write the generated interest transactions as one new, versioned batch output (a new file version or a batch-tagged table load) in the 350-byte transaction layout. Publish it only if the job succeeds and discard it on failure, so the combine step never picks up a partial batch.
  - _Requirements: DTPR-REQ-F-059, DTPR-REQ-F-060, DTPR-REQ-N-002_
  - _Rules: DTPR-BR-063, DTPR-BR-064_
  - _After: DTPR-C08-T1_
- [ ] DTPR-C08-T3 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-059, DTPR-REQ-F-060, DTPR-REQ-N-002, DTPR-REQ-F-061_
  - _Criteria: DTPR-C08-AC-01, DTPR-C08-AC-02, DTPR-C08-AC-03, DTPR-C08-AC-04_
  - _After: DTPR-C08-T1, DTPR-C08-T2_
- [ ] DTPR-C08-T4 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-059, DTPR-REQ-F-060, DTPR-REQ-N-002, DTPR-REQ-F-061_
  - _After: DTPR-C08-T1, DTPR-C08-T2_

## DTPR-C09 Consolidate transactions into the transaction master (final)

- [ ] DTPR-C09-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-003_
  - _Rules: DTPR-BR-067_
- [ ] DTPR-C09-T2 [api] Build the scheduled job
  - DTPR-BR-066: Build a sorted extract that merges the latest transaction backup with the latest system-transaction batch, ordered ascending by the 16-character transaction ID, and publish it as a new version. Make it a scheduled step that depends on the backup and interest jobs, and discard its output if it fails.
  - DTPR-BR-068: Load every record of the combined, sorted set into the transaction store keyed by transaction ID, as a bulk load or upsert in one step. Decide explicitly what to do with duplicate transaction IDs.
  - _Requirements: DTPR-REQ-F-062, DTPR-REQ-F-063_
  - _Rules: DTPR-BR-066, DTPR-BR-068_
  - _After: DTPR-C09-T1_
- [ ] DTPR-C09-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-062, DTPR-REQ-N-003, DTPR-REQ-F-063_
  - _Criteria: DTPR-C09-AC-01, DTPR-C09-AC-02, DTPR-C09-AC-03_
  - _After: DTPR-C09-T1, DTPR-C09-T2_
- [ ] DTPR-C09-T4 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-062, DTPR-REQ-N-003, DTPR-REQ-F-063_
  - _After: DTPR-C09-T1, DTPR-C09-T2_

## DTPR-C10 Back up the transaction master (final)

- [ ] DTPR-C10-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-004, DTPR-REQ-N-005_
  - _Rules: DTPR-BR-069, DTPR-BR-071_
- [ ] DTPR-C10-T2 [api] Build the scheduled job
  - DTPR-BR-069: Run a scheduled snapshot job that copies every transaction to a new, versioned backup in the 350-byte layout. Publish the new version only on success and discard it on failure, keeping earlier versions available.
  - DTPR-BR-070: Take the snapshot with a consistent, non-blocking read (for example a read-only snapshot or export), so other jobs can still read the transaction master during the backup.
  - _Requirements: DTPR-REQ-F-064_
  - _Rules: DTPR-BR-069, DTPR-BR-070_
  - _After: DTPR-C10-T1_
- [ ] DTPR-C10-T3 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-064, DTPR-REQ-N-004, DTPR-REQ-N-005_
  - _Criteria: DTPR-C10-AC-01, DTPR-C10-AC-02, DTPR-C10-AC-03, DTPR-C10-AC-04, DTPR-C10-AC-05_
  - _After: DTPR-C10-T1, DTPR-C10-T2_
- [ ] DTPR-C10-T4 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-064, DTPR-REQ-N-004, DTPR-REQ-N-005_
  - _After: DTPR-C10-T1, DTPR-C10-T2_

## DTPR-C11 Set up the transaction master and its timestamp index (final)

- [ ] DTPR-C11-T1 [api] Build the scheduled job
  - DTPR-BR-072: Provide a setup or seeding job that empties the transaction store (drop and recreate, or truncate) and bulk-loads every record from the initial daily transaction file. It is for environment setup only and must never be part of the regular daily schedule.
  - DTPR-BR-073: Add a secondary, non-unique index on the transaction's processed timestamp, the 26-character value at offset 304 in the legacy record, alongside the primary key on transaction ID. In a relational store this is an ordinary database index kept up to date automatically rather than rebuilt after loading.
  - _Requirements: DTPR-REQ-F-065, DTPR-REQ-F-066_
  - _Rules: DTPR-BR-072, DTPR-BR-073_
- [ ] DTPR-C11-T2 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-065, DTPR-REQ-F-066_
  - _Criteria: DTPR-C11-AC-01, DTPR-C11-AC-02_
  - _After: DTPR-C11-T1_

## DTPR-C12 Load disclosure group and category balance masters (final)

- [ ] DTPR-C12-T1 [api] Build the scheduled job
  - DTPR-BR-074: Make the disclosure group load a full replace: clear or recreate the store, keyed on the 16-character key of group ID, type and category over 50-byte records, before loading. Treat an absent previous store as normal, not an error.
  - DTPR-BR-075: Bulk-load every record of the disclosure group feed into the keyed disclosure group store. Load it as one unit (in a single transaction, or by swapping in a staging table) so the interest job never sees a partly loaded rate table.
  - DTPR-BR-076: Bulk-load every category balance record from the flat feed into the category balance store, keyed on account ID, type and category. Hold exclusive write access during the load, and schedule it so it never overlaps the posting or interest jobs.
  - _Requirements: DTPR-REQ-F-067, DTPR-REQ-N-006, DTPR-REQ-F-068, DTPR-REQ-F-069_
  - _Rules: DTPR-BR-074, DTPR-BR-075, DTPR-BR-076_
- [ ] DTPR-C12-T2 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-067, DTPR-REQ-N-006, DTPR-REQ-F-068, DTPR-REQ-F-069_
  - _Criteria: DTPR-C12-AC-01, DTPR-C12-AC-02, DTPR-C12-AC-03, DTPR-C12-AC-04, DTPR-C12-AC-05_
  - _After: DTPR-C12-T1_
- [ ] DTPR-C12-T3 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-067, DTPR-REQ-N-006, DTPR-REQ-F-068, DTPR-REQ-F-069_
  - _After: DTPR-C12-T1_

## DTPR-C13 Print the transaction category balance report (final)

- [ ] DTPR-C13-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-007, DTPR-REQ-N-008, DTPR-REQ-F-071_
  - _Rules: DTPR-BR-078, DTPR-BR-079_
- [ ] DTPR-C13-T2 [api] Build the scheduled job
  - DTPR-BR-077: Before reporting, remove the previous category balance report and take a complete point-in-time snapshot of all category balance records as a new numbered backup version. The report is then built from that snapshot, not from the live balances, so it reflects one consistent moment.
  - _Requirements: DTPR-REQ-F-070_
  - _Rules: DTPR-BR-077_
  - _After: DTPR-C13-T1_
- [ ] DTPR-C13-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-070, DTPR-REQ-F-071, DTPR-REQ-N-007, DTPR-REQ-N-008_
  - _Criteria: DTPR-C13-AC-01, DTPR-C13-AC-02, DTPR-C13-AC-03_
  - _After: DTPR-C13-T1, DTPR-C13-T2_
- [ ] DTPR-C13-T4 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-070, DTPR-REQ-F-071, DTPR-REQ-N-007, DTPR-REQ-N-008_
  - _After: DTPR-C13-T1, DTPR-C13-T2_

## DTPR-C14 Produce account extracts from the account master (final)

- [ ] DTPR-C14-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-073_
  - _Rules: DTPR-BR-081_
- [ ] DTPR-C14-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-009, DTPR-REQ-N-010_
  - _Rules: DTPR-BR-082_
- [ ] DTPR-C14-T3 [api] Build the scheduled job
  - DTPR-BR-080: The extract job must clear out the previous run's account extract, account array extract and variable-record extract before writing, so each run's outputs are regenerated from scratch and never appended to or merged with older data.
  - _Requirements: DTPR-REQ-F-072_
  - _Rules: DTPR-BR-080_
  - _After: DTPR-C14-T1, DTPR-C14-T2_
- [ ] DTPR-C14-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-072, DTPR-REQ-F-073, DTPR-REQ-N-009, DTPR-REQ-N-010_
  - _Criteria: DTPR-C14-AC-01, DTPR-C14-AC-02, DTPR-C14-AC-03_
  - _After: DTPR-C14-T1, DTPR-C14-T2, DTPR-C14-T3_
- [ ] DTPR-C14-T5 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-072, DTPR-REQ-F-073, DTPR-REQ-N-009, DTPR-REQ-N-010_
  - _After: DTPR-C14-T1, DTPR-C14-T2, DTPR-C14-T3_

## DTPR-C15 Extract transactions for a reporting period (final)

- [ ] DTPR-C15-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-075, DTPR-REQ-F-076, DTPR-REQ-F-077, DTPR-REQ-F-078_
  - _Rules: DTPR-BR-084, DTPR-BR-085, DTPR-BR-086, DTPR-BR-088_
- [ ] DTPR-C15-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-011_
  - _Rules: DTPR-BR-087_
- [ ] DTPR-C15-T3 [api] Build the scheduled job
  - DTPR-BR-083: Start each reporting run by copying every transaction record into a new numbered backup version, a point-in-time snapshot. Keep the version only if the copy completes, and discard it on failure so later steps never read a partial backup.
  - DTPR-BR-089: The sort test job needs a sorted extract: the selected transactions, in ascending card number order and with the same record layout as the backup, written as a new numbered version of the daily transaction file. Keep the version when the step succeeds and delete it when the step fails.
  - _Requirements: DTPR-REQ-F-074, DTPR-REQ-F-079_
  - _Rules: DTPR-BR-083, DTPR-BR-089_
  - _After: DTPR-C15-T1, DTPR-C15-T2_
- [ ] DTPR-C15-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **primary button** "Submit report": The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again.
  - _Requirements: DTPR-REQ-F-077_
  - _Rules: DTPR-BR-086_
  - _After: DTPR-C15-T1, DTPR-C15-T2, DTPR-C15-T3_
- [ ] DTPR-C15-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-074, DTPR-REQ-F-075, DTPR-REQ-F-076, DTPR-REQ-F-077, DTPR-REQ-N-011, DTPR-REQ-F-078, DTPR-REQ-F-079_
  - _Criteria: DTPR-C15-AC-01, DTPR-C15-AC-02, DTPR-C15-AC-03, DTPR-C15-AC-04, DTPR-C15-AC-05, DTPR-C15-AC-06, DTPR-C15-AC-07, DTPR-C15-AC-08, DTPR-C15-AC-09, DTPR-C15-AC-10, DTPR-C15-AC-11_
  - _After: DTPR-C15-T1, DTPR-C15-T2, DTPR-C15-T3, DTPR-C15-T4_
- [ ] DTPR-C15-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-074, DTPR-REQ-F-075, DTPR-REQ-F-076, DTPR-REQ-F-077, DTPR-REQ-N-011, DTPR-REQ-F-078, DTPR-REQ-F-079_
  - _After: DTPR-C15-T1, DTPR-C15-T2, DTPR-C15-T3, DTPR-C15-T4_

## DTPR-C16 Run the transaction report job (final)

- [ ] DTPR-C16-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-081_
  - _Rules: DTPR-BR-091_
- [ ] DTPR-C16-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-012_
  - _Rules: DTPR-BR-092_
- [ ] DTPR-C16-T3 [api] Build the scheduled job
  - DTPR-BR-090: Run the report as a job step that starts only after the period extract exists. It reads the extract and does keyed lookups on the card cross-reference (card to account), transaction types and transaction categories, plus the report date parameters. It writes a new numbered version of the transaction report as 133-character print lines.
  - _Requirements: DTPR-REQ-F-080_
  - _Rules: DTPR-BR-090_
  - _After: DTPR-C16-T1, DTPR-C16-T2_
- [ ] DTPR-C16-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **primary button** "Submit report": The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again.
  - _Requirements: DTPR-REQ-F-081_
  - _Rules: DTPR-BR-091_
  - _After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3_
- [ ] DTPR-C16-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-080, DTPR-REQ-F-081, DTPR-REQ-N-012_
  - _Criteria: DTPR-C16-AC-01, DTPR-C16-AC-02, DTPR-C16-AC-03_
  - _After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3, DTPR-C16-T4_
- [ ] DTPR-C16-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-080, DTPR-REQ-F-081, DTPR-REQ-N-012_
  - _After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3, DTPR-C16-T4_

## DTPR-C17 Print the daily transaction report with totals (final)

- [ ] DTPR-C17-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA03Y, CVTRA04Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: CVTRA07Y.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
- [ ] DTPR-C17-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
  - _Rules: DTPR-BR-093, DTPR-BR-094, DTPR-BR-096, DTPR-BR-097, DTPR-BR-098_
  - _After: DTPR-C17-T1_
- [ ] DTPR-C17-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-084_
  - _Rules: DTPR-BR-095_
  - _After: DTPR-C17-T1_
- [ ] DTPR-C17-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
  - _Rules: DTPR-BR-093, DTPR-BR-094, DTPR-BR-095, DTPR-BR-096, DTPR-BR-097, DTPR-BR-098_
  - _After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3_
- [ ] DTPR-C17-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
  - _Criteria: DTPR-C17-AC-01, DTPR-C17-AC-02, DTPR-C17-AC-03, DTPR-C17-AC-04, DTPR-C17-AC-05, DTPR-C17-AC-06, DTPR-C17-AC-07_
  - _After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3, DTPR-C17-T4_
- [ ] DTPR-C17-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
  - _After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3, DTPR-C17-T4_

## OATM-C01 Find the account to update (final)

- [ ] OATM-C01-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013, OATM-REQ-F-014_
- [ ] OATM-C01-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: OATM-BR-003.
  - _Requirements: OATM-REQ-F-005, OATM-REQ-F-003_
  - _Rules: OATM-BR-003, OATM-BR-005_
  - _After: OATM-C01-T1_
- [ ] OATM-C01-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-006, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-001, OATM-REQ-F-002_
  - _Rules: OATM-BR-001, OATM-BR-002, OATM-BR-006, OATM-BR-008, OATM-BR-009, OATM-BR-011, OATM-BR-012_
  - _After: OATM-C01-T1_
- [ ] OATM-C01-T4 [api] Build the services behind the screens
  - OATM-BR-004: Look up the card-to-account cross-reference by account ID (a secondary index on account ID, not the card number). The result gives the customer ID and card number, and the following account and customer reads use them. Keep them in the operator's update session.
  - OATM-BR-007: Read the account record by its primary key, the 11-digit account ID, and mark the account as found when it exists. Keep 'not found' separate from other read failures: each has its own message.
  - OATM-BR-010: Read the customer record by its primary key, using the customer ID taken from the cross-reference, and mark the customer as found when it exists. Keep 'not found' separate from other read failures.
  - OATM-BR-013: Keep the account ID, customer ID, customer names, account status and card number in the operator's update session (server-side state or a signed token). This context must survive across requests until the update is saved or cancelled.
  - OATM-BR-014: Keep a snapshot of the account and customer values as fetched. Change detection and the 'changed by someone else' check on save both compare against it. Hold dates as real dates; the screen may still show and edit the open, expiry, reissue and birth dates as separate year, month and day parts. A version number or timestamp on each record can replace the field-by-field snapshot comparison.
  - _Requirements: OATM-REQ-F-004, OATM-REQ-F-007, OATM-REQ-F-010, OATM-REQ-F-013, OATM-REQ-F-014_
  - _Rules: OATM-BR-004, OATM-BR-007, OATM-BR-010, OATM-BR-013, OATM-BR-014_
  - _After: OATM-C01-T1, OATM-C01-T2, OATM-C01-T3_
- [ ] OATM-C01-T5 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **lookup field** "Account number": Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched.
  - _Requirements: OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013_
  - _Rules: OATM-BR-001, OATM-BR-002, OATM-BR-003, OATM-BR-004, OATM-BR-005, OATM-BR-006, OATM-BR-007, OATM-BR-008, OATM-BR-009, OATM-BR-010, OATM-BR-011, OATM-BR-012, OATM-BR-013_
  - _After: OATM-C01-T2, OATM-C01-T3, OATM-C01-T4_
- [ ] OATM-C01-T6 [test-generation] Write a test for every acceptance criterion
  - 14 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013, OATM-REQ-F-014_
  - _Criteria: OATM-C01-AC-01, OATM-C01-AC-02, OATM-C01-AC-03, OATM-C01-AC-04, OATM-C01-AC-05, OATM-C01-AC-06, OATM-C01-AC-07, OATM-C01-AC-08, OATM-C01-AC-09, OATM-C01-AC-10, OATM-C01-AC-11, OATM-C01-AC-12, OATM-C01-AC-13, OATM-C01-AC-14_
  - _After: OATM-C01-T1, OATM-C01-T2, OATM-C01-T3, OATM-C01-T4, OATM-C01-T5_
- [ ] OATM-C01-T7 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003, OATM-REQ-F-004, OATM-REQ-F-005, OATM-REQ-F-006, OATM-REQ-F-007, OATM-REQ-F-008, OATM-REQ-F-009, OATM-REQ-F-010, OATM-REQ-F-011, OATM-REQ-F-012, OATM-REQ-F-013, OATM-REQ-F-014_
  - _After: OATM-C01-T1, OATM-C01-T2, OATM-C01-T3, OATM-C01-T4, OATM-C01-T5_

## OATM-C02 View account and customer details for update (final)

- [ ] OATM-C02-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
- [ ] OATM-C02-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
  - _Rules: OATM-BR-015, OATM-BR-016, OATM-BR-017, OATM-BR-018, OATM-BR-019, OATM-BR-020, OATM-BR-021, OATM-BR-022, OATM-BR-023, OATM-BR-024, OATM-BR-025_
  - _After: OATM-C02-T1_
- [ ] OATM-C02-T3 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **lookup field** "Account number": Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Fix these before saving"
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
  - _Rules: OATM-BR-015, OATM-BR-016, OATM-BR-017, OATM-BR-018, OATM-BR-019, OATM-BR-020, OATM-BR-021, OATM-BR-022, OATM-BR-023, OATM-BR-024, OATM-BR-025_
  - _After: OATM-C02-T2_
- [ ] OATM-C02-T4 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
  - _Criteria: OATM-C02-AC-01, OATM-C02-AC-02, OATM-C02-AC-03, OATM-C02-AC-04, OATM-C02-AC-05, OATM-C02-AC-06, OATM-C02-AC-07, OATM-C02-AC-08, OATM-C02-AC-09, OATM-C02-AC-10, OATM-C02-AC-11, OATM-C02-AC-12, OATM-C02-AC-13, OATM-C02-AC-14, OATM-C02-AC-15_
  - _After: OATM-C02-T1, OATM-C02-T2, OATM-C02-T3_
- [ ] OATM-C02-T5 [compliance] Review the handling of card data, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
  - _After: OATM-C02-T1, OATM-C02-T2, OATM-C02-T3_

## OATM-C03 Capture entered changes (final)

- [ ] OATM-C03-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032_
- [ ] OATM-C03-T2 [api] Build the services behind the screens
  - OATM-BR-026: Model the proposed account group as an optional value: blank or '*' input becomes 'absent' (null), not an empty string. Any other input becomes the proposed group.
  - OATM-BR-027: Treat blank or '*' country code input as absent (null). Otherwise take the entered value as the proposed country code.
  - OATM-BR-028: Treat a blank or '*' customer number as absent (null); otherwise it is the proposed value. Change detection compares it with the stored customer number, and it is written to the customer record on save.
  - OATM-BR-029: Treat a blank or '*' government-issued ID as absent (null); otherwise it is the proposed value. Change detection compares it with the stored ID, and it is written to the customer record on save.
  - OATM-BR-030: Hold each of the five amounts as an optional input: credit limit, cash credit limit, current balance, current cycle credit and current cycle debit. Blank or '*' means absent, which validation then reports as 'must be supplied.'.
  - OATM-BR-031: Parse entered amounts with a currency parser that accepts an optional '$', thousands commas, a sign and decimals. Convert to an exact decimal with two places (a decimal type, never floating point). Input that does not parse stays as entered text so validation can report it as not valid.
  - OATM-BR-032: Capture the open, expiry and reissue dates as three separate optional parts (year, month, day). A blank or '*' part is absent; any other part is kept exactly as typed so date validation can check it.
  - OATM-BR-033: Capture the date of birth as three separate optional parts (year, month, day). A blank or '*' part is absent; any other part is kept as typed for validation.
  - _Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032_
  - _Rules: OATM-BR-026, OATM-BR-027, OATM-BR-028, OATM-BR-029, OATM-BR-030, OATM-BR-031, OATM-BR-032, OATM-BR-033_
  - _After: OATM-C03-T1_
- [ ] OATM-C03-T3 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Account dates": For each date, in the rule's words: '<date> : Year must be supplied.', '<date> must be 4 digit number.', '<date> : Century is not valid.' (year must start 19 or 20), '<date> : Month must be supplied.', '<date>: Month must be a number between 1 and 12.', '<date> : Day must be supplied.', '<date>:day must be a number between 1 and 31.', '<date>:Cannot have 31 days in this month.', '<date>:Cannot have 30 days in this month.', '<date>:Not a leap year.Cannot have 29 days in this month.', and a final calendar check '<date> validation error'. The message sits under the part to fix.
  - **summary card** "Limits and balances": Each amount is required: '<field> must be supplied.' (e.g. 'Credit Limit must be supplied.'), and must be a currency number: '<field> is not valid' - enter an amount such as 1,250.00. Negative values and zero are accepted.
  - **summary card** "Customer identity": SSN: 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.', 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'; the 4th & 5th and last 4 characters must each be supplied, all numeric and non-zero. Date of birth: the date checks above, and 'Date of Birth:cannot be in the future '. FICO: 'FICO Score must be supplied.', 'FICO Score must be all numeric.', 'FICO Score must not be zero.', 'FICO Score: should be between 300 and 850'.
  - **summary card** "Name and address": '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together.
  - _Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032_
  - _Rules: OATM-BR-026, OATM-BR-027, OATM-BR-028, OATM-BR-029, OATM-BR-030, OATM-BR-031, OATM-BR-032, OATM-BR-033_
  - _After: OATM-C03-T2_
- [ ] OATM-C03-T4 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032_
  - _Criteria: OATM-C03-AC-01, OATM-C03-AC-02, OATM-C03-AC-03, OATM-C03-AC-04, OATM-C03-AC-05, OATM-C03-AC-06, OATM-C03-AC-07, OATM-C03-AC-08, OATM-C03-AC-09, OATM-C03-AC-10, OATM-C03-AC-11, OATM-C03-AC-12, OATM-C03-AC-13, OATM-C03-AC-14, OATM-C03-AC-15_
  - _After: OATM-C03-T1, OATM-C03-T2, OATM-C03-T3_
- [ ] OATM-C03-T5 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032_
  - _After: OATM-C03-T1, OATM-C03-T2, OATM-C03-T3_

## OATM-C04 Validate changed account and customer fields (final)

- [ ] OATM-C04-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
- [ ] OATM-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
  - _Rules: OATM-BR-034, OATM-BR-035, OATM-BR-036, OATM-BR-037, OATM-BR-038, OATM-BR-039, OATM-BR-040, OATM-BR-041, OATM-BR-042, OATM-BR-043_
  - _After: OATM-C04-T1_
- [ ] OATM-C04-T3 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Account dates": For each date, in the rule's words: '<date> : Year must be supplied.', '<date> must be 4 digit number.', '<date> : Century is not valid.' (year must start 19 or 20), '<date> : Month must be supplied.', '<date>: Month must be a number between 1 and 12.', '<date> : Day must be supplied.', '<date>:day must be a number between 1 and 31.', '<date>:Cannot have 31 days in this month.', '<date>:Cannot have 30 days in this month.', '<date>:Not a leap year.Cannot have 29 days in this month.', and a final calendar check '<date> validation error'. The message sits under the part to fix.
  - **summary card** "Limits and balances": Each amount is required: '<field> must be supplied.' (e.g. 'Credit Limit must be supplied.'), and must be a currency number: '<field> is not valid' - enter an amount such as 1,250.00. Negative values and zero are accepted.
  - **summary card** "Customer identity": SSN: 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.', 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'; the 4th & 5th and last 4 characters must each be supplied, all numeric and non-zero. Date of birth: the date checks above, and 'Date of Birth:cannot be in the future '. FICO: 'FICO Score must be supplied.', 'FICO Score must be all numeric.', 'FICO Score must not be zero.', 'FICO Score: should be between 300 and 850'.
  - **summary card** "Name and address": '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together.
  - **summary card** "Fix these before saving"
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
  - _Rules: OATM-BR-034, OATM-BR-035, OATM-BR-036, OATM-BR-037, OATM-BR-038, OATM-BR-039, OATM-BR-040, OATM-BR-041, OATM-BR-042, OATM-BR-043_
  - _After: OATM-C04-T2_
- [ ] OATM-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 18 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
  - _Criteria: OATM-C04-AC-01, OATM-C04-AC-02, OATM-C04-AC-03, OATM-C04-AC-04, OATM-C04-AC-05, OATM-C04-AC-06, OATM-C04-AC-07, OATM-C04-AC-08, OATM-C04-AC-09, OATM-C04-AC-10, OATM-C04-AC-11, OATM-C04-AC-12, OATM-C04-AC-13, OATM-C04-AC-14, OATM-C04-AC-15, OATM-C04-AC-16, OATM-C04-AC-17, OATM-C04-AC-18_
  - _After: OATM-C04-T1, OATM-C04-T2, OATM-C04-T3_
- [ ] OATM-C04-T5 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-033, OATM-REQ-F-034, OATM-REQ-F-035, OATM-REQ-F-036, OATM-REQ-F-037, OATM-REQ-F-038, OATM-REQ-F-039, OATM-REQ-F-040, OATM-REQ-F-041, OATM-REQ-F-042, OATM-REQ-F-043, OATM-REQ-N-003, OATM-REQ-F-044_
  - _After: OATM-C04-T1, OATM-C04-T2, OATM-C04-T3_

## OATM-C05 Validate account and customer dates (final)

- [ ] OATM-C05-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057, OATM-REQ-F-058_
- [ ] OATM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057_
  - _Rules: OATM-BR-044, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051, OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056_
  - _After: OATM-C05-T1_
- [ ] OATM-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-058_
  - _Rules: OATM-BR-057_
  - _After: OATM-C05-T1_
- [ ] OATM-C05-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Account dates": For each date, in the rule's words: '<date> : Year must be supplied.', '<date> must be 4 digit number.', '<date> : Century is not valid.' (year must start 19 or 20), '<date> : Month must be supplied.', '<date>: Month must be a number between 1 and 12.', '<date> : Day must be supplied.', '<date>:day must be a number between 1 and 31.', '<date>:Cannot have 31 days in this month.', '<date>:Cannot have 30 days in this month.', '<date>:Not a leap year.Cannot have 29 days in this month.', and a final calendar check '<date> validation error'. The message sits under the part to fix.
  - **summary card** "Customer identity": SSN: 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.', 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'; the 4th & 5th and last 4 characters must each be supplied, all numeric and non-zero. Date of birth: the date checks above, and 'Date of Birth:cannot be in the future '. FICO: 'FICO Score must be supplied.', 'FICO Score must be all numeric.', 'FICO Score must not be zero.', 'FICO Score: should be between 300 and 850'.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057, OATM-REQ-F-058_
  - _Rules: OATM-BR-044, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051, OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057_
  - _After: OATM-C05-T2, OATM-C05-T3_
- [ ] OATM-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057, OATM-REQ-F-058_
  - _Criteria: OATM-C05-AC-01, OATM-C05-AC-02, OATM-C05-AC-03, OATM-C05-AC-04, OATM-C05-AC-05, OATM-C05-AC-06, OATM-C05-AC-07, OATM-C05-AC-08, OATM-C05-AC-09, OATM-C05-AC-10, OATM-C05-AC-11, OATM-C05-AC-12, OATM-C05-AC-13, OATM-C05-AC-14, OATM-C05-AC-15_
  - _After: OATM-C05-T1, OATM-C05-T2, OATM-C05-T3, OATM-C05-T4_
- [ ] OATM-C05-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-045, OATM-REQ-F-046, OATM-REQ-F-047, OATM-REQ-F-048, OATM-REQ-F-049, OATM-REQ-F-050, OATM-REQ-F-051, OATM-REQ-F-052, OATM-REQ-F-053, OATM-REQ-F-054, OATM-REQ-F-055, OATM-REQ-F-056, OATM-REQ-F-057, OATM-REQ-F-058_
  - _After: OATM-C05-T1, OATM-C05-T2, OATM-C05-T3, OATM-C05-T4_

## OATM-C06 Confirm and save the account update (final)

- [ ] OATM-C06-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061_
- [ ] OATM-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-059_
  - _Rules: OATM-BR-058_
  - _After: OATM-C06-T1_
- [ ] OATM-C06-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-060_
  - _Rules: OATM-BR-059_
  - _After: OATM-C06-T1_
- [ ] OATM-C06-T4 [api] Build the services behind the screens
  - OATM-BR-060: This is a layout defect in the legacy program: it writes the account through a layout that has no ZIP field, so the account group lands in the ZIP position and the group field gets filler. The new account record must keep ZIP and account group as separate named fields and save each confirmed value to its own field. The acceptance criterion above only records the legacy result for reconciliation. The business owner must decide whether to keep it before anyone treats it as required. Data migration should expect ZIP values on rewritten accounts that are really group IDs.
  - _Requirements: OATM-REQ-F-061_
  - _Rules: OATM-BR-060_
  - _After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3_
- [ ] OATM-C06-T5 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061_
  - _Rules: OATM-BR-058, OATM-BR-059, OATM-BR-060_
  - _After: OATM-C06-T2, OATM-C06-T3, OATM-C06-T4_
- [ ] OATM-C06-T6 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061_
  - _Criteria: OATM-C06-AC-01, OATM-C06-AC-02, OATM-C06-AC-03, OATM-C06-AC-04, OATM-C06-AC-05, OATM-C06-AC-06, OATM-C06-AC-07_
  - _After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3, OATM-C06-T4, OATM-C06-T5_
- [ ] OATM-C06-T7 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061_
  - _After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3, OATM-C06-T4, OATM-C06-T5_

## OATM-C07 Select an account to update (final)

- [ ] OATM-C07-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
- [ ] OATM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
  - _Rules: OATM-BR-062, OATM-BR-063, OATM-BR-064, OATM-BR-065, OATM-BR-066_
  - _After: OATM-C07-T1_
- [ ] OATM-C07-T3 [api] Build the services behind the screens
  - OATM-BR-061: Treat a blank or '*' account number as absent (null); otherwise use it as the search key. Validation then decides between 'No input received' and the 11-digit check.
  - _Requirements: OATM-REQ-F-062_
  - _Rules: OATM-BR-061_
  - _After: OATM-C07-T1, OATM-C07-T2_
- [ ] OATM-C07-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **lookup field** "Account number": Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched.
  - _Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
  - _Rules: OATM-BR-061, OATM-BR-062, OATM-BR-063, OATM-BR-064, OATM-BR-065, OATM-BR-066_
  - _After: OATM-C07-T2, OATM-C07-T3_
- [ ] OATM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
  - _Criteria: OATM-C07-AC-01, OATM-C07-AC-02, OATM-C07-AC-03, OATM-C07-AC-04, OATM-C07-AC-05, OATM-C07-AC-06, OATM-C07-AC-07, OATM-C07-AC-08, OATM-C07-AC-09, OATM-C07-AC-10, OATM-C07-AC-11_
  - _After: OATM-C07-T1, OATM-C07-T2, OATM-C07-T3, OATM-C07-T4_
- [ ] OATM-C07-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064, OATM-REQ-F-065, OATM-REQ-F-066, OATM-REQ-F-067_
  - _After: OATM-C07-T1, OATM-C07-T2, OATM-C07-T3, OATM-C07-T4_

## OATM-C08 Detect changes before validating (final)

- [ ] OATM-C08-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072_
- [ ] OATM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-072_
  - _Rules: OATM-BR-067, OATM-BR-068, OATM-BR-069, OATM-BR-070, OATM-BR-071, OATM-BR-073_
  - _After: OATM-C08-T1_
- [ ] OATM-C08-T3 [api] Build the services behind the screens
  - OATM-BR-072: Before validating, decide from the update stage and the change-detection result: if nothing changed, or the update is awaiting confirmation or already completed, clear all field-error flags and skip every field and date check. Validation is a step the server runs only when a change is detected while editing.
  - _Requirements: OATM-REQ-F-071_
  - _Rules: OATM-BR-072_
  - _After: OATM-C08-T1, OATM-C08-T2_
- [ ] OATM-C08-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Phone and payments": A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.').
  - **summary card** "Fix these before saving"
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072_
  - _Rules: OATM-BR-067, OATM-BR-068, OATM-BR-069, OATM-BR-070, OATM-BR-071, OATM-BR-072, OATM-BR-073_
  - _After: OATM-C08-T2, OATM-C08-T3_
- [ ] OATM-C08-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072_
  - _Criteria: OATM-C08-AC-01, OATM-C08-AC-02, OATM-C08-AC-03, OATM-C08-AC-04, OATM-C08-AC-05, OATM-C08-AC-06, OATM-C08-AC-07, OATM-C08-AC-08_
  - _After: OATM-C08-T1, OATM-C08-T2, OATM-C08-T3, OATM-C08-T4_
- [ ] OATM-C08-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072_
  - _After: OATM-C08-T1, OATM-C08-T2, OATM-C08-T3, OATM-C08-T4_

## OATM-C09 Validate customer name and address (final)

- [ ] OATM-C09-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-073, OATM-REQ-F-074, OATM-REQ-F-075, OATM-REQ-F-076, OATM-REQ-F-077, OATM-REQ-F-078, OATM-REQ-F-079, OATM-REQ-F-080, OATM-REQ-F-081_
- [ ] OATM-C09-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-074, OATM-REQ-F-075, OATM-REQ-F-076, OATM-REQ-F-077, OATM-REQ-F-078, OATM-REQ-F-079, OATM-REQ-F-080, OATM-REQ-F-081_
  - _Rules: OATM-BR-076, OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-080, OATM-BR-081, OATM-BR-082, OATM-BR-083, OATM-BR-084_
  - _After: OATM-C09-T1_
- [ ] OATM-C09-T3 [api] Build the services behind the screens
  - OATM-BR-074: Treat blank or '*' entries for first, middle and last name, address lines 1 and 2, city and EFT account id as absent (null); otherwise they are the proposed values. The city goes into the customer's third address line, so map the City field to that address field.
  - OATM-BR-075: Treat blank or '*' state and ZIP entries as absent (empty); otherwise keep the entered value for the state-code, ZIP and state/ZIP-prefix checks. Those checks need reference tables of valid US state codes and of valid state plus two-digit ZIP prefix combinations.
  - _Requirements: OATM-REQ-F-073_
  - _Rules: OATM-BR-074, OATM-BR-075_
  - _After: OATM-C09-T1, OATM-C09-T2_
- [ ] OATM-C09-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Name and address": '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together.
  - **summary card** "Phone and payments": A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.').
  - _Requirements: OATM-REQ-F-073, OATM-REQ-F-074, OATM-REQ-F-075, OATM-REQ-F-076, OATM-REQ-F-077, OATM-REQ-F-078, OATM-REQ-F-079, OATM-REQ-F-080, OATM-REQ-F-081_
  - _Rules: OATM-BR-074, OATM-BR-075, OATM-BR-076, OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-080, OATM-BR-081, OATM-BR-082, OATM-BR-083, OATM-BR-084_
  - _After: OATM-C09-T2, OATM-C09-T3_
- [ ] OATM-C09-T5 [test-generation] Write a test for every acceptance criterion
  - 16 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-073, OATM-REQ-F-074, OATM-REQ-F-075, OATM-REQ-F-076, OATM-REQ-F-077, OATM-REQ-F-078, OATM-REQ-F-079, OATM-REQ-F-080, OATM-REQ-F-081_
  - _Criteria: OATM-C09-AC-01, OATM-C09-AC-02, OATM-C09-AC-03, OATM-C09-AC-04, OATM-C09-AC-05, OATM-C09-AC-06, OATM-C09-AC-07, OATM-C09-AC-08, OATM-C09-AC-09, OATM-C09-AC-10, OATM-C09-AC-11, OATM-C09-AC-12, OATM-C09-AC-13, OATM-C09-AC-14, OATM-C09-AC-15, OATM-C09-AC-16_
  - _After: OATM-C09-T1, OATM-C09-T2, OATM-C09-T3, OATM-C09-T4_
- [ ] OATM-C09-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-073, OATM-REQ-F-074, OATM-REQ-F-075, OATM-REQ-F-076, OATM-REQ-F-077, OATM-REQ-F-078, OATM-REQ-F-079, OATM-REQ-F-080, OATM-REQ-F-081_
  - _After: OATM-C09-T1, OATM-C09-T2, OATM-C09-T3, OATM-C09-T4_

## OATM-C10 Validate customer phone numbers (final)

- [ ] OATM-C10-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094_
- [ ] OATM-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093_
  - _Rules: OATM-BR-086, OATM-BR-087, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094, OATM-BR-095, OATM-BR-096, OATM-BR-097_
  - _After: OATM-C10-T1_
- [ ] OATM-C10-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-094_
  - _Rules: OATM-BR-073_
  - _After: OATM-C10-T1_
- [ ] OATM-C10-T4 [api] Build the services behind the screens
  - OATM-BR-085: Capture phone numbers 1 and 2 as three optional parts each (area code, prefix, line number). Blank or '*' parts are absent before validation, so a phone with all parts absent counts as omitted. Area-code validation needs a reference list of the North American general-purpose area codes.
  - _Requirements: OATM-REQ-F-082_
  - _Rules: OATM-BR-085_
  - _After: OATM-C10-T1, OATM-C10-T2, OATM-C10-T3_
- [ ] OATM-C10-T5 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Phone and payments": A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.').
  - _Requirements: OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094_
  - _Rules: OATM-BR-073, OATM-BR-085, OATM-BR-086, OATM-BR-087, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094, OATM-BR-095, OATM-BR-096, OATM-BR-097_
  - _After: OATM-C10-T2, OATM-C10-T3, OATM-C10-T4_
- [ ] OATM-C10-T6 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094_
  - _Criteria: OATM-C10-AC-01, OATM-C10-AC-02, OATM-C10-AC-03, OATM-C10-AC-04, OATM-C10-AC-05, OATM-C10-AC-06, OATM-C10-AC-07, OATM-C10-AC-08, OATM-C10-AC-09, OATM-C10-AC-10, OATM-C10-AC-11, OATM-C10-AC-12, OATM-C10-AC-13_
  - _After: OATM-C10-T1, OATM-C10-T2, OATM-C10-T3, OATM-C10-T4, OATM-C10-T5_
- [ ] OATM-C10-T7 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094_
  - _After: OATM-C10-T1, OATM-C10-T2, OATM-C10-T3, OATM-C10-T4, OATM-C10-T5_

## OATM-C11 Validate identity and credit details (final)

- [ ] OATM-C11-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
- [ ] OATM-C11-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _Rules: OATM-BR-099, OATM-BR-100, OATM-BR-101, OATM-BR-102, OATM-BR-103, OATM-BR-104, OATM-BR-105, OATM-BR-106_
  - _After: OATM-C11-T1_
- [ ] OATM-C11-T3 [api] Build the services behind the screens
  - OATM-BR-098: Capture the SSN as three optional parts (3, 2 and 4 characters). Blank or '*' parts are absent; others are kept as typed for the supplied, numeric, non-zero and forbidden-range checks. The SSN is sensitive personal data: mask it on screen and in logs, and protect it in storage.
  - _Requirements: OATM-REQ-F-095_
  - _Rules: OATM-BR-098_
  - _After: OATM-C11-T1, OATM-C11-T2_
- [ ] OATM-C11-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Customer identity": SSN: 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.', 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'; the 4th & 5th and last 4 characters must each be supplied, all numeric and non-zero. Date of birth: the date checks above, and 'Date of Birth:cannot be in the future '. FICO: 'FICO Score must be supplied.', 'FICO Score must be all numeric.', 'FICO Score must not be zero.', 'FICO Score: should be between 300 and 850'.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _Rules: OATM-BR-098, OATM-BR-099, OATM-BR-100, OATM-BR-101, OATM-BR-102, OATM-BR-103, OATM-BR-104, OATM-BR-105, OATM-BR-106_
  - _After: OATM-C11-T2, OATM-C11-T3_
- [ ] OATM-C11-T5 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _Criteria: OATM-C11-AC-01, OATM-C11-AC-02, OATM-C11-AC-03, OATM-C11-AC-04, OATM-C11-AC-05, OATM-C11-AC-06, OATM-C11-AC-07, OATM-C11-AC-08, OATM-C11-AC-09, OATM-C11-AC-10, OATM-C11-AC-11, OATM-C11-AC-12_
  - _After: OATM-C11-T1, OATM-C11-T2, OATM-C11-T3, OATM-C11-T4_
- [ ] OATM-C11-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102_
  - _After: OATM-C11-T1, OATM-C11-T2, OATM-C11-T3, OATM-C11-T4_

## OATM-C12 Validate account flags and EFT account (final)

- [ ] OATM-C12-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
- [ ] OATM-C12-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
  - _Rules: OATM-BR-074, OATM-BR-082, OATM-BR-087, OATM-BR-108, OATM-BR-109_
  - _After: OATM-C12-T1_
- [ ] OATM-C12-T3 [api] Build the services behind the screens
  - OATM-BR-107: Treat blank or '*' entries for Account Status and Primary Card Holder as absent (null), never as a value to save. Validation then rejects an absent or non-Y/N value. Store each flag as a two-valued field (Y/N or boolean).
  - OATM-BR-074: Treat a blank or '*' EFT account id as absent (null); otherwise it is the proposed value for the 10-digit supplied, numeric and non-zero checks. Store it as a 10-character digit string so leading zeros are kept.
  - _Requirements: OATM-REQ-F-103_
  - _Rules: OATM-BR-107_
  - _After: OATM-C12-T1, OATM-C12-T2_
- [ ] OATM-C12-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Name and address": '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together.
  - **summary card** "Phone and payments": A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.').
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
  - _Rules: OATM-BR-074, OATM-BR-082, OATM-BR-087, OATM-BR-107, OATM-BR-108, OATM-BR-109_
  - _After: OATM-C12-T2, OATM-C12-T3_
- [ ] OATM-C12-T5 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
  - _Criteria: OATM-C12-AC-01, OATM-C12-AC-02, OATM-C12-AC-03, OATM-C12-AC-04, OATM-C12-AC-05_
  - _After: OATM-C12-T1, OATM-C12-T2, OATM-C12-T3, OATM-C12-T4_
- [ ] OATM-C12-T6 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105, OATM-REQ-F-106_
  - _After: OATM-C12-T1, OATM-C12-T2, OATM-C12-T3, OATM-C12-T4_

## OATM-C13 Save confirmed account and customer changes (final)

- [ ] OATM-C13-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-109, OATM-REQ-F-110, OATM-REQ-F-111, OATM-REQ-N-004, OATM-REQ-F-112, OATM-REQ-F-113_
- [ ] OATM-C13-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-109, OATM-REQ-F-111_
  - _Rules: OATM-BR-111, OATM-BR-113_
  - _After: OATM-C13-T1_
- [ ] OATM-C13-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-110, OATM-REQ-N-004, OATM-REQ-F-113, OATM-REQ-F-112_
  - _Rules: OATM-BR-110, OATM-BR-112, OATM-BR-114, OATM-BR-115, OATM-BR-116_
  - _After: OATM-C13-T1_
- [ ] OATM-C13-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-109, OATM-REQ-F-110, OATM-REQ-F-111, OATM-REQ-N-004, OATM-REQ-F-112, OATM-REQ-F-113_
  - _Rules: OATM-BR-110, OATM-BR-111, OATM-BR-112, OATM-BR-113, OATM-BR-114, OATM-BR-115, OATM-BR-116_
  - _After: OATM-C13-T2, OATM-C13-T3_
- [ ] OATM-C13-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-109, OATM-REQ-F-110, OATM-REQ-F-111, OATM-REQ-N-004, OATM-REQ-F-112, OATM-REQ-F-113_
  - _Criteria: OATM-C13-AC-01, OATM-C13-AC-02, OATM-C13-AC-03, OATM-C13-AC-04, OATM-C13-AC-05, OATM-C13-AC-06, OATM-C13-AC-07, OATM-C13-AC-08_
  - _After: OATM-C13-T1, OATM-C13-T2, OATM-C13-T3, OATM-C13-T4_
- [ ] OATM-C13-T6 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-109, OATM-REQ-F-110, OATM-REQ-F-111, OATM-REQ-N-004, OATM-REQ-F-112, OATM-REQ-F-113_
  - _After: OATM-C13-T1, OATM-C13-T2, OATM-C13-T3, OATM-C13-T4_

## OATM-C14 Navigate the account update screen (final)

- [ ] OATM-C14-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-114, OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
- [ ] OATM-C14-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
  - _Rules: OATM-BR-118, OATM-BR-119, OATM-BR-120_
  - _After: OATM-C14-T1_
- [ ] OATM-C14-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-114_
  - _Rules: OATM-BR-117_
  - _After: OATM-C14-T1_
- [ ] OATM-C14-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **lookup field** "Account number": Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched.
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-114, OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
  - _Rules: OATM-BR-117, OATM-BR-118, OATM-BR-119, OATM-BR-120_
  - _After: OATM-C14-T2, OATM-C14-T3_
- [ ] OATM-C14-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **primary button** "Update account"
  - _Requirements: OATM-REQ-F-114_
  - _Rules: OATM-BR-117_
  - _After: OATM-C14-T2, OATM-C14-T3_
- [ ] OATM-C14-T6 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-114, OATM-REQ-F-115, OATM-REQ-F-116, OATM-REQ-F-117_
  - _Criteria: OATM-C14-AC-01, OATM-C14-AC-02, OATM-C14-AC-03, OATM-C14-AC-04, OATM-C14-AC-05, OATM-C14-AC-06_
  - _After: OATM-C14-T1, OATM-C14-T2, OATM-C14-T3, OATM-C14-T4, OATM-C14-T5_

## OATM-C15 Update account details with validation and confirmation (final)

- [ ] OATM-C15-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121, OATM-REQ-F-122_
- [ ] OATM-C15-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121_
  - _Rules: OATM-BR-121, OATM-BR-122, OATM-BR-123, OATM-BR-124_
  - _After: OATM-C15-T1_
- [ ] OATM-C15-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-122_
  - _Rules: OATM-BR-125_
  - _After: OATM-C15-T1_
- [ ] OATM-C15-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Name and address": '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together.
  - **summary card** "Fix these before saving"
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121, OATM-REQ-F-122_
  - _Rules: OATM-BR-121, OATM-BR-122, OATM-BR-123, OATM-BR-124, OATM-BR-125_
  - _After: OATM-C15-T2, OATM-C15-T3_
- [ ] OATM-C15-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121, OATM-REQ-F-122_
  - _Criteria: OATM-C15-AC-01, OATM-C15-AC-02, OATM-C15-AC-03, OATM-C15-AC-04, OATM-C15-AC-05, OATM-C15-AC-06, OATM-C15-AC-07_
  - _After: OATM-C15-T1, OATM-C15-T2, OATM-C15-T3, OATM-C15-T4_

## OATM-C16 Validate and look up an account for viewing (final)

- [ ] OATM-C16-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-130, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-133, OATM-REQ-F-134, OATM-REQ-F-135, OATM-REQ-F-136_
- [ ] OATM-C16-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-128, OATM-REQ-F-136_
  - _Rules: OATM-BR-126, OATM-BR-127, OATM-BR-128, OATM-BR-129, OATM-BR-131, OATM-BR-139_
  - _After: OATM-C16-T1_
- [ ] OATM-C16-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-129, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-134, OATM-REQ-F-135_
  - _Rules: OATM-BR-132, OATM-BR-134, OATM-BR-135, OATM-BR-137, OATM-BR-138_
  - _After: OATM-C16-T1_
- [ ] OATM-C16-T4 [api] Build the services behind the screens
  - OATM-BR-130: Needs a lookup of the card-to-account link by account number (a secondary index or query on account ID). When a link is found, the customer number and card number it holds are kept in the user's session for the rest of the interaction and used by the later customer lookup.
  - OATM-BR-133: Needs a read of the account by its 11-digit account number, which is the primary key. A successful read sets an 'account found' flag that tells the view to show the account's financial details.
  - OATM-BR-136: Needs a read of the customer by the customer number taken from the card-to-account link, not from anything the user typed. A successful read sets a 'customer found' flag that tells the view to show the customer details.
  - _Requirements: OATM-REQ-F-127, OATM-REQ-F-130, OATM-REQ-F-133_
  - _Rules: OATM-BR-130, OATM-BR-133, OATM-BR-136_
  - _After: OATM-C16-T1, OATM-C16-T2, OATM-C16-T3_
- [ ] OATM-C16-T5 [ui-modernization] Build the screen Account (S-ACCOUNT-VIEW)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-VIEW.
  - **lookup field** "Account or card number": Blank: 'No input received' - enter an account number (11 digits) or a card number (16 digits). Not digits, wrong length or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number' (or a 16-digit card number). Not in the card cross-reference: 'Account:<number> not found in Cross ref file.' - check the number with the caller. The error shows under the field.
  - _Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-130, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-133, OATM-REQ-F-134, OATM-REQ-F-135, OATM-REQ-F-136_
  - _Rules: OATM-BR-126, OATM-BR-127, OATM-BR-128, OATM-BR-129, OATM-BR-130, OATM-BR-131, OATM-BR-132, OATM-BR-133, OATM-BR-134, OATM-BR-135, OATM-BR-136, OATM-BR-137, OATM-BR-138, OATM-BR-139_
  - _After: OATM-C16-T2, OATM-C16-T3, OATM-C16-T4_
- [ ] OATM-C16-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **lookup field** "Find account (account or card number)": Same checks as the account search on S-ACCOUNT-VIEW; an empty search says 'No input received' - enter an account number (11 digits) or a card number (16 digits).
  - _Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126_
  - _Rules: OATM-BR-126, OATM-BR-127, OATM-BR-128, OATM-BR-129_
  - _After: OATM-C16-T2, OATM-C16-T3, OATM-C16-T4_
- [ ] OATM-C16-T7 [test-generation] Write a test for every acceptance criterion
  - 18 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-130, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-133, OATM-REQ-F-134, OATM-REQ-F-135, OATM-REQ-F-136_
  - _Criteria: OATM-C16-AC-01, OATM-C16-AC-02, OATM-C16-AC-03, OATM-C16-AC-04, OATM-C16-AC-05, OATM-C16-AC-06, OATM-C16-AC-07, OATM-C16-AC-08, OATM-C16-AC-09, OATM-C16-AC-10, OATM-C16-AC-11, OATM-C16-AC-12, OATM-C16-AC-13, OATM-C16-AC-14, OATM-C16-AC-15, OATM-C16-AC-16, OATM-C16-AC-17, OATM-C16-AC-18_
  - _After: OATM-C16-T1, OATM-C16-T2, OATM-C16-T3, OATM-C16-T4, OATM-C16-T5, OATM-C16-T6_
- [ ] OATM-C16-T8 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-123, OATM-REQ-F-124, OATM-REQ-F-125, OATM-REQ-F-126, OATM-REQ-F-127, OATM-REQ-F-128, OATM-REQ-F-129, OATM-REQ-F-130, OATM-REQ-F-131, OATM-REQ-F-132, OATM-REQ-F-133, OATM-REQ-F-134, OATM-REQ-F-135, OATM-REQ-F-136_
  - _After: OATM-C16-T1, OATM-C16-T2, OATM-C16-T3, OATM-C16-T4, OATM-C16-T5, OATM-C16-T6_

## OATM-C17 Display account and customer details (final)

- [ ] OATM-C17-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
- [ ] OATM-C17-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-N-005_
  - _Rules: OATM-BR-141, OATM-BR-143_
  - _After: OATM-C17-T1_
- [ ] OATM-C17-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
  - _Rules: OATM-BR-140, OATM-BR-141, OATM-BR-142, OATM-BR-144, OATM-BR-145, OATM-BR-146, OATM-BR-147_
  - _After: OATM-C17-T1_
- [ ] OATM-C17-T4 [ui-modernization] Build the screen Account (S-ACCOUNT-VIEW)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-VIEW.
  - **lookup field** "Account or card number": Blank: 'No input received' - enter an account number (11 digits) or a card number (16 digits). Not digits, wrong length or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number' (or a 16-digit card number). Not in the card cross-reference: 'Account:<number> not found in Cross ref file.' - check the number with the caller. The error shows under the field.
  - **status badge** "Account status"
  - **summary card** "Account"
  - **summary card** "Customer"
  - **summary card** "Address and phone"
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
  - _Rules: OATM-BR-140, OATM-BR-141, OATM-BR-142, OATM-BR-143, OATM-BR-144, OATM-BR-145, OATM-BR-146, OATM-BR-147_
  - _After: OATM-C17-T2, OATM-C17-T3_
- [ ] OATM-C17-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
  - _Criteria: OATM-C17-AC-01, OATM-C17-AC-02, OATM-C17-AC-03, OATM-C17-AC-04, OATM-C17-AC-05, OATM-C17-AC-06, OATM-C17-AC-07, OATM-C17-AC-08, OATM-C17-AC-09, OATM-C17-AC-10, OATM-C17-AC-11_
  - _After: OATM-C17-T1, OATM-C17-T2, OATM-C17-T3, OATM-C17-T4_
- [ ] OATM-C17-T6 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
  - _After: OATM-C17-T1, OATM-C17-T2, OATM-C17-T3, OATM-C17-T4_

## OATM-C18 Navigate the account view screen (final)

- [ ] OATM-C18-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: OATM-REQ-F-143, OATM-REQ-F-144, OATM-REQ-F-145, OATM-REQ-F-146, OATM-REQ-F-147, OATM-REQ-F-148_
- [ ] OATM-C18-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-143, OATM-REQ-F-144, OATM-REQ-F-146_
  - _Rules: OATM-BR-148, OATM-BR-149, OATM-BR-151_
  - _After: OATM-C18-T1_
- [ ] OATM-C18-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-148_
  - _Rules: OATM-BR-153_
  - _After: OATM-C18-T1_
- [ ] OATM-C18-T4 [api] Build the services behind the screens
  - OATM-BR-150: When the view is opened with no session state, or opened from the main menu as a new visit, the application must create a new, empty view state and discard any data handed over by the previous screen. Only an explicit re-entry from the same view may reuse existing state.
  - OATM-BR-152: The view is a request/response interaction that keeps its state between requests. Every time the screen is returned, the session must be marked as 're-entry' and the entered account number and lookup results kept, so that the user's next submission is handled as a continuation of the same Account View interaction.
  - _Requirements: OATM-REQ-F-145, OATM-REQ-F-147_
  - _Rules: OATM-BR-150, OATM-BR-152_
  - _After: OATM-C18-T1, OATM-C18-T2, OATM-C18-T3_
- [ ] OATM-C18-T5 [ui-modernization] Build the screen Account (S-ACCOUNT-VIEW)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-VIEW.
  - **lookup field** "Account or card number": Blank: 'No input received' - enter an account number (11 digits) or a card number (16 digits). Not digits, wrong length or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number' (or a 16-digit card number). Not in the card cross-reference: 'Account:<number> not found in Cross ref file.' - check the number with the caller. The error shows under the field.
  - _Requirements: OATM-REQ-F-143, OATM-REQ-F-146_
  - _Rules: OATM-BR-148, OATM-BR-151_
  - _After: OATM-C18-T2, OATM-C18-T3, OATM-C18-T4_
- [ ] OATM-C18-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **primary button** "Account"
  - _Requirements: OATM-REQ-F-144, OATM-REQ-F-145_
  - _Rules: OATM-BR-149, OATM-BR-150_
  - _After: OATM-C18-T2, OATM-C18-T3, OATM-C18-T4_
- [ ] OATM-C18-T7 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-143, OATM-REQ-F-144, OATM-REQ-F-145, OATM-REQ-F-146, OATM-REQ-F-147, OATM-REQ-F-148_
  - _Criteria: OATM-C18-AC-01, OATM-C18-AC-02, OATM-C18-AC-03, OATM-C18-AC-04, OATM-C18-AC-05, OATM-C18-AC-06, OATM-C18-AC-07, OATM-C18-AC-08_
  - _After: OATM-C18-T1, OATM-C18-T2, OATM-C18-T3, OATM-C18-T4, OATM-C18-T5, OATM-C18-T6_

## OATM-C19 Request a bill payment (final)

- [ ] OATM-C19-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-N-006, OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-151, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159_
- [ ] OATM-C19-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-N-006, OATM-REQ-F-150, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159_
  - _Rules: OATM-BR-154, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-161, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165_
  - _After: OATM-C19-T1_
- [ ] OATM-C19-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-149, OATM-REQ-F-151, OATM-REQ-F-152_
  - _Rules: OATM-BR-155, OATM-BR-157, OATM-BR-158_
  - _After: OATM-C19-T1_
- [ ] OATM-C19-T4 [ui-modernization] Build the screen Pay balance (S-BILL-PAY)
  - To the prototype: ui-reference/index.html#/S-BILL-PAY.
  - **lookup field** "Account number": Blank: 'Acct ID can NOT be empty...' - enter the 11-digit account number. Not found: 'Account ID NOT found...' - check the number with the caller.
  - **summary card** "Balance to pay": When the balance is zero or less: 'You have nothing to pay...' and Pay balance is unavailable.
  - **primary button** "Pay balance": The dialog offers only Pay or Cancel, so no other value can be entered (legacy: 'Invalid value. Valid values are (Y/N)...'). If the card linked to the account is not found, nothing is paid and the message says so. The payment and the balance change are saved together or not at all.
  - _Requirements: OATM-REQ-N-006, OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159_
  - _Rules: OATM-BR-154, OATM-BR-155, OATM-BR-156, OATM-BR-158, OATM-BR-159, OATM-BR-160, OATM-BR-161, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165_
  - _After: OATM-C19-T2, OATM-C19-T3_
- [ ] OATM-C19-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Pay balance"
  - _Requirements: OATM-REQ-N-006, OATM-REQ-F-150, OATM-REQ-F-151_
  - _Rules: OATM-BR-154, OATM-BR-156, OATM-BR-157_
  - _After: OATM-C19-T2, OATM-C19-T3_
- [ ] OATM-C19-T6 [test-generation] Write a test for every acceptance criterion
  - 16 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-N-006, OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-151, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159_
  - _Criteria: OATM-C19-AC-01, OATM-C19-AC-02, OATM-C19-AC-03, OATM-C19-AC-04, OATM-C19-AC-05, OATM-C19-AC-06, OATM-C19-AC-07, OATM-C19-AC-08, OATM-C19-AC-09, OATM-C19-AC-10, OATM-C19-AC-11, OATM-C19-AC-12, OATM-C19-AC-13, OATM-C19-AC-14, OATM-C19-AC-15, OATM-C19-AC-16_
  - _After: OATM-C19-T1, OATM-C19-T2, OATM-C19-T3, OATM-C19-T4, OATM-C19-T5_
- [ ] OATM-C19-T7 [compliance] Review the handling of money, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-N-006, OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-151, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159_
  - _After: OATM-C19-T1, OATM-C19-T2, OATM-C19-T3, OATM-C19-T4, OATM-C19-T5_

## OATM-C20 Post a full-balance bill payment (final)

- [ ] OATM-C20-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170_
- [ ] OATM-C20-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-162, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166_
  - _Rules: OATM-BR-166, OATM-BR-168, OATM-BR-170, OATM-BR-171, OATM-BR-172, OATM-BR-173, OATM-BR-174_
  - _After: OATM-C20-T1_
- [ ] OATM-C20-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-163, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170, OATM-REQ-F-167_
  - _Rules: OATM-BR-169, OATM-BR-175, OATM-BR-176, OATM-BR-177, OATM-BR-178_
  - _After: OATM-C20-T1_
- [ ] OATM-C20-T4 [api] Build the services behind the screens
  - OATM-BR-167: Needs the highest existing transaction ID, taken as the last key in transaction-ID order (equivalent to a max query over transactions), so the new payment can be numbered one higher. Because two payments could otherwise get the same number, the new application should allocate IDs safely under concurrency, for example with a database sequence or a locked read of the max. It must still treat an empty transaction store as ID 0.
  - OATM-BR-174: After the payment transaction is written, the account read earlier for update must be saved with its current balance reduced by the payment amount. This needs a locked or version-checked update of that account by account ID, so that no change made in between is overwritten.
  - _Requirements: OATM-REQ-F-161_
  - _Rules: OATM-BR-167_
  - _After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3_
- [ ] OATM-C20-T5 [ui-modernization] Build the screen Pay balance (S-BILL-PAY)
  - To the prototype: ui-reference/index.html#/S-BILL-PAY.
  - **summary card** "Balance to pay": When the balance is zero or less: 'You have nothing to pay...' and Pay balance is unavailable.
  - **primary button** "Pay balance": The dialog offers only Pay or Cancel, so no other value can be entered (legacy: 'Invalid value. Valid values are (Y/N)...'). If the card linked to the account is not found, nothing is paid and the message says so. The payment and the balance change are saved together or not at all.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170_
  - _Rules: OATM-BR-166, OATM-BR-167, OATM-BR-168, OATM-BR-169, OATM-BR-170, OATM-BR-171, OATM-BR-172, OATM-BR-173, OATM-BR-174, OATM-BR-175, OATM-BR-176, OATM-BR-177, OATM-BR-178_
  - _After: OATM-C20-T2, OATM-C20-T3, OATM-C20-T4_
- [ ] OATM-C20-T6 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170_
  - _Criteria: OATM-C20-AC-01, OATM-C20-AC-02, OATM-C20-AC-03, OATM-C20-AC-04, OATM-C20-AC-05, OATM-C20-AC-06, OATM-C20-AC-07, OATM-C20-AC-08, OATM-C20-AC-09, OATM-C20-AC-10, OATM-C20-AC-11, OATM-C20-AC-12, OATM-C20-AC-13, OATM-C20-AC-14, OATM-C20-AC-15_
  - _After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3, OATM-C20-T4, OATM-C20-T5_
- [ ] OATM-C20-T7 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170_
  - _After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3, OATM-C20-T4, OATM-C20-T5_

## OATM-C21 Set report period for transaction reports (final)

- [ ] OATM-C21-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
  - _Requirements: OATM-REQ-F-171, OATM-REQ-F-172_
- [ ] OATM-C21-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-171, OATM-REQ-F-172_
  - _Rules: OATM-BR-179, OATM-BR-180_
  - _After: OATM-C21-T1_
- [ ] OATM-C21-T3 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **summary card** "Report type": None chosen: 'Select a report type to print report...' - choose Monthly, Yearly or Custom.
  - _Requirements: OATM-REQ-F-171, OATM-REQ-F-172_
  - _Rules: OATM-BR-179, OATM-BR-180_
  - _After: OATM-C21-T2_
- [ ] OATM-C21-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-171, OATM-REQ-F-172_
  - _Criteria: OATM-C21-AC-01, OATM-C21-AC-02, OATM-C21-AC-03_
  - _After: OATM-C21-T1, OATM-C21-T2, OATM-C21-T3_

## OATM-C22 Reach and move around the transaction report screen (final)

- [ ] OATM-C22-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176_
- [ ] OATM-C22-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-175, OATM-REQ-F-176_
  - _Rules: OATM-BR-181, OATM-BR-184, OATM-BR-185_
  - _After: OATM-C22-T1_
- [ ] OATM-C22-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-173, OATM-REQ-F-174_
  - _Rules: OATM-BR-182, OATM-BR-183_
  - _After: OATM-C22-T1_
- [ ] OATM-C22-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **primary button** "Submit report": The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-175, OATM-REQ-F-176_
  - _Rules: OATM-BR-181, OATM-BR-184, OATM-BR-185_
  - _After: OATM-C22-T2, OATM-C22-T3_
- [ ] OATM-C22-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Transaction reports"
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174_
  - _Rules: OATM-BR-181, OATM-BR-182, OATM-BR-183_
  - _After: OATM-C22-T2, OATM-C22-T3_
- [ ] OATM-C22-T6 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176_
  - _Criteria: OATM-C22-AC-01, OATM-C22-AC-02, OATM-C22-AC-03, OATM-C22-AC-04, OATM-C22-AC-05_
  - _After: OATM-C22-T1, OATM-C22-T2, OATM-C22-T3, OATM-C22-T4, OATM-C22-T5_
- [ ] OATM-C22-T7 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176_
  - _After: OATM-C22-T1, OATM-C22-T2, OATM-C22-T3, OATM-C22-T4, OATM-C22-T5_

## OATM-C23 Choose a report type and a valid custom period (final)

- [ ] OATM-C23-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
  - _Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186_
- [ ] OATM-C23-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186_
  - _Rules: OATM-BR-186, OATM-BR-187, OATM-BR-188, OATM-BR-190, OATM-BR-191, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195_
  - _After: OATM-C23-T1_
- [ ] OATM-C23-T3 [api] Build the services behind the screens
  - OATM-BR-189: Before validating, normalise the custom date inputs: pad month and day to two digits (for example '3' becomes '03') and year to four digits, so that the range checks and the calendar-date check see a consistent YYYY-MM-DD value. A typed date input or a date-parsing library in the new application can do this step.
  - _Requirements: OATM-REQ-F-180_
  - _Rules: OATM-BR-189_
  - _After: OATM-C23-T1, OATM-C23-T2_
- [ ] OATM-C23-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **summary card** "Report type": None chosen: 'Select a report type to print report...' - choose Monthly, Yearly or Custom.
  - **summary card** "Custom period": Every part is required, checked start month, day, year then end month, day, year ('Start Date - Month can NOT be empty...' and so on). 'Start Date - Not a valid Month...' / 'End Date - Not a valid Month...' (1 to 12); 'Start Date - Not a valid Day...' / 'End Date - Not a valid Day...' (1 to 31); 'Start Date - Not a valid Year...' / 'End Date - Not a valid Year...'; 'Start Date - Not a valid date...' / 'End Date - Not a valid date...' for a date not on the calendar. The message sits under the part to fix.
  - _Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186_
  - _Rules: OATM-BR-186, OATM-BR-187, OATM-BR-188, OATM-BR-189, OATM-BR-190, OATM-BR-191, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195_
  - _After: OATM-C23-T2, OATM-C23-T3_
- [ ] OATM-C23-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186_
  - _Criteria: OATM-C23-AC-01, OATM-C23-AC-02, OATM-C23-AC-03, OATM-C23-AC-04, OATM-C23-AC-05, OATM-C23-AC-06, OATM-C23-AC-07, OATM-C23-AC-08, OATM-C23-AC-09, OATM-C23-AC-10, OATM-C23-AC-11, OATM-C23-AC-12, OATM-C23-AC-13_
  - _After: OATM-C23-T1, OATM-C23-T2, OATM-C23-T3, OATM-C23-T4_

## OATM-C24 Confirm and submit a transaction report for printing (final)

- [ ] OATM-C24-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
  - _Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-191, OATM-REQ-F-192, OATM-REQ-F-193, OATM-REQ-F-194_
- [ ] OATM-C24-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-192_
  - _Rules: OATM-BR-196, OATM-BR-197, OATM-BR-198, OATM-BR-199, OATM-BR-201_
  - _After: OATM-C24-T1_
- [ ] OATM-C24-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-193, OATM-REQ-F-194_
  - _Rules: OATM-BR-202, OATM-BR-203, OATM-BR-204_
  - _After: OATM-C24-T1_
- [ ] OATM-C24-T4 [api] Build the services behind the screens
  - OATM-BR-200: The report job takes its period as two parameters, a start date and an end date, each in YYYY-MM-DD form. In the legacy job these are also passed together as the single string 'YYYY-MM-DD YYYY-MM-DD'. The new application should send these as typed parameters on the request it submits to the scheduled or queued transaction-report job, so that the batch run filters transactions to exactly that inclusive range.
  - _Requirements: OATM-REQ-F-191_
  - _Rules: OATM-BR-200_
  - _After: OATM-C24-T1, OATM-C24-T2, OATM-C24-T3_
- [ ] OATM-C24-T5 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **primary button** "Submit report": The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again.
  - _Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-191, OATM-REQ-F-192, OATM-REQ-F-193, OATM-REQ-F-194_
  - _Rules: OATM-BR-196, OATM-BR-197, OATM-BR-198, OATM-BR-199, OATM-BR-200, OATM-BR-201, OATM-BR-202, OATM-BR-203, OATM-BR-204_
  - _After: OATM-C24-T2, OATM-C24-T3, OATM-C24-T4_
- [ ] OATM-C24-T6 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-191, OATM-REQ-F-192, OATM-REQ-F-193, OATM-REQ-F-194_
  - _Criteria: OATM-C24-AC-01, OATM-C24-AC-02, OATM-C24-AC-03, OATM-C24-AC-04, OATM-C24-AC-05, OATM-C24-AC-06, OATM-C24-AC-07, OATM-C24-AC-08, OATM-C24-AC-09_
  - _After: OATM-C24-T1, OATM-C24-T2, OATM-C24-T3, OATM-C24-T4, OATM-C24-T5_

## OATM-C25 Browse and page through the transaction list (final)

- [ ] OATM-C25-T1 [data] Model the data the capability reads and writes
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-F-195, OATM-REQ-F-196, OATM-REQ-F-197, OATM-REQ-F-198, OATM-REQ-F-199, OATM-REQ-F-200, OATM-REQ-F-201, OATM-REQ-F-202, OATM-REQ-F-203, OATM-REQ-F-204, OATM-REQ-F-205, OATM-REQ-F-206, OATM-REQ-F-207, OATM-REQ-F-208, OATM-REQ-F-209, OATM-REQ-F-210, OATM-REQ-F-211, OATM-REQ-F-212, OATM-REQ-F-213, OATM-REQ-F-214, OATM-REQ-F-215, OATM-REQ-F-216, OATM-REQ-F-217, OATM-REQ-F-218, OATM-REQ-F-219_
- [ ] OATM-C25-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-195, OATM-REQ-F-197, OATM-REQ-F-198, OATM-REQ-F-199, OATM-REQ-F-200, OATM-REQ-F-201, OATM-REQ-F-203, OATM-REQ-F-208, OATM-REQ-F-209, OATM-REQ-F-212, OATM-REQ-F-214, OATM-REQ-F-218_
  - _Rules: OATM-BR-205, OATM-BR-207, OATM-BR-208, OATM-BR-209, OATM-BR-210, OATM-BR-211, OATM-BR-213, OATM-BR-218, OATM-BR-219, OATM-BR-222, OATM-BR-224, OATM-BR-228_
  - _After: OATM-C25-T1_
- [ ] OATM-C25-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-211, OATM-REQ-F-219, OATM-REQ-F-202, OATM-REQ-F-204, OATM-REQ-F-205, OATM-REQ-F-210, OATM-REQ-F-213, OATM-REQ-F-215, OATM-REQ-F-217_
  - _Rules: OATM-BR-212, OATM-BR-214, OATM-BR-215, OATM-BR-220, OATM-BR-221, OATM-BR-223, OATM-BR-225, OATM-BR-227, OATM-BR-229_
  - _After: OATM-C25-T1_
- [ ] OATM-C25-T4 [api] Build the services behind the screens
  - OATM-BR-206: Each request to the list starts from a clean screen state: no leftover message, error, end-of-list or next-page flags, and focus on the Tran ID filter. In a modern UI this is just rendering the list view fresh per request rather than carrying flags between requests.
  - OATM-BR-216: The page needs to keep the IDs of its first and last rows (in the page response or a cursor token) so the next request can page backward from the first ID. A keyset/cursor query on transaction ID does this; offset paging would not match the legacy behaviour.
  - OATM-BR-217: The ID of the tenth row is the forward cursor: the next-page query reads transactions with ID greater than it, in ascending ID order, limit 10 (plus one look-ahead row to know whether another page exists).
  - OATM-BR-226: The previous-page query reads transactions with ID strictly less than the current page's first ID, in descending order, limit 10 (plus one look-ahead), and reverses them for display, so the current first row is never repeated.
  - _Requirements: OATM-REQ-F-196, OATM-REQ-F-206, OATM-REQ-F-207, OATM-REQ-F-216_
  - _Rules: OATM-BR-206, OATM-BR-216, OATM-BR-217, OATM-BR-226_
  - _After: OATM-C25-T1, OATM-C25-T2, OATM-C25-T3_
- [ ] OATM-C25-T5 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **lookup field** "Start from transaction ID": Not all digits: 'Tran ID must be Numeric ...' - enter digits only. Higher than every ID on file: 'You are at the top of the page...'.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
  - _Requirements: OATM-REQ-F-195, OATM-REQ-F-196, OATM-REQ-F-197, OATM-REQ-F-198, OATM-REQ-F-199, OATM-REQ-F-200, OATM-REQ-F-201, OATM-REQ-F-202, OATM-REQ-F-203, OATM-REQ-F-204, OATM-REQ-F-205, OATM-REQ-F-206, OATM-REQ-F-207, OATM-REQ-F-208, OATM-REQ-F-209, OATM-REQ-F-210, OATM-REQ-F-211, OATM-REQ-F-212, OATM-REQ-F-213, OATM-REQ-F-214, OATM-REQ-F-215, OATM-REQ-F-216, OATM-REQ-F-217, OATM-REQ-F-218, OATM-REQ-F-219_
  - _Rules: OATM-BR-205, OATM-BR-206, OATM-BR-207, OATM-BR-208, OATM-BR-209, OATM-BR-210, OATM-BR-211, OATM-BR-212, OATM-BR-213, OATM-BR-214, OATM-BR-215, OATM-BR-216, OATM-BR-217, OATM-BR-218, OATM-BR-219, OATM-BR-220, OATM-BR-221, OATM-BR-222, OATM-BR-223, OATM-BR-224, OATM-BR-225, OATM-BR-226, OATM-BR-227, OATM-BR-228, OATM-BR-229_
  - _After: OATM-C25-T2, OATM-C25-T3, OATM-C25-T4_
- [ ] OATM-C25-T6 [test-generation] Write a test for every acceptance criterion
  - 32 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-195, OATM-REQ-F-196, OATM-REQ-F-197, OATM-REQ-F-198, OATM-REQ-F-199, OATM-REQ-F-200, OATM-REQ-F-201, OATM-REQ-F-202, OATM-REQ-F-203, OATM-REQ-F-204, OATM-REQ-F-205, OATM-REQ-F-206, OATM-REQ-F-207, OATM-REQ-F-208, OATM-REQ-F-209, OATM-REQ-F-210, OATM-REQ-F-211, OATM-REQ-F-212, OATM-REQ-F-213, OATM-REQ-F-214, OATM-REQ-F-215, OATM-REQ-F-216, OATM-REQ-F-217, OATM-REQ-F-218, OATM-REQ-F-219_
  - _Criteria: OATM-C25-AC-01, OATM-C25-AC-02, OATM-C25-AC-03, OATM-C25-AC-04, OATM-C25-AC-05, OATM-C25-AC-06, OATM-C25-AC-07, OATM-C25-AC-08, OATM-C25-AC-09, OATM-C25-AC-10, OATM-C25-AC-11, OATM-C25-AC-12, OATM-C25-AC-13, OATM-C25-AC-14, OATM-C25-AC-15, OATM-C25-AC-16, OATM-C25-AC-17, OATM-C25-AC-18, OATM-C25-AC-19, OATM-C25-AC-20, OATM-C25-AC-21, OATM-C25-AC-22, OATM-C25-AC-23, OATM-C25-AC-24, OATM-C25-AC-25, OATM-C25-AC-26, OATM-C25-AC-27, OATM-C25-AC-28, OATM-C25-AC-29, OATM-C25-AC-30, OATM-C25-AC-31, OATM-C25-AC-32_
  - _After: OATM-C25-T1, OATM-C25-T2, OATM-C25-T3, OATM-C25-T4, OATM-C25-T5_
- [ ] OATM-C25-T7 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-195, OATM-REQ-F-196, OATM-REQ-F-197, OATM-REQ-F-198, OATM-REQ-F-199, OATM-REQ-F-200, OATM-REQ-F-201, OATM-REQ-F-202, OATM-REQ-F-203, OATM-REQ-F-204, OATM-REQ-F-205, OATM-REQ-F-206, OATM-REQ-F-207, OATM-REQ-F-208, OATM-REQ-F-209, OATM-REQ-F-210, OATM-REQ-F-211, OATM-REQ-F-212, OATM-REQ-F-213, OATM-REQ-F-214, OATM-REQ-F-215, OATM-REQ-F-216, OATM-REQ-F-217, OATM-REQ-F-218, OATM-REQ-F-219_
  - _After: OATM-C25-T1, OATM-C25-T2, OATM-C25-T3, OATM-C25-T4, OATM-C25-T5_

## OATM-C26 Select a transaction from the list to view its details (final)

- [ ] OATM-C26-T1 [data] Model the data the capability reads and writes
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223_
- [ ] OATM-C26-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222_
  - _Rules: OATM-BR-230, OATM-BR-231, OATM-BR-232_
  - _After: OATM-C26-T1_
- [ ] OATM-C26-T3 [api] Build the services behind the screens
  - OATM-BR-233: When Enter is submitted with no row marked, discard any selection kept from an earlier request (selection code and selected transaction ID) and simply redisplay the list. A stale selection must never open a transaction.
  - _Requirements: OATM-REQ-F-223_
  - _Rules: OATM-BR-233_
  - _After: OATM-C26-T1, OATM-C26-T2_
- [ ] OATM-C26-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223_
  - _Rules: OATM-BR-230, OATM-BR-231, OATM-BR-232, OATM-BR-233_
  - _After: OATM-C26-T2, OATM-C26-T3_
- [ ] OATM-C26-T5 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223_
  - _Criteria: OATM-C26-AC-01, OATM-C26-AC-02, OATM-C26-AC-03, OATM-C26-AC-04, OATM-C26-AC-05, OATM-C26-AC-06_
  - _After: OATM-C26-T1, OATM-C26-T2, OATM-C26-T3, OATM-C26-T4_
- [ ] OATM-C26-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-220, OATM-REQ-F-221, OATM-REQ-F-222, OATM-REQ-F-223_
  - _After: OATM-C26-T1, OATM-C26-T2, OATM-C26-T3, OATM-C26-T4_

## OATM-C27 Transaction list access and session handling (final)

- [ ] OATM-C27-T1 [data] Model the data the capability reads and writes
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010_
- [ ] OATM-C27-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225_
  - _Rules: OATM-BR-234, OATM-BR-235, OATM-BR-236, OATM-BR-237_
  - _After: OATM-C27-T1_
- [ ] OATM-C27-T3 [api] Build the services behind the screens
  - OATM-BR-238: The list needs server-side session state (or a signed cursor carried with each request) that holds the page position (first/last IDs, page number), the current selection and the signed-on user between requests and across the hand-off to the detail screen. No other transaction routing is needed.
  - _Requirements: OATM-REQ-N-010_
  - _Rules: OATM-BR-238_
  - _After: OATM-C27-T1, OATM-C27-T2_
- [ ] OATM-C27-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-225, OATM-REQ-N-010_
  - _Rules: OATM-BR-234, OATM-BR-235, OATM-BR-237, OATM-BR-238_
  - _After: OATM-C27-T2, OATM-C27-T3_
- [ ] OATM-C27-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Transactions"
  - _Requirements: OATM-REQ-N-008, OATM-REQ-F-224_
  - _Rules: OATM-BR-234, OATM-BR-236_
  - _After: OATM-C27-T2, OATM-C27-T3_
- [ ] OATM-C27-T6 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010_
  - _Criteria: OATM-C27-AC-01, OATM-C27-AC-02, OATM-C27-AC-03, OATM-C27-AC-04, OATM-C27-AC-05_
  - _After: OATM-C27-T1, OATM-C27-T2, OATM-C27-T3, OATM-C27-T4, OATM-C27-T5_
- [ ] OATM-C27-T7 [compliance] Review the handling of card data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010_
  - _After: OATM-C27-T1, OATM-C27-T2, OATM-C27-T3, OATM-C27-T4, OATM-C27-T5_

## OATM-C28 Look up a single transaction (final)

- [ ] OATM-C28-T1 [data] Model the data the capability reads and writes
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-F-226, OATM-REQ-F-227_
- [ ] OATM-C28-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-227_
  - _Rules: OATM-BR-240_
  - _After: OATM-C28-T1_
- [ ] OATM-C28-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-226_
  - _Rules: OATM-BR-239_
  - _After: OATM-C28-T1_
- [ ] OATM-C28-T4 [ui-modernization] Build the screen Transaction (S-TRANSACTION-VIEW)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-VIEW.
  - **lookup field** "Transaction ID": Blank: 'Tran ID can NOT be empty...' - enter a transaction ID. Not found: 'Transaction ID NOT found...' - check the ID or find it in Transactions.
  - _Requirements: OATM-REQ-F-226, OATM-REQ-F-227_
  - _Rules: OATM-BR-239, OATM-BR-240_
  - _After: OATM-C28-T2, OATM-C28-T3_
- [ ] OATM-C28-T5 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-226, OATM-REQ-F-227_
  - _Criteria: OATM-C28-AC-01, OATM-C28-AC-02_
  - _After: OATM-C28-T1, OATM-C28-T2, OATM-C28-T3, OATM-C28-T4_
- [ ] OATM-C28-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-226, OATM-REQ-F-227_
  - _After: OATM-C28-T1, OATM-C28-T2, OATM-C28-T3, OATM-C28-T4_

## OATM-C29 View a single transaction (final)

- [ ] OATM-C29-T1 [data] Model the data the capability reads and writes
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-233, OATM-REQ-N-011, OATM-REQ-F-234, OATM-REQ-F-235, OATM-REQ-F-236, OATM-REQ-F-237_
- [ ] OATM-C29-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-233, OATM-REQ-F-234, OATM-REQ-F-236, OATM-REQ-F-237_
  - _Rules: OATM-BR-241, OATM-BR-242, OATM-BR-243, OATM-BR-246, OATM-BR-248, OATM-BR-250, OATM-BR-251_
  - _After: OATM-C29-T1_
- [ ] OATM-C29-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-N-011, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-235_
  - _Rules: OATM-BR-244, OATM-BR-245, OATM-BR-247, OATM-BR-249_
  - _After: OATM-C29-T1_
- [ ] OATM-C29-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - **data table** "Transactions": Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.'
  - _Requirements: OATM-REQ-N-011_
  - _Rules: OATM-BR-247_
  - _After: OATM-C29-T2, OATM-C29-T3_
- [ ] OATM-C29-T5 [ui-modernization] Build the screen Transaction (S-TRANSACTION-VIEW)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-VIEW.
  - **lookup field** "Transaction ID": Blank: 'Tran ID can NOT be empty...' - enter a transaction ID. Not found: 'Transaction ID NOT found...' - check the ID or find it in Transactions.
  - **summary card** "Transaction"
  - **summary card** "Merchant"
  - **primary button** "Back to transactions"
  - _Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-233, OATM-REQ-F-234, OATM-REQ-F-235, OATM-REQ-F-236, OATM-REQ-F-237_
  - _Rules: OATM-BR-241, OATM-BR-242, OATM-BR-243, OATM-BR-244, OATM-BR-245, OATM-BR-246, OATM-BR-248, OATM-BR-249, OATM-BR-250, OATM-BR-251_
  - _After: OATM-C29-T2, OATM-C29-T3_
- [ ] OATM-C29-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **primary button** "Transactions"
  - _Requirements: OATM-REQ-F-234_
  - _Rules: OATM-BR-248_
  - _After: OATM-C29-T2, OATM-C29-T3_
- [ ] OATM-C29-T7 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-233, OATM-REQ-N-011, OATM-REQ-F-234, OATM-REQ-F-235, OATM-REQ-F-236, OATM-REQ-F-237_
  - _Criteria: OATM-C29-AC-01, OATM-C29-AC-02, OATM-C29-AC-03, OATM-C29-AC-04, OATM-C29-AC-05, OATM-C29-AC-06, OATM-C29-AC-07, OATM-C29-AC-08, OATM-C29-AC-09, OATM-C29-AC-10, OATM-C29-AC-11, OATM-C29-AC-12, OATM-C29-AC-13_
  - _After: OATM-C29-T1, OATM-C29-T2, OATM-C29-T3, OATM-C29-T4, OATM-C29-T5, OATM-C29-T6_
- [ ] OATM-C29-T8 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-228, OATM-REQ-F-229, OATM-REQ-F-230, OATM-REQ-F-231, OATM-REQ-F-232, OATM-REQ-F-233, OATM-REQ-N-011, OATM-REQ-F-234, OATM-REQ-F-235, OATM-REQ-F-236, OATM-REQ-F-237_
  - _After: OATM-C29-T1, OATM-C29-T2, OATM-C29-T3, OATM-C29-T4, OATM-C29-T5, OATM-C29-T6_

## OATM-C30 Open and navigate the Add Transaction screen (final)

- [ ] OATM-C30-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-N-012, OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-F-240, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244_
- [ ] OATM-C30-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-N-012, OATM-REQ-F-239, OATM-REQ-F-240, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244_
  - _Rules: OATM-BR-252, OATM-BR-254, OATM-BR-255, OATM-BR-256, OATM-BR-257, OATM-BR-258_
  - _After: OATM-C30-T1_
- [ ] OATM-C30-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-238_
  - _Rules: OATM-BR-253_
  - _After: OATM-C30-T1_
- [ ] OATM-C30-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **lookup field** "Account or card number": Blank: 'Account or Card Number must be entered...'. Not digits: 'Account ID must be Numeric...' / 'Card Number must be Numeric...'. Not in the card cross-reference: 'Account ID NOT found...' / 'Card Number NOT found...' - check the number with the caller.
  - **summary card** "Transaction details": Each is required, in the rule's words: 'Type CD can NOT be empty...', 'Category CD can NOT be empty...', 'Source can NOT be empty...', 'Description can NOT be empty...', 'Amount can NOT be empty...', 'Orig Date can NOT be empty...', 'Proc Date can NOT be empty...'. 'Type CD must be Numeric...', 'Category CD must be Numeric...'. 'Amount should be in format -99999999.99'. 'Orig Date should be in format YYYY-MM-DD', 'Proc Date should be in format YYYY-MM-DD', and 'Orig Date - Not a valid date...' / 'Proc Date - Not a valid date...' for a date not on the calendar. Every failing field shows its message under it.
  - **primary button** "Add transaction": The dialog offers only Add or Cancel, replacing the typed confirmation and its messages 'Confirm to add this transaction...' and 'Invalid value. Valid values are (Y/N)...'. If the ID already exists: 'Tran ID already exist...'; other failures: 'Unable to Add Transaction...'.
  - _Requirements: OATM-REQ-N-012, OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244_
  - _Rules: OATM-BR-252, OATM-BR-253, OATM-BR-254, OATM-BR-256, OATM-BR-257, OATM-BR-258_
  - _After: OATM-C30-T2, OATM-C30-T3_
- [ ] OATM-C30-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Add transaction"
  - _Requirements: OATM-REQ-N-012, OATM-REQ-F-240_
  - _Rules: OATM-BR-252, OATM-BR-255_
  - _After: OATM-C30-T2, OATM-C30-T3_
- [ ] OATM-C30-T6 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-N-012, OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-F-240, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244_
  - _Criteria: OATM-C30-AC-01, OATM-C30-AC-02, OATM-C30-AC-03, OATM-C30-AC-04, OATM-C30-AC-05, OATM-C30-AC-06, OATM-C30-AC-07, OATM-C30-AC-08, OATM-C30-AC-09_
  - _After: OATM-C30-T1, OATM-C30-T2, OATM-C30-T3, OATM-C30-T4, OATM-C30-T5_
- [ ] OATM-C30-T7 [compliance] Review the handling of card data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-N-012, OATM-REQ-F-238, OATM-REQ-F-239, OATM-REQ-F-240, OATM-REQ-F-241, OATM-REQ-F-242, OATM-REQ-F-243, OATM-REQ-F-244_
  - _After: OATM-C30-T1, OATM-C30-T2, OATM-C30-T3, OATM-C30-T4, OATM-C30-T5_

## OATM-C31 Identify the account and card for a new transaction (final)

- [ ] OATM-C31-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014_
- [ ] OATM-C31-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252_
  - _Rules: OATM-BR-259, OATM-BR-260, OATM-BR-261, OATM-BR-262, OATM-BR-263, OATM-BR-265, OATM-BR-266, OATM-BR-267_
  - _After: OATM-C31-T1_
- [ ] OATM-C31-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-N-013, OATM-REQ-N-014_
  - _Rules: OATM-BR-264, OATM-BR-268_
  - _After: OATM-C31-T1_
- [ ] OATM-C31-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **lookup field** "Account or card number": Blank: 'Account or Card Number must be entered...'. Not digits: 'Account ID must be Numeric...' / 'Card Number must be Numeric...'. Not in the card cross-reference: 'Account ID NOT found...' / 'Card Number NOT found...' - check the number with the caller.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014_
  - _Rules: OATM-BR-259, OATM-BR-260, OATM-BR-261, OATM-BR-262, OATM-BR-263, OATM-BR-264, OATM-BR-265, OATM-BR-266, OATM-BR-267, OATM-BR-268_
  - _After: OATM-C31-T2, OATM-C31-T3_
- [ ] OATM-C31-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014_
  - _Criteria: OATM-C31-AC-01, OATM-C31-AC-02, OATM-C31-AC-03, OATM-C31-AC-04, OATM-C31-AC-05, OATM-C31-AC-06, OATM-C31-AC-07, OATM-C31-AC-08, OATM-C31-AC-09, OATM-C31-AC-10, OATM-C31-AC-11, OATM-C31-AC-12, OATM-C31-AC-13_
  - _After: OATM-C31-T1, OATM-C31-T2, OATM-C31-T3, OATM-C31-T4_
- [ ] OATM-C31-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-N-013, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-014_
  - _After: OATM-C31-T1, OATM-C31-T2, OATM-C31-T3, OATM-C31-T4_

## OATM-C32 Validate new transaction details (final)

- [ ] OATM-C32-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
- [ ] OATM-C32-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
  - _Rules: OATM-BR-269, OATM-BR-270, OATM-BR-271, OATM-BR-272, OATM-BR-273, OATM-BR-274, OATM-BR-275, OATM-BR-276, OATM-BR-277, OATM-BR-278, OATM-BR-279, OATM-BR-280, OATM-BR-281, OATM-BR-282, OATM-BR-283, OATM-BR-284, OATM-BR-285, OATM-BR-287, OATM-BR-288, OATM-BR-289, OATM-BR-290, OATM-BR-291, OATM-BR-292_
  - _After: OATM-C32-T1_
- [ ] OATM-C32-T3 [api] Build the services behind the screens
  - OATM-BR-286: Parse the accepted amount text into an exact signed decimal with two decimal places (no floating point), echo it back formatted as +99999999.99, and use that same parsed value as the stored transaction amount.
  - _Requirements: OATM-REQ-F-270_
  - _Rules: OATM-BR-286_
  - _After: OATM-C32-T1, OATM-C32-T2_
- [ ] OATM-C32-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **summary card** "Transaction details": Each is required, in the rule's words: 'Type CD can NOT be empty...', 'Category CD can NOT be empty...', 'Source can NOT be empty...', 'Description can NOT be empty...', 'Amount can NOT be empty...', 'Orig Date can NOT be empty...', 'Proc Date can NOT be empty...'. 'Type CD must be Numeric...', 'Category CD must be Numeric...'. 'Amount should be in format -99999999.99'. 'Orig Date should be in format YYYY-MM-DD', 'Proc Date should be in format YYYY-MM-DD', and 'Orig Date - Not a valid date...' / 'Proc Date - Not a valid date...' for a date not on the calendar. Every failing field shows its message under it.
  - **summary card** "Merchant": 'Merchant ID can NOT be empty...', 'Merchant Name can NOT be empty...', 'Merchant City can NOT be empty...', 'Merchant Zip can NOT be empty...'; 'Merchant ID must be Numeric...'.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
  - _Rules: OATM-BR-269, OATM-BR-270, OATM-BR-271, OATM-BR-272, OATM-BR-273, OATM-BR-274, OATM-BR-275, OATM-BR-276, OATM-BR-277, OATM-BR-278, OATM-BR-279, OATM-BR-280, OATM-BR-281, OATM-BR-282, OATM-BR-283, OATM-BR-284, OATM-BR-285, OATM-BR-286, OATM-BR-287, OATM-BR-288, OATM-BR-289, OATM-BR-290, OATM-BR-291, OATM-BR-292_
  - _After: OATM-C32-T2, OATM-C32-T3_
- [ ] OATM-C32-T5 [test-generation] Write a test for every acceptance criterion
  - 30 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
  - _Criteria: OATM-C32-AC-01, OATM-C32-AC-02, OATM-C32-AC-03, OATM-C32-AC-04, OATM-C32-AC-05, OATM-C32-AC-06, OATM-C32-AC-07, OATM-C32-AC-08, OATM-C32-AC-09, OATM-C32-AC-10, OATM-C32-AC-11, OATM-C32-AC-12, OATM-C32-AC-13, OATM-C32-AC-14, OATM-C32-AC-15, OATM-C32-AC-16, OATM-C32-AC-17, OATM-C32-AC-18, OATM-C32-AC-19, OATM-C32-AC-20, OATM-C32-AC-21, OATM-C32-AC-22, OATM-C32-AC-23, OATM-C32-AC-24, OATM-C32-AC-25, OATM-C32-AC-26, OATM-C32-AC-27, OATM-C32-AC-28, OATM-C32-AC-29, OATM-C32-AC-30_
  - _After: OATM-C32-T1, OATM-C32-T2, OATM-C32-T3, OATM-C32-T4_
- [ ] OATM-C32-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
  - _After: OATM-C32-T1, OATM-C32-T2, OATM-C32-T3, OATM-C32-T4_

## OATM-C33 Record a confirmed new transaction (final)

- [ ] OATM-C33-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015_
- [ ] OATM-C33-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-281_
  - _Rules: OATM-BR-293, OATM-BR-294, OATM-BR-295, OATM-BR-297_
  - _After: OATM-C33-T1_
- [ ] OATM-C33-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-280, OATM-REQ-F-283, OATM-REQ-N-015, OATM-REQ-F-282_
  - _Rules: OATM-BR-296, OATM-BR-298, OATM-BR-299, OATM-BR-300_
  - _After: OATM-C33-T1_
- [ ] OATM-C33-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **primary button** "Add transaction": The dialog offers only Add or Cancel, replacing the typed confirmation and its messages 'Confirm to add this transaction...' and 'Invalid value. Valid values are (Y/N)...'. If the ID already exists: 'Tran ID already exist...'; other failures: 'Unable to Add Transaction...'.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015_
  - _Rules: OATM-BR-293, OATM-BR-294, OATM-BR-295, OATM-BR-296, OATM-BR-297, OATM-BR-298, OATM-BR-299, OATM-BR-300_
  - _After: OATM-C33-T2, OATM-C33-T3_
- [ ] OATM-C33-T5 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015_
  - _Criteria: OATM-C33-AC-01, OATM-C33-AC-02, OATM-C33-AC-03, OATM-C33-AC-04, OATM-C33-AC-05, OATM-C33-AC-06, OATM-C33-AC-07, OATM-C33-AC-08, OATM-C33-AC-09_
  - _After: OATM-C33-T1, OATM-C33-T2, OATM-C33-T3, OATM-C33-T4_
- [ ] OATM-C33-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-277, OATM-REQ-F-278, OATM-REQ-F-279, OATM-REQ-F-280, OATM-REQ-F-281, OATM-REQ-F-282, OATM-REQ-F-283, OATM-REQ-N-015_
  - _After: OATM-C33-T1, OATM-C33-T2, OATM-C33-T3, OATM-C33-T4_

## OATM-C34 Confirm a transaction before it is added (final)

- [ ] OATM-C34-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-F-284, OATM-REQ-F-285_
- [ ] OATM-C34-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-284, OATM-REQ-F-285_
  - _Rules: OATM-BR-301, OATM-BR-302_
  - _After: OATM-C34-T1_
- [ ] OATM-C34-T3 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **primary button** "Add transaction": The dialog offers only Add or Cancel, replacing the typed confirmation and its messages 'Confirm to add this transaction...' and 'Invalid value. Valid values are (Y/N)...'. If the ID already exists: 'Tran ID already exist...'; other failures: 'Unable to Add Transaction...'.
  - _Requirements: OATM-REQ-F-284, OATM-REQ-F-285_
  - _Rules: OATM-BR-301, OATM-BR-302_
  - _After: OATM-C34-T2_
- [ ] OATM-C34-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-284, OATM-REQ-F-285_
  - _Criteria: OATM-C34-AC-01, OATM-C34-AC-02, OATM-C34-AC-03_
  - _After: OATM-C34-T1, OATM-C34-T2, OATM-C34-T3_

## OATM-C35 Validate a date against a format mask (final)

- [ ] OATM-C35-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-288, OATM-REQ-F-289, OATM-REQ-F-290, OATM-REQ-F-291, OATM-REQ-F-292, OATM-REQ-F-293, OATM-REQ-F-294, OATM-REQ-F-295, OATM-REQ-F-296, OATM-REQ-F-297, OATM-REQ-F-298_
  - _Rules: OATM-BR-305, OATM-BR-306, OATM-BR-307, OATM-BR-308, OATM-BR-309, OATM-BR-310, OATM-BR-311, OATM-BR-312, OATM-BR-313, OATM-BR-314, OATM-BR-315_
- [ ] OATM-C35-T2 [api] Build the service
  - OATM-BR-303: Expose date validation as one shared function or service that takes a date string and a format mask and returns a structured result (severity, message code, reason). Implement it with the platform's standard date-parsing library instead of the mainframe date service, and keep the legacy severity/message codes (0000, 2508, 2513 and so on) only as far as callers need them to tell valid from invalid.
  - OATM-BR-304: Callers need a result they can test: a severity/status, a message code, the reason text, and the tested date and mask for diagnostics. A typed result object replaces the fixed 80-character string and the program return code. Keep the layout only if a remaining legacy consumer still reads it.
  - _Requirements: OATM-REQ-F-286, OATM-REQ-F-287_
  - _Rules: OATM-BR-303, OATM-BR-304_
  - _After: OATM-C35-T1_
- [ ] OATM-C35-T3 [test-generation] Write a test for every acceptance criterion
  - 14 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-286, OATM-REQ-F-287, OATM-REQ-F-288, OATM-REQ-F-289, OATM-REQ-F-290, OATM-REQ-F-291, OATM-REQ-F-292, OATM-REQ-F-293, OATM-REQ-F-294, OATM-REQ-F-295, OATM-REQ-F-296, OATM-REQ-F-297, OATM-REQ-F-298_
  - _Criteria: OATM-C35-AC-01, OATM-C35-AC-02, OATM-C35-AC-03, OATM-C35-AC-04, OATM-C35-AC-05, OATM-C35-AC-06, OATM-C35-AC-07, OATM-C35-AC-08, OATM-C35-AC-09, OATM-C35-AC-10, OATM-C35-AC-11, OATM-C35-AC-12, OATM-C35-AC-13, OATM-C35-AC-14_
  - _After: OATM-C35-T1, OATM-C35-T2_

## CCLDV-C01 Browse and page the card list (draft)

- [ ] CCLDV-C01-T1 [data] Model the data the capability reads and writes
  - File records: CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y.
  - _Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-002, CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-009, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019, CCLDV-REQ-F-020_
- [ ] CCLDV-C01-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-020_
  - _Rules: CCLDV-BR-003, CCLDV-BR-004, CCLDV-BR-005, CCLDV-BR-006, CCLDV-BR-007, CCLDV-BR-008, CCLDV-BR-009, CCLDV-BR-011, CCLDV-BR-012, CCLDV-BR-013, CCLDV-BR-014, CCLDV-BR-015, CCLDV-BR-016, CCLDV-BR-022_
  - _After: CCLDV-C01-T1_
- [ ] CCLDV-C01-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-009, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019_
  - _Rules: CCLDV-BR-001, CCLDV-BR-010, CCLDV-BR-019, CCLDV-BR-020, CCLDV-BR-021_
  - _After: CCLDV-C01-T1_
- [ ] CCLDV-C01-T4 [api] Build the services behind the screens
  - CCLDV-BR-002: When the list is opened fresh (from the main menu, or on return from card detail or card update), start a new list session: no saved first or last card positions, page number 1, last-page-shown false. Ignore any form or filter input sent with that request.
  - CCLDV-BR-017: When paging back, set the session's 'has next page' to true and save the first card number of the page being left as the start of the next page, so the next forward page request goes back to exactly that page.
  - CCLDV-BR-018: Keep a 'last page already shown' flag in the list session. Clear it on every user action except next page, so that only two next-page requests in a row on the last page lead to the 'no more pages' message.
  - _Requirements: CCLDV-REQ-F-002, CCLDV-REQ-F-015, CCLDV-REQ-F-016_
  - _Rules: CCLDV-BR-002, CCLDV-BR-017, CCLDV-BR-018_
  - _After: CCLDV-C01-T1, CCLDV-C01-T2, CCLDV-C01-T3_
- [ ] CCLDV-C01-T5 [ui-modernization] Build the screen Cards (S-CARD-LIST)
  - To the prototype: ui-reference/index.html#/S-CARD-LIST.
  - **data table** "Cards found": Each row is its own link and only one opens at a time, so no selection code is typed and 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' and 'INVALID ACTION CODE' cannot occur
  - **status badge** "Card status"
  - _Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-004, CCLDV-REQ-F-009_
  - _Rules: CCLDV-BR-001, CCLDV-BR-004, CCLDV-BR-010_
  - _After: CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4_
- [ ] CCLDV-C01-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Cards"
  - _Requirements: CCLDV-REQ-F-020_
  - _Rules: CCLDV-BR-022_
  - _After: CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4_
- [ ] CCLDV-C01-T7 [test-generation] Write a test for every acceptance criterion
  - 28 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-002, CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-009, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019, CCLDV-REQ-F-020_
  - _Criteria: CCLDV-C01-AC-01, CCLDV-C01-AC-02, CCLDV-C01-AC-03, CCLDV-C01-AC-04, CCLDV-C01-AC-05, CCLDV-C01-AC-06, CCLDV-C01-AC-07, CCLDV-C01-AC-08, CCLDV-C01-AC-09, CCLDV-C01-AC-10, CCLDV-C01-AC-11, CCLDV-C01-AC-12, CCLDV-C01-AC-13, CCLDV-C01-AC-14, CCLDV-C01-AC-15, CCLDV-C01-AC-16, CCLDV-C01-AC-17, CCLDV-C01-AC-18, CCLDV-C01-AC-19, CCLDV-C01-AC-20, CCLDV-C01-AC-21, CCLDV-C01-AC-22, CCLDV-C01-AC-23, CCLDV-C01-AC-24, CCLDV-C01-AC-25, CCLDV-C01-AC-26, CCLDV-C01-AC-27, CCLDV-C01-AC-28_
  - _After: CCLDV-C01-T1, CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4, CCLDV-C01-T5, CCLDV-C01-T6_
- [ ] CCLDV-C01-T8 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-001, CCLDV-REQ-F-002, CCLDV-REQ-F-003, CCLDV-REQ-F-004, CCLDV-REQ-F-005, CCLDV-REQ-F-006, CCLDV-REQ-F-007, CCLDV-REQ-F-008, CCLDV-REQ-F-009, CCLDV-REQ-F-010, CCLDV-REQ-F-011, CCLDV-REQ-F-012, CCLDV-REQ-F-013, CCLDV-REQ-F-014, CCLDV-REQ-F-015, CCLDV-REQ-F-016, CCLDV-REQ-F-017, CCLDV-REQ-F-018, CCLDV-REQ-F-019, CCLDV-REQ-F-020_
  - _After: CCLDV-C01-T1, CCLDV-C01-T2, CCLDV-C01-T3, CCLDV-C01-T4, CCLDV-C01-T5, CCLDV-C01-T6_

## CCLDV-C02 Filter the card list by account and card number (draft)

- [ ] CCLDV-C02-T1 [data] Model the data the capability reads and writes
  - File records: CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y.
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027_
- [ ] CCLDV-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026_
  - _Rules: CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-025, CCLDV-BR-026, CCLDV-BR-027_
  - _After: CCLDV-C02-T1_
- [ ] CCLDV-C02-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-027_
  - _Rules: CCLDV-BR-021, CCLDV-BR-028_
  - _After: CCLDV-C02-T1_
- [ ] CCLDV-C02-T4 [ui-modernization] Build the screen Cards (S-CARD-LIST)
  - To the prototype: ui-reference/index.html#/S-CARD-LIST.
  - **lookup field** "Account number": Must be an 11-digit number if entered: 'Account filter, if supplied, must be an 11 digit number. Enter the 11 digits or leave it blank.'
  - **lookup field** "Card number": Must be a 16-digit number if entered: 'Card ID filter, if supplied, must be a 16 digit number. Enter the 16 digits or leave it blank.'
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-025, CCLDV-REQ-F-026_
  - _Rules: CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-025, CCLDV-BR-026, CCLDV-BR-027_
  - _After: CCLDV-C02-T2, CCLDV-C02-T3_
- [ ] CCLDV-C02-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027_
  - _Criteria: CCLDV-C02-AC-01, CCLDV-C02-AC-02, CCLDV-C02-AC-03, CCLDV-C02-AC-04, CCLDV-C02-AC-05, CCLDV-C02-AC-06, CCLDV-C02-AC-07, CCLDV-C02-AC-08, CCLDV-C02-AC-09, CCLDV-C02-AC-10_
  - _After: CCLDV-C02-T1, CCLDV-C02-T2, CCLDV-C02-T3, CCLDV-C02-T4_
- [ ] CCLDV-C02-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027_
  - _After: CCLDV-C02-T1, CCLDV-C02-T2, CCLDV-C02-T3, CCLDV-C02-T4_

## CCLDV-C03 Select a card to view or update (draft)

- [ ] CCLDV-C03-T1 [data] Model the data the capability reads and writes
  - File records: CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y.
  - _Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-031, CCLDV-REQ-F-032, CCLDV-REQ-F-033_
- [ ] CCLDV-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-032, CCLDV-REQ-F-033_
  - _Rules: CCLDV-BR-029, CCLDV-BR-030, CCLDV-BR-031_
  - _After: CCLDV-C03-T1_
- [ ] CCLDV-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-031_
  - _Rules: CCLDV-BR-028_
  - _After: CCLDV-C03-T1_
- [ ] CCLDV-C03-T4 [ui-modernization] Build the screen Cards (S-CARD-LIST)
  - To the prototype: ui-reference/index.html#/S-CARD-LIST.
  - **data table** "Cards found": Each row is its own link and only one opens at a time, so no selection code is typed and 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' and 'INVALID ACTION CODE' cannot occur
  - _Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-032, CCLDV-REQ-F-033_
  - _Rules: CCLDV-BR-029, CCLDV-BR-030, CCLDV-BR-031_
  - _After: CCLDV-C03-T2, CCLDV-C03-T3_
- [ ] CCLDV-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-031, CCLDV-REQ-F-032, CCLDV-REQ-F-033_
  - _Criteria: CCLDV-C03-AC-01, CCLDV-C03-AC-02, CCLDV-C03-AC-03, CCLDV-C03-AC-04, CCLDV-C03-AC-05, CCLDV-C03-AC-06, CCLDV-C03-AC-07_
  - _After: CCLDV-C03-T1, CCLDV-C03-T2, CCLDV-C03-T3, CCLDV-C03-T4_
- [ ] CCLDV-C03-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-031, CCLDV-REQ-F-032, CCLDV-REQ-F-033_
  - _After: CCLDV-C03-T1, CCLDV-C03-T2, CCLDV-C03-T3, CCLDV-C03-T4_

## CCLDV-C04 Search and view card details (draft)

- [ ] CCLDV-C04-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-034, CCLDV-REQ-F-035, CCLDV-REQ-F-036, CCLDV-REQ-F-037, CCLDV-REQ-F-038, CCLDV-REQ-F-039, CCLDV-REQ-F-040, CCLDV-REQ-F-041, CCLDV-REQ-F-042, CCLDV-REQ-F-043, CCLDV-REQ-F-044, CCLDV-REQ-F-045, CCLDV-REQ-F-046, CCLDV-REQ-F-047, CCLDV-REQ-F-048, CCLDV-REQ-F-049, CCLDV-REQ-F-050, CCLDV-REQ-F-051, CCLDV-REQ-F-052, CCLDV-REQ-F-053_
- [ ] CCLDV-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-034, CCLDV-REQ-F-035, CCLDV-REQ-F-036, CCLDV-REQ-F-037, CCLDV-REQ-F-038, CCLDV-REQ-F-039, CCLDV-REQ-F-040, CCLDV-REQ-F-041, CCLDV-REQ-F-042, CCLDV-REQ-F-043, CCLDV-REQ-F-044, CCLDV-REQ-F-046_
  - _Rules: CCLDV-BR-032, CCLDV-BR-033, CCLDV-BR-034, CCLDV-BR-035, CCLDV-BR-036, CCLDV-BR-037, CCLDV-BR-038, CCLDV-BR-039, CCLDV-BR-040, CCLDV-BR-041, CCLDV-BR-042, CCLDV-BR-043, CCLDV-BR-045_
  - _After: CCLDV-C04-T1_
- [ ] CCLDV-C04-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-047, CCLDV-REQ-F-045, CCLDV-REQ-F-048, CCLDV-REQ-F-049, CCLDV-REQ-F-050, CCLDV-REQ-F-051, CCLDV-REQ-F-052, CCLDV-REQ-F-053_
  - _Rules: CCLDV-BR-044, CCLDV-BR-046, CCLDV-BR-047, CCLDV-BR-048, CCLDV-BR-049, CCLDV-BR-050, CCLDV-BR-051, CCLDV-BR-052_
  - _After: CCLDV-C04-T1_
- [ ] CCLDV-C04-T4 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **lookup field** "Account number": Required, an 11-digit number other than zeros: 'Account number not provided. Enter the 11-digit account number.' or 'Account filter, if supplied, must be an 11 digit number. Enter digits only.' Both fields empty: 'No input received. Enter the account and card number.' Account is checked before card, and focus moves to the first field in error.
  - **lookup field** "Card number": Required, a 16-digit number other than zeros: 'Card number not provided. Enter the 16-digit card number.' or 'Card ID filter, if supplied, must be a 16 digit number. Enter digits only.' No card with that number: 'Did not find cards for this search condition. Check the card number.'
  - **summary card** "Card"
  - **status badge** "Current status"
  - _Requirements: CCLDV-REQ-F-044, CCLDV-REQ-F-045, CCLDV-REQ-F-046, CCLDV-REQ-F-047, CCLDV-REQ-F-051, CCLDV-REQ-F-053_
  - _Rules: CCLDV-BR-043, CCLDV-BR-044, CCLDV-BR-045, CCLDV-BR-046, CCLDV-BR-050, CCLDV-BR-052_
  - _After: CCLDV-C04-T2, CCLDV-C04-T3_
- [ ] CCLDV-C04-T5 [test-generation] Write a test for every acceptance criterion
  - 33 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-034, CCLDV-REQ-F-035, CCLDV-REQ-F-036, CCLDV-REQ-F-037, CCLDV-REQ-F-038, CCLDV-REQ-F-039, CCLDV-REQ-F-040, CCLDV-REQ-F-041, CCLDV-REQ-F-042, CCLDV-REQ-F-043, CCLDV-REQ-F-044, CCLDV-REQ-F-045, CCLDV-REQ-F-046, CCLDV-REQ-F-047, CCLDV-REQ-F-048, CCLDV-REQ-F-049, CCLDV-REQ-F-050, CCLDV-REQ-F-051, CCLDV-REQ-F-052, CCLDV-REQ-F-053_
  - _Criteria: CCLDV-C04-AC-01, CCLDV-C04-AC-02, CCLDV-C04-AC-03, CCLDV-C04-AC-04, CCLDV-C04-AC-05, CCLDV-C04-AC-06, CCLDV-C04-AC-07, CCLDV-C04-AC-08, CCLDV-C04-AC-09, CCLDV-C04-AC-10, CCLDV-C04-AC-11, CCLDV-C04-AC-12, CCLDV-C04-AC-13, CCLDV-C04-AC-14, CCLDV-C04-AC-15, CCLDV-C04-AC-16, CCLDV-C04-AC-17, CCLDV-C04-AC-18, CCLDV-C04-AC-19, CCLDV-C04-AC-20, CCLDV-C04-AC-21, CCLDV-C04-AC-22, CCLDV-C04-AC-23, CCLDV-C04-AC-24, CCLDV-C04-AC-25, CCLDV-C04-AC-26, CCLDV-C04-AC-27, CCLDV-C04-AC-28, CCLDV-C04-AC-29, CCLDV-C04-AC-30, CCLDV-C04-AC-31, CCLDV-C04-AC-32, CCLDV-C04-AC-33_
  - _After: CCLDV-C04-T1, CCLDV-C04-T2, CCLDV-C04-T3, CCLDV-C04-T4_
- [ ] CCLDV-C04-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-034, CCLDV-REQ-F-035, CCLDV-REQ-F-036, CCLDV-REQ-F-037, CCLDV-REQ-F-038, CCLDV-REQ-F-039, CCLDV-REQ-F-040, CCLDV-REQ-F-041, CCLDV-REQ-F-042, CCLDV-REQ-F-043, CCLDV-REQ-F-044, CCLDV-REQ-F-045, CCLDV-REQ-F-046, CCLDV-REQ-F-047, CCLDV-REQ-F-048, CCLDV-REQ-F-049, CCLDV-REQ-F-050, CCLDV-REQ-F-051, CCLDV-REQ-F-052, CCLDV-REQ-F-053_
  - _After: CCLDV-C04-T1, CCLDV-C04-T2, CCLDV-C04-T3, CCLDV-C04-T4_

## CCLDV-C05 Enter and leave the card detail screen (draft)

- [ ] CCLDV-C05-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058_
- [ ] CCLDV-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-056, CCLDV-REQ-F-057_
  - _Rules: CCLDV-BR-056, CCLDV-BR-058_
  - _After: CCLDV-C05-T1_
- [ ] CCLDV-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-055_
  - _Rules: CCLDV-BR-054, CCLDV-BR-055_
  - _After: CCLDV-C05-T1_
- [ ] CCLDV-C05-T4 [api] Build the services behind the screens
  - CCLDV-BR-053: When card detail opens with no navigation context, or opens fresh from the main menu, clear the whole shared navigation/session context (selected account, card, caller and last screen) before doing anything else.
  - CCLDV-BR-057: Card detail is a stateful page. Every response it sends keeps the user in the card detail conversation, so the next submit from that page comes back to the card detail handler as a continuation of the same search, not as a fresh entry.
  - CCLDV-BR-059: On leaving card detail, update the shared navigation context: sender = card detail, user type = regular user ('U'), last screen = card detail, and mark the next screen's entry as a first entry so it starts fresh.
  - _Requirements: CCLDV-REQ-F-054, CCLDV-REQ-N-001, CCLDV-REQ-F-058_
  - _Rules: CCLDV-BR-053, CCLDV-BR-057, CCLDV-BR-059_
  - _After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3_
- [ ] CCLDV-C05-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Cards"
  - _Requirements: CCLDV-REQ-F-057_
  - _Rules: CCLDV-BR-058_
  - _After: CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4_
- [ ] CCLDV-C05-T6 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058_
  - _Criteria: CCLDV-C05-AC-01, CCLDV-C05-AC-02, CCLDV-C05-AC-03, CCLDV-C05-AC-04, CCLDV-C05-AC-05, CCLDV-C05-AC-06, CCLDV-C05-AC-07, CCLDV-C05-AC-08_
  - _After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4, CCLDV-C05-T5_
- [ ] CCLDV-C05-T7 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-054, CCLDV-REQ-F-055, CCLDV-REQ-F-056, CCLDV-REQ-N-001, CCLDV-REQ-F-057, CCLDV-REQ-F-058_
  - _After: CCLDV-C05-T1, CCLDV-C05-T2, CCLDV-C05-T3, CCLDV-C05-T4, CCLDV-C05-T5_

## CCLDV-C06 Detect unchanged card details on update (draft)

- [ ] CCLDV-C06-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
- [ ] CCLDV-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
  - _Rules: CCLDV-BR-060_
  - _After: CCLDV-C06-T1_
- [ ] CCLDV-C06-T3 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **primary button** "Save card": Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
  - _Rules: CCLDV-BR-060_
  - _After: CCLDV-C06-T2_
- [ ] CCLDV-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
  - _Criteria: CCLDV-C06-AC-01, CCLDV-C06-AC-02, CCLDV-C06-AC-03_
  - _After: CCLDV-C06-T1, CCLDV-C06-T2, CCLDV-C06-T3_
- [ ] CCLDV-C06-T5 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
  - _After: CCLDV-C06-T1, CCLDV-C06-T2, CCLDV-C06-T3_

## CCLDV-C07 Find and show a card for update (draft)

- [ ] CCLDV-C07-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-065, CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-074, CCLDV-REQ-F-075, CCLDV-REQ-F-076, CCLDV-REQ-F-077_
- [ ] CCLDV-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-077_
  - _Rules: CCLDV-BR-069, CCLDV-BR-070, CCLDV-BR-071, CCLDV-BR-072, CCLDV-BR-073, CCLDV-BR-074, CCLDV-BR-075, CCLDV-BR-076, CCLDV-BR-077, CCLDV-BR-078, CCLDV-BR-079, CCLDV-BR-084_
  - _After: CCLDV-C07-T1_
- [ ] CCLDV-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-074, CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-076_
  - _Rules: CCLDV-BR-061, CCLDV-BR-062, CCLDV-BR-063, CCLDV-BR-064, CCLDV-BR-065, CCLDV-BR-066, CCLDV-BR-080, CCLDV-BR-082, CCLDV-BR-083_
  - _After: CCLDV-C07-T1_
- [ ] CCLDV-C07-T4 [api] Build the services behind the screens
  - CCLDV-BR-067: Normalise the account number input: '*' or blank means 'not supplied' (null). Any other value is used both as the account to search by and as the account number held for the update.
  - CCLDV-BR-068: Normalise the card number input: '*' or blank means 'not supplied' (null). Any other value is used both as the card number to look up and as the card number held for the update.
  - CCLDV-BR-081: When the card is loaded, keep a snapshot of the original values in the update session: embossed name in upper case, expiry year, month and day split from the stored expiry date (characters 1-4, 6-7 and 9-10), active status and CVV. Use this snapshot for no-change detection and to check at save time whether someone else has changed the card.
  - _Requirements: CCLDV-REQ-F-065, CCLDV-REQ-F-075_
  - _Rules: CCLDV-BR-067, CCLDV-BR-068, CCLDV-BR-081_
  - _After: CCLDV-C07-T1, CCLDV-C07-T2, CCLDV-C07-T3_
- [ ] CCLDV-C07-T5 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **lookup field** "Account number": Required, an 11-digit number other than zeros: 'Account number not provided. Enter the 11-digit account number.' or 'Account filter, if supplied, must be an 11 digit number. Enter digits only.' Both fields empty: 'No input received. Enter the account and card number.' Account is checked before card, and focus moves to the first field in error.
  - **lookup field** "Card number": Required, a 16-digit number other than zeros: 'Card number not provided. Enter the 16-digit card number.' or 'Card ID filter, if supplied, must be a 16 digit number. Enter digits only.' No card with that number: 'Did not find cards for this search condition. Check the card number.'
  - **summary card** "Card"
  - _Requirements: CCLDV-REQ-F-064, CCLDV-REQ-F-073, CCLDV-REQ-F-077_
  - _Rules: CCLDV-BR-066, CCLDV-BR-077, CCLDV-BR-079, CCLDV-BR-084_
  - _After: CCLDV-C07-T2, CCLDV-C07-T3, CCLDV-C07-T4_
- [ ] CCLDV-C07-T6 [test-generation] Write a test for every acceptance criterion
  - 34 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-065, CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-074, CCLDV-REQ-F-075, CCLDV-REQ-F-076, CCLDV-REQ-F-077_
  - _Criteria: CCLDV-C07-AC-01, CCLDV-C07-AC-02, CCLDV-C07-AC-03, CCLDV-C07-AC-04, CCLDV-C07-AC-05, CCLDV-C07-AC-06, CCLDV-C07-AC-07, CCLDV-C07-AC-08, CCLDV-C07-AC-09, CCLDV-C07-AC-10, CCLDV-C07-AC-11, CCLDV-C07-AC-12, CCLDV-C07-AC-13, CCLDV-C07-AC-14, CCLDV-C07-AC-15, CCLDV-C07-AC-16, CCLDV-C07-AC-17, CCLDV-C07-AC-18, CCLDV-C07-AC-19, CCLDV-C07-AC-20, CCLDV-C07-AC-21, CCLDV-C07-AC-22, CCLDV-C07-AC-23, CCLDV-C07-AC-24, CCLDV-C07-AC-25, CCLDV-C07-AC-26, CCLDV-C07-AC-27, CCLDV-C07-AC-28, CCLDV-C07-AC-29, CCLDV-C07-AC-30, CCLDV-C07-AC-31, CCLDV-C07-AC-32, CCLDV-C07-AC-33, CCLDV-C07-AC-34_
  - _After: CCLDV-C07-T1, CCLDV-C07-T2, CCLDV-C07-T3, CCLDV-C07-T4, CCLDV-C07-T5_
- [ ] CCLDV-C07-T7 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-065, CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-074, CCLDV-REQ-F-075, CCLDV-REQ-F-076, CCLDV-REQ-F-077_
  - _After: CCLDV-C07-T1, CCLDV-C07-T2, CCLDV-C07-T3, CCLDV-C07-T4, CCLDV-C07-T5_

## CCLDV-C08 Edit and validate card details (draft)

- [ ] CCLDV-C08-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-087, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091, CCLDV-REQ-F-092_
- [ ] CCLDV-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091_
  - _Rules: CCLDV-BR-091, CCLDV-BR-092, CCLDV-BR-093, CCLDV-BR-094, CCLDV-BR-095, CCLDV-BR-096, CCLDV-BR-097, CCLDV-BR-098, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-102, CCLDV-BR-103, CCLDV-BR-104, CCLDV-BR-105_
  - _After: CCLDV-C08-T1_
- [ ] CCLDV-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-087, CCLDV-REQ-F-092_
  - _Rules: CCLDV-BR-101, CCLDV-BR-106_
  - _After: CCLDV-C08-T1_
- [ ] CCLDV-C08-T4 [api] Build the services behind the screens
  - CCLDV-BR-085: Normalise the editable card fields on submit: an embossed name, active status, expiry month or expiry year entered as '*' or left blank becomes 'not supplied' (null). Any other entry becomes the new value.
  - CCLDV-BR-086: Embossed name input: '*' or blank becomes 'not supplied'. Otherwise the entered text is the new embossed name, passed to the name check.
  - CCLDV-BR-087: Active status input: '*' or blank becomes 'not supplied', which the status check then rejects as not Y or N.
  - CCLDV-BR-088: Expiry month and expiry year inputs: '*' or blank becomes 'not supplied'. Otherwise the entered value is the new month or year, passed to the range checks.
  - CCLDV-BR-089: The expiry day is not normalised or validated. Carry it through exactly as the screen returns it. The screen shows the original expiry day, so in practice the stored day is kept.
  - CCLDV-BR-090: When building the expiry date to save, use the expiry day as returned by the screen, unchanged, together with the validated new year and month.
  - _Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079_
  - _Rules: CCLDV-BR-085, CCLDV-BR-086, CCLDV-BR-087, CCLDV-BR-088, CCLDV-BR-089, CCLDV-BR-090_
  - _After: CCLDV-C08-T1, CCLDV-C08-T2, CCLDV-C08-T3_
- [ ] CCLDV-C08-T5 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **summary card** "Name on card": Required, letters and spaces only: 'Card name not provided. Enter the name as it should appear on the card.' or 'Card name can only contain alphabets and spaces. Remove digits and symbols.'
  - **summary card** "Card active": One must be chosen; 'Card Active Status must be Y or N' becomes 'Choose Active or Inactive.'
  - **summary card** "Expiry month": 'Card expiry month must be between 1 and 12. Choose the month printed on the card.'
  - **summary card** "Expiry year": 'Invalid card expiry year. Enter a year from 1950 to 2099.'
  - **primary button** "Save card": Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year.
  - _Requirements: CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-088, CCLDV-REQ-F-090_
  - _Rules: CCLDV-BR-089, CCLDV-BR-090, CCLDV-BR-091, CCLDV-BR-092, CCLDV-BR-093, CCLDV-BR-095, CCLDV-BR-096, CCLDV-BR-097, CCLDV-BR-098, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-102, CCLDV-BR-104_
  - _After: CCLDV-C08-T2, CCLDV-C08-T3, CCLDV-C08-T4_
- [ ] CCLDV-C08-T6 [test-generation] Write a test for every acceptance criterion
  - 33 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-087, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091, CCLDV-REQ-F-092_
  - _Criteria: CCLDV-C08-AC-01, CCLDV-C08-AC-02, CCLDV-C08-AC-03, CCLDV-C08-AC-04, CCLDV-C08-AC-05, CCLDV-C08-AC-06, CCLDV-C08-AC-07, CCLDV-C08-AC-08, CCLDV-C08-AC-09, CCLDV-C08-AC-10, CCLDV-C08-AC-11, CCLDV-C08-AC-12, CCLDV-C08-AC-13, CCLDV-C08-AC-14, CCLDV-C08-AC-15, CCLDV-C08-AC-16, CCLDV-C08-AC-17, CCLDV-C08-AC-18, CCLDV-C08-AC-19, CCLDV-C08-AC-20, CCLDV-C08-AC-21, CCLDV-C08-AC-22, CCLDV-C08-AC-23, CCLDV-C08-AC-24, CCLDV-C08-AC-25, CCLDV-C08-AC-26, CCLDV-C08-AC-27, CCLDV-C08-AC-28, CCLDV-C08-AC-29, CCLDV-C08-AC-30, CCLDV-C08-AC-31, CCLDV-C08-AC-32, CCLDV-C08-AC-33_
  - _After: CCLDV-C08-T1, CCLDV-C08-T2, CCLDV-C08-T3, CCLDV-C08-T4, CCLDV-C08-T5_
- [ ] CCLDV-C08-T7 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-087, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091, CCLDV-REQ-F-092_
  - _After: CCLDV-C08-T1, CCLDV-C08-T2, CCLDV-C08-T3, CCLDV-C08-T4, CCLDV-C08-T5_

## CCLDV-C09 Confirm and save card changes (draft)

- [ ] CCLDV-C09-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-093, CCLDV-REQ-F-094, CCLDV-REQ-F-095, CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099_
- [ ] CCLDV-C09-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-093, CCLDV-REQ-F-094, CCLDV-REQ-F-095, CCLDV-REQ-F-097, CCLDV-REQ-F-099_
  - _Rules: CCLDV-BR-105, CCLDV-BR-107, CCLDV-BR-108, CCLDV-BR-109, CCLDV-BR-110, CCLDV-BR-114, CCLDV-BR-115, CCLDV-BR-116_
  - _After: CCLDV-C09-T1_
- [ ] CCLDV-C09-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-096, CCLDV-REQ-F-098_
  - _Rules: CCLDV-BR-111, CCLDV-BR-112, CCLDV-BR-113_
  - _After: CCLDV-C09-T1_
- [ ] CCLDV-C09-T4 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **primary button** "Save card": Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year.
  - _Requirements: CCLDV-REQ-F-094, CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099_
  - _Rules: CCLDV-BR-109, CCLDV-BR-111, CCLDV-BR-112, CCLDV-BR-113, CCLDV-BR-114, CCLDV-BR-115, CCLDV-BR-116_
  - _After: CCLDV-C09-T2, CCLDV-C09-T3_
- [ ] CCLDV-C09-T5 [test-generation] Write a test for every acceptance criterion
  - 14 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-093, CCLDV-REQ-F-094, CCLDV-REQ-F-095, CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099_
  - _Criteria: CCLDV-C09-AC-01, CCLDV-C09-AC-02, CCLDV-C09-AC-03, CCLDV-C09-AC-04, CCLDV-C09-AC-05, CCLDV-C09-AC-06, CCLDV-C09-AC-07, CCLDV-C09-AC-08, CCLDV-C09-AC-09, CCLDV-C09-AC-10, CCLDV-C09-AC-11, CCLDV-C09-AC-12, CCLDV-C09-AC-13, CCLDV-C09-AC-14_
  - _After: CCLDV-C09-T1, CCLDV-C09-T2, CCLDV-C09-T3, CCLDV-C09-T4_
- [ ] CCLDV-C09-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-093, CCLDV-REQ-F-094, CCLDV-REQ-F-095, CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099_
  - _After: CCLDV-C09-T1, CCLDV-C09-T2, CCLDV-C09-T3, CCLDV-C09-T4_

## CCLDV-C10 Leave or restart card update (draft)

- [ ] CCLDV-C10-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-100, CCLDV-REQ-F-101, CCLDV-REQ-F-102, CCLDV-REQ-F-103_
- [ ] CCLDV-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-100, CCLDV-REQ-F-103_
  - _Rules: CCLDV-BR-117, CCLDV-BR-120_
  - _After: CCLDV-C10-T1_
- [ ] CCLDV-C10-T3 [api] Build the services behind the screens
  - CCLDV-BR-118: When card update returns to the card list, clear the selected account and card numbers from the shared navigation context, so the list starts without a stale selection.
  - CCLDV-BR-119: On leaving card update, update the shared navigation context: sender = card update, user type = regular user, and mark the next screen's entry as a first entry so it starts fresh.
  - _Requirements: CCLDV-REQ-F-101, CCLDV-REQ-F-102_
  - _Rules: CCLDV-BR-118, CCLDV-BR-119_
  - _After: CCLDV-C10-T1, CCLDV-C10-T2_
- [ ] CCLDV-C10-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Cards"
  - _Requirements: CCLDV-REQ-F-100_
  - _Rules: CCLDV-BR-117_
  - _After: CCLDV-C10-T2, CCLDV-C10-T3_
- [ ] CCLDV-C10-T5 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-100, CCLDV-REQ-F-101, CCLDV-REQ-F-102, CCLDV-REQ-F-103_
  - _Criteria: CCLDV-C10-AC-01, CCLDV-C10-AC-02, CCLDV-C10-AC-03, CCLDV-C10-AC-04, CCLDV-C10-AC-05_
  - _After: CCLDV-C10-T1, CCLDV-C10-T2, CCLDV-C10-T3, CCLDV-C10-T4_
- [ ] CCLDV-C10-T6 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-100, CCLDV-REQ-F-101, CCLDV-REQ-F-102, CCLDV-REQ-F-103_
  - _After: CCLDV-C10-T1, CCLDV-C10-T2, CCLDV-C10-T3, CCLDV-C10-T4_

## CCLDV-C11 Save card changes (draft)

- [ ] CCLDV-C11-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105_
- [ ] CCLDV-C11-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-104_
  - _Rules: CCLDV-BR-121_
  - _After: CCLDV-C11-T1_
- [ ] CCLDV-C11-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-105_
  - _Rules: CCLDV-BR-122_
  - _After: CCLDV-C11-T1_
- [ ] CCLDV-C11-T4 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **primary button** "Save card": Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year.
  - _Requirements: CCLDV-REQ-F-104_
  - _Rules: CCLDV-BR-121_
  - _After: CCLDV-C11-T2, CCLDV-C11-T3_
- [ ] CCLDV-C11-T5 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105_
  - _Criteria: CCLDV-C11-AC-01, CCLDV-C11-AC-02_
  - _After: CCLDV-C11-T1, CCLDV-C11-T2, CCLDV-C11-T3, CCLDV-C11-T4_
- [ ] CCLDV-C11-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105_
  - _After: CCLDV-C11-T1, CCLDV-C11-T2, CCLDV-C11-T3, CCLDV-C11-T4_

## CPBM-C01 Export complete customer profiles for branch migration (draft)

- [ ] CPBM-C01-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-001, CPBM-REQ-F-002, CPBM-REQ-F-003, CPBM-REQ-F-004, CPBM-REQ-F-005, CPBM-REQ-F-006, CPBM-REQ-F-007_
- [ ] CPBM-C01-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-F-003, CPBM-REQ-F-006_
  - _Rules: CPBM-BR-003, CPBM-BR-006_
  - _After: CPBM-C01-T1_
- [ ] CPBM-C01-T3 [api] Build the scheduled job
  - CPBM-BR-001: A scheduled batch job that starts from an empty migration file every run (replace, never append), keyed by sequence number with room for a 500-character record, then runs the export with no parameters against the shared customer, account, cross-reference, transaction and card data, writing its messages to the job log.
  - CPBM-BR-002: One run: take the timestamp, open all five sources and the target, then stream each source in its key order — customers, accounts, cross-references, transactions, cards — one after another; a sorted extract per source in key order, never interleaved.
  - CPBM-BR-004: A one-to-one mapping from each source record to an export record tagged with its type code ('C', 'A', 'X', 'T', 'D') and carrying that record's fields; the migration file is a tagged union of the five record layouts.
  - CPBM-BR-005: A single counter starting at 1, incremented for each record written across all types in output order, used as the unique key of the migration file; the last value equals the total written.
  - CPBM-BR-007: Format the run timestamp from the system clock as 'YYYY-MM-DD HH:MM:SS.00', with the fraction fixed at '00' rather than real hundredths.
  - CPBM-BR-008: Capture the timestamp once at run start and reuse that value on every record; do not read the clock per record.
  - _Requirements: CPBM-REQ-F-001, CPBM-REQ-F-002, CPBM-REQ-F-004, CPBM-REQ-F-005, CPBM-REQ-F-007_
  - _Rules: CPBM-BR-001, CPBM-BR-002, CPBM-BR-004, CPBM-BR-005, CPBM-BR-007, CPBM-BR-008_
  - _After: CPBM-C01-T1, CPBM-C01-T2_
- [ ] CPBM-C01-T4 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-001, CPBM-REQ-F-002, CPBM-REQ-F-003, CPBM-REQ-F-004, CPBM-REQ-F-005, CPBM-REQ-F-006, CPBM-REQ-F-007_
  - _Criteria: CPBM-C01-AC-01, CPBM-C01-AC-02, CPBM-C01-AC-03, CPBM-C01-AC-04, CPBM-C01-AC-05, CPBM-C01-AC-06, CPBM-C01-AC-07, CPBM-C01-AC-08, CPBM-C01-AC-09, CPBM-C01-AC-10_
  - _After: CPBM-C01-T1, CPBM-C01-T2, CPBM-C01-T3_
- [ ] CPBM-C01-T5 [compliance] Review the handling of card data, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-001, CPBM-REQ-F-002, CPBM-REQ-F-003, CPBM-REQ-F-004, CPBM-REQ-F-005, CPBM-REQ-F-006, CPBM-REQ-F-007_
  - _After: CPBM-C01-T1, CPBM-C01-T2, CPBM-C01-T3_

## CPBM-C02 Carry sensitive customer and card data in the export (draft)

- [ ] CPBM-C02-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
- [ ] CPBM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
  - _Rules: CPBM-BR-009, CPBM-BR-010, CPBM-BR-011_
  - _After: CPBM-C02-T1_
- [ ] CPBM-C02-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
  - _Rules: CPBM-BR-009, CPBM-BR-010, CPBM-BR-011_
  - _After: CPBM-C02-T1, CPBM-C02-T2_
- [ ] CPBM-C02-T4 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
  - _Criteria: CPBM-C02-AC-01, CPBM-C02-AC-02, CPBM-C02-AC-03, CPBM-C02-AC-04_
  - _After: CPBM-C02-T1, CPBM-C02-T2, CPBM-C02-T3_
- [ ] CPBM-C02-T5 [compliance] Review the handling of card data, personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-N-001, CPBM-REQ-N-002, CPBM-REQ-N-003_
  - _After: CPBM-C02-T1, CPBM-C02-T2, CPBM-C02-T3_

## CPBM-C03 Report export reconciliation counts (draft)

- [ ] CPBM-C03-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
- [ ] CPBM-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
  - _Rules: CPBM-BR-012, CPBM-BR-013_
  - _After: CPBM-C03-T1_
- [ ] CPBM-C03-T3 [api] Build the service
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
  - _Rules: CPBM-BR-012, CPBM-BR-013_
  - _After: CPBM-C03-T1, CPBM-C03-T2_
- [ ] CPBM-C03-T4 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
  - _Criteria: CPBM-C03-AC-01, CPBM-C03-AC-02_
  - _After: CPBM-C03-T1, CPBM-C03-T2, CPBM-C03-T3_
- [ ] CPBM-C03-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-008, CPBM-REQ-F-009_
  - _After: CPBM-C03-T1, CPBM-C03-T2, CPBM-C03-T3_

## CPBM-C04 Stop the export on any file error (draft)

- [ ] CPBM-C04-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
- [ ] CPBM-C04-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
  - _Rules: CPBM-BR-014, CPBM-BR-015, CPBM-BR-016_
  - _After: CPBM-C04-T1_
- [ ] CPBM-C04-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
  - _Rules: CPBM-BR-014, CPBM-BR-015, CPBM-BR-016_
  - _After: CPBM-C04-T1, CPBM-C04-T2_
- [ ] CPBM-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
  - _Criteria: CPBM-C04-AC-01, CPBM-C04-AC-02, CPBM-C04-AC-03, CPBM-C04-AC-04, CPBM-C04-AC-05, CPBM-C04-AC-06_
  - _After: CPBM-C04-T1, CPBM-C04-T2, CPBM-C04-T3_
- [ ] CPBM-C04-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-010, CPBM-REQ-F-011, CPBM-REQ-F-012_
  - _After: CPBM-C04-T1, CPBM-C04-T2, CPBM-C04-T3_

## CPBM-C05 Import and split the migration file into target files (draft)

- [ ] CPBM-C05-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-013, CPBM-REQ-F-014, CPBM-REQ-F-015, CPBM-REQ-F-016, CPBM-REQ-F-017, CPBM-REQ-F-018, CPBM-REQ-F-019, CPBM-REQ-F-020, CPBM-REQ-F-021_
- [ ] CPBM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-F-015, CPBM-REQ-F-016, CPBM-REQ-F-020, CPBM-REQ-F-021_
  - _Rules: CPBM-BR-019, CPBM-BR-020, CPBM-BR-024, CPBM-BR-025_
  - _After: CPBM-C05-T1_
- [ ] CPBM-C05-T3 [api] Build the scheduled job
  - CPBM-BR-017: A scheduled import job that reads the shared migration file and creates fresh customer (500-character), account (300), cross-reference (50) and transaction (350) target files plus a 132-character error report; the outputs are kept only if the step succeeds and are removed if it fails.
  - CPBM-BR-018: The legacy job sets up no card target although the program writes card records to one; the new job must provide a card target explicitly (a known gap to confirm, not behaviour to copy).
  - CPBM-BR-021: Map an 'A' record field for field to an account record (number, active status, current balance, credit limit, cash credit limit, open/expiration/reissue dates, current-cycle credit and debit, zip, group id) and write it to the account target; any write failure stops the run.
  - CPBM-BR-022: Map an 'X' record to a cross-reference row linking card number, customer number and account number, and write it to the cross-reference target; any write failure stops the run.
  - CPBM-BR-023: Map a 'T' record field for field to a transaction record and write it to the transaction target; any write failure stops the run.
  - _Requirements: CPBM-REQ-F-013, CPBM-REQ-F-014, CPBM-REQ-F-017, CPBM-REQ-F-018, CPBM-REQ-F-019_
  - _Rules: CPBM-BR-017, CPBM-BR-018, CPBM-BR-021, CPBM-BR-022, CPBM-BR-023_
  - _After: CPBM-C05-T1, CPBM-C05-T2_
- [ ] CPBM-C05-T4 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-013, CPBM-REQ-F-014, CPBM-REQ-F-015, CPBM-REQ-F-016, CPBM-REQ-F-017, CPBM-REQ-F-018, CPBM-REQ-F-019, CPBM-REQ-F-020, CPBM-REQ-F-021_
  - _Criteria: CPBM-C05-AC-01, CPBM-C05-AC-02, CPBM-C05-AC-03, CPBM-C05-AC-04, CPBM-C05-AC-05, CPBM-C05-AC-06, CPBM-C05-AC-07, CPBM-C05-AC-08, CPBM-C05-AC-09, CPBM-C05-AC-10, CPBM-C05-AC-11, CPBM-C05-AC-12, CPBM-C05-AC-13_
  - _After: CPBM-C05-T1, CPBM-C05-T2, CPBM-C05-T3_
- [ ] CPBM-C05-T5 [compliance] Review the handling of card data, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-013, CPBM-REQ-F-014, CPBM-REQ-F-015, CPBM-REQ-F-016, CPBM-REQ-F-017, CPBM-REQ-F-018, CPBM-REQ-F-019, CPBM-REQ-F-020, CPBM-REQ-F-021_
  - _After: CPBM-C05-T1, CPBM-C05-T2, CPBM-C05-T3_

## CPBM-C06 Log unknown record types during import (draft)

- [ ] CPBM-C06-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
- [ ] CPBM-C06-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
  - _Rules: CPBM-BR-026, CPBM-BR-027, CPBM-BR-028_
  - _After: CPBM-C06-T1_
- [ ] CPBM-C06-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
  - _Rules: CPBM-BR-026, CPBM-BR-027, CPBM-BR-028_
  - _After: CPBM-C06-T1, CPBM-C06-T2_
- [ ] CPBM-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
  - _Criteria: CPBM-C06-AC-01, CPBM-C06-AC-02, CPBM-C06-AC-03, CPBM-C06-AC-04_
  - _After: CPBM-C06-T1, CPBM-C06-T2, CPBM-C06-T3_
- [ ] CPBM-C06-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-022, CPBM-REQ-F-023_
  - _After: CPBM-C06-T1, CPBM-C06-T2, CPBM-C06-T3_

## CPBM-C07 Report import run statistics (draft)

- [ ] CPBM-C07-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
- [ ] CPBM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CPBM-BR-030, CPBM-BR-031.
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
  - _Rules: CPBM-BR-029, CPBM-BR-030, CPBM-BR-031_
  - _After: CPBM-C07-T1_
- [ ] CPBM-C07-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
  - _Rules: CPBM-BR-029, CPBM-BR-030, CPBM-BR-031_
  - _After: CPBM-C07-T1, CPBM-C07-T2_
- [ ] CPBM-C07-T4 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
  - _Criteria: CPBM-C07-AC-01, CPBM-C07-AC-02, CPBM-C07-AC-03, CPBM-C07-AC-04, CPBM-C07-AC-05_
  - _After: CPBM-C07-T1, CPBM-C07-T2, CPBM-C07-T3_
- [ ] CPBM-C07-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-024, CPBM-REQ-F-025_
  - _After: CPBM-C07-T1, CPBM-C07-T2, CPBM-C07-T3_

## CPBM-C08 Abort the import on any file failure (draft)

- [ ] CPBM-C08-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029_
- [ ] CPBM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-F-028_
  - _Rules: CPBM-BR-020, CPBM-BR-021, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-034_
  - _After: CPBM-C08-T1_
- [ ] CPBM-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-029_
  - _Rules: CPBM-BR-017, CPBM-BR-032, CPBM-BR-033, CPBM-BR-035_
  - _After: CPBM-C08-T1_
- [ ] CPBM-C08-T4 [api] Build the scheduled job
  - CPBM-BR-021: The account write must report failure to the job, so that a failed write stops the whole import rather than being skipped.
  - CPBM-BR-022: The cross-reference write must report failure to the job, so that a failed write stops the whole import.
  - CPBM-BR-023: The transaction write must report failure to the job, so that a failed write stops the whole import.
  - CPBM-BR-017: Make the import all-or-nothing: write the targets to staging (or inside a transaction) and publish them only when the step succeeds; on an abnormal end, remove the customer, account, cross-reference, transaction and error outputs.
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029_
  - _Rules: CPBM-BR-017, CPBM-BR-020, CPBM-BR-021, CPBM-BR-022, CPBM-BR-023, CPBM-BR-024, CPBM-BR-032, CPBM-BR-033, CPBM-BR-034, CPBM-BR-035_
  - _After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3_
- [ ] CPBM-C08-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029_
  - _Criteria: CPBM-C08-AC-01, CPBM-C08-AC-02, CPBM-C08-AC-03, CPBM-C08-AC-04, CPBM-C08-AC-05, CPBM-C08-AC-06, CPBM-C08-AC-07, CPBM-C08-AC-08, CPBM-C08-AC-09, CPBM-C08-AC-10_
  - _After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3, CPBM-C08-T4_
- [ ] CPBM-C08-T6 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-026, CPBM-REQ-F-027, CPBM-REQ-F-028, CPBM-REQ-F-029_
  - _After: CPBM-C08-T1, CPBM-C08-T2, CPBM-C08-T3, CPBM-C08-T4_

## MDFI-C01 Load account master (draft)

- [ ] MDFI-C01-T1 [api] Build the scheduled job
  - MDFI-BR-001: The scheduled load job starts by clearing out the account store (drop and recreate, or truncate the accounts table). It must succeed whether or not the store already exists. The rebuilt store has the 11-digit account ID as its unique primary key, so later processing can look up an account by its ID.
  - MDFI-BR-002: A bulk import that reads every record of the account extract file into the freshly emptied account store, keyed by account ID. The job should check that the number of rows loaded equals the number of input records, and it should fail visibly rather than load only part of the file.
  - _Requirements: MDFI-REQ-F-001, MDFI-REQ-F-002_
  - _Rules: MDFI-BR-001, MDFI-BR-002_
- [ ] MDFI-C01-T2 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: MDFI-REQ-F-001, MDFI-REQ-F-002_
  - _Criteria: MDFI-C01-AC-01, MDFI-C01-AC-02_
  - _After: MDFI-C01-T1_

## MDFI-C02 Load card master and its account index (draft)

- [ ] MDFI-C02-T1 [api] Build the scheduled job
  - MDFI-BR-003: A scheduled bulk import that copies every record of the card extract file into the card store, keyed on card number. The shared access in the old job means the load must not lock out other readers of the source file. Row counts should be reconciled against the input.
  - MDFI-BR-004: Add a non-unique secondary index on the card's 11-character account ID column, which sits right after the card number in the legacy record (position 17). The database must keep this index up to date automatically on every insert, update and delete, and it must be queryable as 'cards for account X'.
  - MDFI-BR-005: Build or refresh the account-ID index only after the card load has finished, either as the last step of the load job or by creating the index after the bulk insert. That way, lookups by account show every loaded card.
  - _Requirements: MDFI-REQ-F-003, MDFI-REQ-F-004, MDFI-REQ-F-005_
  - _Rules: MDFI-BR-003, MDFI-BR-004, MDFI-BR-005_
- [ ] MDFI-C02-T2 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: MDFI-REQ-F-003, MDFI-REQ-F-004, MDFI-REQ-F-005_
  - _Criteria: MDFI-C02-AC-01, MDFI-C02-AC-02, MDFI-C02-AC-03_
  - _After: MDFI-C02-T1_
- [ ] MDFI-C02-T3 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: MDFI-REQ-F-003, MDFI-REQ-F-004, MDFI-REQ-F-005_
  - _After: MDFI-C02-T1_

## MDFI-C03 Refresh customer master (draft)

- [ ] MDFI-C03-T1 [api] Build the scheduled job
  - MDFI-BR-006: Before the reload starts, the job must tell the online application to stop serving customer data, for example with a maintenance flag, a message, or an admin API call that makes customer reads return 'temporarily unavailable'. When the load is done it must turn customer access back on. Alternatively, the job can load into a staging table and swap it in atomically, so online users never see a partial store.
  - MDFI-BR-007: Recreate or empty the customer store with the 9-character customer ID as its unique key. Each customer record holds the fields of the 500-byte legacy layout. A store that does not exist yet must not make the job fail.
  - MDFI-BR-008: A bulk import of every record in the customer extract file into the new customer store. It must produce a run report, at least the records read and written plus any errors, and keep it as the job's output or log for operations.
  - _Requirements: MDFI-REQ-F-006, MDFI-REQ-F-007, MDFI-REQ-F-008_
  - _Rules: MDFI-BR-006, MDFI-BR-007, MDFI-BR-008_
- [ ] MDFI-C03-T2 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: MDFI-REQ-F-006, MDFI-REQ-F-007, MDFI-REQ-F-008_
  - _Criteria: MDFI-C03-AC-01, MDFI-C03-AC-02, MDFI-C03-AC-03, MDFI-C03-AC-04_
  - _After: MDFI-C03-T1_
- [ ] MDFI-C03-T3 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: MDFI-REQ-F-006, MDFI-REQ-F-007, MDFI-REQ-F-008_
  - _After: MDFI-C03-T1_

## MDFI-C04 Load card cross-reference master and its account index (draft)

- [ ] MDFI-C04-T1 [api] Build the scheduled job
  - MDFI-BR-009: The scheduled job drops or empties the cross-reference store and its by-account index, and it must succeed even if they do not exist yet. It then recreates the store with the 16-character card number as its unique primary key.
  - MDFI-BR-010: A bulk import of every card cross-reference record from the extract file into the new store, keyed on card number. The loaded row count should be reconciled against the input file.
  - MDFI-BR-011: After the load, create a non-unique secondary index on account ID over every cross-reference record. This supports the query 'all cards for account X', which can return many cards for one account. In a relational store, the index itself replaces the separate index and access-path objects of the old job.
  - _Requirements: MDFI-REQ-F-009, MDFI-REQ-F-010, MDFI-REQ-F-011_
  - _Rules: MDFI-BR-009, MDFI-BR-010, MDFI-BR-011_
- [ ] MDFI-C04-T2 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: MDFI-REQ-F-009, MDFI-REQ-F-010, MDFI-REQ-F-011_
  - _Criteria: MDFI-C04-AC-01, MDFI-C04-AC-02, MDFI-C04-AC-03_
  - _After: MDFI-C04-T1_
- [ ] MDFI-C04-T3 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: MDFI-REQ-F-009, MDFI-REQ-F-010, MDFI-REQ-F-011_
  - _After: MDFI-C04-T1_

## TTRDM-C01 Batch maintenance of transaction types (draft)

- [ ] TTRDM-C01-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-001, TTRDM-REQ-F-002, TTRDM-REQ-F-003, TTRDM-REQ-F-004, TTRDM-REQ-F-006, TTRDM-REQ-F-009_
  - _Rules: TTRDM-BR-001, TTRDM-BR-002, TTRDM-BR-003, TTRDM-BR-004, TTRDM-BR-006, TTRDM-BR-010_
- [ ] TTRDM-C01-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-005, TTRDM-REQ-F-007, TTRDM-REQ-F-008, TTRDM-REQ-F-010, TTRDM-REQ-F-011, TTRDM-REQ-N-001_
  - _Rules: TTRDM-BR-005, TTRDM-BR-007, TTRDM-BR-008, TTRDM-BR-009, TTRDM-BR-011, TTRDM-BR-012, TTRDM-BR-013_
- [ ] TTRDM-C01-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: TTRDM-REQ-F-001, TTRDM-REQ-F-002, TTRDM-REQ-F-003, TTRDM-REQ-F-004, TTRDM-REQ-F-005, TTRDM-REQ-F-006, TTRDM-REQ-F-007, TTRDM-REQ-F-008, TTRDM-REQ-F-009, TTRDM-REQ-F-010, TTRDM-REQ-F-011, TTRDM-REQ-N-001_
  - _Rules: TTRDM-BR-001, TTRDM-BR-002, TTRDM-BR-003, TTRDM-BR-004, TTRDM-BR-005, TTRDM-BR-006, TTRDM-BR-007, TTRDM-BR-008, TTRDM-BR-009, TTRDM-BR-010, TTRDM-BR-011, TTRDM-BR-012, TTRDM-BR-013_
  - _After: TTRDM-C01-T1, TTRDM-C01-T2_
- [ ] TTRDM-C01-T4 [test-generation] Write a test for every acceptance criterion
  - 16 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-001, TTRDM-REQ-F-002, TTRDM-REQ-F-003, TTRDM-REQ-F-004, TTRDM-REQ-F-005, TTRDM-REQ-F-006, TTRDM-REQ-F-007, TTRDM-REQ-F-008, TTRDM-REQ-F-009, TTRDM-REQ-F-010, TTRDM-REQ-F-011, TTRDM-REQ-N-001_
  - _Criteria: TTRDM-C01-AC-01, TTRDM-C01-AC-02, TTRDM-C01-AC-03, TTRDM-C01-AC-04, TTRDM-C01-AC-05, TTRDM-C01-AC-06, TTRDM-C01-AC-07, TTRDM-C01-AC-08, TTRDM-C01-AC-09, TTRDM-C01-AC-10, TTRDM-C01-AC-11, TTRDM-C01-AC-12, TTRDM-C01-AC-13, TTRDM-C01-AC-14, TTRDM-C01-AC-15, TTRDM-C01-AC-16_
  - _After: TTRDM-C01-T1, TTRDM-C01-T2, TTRDM-C01-T3_

## TTRDM-C02 Enter and leave the transaction type list (draft)

- [ ] TTRDM-C02-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013, TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016_
- [ ] TTRDM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013_
  - _Rules: TTRDM-BR-014, TTRDM-BR-015, TTRDM-BR-016, TTRDM-BR-017, TTRDM-BR-018_
  - _After: TTRDM-C02-T1_
- [ ] TTRDM-C02-T3 [api] Build the services behind the screens
  - TTRDM-BR-015: The list keeps per-user view state (filters, selected row, page number, first and last code on the page). When the user navigates to the list from any other screen, that state must be reset, not restored, and the first page loaded.
  - TTRDM-BR-016: Opening the list from another screen is handled exactly like a plain refresh (Enter): clear filters and paging and load page 1 from the lowest type code. A route or entry parameter telling the list it was opened fresh is enough; no previous view state is carried over.
  - TTRDM-BR-017: Coming back from the add/change transaction type screen via its Back/Exit action counts as a fresh entry to the list: the list must not interpret it as its own exit, and must load page 1 with no filters.
  - TTRDM-BR-018: Same as returning from the add/change screen: the back navigation lands on a freshly reset list (page 1, no filters, no selection); any earlier list state is discarded rather than restored.
  - TTRDM-BR-019: Exit from the list finishes any open unit of work (commit) and navigates back to the screen that opened it; if it was opened directly or there is no recorded caller other than itself, navigate to the admin menu. The navigation needs a recorded 'return to' target in the user's session.
  - TTRDM-BR-020: When the list form is submitted, the server reads the submitted form and validates in a fixed order: row actions, then the description filter, then the type code filter, then a count of records matching the filters. Keep this order, since it decides which error message the user sees first.
  - TTRDM-BR-021: Page numbers start at 1: when the first page is loaded on a fresh start, the page number in the view state is set to 1, not left at 0.
  - _Requirements: TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016_
  - _Rules: TTRDM-BR-019, TTRDM-BR-020, TTRDM-BR-021_
  - _After: TTRDM-C02-T1, TTRDM-C02-T2_
- [ ] TTRDM-C02-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
  - _Requirements: TTRDM-REQ-F-014_
  - _Rules: TTRDM-BR-019_
  - _After: TTRDM-C02-T2, TTRDM-C02-T3_
- [ ] TTRDM-C02-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-012, TTRDM-REQ-F-013, TTRDM-REQ-F-014, TTRDM-REQ-F-015, TTRDM-REQ-F-016_
  - _Criteria: TTRDM-C02-AC-01, TTRDM-C02-AC-02, TTRDM-C02-AC-03, TTRDM-C02-AC-04, TTRDM-C02-AC-05, TTRDM-C02-AC-06, TTRDM-C02-AC-07, TTRDM-C02-AC-08, TTRDM-C02-AC-09, TTRDM-C02-AC-10, TTRDM-C02-AC-11_
  - _After: TTRDM-C02-T1, TTRDM-C02-T2, TTRDM-C02-T3, TTRDM-C02-T4_

## TTRDM-C03 Page through transaction types (draft)

- [ ] TTRDM-C03-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-017, TTRDM-REQ-F-018, TTRDM-REQ-F-019, TTRDM-REQ-F-020, TTRDM-REQ-F-021, TTRDM-REQ-F-022, TTRDM-REQ-F-023, TTRDM-REQ-F-024, TTRDM-REQ-F-025, TTRDM-REQ-F-026, TTRDM-REQ-F-027, TTRDM-REQ-F-028, TTRDM-REQ-F-029, TTRDM-REQ-F-030, TTRDM-REQ-F-031_
- [ ] TTRDM-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-018, TTRDM-REQ-F-019, TTRDM-REQ-F-020, TTRDM-REQ-F-021, TTRDM-REQ-F-024_
  - _Rules: TTRDM-BR-023, TTRDM-BR-024, TTRDM-BR-025, TTRDM-BR-026, TTRDM-BR-027, TTRDM-BR-030_
  - _After: TTRDM-C03-T1_
- [ ] TTRDM-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-030, TTRDM-REQ-F-031, TTRDM-REQ-F-017, TTRDM-REQ-F-022, TTRDM-REQ-F-023, TTRDM-REQ-F-025, TTRDM-REQ-F-026, TTRDM-REQ-F-027, TTRDM-REQ-F-028, TTRDM-REQ-F-029_
  - _Rules: TTRDM-BR-022, TTRDM-BR-028, TTRDM-BR-029, TTRDM-BR-031, TTRDM-BR-032, TTRDM-BR-033, TTRDM-BR-034, TTRDM-BR-035, TTRDM-BR-036, TTRDM-BR-037_
  - _After: TTRDM-C03-T1_
- [ ] TTRDM-C03-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **data table** "Transaction types": In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes.
  - _Requirements: TTRDM-REQ-F-017_
  - _Rules: TTRDM-BR-022_
  - _After: TTRDM-C03-T2, TTRDM-C03-T3_
- [ ] TTRDM-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 21 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-017, TTRDM-REQ-F-018, TTRDM-REQ-F-019, TTRDM-REQ-F-020, TTRDM-REQ-F-021, TTRDM-REQ-F-022, TTRDM-REQ-F-023, TTRDM-REQ-F-024, TTRDM-REQ-F-025, TTRDM-REQ-F-026, TTRDM-REQ-F-027, TTRDM-REQ-F-028, TTRDM-REQ-F-029, TTRDM-REQ-F-030, TTRDM-REQ-F-031_
  - _Criteria: TTRDM-C03-AC-01, TTRDM-C03-AC-02, TTRDM-C03-AC-03, TTRDM-C03-AC-04, TTRDM-C03-AC-05, TTRDM-C03-AC-06, TTRDM-C03-AC-07, TTRDM-C03-AC-08, TTRDM-C03-AC-09, TTRDM-C03-AC-10, TTRDM-C03-AC-11, TTRDM-C03-AC-12, TTRDM-C03-AC-13, TTRDM-C03-AC-14, TTRDM-C03-AC-15, TTRDM-C03-AC-16, TTRDM-C03-AC-17, TTRDM-C03-AC-18, TTRDM-C03-AC-19, TTRDM-C03-AC-20, TTRDM-C03-AC-21_
  - _After: TTRDM-C03-T1, TTRDM-C03-T2, TTRDM-C03-T3, TTRDM-C03-T4_

## TTRDM-C04 Filter the transaction type list (draft)

- [ ] TTRDM-C04-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034, TTRDM-REQ-F-035, TTRDM-REQ-F-036, TTRDM-REQ-F-037, TTRDM-REQ-F-038, TTRDM-REQ-F-039, TTRDM-REQ-F-040_
- [ ] TTRDM-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034, TTRDM-REQ-F-037, TTRDM-REQ-F-038, TTRDM-REQ-F-039_
  - _Rules: TTRDM-BR-038, TTRDM-BR-039, TTRDM-BR-040, TTRDM-BR-041, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-046_
  - _After: TTRDM-C04-T1_
- [ ] TTRDM-C04-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-040_
  - _Rules: TTRDM-BR-047_
  - _After: TTRDM-C04-T1_
- [ ] TTRDM-C04-T4 [api] Build the services behind the screens
  - TTRDM-BR-042: The view state keeps the type code filter used for the last page shown. When the submitted filter differs, reset paging to page 1, store the new filter and mark it changed; a pending update/delete confirmation must then be treated as a plain refresh, not applied.
  - TTRDM-BR-043: When the submitted type code filter equals the stored one (two empty values count as equal), keep the current page and mark the filter unchanged, so a pending confirmation can still proceed.
  - _Requirements: TTRDM-REQ-F-035, TTRDM-REQ-F-036_
  - _Rules: TTRDM-BR-042, TTRDM-BR-043_
  - _After: TTRDM-C04-T1, TTRDM-C04-T2, TTRDM-C04-T3_
- [ ] TTRDM-C04-T5 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **lookup field** "Type code": 'Type code filter, if supplied, must be a 2 digit number. Enter two digits, for example 01, or leave it blank.' No type matches: 'No Records found for these filter conditions. Change or clear the filters.'
  - **lookup field** "Description contains": Checked against the data only when a filter holds a value: 'No Records found for these filter conditions. Change or clear the filters.'
  - _Requirements: TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034, TTRDM-REQ-F-037, TTRDM-REQ-F-038_
  - _Rules: TTRDM-BR-038, TTRDM-BR-039, TTRDM-BR-040, TTRDM-BR-041, TTRDM-BR-044, TTRDM-BR-045_
  - _After: TTRDM-C04-T2, TTRDM-C04-T3, TTRDM-C04-T4_
- [ ] TTRDM-C04-T6 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034, TTRDM-REQ-F-035, TTRDM-REQ-F-036, TTRDM-REQ-F-037, TTRDM-REQ-F-038, TTRDM-REQ-F-039, TTRDM-REQ-F-040_
  - _Criteria: TTRDM-C04-AC-01, TTRDM-C04-AC-02, TTRDM-C04-AC-03, TTRDM-C04-AC-04, TTRDM-C04-AC-05, TTRDM-C04-AC-06, TTRDM-C04-AC-07, TTRDM-C04-AC-08, TTRDM-C04-AC-09, TTRDM-C04-AC-10, TTRDM-C04-AC-11, TTRDM-C04-AC-12_
  - _After: TTRDM-C04-T1, TTRDM-C04-T2, TTRDM-C04-T3, TTRDM-C04-T4, TTRDM-C04-T5_

## TTRDM-C05 Update transaction type descriptions from the list (draft)

- [ ] TTRDM-C05-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042, TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-047, TTRDM-REQ-F-048, TTRDM-REQ-F-049, TTRDM-REQ-F-050, TTRDM-REQ-F-051_
- [ ] TTRDM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-050_
  - _Rules: TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053, TTRDM-BR-057_
  - _After: TTRDM-C05-T1_
- [ ] TTRDM-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-047, TTRDM-REQ-F-048, TTRDM-REQ-F-049, TTRDM-REQ-F-051_
  - _Rules: TTRDM-BR-054, TTRDM-BR-055, TTRDM-BR-056, TTRDM-BR-058_
  - _After: TTRDM-C05-T1_
- [ ] TTRDM-C05-T4 [api] Build the services behind the screens
  - TTRDM-BR-048: The list form submits the two filters and, for each of up to 7 rows, the action code, type code and description. The server binds these into a request model, treating a description of '*' or only spaces as not entered and trimming any other description.
  - TTRDM-BR-049: Normalise each submitted row description on input: blank or a lone '*' becomes 'not entered' (null); any other value is trimmed of leading and trailing spaces before comparison and validation.
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042_
  - _Rules: TTRDM-BR-048, TTRDM-BR-049_
  - _After: TTRDM-C05-T1, TTRDM-C05-T2, TTRDM-C05-T3_
- [ ] TTRDM-C05-T5 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **data table** "Transaction types": In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes.
  - _Requirements: TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046_
  - _Rules: TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053_
  - _After: TTRDM-C05-T2, TTRDM-C05-T3, TTRDM-C05-T4_
- [ ] TTRDM-C05-T6 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042, TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-047, TTRDM-REQ-F-048, TTRDM-REQ-F-049, TTRDM-REQ-F-050, TTRDM-REQ-F-051_
  - _Criteria: TTRDM-C05-AC-01, TTRDM-C05-AC-02, TTRDM-C05-AC-03, TTRDM-C05-AC-04, TTRDM-C05-AC-05, TTRDM-C05-AC-06, TTRDM-C05-AC-07, TTRDM-C05-AC-08, TTRDM-C05-AC-09, TTRDM-C05-AC-10, TTRDM-C05-AC-11, TTRDM-C05-AC-12, TTRDM-C05-AC-13_
  - _After: TTRDM-C05-T1, TTRDM-C05-T2, TTRDM-C05-T3, TTRDM-C05-T4, TTRDM-C05-T5_

## TTRDM-C06 Access to transaction type maintenance (draft)

- [ ] TTRDM-C06-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
- [ ] TTRDM-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
  - _Rules: TTRDM-BR-059, TTRDM-BR-060_
  - _After: TTRDM-C06-T1_
- [ ] TTRDM-C06-T3 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
  - _Rules: TTRDM-BR-059, TTRDM-BR-060_
  - _After: TTRDM-C06-T2_
- [ ] TTRDM-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
  - _Criteria: TTRDM-C06-AC-01, TTRDM-C06-AC-02_
  - _After: TTRDM-C06-T1, TTRDM-C06-T2, TTRDM-C06-T3_
- [ ] TTRDM-C06-T5 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
  - _After: TTRDM-C06-T1, TTRDM-C06-T2, TTRDM-C06-T3_

## TTRDM-C07 Filter the transaction type list (draft)

- [ ] TTRDM-C07-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054, TTRDM-REQ-F-055_
- [ ] TTRDM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054_
  - _Rules: TTRDM-BR-061, TTRDM-BR-062, TTRDM-BR-063_
  - _After: TTRDM-C07-T1_
- [ ] TTRDM-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-055_
  - _Rules: TTRDM-BR-064_
  - _After: TTRDM-C07-T1_
- [ ] TTRDM-C07-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **lookup field** "Type code": 'Type code filter, if supplied, must be a 2 digit number. Enter two digits, for example 01, or leave it blank.' No type matches: 'No Records found for these filter conditions. Change or clear the filters.'
  - **lookup field** "Description contains": Checked against the data only when a filter holds a value: 'No Records found for these filter conditions. Change or clear the filters.'
  - _Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-054_
  - _Rules: TTRDM-BR-061, TTRDM-BR-063_
  - _After: TTRDM-C07-T2, TTRDM-C07-T3_
- [ ] TTRDM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054, TTRDM-REQ-F-055_
  - _Criteria: TTRDM-C07-AC-01, TTRDM-C07-AC-02, TTRDM-C07-AC-03, TTRDM-C07-AC-04_
  - _After: TTRDM-C07-T1, TTRDM-C07-T2, TTRDM-C07-T3, TTRDM-C07-T4_

## TTRDM-C08 Mark a list row for update or delete (draft)

- [ ] TTRDM-C08-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-056, TTRDM-REQ-F-057, TTRDM-REQ-F-058, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061, TTRDM-REQ-F-062, TTRDM-REQ-F-063, TTRDM-REQ-F-064_
- [ ] TTRDM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-056, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061, TTRDM-REQ-F-062, TTRDM-REQ-F-063_
  - _Rules: TTRDM-BR-065, TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070, TTRDM-BR-071, TTRDM-BR-072_
  - _After: TTRDM-C08-T1_
- [ ] TTRDM-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-064_
  - _Rules: TTRDM-BR-073_
  - _After: TTRDM-C08-T1_
- [ ] TTRDM-C08-T4 [api] Build the services behind the screens
  - TTRDM-BR-066: When the filters are unchanged, validation counts the non-blank row actions across the 7 submitted rows, and separately the 'D' and 'U' rows; these counts drive the 'only one action' and confirmation-prompt rules.
  - TTRDM-BR-067: The view state records the selected row (the top-most row marked 'D' or 'U', or none) and compares it with the selection stored from the previous screen; a changed selection cancels any pending confirmation.
  - _Requirements: TTRDM-REQ-F-057, TTRDM-REQ-F-058_
  - _Rules: TTRDM-BR-066, TTRDM-BR-067_
  - _After: TTRDM-C08-T1, TTRDM-C08-T2, TTRDM-C08-T3_
- [ ] TTRDM-C08-T5 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **data table** "Transaction types": In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes.
  - _Requirements: TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-062, TTRDM-REQ-F-063_
  - _Rules: TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-071, TTRDM-BR-072_
  - _After: TTRDM-C08-T2, TTRDM-C08-T3, TTRDM-C08-T4_
- [ ] TTRDM-C08-T6 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-056, TTRDM-REQ-F-057, TTRDM-REQ-F-058, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061, TTRDM-REQ-F-062, TTRDM-REQ-F-063, TTRDM-REQ-F-064_
  - _Criteria: TTRDM-C08-AC-01, TTRDM-C08-AC-02, TTRDM-C08-AC-03, TTRDM-C08-AC-04, TTRDM-C08-AC-05, TTRDM-C08-AC-06, TTRDM-C08-AC-07, TTRDM-C08-AC-08, TTRDM-C08-AC-09, TTRDM-C08-AC-10, TTRDM-C08-AC-11, TTRDM-C08-AC-12_
  - _After: TTRDM-C08-T1, TTRDM-C08-T2, TTRDM-C08-T3, TTRDM-C08-T4, TTRDM-C08-T5_

## TTRDM-C09 Confirm and apply a list update or delete (draft)

- [ ] TTRDM-C09-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-065, TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-069, TTRDM-REQ-F-070, TTRDM-REQ-F-071, TTRDM-REQ-F-072, TTRDM-REQ-F-073, TTRDM-REQ-F-074, TTRDM-REQ-F-075, TTRDM-REQ-F-076, TTRDM-REQ-F-077_
- [ ] TTRDM-C09-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-065, TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-074, TTRDM-REQ-F-075_
  - _Rules: TTRDM-BR-074, TTRDM-BR-075, TTRDM-BR-076, TTRDM-BR-077, TTRDM-BR-078, TTRDM-BR-084_
  - _After: TTRDM-C09-T1_
- [ ] TTRDM-C09-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-071, TTRDM-REQ-F-072, TTRDM-REQ-F-073, TTRDM-REQ-F-076, TTRDM-REQ-F-077, TTRDM-REQ-F-069, TTRDM-REQ-F-070_
  - _Rules: TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-081, TTRDM-BR-082, TTRDM-BR-083, TTRDM-BR-085, TTRDM-BR-086_
  - _After: TTRDM-C09-T1_
- [ ] TTRDM-C09-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **data table** "Transaction types": In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes.
  - _Requirements: TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-074, TTRDM-REQ-F-076_
  - _Rules: TTRDM-BR-075, TTRDM-BR-076, TTRDM-BR-077, TTRDM-BR-078, TTRDM-BR-085_
  - _After: TTRDM-C09-T2, TTRDM-C09-T3_
- [ ] TTRDM-C09-T5 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-065, TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-069, TTRDM-REQ-F-070, TTRDM-REQ-F-071, TTRDM-REQ-F-072, TTRDM-REQ-F-073, TTRDM-REQ-F-074, TTRDM-REQ-F-075, TTRDM-REQ-F-076, TTRDM-REQ-F-077_
  - _Criteria: TTRDM-C09-AC-01, TTRDM-C09-AC-02, TTRDM-C09-AC-03, TTRDM-C09-AC-04, TTRDM-C09-AC-05, TTRDM-C09-AC-06, TTRDM-C09-AC-07, TTRDM-C09-AC-08, TTRDM-C09-AC-09, TTRDM-C09-AC-10, TTRDM-C09-AC-11, TTRDM-C09-AC-12, TTRDM-C09-AC-13, TTRDM-C09-AC-14, TTRDM-C09-AC-15_
  - _After: TTRDM-C09-T1, TTRDM-C09-T2, TTRDM-C09-T3, TTRDM-C09-T4_

## TTRDM-C10 Navigate from the transaction type list (draft)

- [ ] TTRDM-C10-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079_
- [ ] TTRDM-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079_
  - _Rules: TTRDM-BR-087, TTRDM-BR-088_
  - _After: TTRDM-C10-T1_
- [ ] TTRDM-C10-T3 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **primary button** "Add transaction type"
  - _Requirements: TTRDM-REQ-F-079_
  - _Rules: TTRDM-BR-088_
  - _After: TTRDM-C10-T2_
- [ ] TTRDM-C10-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
  - _Requirements: TTRDM-REQ-F-078_
  - _Rules: TTRDM-BR-087_
  - _After: TTRDM-C10-T2_
- [ ] TTRDM-C10-T5 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079_
  - _Criteria: TTRDM-C10-AC-01, TTRDM-C10-AC-02_
  - _After: TTRDM-C10-T1, TTRDM-C10-T2, TTRDM-C10-T3, TTRDM-C10-T4_

## TTRDM-C11 Look up a transaction type to maintain (draft)

- [ ] TTRDM-C11-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-083, TTRDM-REQ-F-084, TTRDM-REQ-F-085, TTRDM-REQ-F-086, TTRDM-REQ-F-087, TTRDM-REQ-F-088, TTRDM-REQ-F-089, TTRDM-REQ-F-090_
- [ ] TTRDM-C11-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: TTRDM-BR-102.
  - _Requirements: TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-084, TTRDM-REQ-F-088, TTRDM-REQ-F-089, TTRDM-REQ-F-090_
  - _Rules: TTRDM-BR-089, TTRDM-BR-090, TTRDM-BR-091, TTRDM-BR-094, TTRDM-BR-098, TTRDM-BR-099, TTRDM-BR-100, TTRDM-BR-101, TTRDM-BR-102_
  - _After: TTRDM-C11-T1_
- [ ] TTRDM-C11-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-083_
  - _Rules: TTRDM-BR-092, TTRDM-BR-093_
  - _After: TTRDM-C11-T1_
- [ ] TTRDM-C11-T4 [api] Build the services behind the screens
  - TTRDM-BR-095: Each lookup starts by clearing the 'original' snapshot and the information message held in the screen's state, so a failed lookup can never leave the previous type's values behind.
  - TTRDM-BR-096: A keyed read of the transaction type table by its two-digit code. On a hit, return a 'found' result with code and description; the description is used both for display and as the baseline for change detection.
  - TTRDM-BR-097: Hold the fetched code and description, at their stored length, as an 'original' snapshot in the edit session (or as a version/ETag) to compare against the user's later edits. On not-found or a read error, leave the snapshot empty.
  - TTRDM-BR-100: In the not-found state, if the same code is submitted again without choosing Add, keep the code and description already held in the edit session and ignore the submitted form values, including any description typed.
  - _Requirements: TTRDM-REQ-F-085, TTRDM-REQ-F-086, TTRDM-REQ-F-087_
  - _Rules: TTRDM-BR-095, TTRDM-BR-096, TTRDM-BR-097_
  - _After: TTRDM-C11-T1, TTRDM-C11-T2, TTRDM-C11-T3_
- [ ] TTRDM-C11-T5 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **lookup field** "Transaction type code": 'Tran Type code must be supplied. Enter a two-digit code.'; 'Tran Type code must be numeric. Enter digits only.'; 'Tran Type code must not be zero. Enter a code from 01 to 99.' Only the first failing check is shown.
  - _Requirements: TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-088_
  - _Rules: TTRDM-BR-089, TTRDM-BR-090, TTRDM-BR-091, TTRDM-BR-098_
  - _After: TTRDM-C11-T2, TTRDM-C11-T3, TTRDM-C11-T4_
- [ ] TTRDM-C11-T6 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-083, TTRDM-REQ-F-084, TTRDM-REQ-F-085, TTRDM-REQ-F-086, TTRDM-REQ-F-087, TTRDM-REQ-F-088, TTRDM-REQ-F-089, TTRDM-REQ-F-090_
  - _Criteria: TTRDM-C11-AC-01, TTRDM-C11-AC-02, TTRDM-C11-AC-03, TTRDM-C11-AC-04, TTRDM-C11-AC-05, TTRDM-C11-AC-06, TTRDM-C11-AC-07, TTRDM-C11-AC-08, TTRDM-C11-AC-09, TTRDM-C11-AC-10, TTRDM-C11-AC-11_
  - _After: TTRDM-C11-T1, TTRDM-C11-T2, TTRDM-C11-T3, TTRDM-C11-T4, TTRDM-C11-T5_

## TTRDM-C12 Show maintenance screen values and messages (draft)

- [ ] TTRDM-C12-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097, TTRDM-REQ-F-098, TTRDM-REQ-F-099_
- [ ] TTRDM-C12-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-098_
  - _Rules: TTRDM-BR-109_
  - _After: TTRDM-C12-T1_
- [ ] TTRDM-C12-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097_
  - _Rules: TTRDM-BR-093, TTRDM-BR-103, TTRDM-BR-104, TTRDM-BR-105, TTRDM-BR-106, TTRDM-BR-107, TTRDM-BR-108_
  - _After: TTRDM-C12-T1_
- [ ] TTRDM-C12-T4 [api] Build the services behind the screens
  - TTRDM-BR-110: The screen's controller has a default path: any action not handled by a dedicated step (exit, first entry, delete, save, cancel, or a key not allowed in the current state) binds the submitted form, validates it, works out the next state and re-renders the screen.
  - TTRDM-BR-111: Route requests by action and current edit state; when no specific action-and-state handler matches, fall through to the default bind, validate, decide-next-state and re-render path rather than raising an error.
  - _Requirements: TTRDM-REQ-F-099_
  - _Rules: TTRDM-BR-110, TTRDM-BR-111_
  - _After: TTRDM-C12-T1, TTRDM-C12-T2, TTRDM-C12-T3_
- [ ] TTRDM-C12-T5 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097, TTRDM-REQ-F-098, TTRDM-REQ-F-099_
  - _Criteria: TTRDM-C12-AC-01, TTRDM-C12-AC-02, TTRDM-C12-AC-03, TTRDM-C12-AC-04, TTRDM-C12-AC-05, TTRDM-C12-AC-06, TTRDM-C12-AC-07, TTRDM-C12-AC-08, TTRDM-C12-AC-09, TTRDM-C12-AC-10, TTRDM-C12-AC-11, TTRDM-C12-AC-12_
  - _After: TTRDM-C12-T1, TTRDM-C12-T2, TTRDM-C12-T3, TTRDM-C12-T4_

## TTRDM-C13 Detect changes to a fetched transaction type (draft)

- [ ] TTRDM-C13-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102_
- [ ] TTRDM-C13-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102_
  - _Rules: TTRDM-BR-112, TTRDM-BR-113, TTRDM-BR-114, TTRDM-BR-115_
  - _After: TTRDM-C13-T1_
- [ ] TTRDM-C13-T3 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **primary button** "Save transaction type": Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.'
  - _Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101_
  - _Rules: TTRDM-BR-112, TTRDM-BR-113, TTRDM-BR-114_
  - _After: TTRDM-C13-T2_
- [ ] TTRDM-C13-T4 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102_
  - _Criteria: TTRDM-C13-AC-01, TTRDM-C13-AC-02, TTRDM-C13-AC-03, TTRDM-C13-AC-04, TTRDM-C13-AC-05, TTRDM-C13-AC-06_
  - _After: TTRDM-C13-T1, TTRDM-C13-T2, TTRDM-C13-T3_

## TTRDM-C14 Cancel a pending maintenance change (draft)

- [ ] TTRDM-C14-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-103, TTRDM-REQ-F-104, TTRDM-REQ-F-105_
- [ ] TTRDM-C14-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: TTRDM-BR-118.
  - _Requirements: TTRDM-REQ-F-103, TTRDM-REQ-F-104, TTRDM-REQ-F-105_
  - _Rules: TTRDM-BR-116, TTRDM-BR-117, TTRDM-BR-118_
  - _After: TTRDM-C14-T1_
- [ ] TTRDM-C14-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-103, TTRDM-REQ-F-104, TTRDM-REQ-F-105_
  - _Criteria: TTRDM-C14-AC-01, TTRDM-C14-AC-02, TTRDM-C14-AC-03_
  - _After: TTRDM-C14-T1, TTRDM-C14-T2_

## TTRDM-C15 Exit the maintenance screen (draft)

- [ ] TTRDM-C15-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-106, TTRDM-REQ-F-107_
- [ ] TTRDM-C15-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-107_
  - _Rules: TTRDM-BR-120_
  - _After: TTRDM-C15-T1_
- [ ] TTRDM-C15-T3 [api] Build the services behind the screens
  - TTRDM-BR-119: On exit, the new application must commit or close any open database transaction for the session before navigating. It then redirects to the return route stored in the session, falling back to the Admin menu route when none is stored. No unit of work may be left open across the navigation.
  - _Requirements: TTRDM-REQ-F-106_
  - _Rules: TTRDM-BR-119_
  - _After: TTRDM-C15-T1, TTRDM-C15-T2_
- [ ] TTRDM-C15-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
  - _Requirements: TTRDM-REQ-F-106_
  - _Rules: TTRDM-BR-119_
  - _After: TTRDM-C15-T2, TTRDM-C15-T3_
- [ ] TTRDM-C15-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-106, TTRDM-REQ-F-107_
  - _Criteria: TTRDM-C15-AC-01, TTRDM-C15-AC-02, TTRDM-C15-AC-03_
  - _After: TTRDM-C15-T1, TTRDM-C15-T2, TTRDM-C15-T3, TTRDM-C15-T4_

## TTRDM-C16 Find a transaction type to maintain (draft)

- [ ] TTRDM-C16-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-108, TTRDM-REQ-F-109, TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-114, TTRDM-REQ-F-115, TTRDM-REQ-F-116_
- [ ] TTRDM-C16-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-115, TTRDM-REQ-F-116_
  - _Rules: TTRDM-BR-123, TTRDM-BR-124, TTRDM-BR-125, TTRDM-BR-126, TTRDM-BR-128, TTRDM-BR-129_
  - _After: TTRDM-C16-T1_
- [ ] TTRDM-C16-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-108, TTRDM-REQ-F-114_
  - _Rules: TTRDM-BR-121, TTRDM-BR-127_
  - _After: TTRDM-C16-T1_
- [ ] TTRDM-C16-T4 [api] Build the services behind the screens
  - TTRDM-BR-122: The search request needs server-side validation of the type code (supplied, numeric, non-zero) that runs before any database lookup. It applies only when the screen is in search mode, meaning not while adding a new record and not while awaiting confirmation. The validator stops at the first failure. Only a valid code, normalised to two digits, is used as the key for the single-row lookup by primary key.
  - _Requirements: TTRDM-REQ-F-109_
  - _Rules: TTRDM-BR-122_
  - _After: TTRDM-C16-T1, TTRDM-C16-T2, TTRDM-C16-T3_
- [ ] TTRDM-C16-T5 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **lookup field** "Transaction type code": 'Tran Type code must be supplied. Enter a two-digit code.'; 'Tran Type code must be numeric. Enter digits only.'; 'Tran Type code must not be zero. Enter a code from 01 to 99.' Only the first failing check is shown.
  - _Requirements: TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-115_
  - _Rules: TTRDM-BR-123, TTRDM-BR-124, TTRDM-BR-125, TTRDM-BR-126, TTRDM-BR-128_
  - _After: TTRDM-C16-T2, TTRDM-C16-T3, TTRDM-C16-T4_
- [ ] TTRDM-C16-T6 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-108, TTRDM-REQ-F-109, TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-114, TTRDM-REQ-F-115, TTRDM-REQ-F-116_
  - _Criteria: TTRDM-C16-AC-01, TTRDM-C16-AC-02, TTRDM-C16-AC-03, TTRDM-C16-AC-04, TTRDM-C16-AC-05, TTRDM-C16-AC-06, TTRDM-C16-AC-07, TTRDM-C16-AC-08, TTRDM-C16-AC-09, TTRDM-C16-AC-10, TTRDM-C16-AC-11, TTRDM-C16-AC-12_
  - _After: TTRDM-C16-T1, TTRDM-C16-T2, TTRDM-C16-T3, TTRDM-C16-T4, TTRDM-C16-T5_

## TTRDM-C17 Change a transaction type description (draft)

- [ ] TTRDM-C17-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-117, TTRDM-REQ-F-118, TTRDM-REQ-F-119, TTRDM-REQ-F-120, TTRDM-REQ-F-121, TTRDM-REQ-F-122, TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-126, TTRDM-REQ-F-127, TTRDM-REQ-F-128, TTRDM-REQ-F-129_
- [ ] TTRDM-C17-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-117, TTRDM-REQ-F-119, TTRDM-REQ-F-120, TTRDM-REQ-F-121, TTRDM-REQ-F-122, TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-127, TTRDM-REQ-F-128, TTRDM-REQ-F-129_
  - _Rules: TTRDM-BR-130, TTRDM-BR-132, TTRDM-BR-133, TTRDM-BR-134, TTRDM-BR-135, TTRDM-BR-136, TTRDM-BR-137, TTRDM-BR-138, TTRDM-BR-139, TTRDM-BR-141, TTRDM-BR-142_
  - _After: TTRDM-C17-T1_
- [ ] TTRDM-C17-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-126_
  - _Rules: TTRDM-BR-140_
  - _After: TTRDM-C17-T1_
- [ ] TTRDM-C17-T4 [api] Build the services behind the screens
  - TTRDM-BR-131: Input normalisation for the description field: trim leading and trailing spaces, and treat an empty result or a lone '*' as 'not supplied' before any validation or change comparison. Put this in one shared helper so that change detection and description validation see the same value.
  - _Requirements: TTRDM-REQ-F-118_
  - _Rules: TTRDM-BR-131_
  - _After: TTRDM-C17-T1, TTRDM-C17-T2, TTRDM-C17-T3_
- [ ] TTRDM-C17-T5 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **summary card** "Description": 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'
  - **primary button** "Save transaction type": Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.'
  - _Requirements: TTRDM-REQ-F-117, TTRDM-REQ-F-119, TTRDM-REQ-F-120, TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125_
  - _Rules: TTRDM-BR-130, TTRDM-BR-132, TTRDM-BR-133, TTRDM-BR-136, TTRDM-BR-137, TTRDM-BR-138, TTRDM-BR-139_
  - _After: TTRDM-C17-T2, TTRDM-C17-T3, TTRDM-C17-T4_
- [ ] TTRDM-C17-T6 [test-generation] Write a test for every acceptance criterion
  - 14 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-117, TTRDM-REQ-F-118, TTRDM-REQ-F-119, TTRDM-REQ-F-120, TTRDM-REQ-F-121, TTRDM-REQ-F-122, TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-126, TTRDM-REQ-F-127, TTRDM-REQ-F-128, TTRDM-REQ-F-129_
  - _Criteria: TTRDM-C17-AC-01, TTRDM-C17-AC-02, TTRDM-C17-AC-03, TTRDM-C17-AC-04, TTRDM-C17-AC-05, TTRDM-C17-AC-06, TTRDM-C17-AC-07, TTRDM-C17-AC-08, TTRDM-C17-AC-09, TTRDM-C17-AC-10, TTRDM-C17-AC-11, TTRDM-C17-AC-12, TTRDM-C17-AC-13, TTRDM-C17-AC-14_
  - _After: TTRDM-C17-T1, TTRDM-C17-T2, TTRDM-C17-T3, TTRDM-C17-T4, TTRDM-C17-T5_

## TTRDM-C18 Add a new transaction type (draft)

- [ ] TTRDM-C18-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131, TTRDM-REQ-F-132_
- [ ] TTRDM-C18-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131_
  - _Rules: TTRDM-BR-143, TTRDM-BR-144_
  - _After: TTRDM-C18-T1_
- [ ] TTRDM-C18-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-132_
  - _Rules: TTRDM-BR-140_
  - _After: TTRDM-C18-T1_
- [ ] TTRDM-C18-T4 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **lookup field** "Transaction type code": 'Tran Type code must be supplied. Enter a two-digit code.'; 'Tran Type code must be numeric. Enter digits only.'; 'Tran Type code must not be zero. Enter a code from 01 to 99.' Only the first failing check is shown.
  - **primary button** "Save transaction type": Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.'
  - _Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131_
  - _Rules: TTRDM-BR-143, TTRDM-BR-144_
  - _After: TTRDM-C18-T2, TTRDM-C18-T3_
- [ ] TTRDM-C18-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131, TTRDM-REQ-F-132_
  - _Criteria: TTRDM-C18-AC-01, TTRDM-C18-AC-02, TTRDM-C18-AC-03_
  - _After: TTRDM-C18-T1, TTRDM-C18-T2, TTRDM-C18-T3, TTRDM-C18-T4_

## TTRDM-C19 Delete a transaction type (draft)

- [ ] TTRDM-C19-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-138, TTRDM-REQ-F-139_
- [ ] TTRDM-C19-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-138_
  - _Rules: TTRDM-BR-145, TTRDM-BR-146, TTRDM-BR-147, TTRDM-BR-150_
  - _After: TTRDM-C19-T1_
- [ ] TTRDM-C19-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-139_
  - _Rules: TTRDM-BR-148, TTRDM-BR-149, TTRDM-BR-151_
  - _After: TTRDM-C19-T1_
- [ ] TTRDM-C19-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **data table** "Transaction types": In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes.
  - _Requirements: TTRDM-REQ-F-134, TTRDM-REQ-F-136_
  - _Rules: TTRDM-BR-146, TTRDM-BR-148_
  - _After: TTRDM-C19-T2, TTRDM-C19-T3_
- [ ] TTRDM-C19-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-138, TTRDM-REQ-F-139_
  - _Criteria: TTRDM-C19-AC-01, TTRDM-C19-AC-02, TTRDM-C19-AC-03, TTRDM-C19-AC-04, TTRDM-C19-AC-05, TTRDM-C19-AC-06, TTRDM-C19-AC-07_
  - _After: TTRDM-C19-T1, TTRDM-C19-T2, TTRDM-C19-T3, TTRDM-C19-T4_

## TTRDM-C20 Control maintenance screen keys and flow (draft)

- [ ] TTRDM-C20-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143, TTRDM-REQ-F-144_
- [ ] TTRDM-C20-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143_
  - _Rules: TTRDM-BR-152, TTRDM-BR-153, TTRDM-BR-154, TTRDM-BR-155_
  - _After: TTRDM-C20-T1_
- [ ] TTRDM-C20-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-144_
  - _Rules: TTRDM-BR-156_
  - _After: TTRDM-C20-T1_
- [ ] TTRDM-C20-T4 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **primary button** "Save transaction type": Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.'
  - _Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142_
  - _Rules: TTRDM-BR-152, TTRDM-BR-153, TTRDM-BR-154_
  - _After: TTRDM-C20-T2, TTRDM-C20-T3_
- [ ] TTRDM-C20-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143, TTRDM-REQ-F-144_
  - _Criteria: TTRDM-C20-AC-01, TTRDM-C20-AC-02, TTRDM-C20-AC-03, TTRDM-C20-AC-04, TTRDM-C20-AC-05, TTRDM-C20-AC-06, TTRDM-C20-AC-07_
  - _After: TTRDM-C20-T1, TTRDM-C20-T2, TTRDM-C20-T3, TTRDM-C20-T4_

## TTRDM-C21 Maintain transaction types in batch (draft)

- [ ] TTRDM-C21-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-146_
  - _Rules: TTRDM-BR-158_
- [ ] TTRDM-C21-T2 [api] Build the scheduled job
  - TTRDM-BR-157: A scheduled or on-demand batch job that reads a request file without taking it exclusively. It connects to the reference data database with the application's own credentials and applies each request to the transaction types table. It writes a per-run log of messages that operations can review. The subsystem and plan names have no counterpart: they become the job's database connection configuration.
  - _Requirements: TTRDM-REQ-F-145_
  - _Rules: TTRDM-BR-157_
  - _After: TTRDM-C21-T1_
- [ ] TTRDM-C21-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-145, TTRDM-REQ-F-146_
  - _Criteria: TTRDM-C21-AC-01, TTRDM-C21-AC-02_
  - _After: TTRDM-C21-T1, TTRDM-C21-T2_

## TTRDM-C22 Set up reference data backups (draft)

- [ ] TTRDM-C22-T1 [api] Build the scheduled job
  - TTRDM-BR-159: A versioned backup location for transaction type snapshots, such as a versioned object-store prefix or a backup table keyed by snapshot date. It needs a retention policy that keeps the five newest versions and removes the oldest when a sixth is written. It must exist before the first snapshot is taken.
  - TTRDM-BR-160: A job step that runs only when the backup location was set up successfully. It writes a first snapshot of the current transaction type reference data, unchanged and in its 60-character record layout, as a new recorded version in that location.
  - TTRDM-BR-161: A job step that runs only when every earlier step succeeded. It writes a first snapshot of the current transaction category reference data, unchanged and in its 60-character record layout, as a new recorded version in the category backup location.
  - TTRDM-BR-162: A job step that runs only when every earlier step succeeded. It writes a first snapshot of the current disclosure group reference data, unchanged and in its 50-character record layout, as a new recorded version in the disclosure group backup location.
  - _Requirements: TTRDM-REQ-F-147, TTRDM-REQ-F-148, TTRDM-REQ-F-149, TTRDM-REQ-F-150_
  - _Rules: TTRDM-BR-159, TTRDM-BR-160, TTRDM-BR-161, TTRDM-BR-162_
- [ ] TTRDM-C22-T2 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-147, TTRDM-REQ-F-148, TTRDM-REQ-F-149, TTRDM-REQ-F-150_
  - _Criteria: TTRDM-C22-AC-01, TTRDM-C22-AC-02, TTRDM-C22-AC-03, TTRDM-C22-AC-04, TTRDM-C22-AC-05, TTRDM-C22-AC-06, TTRDM-C22-AC-07_
  - _After: TTRDM-C22-T1_

## TTRDM-C23 Extract transaction types and categories to files (draft)

- [ ] TTRDM-C23-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-154, TTRDM-REQ-F-157_
  - _Rules: TTRDM-BR-166, TTRDM-BR-169_
- [ ] TTRDM-C23-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-153, TTRDM-REQ-F-156, TTRDM-REQ-F-159_
  - _Rules: TTRDM-BR-165, TTRDM-BR-168, TTRDM-BR-171_
- [ ] TTRDM-C23-T3 [api] Build the scheduled job
  - TTRDM-BR-163: The extract job's first step copies the current transaction type extract, unchanged and in its 60-character records, into a new version in the versioned transaction type backup location before anything is overwritten.
  - TTRDM-BR-164: A conditional job step that runs only when every earlier step succeeded. It copies the current transaction category extract, unchanged and in its 60-character records, into a new version in the category backup location. The orchestrator must skip it after any earlier failure.
  - TTRDM-BR-167: A fixed-width writer for the sorted transaction type extract (ordered by type code). Each record has the 2-character type code, the description right-padded with spaces to 50 characters, then the literal '00000000', 60 characters in all. Downstream consumers depend on this exact layout.
  - TTRDM-BR-170: A fixed-width writer for the sorted transaction category extract (ordered by type code, then category code). Each record has the type code, the category code, the category description right-padded with spaces to 50 characters, then the literal '0000', 60 characters in all.
  - _Requirements: TTRDM-REQ-F-151, TTRDM-REQ-F-152, TTRDM-REQ-F-155, TTRDM-REQ-F-158_
  - _Rules: TTRDM-BR-163, TTRDM-BR-164, TTRDM-BR-167, TTRDM-BR-170_
  - _After: TTRDM-C23-T1, TTRDM-C23-T2_
- [ ] TTRDM-C23-T4 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-151, TTRDM-REQ-F-152, TTRDM-REQ-F-153, TTRDM-REQ-F-154, TTRDM-REQ-F-155, TTRDM-REQ-F-156, TTRDM-REQ-F-157, TTRDM-REQ-F-158, TTRDM-REQ-F-159_
  - _Criteria: TTRDM-C23-AC-01, TTRDM-C23-AC-02, TTRDM-C23-AC-03, TTRDM-C23-AC-04, TTRDM-C23-AC-05, TTRDM-C23-AC-06, TTRDM-C23-AC-07, TTRDM-C23-AC-08, TTRDM-C23-AC-09, TTRDM-C23-AC-10, TTRDM-C23-AC-11_
  - _After: TTRDM-C23-T1, TTRDM-C23-T2, TTRDM-C23-T3_

## TTRDM-C24 Load reference data into keyed files (draft)

- [ ] TTRDM-C24-T1 [api] Build the scheduled job
  - TTRDM-BR-172: A full-refresh load of the transaction category lookup store (a table or cache keyed by type code plus category code, the first 6 characters of each 60-character record). Truncate or recreate it, then load every record from the category extract, which is read without locking it. Hold the store exclusively, or swap it in atomically, so readers never see a half-loaded store.
  - TTRDM-BR-173: A full-refresh load of the transaction type lookup store, keyed by the 2-character type code at the start of each 60-character record. Truncate or recreate it, then load every record from the transaction type extract, which is read without locking it. Hold the store exclusively, or swap it in atomically, so readers never see a half-loaded store.
  - _Requirements: TTRDM-REQ-F-160, TTRDM-REQ-F-161_
  - _Rules: TTRDM-BR-172, TTRDM-BR-173_
- [ ] TTRDM-C24-T2 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-160, TTRDM-REQ-F-161_
  - _Criteria: TTRDM-C24-AC-01, TTRDM-C24-AC-02, TTRDM-C24-AC-03_
  - _After: TTRDM-C24-T1_

## UP-C01 Build screen map copybooks (draft)

- [ ] UP-C01-T1 [api] Build the scheduled job
  - UP-BR-001: A build-pipeline step that generates the screen's field-layout (view model / DTO) definition from the screen source. It produces only that definition, not an executable artefact. In the new stack this belongs in the UI build or code generation, not in a runtime job.
  - UP-BR-002: Write the generated layout to the shared source location under the screen's name, replacing the previous version atomically so nothing else writes it at the same time. Keep the build log or listing as a build artefact named after the screen.
  - _Requirements: UP-REQ-F-001, UP-REQ-F-002_
  - _Rules: UP-BR-001, UP-BR-002_
- [ ] UP-C01-T2 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-001, UP-REQ-F-002_
  - _Criteria: UP-C01-AC-01, UP-C01-AC-02_
  - _After: UP-C01-T1_

## UP-C02 List card master records (draft)

- [ ] UP-C02-T1 [data] Model the data the capability reads and writes
  - File records: CVACT02Y, CVACT03Y (see data-contracts.md).
  - _Requirements: UP-REQ-F-003, UP-REQ-F-004, UP-REQ-F-005, UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009_
- [ ] UP-C02-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009, UP-REQ-F-004_
  - _Rules: UP-BR-004, UP-BR-005, UP-BR-009, UP-BR-010, UP-BR-011_
  - _After: UP-C02-T1_
- [ ] UP-C02-T3 [api] Build the scheduled job
  - UP-BR-003: A scheduled or on-demand report job that reads the card store through a read-only connection, so it can run while online users are working. Its progress messages and the listing go to the job's log or report output.
  - UP-BR-006: Each successful fetch of the next card in the ordered read is written to the report. The new application needs a sequential read of all cards, ordered by card number.
  - UP-BR-007: When the cursor or stream runs out of cards, the job ends normally. End of data is the normal way to finish, not an error.
  - UP-BR-008: Iterate until there are no more rows and write nothing for the empty fetch, so no blank or repeated line appears after the last card.
  - _Requirements: UP-REQ-F-003, UP-REQ-F-005, UP-REQ-F-006_
  - _Rules: UP-BR-003, UP-BR-006, UP-BR-007, UP-BR-008_
  - _After: UP-C02-T1, UP-C02-T2_
- [ ] UP-C02-T4 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-003, UP-REQ-F-004, UP-REQ-F-005, UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009_
  - _Criteria: UP-C02-AC-01, UP-C02-AC-02, UP-C02-AC-03, UP-C02-AC-04, UP-C02-AC-05, UP-C02-AC-06, UP-C02-AC-07, UP-C02-AC-08, UP-C02-AC-09, UP-C02-AC-10_
  - _After: UP-C02-T1, UP-C02-T2, UP-C02-T3_
- [ ] UP-C02-T5 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-003, UP-REQ-F-004, UP-REQ-F-005, UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009_
  - _After: UP-C02-T1, UP-C02-T2, UP-C02-T3_

## UP-C03 List card cross-reference records (draft)

- [ ] UP-C03-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y (see data-contracts.md).
  - _Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012_
- [ ] UP-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-014.
  - _Requirements: UP-REQ-F-012_
  - _Rules: UP-BR-014_
  - _After: UP-C03-T1_
- [ ] UP-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-011_
  - _Rules: UP-BR-013_
  - _After: UP-C03-T1_
- [ ] UP-C03-T4 [api] Build the scheduled job
  - UP-BR-012: A report job that reads the full card-to-account/customer link table through a read-only connection, from start to end, and writes every link to the job's report output. It changes nothing.
  - _Requirements: UP-REQ-F-010_
  - _Rules: UP-BR-012_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3_
- [ ] UP-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012_
  - _Criteria: UP-C03-AC-01, UP-C03-AC-02, UP-C03-AC-03_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4_
- [ ] UP-C03-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4_

## UP-C04 List customer records (draft)

- [ ] UP-C04-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVCUS01Y (see data-contracts.md).
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
- [ ] UP-C04-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
  - _Rules: UP-BR-005, UP-BR-015, UP-BR-016_
  - _After: UP-C04-T1_
- [ ] UP-C04-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
  - _Rules: UP-BR-005, UP-BR-015, UP-BR-016_
  - _After: UP-C04-T1, UP-C04-T2_
- [ ] UP-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
  - _Criteria: UP-C04-AC-01, UP-C04-AC-02, UP-C04-AC-03, UP-C04-AC-04, UP-C04-AC-05_
  - _After: UP-C04-T1, UP-C04-T2, UP-C04-T3_
- [ ] UP-C04-T5 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-013, UP-REQ-F-014_
  - _After: UP-C04-T1, UP-C04-T2, UP-C04-T3_

## UP-C05 Verify daily transaction cards and accounts (draft)

- [ ] UP-C05-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA06Y (see data-contracts.md).
  - Working records it passes or builds: CVACT02Y, CVCUS01Y, CVTRA05Y.
  - _Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024_
- [ ] UP-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-025.
  - _Requirements: UP-REQ-F-017, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-023_
  - _Rules: UP-BR-019, UP-BR-021, UP-BR-022, UP-BR-025_
  - _After: UP-C05-T1_
- [ ] UP-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-016, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-018, UP-REQ-F-024_
  - _Rules: UP-BR-018, UP-BR-020, UP-BR-023, UP-BR-024, UP-BR-026_
  - _After: UP-C05-T1_
- [ ] UP-C05-T4 [api] Build the service
  - UP-BR-017: A batch job that streams the day's transaction feed in file order, one record at a time. It logs each record and runs card verification on it, and it finishes when the feed is used up. End of feed is the normal way to finish.
  - _Requirements: UP-REQ-F-015_
  - _Rules: UP-BR-017_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3_
- [ ] UP-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024_
  - _Criteria: UP-C05-AC-01, UP-C05-AC-02, UP-C05-AC-03, UP-C05-AC-04, UP-C05-AC-05, UP-C05-AC-06, UP-C05-AC-07, UP-C05-AC-08, UP-C05-AC-09, UP-C05-AC-10, UP-C05-AC-11_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4_
- [ ] UP-C05-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023, UP-REQ-F-024_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4_

## UP-C06 Build and deploy online programs (draft)

- [ ] UP-C06-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-028_
  - _Rules: UP-BR-030_
- [ ] UP-C06-T2 [api] Build the scheduled job
  - UP-BR-027: A CI/CD deploy step. When the build succeeds (warnings allowed, no errors), roll out the new version to the running online service, for example by a rolling restart or a hot reload, so new requests use the new code.
  - UP-BR-028: Run this only when every build step succeeded without warnings. It registers or refreshes the program's database access against the CARDDEMO schema, replacing the previous version, using read-committed isolation. In a modern stack this is usually a schema migration or a step that grants database permissions, gated on a green build.
  - UP-BR-029: After the database access step succeeds (warnings allowed), refresh the application-level database binding that covers all CARDDEMO programs. Keep the existing permissions and use the same CARDDEMO schema and isolation. In a modern stack this is the deploy-time database configuration or role setup, and it must not reset grants.
  - _Requirements: UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027_
  - _Rules: UP-BR-027, UP-BR-028, UP-BR-029_
  - _After: UP-C06-T1_
- [ ] UP-C06-T3 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028_
  - _Criteria: UP-C06-AC-01, UP-C06-AC-02, UP-C06-AC-03, UP-C06-AC-04, UP-C06-AC-05, UP-C06-AC-06, UP-C06-AC-07_
  - _After: UP-C06-T1, UP-C06-T2_
- [ ] UP-C06-T4 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028_
  - _After: UP-C06-T1, UP-C06-T2_

## UP-C07 Convert date formats (draft)

- [ ] UP-C07-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: UP-REQ-F-029, UP-REQ-F-031, UP-REQ-F-033_
  - _Rules: UP-BR-031, UP-BR-032, UP-BR-034, UP-BR-036_
- [ ] UP-C07-T2 [api] Build the scheduled job
  - UP-BR-033: A pure, reusable date-formatting function that takes YYYYMMDD and returns YYYY-MM-DD. Build it as a library function, not a separate service call.
  - UP-BR-035: The same library function going the other way: it takes YYYY-MM-DD and returns YYYYMMDD by position (characters 1-4, 6-7 and 9-10). It does not validate the separators.
  - UP-BR-037: The account extract calls the date-formatting function on the reissue date for every record it writes, so the extract carries the date as YYYYMMDD.
  - _Requirements: UP-REQ-F-030, UP-REQ-F-032, UP-REQ-F-034_
  - _Rules: UP-BR-033, UP-BR-035, UP-BR-037_
  - _After: UP-C07-T1_
- [ ] UP-C07-T3 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-029, UP-REQ-F-030, UP-REQ-F-031, UP-REQ-F-032, UP-REQ-F-033, UP-REQ-F-034_
  - _Criteria: UP-C07-AC-01, UP-C07-AC-02, UP-C07-AC-03, UP-C07-AC-04, UP-C07-AC-05, UP-C07-AC-06_
  - _After: UP-C07-T1, UP-C07-T2_

## UP-C08 Pause a batch job (draft)

- [ ] UP-C08-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-040.
  - _Requirements: UP-REQ-F-037_
  - _Rules: UP-BR-040_
- [ ] UP-C08-T2 [api] Build the scheduled job
  - UP-BR-038: A configurable delay step in the job scheduler or workflow. It reads an 8-digit duration in hundredths of a second (for example 00000500 = 5 seconds), sleeps for that long, and always exits successfully. In most schedulers this is a built-in wait or delay task rather than custom code.
  - UP-BR-039: The timer behind the delay step: suspend for the given number of hundredths of a second and then return success to the caller. A standard sleep in the job runtime covers it.
  - _Requirements: UP-REQ-F-035, UP-REQ-F-036_
  - _Rules: UP-BR-038, UP-BR-039_
  - _After: UP-C08-T1_
- [ ] UP-C08-T3 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-035, UP-REQ-F-036, UP-REQ-F-037_
  - _Criteria: UP-C08-AC-01, UP-C08-AC-02, UP-C08-AC-03, UP-C08-AC-04, UP-C08-AC-05_
  - _After: UP-C08-T1, UP-C08-T2_

## UP-C09 Retain dataset generations (draft)

- [ ] UP-C09-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-046_
  - _Rules: UP-BR-049_
- [ ] UP-C09-T2 [api] Build the scheduled job
  - UP-BR-041: Keep each run's daily rejected-transactions output as a versioned object, for example a dated file in object storage. A retention policy keeps the latest 5 and deletes older ones.
  - UP-BR-042: Version the combined transaction file (the transaction backup merged with system-generated transactions) per run. Keep the latest 5 and delete the data of older versions automatically.
  - UP-BR-043: Version the daily transaction input per run. Keep the latest 5 and delete older versions automatically.
  - UP-BR-044: Version the transaction report per run and keep the latest 5. Another set-up job defines the same report history with 10 versions (rule bc474731…), so the team must choose one limit.
  - UP-BR-045: A retention policy for the daily transaction report that keeps the latest 10 versions; the oldest goes when an eleventh is created. This conflicts with the 5-version definition in the main set-up (rule 1b564856…), so the team must decide which one applies.
  - UP-BR-046: Take a versioned backup of the transaction category balances on each run. Keep the latest 5 and delete older ones automatically.
  - UP-BR-047: Take a versioned backup of the transaction master on each run. Keep the latest 5 and delete older ones automatically.
  - UP-BR-048: Version the system-generated transaction file per run. Keep the latest 5 and delete older ones automatically.
  - _Requirements: UP-REQ-F-038, UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044, UP-REQ-F-045_
  - _Rules: UP-BR-041, UP-BR-042, UP-BR-043, UP-BR-044, UP-BR-045, UP-BR-046, UP-BR-047, UP-BR-048_
  - _After: UP-C09-T1_
- [ ] UP-C09-T3 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-038, UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044, UP-REQ-F-045, UP-REQ-F-046_
  - _Criteria: UP-C09-AC-01, UP-C09-AC-02, UP-C09-AC-03, UP-C09-AC-04, UP-C09-AC-05, UP-C09-AC-06, UP-C09-AC-07, UP-C09-AC-08, UP-C09-AC-09, UP-C09-AC-10_
  - _After: UP-C09-T1, UP-C09-T2_

## UP-C10 List the CardDemo dataset catalog (draft)

- [ ] UP-C10-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-047_
  - _Rules: UP-BR-050_
- [ ] UP-C10-T2 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: UP-REQ-F-047_
  - _Rules: UP-BR-050_
  - _After: UP-C10-T1_
- [ ] UP-C10-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-047_
  - _Criteria: UP-C10-AC-01, UP-C10-AC-02_
  - _After: UP-C10-T1, UP-C10-T2_

## UP-C11 Read transactions by processed timestamp (draft)

- [ ] UP-C11-T1 [api] Build the scheduled job
  - UP-BR-051: A non-unique secondary index on the transaction table's processed-timestamp column, covering every existing row. In a relational database this is a CREATE INDEX, which the database keeps up to date, not a separate rebuild job.
  - UP-BR-052: Expose a query or repository method that reads transactions by processed timestamp (exact match or range, in timestamp order) using that non-unique index. It must allow many transactions per timestamp.
  - _Requirements: UP-REQ-F-048, UP-REQ-F-049_
  - _Rules: UP-BR-051, UP-BR-052_
- [ ] UP-C11-T2 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-048, UP-REQ-F-049_
  - _Criteria: UP-C11-AC-01, UP-C11-AC-02_
  - _After: UP-C11-T1_

## CAFM-C01 Purge expired pending authorizations (draft)

- [ ] CAFM-C01-T1 [data] Model the data the capability reads and writes
  - File records: CIPAUSMY (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY.
  - _Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-002, CAFM-REQ-F-003, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-008, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013_
- [ ] CAFM-C01-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-002, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013_
  - _Rules: CAFM-BR-003, CAFM-BR-005, CAFM-BR-006, CAFM-BR-007, CAFM-BR-009, CAFM-BR-010, CAFM-BR-011, CAFM-BR-012_
  - _After: CAFM-C01-T1_
- [ ] CAFM-C01-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-008_
  - _Rules: CAFM-BR-008_
  - _After: CAFM-C01-T1_
- [ ] CAFM-C01-T4 [api] Build the scheduled job
  - CAFM-BR-001: At start-up the job takes the run date from the system clock and reads two run parameters. Expiry days is used when numeric and defaults to 5 otherwise. Checkpoint frequency defaults to 5 when it is blank, zero or missing. Check both values before any data is touched.
  - CAFM-BR-002: Run the purge as a scheduled batch job that has update access to the pending authorization store, both summaries and details. It runs alongside the online authorization service, so it must commit in small batches (see the checkpoint frequency) rather than locking the whole store.
  - CAFM-BR-004: Read every account summary in turn and, for each one, all of its authorization details. Delete the details that qualify, then decide whether the summary goes too, before moving to the next account. A parent-child query or keyset cursor over summaries with their details is enough. Commit every checkpoint-frequency summaries so a restart can resume from the last committed account.
  - _Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-003_
  - _Rules: CAFM-BR-001, CAFM-BR-002, CAFM-BR-004_
  - _After: CAFM-C01-T1, CAFM-C01-T2, CAFM-C01-T3_
- [ ] CAFM-C01-T5 [test-generation] Write a test for every acceptance criterion
  - 18 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-002, CAFM-REQ-F-003, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-008, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013_
  - _Criteria: CAFM-C01-AC-01, CAFM-C01-AC-02, CAFM-C01-AC-03, CAFM-C01-AC-04, CAFM-C01-AC-05, CAFM-C01-AC-06, CAFM-C01-AC-07, CAFM-C01-AC-08, CAFM-C01-AC-09, CAFM-C01-AC-10, CAFM-C01-AC-11, CAFM-C01-AC-12, CAFM-C01-AC-13, CAFM-C01-AC-14, CAFM-C01-AC-15, CAFM-C01-AC-16, CAFM-C01-AC-17, CAFM-C01-AC-18_
  - _After: CAFM-C01-T1, CAFM-C01-T2, CAFM-C01-T3, CAFM-C01-T4_
- [ ] CAFM-C01-T6 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-001, CAFM-REQ-N-001, CAFM-REQ-F-002, CAFM-REQ-F-003, CAFM-REQ-F-004, CAFM-REQ-F-005, CAFM-REQ-F-006, CAFM-REQ-F-007, CAFM-REQ-F-008, CAFM-REQ-F-009, CAFM-REQ-F-010, CAFM-REQ-F-011, CAFM-REQ-F-012, CAFM-REQ-F-013_
  - _After: CAFM-C01-T1, CAFM-C01-T2, CAFM-C01-T3, CAFM-C01-T4_

## CAFM-C02 Answer account inquiry requests from the queue (draft)

- [ ] CAFM-C02-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y (see data-contracts.md).
  - _Requirements: CAFM-REQ-F-014, CAFM-REQ-F-015, CAFM-REQ-N-002, CAFM-REQ-F-016, CAFM-REQ-F-017, CAFM-REQ-F-018, CAFM-REQ-F-019, CAFM-REQ-F-020, CAFM-REQ-F-021, CAFM-REQ-F-022, CAFM-REQ-F-023, CAFM-REQ-F-024, CAFM-REQ-F-025, CAFM-REQ-F-026, CAFM-REQ-F-027, CAFM-REQ-F-028_
- [ ] CAFM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CAFM-BR-017.
  - _Requirements: CAFM-REQ-F-015, CAFM-REQ-F-020, CAFM-REQ-F-021, CAFM-REQ-F-024, CAFM-REQ-F-017_
  - _Rules: CAFM-BR-014, CAFM-BR-017, CAFM-BR-019, CAFM-BR-020, CAFM-BR-021, CAFM-BR-024_
  - _After: CAFM-C02-T1_
- [ ] CAFM-C02-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-025, CAFM-REQ-F-026, CAFM-REQ-F-027, CAFM-REQ-F-028, CAFM-REQ-F-022, CAFM-REQ-F-023_
  - _Rules: CAFM-BR-022, CAFM-BR-023, CAFM-BR-025, CAFM-BR-026, CAFM-BR-027, CAFM-BR-028, CAFM-BR-029, CAFM-BR-030_
  - _After: CAFM-C02-T1_
- [ ] CAFM-C02-T4 [api] Build the services behind the screens
  - CAFM-BR-013: Run the account inquiry as a consumer on the account inquiry request queue, started when messages arrive. It replies on the fixed account reply queue ('CARD.DEMO.REPLY.ACCT') and reports failures to a shared error queue ('CARD.DEMO.ERROR'). Queue names come from configuration, and the request queue is whichever one triggered the consumer.
  - CAFM-BR-015: Take a request and send its reply in one transaction, so that a request counts as consumed only when its reply is sent. Commit before taking the next request, and commit the final request's transaction when the consumer stops.
  - CAFM-BR-016: Keep each request's message id and correlation id for its reply. Read the request body as fixed positions: characters 1–4 are the function code and the next 11 digits are the account number. Validate the account number as numeric before looking it up.
  - CAFM-BR-018: Publish the reply to the account reply queue with the request's message and correlation identifiers, so the caller can match it to its request. If publishing fails, send an 'MQPUT ERR' record to the error queue and stop the consumer.
  - _Requirements: CAFM-REQ-F-014, CAFM-REQ-N-002, CAFM-REQ-F-016, CAFM-REQ-F-018, CAFM-REQ-F-019_
  - _Rules: CAFM-BR-013, CAFM-BR-015, CAFM-BR-016, CAFM-BR-018_
  - _After: CAFM-C02-T1, CAFM-C02-T2, CAFM-C02-T3_
- [ ] CAFM-C02-T5 [test-generation] Write a test for every acceptance criterion
  - 20 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-014, CAFM-REQ-F-015, CAFM-REQ-N-002, CAFM-REQ-F-016, CAFM-REQ-F-017, CAFM-REQ-F-018, CAFM-REQ-F-019, CAFM-REQ-F-020, CAFM-REQ-F-021, CAFM-REQ-F-022, CAFM-REQ-F-023, CAFM-REQ-F-024, CAFM-REQ-F-025, CAFM-REQ-F-026, CAFM-REQ-F-027, CAFM-REQ-F-028_
  - _Criteria: CAFM-C02-AC-01, CAFM-C02-AC-02, CAFM-C02-AC-03, CAFM-C02-AC-04, CAFM-C02-AC-05, CAFM-C02-AC-06, CAFM-C02-AC-07, CAFM-C02-AC-08, CAFM-C02-AC-09, CAFM-C02-AC-10, CAFM-C02-AC-11, CAFM-C02-AC-12, CAFM-C02-AC-13, CAFM-C02-AC-14, CAFM-C02-AC-15, CAFM-C02-AC-16, CAFM-C02-AC-17, CAFM-C02-AC-18, CAFM-C02-AC-19, CAFM-C02-AC-20_
  - _After: CAFM-C02-T1, CAFM-C02-T2, CAFM-C02-T3, CAFM-C02-T4_
- [ ] CAFM-C02-T6 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-014, CAFM-REQ-F-015, CAFM-REQ-N-002, CAFM-REQ-F-016, CAFM-REQ-F-017, CAFM-REQ-F-018, CAFM-REQ-F-019, CAFM-REQ-F-020, CAFM-REQ-F-021, CAFM-REQ-F-022, CAFM-REQ-F-023, CAFM-REQ-F-024, CAFM-REQ-F-025, CAFM-REQ-F-026, CAFM-REQ-F-027, CAFM-REQ-F-028_
  - _After: CAFM-C02-T1, CAFM-C02-T2, CAFM-C02-T3, CAFM-C02-T4_

## CAFM-C03 Answer system date requests from the queue (draft)

- [ ] CAFM-C03-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-034, CAFM-REQ-F-035, CAFM-REQ-F-036, CAFM-REQ-F-037, CAFM-REQ-F-038, CAFM-REQ-F-039, CAFM-REQ-F-031_
  - _Rules: CAFM-BR-033, CAFM-BR-036, CAFM-BR-037, CAFM-BR-038, CAFM-BR-039, CAFM-BR-040, CAFM-BR-041_
- [ ] CAFM-C03-T2 [api] Build the services behind the screens
  - CAFM-BR-031: Run the date inquiry as a consumer on the queue whose arrival started it. It always replies on the fixed date reply queue ('CARD.DEMO.REPLY.DATE') and ignores any reply-to queue the requester names.
  - CAFM-BR-032: Process requests one at a time until the queue is empty: wait up to 5 seconds for each, and stop when none arrives. Take a request and send its reply in one transaction, committed before the next request is taken.
  - CAFM-BR-034: Send the reply as a text message in the broker's standard character set, carrying the request's message ID and correlation ID, inside the same transaction that consumed the request.
  - CAFM-BR-035: On shutdown, normal or after an error, release every queue connection that was opened (request, reply and error). Release only the ones that opened successfully, then end the task.
  - _Requirements: CAFM-REQ-F-029, CAFM-REQ-F-030, CAFM-REQ-F-032, CAFM-REQ-F-033_
  - _Rules: CAFM-BR-031, CAFM-BR-032, CAFM-BR-034, CAFM-BR-035_
  - _After: CAFM-C03-T1_
- [ ] CAFM-C03-T3 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-029, CAFM-REQ-F-030, CAFM-REQ-F-031, CAFM-REQ-F-032, CAFM-REQ-F-033, CAFM-REQ-F-034, CAFM-REQ-F-035, CAFM-REQ-F-036, CAFM-REQ-F-037, CAFM-REQ-F-038, CAFM-REQ-F-039_
  - _Criteria: CAFM-C03-AC-01, CAFM-C03-AC-02, CAFM-C03-AC-03, CAFM-C03-AC-04, CAFM-C03-AC-05, CAFM-C03-AC-06, CAFM-C03-AC-07, CAFM-C03-AC-08, CAFM-C03-AC-09, CAFM-C03-AC-10, CAFM-C03-AC-11, CAFM-C03-AC-12, CAFM-C03-AC-13_
  - _After: CAFM-C03-T1, CAFM-C03-T2_

## CAFM-C04 Receive and prepare card authorization requests (draft)

- [ ] CAFM-C04-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051_
- [ ] CAFM-C04-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-050_
  - _Rules: CAFM-BR-046, CAFM-BR-047, CAFM-BR-049, CAFM-BR-050, CAFM-BR-052_
  - _After: CAFM-C04-T1_
- [ ] CAFM-C04-T3 [api] Build the services behind the screens
  - CAFM-BR-042: Consume authorization requests from the request queue one at a time, committing after each. Stop after 501 messages in one activation (the limit is 500, checked as 'more than') and leave the rest for the next activation. Make the limit a configuration value.
  - CAFM-BR-043: Wait up to 5 seconds for each next request, and end the consumer cleanly when none arrives.
  - CAFM-BR-044: Read the request as comma-separated text in this field order: auth date, auth time, card number, auth type, card expiry, message type, message source, processing code, amount, merchant category code, acquirer country code, POS entry mode, merchant id, merchant name, merchant city, merchant state, merchant zip, transaction id. Convert the amount text to a decimal number.
  - CAFM-BR-045: Once the card is found, look up the account by the account id from the card cross-reference (a keyed lookup by account id) and record whether it was found.
  - CAFM-BR-048: Once the card is found, look up the customer by the customer id from the card cross-reference (a keyed lookup by customer id) and record whether it was found.
  - CAFM-BR-051: Look up the pending-authorization summary by the card's account id. Keep three outcomes apart: found, not found (a valid state, after which a new summary is created) and read failure (critical error 'I002').
  - CAFM-BR-053: Authorization details must list newest first under their account. The legacy key does this with an inverted date (99999 minus YYDDD) and an inverted time (999999999 minus time×1000+milliseconds). A modern store can order by a full timestamp descending instead, but the purge's age calculation and the paging keys must use the same date.
  - _Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-046, CAFM-REQ-F-049, CAFM-REQ-F-051_
  - _Rules: CAFM-BR-042, CAFM-BR-043, CAFM-BR-044, CAFM-BR-045, CAFM-BR-048, CAFM-BR-051, CAFM-BR-053_
  - _After: CAFM-C04-T1, CAFM-C04-T2_
- [ ] CAFM-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051_
  - _Criteria: CAFM-C04-AC-01, CAFM-C04-AC-02, CAFM-C04-AC-03, CAFM-C04-AC-04, CAFM-C04-AC-05, CAFM-C04-AC-06, CAFM-C04-AC-07, CAFM-C04-AC-08, CAFM-C04-AC-09, CAFM-C04-AC-10, CAFM-C04-AC-11, CAFM-C04-AC-12, CAFM-C04-AC-13, CAFM-C04-AC-14, CAFM-C04-AC-15_
  - _After: CAFM-C04-T1, CAFM-C04-T2, CAFM-C04-T3_
- [ ] CAFM-C04-T5 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051_
  - _After: CAFM-C04-T1, CAFM-C04-T2, CAFM-C04-T3_

## CAFM-C05 Decide and reply to card authorization requests (draft)

- [ ] CAFM-C05-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060_
- [ ] CAFM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057_
  - _Rules: CAFM-BR-054, CAFM-BR-055, CAFM-BR-056, CAFM-BR-057, CAFM-BR-058_
  - _After: CAFM-C05-T1_
- [ ] CAFM-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-058_
  - _Rules: CAFM-BR-059_
  - _After: CAFM-C05-T1_
- [ ] CAFM-C05-T4 [api] Build the services behind the screens
  - CAFM-BR-060: Publish each authorization reply once to the reply queue the requester named, carrying the request's correlation id. Send it non-persistent with a short expiry (50, in tenths of a second, so 5 seconds), so stale answers are dropped. If publishing fails, log critical error 'M004'.
  - _Requirements: CAFM-REQ-F-059, CAFM-REQ-F-060_
  - _Rules: CAFM-BR-060_
  - _After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3_
- [ ] CAFM-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060_
  - _Criteria: CAFM-C05-AC-01, CAFM-C05-AC-02, CAFM-C05-AC-03, CAFM-C05-AC-04, CAFM-C05-AC-05, CAFM-C05-AC-06, CAFM-C05-AC-07, CAFM-C05-AC-08, CAFM-C05-AC-09_
  - _After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3, CAFM-C05-T4_
- [ ] CAFM-C05-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060_
  - _After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3, CAFM-C05-T4_

## CAFM-C06 Decide a card authorization request (draft)

- [ ] CAFM-C06-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070_
- [ ] CAFM-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CAFM-BR-070.
  - _Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-065, CAFM-REQ-F-070_
  - _Rules: CAFM-BR-061, CAFM-BR-062, CAFM-BR-063, CAFM-BR-064, CAFM-BR-065, CAFM-BR-067, CAFM-BR-068, CAFM-BR-069, CAFM-BR-070_
  - _After: CAFM-C06-T1_
- [ ] CAFM-C06-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-066_
  - _Rules: CAFM-BR-066_
  - _After: CAFM-C06-T1_
- [ ] CAFM-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070_
  - _Criteria: CAFM-C06-AC-01, CAFM-C06-AC-02, CAFM-C06-AC-03, CAFM-C06-AC-04, CAFM-C06-AC-05, CAFM-C06-AC-06, CAFM-C06-AC-07, CAFM-C06-AC-08, CAFM-C06-AC-09, CAFM-C06-AC-10, CAFM-C06-AC-11, CAFM-C06-AC-12, CAFM-C06-AC-13_
  - _After: CAFM-C06-T1, CAFM-C06-T2, CAFM-C06-T3_
- [ ] CAFM-C06-T5 [compliance] Review the handling of audit, card data, money, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070_
  - _After: CAFM-C06-T1, CAFM-C06-T2, CAFM-C06-T3_

## CAFM-C07 Record pending authorization summary and detail (draft)

- [ ] CAFM-C07-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
- [ ] CAFM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-077, CAFM-REQ-F-078_
  - _Rules: CAFM-BR-071, CAFM-BR-072, CAFM-BR-073, CAFM-BR-074, CAFM-BR-075, CAFM-BR-079, CAFM-BR-080_
  - _After: CAFM-C07-T1_
- [ ] CAFM-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-075, CAFM-REQ-F-079_
  - _Rules: CAFM-BR-076, CAFM-BR-077, CAFM-BR-081_
  - _After: CAFM-C07-T1_
- [ ] CAFM-C07-T4 [api] Build the services behind the screens
  - CAFM-BR-072: Save the account's summary as an upsert keyed by account id: update it if one was found, insert it if not. Do the save in the same transaction as the detail insert, so the summary and its details cannot drift apart.
  - CAFM-BR-078: Insert the authorization detail as a child of the account's summary (a foreign key to the account summary). It holds the request fields and the reply's authorization id, response code, reason and approved amount, and is keyed newest first for paging and purge.
  - _Requirements: CAFM-REQ-F-076_
  - _Rules: CAFM-BR-078_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3_
- [ ] CAFM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
  - _Criteria: CAFM-C07-AC-01, CAFM-C07-AC-02, CAFM-C07-AC-03, CAFM-C07-AC-04, CAFM-C07-AC-05, CAFM-C07-AC-06, CAFM-C07-AC-07, CAFM-C07-AC-08, CAFM-C07-AC-09, CAFM-C07-AC-10, CAFM-C07-AC-11, CAFM-C07-AC-12, CAFM-C07-AC-13_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3, CAFM-C07-T4_
- [ ] CAFM-C07-T6 [compliance] Review the handling of audit, card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3, CAFM-C07-T4_

## CAFM-C08 Log errors and stop on critical failures (draft)

- [ ] CAFM-C08-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081_
- [ ] CAFM-C08-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081_
  - _Rules: CAFM-BR-082, CAFM-BR-083_
  - _After: CAFM-C08-T1_
- [ ] CAFM-C08-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081_
  - _Criteria: CAFM-C08-AC-01, CAFM-C08-AC-02_
  - _After: CAFM-C08-T1, CAFM-C08-T2_
- [ ] CAFM-C08-T4 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081_
  - _After: CAFM-C08-T1, CAFM-C08-T2_

## CAFM-C09 Inquire on an account's pending authorizations (draft)

- [ ] CAFM-C09-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y, CVACT02Y.
  - _Requirements: CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-099, CAFM-REQ-F-100_
- [ ] CAFM-C09-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-099, CAFM-REQ-F-100_
  - _Rules: CAFM-BR-085, CAFM-BR-086, CAFM-BR-087, CAFM-BR-088, CAFM-BR-089, CAFM-BR-103, CAFM-BR-104_
  - _After: CAFM-C09-T1_
- [ ] CAFM-C09-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-082, CAFM-REQ-F-087, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094_
  - _Rules: CAFM-BR-084, CAFM-BR-090, CAFM-BR-093, CAFM-BR-094, CAFM-BR-095, CAFM-BR-096, CAFM-BR-097, CAFM-BR-098, CAFM-BR-099, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102_
  - _After: CAFM-C09-T1_
- [ ] CAFM-C09-T4 [api] Build the services behind the screens
  - CAFM-BR-091: For a valid account number, the screen's backend runs four keyed lookups: the card cross-reference by account id, the account, the customer (by the customer id from the cross-reference) and the pending-authorization summary. It returns them as one view, and fetches the first page of authorization details only when a summary exists.
  - CAFM-BR-092: Keep the customer ID and card number from the cross-reference in the operator's session (or pass them in the navigation state), so the detail and fraud screens can use them without another lookup.
  - _Requirements: CAFM-REQ-F-088, CAFM-REQ-F-089_
  - _Rules: CAFM-BR-091, CAFM-BR-092_
  - _After: CAFM-C09-T1, CAFM-C09-T2, CAFM-C09-T3_
- [ ] CAFM-C09-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **lookup field** "Account ID": Blank: 'Please enter Acct Id' - type the account ID, then press Enter. Not all digits: 'Acct Id must be Numeric' - remove letters, spaces and symbols and use digits only. No card on file: 'Account <account> not found in XREF file' - check the account ID. No account record: 'Account <account> not found in ACCT file' - check the account ID. No customer record: 'Customer <customer> not found in CUST file' - report it to support. Any other read failure: 'System error while reading' with the file and code - try again, or report the code. On any error nothing is loaded, the field keeps the entry so it can be corrected, and focus returns to it.
  - **summary card** "Customer"
  - **summary card** "Limits and balances"
  - **summary card** "Pending authorizations": Summary unreadable: 'System error while reading AUTH Summary: Code <code>' - try again, and report the code if it repeats. The totals and the table stay empty.
  - **data table** "Authorizations": Previous page is disabled on the first page, with 'You are already on the first page'. Next page is disabled on the last page, with 'You are already on the last page'. Next authorization on the last one says 'Already at the last authorization' and keeps the current one open. Rows open directly, so no selection code is typed and 'Invalid selection. Valid value is S' cannot arise. There are no unsupported keys to warn about.
  - _Requirements: CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-100_
  - _Rules: CAFM-BR-084, CAFM-BR-085, CAFM-BR-086, CAFM-BR-087, CAFM-BR-088, CAFM-BR-089, CAFM-BR-090, CAFM-BR-091, CAFM-BR-092, CAFM-BR-093, CAFM-BR-094, CAFM-BR-095, CAFM-BR-096, CAFM-BR-097, CAFM-BR-098, CAFM-BR-099, CAFM-BR-100, CAFM-BR-101, CAFM-BR-102, CAFM-BR-104_
  - _After: CAFM-C09-T2, CAFM-C09-T3, CAFM-C09-T4_
- [ ] CAFM-C09-T6 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER)
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **primary button** "Main menu"
  - _Requirements: CAFM-REQ-F-099_
  - _Rules: CAFM-BR-103_
  - _After: CAFM-C09-T2, CAFM-C09-T3, CAFM-C09-T4_
- [ ] CAFM-C09-T7 [test-generation] Write a test for every acceptance criterion
  - 24 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-099, CAFM-REQ-F-100_
  - _Criteria: CAFM-C09-AC-01, CAFM-C09-AC-02, CAFM-C09-AC-03, CAFM-C09-AC-04, CAFM-C09-AC-05, CAFM-C09-AC-06, CAFM-C09-AC-07, CAFM-C09-AC-08, CAFM-C09-AC-09, CAFM-C09-AC-10, CAFM-C09-AC-11, CAFM-C09-AC-12, CAFM-C09-AC-13, CAFM-C09-AC-14, CAFM-C09-AC-15, CAFM-C09-AC-16, CAFM-C09-AC-17, CAFM-C09-AC-18, CAFM-C09-AC-19, CAFM-C09-AC-20, CAFM-C09-AC-21, CAFM-C09-AC-22, CAFM-C09-AC-23, CAFM-C09-AC-24_
  - _After: CAFM-C09-T1, CAFM-C09-T2, CAFM-C09-T3, CAFM-C09-T4, CAFM-C09-T5, CAFM-C09-T6_
- [ ] CAFM-C09-T8 [compliance] Review the handling of card data, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-082, CAFM-REQ-F-083, CAFM-REQ-F-084, CAFM-REQ-F-085, CAFM-REQ-F-086, CAFM-REQ-F-087, CAFM-REQ-F-088, CAFM-REQ-F-089, CAFM-REQ-F-090, CAFM-REQ-F-091, CAFM-REQ-F-092, CAFM-REQ-F-093, CAFM-REQ-F-094, CAFM-REQ-F-095, CAFM-REQ-F-096, CAFM-REQ-F-097, CAFM-REQ-F-098, CAFM-REQ-F-099, CAFM-REQ-F-100_
  - _After: CAFM-C09-T1, CAFM-C09-T2, CAFM-C09-T3, CAFM-C09-T4, CAFM-C09-T5, CAFM-C09-T6_

## CAFM-C10 Page through an account's pending authorizations (draft)

- [ ] CAFM-C10-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y, CVACT02Y.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108_
- [ ] CAFM-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107_
  - _Rules: CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-109, CAFM-BR-110, CAFM-BR-111, CAFM-BR-112_
  - _After: CAFM-C10-T1_
- [ ] CAFM-C10-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-108_
  - _Rules: CAFM-BR-113, CAFM-BR-114_
  - _After: CAFM-C10-T1_
- [ ] CAFM-C10-T4 [api] Build the services behind the screens
  - CAFM-BR-106: Use keyset paging: a forward page request carries the key of the last authorization shown and returns the next rows after it, or starts from the beginning when there is no key. Re-check that the account's summary still exists before reading the page.
  - CAFM-BR-108: A forward page replaces all five list rows with the next set of up to 5 authorizations. Fetch one row more than the page size to tell whether a further page exists. Keep the first key of each page visited so backward paging can go back to it.
  - _Requirements: CAFM-REQ-F-102_
  - _Rules: CAFM-BR-106_
  - _After: CAFM-C10-T1, CAFM-C10-T2, CAFM-C10-T3_
- [ ] CAFM-C10-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **data table** "Authorizations": Previous page is disabled on the first page, with 'You are already on the first page'. Next page is disabled on the last page, with 'You are already on the last page'. Next authorization on the last one says 'Already at the last authorization' and keeps the current one open. Rows open directly, so no selection code is typed and 'Invalid selection. Valid value is S' cannot arise. There are no unsupported keys to warn about.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108_
  - _Rules: CAFM-BR-105, CAFM-BR-106, CAFM-BR-107, CAFM-BR-108, CAFM-BR-109, CAFM-BR-110, CAFM-BR-111, CAFM-BR-112, CAFM-BR-113, CAFM-BR-114_
  - _After: CAFM-C10-T2, CAFM-C10-T3, CAFM-C10-T4_
- [ ] CAFM-C10-T6 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108_
  - _Criteria: CAFM-C10-AC-01, CAFM-C10-AC-02, CAFM-C10-AC-03, CAFM-C10-AC-04, CAFM-C10-AC-05, CAFM-C10-AC-06, CAFM-C10-AC-07, CAFM-C10-AC-08, CAFM-C10-AC-09, CAFM-C10-AC-10, CAFM-C10-AC-11, CAFM-C10-AC-12, CAFM-C10-AC-13_
  - _After: CAFM-C10-T1, CAFM-C10-T2, CAFM-C10-T3, CAFM-C10-T4, CAFM-C10-T5_
- [ ] CAFM-C10-T7 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108_
  - _After: CAFM-C10-T1, CAFM-C10-T2, CAFM-C10-T3, CAFM-C10-T4, CAFM-C10-T5_

## CAFM-C11 Select an authorization for detail (draft)

- [ ] CAFM-C11-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y, CVACT02Y.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
- [ ] CAFM-C11-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
  - _Rules: CAFM-BR-115, CAFM-BR-116, CAFM-BR-117_
  - _After: CAFM-C11-T1_
- [ ] CAFM-C11-T3 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **data table** "Authorizations": Previous page is disabled on the first page, with 'You are already on the first page'. Next page is disabled on the last page, with 'You are already on the last page'. Next authorization on the last one says 'Already at the last authorization' and keeps the current one open. Rows open directly, so no selection code is typed and 'Invalid selection. Valid value is S' cannot arise. There are no unsupported keys to warn about.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
  - _Rules: CAFM-BR-115, CAFM-BR-116, CAFM-BR-117_
  - _After: CAFM-C11-T2_
- [ ] CAFM-C11-T4 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
  - _Criteria: CAFM-C11-AC-01, CAFM-C11-AC-02, CAFM-C11-AC-03, CAFM-C11-AC-04_
  - _After: CAFM-C11-T1, CAFM-C11-T2, CAFM-C11-T3_
- [ ] CAFM-C11-T5 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
  - _After: CAFM-C11-T1, CAFM-C11-T2, CAFM-C11-T3_

## CAFM-C12 View authorization detail and mark fraud (draft)

- [ ] CAFM-C12-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114_
- [ ] CAFM-C12-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-114_
  - _Rules: CAFM-BR-120_
  - _After: CAFM-C12-T1_
- [ ] CAFM-C12-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113_
  - _Rules: CAFM-BR-118, CAFM-BR-119_
  - _After: CAFM-C12-T1_
- [ ] CAFM-C12-T4 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **status badge** "Response"
  - **summary card** "Authorization": Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed.
  - **primary button** "Report fraud / Remove fraud mark": Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.'
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114_
  - _Rules: CAFM-BR-118, CAFM-BR-119, CAFM-BR-120_
  - _After: CAFM-C12-T2, CAFM-C12-T3_
- [ ] CAFM-C12-T5 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114_
  - _Criteria: CAFM-C12-AC-01, CAFM-C12-AC-02, CAFM-C12-AC-03, CAFM-C12-AC-04, CAFM-C12-AC-05, CAFM-C12-AC-06_
  - _After: CAFM-C12-T1, CAFM-C12-T2, CAFM-C12-T3, CAFM-C12-T4_
- [ ] CAFM-C12-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114_
  - _After: CAFM-C12-T1, CAFM-C12-T2, CAFM-C12-T3, CAFM-C12-T4_

## CAFM-C13 View pending authorization details (draft)

- [ ] CAFM-C13-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
  - _Requirements: CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126_
- [ ] CAFM-C13-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-115, CAFM-REQ-F-121, CAFM-REQ-F-122_
  - _Rules: CAFM-BR-121, CAFM-BR-122, CAFM-BR-123, CAFM-BR-129, CAFM-BR-130_
  - _After: CAFM-C13-T1_
- [ ] CAFM-C13-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120_
  - _Rules: CAFM-BR-124, CAFM-BR-125, CAFM-BR-126, CAFM-BR-127, CAFM-BR-128, CAFM-BR-132, CAFM-BR-133, CAFM-BR-134_
  - _After: CAFM-C13-T1_
- [ ] CAFM-C13-T4 [api] Build the services behind the screens
  - CAFM-BR-131: Retrieval is two keyed lookups, one after the other: first the account's pending authorization summary by account id, then, only if that is found, the authorization detail under that account by the selected authorization key. The new store needs the account to own its authorizations (for example a summary keyed by account id with details keyed by account id plus authorization key), so a detail can never be fetched for an account that has no summary. A missing summary or detail is treated as 'nothing to show', not as an error.
  - _Requirements: CAFM-REQ-F-123_
  - _Rules: CAFM-BR-131_
  - _After: CAFM-C13-T1, CAFM-C13-T2, CAFM-C13-T3_
- [ ] CAFM-C13-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **summary card** "Authorization": Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed.
  - **summary card** "Merchant"
  - **status badge** "Fraud status"
  - _Requirements: CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126_
  - _Rules: CAFM-BR-121, CAFM-BR-122, CAFM-BR-123, CAFM-BR-124, CAFM-BR-125, CAFM-BR-126, CAFM-BR-127, CAFM-BR-128, CAFM-BR-129, CAFM-BR-130, CAFM-BR-131, CAFM-BR-132, CAFM-BR-133, CAFM-BR-134_
  - _After: CAFM-C13-T2, CAFM-C13-T3, CAFM-C13-T4_
- [ ] CAFM-C13-T6 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126_
  - _Criteria: CAFM-C13-AC-01, CAFM-C13-AC-02, CAFM-C13-AC-03, CAFM-C13-AC-04, CAFM-C13-AC-05, CAFM-C13-AC-06, CAFM-C13-AC-07, CAFM-C13-AC-08, CAFM-C13-AC-09, CAFM-C13-AC-10, CAFM-C13-AC-11, CAFM-C13-AC-12, CAFM-C13-AC-13, CAFM-C13-AC-14, CAFM-C13-AC-15_
  - _After: CAFM-C13-T1, CAFM-C13-T2, CAFM-C13-T3, CAFM-C13-T4, CAFM-C13-T5_
- [ ] CAFM-C13-T7 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126_
  - _After: CAFM-C13-T1, CAFM-C13-T2, CAFM-C13-T3, CAFM-C13-T4, CAFM-C13-T5_

## CAFM-C14 Navigate the authorization detail screen (draft)

- [ ] CAFM-C14-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
  - _Requirements: CAFM-REQ-F-127, CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132_
- [ ] CAFM-C14-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-132_
  - _Rules: CAFM-BR-136, CAFM-BR-137, CAFM-BR-138, CAFM-BR-139, CAFM-BR-141, CAFM-BR-142_
  - _After: CAFM-C14-T1_
- [ ] CAFM-C14-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-131_
  - _Rules: CAFM-BR-140_
  - _After: CAFM-C14-T1_
- [ ] CAFM-C14-T4 [api] Build the services behind the screens
  - CAFM-BR-135: The detail view can only be reached with an account and a selected authorization from the pending authorization list. If it is opened directly, with no account or selection carried in (a bare URL, an expired session), it must redirect to the account's pending authorization list instead of showing an empty or default detail page.
  - _Requirements: CAFM-REQ-F-127_
  - _Rules: CAFM-BR-135_
  - _After: CAFM-C14-T1, CAFM-C14-T2, CAFM-C14-T3_
- [ ] CAFM-C14-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **data table** "Authorizations": Previous page is disabled on the first page, with 'You are already on the first page'. Next page is disabled on the last page, with 'You are already on the last page'. Next authorization on the last one says 'Already at the last authorization' and keeps the current one open. Rows open directly, so no selection code is typed and 'Invalid selection. Valid value is S' cannot arise. There are no unsupported keys to warn about.
  - **summary card** "Authorization": Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed.
  - _Requirements: CAFM-REQ-F-127, CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132_
  - _Rules: CAFM-BR-135, CAFM-BR-136, CAFM-BR-137, CAFM-BR-138, CAFM-BR-139, CAFM-BR-140, CAFM-BR-141, CAFM-BR-142_
  - _After: CAFM-C14-T2, CAFM-C14-T3, CAFM-C14-T4_
- [ ] CAFM-C14-T6 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-127, CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132_
  - _Criteria: CAFM-C14-AC-01, CAFM-C14-AC-02, CAFM-C14-AC-03, CAFM-C14-AC-04, CAFM-C14-AC-05, CAFM-C14-AC-06, CAFM-C14-AC-07, CAFM-C14-AC-08_
  - _After: CAFM-C14-T1, CAFM-C14-T2, CAFM-C14-T3, CAFM-C14-T4, CAFM-C14-T5_
- [ ] CAFM-C14-T7 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-127, CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132_
  - _After: CAFM-C14-T1, CAFM-C14-T2, CAFM-C14-T3, CAFM-C14-T4, CAFM-C14-T5_

## CAFM-C15 Mark or unmark an authorization as fraud (draft)

- [ ] CAFM-C15-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
  - _Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141_
- [ ] CAFM-C15-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-F-141_
  - _Rules: CAFM-BR-143, CAFM-BR-144, CAFM-BR-145, CAFM-BR-146, CAFM-BR-147, CAFM-BR-148, CAFM-BR-149, CAFM-BR-150, CAFM-BR-151, CAFM-BR-156_
  - _After: CAFM-C15-T1_
- [ ] CAFM-C15-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140_
  - _Rules: CAFM-BR-152, CAFM-BR-153, CAFM-BR-154, CAFM-BR-155_
  - _After: CAFM-C15-T1_
- [ ] CAFM-C15-T4 [api] Build the services behind the screens
  - CAFM-BR-147: The fraud action is one synchronous call from the detail screen to a fraud-recording service, passing the full authorization, the account number, the customer number and the action ('F' report or 'R' remove). The service stamps today's date (MM/DD/YY) as the fraud report date on the authorization it returns and reports success or failure with a message. Both the fraud register write and the authorization update must run in one transaction (or an equivalent all-or-nothing mechanism), committed only after the authorization update succeeds.
  - _Requirements: CAFM-REQ-F-135_
  - _Rules: CAFM-BR-147_
  - _After: CAFM-C15-T1, CAFM-C15-T2, CAFM-C15-T3_
- [ ] CAFM-C15-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **primary button** "Report fraud / Remove fraud mark": Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.'
  - _Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141_
  - _Rules: CAFM-BR-143, CAFM-BR-144, CAFM-BR-145, CAFM-BR-146, CAFM-BR-147, CAFM-BR-148, CAFM-BR-149, CAFM-BR-150, CAFM-BR-151, CAFM-BR-152, CAFM-BR-153, CAFM-BR-154, CAFM-BR-155, CAFM-BR-156_
  - _After: CAFM-C15-T2, CAFM-C15-T3, CAFM-C15-T4_
- [ ] CAFM-C15-T6 [test-generation] Write a test for every acceptance criterion
  - 17 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141_
  - _Criteria: CAFM-C15-AC-01, CAFM-C15-AC-02, CAFM-C15-AC-03, CAFM-C15-AC-04, CAFM-C15-AC-05, CAFM-C15-AC-06, CAFM-C15-AC-07, CAFM-C15-AC-08, CAFM-C15-AC-09, CAFM-C15-AC-10, CAFM-C15-AC-11, CAFM-C15-AC-12, CAFM-C15-AC-13, CAFM-C15-AC-14, CAFM-C15-AC-15, CAFM-C15-AC-16, CAFM-C15-AC-17_
  - _After: CAFM-C15-T1, CAFM-C15-T2, CAFM-C15-T3, CAFM-C15-T4, CAFM-C15-T5_
- [ ] CAFM-C15-T7 [compliance] Review the handling of audit, card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141_
  - _After: CAFM-C15-T1, CAFM-C15-T2, CAFM-C15-T3, CAFM-C15-T4, CAFM-C15-T5_

## CAFM-C16 Record fraud action in the fraud register (draft)

- [ ] CAFM-C16-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY.
  - _Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146_
- [ ] CAFM-C16-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-143, CAFM-REQ-F-144_
  - _Rules: CAFM-BR-158, CAFM-BR-159_
  - _After: CAFM-C16-T1_
- [ ] CAFM-C16-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-145, CAFM-REQ-F-146_
  - _Rules: CAFM-BR-160, CAFM-BR-161_
  - _After: CAFM-C16-T1_
- [ ] CAFM-C16-T4 [api] Build the services behind the screens
  - CAFM-BR-157: The fraud register is keyed by card number plus the authorization's original timestamp. The legacy authorization stores its time as a complement (999999999 minus the time) so newest sorts first; the new application should store the real authorization timestamp on the authorization and use it directly, with a unique key on (card number, authorization timestamp) so that recording is an upsert. If legacy data is migrated, convert the complemented time once, during migration.
  - _Requirements: CAFM-REQ-F-142_
  - _Rules: CAFM-BR-157_
  - _After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3_
- [ ] CAFM-C16-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **primary button** "Report fraud / Remove fraud mark": Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.'
  - _Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146_
  - _Rules: CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-160, CAFM-BR-161_
  - _After: CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4_
- [ ] CAFM-C16-T6 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146_
  - _Criteria: CAFM-C16-AC-01, CAFM-C16-AC-02, CAFM-C16-AC-03, CAFM-C16-AC-04, CAFM-C16-AC-05_
  - _After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4, CAFM-C16-T5_
- [ ] CAFM-C16-T7 [compliance] Review the handling of audit, card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146_
  - _After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4, CAFM-C16-T5_

## CAFM-C17 Unload the pending authorization database (draft)

- [ ] CAFM-C17-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PADFLPCB, PASFLPCB, PAUTBPCB.
  - _Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155_
- [ ] CAFM-C17-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-149_
  - _Rules: CAFM-BR-164_
  - _After: CAFM-C17-T1_
- [ ] CAFM-C17-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155_
  - _Rules: CAFM-BR-168, CAFM-BR-169, CAFM-BR-170, CAFM-BR-171_
  - _After: CAFM-C17-T1_
- [ ] CAFM-C17-T4 [api] Build the scheduled job
  - CAFM-BR-162: A scheduled full extract of the pending authorization store into a single new file of variable-length records (up to 27990 bytes), read without locking out online users. The file must only be published when the job succeeds: write to a temporary name and rename on success, or delete it on failure, so a failed run never leaves a usable-looking extract.
  - CAFM-BR-163: The extract walks all summaries in a stable order (by account id) and, for each one with a numeric account id, writes the summary and then all its details before moving to the next summary. With a relational store this is a query of summaries ordered by account id joined to their details, streamed out so memory use does not grow with volume.
  - CAFM-BR-165: The job ends normally when there are no more summaries to read; reaching the end of the data is a normal finish, not an error.
  - CAFM-BR-166: For each summary, every one of its details is written to the separate detail file, in the order they are held under that summary (newest first in the legacy store), so a reload can attach each detail to its summary.
  - CAFM-BR-167: Running out of details for a summary is a normal step, not an error: log 'CHILD SEG FLAG GE : Y', reset the per-summary state and continue with the next summary.
  - _Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152_
  - _Rules: CAFM-BR-162, CAFM-BR-163, CAFM-BR-165, CAFM-BR-166, CAFM-BR-167_
  - _After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3_
- [ ] CAFM-C17-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155_
  - _Criteria: CAFM-C17-AC-01, CAFM-C17-AC-02, CAFM-C17-AC-03, CAFM-C17-AC-04, CAFM-C17-AC-05, CAFM-C17-AC-06, CAFM-C17-AC-07, CAFM-C17-AC-08, CAFM-C17-AC-09, CAFM-C17-AC-10_
  - _After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3, CAFM-C17-T4_
- [ ] CAFM-C17-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155_
  - _After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3, CAFM-C17-T4_

## CAFM-C18 Load pending authorizations into the database (draft)

- [ ] CAFM-C18-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
  - _Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165_
- [ ] CAFM-C18-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-158, CAFM-REQ-F-159_
  - _Rules: CAFM-BR-175, CAFM-BR-176_
  - _After: CAFM-C18-T1_
- [ ] CAFM-C18-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165_
  - _Rules: CAFM-BR-177, CAFM-BR-178, CAFM-BR-179, CAFM-BR-180_
  - _After: CAFM-C18-T1_
- [ ] CAFM-C18-T4 [api] Build the scheduled job
  - CAFM-BR-172: A batch load job that takes two input files, a summary file and a detail file, and inserts their records into the pending authorization store while online use continues (it must not need exclusive access to the store).
  - CAFM-BR-173: The load runs in two phases: read the whole summary file and insert every summary, and only then read the detail file. This order guarantees each detail's parent summary already exists when the detail is inserted.
  - CAFM-BR-174: Each detail is attached to its summary by account id: look up the summary by account id (a keyed lookup) and insert the detail under it, for example as a child row with a foreign key to the summary. A detail whose summary cannot be found is skipped, not loaded as an orphan.
  - _Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157_
  - _Rules: CAFM-BR-172, CAFM-BR-173, CAFM-BR-174_
  - _After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3_
- [ ] CAFM-C18-T5 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165_
  - _Criteria: CAFM-C18-AC-01, CAFM-C18-AC-02, CAFM-C18-AC-03, CAFM-C18-AC-04, CAFM-C18-AC-05, CAFM-C18-AC-06, CAFM-C18-AC-07, CAFM-C18-AC-08, CAFM-C18-AC-09, CAFM-C18-AC-10, CAFM-C18-AC-11, CAFM-C18-AC-12_
  - _After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3, CAFM-C18-T4_
- [ ] CAFM-C18-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-156, CAFM-REQ-F-157, CAFM-REQ-F-158, CAFM-REQ-F-159, CAFM-REQ-F-160, CAFM-REQ-F-161, CAFM-REQ-F-162, CAFM-REQ-F-163, CAFM-REQ-F-164, CAFM-REQ-F-165_
  - _After: CAFM-C18-T1, CAFM-C18-T2, CAFM-C18-T3, CAFM-C18-T4_

## CAFM-C19 Load pending authorization summaries (draft)

- [ ] CAFM-C19-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169_
- [ ] CAFM-C19-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167_
  - _Rules: CAFM-BR-181_
  - _After: CAFM-C19-T1_
- [ ] CAFM-C19-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-168, CAFM-REQ-F-169_
  - _Rules: CAFM-BR-182, CAFM-BR-183_
  - _After: CAFM-C19-T1_
- [ ] CAFM-C19-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169_
  - _Rules: CAFM-BR-181, CAFM-BR-182, CAFM-BR-183_
  - _After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3_
- [ ] CAFM-C19-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169_
  - _Criteria: CAFM-C19-AC-01, CAFM-C19-AC-02, CAFM-C19-AC-03_
  - _After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3, CAFM-C19-T4_
- [ ] CAFM-C19-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169_
  - _After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3, CAFM-C19-T4_

## CAFM-C20 Unload all pending authorizations (draft)

- [ ] CAFM-C20-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
  - _Requirements: CAFM-REQ-F-170, CAFM-REQ-F-171, CAFM-REQ-F-172, CAFM-REQ-F-173, CAFM-REQ-F-174, CAFM-REQ-F-175, CAFM-REQ-F-176, CAFM-REQ-F-177, CAFM-REQ-F-178, CAFM-REQ-F-179_
- [ ] CAFM-C20-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-170, CAFM-REQ-F-172, CAFM-REQ-F-174_
  - _Rules: CAFM-BR-184, CAFM-BR-186, CAFM-BR-188_
  - _After: CAFM-C20-T1_
- [ ] CAFM-C20-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-176, CAFM-REQ-F-179_
  - _Rules: CAFM-BR-190, CAFM-BR-193_
  - _After: CAFM-C20-T1_
- [ ] CAFM-C20-T4 [api] Build the scheduled job
  - CAFM-BR-185: The job walks all summaries one by one in a stable order (by account id), finishing each summary and its details before moving to the next; stream the results rather than loading them all into memory.
  - CAFM-BR-187: The summary file holds one fixed 100-byte record per summary, the summary exactly as stored. The new application needs a defined summary export layout of the same fields, byte-compatible with the legacy layout for as long as anything still reads these files.
  - CAFM-BR-189: When there are no more summaries, the job closes both output files and ends normally (return code 0); reaching the end of the data is not an error.
  - CAFM-BR-191: The detail file holds one fixed 206-byte record per detail: the parent account id (6 bytes, packed decimal in the legacy layout) followed by the 200-byte detail as stored. The account id prefix is what lets a reload attach each detail to its summary, so the new export must always carry it; keep packed decimal only while legacy consumers need it.
  - CAFM-BR-192: Running out of details for a summary is a normal step: log 'CHILD SEG FLAG GE : ' with the end flag and continue with the next summary.
  - _Requirements: CAFM-REQ-F-171, CAFM-REQ-F-173, CAFM-REQ-F-175, CAFM-REQ-F-177, CAFM-REQ-F-178_
  - _Rules: CAFM-BR-185, CAFM-BR-187, CAFM-BR-189, CAFM-BR-191, CAFM-BR-192_
  - _After: CAFM-C20-T1, CAFM-C20-T2, CAFM-C20-T3_
- [ ] CAFM-C20-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-170, CAFM-REQ-F-171, CAFM-REQ-F-172, CAFM-REQ-F-173, CAFM-REQ-F-174, CAFM-REQ-F-175, CAFM-REQ-F-176, CAFM-REQ-F-177, CAFM-REQ-F-178, CAFM-REQ-F-179_
  - _Criteria: CAFM-C20-AC-01, CAFM-C20-AC-02, CAFM-C20-AC-03, CAFM-C20-AC-04, CAFM-C20-AC-05, CAFM-C20-AC-06, CAFM-C20-AC-07, CAFM-C20-AC-08, CAFM-C20-AC-09, CAFM-C20-AC-10_
  - _After: CAFM-C20-T1, CAFM-C20-T2, CAFM-C20-T3, CAFM-C20-T4_
- [ ] CAFM-C20-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-170, CAFM-REQ-F-171, CAFM-REQ-F-172, CAFM-REQ-F-173, CAFM-REQ-F-174, CAFM-REQ-F-175, CAFM-REQ-F-176, CAFM-REQ-F-177, CAFM-REQ-F-178, CAFM-REQ-F-179_
  - _After: CAFM-C20-T1, CAFM-C20-T2, CAFM-C20-T3, CAFM-C20-T4_

## CAFM-C21 Run the unload jobs and manage unload files (draft)

- [ ] CAFM-C21-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
  - _Requirements: CAFM-REQ-N-004, CAFM-REQ-N-005, CAFM-REQ-N-006, CAFM-REQ-F-180, CAFM-REQ-F-181, CAFM-REQ-F-182, CAFM-REQ-F-183_
- [ ] CAFM-C21-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-182, CAFM-REQ-F-183_
  - _Rules: CAFM-BR-199, CAFM-BR-200_
  - _After: CAFM-C21-T1_
- [ ] CAFM-C21-T3 [api] Build the scheduled job
  - CAFM-BR-194: A scheduled batch job (legacy DBUNLDGS) that reads the whole pending authorization store, summaries with their details, with read-only shared access so online users are not locked out.
  - CAFM-BR-195: This job writes to two standing output files, root (summary) and child (detail), that already exist. Only this job may write to them while it runs, and both are kept whether the job succeeds or fails, so downstream users must check the job's outcome before trusting their contents.
  - CAFM-BR-196: A second scheduled batch job (legacy PAUDBUNL) that reads the pending authorization store with shared read-only access and writes summaries to the first output file and details to the second.
  - CAFM-BR-197: The root unload file, of fixed 100-byte records, is created new on each run and published only when the job succeeds; on failure it is deleted (write under a temporary name and rename on success).
  - CAFM-BR-198: The child unload file, of fixed 206-byte records, is created new on each run and published only when the job succeeds; on failure it is deleted, the same as the root file.
  - _Requirements: CAFM-REQ-N-004, CAFM-REQ-N-005, CAFM-REQ-N-006, CAFM-REQ-F-180, CAFM-REQ-F-181_
  - _Rules: CAFM-BR-194, CAFM-BR-195, CAFM-BR-196, CAFM-BR-197, CAFM-BR-198_
  - _After: CAFM-C21-T1, CAFM-C21-T2_
- [ ] CAFM-C21-T4 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-N-004, CAFM-REQ-N-005, CAFM-REQ-N-006, CAFM-REQ-F-180, CAFM-REQ-F-181, CAFM-REQ-F-182, CAFM-REQ-F-183_
  - _Criteria: CAFM-C21-AC-01, CAFM-C21-AC-02, CAFM-C21-AC-03, CAFM-C21-AC-04, CAFM-C21-AC-05, CAFM-C21-AC-06, CAFM-C21-AC-07, CAFM-C21-AC-08, CAFM-C21-AC-09, CAFM-C21-AC-10_
  - _After: CAFM-C21-T1, CAFM-C21-T2, CAFM-C21-T3_
- [ ] CAFM-C21-T5 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-N-004, CAFM-REQ-N-005, CAFM-REQ-N-006, CAFM-REQ-F-180, CAFM-REQ-F-181, CAFM-REQ-F-182, CAFM-REQ-F-183_
  - _After: CAFM-C21-T1, CAFM-C21-T2, CAFM-C21-T3_

## SOM-C01 Register online CardDemo programs and transactions (draft)

- [ ] SOM-C01-T1 [api] Build the scheduled job
  - SOM-BR-001: Register the sign-on screen as a routable entry point (for example a route or deep-link code that matches legacy code CC00) in the application's deployment or route configuration, which is applied when the environment is provisioned. It must be open to any user who has not signed on. No data-location setting is needed.
  - SOM-BR-002: Register the Admin Menu as a routable entry point under the code CCAD in the same deployment or route configuration as the sign-on screen, so the configuration is versioned and applied with each release.
  - SOM-BR-003: Map a second entry code, CCDM, to the same Admin Menu route, so both CCAD and CCDM open the Admin Menu. Keep it as an alias in the route configuration, not a separate screen.
  - _Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003_
  - _Rules: SOM-BR-001, SOM-BR-002, SOM-BR-003_
- [ ] SOM-C01-T2 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003_
  - _Criteria: SOM-C01-AC-01, SOM-C01-AC-02, SOM-C01-AC-03_
  - _After: SOM-C01-T1_
- [ ] SOM-C01-T3 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003_
  - _After: SOM-C01-T1_

## SOM-C02 Navigate the Admin Menu (draft)

- [ ] SOM-C02-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COADM02Y, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSUSR01Y.
  - _Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001_
- [ ] SOM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: SOM-BR-012.
  - _Requirements: SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-N-001, SOM-REQ-F-011_
  - _Rules: SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-010, SOM-BR-012, SOM-BR-013_
  - _After: SOM-C02-T1_
- [ ] SOM-C02-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: SOM-REQ-F-010, SOM-REQ-F-004, SOM-REQ-F-005_
  - _Rules: SOM-BR-004, SOM-BR-005, SOM-BR-011_
  - _After: SOM-C02-T1_
- [ ] SOM-C02-T4 [ui-modernization] Build the screen Home (S-HOME)
  - To the prototype: ui-reference/index.html#/S-HOME.
  - **data table** "Functions": Only the functions the role may use are listed, so the 'Please enter a valid option number...' error cannot happen. If a regular user still reaches an administrator function, the server refuses it with 'No access - Admin Only option... '. A coming-soon row opens nothing and says 'This option <name> is coming soon ...'. A function that is not installed opens nothing and says 'This option <name> is not installed...'. Only Enter and click act on a row, so the 'Invalid key pressed. Please see below...' message is no longer needed.
  - **status badge** "Availability"
  - _Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011_
  - _Rules: SOM-BR-004, SOM-BR-005, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-010, SOM-BR-011, SOM-BR-012_
  - _After: SOM-C02-T2, SOM-C02-T3_
- [ ] SOM-C02-T5 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER)
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **data table** "Navigation": Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home.
  - _Requirements: SOM-REQ-N-001_
  - _Rules: SOM-BR-013_
  - _After: SOM-C02-T2, SOM-C02-T3_
- [ ] SOM-C02-T6 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001_
  - _Criteria: SOM-C02-AC-01, SOM-C02-AC-02, SOM-C02-AC-03, SOM-C02-AC-04, SOM-C02-AC-05, SOM-C02-AC-06, SOM-C02-AC-07, SOM-C02-AC-08, SOM-C02-AC-09, SOM-C02-AC-10, SOM-C02-AC-11, SOM-C02-AC-12, SOM-C02-AC-13, SOM-C02-AC-14, SOM-C02-AC-15_
  - _After: SOM-C02-T1, SOM-C02-T2, SOM-C02-T3, SOM-C02-T4, SOM-C02-T5_
- [ ] SOM-C02-T7 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001_
  - _After: SOM-C02-T1, SOM-C02-T2, SOM-C02-T3, SOM-C02-T4, SOM-C02-T5_

## SOM-C03 Navigate the Main Menu with access control (draft)

- [ ] SOM-C03-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COMEN02Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSUSR01Y.
  - _Requirements: SOM-REQ-F-012, SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-015, SOM-REQ-F-016, SOM-REQ-F-017, SOM-REQ-F-018, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-021, SOM-REQ-F-022, SOM-REQ-F-023, SOM-REQ-F-024, SOM-REQ-F-025_
- [ ] SOM-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: SOM-REQ-F-012, SOM-REQ-F-016, SOM-REQ-F-017, SOM-REQ-F-018, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-022, SOM-REQ-F-023_
  - _Rules: SOM-BR-014, SOM-BR-017, SOM-BR-019, SOM-BR-020, SOM-BR-021, SOM-BR-022, SOM-BR-023, SOM-BR-024, SOM-BR-026, SOM-BR-027_
  - _After: SOM-C03-T1_
- [ ] SOM-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: SOM-REQ-F-024, SOM-REQ-F-015, SOM-REQ-F-021_
  - _Rules: SOM-BR-018, SOM-BR-025, SOM-BR-028_
  - _After: SOM-C03-T1_
- [ ] SOM-C03-T4 [api] Build the services behind the screens
  - SOM-BR-015: Distinguish the first display of the menu from a submission: arriving at the menu (a GET or navigation) renders it, and only a submission (POST or action) reads the input and handles the key. Track this through the request type or a per-session screen state. Do not use a shared flag.
  - SOM-BR-016: When the menu is entered fresh, for example after sign-on or on return from a function screen, set the session's menu state to 're-enter' and render a clean menu with no option value and no message. Do not process any input on this request.
  - SOM-BR-017: On a submission, dispatch on the action: 'Enter' or submit processes the chosen option, 'PF3' (a Back or Exit action) returns to the sign-on screen, and any other action re-renders the menu with 'Invalid key pressed. Please see below...'. Map the legacy function keys to explicit actions or keyboard shortcuts in the new UI.
  - SOM-BR-019: Normalise the typed option before validating it: trim trailing blanks, left-pad it to two digits with zeros, and echo the two-digit value back in the option field. A numeric input limited to two digits is enough in the new UI, provided the echo and the validation behave the same.
  - SOM-BR-029: After any interaction that stays on the menu, keep the user's session, including user identity, type and navigation origin, so the next submission returns to the Main Menu. In a web application this is ordinary server-side or token session state between requests. Nothing needs to stay running while the application waits for the user.
  - _Requirements: SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-025_
  - _Rules: SOM-BR-015, SOM-BR-016, SOM-BR-017, SOM-BR-029_
  - _After: SOM-C03-T1, SOM-C03-T2, SOM-C03-T3_
- [ ] SOM-C03-T5 [ui-modernization] Build the screen Home (S-HOME)
  - To the prototype: ui-reference/index.html#/S-HOME.
  - **data table** "Functions": Only the functions the role may use are listed, so the 'Please enter a valid option number...' error cannot happen. If a regular user still reaches an administrator function, the server refuses it with 'No access - Admin Only option... '. A coming-soon row opens nothing and says 'This option <name> is coming soon ...'. A function that is not installed opens nothing and says 'This option <name> is not installed...'. Only Enter and click act on a row, so the 'Invalid key pressed. Please see below...' message is no longer needed.
  - **status badge** "Availability"
  - _Requirements: SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-015, SOM-REQ-F-016, SOM-REQ-F-018, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-021, SOM-REQ-F-022, SOM-REQ-F-023, SOM-REQ-F-024, SOM-REQ-F-025_
  - _Rules: SOM-BR-015, SOM-BR-016, SOM-BR-017, SOM-BR-018, SOM-BR-019, SOM-BR-020, SOM-BR-022, SOM-BR-023, SOM-BR-024, SOM-BR-025, SOM-BR-026, SOM-BR-027, SOM-BR-028, SOM-BR-029_
  - _After: SOM-C03-T2, SOM-C03-T3, SOM-C03-T4_
- [ ] SOM-C03-T6 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER)
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **data table** "Navigation": Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home.
  - **primary button** "Sign out"
  - _Requirements: SOM-REQ-F-012, SOM-REQ-F-017_
  - _Rules: SOM-BR-014, SOM-BR-017, SOM-BR-021_
  - _After: SOM-C03-T2, SOM-C03-T3, SOM-C03-T4_
- [ ] SOM-C03-T7 [test-generation] Write a test for every acceptance criterion
  - 23 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-012, SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-015, SOM-REQ-F-016, SOM-REQ-F-017, SOM-REQ-F-018, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-021, SOM-REQ-F-022, SOM-REQ-F-023, SOM-REQ-F-024, SOM-REQ-F-025_
  - _Criteria: SOM-C03-AC-01, SOM-C03-AC-02, SOM-C03-AC-03, SOM-C03-AC-04, SOM-C03-AC-05, SOM-C03-AC-06, SOM-C03-AC-07, SOM-C03-AC-08, SOM-C03-AC-09, SOM-C03-AC-10, SOM-C03-AC-11, SOM-C03-AC-12, SOM-C03-AC-13, SOM-C03-AC-14, SOM-C03-AC-15, SOM-C03-AC-16, SOM-C03-AC-17, SOM-C03-AC-18, SOM-C03-AC-19, SOM-C03-AC-20, SOM-C03-AC-21, SOM-C03-AC-22, SOM-C03-AC-23_
  - _After: SOM-C03-T1, SOM-C03-T2, SOM-C03-T3, SOM-C03-T4, SOM-C03-T5, SOM-C03-T6_
- [ ] SOM-C03-T8 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: SOM-REQ-F-012, SOM-REQ-F-013, SOM-REQ-F-014, SOM-REQ-F-015, SOM-REQ-F-016, SOM-REQ-F-017, SOM-REQ-F-018, SOM-REQ-F-019, SOM-REQ-F-020, SOM-REQ-F-021, SOM-REQ-F-022, SOM-REQ-F-023, SOM-REQ-F-024, SOM-REQ-F-025_
  - _After: SOM-C03-T1, SOM-C03-T2, SOM-C03-T3, SOM-C03-T4, SOM-C03-T5, SOM-C03-T6_

## SOM-C04 Send the CardDemo test file by FTP (draft)

- [ ] SOM-C04-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: SOM-REQ-F-026, SOM-REQ-F-027_
  - _Rules: SOM-BR-030, SOM-BR-031_
- [ ] SOM-C04-T2 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: SOM-REQ-F-026, SOM-REQ-F-027_
  - _Rules: SOM-BR-030, SOM-BR-031_
  - _After: SOM-C04-T1_
- [ ] SOM-C04-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-026, SOM-REQ-F-027_
  - _Criteria: SOM-C04-AC-01, SOM-C04-AC-02_
  - _After: SOM-C04-T1, SOM-C04-T2_
- [ ] SOM-C04-T4 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: SOM-REQ-F-026, SOM-REQ-F-027_
  - _After: SOM-C04-T1, SOM-C04-T2_

## SOM-C05 Back up and distribute the FTP test file (draft)

- [ ] SOM-C05-T1 [api] Build the scheduled job
  - SOM-BR-032: A scheduled job step that copies the FTP test file record for record into the existing backup location, for example object-storage copy or file copy. It must not lock out other readers or writers while it runs, and it fails if the backup target does not already exist.
  - SOM-BR-033: After the backup step succeeds, the job triggers the follow-on job (INTRDRJ2) from its stored, unchanged definition. In a modern scheduler or workflow engine this is a job dependency or chained trigger, not the copying of a job definition to a reader. The legacy output class 'A' becomes the follow-on job's default log destination.
  - SOM-BR-034: A follow-on job that copies every record of the backup file into the already-existing secondary copy (the '.INTRDR' copy). Both files stay readable by other jobs while it runs. It runs only when the first job triggers it.
  - _Requirements: SOM-REQ-F-028, SOM-REQ-F-029, SOM-REQ-F-030_
  - _Rules: SOM-BR-032, SOM-BR-033, SOM-BR-034_
- [ ] SOM-C05-T2 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-028, SOM-REQ-F-029, SOM-REQ-F-030_
  - _Criteria: SOM-C05-AC-01, SOM-C05-AC-02, SOM-C05-AC-03_
  - _After: SOM-C05-T1_

## SOM-C06 Authorize online transaction under the card security profile (draft)

- [ ] SOM-C06-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: SOM-REQ-F-031_
  - _Rules: SOM-BR-035_
- [ ] SOM-C06-T2 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: SOM-REQ-F-031_
  - _Rules: SOM-BR-035_
  - _After: SOM-C06-T1_
- [ ] SOM-C06-T3 [test-generation] Write a test for every acceptance criterion
  - 1 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-031_
  - _Criteria: SOM-C06-AC-01_
  - _After: SOM-C06-T1, SOM-C06-T2_
- [ ] SOM-C06-T4 [compliance] Review the handling of audit, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: SOM-REQ-F-031_
  - _After: SOM-C06-T1, SOM-C06-T2_

## USPM-C01 Sign on to CardDemo (draft)

- [ ] USPM-C01-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-001, USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013, USPM-REQ-F-014_
- [ ] USPM-C01-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013_
  - _Rules: USPM-BR-002, USPM-BR-003, USPM-BR-004, USPM-BR-005, USPM-BR-006, USPM-BR-008, USPM-BR-009, USPM-BR-010, USPM-BR-011, USPM-BR-012, USPM-BR-013, USPM-BR-014, USPM-BR-015, USPM-BR-016_
  - _After: USPM-C01-T1_
- [ ] USPM-C01-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-007, USPM-REQ-F-001_
  - _Rules: USPM-BR-001, USPM-BR-007_
  - _After: USPM-C01-T1_
- [ ] USPM-C01-T4 [api] Build the services behind the screens
  - USPM-BR-010: After a successful sign-on, create a session that holds the upper-cased user ID, the user type read from the user record, where the user came from (sign-on) and a 'first entry' marker. Every later screen reads this session to know who the user is and what role they have.
  - USPM-BR-017: While the sign-on screen is showing (first visit, after an input error or after an invalid key), keep the session alive and wait for the user's next action on that screen. Do not lose session data between round trips.
  - _Requirements: USPM-REQ-F-014_
  - _Rules: USPM-BR-017_
  - _After: USPM-C01-T1, USPM-C01-T2, USPM-C01-T3_
- [ ] USPM-C01-T5 [ui-modernization] Build the screen Sign in (S-SIGN-IN)
  - To the prototype: ui-reference/index.html#/S-SIGN-IN.
  - **summary card** "You have signed out"
  - **lookup field** "User ID": Blank: 'Please enter User ID ...', with focus back on User ID. Not on file: 'User not found. Try again ...' Read failure: 'Unable to verify the User ...' Each message shows under User ID.
  - **lookup field** "Password": Blank: 'Please enter Password ...' Wrong password: 'Wrong Password. Try again ...' Each message shows under Password, with focus on it. Failed attempts are logged; the owner decides the attempt limit and lockout (the legacy allows unlimited attempts).
  - **primary button** "Sign in": Checks User ID first, then Password, and reports the first problem under its field.
  - _Requirements: USPM-REQ-F-001, USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013, USPM-REQ-F-014_
  - _Rules: USPM-BR-001, USPM-BR-002, USPM-BR-003, USPM-BR-004, USPM-BR-005, USPM-BR-006, USPM-BR-007, USPM-BR-008, USPM-BR-009, USPM-BR-010, USPM-BR-011, USPM-BR-012, USPM-BR-013, USPM-BR-014, USPM-BR-015, USPM-BR-016, USPM-BR-017_
  - _After: USPM-C01-T2, USPM-C01-T3, USPM-C01-T4_
- [ ] USPM-C01-T6 [ui-modernization] Build the screen Add user (S-USER-ADD)
  - To the prototype: ui-reference/index.html#/S-USER-ADD.
  - **lookup field** "User type": None chosen: 'User Type can NOT be empty...'
  - _Requirements: USPM-REQ-F-011_
  - _Rules: USPM-BR-011, USPM-BR-013, USPM-BR-014_
  - _After: USPM-C01-T2, USPM-C01-T3, USPM-C01-T4_
- [ ] USPM-C01-T7 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER)
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **summary card** "Signed in as"
  - **primary button** "Sign out"
  - _Requirements: USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012_
  - _Rules: USPM-BR-010, USPM-BR-011, USPM-BR-012, USPM-BR-013, USPM-BR-014, USPM-BR-015_
  - _After: USPM-C01-T2, USPM-C01-T3, USPM-C01-T4_
- [ ] USPM-C01-T8 [test-generation] Write a test for every acceptance criterion
  - 19 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-001, USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013, USPM-REQ-F-014_
  - _Criteria: USPM-C01-AC-01, USPM-C01-AC-02, USPM-C01-AC-03, USPM-C01-AC-04, USPM-C01-AC-05, USPM-C01-AC-06, USPM-C01-AC-07, USPM-C01-AC-08, USPM-C01-AC-09, USPM-C01-AC-10, USPM-C01-AC-11, USPM-C01-AC-12, USPM-C01-AC-13, USPM-C01-AC-14, USPM-C01-AC-15, USPM-C01-AC-16, USPM-C01-AC-17, USPM-C01-AC-18, USPM-C01-AC-19_
  - _After: USPM-C01-T1, USPM-C01-T2, USPM-C01-T3, USPM-C01-T4, USPM-C01-T5, USPM-C01-T6, USPM-C01-T7_
- [ ] USPM-C01-T9 [compliance] Review the handling of audit, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-001, USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013, USPM-REQ-F-014_
  - _After: USPM-C01-T1, USPM-C01-T2, USPM-C01-T3, USPM-C01-T4, USPM-C01-T5, USPM-C01-T6, USPM-C01-T7_

## USPM-C02 Browse the user list (draft)

- [ ] USPM-C02-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-019, USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031, USPM-REQ-F-032, USPM-REQ-F-033_
- [ ] USPM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-015, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-031_
  - _Rules: USPM-BR-018, USPM-BR-020, USPM-BR-021, USPM-BR-026, USPM-BR-027, USPM-BR-028, USPM-BR-029, USPM-BR-030, USPM-BR-032, USPM-BR-033, USPM-BR-035_
  - _After: USPM-C02-T1_
- [ ] USPM-C02-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-027, USPM-REQ-F-032, USPM-REQ-F-016, USPM-REQ-F-019, USPM-REQ-F-020_
  - _Rules: USPM-BR-019, USPM-BR-022, USPM-BR-023, USPM-BR-031, USPM-BR-036_
  - _After: USPM-C02-T1_
- [ ] USPM-C02-T4 [api] Build the services behind the screens
  - USPM-BR-024: Remember the User ID shown in the first row of the current page. Paging backward uses it as a cursor: fetch the up to ten users whose IDs sort before it, in descending key order, then show them in ascending order.
  - USPM-BR-025: Remember the User ID shown in the last row (row 10) of the current page. Paging forward uses it as a cursor: fetch the next up to ten users whose IDs sort after it.
  - USPM-BR-034: Any backward-page request sets the list's 'next page available' state to yes, even when it is refused at the top, so that a forward page is allowed afterwards. Keep this flag in the paging state.
  - USPM-BR-037: Keep the list's paging state (page number, first and last User ID shown, next-page flag) in the user's session or the request between interactions, so that the next action continues from the same page.
  - _Requirements: USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-030, USPM-REQ-F-033_
  - _Rules: USPM-BR-024, USPM-BR-025, USPM-BR-034, USPM-BR-037_
  - _After: USPM-C02-T1, USPM-C02-T2, USPM-C02-T3_
- [ ] USPM-C02-T5 [ui-modernization] Build the screen Users (S-USER-LIST)
  - To the prototype: ui-reference/index.html#/S-USER-LIST.
  - **lookup field** "Start from user ID": If the users cannot be read, 'Unable to lookup User...' shows above the table with a Try again link.
  - **data table** "Users": Previous is disabled on page 1 and Next on the last page. The disabled buttons say 'You are already at the top of the page...' and 'You are already at the bottom of the page...', and the last page says 'You have reached the bottom of the page...'. The actions are buttons on each row, so the 'Invalid selection. Valid values are U and D' error cannot happen. If the users cannot be read while paging: 'Unable to lookup User...'.
  - _Requirements: USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-019, USPM-REQ-F-020, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-032_
  - _Rules: USPM-BR-019, USPM-BR-020, USPM-BR-021, USPM-BR-022, USPM-BR-023, USPM-BR-026, USPM-BR-027, USPM-BR-028, USPM-BR-030, USPM-BR-031, USPM-BR-032, USPM-BR-033, USPM-BR-036_
  - _After: USPM-C02-T2, USPM-C02-T3, USPM-C02-T4_
- [ ] USPM-C02-T6 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER)
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **data table** "Navigation": Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home.
  - _Requirements: USPM-REQ-F-015_
  - _Rules: USPM-BR-018_
  - _After: USPM-C02-T2, USPM-C02-T3, USPM-C02-T4_
- [ ] USPM-C02-T7 [test-generation] Write a test for every acceptance criterion
  - 25 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-019, USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031, USPM-REQ-F-032, USPM-REQ-F-033_
  - _Criteria: USPM-C02-AC-01, USPM-C02-AC-02, USPM-C02-AC-03, USPM-C02-AC-04, USPM-C02-AC-05, USPM-C02-AC-06, USPM-C02-AC-07, USPM-C02-AC-08, USPM-C02-AC-09, USPM-C02-AC-10, USPM-C02-AC-11, USPM-C02-AC-12, USPM-C02-AC-13, USPM-C02-AC-14, USPM-C02-AC-15, USPM-C02-AC-16, USPM-C02-AC-17, USPM-C02-AC-18, USPM-C02-AC-19, USPM-C02-AC-20, USPM-C02-AC-21, USPM-C02-AC-22, USPM-C02-AC-23, USPM-C02-AC-24, USPM-C02-AC-25_
  - _After: USPM-C02-T1, USPM-C02-T2, USPM-C02-T3, USPM-C02-T4, USPM-C02-T5, USPM-C02-T6_
- [ ] USPM-C02-T8 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-019, USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031, USPM-REQ-F-032, USPM-REQ-F-033_
  - _After: USPM-C02-T1, USPM-C02-T2, USPM-C02-T3, USPM-C02-T4, USPM-C02-T5, USPM-C02-T6_

## USPM-C03 Select a user to update or delete (draft)

- [ ] USPM-C03-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
- [ ] USPM-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
  - _Rules: USPM-BR-038, USPM-BR-041, USPM-BR-042, USPM-BR-043_
  - _After: USPM-C03-T1_
- [ ] USPM-C03-T3 [api] Build the services behind the screens
  - USPM-BR-039: When the list is submitted with no row marked, clear any pending action and selected User ID held in the session, so that no stale selection opens an update or delete screen. Then just refresh the list.
  - USPM-BR-040: The pending selection (action code and User ID) must be reset to empty on every submit that has no marked row. It must not be carried over from an earlier interaction.
  - _Requirements: USPM-REQ-F-035_
  - _Rules: USPM-BR-039, USPM-BR-040_
  - _After: USPM-C03-T1, USPM-C03-T2_
- [ ] USPM-C03-T4 [ui-modernization] Build the screen Users (S-USER-LIST)
  - To the prototype: ui-reference/index.html#/S-USER-LIST.
  - **data table** "Users": Previous is disabled on page 1 and Next on the last page. The disabled buttons say 'You are already at the top of the page...' and 'You are already at the bottom of the page...', and the last page says 'You have reached the bottom of the page...'. The actions are buttons on each row, so the 'Invalid selection. Valid values are U and D' error cannot happen. If the users cannot be read while paging: 'Unable to lookup User...'.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
  - _Rules: USPM-BR-038, USPM-BR-041, USPM-BR-042, USPM-BR-043_
  - _After: USPM-C03-T2, USPM-C03-T3_
- [ ] USPM-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
  - _Criteria: USPM-C03-AC-01, USPM-C03-AC-02, USPM-C03-AC-03, USPM-C03-AC-04, USPM-C03-AC-05, USPM-C03-AC-06, USPM-C03-AC-07, USPM-C03-AC-08_
  - _After: USPM-C03-T1, USPM-C03-T2, USPM-C03-T3, USPM-C03-T4_
- [ ] USPM-C03-T6 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-034, USPM-REQ-F-035, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038_
  - _After: USPM-C03-T1, USPM-C03-T2, USPM-C03-T3, USPM-C03-T4_

## USPM-C04 Add a new user (draft)

- [ ] USPM-C04-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-F-046, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-049, USPM-REQ-F-050_
- [ ] USPM-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-050_
  - _Rules: USPM-BR-044, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-050, USPM-BR-052, USPM-BR-053, USPM-BR-054, USPM-BR-056_
  - _After: USPM-C04-T1_
- [ ] USPM-C04-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-049_
  - _Rules: USPM-BR-055_
  - _After: USPM-C04-T1_
- [ ] USPM-C04-T4 [api] Build the services behind the screens
  - USPM-BR-051: Map the five entered fields onto a new user record keyed by User ID and insert it into the user store as a create-only operation. The insert must fail with a distinct 'duplicate key' result when the User ID already exists, so the screen can tell 'already exists' apart from other failures.
  - _Requirements: USPM-REQ-F-046_
  - _Rules: USPM-BR-051_
  - _After: USPM-C04-T1, USPM-C04-T2, USPM-C04-T3_
- [ ] USPM-C04-T5 [ui-modernization] Build the screen Add user (S-USER-ADD)
  - To the prototype: ui-reference/index.html#/S-USER-ADD.
  - **lookup field** "First name": Blank: 'First Name can NOT be empty...'
  - **lookup field** "Last name": Blank: 'Last Name can NOT be empty...'
  - **lookup field** "User ID": Blank: 'User ID can NOT be empty...' Already used: 'User ID already exist...'; nothing is added and the existing user is not changed.
  - **lookup field** "Password": Blank: 'Password can NOT be empty...'
  - **lookup field** "User type": None chosen: 'User Type can NOT be empty...'
  - **primary button** "Add user": Checks First name, Last name, User ID, Password and User type in that order. Every blank field is listed in an error summary at the top, each linked to its field, and nothing is added until all are filled. Any other failure: 'Unable to Add User...', with focus on First name.
  - _Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-F-046, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-049, USPM-REQ-F-050_
  - _Rules: USPM-BR-044, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-050, USPM-BR-051, USPM-BR-052, USPM-BR-053, USPM-BR-054, USPM-BR-055, USPM-BR-056_
  - _After: USPM-C04-T2, USPM-C04-T3, USPM-C04-T4_
- [ ] USPM-C04-T6 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-F-046, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-049, USPM-REQ-F-050_
  - _Criteria: USPM-C04-AC-01, USPM-C04-AC-02, USPM-C04-AC-03, USPM-C04-AC-04, USPM-C04-AC-05, USPM-C04-AC-06, USPM-C04-AC-07, USPM-C04-AC-08, USPM-C04-AC-09, USPM-C04-AC-10, USPM-C04-AC-11, USPM-C04-AC-12, USPM-C04-AC-13_
  - _After: USPM-C04-T1, USPM-C04-T2, USPM-C04-T3, USPM-C04-T4, USPM-C04-T5_
- [ ] USPM-C04-T7 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-F-046, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-049, USPM-REQ-F-050_
  - _After: USPM-C04-T1, USPM-C04-T2, USPM-C04-T3, USPM-C04-T4, USPM-C04-T5_

## USPM-C05 Look up and update a user (draft)

- [ ] USPM-C05-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053_
- [ ] USPM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-051_
  - _Rules: USPM-BR-057, USPM-BR-058_
  - _After: USPM-C05-T1_
- [ ] USPM-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-053_
  - _Rules: USPM-BR-060_
  - _After: USPM-C05-T1_
- [ ] USPM-C05-T4 [api] Build the services behind the screens
  - USPM-BR-059: For a non-blank User ID, clear the detail fields, then fetch that user by its key from the user store. Read it so that a later save in the same flow can update that record safely, for example with optimistic concurrency (a version or the read values).
  - _Requirements: USPM-REQ-F-052_
  - _Rules: USPM-BR-059_
  - _After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3_
- [ ] USPM-C05-T5 [ui-modernization] Build the screen Update user (S-USER-EDIT)
  - To the prototype: ui-reference/index.html#/S-USER-EDIT.
  - **lookup field** "User ID": Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...', and the details stay blank. Read failure: 'Unable to lookup User...'.
  - **primary button** "Save changes": Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'.
  - _Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053_
  - _Rules: USPM-BR-057, USPM-BR-058, USPM-BR-059, USPM-BR-060_
  - _After: USPM-C05-T2, USPM-C05-T3, USPM-C05-T4_
- [ ] USPM-C05-T6 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053_
  - _Criteria: USPM-C05-AC-01, USPM-C05-AC-02, USPM-C05-AC-03, USPM-C05-AC-04_
  - _After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3, USPM-C05-T4, USPM-C05-T5_
- [ ] USPM-C05-T7 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053_
  - _After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3, USPM-C05-T4, USPM-C05-T5_

## USPM-C06 Open the User Update screen and look up a user (draft)

- [ ] USPM-C06-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063_
- [ ] USPM-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-057, USPM-REQ-F-059, USPM-REQ-F-062, USPM-REQ-F-063_
  - _Rules: USPM-BR-061, USPM-BR-062, USPM-BR-063, USPM-BR-065, USPM-BR-067, USPM-BR-070, USPM-BR-071_
  - _After: USPM-C06-T1_
- [ ] USPM-C06-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-060, USPM-REQ-F-056, USPM-REQ-F-058, USPM-REQ-F-061_
  - _Rules: USPM-BR-064, USPM-BR-066, USPM-BR-068, USPM-BR-069_
  - _After: USPM-C06-T1_
- [ ] USPM-C06-T4 [ui-modernization] Build the screen Update user (S-USER-EDIT)
  - To the prototype: ui-reference/index.html#/S-USER-EDIT.
  - **lookup field** "User ID": Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...', and the details stay blank. Read failure: 'Unable to lookup User...'.
  - **primary button** "Save changes": Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'.
  - _Requirements: USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063_
  - _Rules: USPM-BR-062, USPM-BR-063, USPM-BR-064, USPM-BR-065, USPM-BR-066, USPM-BR-067, USPM-BR-068, USPM-BR-069, USPM-BR-070, USPM-BR-071_
  - _After: USPM-C06-T2, USPM-C06-T3_
- [ ] USPM-C06-T5 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER)
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **data table** "Navigation": Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home.
  - _Requirements: USPM-REQ-F-054_
  - _Rules: USPM-BR-061_
  - _After: USPM-C06-T2, USPM-C06-T3_
- [ ] USPM-C06-T6 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063_
  - _Criteria: USPM-C06-AC-01, USPM-C06-AC-02, USPM-C06-AC-03, USPM-C06-AC-04, USPM-C06-AC-05, USPM-C06-AC-06, USPM-C06-AC-07, USPM-C06-AC-08, USPM-C06-AC-09, USPM-C06-AC-10_
  - _After: USPM-C06-T1, USPM-C06-T2, USPM-C06-T3, USPM-C06-T4, USPM-C06-T5_
- [ ] USPM-C06-T7 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063_
  - _After: USPM-C06-T1, USPM-C06-T2, USPM-C06-T3, USPM-C06-T4, USPM-C06-T5_

## USPM-C07 Save changes to a user profile (draft)

- [ ] USPM-C07-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075_
- [ ] USPM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-073, USPM-REQ-F-074_
  - _Rules: USPM-BR-072, USPM-BR-073, USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-079, USPM-BR-081, USPM-BR-082_
  - _After: USPM-C07-T1_
- [ ] USPM-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-072, USPM-REQ-F-075_
  - _Rules: USPM-BR-080, USPM-BR-083_
  - _After: USPM-C07-T1_
- [ ] USPM-C07-T4 [ui-modernization] Build the screen Update user (S-USER-EDIT)
  - To the prototype: ui-reference/index.html#/S-USER-EDIT.
  - **lookup field** "First name": Blank: 'First Name can NOT be empty...'
  - **lookup field** "Last name": Blank: 'Last Name can NOT be empty...'
  - **lookup field** "Password": Cleared without a new password: 'Password can NOT be empty...'
  - **lookup field** "User type": None chosen: 'User Type can NOT be empty...'
  - **primary button** "Save changes": Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'.
  - _Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075_
  - _Rules: USPM-BR-072, USPM-BR-073, USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-079, USPM-BR-080, USPM-BR-081, USPM-BR-082, USPM-BR-083_
  - _After: USPM-C07-T2, USPM-C07-T3_
- [ ] USPM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075_
  - _Criteria: USPM-C07-AC-01, USPM-C07-AC-02, USPM-C07-AC-03, USPM-C07-AC-04, USPM-C07-AC-05, USPM-C07-AC-06, USPM-C07-AC-07, USPM-C07-AC-08, USPM-C07-AC-09, USPM-C07-AC-10, USPM-C07-AC-11, USPM-C07-AC-12, USPM-C07-AC-13_
  - _After: USPM-C07-T1, USPM-C07-T2, USPM-C07-T3, USPM-C07-T4_
- [ ] USPM-C07-T6 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075_
  - _After: USPM-C07-T1, USPM-C07-T2, USPM-C07-T3, USPM-C07-T4_

## USPM-C08 Delete a user (draft)

- [ ] USPM-C08-T1 [data] Model the data the capability reads and writes
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089, USPM-REQ-F-090_
- [ ] USPM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086_
  - _Rules: USPM-BR-084, USPM-BR-085, USPM-BR-089, USPM-BR-090, USPM-BR-092, USPM-BR-093, USPM-BR-094_
  - _After: USPM-C08-T1_
- [ ] USPM-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-083, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-089, USPM-REQ-F-090_
  - _Rules: USPM-BR-086, USPM-BR-087, USPM-BR-088, USPM-BR-091, USPM-BR-095, USPM-BR-096, USPM-BR-097, USPM-BR-098_
  - _After: USPM-C08-T1_
- [ ] USPM-C08-T4 [ui-modernization] Build the screen Delete user (S-USER-DELETE)
  - To the prototype: ui-reference/index.html#/S-USER-DELETE.
  - **lookup field** "User ID": Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...' Read failure: 'Unable to lookup User...'.
  - **summary card** "User to delete"
  - **primary button** "Delete user": No user found: 'User ID can NOT be empty...' or 'User ID NOT found...', and nothing is deleted or attempted. Delete failure: 'Unable to Update User...'.
  - _Requirements: USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089, USPM-REQ-F-090_
  - _Rules: USPM-BR-086, USPM-BR-087, USPM-BR-088, USPM-BR-089, USPM-BR-090, USPM-BR-091, USPM-BR-092, USPM-BR-093, USPM-BR-094, USPM-BR-095, USPM-BR-096, USPM-BR-097, USPM-BR-098_
  - _After: USPM-C08-T2, USPM-C08-T3_
- [ ] USPM-C08-T5 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER)
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **data table** "Navigation": Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077_
  - _Rules: USPM-BR-084, USPM-BR-085_
  - _After: USPM-C08-T2, USPM-C08-T3_
- [ ] USPM-C08-T6 [test-generation] Write a test for every acceptance criterion
  - 16 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089, USPM-REQ-F-090_
  - _Criteria: USPM-C08-AC-01, USPM-C08-AC-02, USPM-C08-AC-03, USPM-C08-AC-04, USPM-C08-AC-05, USPM-C08-AC-06, USPM-C08-AC-07, USPM-C08-AC-08, USPM-C08-AC-09, USPM-C08-AC-10, USPM-C08-AC-11, USPM-C08-AC-12, USPM-C08-AC-13, USPM-C08-AC-14, USPM-C08-AC-15, USPM-C08-AC-16_
  - _After: USPM-C08-T1, USPM-C08-T2, USPM-C08-T3, USPM-C08-T4, USPM-C08-T5_
- [ ] USPM-C08-T7 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-076, USPM-REQ-F-077, USPM-REQ-F-078, USPM-REQ-F-079, USPM-REQ-F-080, USPM-REQ-F-081, USPM-REQ-F-082, USPM-REQ-F-083, USPM-REQ-F-084, USPM-REQ-F-085, USPM-REQ-F-086, USPM-REQ-F-087, USPM-REQ-F-088, USPM-REQ-F-089, USPM-REQ-F-090_
  - _After: USPM-C08-T1, USPM-C08-T2, USPM-C08-T3, USPM-C08-T4, USPM-C08-T5_

## USPM-C09 Seed and load the user security file (draft)

- [ ] USPM-C09-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-091, USPM-REQ-F-094_
  - _Rules: USPM-BR-099, USPM-BR-102_
- [ ] USPM-C09-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-095, USPM-REQ-F-096_
  - _Rules: USPM-BR-103_
- [ ] USPM-C09-T3 [api] Build the scheduled job
  - USPM-BR-100: The seed step must be repeatable. Remove any previous staged seed set first, keep the new one only if staging finishes successfully, and discard it if staging fails. A transactional load or a temporary table swapped in on success meets this.
  - USPM-BR-101: Recreate the user store from scratch, with the user ID (8 characters) as its unique primary key, then bulk-insert every staged seed record into it. This is a full reset, not a merge.
  - USPM-BR-104: The legacy job also copies the staged records, in arrival order, into an entry-sequenced copy of the user security file, whatever happened in earlier steps. The new application needs this only if something reads users in insertion order. Otherwise one keyed user store is enough. Confirm with the owner before building a second copy.
  - USPM-BR-105: The legacy job also copies the staged records into a relative-record (slot-numbered) copy of the user security file, whatever happened in earlier steps. The new application needs this only if a consumer looks users up by record number. Otherwise the keyed user store covers it. Confirm with the owner before building it.
  - _Requirements: USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-097, USPM-REQ-F-098_
  - _Rules: USPM-BR-100, USPM-BR-101, USPM-BR-104, USPM-BR-105_
  - _After: USPM-C09-T1, USPM-C09-T2_
- [ ] USPM-C09-T4 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-091, USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-094, USPM-REQ-F-095, USPM-REQ-F-096, USPM-REQ-F-097, USPM-REQ-F-098_
  - _Criteria: USPM-C09-AC-01, USPM-C09-AC-02, USPM-C09-AC-03, USPM-C09-AC-04, USPM-C09-AC-05, USPM-C09-AC-06, USPM-C09-AC-07, USPM-C09-AC-08, USPM-C09-AC-09_
  - _After: USPM-C09-T1, USPM-C09-T2, USPM-C09-T3_
- [ ] USPM-C09-T5 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-091, USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-094, USPM-REQ-F-095, USPM-REQ-F-096, USPM-REQ-F-097, USPM-REQ-F-098_
  - _After: USPM-C09-T1, USPM-C09-T2, USPM-C09-T3_
