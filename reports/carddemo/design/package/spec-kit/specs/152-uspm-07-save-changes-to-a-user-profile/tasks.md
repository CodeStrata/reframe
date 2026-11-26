# Tasks: Save changes to a user profile (USPM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] USPM-C07-T1 [data] Model the data the capability reads and writes. Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075.
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] USPM-C07-T2 [business-rules] Implement the business rules. Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-073, USPM-REQ-F-074. Rules: USPM-BR-072, USPM-BR-073, USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-079, USPM-BR-081, USPM-BR-082. After: USPM-C07-T1.
  - Keep each business rule exactly as specified.
- [ ] USPM-C07-T3 [business-rules] Implement error handling and messages. Requirements: USPM-REQ-F-072, USPM-REQ-F-075. Rules: USPM-BR-080, USPM-BR-083. After: USPM-C07-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] USPM-C07-T4 [ui-modernization] Build the screen Update user (S-USER-EDIT). Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075. Rules: USPM-BR-072, USPM-BR-073, USPM-BR-074, USPM-BR-075, USPM-BR-076, USPM-BR-077, USPM-BR-078, USPM-BR-079, USPM-BR-080, USPM-BR-081, USPM-BR-082, USPM-BR-083. After: USPM-C07-T2, USPM-C07-T3.
  - To the prototype: ui-reference/index.html#/S-USER-EDIT.
  - search "User ID": Required: 'User ID can NOT be empty...'. Unknown: 'User ID NOT found...' and the details stay empty
  - form "User details"
  - text "First name": Required: 'First Name can NOT be empty...'
  - text "Last name": Required: 'Last Name can NOT be empty...'
  - password "Password": Required: 'Password can NOT be empty...'
  - radio "User type": Required: 'User Type can NOT be empty...'
  - button "Save": Nothing changed: 'Please modify to update ...'
  - button "Save and close"
- [ ] USPM-C07-T5 [test-generation] Write a test for every acceptance criterion. Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075. Criteria: USPM-C07-AC-01, USPM-C07-AC-02, USPM-C07-AC-03, USPM-C07-AC-04, USPM-C07-AC-05, USPM-C07-AC-06, USPM-C07-AC-07, USPM-C07-AC-08, USPM-C07-AC-09, USPM-C07-AC-10, USPM-C07-AC-11, USPM-C07-AC-12, USPM-C07-AC-13. After: USPM-C07-T1, USPM-C07-T2, USPM-C07-T3, USPM-C07-T4.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] USPM-C07-T6 [compliance] Review the handling of personal data, security. Requirements: USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-067, USPM-REQ-F-068, USPM-REQ-F-069, USPM-REQ-F-070, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075. After: USPM-C07-T1, USPM-C07-T2, USPM-C07-T3, USPM-C07-T4.
  - Check storage, logs, screens and audit against the rules.
