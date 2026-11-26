# Implementation plan: Authorize online transaction under the card security profile (SOM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. SOM-C06-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: SOM-REQ-F-031_
  - _Rules: SOM-BR-035_
- [ ] 2. SOM-C06-T2 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: SOM-REQ-F-031_
  - _Rules: SOM-BR-035_
  - _After: SOM-C06-T1_
- [ ] 3. SOM-C06-T3 [test-generation] Write a test for every acceptance criterion
  - 1 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-031_
  - _Criteria: SOM-C06-AC-01_
  - _After: SOM-C06-T1, SOM-C06-T2_
- [ ] 4. SOM-C06-T4 [compliance] Review the handling of audit, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: SOM-REQ-F-031_
  - _After: SOM-C06-T1, SOM-C06-T2_
