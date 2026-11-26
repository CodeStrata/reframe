# Tasks: Navigate the authorization detail screen (CAFM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C14-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-127, CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132.
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
- [ ] CAFM-C14-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-132. Rules: CAFM-BR-136, CAFM-BR-137, CAFM-BR-138, CAFM-BR-139, CAFM-BR-141, CAFM-BR-142. After: CAFM-C14-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C14-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-131. Rules: CAFM-BR-140. After: CAFM-C14-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C14-T4 [api] Build the services behind the screens. Requirements: CAFM-REQ-F-127. Rules: CAFM-BR-135. After: CAFM-C14-T1, CAFM-C14-T2, CAFM-C14-T3.
  - CAFM-BR-135: The detail view can only be reached with an account and a selected authorization supplied by the pending authorization list. If it is opened directly without that context (e.g. a deep link or a fresh session), the application must redirect the user to the pending authorization list instead of showing an empty detail page.
- [ ] CAFM-C14-T5 [ui-modernization] Build the screen Authorization details (S-AUTH-DETAIL). Requirements: CAFM-REQ-F-127, CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132. Rules: CAFM-BR-135, CAFM-BR-136, CAFM-BR-137, CAFM-BR-138, CAFM-BR-139, CAFM-BR-140, CAFM-BR-141, CAFM-BR-142. After: CAFM-C14-T2, CAFM-C14-T3, CAFM-C14-T4.
  - To the prototype: ui-reference/index.html#/S-AUTH-DETAIL.
  - message "Authorization could not be shown": If the account is not numeric or no authorization is selected, details are left blank and the user is sent back to choose an authorization from the list. System errors: ' System error while reading Auth Summary: Code:<code>', ' System error while reading Auth Details: Code:<code>', ' System error while reading next Auth: Code:<code>'.
  - message "Shortcut not available": Unsupported shortcut: 'Invalid key pressed. Please see below...' — use Refresh, Next authorization, Mark/Remove fraud or Back.
  - button "Next authorization"
  - link "Back to pending authorizations"
- [ ] CAFM-C14-T6 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-127, CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132. Criteria: CAFM-C14-AC-01, CAFM-C14-AC-02, CAFM-C14-AC-03, CAFM-C14-AC-04, CAFM-C14-AC-05, CAFM-C14-AC-06, CAFM-C14-AC-07, CAFM-C14-AC-08. After: CAFM-C14-T1, CAFM-C14-T2, CAFM-C14-T3, CAFM-C14-T4, CAFM-C14-T5.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C14-T7 [compliance] Review the handling of card data. Requirements: CAFM-REQ-F-127, CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132. After: CAFM-C14-T1, CAFM-C14-T2, CAFM-C14-T3, CAFM-C14-T4, CAFM-C14-T5.
  - Check storage, logs, screens and audit against the rules.
