# Tasks: Change a transaction type description (TTRDM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C17-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-117, TTRDM-REQ-F-118, TTRDM-REQ-F-119, TTRDM-REQ-F-120, TTRDM-REQ-F-121, TTRDM-REQ-F-122, TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-126, TTRDM-REQ-F-127, TTRDM-REQ-F-128, TTRDM-REQ-F-129.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C17-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-117, TTRDM-REQ-F-119, TTRDM-REQ-F-120, TTRDM-REQ-F-121, TTRDM-REQ-F-122, TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-127, TTRDM-REQ-F-128, TTRDM-REQ-F-129. Rules: TTRDM-BR-130, TTRDM-BR-132, TTRDM-BR-133, TTRDM-BR-134, TTRDM-BR-135, TTRDM-BR-136, TTRDM-BR-137, TTRDM-BR-138, TTRDM-BR-139, TTRDM-BR-141, TTRDM-BR-142. After: TTRDM-C17-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C17-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-126. Rules: TTRDM-BR-140. After: TTRDM-C17-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C17-T4 [api] Build the services behind the screens. Requirements: TTRDM-REQ-F-118. Rules: TTRDM-BR-131. After: TTRDM-C17-T1, TTRDM-C17-T2, TTRDM-C17-T3.
  - TTRDM-BR-131: Description input needs normalising before validation and comparison. Remove leading and trailing spaces, and treat an empty value or a lone '*' as 'not supplied' (null). Validation then sees a missing description rather than a literal '*' or blanks.
- [ ] TTRDM-C17-T5 [ui-modernization] Build the screen Transaction type (S-TRANTYPE-EDIT). Requirements: TTRDM-REQ-F-117, TTRDM-REQ-F-118, TTRDM-REQ-F-119, TTRDM-REQ-F-120, TTRDM-REQ-F-121, TTRDM-REQ-F-122, TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-126, TTRDM-REQ-F-127, TTRDM-REQ-F-128, TTRDM-REQ-F-129. Rules: TTRDM-BR-130, TTRDM-BR-131, TTRDM-BR-132, TTRDM-BR-133, TTRDM-BR-134, TTRDM-BR-135, TTRDM-BR-136, TTRDM-BR-137, TTRDM-BR-138, TTRDM-BR-139, TTRDM-BR-140, TTRDM-BR-141, TTRDM-BR-142. After: TTRDM-C17-T2, TTRDM-C17-T3, TTRDM-C17-T4.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - text "Description": Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.')
  - message "No changes": Description must differ from the stored value (ignoring case and surrounding spaces): 'No changes to save.' (legacy 'No change detected with respect to values fetched.')
  - button "Save": Actions not available in the current step are disabled rather than rejected (legacy 'Invalid key pressed').
  - dialog "Save this transaction type?"
  - message "Result"
- [ ] TTRDM-C17-T6 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-117, TTRDM-REQ-F-118, TTRDM-REQ-F-119, TTRDM-REQ-F-120, TTRDM-REQ-F-121, TTRDM-REQ-F-122, TTRDM-REQ-F-123, TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-126, TTRDM-REQ-F-127, TTRDM-REQ-F-128, TTRDM-REQ-F-129. Criteria: TTRDM-C17-AC-01, TTRDM-C17-AC-02, TTRDM-C17-AC-03, TTRDM-C17-AC-04, TTRDM-C17-AC-05, TTRDM-C17-AC-06, TTRDM-C17-AC-07, TTRDM-C17-AC-08, TTRDM-C17-AC-09, TTRDM-C17-AC-10, TTRDM-C17-AC-11, TTRDM-C17-AC-12, TTRDM-C17-AC-13, TTRDM-C17-AC-14. After: TTRDM-C17-T1, TTRDM-C17-T2, TTRDM-C17-T3, TTRDM-C17-T4, TTRDM-C17-T5.
  - 14 acceptance criteria, each a test named by its ID.
