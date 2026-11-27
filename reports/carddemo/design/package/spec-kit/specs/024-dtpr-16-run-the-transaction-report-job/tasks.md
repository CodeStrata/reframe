# Tasks: Run the transaction report job (DTPR-C16)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C16-T1 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-081. Rules: DTPR-BR-091.
  - Keep each business rule exactly as specified.
- [ ] DTPR-C16-T2 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-N-012. Rules: DTPR-BR-092.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C16-T3 [api] Build the scheduled job. Requirements: DTPR-REQ-F-080. Rules: DTPR-BR-090. After: DTPR-C16-T1, DTPR-C16-T2.
  - DTPR-BR-090: Run the report as a job step that starts only after the period extract exists. It reads the extract and does keyed lookups on the card cross-reference (card to account), transaction types and transaction categories, plus the report date parameters. It writes a new numbered version of the transaction report as 133-character print lines.
- [ ] DTPR-C16-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST). Requirements: DTPR-REQ-F-081. Rules: DTPR-BR-091. After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3.
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **primary button** "Submit report": The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again.
- [ ] DTPR-C16-T5 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-080, DTPR-REQ-F-081, DTPR-REQ-N-012. Criteria: DTPR-C16-AC-01, DTPR-C16-AC-02, DTPR-C16-AC-03. After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3, DTPR-C16-T4.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C16-T6 [compliance] Review the handling of card data, money. Requirements: DTPR-REQ-F-080, DTPR-REQ-F-081, DTPR-REQ-N-012. After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3, DTPR-C16-T4.
  - Check storage, logs, screens and audit against the rules.
