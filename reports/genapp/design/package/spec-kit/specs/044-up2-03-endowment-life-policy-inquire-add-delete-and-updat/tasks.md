# Tasks: Endowment (life) policy inquire, add, delete and update (UP2-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP2-C03-T1 [data] Model the data the capability reads and writes. Requirements: UP2-REQ-F-029, UP2-REQ-F-030, UP2-REQ-F-031, UP2-REQ-F-032, UP2-REQ-F-033, UP2-REQ-F-034, UP2-REQ-F-035, UP2-REQ-F-036, UP2-REQ-F-037, UP2-REQ-F-038, UP2-REQ-F-039, UP2-REQ-F-040, UP2-REQ-F-041, UP2-REQ-F-042, UP2-REQ-F-043, UP2-REQ-F-044.
  - Working records it passes or builds: LGCMAREA.
- [ ] UP2-C03-T2 [business-rules] Implement the business rules. Requirements: UP2-REQ-F-029, UP2-REQ-F-030, UP2-REQ-F-033, UP2-REQ-F-035, UP2-REQ-F-040. Rules: UP2-BR-023, UP2-BR-024, UP2-BR-026, UP2-BR-028, UP2-BR-029, UP2-BR-034. After: UP2-C03-T1.
  - Keep each business rule exactly as specified.
- [ ] UP2-C03-T3 [business-rules] Implement error handling and messages. Requirements: UP2-REQ-F-034, UP2-REQ-F-037, UP2-REQ-F-038, UP2-REQ-F-041, UP2-REQ-F-043, UP2-REQ-F-044, UP2-REQ-F-031, UP2-REQ-F-032, UP2-REQ-F-036, UP2-REQ-F-039, UP2-REQ-F-042. Rules: UP2-BR-025, UP2-BR-027, UP2-BR-030, UP2-BR-031, UP2-BR-032, UP2-BR-033, UP2-BR-035, UP2-BR-036, UP2-BR-037. After: UP2-C03-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP2-C03-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: UP2-REQ-F-029, UP2-REQ-F-031. Rules: UP2-BR-023, UP2-BR-025. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - link "Policies"
  - button "Sign out"
- [ ] UP2-C03-T5 [ui-modernization] Build the screen New customer (S-CUSTOMER-NEW). Requirements: UP2-REQ-F-030. Rules: UP2-BR-024. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-CUSTOMER-NEW.
  - message "Action not available": Only the actions shown as buttons here (Add customer, Clear form) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C03-T6 [ui-modernization] Build the screen Customer details (S-CUSTOMER-EDIT). Requirements: UP2-REQ-F-030. Rules: UP2-BR-024. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-CUSTOMER-EDIT.
  - message "Action not available": Only the actions shown as buttons here (Find, Save changes, Discard changes) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C03-T7 [ui-modernization] Build the screen Find policies (S-POLICY-FIND). Requirements: UP2-REQ-F-030, UP2-REQ-F-032, UP2-REQ-F-033, UP2-REQ-F-034, UP2-REQ-F-035. Rules: UP2-BR-024, UP2-BR-025, UP2-BR-026, UP2-BR-027, UP2-BR-028, UP2-BR-029. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-POLICY-FIND.
  - button "Search"
  - message "Nothing found"
  - button "New life policy"
  - button "Clear search"
  - message "Action not available": Only the actions shown as buttons here (Search, Open, New policy, Clear search) can run. Motor and life policies offer inquire, add, delete and update; house policies offer add, update and delete; commercial policies offer inquire, add and delete. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown.
- [ ] UP2-C03-T8 [ui-modernization] Build the screen Motor policy (S-MOTOR-POLICY). Requirements: UP2-REQ-F-030. Rules: UP2-BR-024. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-MOTOR-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C03-T9 [ui-modernization] Build the screen Life (endowment) policy (S-LIFE-POLICY). Requirements: UP2-REQ-F-029, UP2-REQ-F-030, UP2-REQ-F-035, UP2-REQ-F-036, UP2-REQ-F-037, UP2-REQ-F-038, UP2-REQ-F-039, UP2-REQ-F-040, UP2-REQ-F-041, UP2-REQ-F-042, UP2-REQ-F-043, UP2-REQ-F-044. Rules: UP2-BR-023, UP2-BR-024, UP2-BR-028, UP2-BR-029, UP2-BR-030, UP2-BR-031, UP2-BR-032, UP2-BR-033, UP2-BR-034, UP2-BR-035, UP2-BR-036, UP2-BR-037. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-LIFE-POLICY.
  - button "Add life policy"
  - button "Save changes"
  - button "Delete life policy"
  - dialog "Delete this policy?"
  - message "Result"
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C03-T10 [ui-modernization] Build the screen House policy (S-HOUSE-POLICY). Requirements: UP2-REQ-F-030, UP2-REQ-F-035, UP2-REQ-F-040. Rules: UP2-BR-024, UP2-BR-028, UP2-BR-029, UP2-BR-034. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-HOUSE-POLICY.
  - button "Add house policy"
  - button "Save changes"
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C03-T11 [ui-modernization] Build the screen Commercial property policy (S-COMMERCIAL-POLICY). Requirements: UP2-REQ-F-030. Rules: UP2-BR-024. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-COMMERCIAL-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Delete) can run, plus finding a policy on S-POLICY-FIND; commercial policies cannot be updated. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C03-T12 [ui-modernization] Build the screen Claim (S-CLAIM-VIEW). Requirements: UP2-REQ-F-030. Rules: UP2-BR-024. After: UP2-C03-T2, UP2-C03-T3.
  - To the prototype: ui-reference/index.html#/S-CLAIM-VIEW.
  - message "Action not available": Only Find can run here. Any other request calls no back-end service and shows 'Please enter a valid option': use the Find button.
- [ ] UP2-C03-T13 [test-generation] Write a test for every acceptance criterion. Requirements: UP2-REQ-F-029, UP2-REQ-F-030, UP2-REQ-F-031, UP2-REQ-F-032, UP2-REQ-F-033, UP2-REQ-F-034, UP2-REQ-F-035, UP2-REQ-F-036, UP2-REQ-F-037, UP2-REQ-F-038, UP2-REQ-F-039, UP2-REQ-F-040, UP2-REQ-F-041, UP2-REQ-F-042, UP2-REQ-F-043, UP2-REQ-F-044. Criteria: UP2-C03-AC-01, UP2-C03-AC-02, UP2-C03-AC-03, UP2-C03-AC-04, UP2-C03-AC-05, UP2-C03-AC-06, UP2-C03-AC-07, UP2-C03-AC-08, UP2-C03-AC-09, UP2-C03-AC-10, UP2-C03-AC-11, UP2-C03-AC-12, UP2-C03-AC-13, UP2-C03-AC-14, UP2-C03-AC-15, UP2-C03-AC-16, UP2-C03-AC-17, UP2-C03-AC-18, UP2-C03-AC-19, UP2-C03-AC-20, UP2-C03-AC-21. After: UP2-C03-T1, UP2-C03-T2, UP2-C03-T3, UP2-C03-T4, UP2-C03-T5, UP2-C03-T6, UP2-C03-T7, UP2-C03-T8, UP2-C03-T9, UP2-C03-T10, UP2-C03-T11, UP2-C03-T12.
  - 21 acceptance criteria, each a test named by its ID.
- [ ] UP2-C03-T14 [compliance] Review the handling of money. Requirements: UP2-REQ-F-029, UP2-REQ-F-030, UP2-REQ-F-031, UP2-REQ-F-032, UP2-REQ-F-033, UP2-REQ-F-034, UP2-REQ-F-035, UP2-REQ-F-036, UP2-REQ-F-037, UP2-REQ-F-038, UP2-REQ-F-039, UP2-REQ-F-040, UP2-REQ-F-041, UP2-REQ-F-042, UP2-REQ-F-043, UP2-REQ-F-044. After: UP2-C03-T1, UP2-C03-T2, UP2-C03-T3, UP2-C03-T4, UP2-C03-T5, UP2-C03-T6, UP2-C03-T7, UP2-C03-T8, UP2-C03-T9, UP2-C03-T10, UP2-C03-T11, UP2-C03-T12.
  - Check storage, logs, screens and audit against the rules.
