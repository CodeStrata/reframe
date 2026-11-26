# Tasks: Filter the card list by account and card number (CCLDV-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CCLDV-C02-T1 [data] Model the data the capability reads and writes. Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027.
  - File records: CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y.
- [ ] CCLDV-C02-T2 [business-rules] Implement the business rules. Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026. Rules: CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-025, CCLDV-BR-026, CCLDV-BR-027. After: CCLDV-C02-T1.
  - Keep each business rule exactly as specified.
- [ ] CCLDV-C02-T3 [business-rules] Implement error handling and messages. Requirements: CCLDV-REQ-F-027. Rules: CCLDV-BR-021, CCLDV-BR-028. After: CCLDV-C02-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CCLDV-C02-T4 [ui-modernization] Build the screen Cards (S-CARD-LIST). Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027. Rules: CCLDV-BR-021, CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-025, CCLDV-BR-026, CCLDV-BR-027, CCLDV-BR-028. After: CCLDV-C02-T2, CCLDV-C02-T3.
  - To the prototype: ui-reference/index.html#/S-CARD-LIST.
  - form "Filter cards"
  - text "Account number": If supplied, must be an 11-digit number; blank or all zeros means no account filter. Message: 'Account filter, if supplied, must be an 11-digit number.'
  - text "Card number": If supplied, must be a 16-digit number; blank or all zeros means no card filter. Message: 'Card number filter, if supplied, must be a 16-digit number.'
  - message "Problems with the filters"
- [ ] CCLDV-C02-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027. Criteria: CCLDV-C02-AC-01, CCLDV-C02-AC-02, CCLDV-C02-AC-03, CCLDV-C02-AC-04, CCLDV-C02-AC-05, CCLDV-C02-AC-06, CCLDV-C02-AC-07, CCLDV-C02-AC-08, CCLDV-C02-AC-09, CCLDV-C02-AC-10. After: CCLDV-C02-T1, CCLDV-C02-T2, CCLDV-C02-T3, CCLDV-C02-T4.
  - 10 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C02-T6 [compliance] Review the handling of card data. Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027. After: CCLDV-C02-T1, CCLDV-C02-T2, CCLDV-C02-T3, CCLDV-C02-T4.
  - Check storage, logs, screens and audit against the rules.
