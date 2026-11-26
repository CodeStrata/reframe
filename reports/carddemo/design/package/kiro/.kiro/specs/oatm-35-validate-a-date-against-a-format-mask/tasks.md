# Implementation plan: Validate a date against a format mask (OATM-C35)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C35-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-288, OATM-REQ-F-289, OATM-REQ-F-290, OATM-REQ-F-291, OATM-REQ-F-292, OATM-REQ-F-293, OATM-REQ-F-294, OATM-REQ-F-295, OATM-REQ-F-296, OATM-REQ-F-297, OATM-REQ-F-298_
  - _Rules: OATM-BR-305, OATM-BR-306, OATM-BR-307, OATM-BR-308, OATM-BR-309, OATM-BR-310, OATM-BR-311, OATM-BR-312, OATM-BR-313, OATM-BR-314, OATM-BR-315_
- [ ] 2. OATM-C35-T2 [api] Build the service
  - OATM-BR-303: Provide a reusable date-validation function that takes a date string and a format pattern and returns a structured result: a 4-digit severity, a 4-digit message number and a reason. Implement it with the platform's standard strict date parsing, which rejects impossible dates. Map outcomes to the legacy message numbers (2507, 2508, 2509, 2513, 2517, 2518, 2521) where callers depend on them, for example the 2513 exception.
  - OATM-BR-304: Return the result as a structured value (severity, message number, result text, tested date, mask used) with severity as the outcome code. Keep a formatter that renders the legacy 80-character text ('Mesg Code:', 'TstDate:', 'Mask used:') only if a consumer still needs that exact layout.
  - _Requirements: OATM-REQ-F-286, OATM-REQ-F-287_
  - _Rules: OATM-BR-303, OATM-BR-304_
  - _After: OATM-C35-T1_
- [ ] 3. OATM-C35-T3 [test-generation] Write a test for every acceptance criterion
  - 14 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-286, OATM-REQ-F-287, OATM-REQ-F-288, OATM-REQ-F-289, OATM-REQ-F-290, OATM-REQ-F-291, OATM-REQ-F-292, OATM-REQ-F-293, OATM-REQ-F-294, OATM-REQ-F-295, OATM-REQ-F-296, OATM-REQ-F-297, OATM-REQ-F-298_
  - _Criteria: OATM-C35-AC-01, OATM-C35-AC-02, OATM-C35-AC-03, OATM-C35-AC-04, OATM-C35-AC-05, OATM-C35-AC-06, OATM-C35-AC-07, OATM-C35-AC-08, OATM-C35-AC-09, OATM-C35-AC-10, OATM-C35-AC-11, OATM-C35-AC-12, OATM-C35-AC-13, OATM-C35-AC-14_
  - _After: OATM-C35-T1, OATM-C35-T2_
