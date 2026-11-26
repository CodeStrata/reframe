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
  - CAFM-BR-157: The pending authorization stores its time in complemented form (999999999 minus the time) so newest sorts first. The fraud register needs the real timestamp, so the new application must convert back (999999999 minus the stored value) and combine it with the original authorization date. Card number plus that timestamp is the unique key of a fraud record; if the new data model stores the real time directly, the conversion goes away but the key must stay the same.
  - _Requirements: CAFM-REQ-F-142_
  - _Rules: CAFM-BR-157_
  - _After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3_
- [ ] 5. CAFM-C16-T5 [ui-modernization] Build the screen Authorization details (S-AUTH-DETAIL)
  - To the prototype: ui-reference/index.html#/S-AUTH-DETAIL.
  - dialog "Confirm fraud action"
  - message "Fraud action result"
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
