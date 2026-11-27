# Implementation plan: Answer system date requests from the queue (CAFM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C03-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-034, CAFM-REQ-F-035, CAFM-REQ-F-036, CAFM-REQ-F-037, CAFM-REQ-F-038, CAFM-REQ-F-039, CAFM-REQ-F-031_
  - _Rules: CAFM-BR-033, CAFM-BR-036, CAFM-BR-037, CAFM-BR-038, CAFM-BR-039, CAFM-BR-040, CAFM-BR-041_
- [ ] 2. CAFM-C03-T2 [api] Build the services behind the screens
  - CAFM-BR-031: Run the date inquiry as a consumer on the queue whose arrival started it. It always replies on the fixed date reply queue ('CARD.DEMO.REPLY.DATE') and ignores any reply-to queue the requester names.
  - CAFM-BR-032: Process requests one at a time until the queue is empty: wait up to 5 seconds for each, and stop when none arrives. Take a request and send its reply in one transaction, committed before the next request is taken.
  - CAFM-BR-034: Send the reply as a text message in the broker's standard character set, carrying the request's message ID and correlation ID, inside the same transaction that consumed the request.
  - CAFM-BR-035: On shutdown, normal or after an error, release every queue connection that was opened (request, reply and error). Release only the ones that opened successfully, then end the task.
  - _Requirements: CAFM-REQ-F-029, CAFM-REQ-F-030, CAFM-REQ-F-032, CAFM-REQ-F-033_
  - _Rules: CAFM-BR-031, CAFM-BR-032, CAFM-BR-034, CAFM-BR-035_
  - _After: CAFM-C03-T1_
- [ ] 3. CAFM-C03-T3 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-029, CAFM-REQ-F-030, CAFM-REQ-F-031, CAFM-REQ-F-032, CAFM-REQ-F-033, CAFM-REQ-F-034, CAFM-REQ-F-035, CAFM-REQ-F-036, CAFM-REQ-F-037, CAFM-REQ-F-038, CAFM-REQ-F-039_
  - _Criteria: CAFM-C03-AC-01, CAFM-C03-AC-02, CAFM-C03-AC-03, CAFM-C03-AC-04, CAFM-C03-AC-05, CAFM-C03-AC-06, CAFM-C03-AC-07, CAFM-C03-AC-08, CAFM-C03-AC-09, CAFM-C03-AC-10, CAFM-C03-AC-11, CAFM-C03-AC-12, CAFM-C03-AC-13_
  - _After: CAFM-C03-T1, CAFM-C03-T2_
