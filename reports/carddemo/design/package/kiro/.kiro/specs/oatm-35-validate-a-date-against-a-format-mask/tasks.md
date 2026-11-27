# Implementation plan: Validate a date against a format mask (OATM-C35)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C35-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-288, OATM-REQ-F-289, OATM-REQ-F-290, OATM-REQ-F-291, OATM-REQ-F-292, OATM-REQ-F-293, OATM-REQ-F-294, OATM-REQ-F-295, OATM-REQ-F-296, OATM-REQ-F-297, OATM-REQ-F-298_
  - _Rules: OATM-BR-305, OATM-BR-306, OATM-BR-307, OATM-BR-308, OATM-BR-309, OATM-BR-310, OATM-BR-311, OATM-BR-312, OATM-BR-313, OATM-BR-314, OATM-BR-315_
- [ ] 2. OATM-C35-T2 [api] Build the service
  - OATM-BR-303: Expose date validation as one shared function or service that takes a date string and a format mask and returns a structured result (severity, message code, reason). Implement it with the platform's standard date-parsing library instead of the mainframe date service, and keep the legacy severity/message codes (0000, 2508, 2513 and so on) only as far as callers need them to tell valid from invalid.
  - OATM-BR-304: Callers need a result they can test: a severity/status, a message code, the reason text, and the tested date and mask for diagnostics. A typed result object replaces the fixed 80-character string and the program return code. Keep the layout only if a remaining legacy consumer still reads it.
  - _Requirements: OATM-REQ-F-286, OATM-REQ-F-287_
  - _Rules: OATM-BR-303, OATM-BR-304_
  - _After: OATM-C35-T1_
- [ ] 3. OATM-C35-T3 [test-generation] Write a test for every acceptance criterion
  - 14 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-286, OATM-REQ-F-287, OATM-REQ-F-288, OATM-REQ-F-289, OATM-REQ-F-290, OATM-REQ-F-291, OATM-REQ-F-292, OATM-REQ-F-293, OATM-REQ-F-294, OATM-REQ-F-295, OATM-REQ-F-296, OATM-REQ-F-297, OATM-REQ-F-298_
  - _Criteria: OATM-C35-AC-01, OATM-C35-AC-02, OATM-C35-AC-03, OATM-C35-AC-04, OATM-C35-AC-05, OATM-C35-AC-06, OATM-C35-AC-07, OATM-C35-AC-08, OATM-C35-AC-09, OATM-C35-AC-10, OATM-C35-AC-11, OATM-C35-AC-12, OATM-C35-AC-13, OATM-C35-AC-14_
  - _After: OATM-C35-T1, OATM-C35-T2_
