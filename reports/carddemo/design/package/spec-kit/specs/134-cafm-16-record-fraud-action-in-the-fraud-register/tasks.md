# Tasks: Record fraud action in the fraud register (CAFM-C16)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C16-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146.
  - Working records it passes or builds: CIPAUDTY.
- [ ] CAFM-C16-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-143, CAFM-REQ-F-144. Rules: CAFM-BR-158, CAFM-BR-159. After: CAFM-C16-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C16-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-145, CAFM-REQ-F-146. Rules: CAFM-BR-160, CAFM-BR-161. After: CAFM-C16-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C16-T4 [api] Build the services behind the screens. Requirements: CAFM-REQ-F-142. Rules: CAFM-BR-157. After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3.
  - CAFM-BR-157: The fraud register is keyed by card number plus the authorization's original timestamp. The legacy authorization stores its time as a complement (999999999 minus the time) so newest sorts first; the new application should store the real authorization timestamp on the authorization and use it directly, with a unique key on (card number, authorization timestamp) so that recording is an upsert. If legacy data is migrated, convert the complemented time once, during migration.
- [ ] CAFM-C16-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS). Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146. Rules: CAFM-BR-157, CAFM-BR-158, CAFM-BR-159, CAFM-BR-160, CAFM-BR-161. After: CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **primary button** "Report fraud / Remove fraud mark": Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.'
- [ ] CAFM-C16-T6 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146. Criteria: CAFM-C16-AC-01, CAFM-C16-AC-02, CAFM-C16-AC-03, CAFM-C16-AC-04, CAFM-C16-AC-05. After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4, CAFM-C16-T5.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C16-T7 [compliance] Review the handling of audit, card data, personal data. Requirements: CAFM-REQ-F-142, CAFM-REQ-F-143, CAFM-REQ-F-144, CAFM-REQ-F-145, CAFM-REQ-F-146. After: CAFM-C16-T1, CAFM-C16-T2, CAFM-C16-T3, CAFM-C16-T4, CAFM-C16-T5.
  - Check storage, logs, screens and audit against the rules.
