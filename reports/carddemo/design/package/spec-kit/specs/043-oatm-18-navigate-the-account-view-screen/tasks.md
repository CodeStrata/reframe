# Tasks: Navigate the account view screen (OATM-C18)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C18-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-143, OATM-REQ-F-144, OATM-REQ-F-145, OATM-REQ-F-146, OATM-REQ-F-147, OATM-REQ-F-148.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
- [ ] OATM-C18-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-143, OATM-REQ-F-144, OATM-REQ-F-146. Rules: OATM-BR-148, OATM-BR-149, OATM-BR-151. After: OATM-C18-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C18-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-148. Rules: OATM-BR-153. After: OATM-C18-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C18-T4 [api] Build the services behind the screens. Requirements: OATM-REQ-F-145, OATM-REQ-F-147. Rules: OATM-BR-150, OATM-BR-152. After: OATM-C18-T1, OATM-C18-T2, OATM-C18-T3.
  - OATM-BR-150: The screen needs a per-user conversation state with a 'first entry' marker. When there is no session, or the user arrives fresh from the main menu, the server creates new screen state and ignores any data passed in. Only a return visit to the same screen reuses its state.
  - OATM-BR-152: Each time the account view is rendered, store its session state server-side (or in a signed client token) marked as 're-entry'. The next request from the user then resumes the same account view conversation. No process stays waiting between requests: the flow is stateless request handling with persisted session state.
- [ ] OATM-C18-T5 [ui-modernization] Build the screen Account (S-ACCOUNT-VIEW). Requirements: OATM-REQ-F-143, OATM-REQ-F-144, OATM-REQ-F-145, OATM-REQ-F-146, OATM-REQ-F-147. Rules: OATM-BR-148, OATM-BR-149, OATM-BR-150, OATM-BR-151, OATM-BR-152. After: OATM-C18-T2, OATM-C18-T3, OATM-C18-T4.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-VIEW.
  - button "View account"
  - message "Account lookup error"
  - link "Back"
- [ ] OATM-C18-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-143, OATM-REQ-F-144, OATM-REQ-F-145, OATM-REQ-F-146, OATM-REQ-F-147, OATM-REQ-F-148. Criteria: OATM-C18-AC-01, OATM-C18-AC-02, OATM-C18-AC-03, OATM-C18-AC-04, OATM-C18-AC-05, OATM-C18-AC-06, OATM-C18-AC-07, OATM-C18-AC-08. After: OATM-C18-T1, OATM-C18-T2, OATM-C18-T3, OATM-C18-T4, OATM-C18-T5.
  - 8 acceptance criteria, each a test named by its ID.
