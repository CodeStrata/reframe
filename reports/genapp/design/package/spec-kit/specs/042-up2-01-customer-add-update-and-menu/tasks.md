# Tasks: Customer add, update and menu (UP2-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP2-C01-T1 [data] Model the data the capability reads and writes. Requirements: UP2-REQ-F-001, UP2-REQ-F-002, UP2-REQ-F-003, UP2-REQ-F-004, UP2-REQ-F-005, UP2-REQ-F-006, UP2-REQ-F-007, UP2-REQ-F-008, UP2-REQ-F-009, UP2-REQ-F-010, UP2-REQ-F-011, UP2-REQ-F-012, UP2-REQ-F-013.
  - Working records it passes or builds: LGCMAREA.
- [ ] UP2-C01-T2 [business-rules] Implement the business rules. Requirements: UP2-REQ-F-001, UP2-REQ-F-006, UP2-REQ-F-007, UP2-REQ-F-008, UP2-REQ-F-011, UP2-REQ-F-003, UP2-REQ-F-004. Rules: UP2-BR-001, UP2-BR-003, UP2-BR-004, UP2-BR-006, UP2-BR-007, UP2-BR-009. After: UP2-C01-T1.
  - Keep each business rule exactly as specified.
- [ ] UP2-C01-T3 [business-rules] Implement error handling and messages. Requirements: UP2-REQ-F-005, UP2-REQ-F-009, UP2-REQ-F-010, UP2-REQ-F-002, UP2-REQ-F-012, UP2-REQ-F-013. Rules: UP2-BR-002, UP2-BR-005, UP2-BR-008, UP2-BR-010. After: UP2-C01-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP2-C01-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: UP2-REQ-F-001, UP2-REQ-F-006, UP2-REQ-F-012. Rules: UP2-BR-001, UP2-BR-006, UP2-BR-010. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - link "New customer"
  - link "Find customer"
  - button "Sign out"
- [ ] UP2-C01-T5 [ui-modernization] Build the screen New customer (S-CUSTOMER-NEW). Requirements: UP2-REQ-F-001, UP2-REQ-F-002, UP2-REQ-F-003, UP2-REQ-F-004, UP2-REQ-F-005, UP2-REQ-F-011, UP2-REQ-F-013. Rules: UP2-BR-001, UP2-BR-002, UP2-BR-003, UP2-BR-004, UP2-BR-005, UP2-BR-009, UP2-BR-010. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-CUSTOMER-NEW.
  - text "Postcode": Postcode can be at most 8 characters
  - button "Add customer"
  - button "Clear form"
  - display "Customer number"
  - message "Result"
  - message "Action not available": Only the actions shown as buttons here (Add customer, Clear form) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C01-T6 [ui-modernization] Build the screen Customer details (S-CUSTOMER-EDIT). Requirements: UP2-REQ-F-006, UP2-REQ-F-007, UP2-REQ-F-008, UP2-REQ-F-009, UP2-REQ-F-010, UP2-REQ-F-011, UP2-REQ-F-013. Rules: UP2-BR-006, UP2-BR-007, UP2-BR-008, UP2-BR-009, UP2-BR-010. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-CUSTOMER-EDIT.
  - search "Customer number": Customer number must be up to 10 digits: enter digits only, for example 0000000001
  - button "Find"
  - message "Customer not found"
  - text "Postcode": Postcode can be at most 8 characters
  - button "Save changes"
  - button "Discard changes"
  - message "Result"
  - message "Action not available": Only the actions shown as buttons here (Find, Save changes, Discard changes) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C01-T7 [ui-modernization] Build the screen Find policies (S-POLICY-FIND). Requirements: UP2-REQ-F-011. Rules: UP2-BR-009. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-POLICY-FIND.
  - button "Search"
  - message "Action not available": Only the actions shown as buttons here (Search, Open, New policy, Clear search) can run. Motor and life policies offer inquire, add, delete and update; house policies offer add, update and delete; commercial policies offer inquire, add and delete. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown.
- [ ] UP2-C01-T8 [ui-modernization] Build the screen Motor policy (S-MOTOR-POLICY). Requirements: UP2-REQ-F-011. Rules: UP2-BR-009. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-MOTOR-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C01-T9 [ui-modernization] Build the screen Life (endowment) policy (S-LIFE-POLICY). Requirements: UP2-REQ-F-011. Rules: UP2-BR-009. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-LIFE-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C01-T10 [ui-modernization] Build the screen House policy (S-HOUSE-POLICY). Requirements: UP2-REQ-F-011. Rules: UP2-BR-009. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-HOUSE-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Save changes, Delete) can run. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C01-T11 [ui-modernization] Build the screen Commercial property policy (S-COMMERCIAL-POLICY). Requirements: UP2-REQ-F-011. Rules: UP2-BR-009. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-COMMERCIAL-POLICY.
  - message "Action not available": Only the actions shown as buttons here (Add, Delete) can run, plus finding a policy on S-POLICY-FIND; commercial policies cannot be updated. Any other request calls no back-end service and shows 'Please enter a valid option': choose one of the action buttons shown. Focus moves to the first action button.
- [ ] UP2-C01-T12 [ui-modernization] Build the screen Claim (S-CLAIM-VIEW). Requirements: UP2-REQ-F-011. Rules: UP2-BR-009. After: UP2-C01-T2, UP2-C01-T3.
  - To the prototype: ui-reference/index.html#/S-CLAIM-VIEW.
  - message "Action not available": Only Find can run here. Any other request calls no back-end service and shows 'Please enter a valid option': use the Find button.
- [ ] UP2-C01-T13 [test-generation] Write a test for every acceptance criterion. Requirements: UP2-REQ-F-001, UP2-REQ-F-002, UP2-REQ-F-003, UP2-REQ-F-004, UP2-REQ-F-005, UP2-REQ-F-006, UP2-REQ-F-007, UP2-REQ-F-008, UP2-REQ-F-009, UP2-REQ-F-010, UP2-REQ-F-011, UP2-REQ-F-012, UP2-REQ-F-013. Criteria: UP2-C01-AC-01, UP2-C01-AC-02, UP2-C01-AC-03, UP2-C01-AC-04, UP2-C01-AC-05, UP2-C01-AC-06, UP2-C01-AC-07, UP2-C01-AC-08, UP2-C01-AC-09, UP2-C01-AC-10, UP2-C01-AC-11, UP2-C01-AC-12, UP2-C01-AC-13, UP2-C01-AC-14. After: UP2-C01-T1, UP2-C01-T2, UP2-C01-T3, UP2-C01-T4, UP2-C01-T5, UP2-C01-T6, UP2-C01-T7, UP2-C01-T8, UP2-C01-T9, UP2-C01-T10, UP2-C01-T11, UP2-C01-T12.
  - 14 acceptance criteria, each a test named by its ID.
- [ ] UP2-C01-T14 [compliance] Review the handling of personal data. Requirements: UP2-REQ-F-001, UP2-REQ-F-002, UP2-REQ-F-003, UP2-REQ-F-004, UP2-REQ-F-005, UP2-REQ-F-006, UP2-REQ-F-007, UP2-REQ-F-008, UP2-REQ-F-009, UP2-REQ-F-010, UP2-REQ-F-011, UP2-REQ-F-012, UP2-REQ-F-013. After: UP2-C01-T1, UP2-C01-T2, UP2-C01-T3, UP2-C01-T4, UP2-C01-T5, UP2-C01-T6, UP2-C01-T7, UP2-C01-T8, UP2-C01-T9, UP2-C01-T10, UP2-C01-T11, UP2-C01-T12.
  - Check storage, logs, screens and audit against the rules.
