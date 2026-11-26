# Tasks: Find a transaction type to maintain (TTRDM-C16)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C16-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-108, TTRDM-REQ-F-109, TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-114, TTRDM-REQ-F-115, TTRDM-REQ-F-116.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C16-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-115, TTRDM-REQ-F-116. Rules: TTRDM-BR-123, TTRDM-BR-124, TTRDM-BR-125, TTRDM-BR-126, TTRDM-BR-128, TTRDM-BR-129. After: TTRDM-C16-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C16-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-108, TTRDM-REQ-F-114. Rules: TTRDM-BR-121, TTRDM-BR-127. After: TTRDM-C16-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C16-T4 [api] Build the services behind the screens. Requirements: TTRDM-REQ-F-109. Rules: TTRDM-BR-122. After: TTRDM-C16-T1, TTRDM-C16-T2, TTRDM-C16-T3.
  - TTRDM-BR-122: Code validation needs to run before the lookup, as a step in the search action. It applies only when the screen is neither adding a new record nor waiting for confirmation of changes. In those two modes, an Enter press must not re-validate the search code or look it up again.
- [ ] TTRDM-C16-T5 [ui-modernization] Build the screen Transaction type (S-TRANTYPE-EDIT). Requirements: TTRDM-REQ-F-108, TTRDM-REQ-F-109, TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-114, TTRDM-REQ-F-115, TTRDM-REQ-F-116. Rules: TTRDM-BR-121, TTRDM-BR-122, TTRDM-BR-123, TTRDM-BR-124, TTRDM-BR-125, TTRDM-BR-126, TTRDM-BR-127, TTRDM-BR-128, TTRDM-BR-129. After: TTRDM-C16-T2, TTRDM-C16-T3, TTRDM-C16-T4.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - form "Find a transaction type"
  - text "Type code": Required; a number other than zero. Messages: 'Enter a type code.' (legacy 'Tran Type code must be supplied.'), 'Type code must be a number.' (legacy 'Tran Type code must be numeric.'), 'Type code must not be 00.' (legacy 'Tran Type code must not be zero.'). Only the first problem is shown.
  - button "Find"
- [ ] TTRDM-C16-T6 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: TTRDM-REQ-F-108. Rules: TTRDM-BR-121. After: TTRDM-C16-T2, TTRDM-C16-T3, TTRDM-C16-T4.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - link "Maintain a transaction type"
- [ ] TTRDM-C16-T7 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-108, TTRDM-REQ-F-109, TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-114, TTRDM-REQ-F-115, TTRDM-REQ-F-116. Criteria: TTRDM-C16-AC-01, TTRDM-C16-AC-02, TTRDM-C16-AC-03, TTRDM-C16-AC-04, TTRDM-C16-AC-05, TTRDM-C16-AC-06, TTRDM-C16-AC-07, TTRDM-C16-AC-08, TTRDM-C16-AC-09, TTRDM-C16-AC-10, TTRDM-C16-AC-11, TTRDM-C16-AC-12. After: TTRDM-C16-T1, TTRDM-C16-T2, TTRDM-C16-T3, TTRDM-C16-T4, TTRDM-C16-T5, TTRDM-C16-T6.
  - 12 acceptance criteria, each a test named by its ID.
