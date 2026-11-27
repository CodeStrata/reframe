# Tasks: Mark or unmark an authorization as fraud (CAFM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C15-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141.
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
- [ ] CAFM-C15-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-F-141. Rules: CAFM-BR-143, CAFM-BR-144, CAFM-BR-145, CAFM-BR-146, CAFM-BR-147, CAFM-BR-148, CAFM-BR-149, CAFM-BR-150, CAFM-BR-151, CAFM-BR-156. After: CAFM-C15-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C15-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140. Rules: CAFM-BR-152, CAFM-BR-153, CAFM-BR-154, CAFM-BR-155. After: CAFM-C15-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C15-T4 [api] Build the services behind the screens. Requirements: CAFM-REQ-F-135. Rules: CAFM-BR-147. After: CAFM-C15-T1, CAFM-C15-T2, CAFM-C15-T3.
  - CAFM-BR-147: The fraud action is one synchronous call from the detail screen to a fraud-recording service, passing the full authorization, the account number, the customer number and the action ('F' report or 'R' remove). The service stamps today's date (MM/DD/YY) as the fraud report date on the authorization it returns and reports success or failure with a message. Both the fraud register write and the authorization update must run in one transaction (or an equivalent all-or-nothing mechanism), committed only after the authorization update succeeds.
- [ ] CAFM-C15-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS). Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141. Rules: CAFM-BR-143, CAFM-BR-144, CAFM-BR-145, CAFM-BR-146, CAFM-BR-147, CAFM-BR-148, CAFM-BR-149, CAFM-BR-150, CAFM-BR-151, CAFM-BR-152, CAFM-BR-153, CAFM-BR-154, CAFM-BR-155, CAFM-BR-156. After: CAFM-C15-T2, CAFM-C15-T3, CAFM-C15-T4.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **primary button** "Report fraud / Remove fraud mark": Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.'
- [ ] CAFM-C15-T6 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141. Criteria: CAFM-C15-AC-01, CAFM-C15-AC-02, CAFM-C15-AC-03, CAFM-C15-AC-04, CAFM-C15-AC-05, CAFM-C15-AC-06, CAFM-C15-AC-07, CAFM-C15-AC-08, CAFM-C15-AC-09, CAFM-C15-AC-10, CAFM-C15-AC-11, CAFM-C15-AC-12, CAFM-C15-AC-13, CAFM-C15-AC-14, CAFM-C15-AC-15, CAFM-C15-AC-16, CAFM-C15-AC-17. After: CAFM-C15-T1, CAFM-C15-T2, CAFM-C15-T3, CAFM-C15-T4, CAFM-C15-T5.
  - 17 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C15-T7 [compliance] Review the handling of audit, card data, personal data. Requirements: CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-N-003, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141. After: CAFM-C15-T1, CAFM-C15-T2, CAFM-C15-T3, CAFM-C15-T4, CAFM-C15-T5.
  - Check storage, logs, screens and audit against the rules.
