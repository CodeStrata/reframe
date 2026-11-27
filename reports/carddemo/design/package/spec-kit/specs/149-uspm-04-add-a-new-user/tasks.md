# Tasks: Add a new user (USPM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] USPM-C04-T1 [data] Model the data the capability reads and writes. Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-F-046, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-049, USPM-REQ-F-050.
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] USPM-C04-T2 [business-rules] Implement the business rules. Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-050. Rules: USPM-BR-044, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-050, USPM-BR-052, USPM-BR-053, USPM-BR-054, USPM-BR-056. After: USPM-C04-T1.
  - Keep each business rule exactly as specified.
- [ ] USPM-C04-T3 [business-rules] Implement error handling and messages. Requirements: USPM-REQ-F-049. Rules: USPM-BR-055. After: USPM-C04-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] USPM-C04-T4 [api] Build the services behind the screens. Requirements: USPM-REQ-F-046. Rules: USPM-BR-051. After: USPM-C04-T1, USPM-C04-T2, USPM-C04-T3.
  - USPM-BR-051: Map the five entered fields onto a new user record keyed by User ID and insert it into the user store as a create-only operation. The insert must fail with a distinct 'duplicate key' result when the User ID already exists, so the screen can tell 'already exists' apart from other failures.
- [ ] USPM-C04-T5 [ui-modernization] Build the screen Add user (S-USER-ADD). Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-F-046, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-049, USPM-REQ-F-050. Rules: USPM-BR-044, USPM-BR-045, USPM-BR-046, USPM-BR-047, USPM-BR-048, USPM-BR-049, USPM-BR-050, USPM-BR-051, USPM-BR-052, USPM-BR-053, USPM-BR-054, USPM-BR-055, USPM-BR-056. After: USPM-C04-T2, USPM-C04-T3, USPM-C04-T4.
  - To the prototype: ui-reference/index.html#/S-USER-ADD.
  - **lookup field** "First name": Blank: 'First Name can NOT be empty...'
  - **lookup field** "Last name": Blank: 'Last Name can NOT be empty...'
  - **lookup field** "User ID": Blank: 'User ID can NOT be empty...' Already used: 'User ID already exist...'; nothing is added and the existing user is not changed.
  - **lookup field** "Password": Blank: 'Password can NOT be empty...'
  - **lookup field** "User type": None chosen: 'User Type can NOT be empty...'
  - **primary button** "Add user": Checks First name, Last name, User ID, Password and User type in that order. Every blank field is listed in an error summary at the top, each linked to its field, and nothing is added until all are filled. Any other failure: 'Unable to Add User...', with focus on First name.
- [ ] USPM-C04-T6 [test-generation] Write a test for every acceptance criterion. Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-F-046, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-049, USPM-REQ-F-050. Criteria: USPM-C04-AC-01, USPM-C04-AC-02, USPM-C04-AC-03, USPM-C04-AC-04, USPM-C04-AC-05, USPM-C04-AC-06, USPM-C04-AC-07, USPM-C04-AC-08, USPM-C04-AC-09, USPM-C04-AC-10, USPM-C04-AC-11, USPM-C04-AC-12, USPM-C04-AC-13. After: USPM-C04-T1, USPM-C04-T2, USPM-C04-T3, USPM-C04-T4, USPM-C04-T5.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] USPM-C04-T7 [compliance] Review the handling of personal data, security. Requirements: USPM-REQ-F-039, USPM-REQ-F-040, USPM-REQ-F-041, USPM-REQ-F-042, USPM-REQ-F-043, USPM-REQ-F-044, USPM-REQ-F-045, USPM-REQ-F-046, USPM-REQ-N-002, USPM-REQ-F-047, USPM-REQ-F-048, USPM-REQ-F-049, USPM-REQ-F-050. After: USPM-C04-T1, USPM-C04-T2, USPM-C04-T3, USPM-C04-T4, USPM-C04-T5.
  - Check storage, logs, screens and audit against the rules.
