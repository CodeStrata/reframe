# Tasks: List card master records (UP-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C02-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-003, UP-REQ-F-004, UP-REQ-F-005, UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009.
  - File records: CVACT02Y, CVACT03Y (see data-contracts.md).
- [ ] UP-C02-T2 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009, UP-REQ-F-004. Rules: UP-BR-004, UP-BR-005, UP-BR-009, UP-BR-010, UP-BR-011. After: UP-C02-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C02-T3 [api] Build the scheduled job. Requirements: UP-REQ-F-003, UP-REQ-F-005, UP-REQ-F-006. Rules: UP-BR-003, UP-BR-006, UP-BR-007, UP-BR-008. After: UP-C02-T1, UP-C02-T2.
  - UP-BR-003: A scheduled or on-demand report job that reads the card store through a read-only connection, so it can run while online users are working. Its progress messages and the listing go to the job's log or report output.
  - UP-BR-006: Each successful fetch of the next card in the ordered read is written to the report. The new application needs a sequential read of all cards, ordered by card number.
  - UP-BR-007: When the cursor or stream runs out of cards, the job ends normally. End of data is the normal way to finish, not an error.
  - UP-BR-008: Iterate until there are no more rows and write nothing for the empty fetch, so no blank or repeated line appears after the last card.
- [ ] UP-C02-T4 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-003, UP-REQ-F-004, UP-REQ-F-005, UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009. Criteria: UP-C02-AC-01, UP-C02-AC-02, UP-C02-AC-03, UP-C02-AC-04, UP-C02-AC-05, UP-C02-AC-06, UP-C02-AC-07, UP-C02-AC-08, UP-C02-AC-09, UP-C02-AC-10. After: UP-C02-T1, UP-C02-T2, UP-C02-T3.
  - 10 acceptance criteria, each a test named by its ID.
- [ ] UP-C02-T5 [compliance] Review the handling of card data. Requirements: UP-REQ-F-003, UP-REQ-F-004, UP-REQ-F-005, UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009. After: UP-C02-T1, UP-C02-T2, UP-C02-T3.
  - Check storage, logs, screens and audit against the rules.
