# Tasks: Find and show a card for update (CCLDV-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CCLDV-C07-T1 [data] Model the data the capability reads and writes. Requirements: CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-065, CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-074, CCLDV-REQ-F-075, CCLDV-REQ-F-076, CCLDV-REQ-F-077.
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
- [ ] CCLDV-C07-T2 [business-rules] Implement the business rules. Requirements: CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-077. Rules: CCLDV-BR-069, CCLDV-BR-070, CCLDV-BR-071, CCLDV-BR-072, CCLDV-BR-073, CCLDV-BR-074, CCLDV-BR-075, CCLDV-BR-076, CCLDV-BR-077, CCLDV-BR-078, CCLDV-BR-079, CCLDV-BR-084. After: CCLDV-C07-T1.
  - Keep each business rule exactly as specified.
- [ ] CCLDV-C07-T3 [business-rules] Implement error handling and messages. Requirements: CCLDV-REQ-F-074, CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-076. Rules: CCLDV-BR-061, CCLDV-BR-062, CCLDV-BR-063, CCLDV-BR-064, CCLDV-BR-065, CCLDV-BR-066, CCLDV-BR-080, CCLDV-BR-082, CCLDV-BR-083. After: CCLDV-C07-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CCLDV-C07-T4 [api] Build the services behind the screens. Requirements: CCLDV-REQ-F-065, CCLDV-REQ-F-075. Rules: CCLDV-BR-067, CCLDV-BR-068, CCLDV-BR-081. After: CCLDV-C07-T1, CCLDV-C07-T2, CCLDV-C07-T3.
  - CCLDV-BR-067: The account number input treats '*' or blank as 'not supplied'. Any other value is used both as the account to search on and as the account carried forward with the edit. The new form should keep the two meanings separate in its model, even though one field fills both.
  - CCLDV-BR-068: The card number input treats '*' or blank as 'not supplied'. Any other value is used both as the lookup key (a keyed lookup of the card by card number) and as the card number carried forward with the edit.
  - CCLDV-BR-081: When the card is found, the server keeps a snapshot of the original values for the length of the edit: the embossed name in upper case, the expiry year, month and day split from the stored date (YYYY-MM-DD), the active status and the CVV code. This snapshot is the baseline for the 'no change' check and for spotting that someone else changed the card before the save (optimistic concurrency), so it must be held on the server and not trusted from the browser.
- [ ] CCLDV-C07-T5 [ui-modernization] Build the screen Card (S-CARD-DETAIL). Requirements: CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-065, CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-074, CCLDV-REQ-F-075, CCLDV-REQ-F-076, CCLDV-REQ-F-077. Rules: CCLDV-BR-061, CCLDV-BR-062, CCLDV-BR-063, CCLDV-BR-064, CCLDV-BR-065, CCLDV-BR-066, CCLDV-BR-067, CCLDV-BR-068, CCLDV-BR-069, CCLDV-BR-070, CCLDV-BR-071, CCLDV-BR-072, CCLDV-BR-073, CCLDV-BR-074, CCLDV-BR-075, CCLDV-BR-076, CCLDV-BR-077, CCLDV-BR-078, CCLDV-BR-079, CCLDV-BR-080, CCLDV-BR-081, CCLDV-BR-082, CCLDV-BR-083, CCLDV-BR-084. After: CCLDV-C07-T2, CCLDV-C07-T3, CCLDV-C07-T4.
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - form "Find a card"
  - text "Account number": Required; must be an 11-digit number other than all zeros. Messages: 'Enter the account number.' (blank or zeros; legacy 'Account number not provided'), 'Account number must be an 11-digit number.' (not numeric). When both numbers are missing: 'Enter the account number and card number.' (legacy 'No input received'). Only the search fields are checked until a card is found.
  - text "Card number": Required; must be a 16-digit number other than all zeros. Messages: 'Enter the card number.' (blank or zeros; legacy 'Card number not provided'), 'Card number must be a 16-digit number.' (not numeric)
  - button "Find card"
  - message "Card not found": Card number must exist on the card file: 'No card was found with this card number. Check the numbers and try again.' (legacy 'Did not find cards for this search condition')
  - display "Name on card"
  - display "Status"
  - display "Expiry date"
  - button "Edit card"
  - form "Edit card": Something must change (ignoring upper/lower case): 'No changes to save. The details match the stored values.' (legacy 'No change detected with respect to values fetched.') Errors are reported in the order name, status, expiry month, expiry year.
- [ ] CCLDV-C07-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: CCLDV-REQ-F-061, CCLDV-REQ-F-062. Rules: CCLDV-BR-061, CCLDV-BR-062, CCLDV-BR-063. After: CCLDV-C07-T2, CCLDV-C07-T3, CCLDV-C07-T4.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - link "Find a card by number"
- [ ] CCLDV-C07-T7 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-065, CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-074, CCLDV-REQ-F-075, CCLDV-REQ-F-076, CCLDV-REQ-F-077. Criteria: CCLDV-C07-AC-01, CCLDV-C07-AC-02, CCLDV-C07-AC-03, CCLDV-C07-AC-04, CCLDV-C07-AC-05, CCLDV-C07-AC-06, CCLDV-C07-AC-07, CCLDV-C07-AC-08, CCLDV-C07-AC-09, CCLDV-C07-AC-10, CCLDV-C07-AC-11, CCLDV-C07-AC-12, CCLDV-C07-AC-13, CCLDV-C07-AC-14, CCLDV-C07-AC-15, CCLDV-C07-AC-16, CCLDV-C07-AC-17, CCLDV-C07-AC-18, CCLDV-C07-AC-19, CCLDV-C07-AC-20, CCLDV-C07-AC-21, CCLDV-C07-AC-22, CCLDV-C07-AC-23, CCLDV-C07-AC-24, CCLDV-C07-AC-25, CCLDV-C07-AC-26, CCLDV-C07-AC-27, CCLDV-C07-AC-28, CCLDV-C07-AC-29, CCLDV-C07-AC-30, CCLDV-C07-AC-31, CCLDV-C07-AC-32, CCLDV-C07-AC-33, CCLDV-C07-AC-34. After: CCLDV-C07-T1, CCLDV-C07-T2, CCLDV-C07-T3, CCLDV-C07-T4, CCLDV-C07-T5, CCLDV-C07-T6.
  - 34 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C07-T8 [compliance] Review the handling of card data, personal data. Requirements: CCLDV-REQ-F-061, CCLDV-REQ-F-062, CCLDV-REQ-F-063, CCLDV-REQ-F-064, CCLDV-REQ-F-065, CCLDV-REQ-F-066, CCLDV-REQ-F-067, CCLDV-REQ-F-068, CCLDV-REQ-F-069, CCLDV-REQ-F-070, CCLDV-REQ-F-071, CCLDV-REQ-F-072, CCLDV-REQ-F-073, CCLDV-REQ-F-074, CCLDV-REQ-F-075, CCLDV-REQ-F-076, CCLDV-REQ-F-077. After: CCLDV-C07-T1, CCLDV-C07-T2, CCLDV-C07-T3, CCLDV-C07-T4, CCLDV-C07-T5, CCLDV-C07-T6.
  - Check storage, logs, screens and audit against the rules.
