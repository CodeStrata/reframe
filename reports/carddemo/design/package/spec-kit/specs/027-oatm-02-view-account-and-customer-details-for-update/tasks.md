# Tasks: View account and customer details for update (OATM-C02)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C02-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
- [ ] OATM-C02-T2 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024. Rules: OATM-BR-015, OATM-BR-016, OATM-BR-017, OATM-BR-018, OATM-BR-019, OATM-BR-020, OATM-BR-021, OATM-BR-022, OATM-BR-023, OATM-BR-024, OATM-BR-025. After: OATM-C02-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C02-T3 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT). Requirements: OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-022, OATM-REQ-N-002. Rules: OATM-BR-018, OATM-BR-019, OATM-BR-022, OATM-BR-025. After: OATM-C02-T2.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - search "Account number": Required: 'No input received' when blank; 'Account Number if supplied must be a 11 digit Non-Zero Number' when not numeric or all zeros; 'Account:<number> not found in Cross ref file' when the account has no card cross-reference.
  - message "Guidance"
  - form "Account and customer details": If nothing differs from the fetched values (ignoring case): 'No change detected with respect to values fetched.' and nothing is checked or saved.
  - display "Customer ID"
  - display "Country"
  - dialog "Save these changes?"
- [ ] OATM-C02-T4 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024. Criteria: OATM-C02-AC-01, OATM-C02-AC-02, OATM-C02-AC-03, OATM-C02-AC-04, OATM-C02-AC-05, OATM-C02-AC-06, OATM-C02-AC-07, OATM-C02-AC-08, OATM-C02-AC-09, OATM-C02-AC-10, OATM-C02-AC-11, OATM-C02-AC-12, OATM-C02-AC-13, OATM-C02-AC-14, OATM-C02-AC-15. After: OATM-C02-T1, OATM-C02-T2, OATM-C02-T3.
  - 15 acceptance criteria, each a test named by its ID.
- [ ] OATM-C02-T5 [compliance] Review the handling of card data, money, personal data. Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024. After: OATM-C02-T1, OATM-C02-T2, OATM-C02-T3.
  - Check storage, logs, screens and audit against the rules.
