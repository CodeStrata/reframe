# Tasks: Answer account inquiry requests from the queue (CAFM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C02-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-014, CAFM-REQ-F-015, CAFM-REQ-N-002, CAFM-REQ-F-016, CAFM-REQ-F-017, CAFM-REQ-F-018, CAFM-REQ-F-019, CAFM-REQ-F-020, CAFM-REQ-F-021, CAFM-REQ-F-022, CAFM-REQ-F-023, CAFM-REQ-F-024, CAFM-REQ-F-025, CAFM-REQ-F-026, CAFM-REQ-F-027, CAFM-REQ-F-028.
  - File records: CVACT01Y (see data-contracts.md).
- [ ] CAFM-C02-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-015, CAFM-REQ-F-020, CAFM-REQ-F-021, CAFM-REQ-F-024, CAFM-REQ-F-017. Rules: CAFM-BR-014, CAFM-BR-017, CAFM-BR-019, CAFM-BR-020, CAFM-BR-021, CAFM-BR-024. After: CAFM-C02-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CAFM-BR-017.
- [ ] CAFM-C02-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-025, CAFM-REQ-F-026, CAFM-REQ-F-027, CAFM-REQ-F-028, CAFM-REQ-F-022, CAFM-REQ-F-023. Rules: CAFM-BR-022, CAFM-BR-023, CAFM-BR-025, CAFM-BR-026, CAFM-BR-027, CAFM-BR-028, CAFM-BR-029, CAFM-BR-030. After: CAFM-C02-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C02-T4 [api] Build the services behind the screens. Requirements: CAFM-REQ-F-014, CAFM-REQ-N-002, CAFM-REQ-F-016, CAFM-REQ-F-018, CAFM-REQ-F-019. Rules: CAFM-BR-013, CAFM-BR-015, CAFM-BR-016, CAFM-BR-018. After: CAFM-C02-T1, CAFM-C02-T2, CAFM-C02-T3.
  - CAFM-BR-013: Run the service as a consumer started when messages arrive on the account inquiry request queue. Take the request queue from the start-up event or configuration, and send replies to the fixed queue 'CARD.DEMO.REPLY.ACCT' and error records to 'CARD.DEMO.ERROR'.
  - CAFM-BR-015: Treat consuming one request and publishing its reply as one transaction, committed before the next request is taken. A failure then never loses a request or sends a reply twice, and the last request's transaction is committed when the consumer stops.
  - CAFM-BR-016: Parse each request as fixed-position text: characters 1-4 are the function code and the next 11 digits are the account number. Keep the message id and correlation id so the reply can be matched to the request.
  - CAFM-BR-018: Publish each reply to 'CARD.DEMO.REPLY.ACCT' with the request's message id and correlation id, so the requester can match it. If the publish fails, record 'MQPUT ERR', send the error to the error queue and stop the consumer.
- [ ] CAFM-C02-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-014, CAFM-REQ-F-015, CAFM-REQ-N-002, CAFM-REQ-F-016, CAFM-REQ-F-017, CAFM-REQ-F-018, CAFM-REQ-F-019, CAFM-REQ-F-020, CAFM-REQ-F-021, CAFM-REQ-F-022, CAFM-REQ-F-023, CAFM-REQ-F-024, CAFM-REQ-F-025, CAFM-REQ-F-026, CAFM-REQ-F-027, CAFM-REQ-F-028. Criteria: CAFM-C02-AC-01, CAFM-C02-AC-02, CAFM-C02-AC-03, CAFM-C02-AC-04, CAFM-C02-AC-05, CAFM-C02-AC-06, CAFM-C02-AC-07, CAFM-C02-AC-08, CAFM-C02-AC-09, CAFM-C02-AC-10, CAFM-C02-AC-11, CAFM-C02-AC-12, CAFM-C02-AC-13, CAFM-C02-AC-14, CAFM-C02-AC-15, CAFM-C02-AC-16, CAFM-C02-AC-17, CAFM-C02-AC-18, CAFM-C02-AC-19, CAFM-C02-AC-20. After: CAFM-C02-T1, CAFM-C02-T2, CAFM-C02-T3, CAFM-C02-T4.
  - 20 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C02-T6 [compliance] Review the handling of money. Requirements: CAFM-REQ-F-014, CAFM-REQ-F-015, CAFM-REQ-N-002, CAFM-REQ-F-016, CAFM-REQ-F-017, CAFM-REQ-F-018, CAFM-REQ-F-019, CAFM-REQ-F-020, CAFM-REQ-F-021, CAFM-REQ-F-022, CAFM-REQ-F-023, CAFM-REQ-F-024, CAFM-REQ-F-025, CAFM-REQ-F-026, CAFM-REQ-F-027, CAFM-REQ-F-028. After: CAFM-C02-T1, CAFM-C02-T2, CAFM-C02-T3, CAFM-C02-T4.
  - Check storage, logs, screens and audit against the rules.
