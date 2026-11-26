# Implementation plan: Send the CardDemo test file by FTP (SOM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. SOM-C04-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: SOM-REQ-F-026, SOM-REQ-F-027_
  - _Rules: SOM-BR-030, SOM-BR-031_
- [ ] 2. SOM-C04-T2 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: SOM-REQ-F-026, SOM-REQ-F-027_
  - _Rules: SOM-BR-030, SOM-BR-031_
  - _After: SOM-C04-T1_
- [ ] 3. SOM-C04-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-026, SOM-REQ-F-027_
  - _Criteria: SOM-C04-AC-01, SOM-C04-AC-02_
  - _After: SOM-C04-T1, SOM-C04-T2_
- [ ] 4. SOM-C04-T4 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: SOM-REQ-F-026, SOM-REQ-F-027_
  - _After: SOM-C04-T1, SOM-C04-T2_
