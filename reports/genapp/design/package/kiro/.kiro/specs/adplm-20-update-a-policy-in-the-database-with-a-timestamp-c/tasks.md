# Implementation plan: Update a policy in the database with a timestamp check (ADPLM-C20)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C20-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: ADPLM-REQ-F-126, ADPLM-REQ-F-127, ADPLM-REQ-F-128, ADPLM-REQ-F-129, ADPLM-REQ-F-130, ADPLM-REQ-F-131, ADPLM-REQ-F-132, ADPLM-REQ-F-133, ADPLM-REQ-F-134, ADPLM-REQ-F-135, ADPLM-REQ-F-136, ADPLM-REQ-F-137, ADPLM-REQ-F-138, ADPLM-REQ-F-139, ADPLM-REQ-F-140, ADPLM-REQ-F-141, ADPLM-REQ-F-142, ADPLM-REQ-F-143_
- [ ] 2. ADPLM-C20-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: ADPLM-BR-153.
  - _Requirements: ADPLM-REQ-F-128, ADPLM-REQ-F-129, ADPLM-REQ-F-130, ADPLM-REQ-F-131, ADPLM-REQ-F-135, ADPLM-REQ-F-139, ADPLM-REQ-F-142, ADPLM-REQ-F-138_
  - _Rules: ADPLM-BR-138, ADPLM-BR-139, ADPLM-BR-140, ADPLM-BR-141, ADPLM-BR-142, ADPLM-BR-143, ADPLM-BR-144, ADPLM-BR-150, ADPLM-BR-153, ADPLM-BR-154, ADPLM-BR-157, ADPLM-BR-158_
  - _After: ADPLM-C20-T1_
- [ ] 3. ADPLM-C20-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ADPLM-REQ-F-126, ADPLM-REQ-F-132, ADPLM-REQ-F-133, ADPLM-REQ-F-134, ADPLM-REQ-F-137, ADPLM-REQ-F-140, ADPLM-REQ-F-141, ADPLM-REQ-F-143_
  - _Rules: ADPLM-BR-136, ADPLM-BR-145, ADPLM-BR-146, ADPLM-BR-147, ADPLM-BR-148, ADPLM-BR-149, ADPLM-BR-152, ADPLM-BR-155, ADPLM-BR-156, ADPLM-BR-159_
  - _After: ADPLM-C20-T1_
- [ ] 4. ADPLM-C20-T4 [api] Build the scheduled job
  - ADPLM-BR-137: Start every update with outcome '00'. Find the policy by a keyed lookup on customer number plus policy number, and read it inside the same transaction as the update.
  - ADPLM-BR-151: After the update, read the new last-changed timestamp, keyed by policy number, or take it from the update's RETURNING clause, and put it in the response so that the caller can make its next change.
  - _Requirements: ADPLM-REQ-F-127, ADPLM-REQ-F-136_
  - _Rules: ADPLM-BR-137, ADPLM-BR-151_
  - _After: ADPLM-C20-T1, ADPLM-C20-T2, ADPLM-C20-T3_
- [ ] 5. ADPLM-C20-T5 [test-generation] Write a test for every acceptance criterion
  - 25 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-126, ADPLM-REQ-F-127, ADPLM-REQ-F-128, ADPLM-REQ-F-129, ADPLM-REQ-F-130, ADPLM-REQ-F-131, ADPLM-REQ-F-132, ADPLM-REQ-F-133, ADPLM-REQ-F-134, ADPLM-REQ-F-135, ADPLM-REQ-F-136, ADPLM-REQ-F-137, ADPLM-REQ-F-138, ADPLM-REQ-F-139, ADPLM-REQ-F-140, ADPLM-REQ-F-141, ADPLM-REQ-F-142, ADPLM-REQ-F-143_
  - _Criteria: ADPLM-C20-AC-01, ADPLM-C20-AC-02, ADPLM-C20-AC-03, ADPLM-C20-AC-04, ADPLM-C20-AC-05, ADPLM-C20-AC-06, ADPLM-C20-AC-07, ADPLM-C20-AC-08, ADPLM-C20-AC-09, ADPLM-C20-AC-10, ADPLM-C20-AC-11, ADPLM-C20-AC-12, ADPLM-C20-AC-13, ADPLM-C20-AC-14, ADPLM-C20-AC-15, ADPLM-C20-AC-16, ADPLM-C20-AC-17, ADPLM-C20-AC-18, ADPLM-C20-AC-19, ADPLM-C20-AC-20, ADPLM-C20-AC-21, ADPLM-C20-AC-22, ADPLM-C20-AC-23, ADPLM-C20-AC-24, ADPLM-C20-AC-25_
  - _After: ADPLM-C20-T1, ADPLM-C20-T2, ADPLM-C20-T3, ADPLM-C20-T4_
- [ ] 6. ADPLM-C20-T6 [compliance] Review the handling of audit, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-126, ADPLM-REQ-F-127, ADPLM-REQ-F-128, ADPLM-REQ-F-129, ADPLM-REQ-F-130, ADPLM-REQ-F-131, ADPLM-REQ-F-132, ADPLM-REQ-F-133, ADPLM-REQ-F-134, ADPLM-REQ-F-135, ADPLM-REQ-F-136, ADPLM-REQ-F-137, ADPLM-REQ-F-138, ADPLM-REQ-F-139, ADPLM-REQ-F-140, ADPLM-REQ-F-141, ADPLM-REQ-F-142, ADPLM-REQ-F-143_
  - _After: ADPLM-C20-T1, ADPLM-C20-T2, ADPLM-C20-T3, ADPLM-C20-T4_
