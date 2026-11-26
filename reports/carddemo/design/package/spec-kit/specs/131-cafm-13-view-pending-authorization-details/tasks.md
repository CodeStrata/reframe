# Tasks: View pending authorization details (CAFM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C13-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126.
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
- [ ] CAFM-C13-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-115, CAFM-REQ-F-121, CAFM-REQ-F-122. Rules: CAFM-BR-121, CAFM-BR-122, CAFM-BR-123, CAFM-BR-129, CAFM-BR-130. After: CAFM-C13-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C13-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120. Rules: CAFM-BR-124, CAFM-BR-125, CAFM-BR-126, CAFM-BR-127, CAFM-BR-128, CAFM-BR-132, CAFM-BR-133, CAFM-BR-134. After: CAFM-C13-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C13-T4 [api] Build the services behind the screens. Requirements: CAFM-REQ-F-123. Rules: CAFM-BR-131. After: CAFM-C13-T1, CAFM-C13-T2, CAFM-C13-T3.
  - CAFM-BR-131: Retrieval is two keyed lookups, one after the other: first the account's pending authorization summary by account id, then, only if that is found, the authorization detail under that account by the selected authorization key. The new store needs the account to own its authorizations (for example a summary keyed by account id with details keyed by account id plus authorization key), so a detail can never be fetched for an account that has no summary. A missing summary or detail is treated as 'nothing to show', not as an error.
- [ ] CAFM-C13-T5 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS). Requirements: CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126. Rules: CAFM-BR-121, CAFM-BR-122, CAFM-BR-123, CAFM-BR-124, CAFM-BR-125, CAFM-BR-126, CAFM-BR-127, CAFM-BR-128, CAFM-BR-129, CAFM-BR-130, CAFM-BR-131, CAFM-BR-132, CAFM-BR-133, CAFM-BR-134. After: CAFM-C13-T2, CAFM-C13-T3, CAFM-C13-T4.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **summary card** "Authorization": Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed.
  - **summary card** "Merchant"
  - **status badge** "Fraud status"
- [ ] CAFM-C13-T6 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126. Criteria: CAFM-C13-AC-01, CAFM-C13-AC-02, CAFM-C13-AC-03, CAFM-C13-AC-04, CAFM-C13-AC-05, CAFM-C13-AC-06, CAFM-C13-AC-07, CAFM-C13-AC-08, CAFM-C13-AC-09, CAFM-C13-AC-10, CAFM-C13-AC-11, CAFM-C13-AC-12, CAFM-C13-AC-13, CAFM-C13-AC-14, CAFM-C13-AC-15. After: CAFM-C13-T1, CAFM-C13-T2, CAFM-C13-T3, CAFM-C13-T4, CAFM-C13-T5.
  - 15 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C13-T7 [compliance] Review the handling of card data, money. Requirements: CAFM-REQ-F-115, CAFM-REQ-F-116, CAFM-REQ-F-117, CAFM-REQ-F-118, CAFM-REQ-F-119, CAFM-REQ-F-120, CAFM-REQ-F-121, CAFM-REQ-F-122, CAFM-REQ-F-123, CAFM-REQ-F-124, CAFM-REQ-F-125, CAFM-REQ-F-126. After: CAFM-C13-T1, CAFM-C13-T2, CAFM-C13-T3, CAFM-C13-T4, CAFM-C13-T5.
  - Check storage, logs, screens and audit against the rules.
