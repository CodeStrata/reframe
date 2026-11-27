# Implementation plan: Record fraud action in the fraud register (CAFM-C16)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C16-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY.
  - _Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146_
- [ ] 2. CAFM-C16-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-143, CAFM-REQ-F-144_
  - _Rules: CAFM-BR-158, CAFM-BR-159_
  - _After: CAFM-C16-T1_
- [ ] 3. CAFM-C16-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-145, CAFM-REQ-F-146_
  - _Rules: CAFM-BR-160, CAFM-BR-161_
  - _After: CAFM-C16-T1_
- [ ] 4. CAFM-C16-T4 [api] Build the services behind the screens
  - CAFM-BR-157: The fraud register is keyed by card number plus the authorization's original timestamp. The legacy authorization stores its time as a complement (999999999 minus the time) so newest sorts first; the new application should store the real authorization timestamp on the authorization and use it directly, with a unique key on (card number, authorization timestamp) so that recording is an upsert. If legacy data is migrated, convert the complemented time once, during migration.
  - _Requirements: CAFM-REQ-F-142_
  - _Rules: CAFM-BR-157_
  - _After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3_
- [ ] 5. CAFM-C16-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **primary button** "Report fraud / Remove fraud mark": Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.'
  - _Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146_
  - _Rules: CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-160, CAFM-BR-161_
  - _After: CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4_
- [ ] 6. CAFM-C16-T6 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146_
  - _Criteria: CAFM-C16-AC-01, CAFM-C16-AC-02, CAFM-C16-AC-03, CAFM-C16-AC-04, CAFM-C16-AC-05_
  - _After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4, CAFM-C16-T5_
- [ ] 7. CAFM-C16-T7 [compliance] Review the handling of audit, card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146_
  - _After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4, CAFM-C16-T5_
