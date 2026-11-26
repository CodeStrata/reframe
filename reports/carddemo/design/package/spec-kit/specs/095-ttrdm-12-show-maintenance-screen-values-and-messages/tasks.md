# Tasks: Show maintenance screen values and messages (TTRDM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C12-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097, TTRDM-REQ-F-098, TTRDM-REQ-F-099.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C12-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-098. Rules: TTRDM-BR-109. After: TTRDM-C12-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C12-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097. Rules: TTRDM-BR-093, TTRDM-BR-103, TTRDM-BR-104, TTRDM-BR-105, TTRDM-BR-106, TTRDM-BR-107, TTRDM-BR-108. After: TTRDM-C12-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C12-T4 [api] Build the services behind the screens. Requirements: TTRDM-REQ-F-099. Rules: TTRDM-BR-110, TTRDM-BR-111. After: TTRDM-C12-T1, TTRDM-C12-T2, TTRDM-C12-T3.
  - TTRDM-BR-110: The maintenance screen handler has a default path for actions without a dedicated handler (exit, first entry, delete, save, cancel, or a key not allowed in the current state): bind the posted form, validate it, work out the next state, and render the screen again.
  - TTRDM-BR-111: Route each request on the pair (action pressed, current screen state). Any pair without a specific handler falls through to the default: bind and validate the input, decide the next action, render again. A state machine with an explicit fallback transition is the natural way to build this.
- [ ] TTRDM-C12-T5 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST). Requirements: TTRDM-REQ-F-095. Rules: TTRDM-BR-106. After: TTRDM-C12-T2, TTRDM-C12-T3, TTRDM-C12-T4.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - table "Transaction types"
- [ ] TTRDM-C12-T6 [ui-modernization] Build the screen Transaction type (S-TRANTYPE-EDIT). Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097, TTRDM-REQ-F-098, TTRDM-REQ-F-099. Rules: TTRDM-BR-093, TTRDM-BR-103, TTRDM-BR-104, TTRDM-BR-105, TTRDM-BR-106, TTRDM-BR-107, TTRDM-BR-108, TTRDM-BR-109, TTRDM-BR-110, TTRDM-BR-111. After: TTRDM-C12-T2, TTRDM-C12-T3, TTRDM-C12-T4.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - form "Find a transaction type"
  - text "Description": Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.')
  - button "Save": Actions not available in the current step are disabled rather than rejected (legacy 'Invalid key pressed').
  - button "Cancel"
- [ ] TTRDM-C12-T7 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097, TTRDM-REQ-F-098, TTRDM-REQ-F-099. Criteria: TTRDM-C12-AC-01, TTRDM-C12-AC-02, TTRDM-C12-AC-03, TTRDM-C12-AC-04, TTRDM-C12-AC-05, TTRDM-C12-AC-06, TTRDM-C12-AC-07, TTRDM-C12-AC-08, TTRDM-C12-AC-09, TTRDM-C12-AC-10, TTRDM-C12-AC-11, TTRDM-C12-AC-12. After: TTRDM-C12-T1, TTRDM-C12-T2, TTRDM-C12-T3, TTRDM-C12-T4, TTRDM-C12-T5, TTRDM-C12-T6.
  - 12 acceptance criteria, each a test named by its ID.
