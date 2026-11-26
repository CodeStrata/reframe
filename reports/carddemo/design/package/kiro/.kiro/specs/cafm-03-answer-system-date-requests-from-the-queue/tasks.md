# Implementation plan: Answer system date requests from the queue (CAFM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C03-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-034, CAFM-REQ-F-035, CAFM-REQ-F-036, CAFM-REQ-F-037, CAFM-REQ-F-038, CAFM-REQ-F-039, CAFM-REQ-F-031_
  - _Rules: CAFM-BR-033, CAFM-BR-036, CAFM-BR-037, CAFM-BR-038, CAFM-BR-039, CAFM-BR-040, CAFM-BR-041_
- [ ] 2. CAFM-C03-T2 [api] Build the services behind the screens
  - CAFM-BR-031: Run the service as a consumer started when messages arrive on the date request queue. Read the request queue name from the start-up event, and always send replies to the fixed queue 'CARD.DEMO.REPLY.DATE'.
  - CAFM-BR-032: Drain the queue: take requests one at a time, commit each read-and-reply as one transaction before taking the next, and stop once no message arrives within 5 seconds.
  - CAFM-BR-034: Publish the reply as a text message to 'CARD.DEMO.REPLY.DATE' with the request's message id and correlation id, inside the same transaction as consuming the request. Ignore any reply-to address the request names.
  - CAFM-BR-035: On shutdown, release every queue connection (request, reply, error) that was opened successfully and leave the others alone, so connections are not leaked across runs.
  - _Requirements: CAFM-REQ-F-029, CAFM-REQ-F-030, CAFM-REQ-F-032, CAFM-REQ-F-033_
  - _Rules: CAFM-BR-031, CAFM-BR-032, CAFM-BR-034, CAFM-BR-035_
  - _After: CAFM-C03-T1_
- [ ] 3. CAFM-C03-T3 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-029, CAFM-REQ-F-030, CAFM-REQ-F-031, CAFM-REQ-F-032, CAFM-REQ-F-033, CAFM-REQ-F-034, CAFM-REQ-F-035, CAFM-REQ-F-036, CAFM-REQ-F-037, CAFM-REQ-F-038, CAFM-REQ-F-039_
  - _Criteria: CAFM-C03-AC-01, CAFM-C03-AC-02, CAFM-C03-AC-03, CAFM-C03-AC-04, CAFM-C03-AC-05, CAFM-C03-AC-06, CAFM-C03-AC-07, CAFM-C03-AC-08, CAFM-C03-AC-09, CAFM-C03-AC-10, CAFM-C03-AC-11, CAFM-C03-AC-12, CAFM-C03-AC-13_
  - _After: CAFM-C03-T1, CAFM-C03-T2_
