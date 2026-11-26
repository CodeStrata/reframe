# Tasks: Pick a customer number within the control range (ADPLM-C16)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C16-T1 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-096, ADPLM-REQ-F-097, ADPLM-REQ-F-101. Rules: ADPLM-BR-103, ADPLM-BR-104, ADPLM-BR-108.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C16-T2 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-102, ADPLM-REQ-F-103. Rules: ADPLM-BR-109, ADPLM-BR-110.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C16-T3 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-092, ADPLM-REQ-F-093, ADPLM-REQ-F-094, ADPLM-REQ-F-095, ADPLM-REQ-F-098, ADPLM-REQ-F-099, ADPLM-REQ-F-100, ADPLM-REQ-F-104. Rules: ADPLM-BR-100, ADPLM-BR-101, ADPLM-BR-102, ADPLM-BR-105, ADPLM-BR-106, ADPLM-BR-107, ADPLM-BR-111. After: ADPLM-C16-T1, ADPLM-C16-T2.
  - ADPLM-BR-100: Expose one operation that two callers share: a service call that returns the result in its response, and an interactive or terminal entry point that shows the result. Choose the presentation by the entry point, not by checking a start code at run time.
  - ADPLM-BR-101: The customer range starts at 1000001 to 1000001 before the control record is read. Reading and repairing the control record must be serialized with an exclusive lock, such as a row lock or a lock held for the transaction, and the lock must be released before the random customer is chosen.
  - ADPLM-BR-102: Store the control data as a small configuration record with a header, a low customer and a high customer, instead of an ordered queue. If the record is absent, treat all three entries as missing. If it is present, read every entry.
  - ADPLM-BR-105: If the header is missing, write the header marker '**** GENAPP CNTL' as part of the same locked repair of the control record.
  - ADPLM-BR-106: If the low customer value is missing, store it as the low end of the range in use, a 10-digit zero-padded number (0001000001 by default), within the same locked repair.
  - ADPLM-BR-107: If the high customer value is missing, store it as the high end of the range in use, a 10-digit zero-padded number (0001000001 by default), within the same locked repair.
  - ADPLM-BR-111: For service callers, return a response that holds only the label 'HIGH CUSTOMER=' and the chosen 10-digit customer number, with no data left over from the request.
- [ ] ADPLM-C16-T4 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-092, ADPLM-REQ-F-093, ADPLM-REQ-F-094, ADPLM-REQ-F-095, ADPLM-REQ-F-096, ADPLM-REQ-F-097, ADPLM-REQ-F-098, ADPLM-REQ-F-099, ADPLM-REQ-F-100, ADPLM-REQ-F-101, ADPLM-REQ-F-102, ADPLM-REQ-F-103, ADPLM-REQ-F-104. Criteria: ADPLM-C16-AC-01, ADPLM-C16-AC-02, ADPLM-C16-AC-03, ADPLM-C16-AC-04, ADPLM-C16-AC-05, ADPLM-C16-AC-06, ADPLM-C16-AC-07, ADPLM-C16-AC-08, ADPLM-C16-AC-09, ADPLM-C16-AC-10, ADPLM-C16-AC-11, ADPLM-C16-AC-12. After: ADPLM-C16-T1, ADPLM-C16-T2, ADPLM-C16-T3.
  - 12 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C16-T5 [compliance] Review the handling of personal data. Requirements: ADPLM-REQ-F-092, ADPLM-REQ-F-093, ADPLM-REQ-F-094, ADPLM-REQ-F-095, ADPLM-REQ-F-096, ADPLM-REQ-F-097, ADPLM-REQ-F-098, ADPLM-REQ-F-099, ADPLM-REQ-F-100, ADPLM-REQ-F-101, ADPLM-REQ-F-102, ADPLM-REQ-F-103, ADPLM-REQ-F-104. After: ADPLM-C16-T1, ADPLM-C16-T2, ADPLM-C16-T3.
  - Check storage, logs, screens and audit against the rules.
