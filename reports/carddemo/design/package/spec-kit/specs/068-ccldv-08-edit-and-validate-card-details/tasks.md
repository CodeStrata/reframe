# Tasks: Edit and validate card details (CCLDV-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CCLDV-C08-T1 [data] Model the data the capability reads and writes. Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-087, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091, CCLDV-REQ-F-092.
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
- [ ] CCLDV-C08-T2 [business-rules] Implement the business rules. Requirements: CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091. Rules: CCLDV-BR-091, CCLDV-BR-092, CCLDV-BR-093, CCLDV-BR-094, CCLDV-BR-095, CCLDV-BR-096, CCLDV-BR-097, CCLDV-BR-098, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-102, CCLDV-BR-103, CCLDV-BR-104, CCLDV-BR-105. After: CCLDV-C08-T1.
  - Keep each business rule exactly as specified.
- [ ] CCLDV-C08-T3 [business-rules] Implement error handling and messages. Requirements: CCLDV-REQ-F-087, CCLDV-REQ-F-092. Rules: CCLDV-BR-101, CCLDV-BR-106. After: CCLDV-C08-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CCLDV-C08-T4 [api] Build the services behind the screens. Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079. Rules: CCLDV-BR-085, CCLDV-BR-086, CCLDV-BR-087, CCLDV-BR-088, CCLDV-BR-089, CCLDV-BR-090. After: CCLDV-C08-T1, CCLDV-C08-T2, CCLDV-C08-T3.
  - CCLDV-BR-085: When the edit form is submitted, an embossed name, active status, expiry month or expiry year entered as '*' or left blank counts as 'not supplied', and any other entry is the proposed new value. Map this once in the form-to-model step so the checks only see a value or 'not supplied'.
  - CCLDV-BR-086: An embossed name entered as '*' or left blank is read as 'not supplied'. Any other text is the proposed new name, which the name check then validates.
  - CCLDV-BR-087: An active status entered as '*' or left blank is read as 'not supplied', so the status check reports it as missing rather than as an invalid value.
  - CCLDV-BR-088: An expiry month or expiry year entered as '*' or left blank is read as 'not supplied'. Any other entry is the proposed new value, which the month and year range checks then validate.
  - CCLDV-BR-089: The expiry day is not editable and is not given the '*' or blank treatment. The new application should carry the original expiry day through unchanged instead of reading it back from the form.
  - CCLDV-BR-090: The expiry day saved with the card is the day held for the edit, unchanged, joined with the new year and month. Take it from the server-side original snapshot, not from a hidden form field, so it cannot be altered.
- [ ] CCLDV-C08-T5 [ui-modernization] Build the screen Card (S-CARD-DETAIL). Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-087, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091, CCLDV-REQ-F-092. Rules: CCLDV-BR-085, CCLDV-BR-086, CCLDV-BR-087, CCLDV-BR-088, CCLDV-BR-089, CCLDV-BR-090, CCLDV-BR-091, CCLDV-BR-092, CCLDV-BR-093, CCLDV-BR-094, CCLDV-BR-095, CCLDV-BR-096, CCLDV-BR-097, CCLDV-BR-098, CCLDV-BR-099, CCLDV-BR-100, CCLDV-BR-101, CCLDV-BR-102, CCLDV-BR-103, CCLDV-BR-104, CCLDV-BR-105, CCLDV-BR-106. After: CCLDV-C08-T2, CCLDV-C08-T3, CCLDV-C08-T4.
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - form "Edit card": Something must change (ignoring upper/lower case): 'No changes to save. The details match the stored values.' (legacy 'No change detected with respect to values fetched.') Errors are reported in the order name, status, expiry month, expiry year.
  - text "Name on card": Required; letters and spaces only. Messages: 'Enter the name on the card.' (legacy 'Card name not provided'), 'Name on card can only contain letters and spaces.' (legacy 'Card name can only contain alphabets and spaces')
  - radio "Status": One must be chosen: 'Choose whether the card is active or inactive.' (legacy 'Card Active Status must be Y or N')
  - select "Expiry month": Required; 1 to 12. Message: 'Card expiry month must be between 1 and 12.'
  - number "Expiry year": Required; 1950 to 2099. Message: 'Enter an expiry year between 1950 and 2099.' (legacy 'Invalid card expiry year')
  - message "Fix the highlighted fields"
  - button "Save changes"
  - button "Discard changes"
  - dialog "Save changes to this card?"
- [ ] CCLDV-C08-T6 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-087, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091, CCLDV-REQ-F-092. Criteria: CCLDV-C08-AC-01, CCLDV-C08-AC-02, CCLDV-C08-AC-03, CCLDV-C08-AC-04, CCLDV-C08-AC-05, CCLDV-C08-AC-06, CCLDV-C08-AC-07, CCLDV-C08-AC-08, CCLDV-C08-AC-09, CCLDV-C08-AC-10, CCLDV-C08-AC-11, CCLDV-C08-AC-12, CCLDV-C08-AC-13, CCLDV-C08-AC-14, CCLDV-C08-AC-15, CCLDV-C08-AC-16, CCLDV-C08-AC-17, CCLDV-C08-AC-18, CCLDV-C08-AC-19, CCLDV-C08-AC-20, CCLDV-C08-AC-21, CCLDV-C08-AC-22, CCLDV-C08-AC-23, CCLDV-C08-AC-24, CCLDV-C08-AC-25, CCLDV-C08-AC-26, CCLDV-C08-AC-27, CCLDV-C08-AC-28, CCLDV-C08-AC-29, CCLDV-C08-AC-30, CCLDV-C08-AC-31, CCLDV-C08-AC-32, CCLDV-C08-AC-33. After: CCLDV-C08-T1, CCLDV-C08-T2, CCLDV-C08-T3, CCLDV-C08-T4, CCLDV-C08-T5.
  - 33 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C08-T7 [compliance] Review the handling of card data, personal data. Requirements: CCLDV-REQ-F-078, CCLDV-REQ-F-079, CCLDV-REQ-F-080, CCLDV-REQ-F-081, CCLDV-REQ-F-082, CCLDV-REQ-F-083, CCLDV-REQ-F-084, CCLDV-REQ-F-085, CCLDV-REQ-F-086, CCLDV-REQ-F-087, CCLDV-REQ-F-088, CCLDV-REQ-F-089, CCLDV-REQ-F-090, CCLDV-REQ-F-091, CCLDV-REQ-F-092. After: CCLDV-C08-T1, CCLDV-C08-T2, CCLDV-C08-T3, CCLDV-C08-T4, CCLDV-C08-T5.
  - Check storage, logs, screens and audit against the rules.
