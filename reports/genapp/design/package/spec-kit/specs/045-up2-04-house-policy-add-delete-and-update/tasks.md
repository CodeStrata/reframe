# Tasks: House policy add, delete and update (UP2-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP2-C04-T1 [data] Model the data the capability reads and writes. Requirements: UP2-REQ-F-045, UP2-REQ-F-046, UP2-REQ-F-047, UP2-REQ-F-048, UP2-REQ-F-049, UP2-REQ-F-050, UP2-REQ-F-051, UP2-REQ-F-052, UP2-REQ-F-053.
  - Working records it passes or builds: LGCMAREA.
- [ ] UP2-C04-T2 [business-rules] Implement the business rules. Requirements: UP2-REQ-F-045, UP2-REQ-F-048, UP2-REQ-F-050, UP2-REQ-F-051. Rules: UP2-BR-029, UP2-BR-038, UP2-BR-041, UP2-BR-043. After: UP2-C04-T1.
  - Keep each business rule exactly as specified.
- [ ] UP2-C04-T3 [business-rules] Implement error handling and messages. Requirements: UP2-REQ-F-047, UP2-REQ-F-049, UP2-REQ-F-052, UP2-REQ-F-053, UP2-REQ-F-046. Rules: UP2-BR-039, UP2-BR-040, UP2-BR-042, UP2-BR-044. After: UP2-C04-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP2-C04-T4 [ui-modernization] Build the screen Find policies (S-POLICY-FIND). Requirements: UP2-REQ-F-045. Rules: UP2-BR-029, UP2-BR-038. After: UP2-C04-T2, UP2-C04-T3.
  - To the prototype: ui-reference/index.html#/S-POLICY-FIND.
  - button "New house policy"
- [ ] UP2-C04-T5 [ui-modernization] Build the screen Life (endowment) policy (S-LIFE-POLICY). Requirements: UP2-REQ-F-045, UP2-REQ-F-050. Rules: UP2-BR-029, UP2-BR-038, UP2-BR-043. After: UP2-C04-T2, UP2-C04-T3.
  - To the prototype: ui-reference/index.html#/S-LIFE-POLICY.
  - button "Add life policy"
  - button "Save changes"
- [ ] UP2-C04-T6 [ui-modernization] Build the screen House policy (S-HOUSE-POLICY). Requirements: UP2-REQ-F-045, UP2-REQ-F-046, UP2-REQ-F-047, UP2-REQ-F-048, UP2-REQ-F-049, UP2-REQ-F-050, UP2-REQ-F-051, UP2-REQ-F-052, UP2-REQ-F-053. Rules: UP2-BR-029, UP2-BR-038, UP2-BR-039, UP2-BR-040, UP2-BR-041, UP2-BR-042, UP2-BR-043, UP2-BR-044. After: UP2-C04-T2, UP2-C04-T3.
  - To the prototype: ui-reference/index.html#/S-HOUSE-POLICY.
  - button "Add house policy"
  - button "Save changes"
  - button "Delete house policy"
  - dialog "Delete this policy?"
  - message "Result"
- [ ] UP2-C04-T7 [test-generation] Write a test for every acceptance criterion. Requirements: UP2-REQ-F-045, UP2-REQ-F-046, UP2-REQ-F-047, UP2-REQ-F-048, UP2-REQ-F-049, UP2-REQ-F-050, UP2-REQ-F-051, UP2-REQ-F-052, UP2-REQ-F-053. Criteria: UP2-C04-AC-01, UP2-C04-AC-02, UP2-C04-AC-03, UP2-C04-AC-04, UP2-C04-AC-05, UP2-C04-AC-06, UP2-C04-AC-07, UP2-C04-AC-08, UP2-C04-AC-09, UP2-C04-AC-10. After: UP2-C04-T1, UP2-C04-T2, UP2-C04-T3, UP2-C04-T4, UP2-C04-T5, UP2-C04-T6.
  - 10 acceptance criteria, each a test named by its ID.
- [ ] UP2-C04-T8 [compliance] Review the handling of money. Requirements: UP2-REQ-F-045, UP2-REQ-F-046, UP2-REQ-F-047, UP2-REQ-F-048, UP2-REQ-F-049, UP2-REQ-F-050, UP2-REQ-F-051, UP2-REQ-F-052, UP2-REQ-F-053. After: UP2-C04-T1, UP2-C04-T2, UP2-C04-T3, UP2-C04-T4, UP2-C04-T5, UP2-C04-T6.
  - Check storage, logs, screens and audit against the rules.
