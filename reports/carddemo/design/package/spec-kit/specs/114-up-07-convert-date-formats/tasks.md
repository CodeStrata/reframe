# Tasks: Convert date formats (UP-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C07-T1 [business-rules] Implement the business rules. Requirements: UP-REQ-F-029, UP-REQ-F-031, UP-REQ-F-033. Rules: UP-BR-031, UP-BR-032, UP-BR-034, UP-BR-036.
  - Keep each business rule exactly as specified.
- [ ] UP-C07-T2 [api] Build the scheduled job. Requirements: UP-REQ-F-030, UP-REQ-F-032, UP-REQ-F-034. Rules: UP-BR-033, UP-BR-035, UP-BR-037. After: UP-C07-T1.
  - UP-BR-033: A pure, reusable date-formatting function that takes YYYYMMDD and returns YYYY-MM-DD. Build it as a library function, not a separate service call.
  - UP-BR-035: The same library function going the other way: it takes YYYY-MM-DD and returns YYYYMMDD by position (characters 1-4, 6-7 and 9-10). It does not validate the separators.
  - UP-BR-037: The account extract calls the date-formatting function on the reissue date for every record it writes, so the extract carries the date as YYYYMMDD.
- [ ] UP-C07-T3 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-029, UP-REQ-F-030, UP-REQ-F-031, UP-REQ-F-032, UP-REQ-F-033, UP-REQ-F-034. Criteria: UP-C07-AC-01, UP-C07-AC-02, UP-C07-AC-03, UP-C07-AC-04, UP-C07-AC-05, UP-C07-AC-06. After: UP-C07-T1, UP-C07-T2.
  - 6 acceptance criteria, each a test named by its ID.
