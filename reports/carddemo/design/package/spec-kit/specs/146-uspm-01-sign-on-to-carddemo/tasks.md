# Tasks: Sign on to CardDemo (USPM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] USPM-C01-T1 [data] Model the data the capability reads and writes. Requirements: USPM-REQ-F-001, USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013, USPM-REQ-F-014.
  - File records: CSUSR01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] USPM-C01-T2 [business-rules] Implement the business rules. Requirements: USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013. Rules: USPM-BR-002, USPM-BR-003, USPM-BR-004, USPM-BR-005, USPM-BR-006, USPM-BR-008, USPM-BR-009, USPM-BR-010, USPM-BR-011, USPM-BR-012, USPM-BR-013, USPM-BR-014, USPM-BR-015, USPM-BR-016. After: USPM-C01-T1.
  - Keep each business rule exactly as specified.
- [ ] USPM-C01-T3 [business-rules] Implement error handling and messages. Requirements: USPM-REQ-F-007, USPM-REQ-F-001. Rules: USPM-BR-001, USPM-BR-007. After: USPM-C01-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] USPM-C01-T4 [api] Build the services behind the screens. Requirements: USPM-REQ-F-014. Rules: USPM-BR-017. After: USPM-C01-T1, USPM-C01-T2, USPM-C01-T3.
  - USPM-BR-010: After a successful sign-on, create a session that holds the upper-cased user ID, the user type read from the user record, where the user came from (sign-on) and a 'first entry' marker. Every later screen reads this session to know who the user is and what role they have.
  - USPM-BR-017: While the sign-on screen is showing (first visit, after an input error or after an invalid key), keep the session alive and wait for the user's next action on that screen. Do not lose session data between round trips.
- [ ] USPM-C01-T5 [ui-modernization] Build the screen Sign in (S-SIGN-IN). Requirements: USPM-REQ-F-001, USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013, USPM-REQ-F-014. Rules: USPM-BR-001, USPM-BR-002, USPM-BR-003, USPM-BR-004, USPM-BR-005, USPM-BR-006, USPM-BR-007, USPM-BR-008, USPM-BR-009, USPM-BR-010, USPM-BR-011, USPM-BR-012, USPM-BR-013, USPM-BR-014, USPM-BR-015, USPM-BR-016, USPM-BR-017. After: USPM-C01-T2, USPM-C01-T3, USPM-C01-T4.
  - To the prototype: ui-reference/index.html#/S-SIGN-IN.
  - **summary card** "You have signed out"
  - **lookup field** "User ID": Blank: 'Please enter User ID ...', with focus back on User ID. Not on file: 'User not found. Try again ...' Read failure: 'Unable to verify the User ...' Each message shows under User ID.
  - **lookup field** "Password": Blank: 'Please enter Password ...' Wrong password: 'Wrong Password. Try again ...' Each message shows under Password, with focus on it. Failed attempts are logged; the owner decides the attempt limit and lockout (the legacy allows unlimited attempts).
  - **primary button** "Sign in": Checks User ID first, then Password, and reports the first problem under its field.
- [ ] USPM-C01-T6 [ui-modernization] Build the screen Add user (S-USER-ADD). Requirements: USPM-REQ-F-011. Rules: USPM-BR-011, USPM-BR-013, USPM-BR-014. After: USPM-C01-T2, USPM-C01-T3, USPM-C01-T4.
  - To the prototype: ui-reference/index.html#/S-USER-ADD.
  - **lookup field** "User type": None chosen: 'User Type can NOT be empty...'
- [ ] USPM-C01-T7 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER). Requirements: USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012. Rules: USPM-BR-010, USPM-BR-011, USPM-BR-012, USPM-BR-013, USPM-BR-014, USPM-BR-015. After: USPM-C01-T2, USPM-C01-T3, USPM-C01-T4.
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **summary card** "Signed in as"
  - **primary button** "Sign out"
- [ ] USPM-C01-T8 [test-generation] Write a test for every acceptance criterion. Requirements: USPM-REQ-F-001, USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013, USPM-REQ-F-014. Criteria: USPM-C01-AC-01, USPM-C01-AC-02, USPM-C01-AC-03, USPM-C01-AC-04, USPM-C01-AC-05, USPM-C01-AC-06, USPM-C01-AC-07, USPM-C01-AC-08, USPM-C01-AC-09, USPM-C01-AC-10, USPM-C01-AC-11, USPM-C01-AC-12, USPM-C01-AC-13, USPM-C01-AC-14, USPM-C01-AC-15, USPM-C01-AC-16, USPM-C01-AC-17, USPM-C01-AC-18, USPM-C01-AC-19. After: USPM-C01-T1, USPM-C01-T2, USPM-C01-T3, USPM-C01-T4, USPM-C01-T5, USPM-C01-T6, USPM-C01-T7.
  - 19 acceptance criteria, each a test named by its ID.
- [ ] USPM-C01-T9 [compliance] Review the handling of audit, security. Requirements: USPM-REQ-F-001, USPM-REQ-F-002, USPM-REQ-F-003, USPM-REQ-F-004, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007, USPM-REQ-F-008, USPM-REQ-N-001, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-012, USPM-REQ-F-013, USPM-REQ-F-014. After: USPM-C01-T1, USPM-C01-T2, USPM-C01-T3, USPM-C01-T4, USPM-C01-T5, USPM-C01-T6, USPM-C01-T7.
  - Check storage, logs, screens and audit against the rules.
