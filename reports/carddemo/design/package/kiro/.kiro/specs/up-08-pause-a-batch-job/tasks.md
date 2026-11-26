# Implementation plan: Pause a batch job (UP-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C08-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-040.
  - _Requirements: UP-REQ-F-037_
  - _Rules: UP-BR-040_
- [ ] 2. UP-C08-T2 [api] Build the scheduled job
  - UP-BR-038: A configurable delay step in the job scheduler or workflow. It reads an 8-digit duration in hundredths of a second (for example 00000500 = 5 seconds), sleeps for that long, and always exits successfully. In most schedulers this is a built-in wait or delay task rather than custom code.
  - UP-BR-039: The timer behind the delay step: suspend for the given number of hundredths of a second and then return success to the caller. A standard sleep in the job runtime covers it.
  - _Requirements: UP-REQ-F-035, UP-REQ-F-036_
  - _Rules: UP-BR-038, UP-BR-039_
  - _After: UP-C08-T1_
- [ ] 3. UP-C08-T3 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-035, UP-REQ-F-036, UP-REQ-F-037_
  - _Criteria: UP-C08-AC-01, UP-C08-AC-02, UP-C08-AC-03, UP-C08-AC-04, UP-C08-AC-05_
  - _After: UP-C08-T1, UP-C08-T2_
