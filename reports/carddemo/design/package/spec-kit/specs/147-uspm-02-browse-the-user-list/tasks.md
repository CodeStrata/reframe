# Tasks: Browse the user list (USPM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] USPM-C02-T1 [data] Model the data the capability reads and writes. Requirements: USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-019, USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031, USPM-REQ-F-032, USPM-REQ-F-033.
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] USPM-C02-T2 [business-rules] Implement the business rules. Requirements: USPM-REQ-F-015, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-031. Rules: USPM-BR-018, USPM-BR-020, USPM-BR-021, USPM-BR-026, USPM-BR-027, USPM-BR-028, USPM-BR-029, USPM-BR-030, USPM-BR-032, USPM-BR-033, USPM-BR-035. After: USPM-C02-T1.
  - Keep each business rule exactly as specified.
- [ ] USPM-C02-T3 [business-rules] Implement error handling and messages. Requirements: USPM-REQ-F-027, USPM-REQ-F-032, USPM-REQ-F-016, USPM-REQ-F-019, USPM-REQ-F-020. Rules: USPM-BR-019, USPM-BR-022, USPM-BR-023, USPM-BR-031, USPM-BR-036. After: USPM-C02-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] USPM-C02-T4 [api] Build the services behind the screens. Requirements: USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-030, USPM-REQ-F-033. Rules: USPM-BR-024, USPM-BR-025, USPM-BR-034, USPM-BR-037. After: USPM-C02-T1, USPM-C02-T2, USPM-C02-T3.
  - USPM-BR-024: Keep the User ID of the first row on the current page as the backward paging cursor. 'Previous page' reads the users whose keys come before this ID, in descending key order.
  - USPM-BR-025: Keep the User ID of the tenth row on the current page as the forward paging cursor. 'Next page' reads users with keys after this ID, in ascending order (keyset pagination on User ID).
  - USPM-BR-034: Set the 'next page available' flag to true every time the user pages backward, including when the request is refused at the top of the list, so that 'Next page' is always allowed after a 'Previous page' request.
  - USPM-BR-037: Keep the list's paging state between requests: page number, first and last User ID shown, and the next-page flag. Store it in the session or as a cursor token passed with each request, so the next action continues from the same position.
- [ ] USPM-C02-T5 [ui-modernization] Build the screen Users (S-USER-LIST). Requirements: USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-019, USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031, USPM-REQ-F-032, USPM-REQ-F-033. Rules: USPM-BR-018, USPM-BR-019, USPM-BR-020, USPM-BR-021, USPM-BR-022, USPM-BR-023, USPM-BR-024, USPM-BR-025, USPM-BR-026, USPM-BR-027, USPM-BR-028, USPM-BR-029, USPM-BR-030, USPM-BR-031, USPM-BR-032, USPM-BR-033, USPM-BR-034, USPM-BR-035, USPM-BR-036, USPM-BR-037. After: USPM-C02-T2, USPM-C02-T3, USPM-C02-T4.
  - To the prototype: ui-reference/index.html#/S-USER-LIST.
  - page "Users"
  - search "Search by User ID"
  - table "Users": On the first page: 'You are already at the top of the page...'; on the last page: 'You are already at the bottom of the page...'
  - message "List messages": An unsupported action shows 'Invalid key pressed. Please see below...'
- [ ] USPM-C02-T6 [test-generation] Write a test for every acceptance criterion. Requirements: USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-019, USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031, USPM-REQ-F-032, USPM-REQ-F-033. Criteria: USPM-C02-AC-01, USPM-C02-AC-02, USPM-C02-AC-03, USPM-C02-AC-04, USPM-C02-AC-05, USPM-C02-AC-06, USPM-C02-AC-07, USPM-C02-AC-08, USPM-C02-AC-09, USPM-C02-AC-10, USPM-C02-AC-11, USPM-C02-AC-12, USPM-C02-AC-13, USPM-C02-AC-14, USPM-C02-AC-15, USPM-C02-AC-16, USPM-C02-AC-17, USPM-C02-AC-18, USPM-C02-AC-19, USPM-C02-AC-20, USPM-C02-AC-21, USPM-C02-AC-22, USPM-C02-AC-23, USPM-C02-AC-24, USPM-C02-AC-25. After: USPM-C02-T1, USPM-C02-T2, USPM-C02-T3, USPM-C02-T4, USPM-C02-T5.
  - 25 acceptance criteria, each a test named by its ID.
- [ ] USPM-C02-T7 [compliance] Review the handling of personal data, security. Requirements: USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-019, USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031, USPM-REQ-F-032, USPM-REQ-F-033. After: USPM-C02-T1, USPM-C02-T2, USPM-C02-T3, USPM-C02-T4, USPM-C02-T5.
  - Check storage, logs, screens and audit against the rules.
