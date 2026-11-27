# Tasks: Look up and update a user (USPM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] USPM-C05-T1 [data] Model the data the capability reads and writes. Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053.
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] USPM-C05-T2 [business-rules] Implement the business rules. Requirements: USPM-REQ-F-051. Rules: USPM-BR-057, USPM-BR-058. After: USPM-C05-T1.
  - Keep each business rule exactly as specified.
- [ ] USPM-C05-T3 [business-rules] Implement error handling and messages. Requirements: USPM-REQ-F-053. Rules: USPM-BR-060. After: USPM-C05-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] USPM-C05-T4 [api] Build the services behind the screens. Requirements: USPM-REQ-F-052. Rules: USPM-BR-059. After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3.
  - USPM-BR-059: For a non-blank User ID, clear the detail fields, then fetch that user by its key from the user store. Read it so that a later save in the same flow can update that record safely, for example with optimistic concurrency (a version or the read values).
- [ ] USPM-C05-T5 [ui-modernization] Build the screen Update user (S-USER-EDIT). Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053. Rules: USPM-BR-057, USPM-BR-058, USPM-BR-059, USPM-BR-060. After: USPM-C05-T2, USPM-C05-T3, USPM-C05-T4.
  - To the prototype: ui-reference/index.html#/S-USER-EDIT.
  - **lookup field** "User ID": Blank: 'User ID can NOT be empty...' Not on file: 'User ID NOT found...', and the details stay blank. Read failure: 'Unable to lookup User...'.
  - **primary button** "Save changes": Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'.
- [ ] USPM-C05-T6 [test-generation] Write a test for every acceptance criterion. Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053. Criteria: USPM-C05-AC-01, USPM-C05-AC-02, USPM-C05-AC-03, USPM-C05-AC-04. After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3, USPM-C05-T4, USPM-C05-T5.
  - 4 acceptance criteria, each a test named by its ID.
- [ ] USPM-C05-T7 [compliance] Review the handling of personal data, security. Requirements: USPM-REQ-F-051, USPM-REQ-F-052, USPM-REQ-F-053. After: USPM-C05-T1, USPM-C05-T2, USPM-C05-T3, USPM-C05-T4, USPM-C05-T5.
  - Check storage, logs, screens and audit against the rules.
