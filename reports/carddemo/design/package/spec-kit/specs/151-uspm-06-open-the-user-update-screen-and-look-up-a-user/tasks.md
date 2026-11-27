# Tasks: Open the User Update screen and look up a user (USPM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] USPM-C06-T1 [data] Model the data the capability reads and writes. Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063.
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] USPM-C06-T2 [business-rules] Implement the business rules. Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-057, USPM-REQ-F-059, USPM-REQ-F-062, USPM-REQ-F-063. Rules: USPM-BR-061, USPM-BR-062, USPM-BR-063, USPM-BR-065, USPM-BR-067, USPM-BR-070, USPM-BR-071. After: USPM-C06-T1.
  - Keep each business rule exactly as specified.
- [ ] USPM-C06-T3 [business-rules] Implement error handling and messages. Requirements: USPM-REQ-F-060, USPM-REQ-F-056, USPM-REQ-F-058, USPM-REQ-F-061. Rules: USPM-BR-064, USPM-BR-066, USPM-BR-068, USPM-BR-069. After: USPM-C06-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] USPM-C06-T4 [ui-modernization] Build the screen Update user (S-USER-EDIT). Requirements: USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063. Rules: USPM-BR-062, USPM-BR-063, USPM-BR-064, USPM-BR-065, USPM-BR-066, USPM-BR-067, USPM-BR-068, USPM-BR-069, USPM-BR-070, USPM-BR-071. After: USPM-C06-T2, USPM-C06-T3.
  - To the prototype: ui-reference/index.html#/S-USER-EDIT.
  - **lookup field** "User ID": Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...', and the details stay blank. Read failure: 'Unable to lookup User...'.
  - **primary button** "Save changes": Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'.
- [ ] USPM-C06-T5 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER). Requirements: USPM-REQ-F-054. Rules: USPM-BR-061. After: USPM-C06-T2, USPM-C06-T3.
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **data table** "Navigation": Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home.
- [ ] USPM-C06-T6 [test-generation] Write a test for every acceptance criterion. Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063. Criteria: USPM-C06-AC-01, USPM-C06-AC-02, USPM-C06-AC-03, USPM-C06-AC-04, USPM-C06-AC-05, USPM-C06-AC-06, USPM-C06-AC-07, USPM-C06-AC-08, USPM-C06-AC-09, USPM-C06-AC-10. After: USPM-C06-T1, USPM-C06-T2, USPM-C06-T3, USPM-C06-T4, USPM-C06-T5.
  - 10 acceptance criteria, each a test named by its ID.
- [ ] USPM-C06-T7 [compliance] Review the handling of personal data, security. Requirements: USPM-REQ-F-054, USPM-REQ-F-055, USPM-REQ-F-056, USPM-REQ-F-057, USPM-REQ-F-058, USPM-REQ-F-059, USPM-REQ-F-060, USPM-REQ-F-061, USPM-REQ-F-062, USPM-REQ-F-063. After: USPM-C06-T1, USPM-C06-T2, USPM-C06-T3, USPM-C06-T4, USPM-C06-T5.
  - Check storage, logs, screens and audit against the rules.
