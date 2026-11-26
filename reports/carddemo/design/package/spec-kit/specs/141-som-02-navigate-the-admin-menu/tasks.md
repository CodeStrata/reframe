# Tasks: Navigate the Admin Menu (SOM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] SOM-C02-T1 [data] Model the data the capability reads and writes. Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001.
  - Working records it passes or builds: COADM02Y, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSUSR01Y.
- [ ] SOM-C02-T2 [business-rules] Implement the business rules. Requirements: SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-N-001, SOM-REQ-F-011. Rules: SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-010, SOM-BR-012, SOM-BR-013. After: SOM-C02-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: SOM-BR-012.
- [ ] SOM-C02-T3 [business-rules] Implement error handling and messages. Requirements: SOM-REQ-F-010, SOM-REQ-F-004, SOM-REQ-F-005. Rules: SOM-BR-004, SOM-BR-005, SOM-BR-011. After: SOM-C02-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] SOM-C02-T4 [ui-modernization] Build the screen Home (S-HOME). Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011. Rules: SOM-BR-004, SOM-BR-005, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-010, SOM-BR-011, SOM-BR-012. After: SOM-C02-T2, SOM-C02-T3.
  - To the prototype: ui-reference/index.html#/S-HOME.
  - **data table** "Functions": Only the functions the role may use are listed, so the 'Please enter a valid option number...' error cannot happen. If a regular user still reaches an administrator function, the server refuses it with 'No access - Admin Only option... '. A coming-soon row opens nothing and says 'This option <name> is coming soon ...'. A function that is not installed opens nothing and says 'This option <name> is not installed...'. Only Enter and click act on a row, so the 'Invalid key pressed. Please see below...' message is no longer needed.
  - **status badge** "Availability"
- [ ] SOM-C02-T5 [ui-modernization] Build the screen CardDemo header and navigation (S-APP-HEADER). Requirements: SOM-REQ-N-001. Rules: SOM-BR-013. After: SOM-C02-T2, SOM-C02-T3.
  - To the prototype: ui-reference/index.html#/S-APP-HEADER.
  - **data table** "Navigation": Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home.
- [ ] SOM-C02-T6 [test-generation] Write a test for every acceptance criterion. Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001. Criteria: SOM-C02-AC-01, SOM-C02-AC-02, SOM-C02-AC-03, SOM-C02-AC-04, SOM-C02-AC-05, SOM-C02-AC-06, SOM-C02-AC-07, SOM-C02-AC-08, SOM-C02-AC-09, SOM-C02-AC-10, SOM-C02-AC-11, SOM-C02-AC-12, SOM-C02-AC-13, SOM-C02-AC-14, SOM-C02-AC-15. After: SOM-C02-T1, SOM-C02-T2, SOM-C02-T3, SOM-C02-T4, SOM-C02-T5.
  - 15 acceptance criteria, each a test named by its ID.
- [ ] SOM-C02-T7 [compliance] Review the handling of security. Requirements: SOM-REQ-F-004, SOM-REQ-F-005, SOM-REQ-F-006, SOM-REQ-F-007, SOM-REQ-F-008, SOM-REQ-F-009, SOM-REQ-F-010, SOM-REQ-F-011, SOM-REQ-N-001. After: SOM-C02-T1, SOM-C02-T2, SOM-C02-T3, SOM-C02-T4, SOM-C02-T5.
  - Check storage, logs, screens and audit against the rules.
