# Implementation plan: Maintain transaction types in batch (TTRDM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C21-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-146_
  - _Rules: TTRDM-BR-158_
- [ ] 2. TTRDM-C21-T2 [api] Build the scheduled job
  - TTRDM-BR-157: A scheduled or on-demand batch job that reads a request file without taking it exclusively. It connects to the reference data database with the application's own credentials and applies each request to the transaction types table. It writes a per-run log of messages that operations can review. The subsystem and plan names have no counterpart: they become the job's database connection configuration.
  - _Requirements: TTRDM-REQ-F-145_
  - _Rules: TTRDM-BR-157_
  - _After: TTRDM-C21-T1_
- [ ] 3. TTRDM-C21-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-145, TTRDM-REQ-F-146_
  - _Criteria: TTRDM-C21-AC-01, TTRDM-C21-AC-02_
  - _After: TTRDM-C21-T1, TTRDM-C21-T2_
