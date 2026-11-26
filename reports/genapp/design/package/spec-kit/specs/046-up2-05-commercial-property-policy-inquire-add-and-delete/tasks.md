# Tasks: Commercial property policy inquire, add and delete (UP2-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP2-C05-T1 [data] Model the data the capability reads and writes. Requirements: UP2-REQ-F-054, UP2-REQ-F-055, UP2-REQ-F-056, UP2-REQ-F-057, UP2-REQ-F-058, UP2-REQ-F-059, UP2-REQ-F-060, UP2-REQ-F-061, UP2-REQ-F-062, UP2-REQ-F-063, UP2-REQ-F-064, UP2-REQ-F-065, UP2-REQ-F-066, UP2-REQ-F-067, UP2-REQ-N-001, UP2-REQ-F-068, UP2-REQ-F-069.
  - Working records it passes or builds: LGCMAREA.
- [ ] UP2-C05-T2 [business-rules] Implement the business rules. Requirements: UP2-REQ-F-055, UP2-REQ-F-056, UP2-REQ-F-057, UP2-REQ-F-058, UP2-REQ-F-059, UP2-REQ-F-062, UP2-REQ-F-065. Rules: UP2-BR-046, UP2-BR-047, UP2-BR-048, UP2-BR-049, UP2-BR-052, UP2-BR-055. After: UP2-C05-T1.
  - Keep each business rule exactly as specified.
- [ ] UP2-C05-T3 [business-rules] Implement error handling and messages. Requirements: UP2-REQ-F-061, UP2-REQ-F-064, UP2-REQ-F-067, UP2-REQ-F-054, UP2-REQ-F-060, UP2-REQ-F-063, UP2-REQ-F-066, UP2-REQ-F-068, UP2-REQ-F-069. Rules: UP2-BR-045, UP2-BR-050, UP2-BR-051, UP2-BR-053, UP2-BR-054, UP2-BR-056, UP2-BR-057, UP2-BR-059. After: UP2-C05-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP2-C05-T4 [api] Build the services and the scheduled job. Requirements: UP2-REQ-N-001. Rules: UP2-BR-058. After: UP2-C05-T1, UP2-C05-T2, UP2-C05-T3.
  - UP2-BR-058: After each option has been processed, the commercial policy screen stays open with its current values, so the user's next submission is handled by the same commercial policy screen and starts the next action. This is ordinary screen navigation in the new application: it needs no transaction code, only a way to keep the user on the commercial policy page between actions until they leave it (PF3 / exit) or clear it.
- [ ] UP2-C05-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: UP2-REQ-F-068. Rules: UP2-BR-059. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - button "Sign out"
- [ ] UP2-C05-T6 [ui-modernization] Build the screen New customer (S-CUSTOMER-NEW). Requirements: UP2-REQ-F-055. Rules: UP2-BR-046. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-CUSTOMER-NEW.
  - message "Action not available": Only the actions shown as buttons here (Add customer, Clear form) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C05-T7 [ui-modernization] Build the screen Customer details (S-CUSTOMER-EDIT). Requirements: UP2-REQ-F-055. Rules: UP2-BR-046. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-CUSTOMER-EDIT.
  - message "Action not available": Only the actions shown as buttons here (Find, Save changes, Discard changes) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C05-T8 [ui-modernization] Build the screen Find policies (S-POLICY-FIND). Requirements: UP2-REQ-F-055, UP2-REQ-F-056, UP2-REQ-F-057, UP2-REQ-F-058, UP2-REQ-F-059, UP2-REQ-F-060, UP2-REQ-F-061, UP2-REQ-F-062, UP2-REQ-F-069. Rules: UP2-BR-046, UP2-BR-047, UP2-BR-048, UP2-BR-049, UP2-BR-050, UP2-BR-051, UP2-BR-052, UP2-BR-059. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-POLICY-FIND.
  - text "Postcode": Postcode can be at most 8 characters
  - button "Search"
  - table "Policies found"
  - message "Nothing found"
  - button "New commercial policy"
  - button "Clear search"
  - message "Action not available": Only the actions shown as buttons here (Search, Open, New policy, Clear search) can run. Motor and life policies offer inquire, add, delete and update; house policies offer add, update and delete; commercial policies offer inquire, add and delete. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown.
- [ ] UP2-C05-T9 [ui-modernization] Build the screen Motor policy (S-MOTOR-POLICY). Requirements: UP2-REQ-F-055. Rules: UP2-BR-046. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-MOTOR-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C05-T10 [ui-modernization] Build the screen Life (endowment) policy (S-LIFE-POLICY). Requirements: UP2-REQ-F-055. Rules: UP2-BR-046. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-LIFE-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C05-T11 [ui-modernization] Build the screen House policy (S-HOUSE-POLICY). Requirements: UP2-REQ-F-055. Rules: UP2-BR-046. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-HOUSE-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C05-T12 [ui-modernization] Build the screen Commercial property policy (S-COMMERCIAL-POLICY). Requirements: UP2-REQ-F-054, UP2-REQ-F-055, UP2-REQ-F-060, UP2-REQ-F-062, UP2-REQ-F-063, UP2-REQ-F-064, UP2-REQ-F-065, UP2-REQ-F-066, UP2-REQ-F-067, UP2-REQ-N-001. Rules: UP2-BR-045, UP2-BR-046, UP2-BR-050, UP2-BR-052, UP2-BR-053, UP2-BR-054, UP2-BR-055, UP2-BR-056, UP2-BR-057, UP2-BR-058. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-COMMERCIAL-POLICY.
  - form "Commercial policy"
  - display "Policy number"
  - button "Add commercial policy"
  - button "Delete commercial policy"
  - dialog "Delete this policy?"
  - message "Result"
  - message "Action not available": Only the actions shown as buttons here (Add, Delete) can run, plus finding a policy on S-POLICY-FIND; commercial policies cannot be updated. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C05-T13 [ui-modernization] Build the screen Claim (S-CLAIM-VIEW). Requirements: UP2-REQ-F-055. Rules: UP2-BR-046. After: UP2-C05-T2, UP2-C05-T3, UP2-C05-T4.
  - To the prototype: ui-reference/index.html#/S-CLAIM-VIEW.
  - message "Action not available": Only Find can run here. Any other request calls no back-end service and shows 'Please enter a valid option': use the Find button.
- [ ] UP2-C05-T14 [test-generation] Write a test for every acceptance criterion. Requirements: UP2-REQ-F-054, UP2-REQ-F-055, UP2-REQ-F-056, UP2-REQ-F-057, UP2-REQ-F-058, UP2-REQ-F-059, UP2-REQ-F-060, UP2-REQ-F-061, UP2-REQ-F-062, UP2-REQ-F-063, UP2-REQ-F-064, UP2-REQ-F-065, UP2-REQ-F-066, UP2-REQ-F-067, UP2-REQ-N-001, UP2-REQ-F-068, UP2-REQ-F-069. Criteria: UP2-C05-AC-01, UP2-C05-AC-02, UP2-C05-AC-03, UP2-C05-AC-04, UP2-C05-AC-05, UP2-C05-AC-06, UP2-C05-AC-07, UP2-C05-AC-08, UP2-C05-AC-09, UP2-C05-AC-10, UP2-C05-AC-11, UP2-C05-AC-12, UP2-C05-AC-13, UP2-C05-AC-14, UP2-C05-AC-15, UP2-C05-AC-16, UP2-C05-AC-17, UP2-C05-AC-18, UP2-C05-AC-19. After: UP2-C05-T1, UP2-C05-T2, UP2-C05-T3, UP2-C05-T4, UP2-C05-T5, UP2-C05-T6, UP2-C05-T7, UP2-C05-T8, UP2-C05-T9, UP2-C05-T10, UP2-C05-T11, UP2-C05-T12, UP2-C05-T13.
  - 19 acceptance criteria, each a test named by its ID.
- [ ] UP2-C05-T15 [compliance] Review the handling of money, personal data. Requirements: UP2-REQ-F-054, UP2-REQ-F-055, UP2-REQ-F-056, UP2-REQ-F-057, UP2-REQ-F-058, UP2-REQ-F-059, UP2-REQ-F-060, UP2-REQ-F-061, UP2-REQ-F-062, UP2-REQ-F-063, UP2-REQ-F-064, UP2-REQ-F-065, UP2-REQ-F-066, UP2-REQ-F-067, UP2-REQ-N-001, UP2-REQ-F-068, UP2-REQ-F-069. After: UP2-C05-T1, UP2-C05-T2, UP2-C05-T3, UP2-C05-T4, UP2-C05-T5, UP2-C05-T6, UP2-C05-T7, UP2-C05-T8, UP2-C05-T9, UP2-C05-T10, UP2-C05-T11, UP2-C05-T12, UP2-C05-T13.
  - Check storage, logs, screens and audit against the rules.
