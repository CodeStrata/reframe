# Tasks: Transaction list access and session handling (OATM-C27)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C27-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010.
  - File records: CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] OATM-C27-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225. Rules: OATM-BR-234, OATM-BR-235, OATM-BR-236, OATM-BR-237. After: OATM-C27-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C27-T3 [api] Build the services behind the screens. Requirements: OATM-REQ-N-010. Rules: OATM-BR-238. After: OATM-C27-T1, OATM-C27-T2.
  - OATM-BR-238: The list is a stateful interaction. Between requests the application must keep the user's session state: signed-on user, current page number, first and last transaction IDs of the page, next-page flag and any selection. This can be a server-side session keyed by an authenticated session token, or signed state round-tripped with the client. Each response then waits for the user's next action.
- [ ] OATM-C27-T4 [ui-modernization] Build the screen Transactions (S-TRANSACTION-LIST). Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225. Rules: OATM-BR-234, OATM-BR-235, OATM-BR-236, OATM-BR-237. After: OATM-C27-T2, OATM-C27-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-LIST.
  - table "Transactions": Previous on the first page: 'You are already at the top of the page...'; Next on the last page: 'You are already at the bottom of the page...'.
  - message "List error"
  - link "Back"
- [ ] OATM-C27-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: OATM-REQ-N-008. Rules: OATM-BR-234. After: OATM-C27-T2, OATM-C27-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - header "CardDemo"
- [ ] OATM-C27-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010. Criteria: OATM-C27-AC-01, OATM-C27-AC-02, OATM-C27-AC-03, OATM-C27-AC-04, OATM-C27-AC-05. After: OATM-C27-T1, OATM-C27-T2, OATM-C27-T3, OATM-C27-T4, OATM-C27-T5.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] OATM-C27-T7 [compliance] Review the handling of card data, security. Requirements: OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-F-224, OATM-REQ-F-225, OATM-REQ-N-010. After: OATM-C27-T1, OATM-C27-T2, OATM-C27-T3, OATM-C27-T4, OATM-C27-T5.
  - Check storage, logs, screens and audit against the rules.
