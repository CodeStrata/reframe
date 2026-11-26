# Implementation plan: Save customised installation members as copies (UP-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C12-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-079, UP-BR-080, UP-BR-081, UP-BR-082, UP-BR-083, UP-BR-084, UP-BR-085, UP-BR-086, UP-BR-087, UP-BR-088, UP-BR-089, UP-BR-090, UP-BR-117, UP-BR-118.
  - _Requirements: UP-REQ-F-094_
  - _Rules: UP-BR-079, UP-BR-080, UP-BR-081, UP-BR-082, UP-BR-083, UP-BR-084, UP-BR-085, UP-BR-086, UP-BR-087, UP-BR-088, UP-BR-089, UP-BR-090, UP-BR-117, UP-BR-118_
- [ ] 2. UP-C12-T2 [api] Build the service
  - UP-BR-115: When the template being customised is named 'ONCICS', its customised text is saved as a new output named '#ONCICS'.
  - UP-BR-116: The whole customised text of 'ONCICS' is written as '#ONCICS' and overwrites any earlier output of that name, so the customisation can be re-run.
  - UP-BR-117: Every template other than 'ONCICS' is saved as a new output named '@' followed by the template name.
  - UP-BR-118: The whole customised text of every other template is written under the '@'-prefixed name and overwrites any earlier output of that name, so the customisation can be re-run.
  - UP-BR-080: After '<LOADX>' has been replaced with the load library name, the result is saved only as the customised copy, never back into the template.
  - UP-BR-081: After '<AORSYSID>' has been replaced with the application-owning region system identifier, the result is saved only as the customised copy, never back into the template.
  - UP-BR-082: After '<DB2RUN>' has been replaced with the database run library value, the result is saved only as the customised copy, never back into the template.
  - UP-BR-083: After '<TORAPPL>' has been replaced with the terminal-owning region application identifier, the result is saved only as the customised copy, never back into the template.
  - UP-BR-084: After '<SOURCEX>' has been replaced with the source library name, the result is saved only as the customised copy, never back into the template.
  - UP-BR-085: After '<TORSYSID>' has been replaced with the terminal-owning region system identifier, the result is saved only as the customised copy, never back into the template.
  - UP-BR-086: After '<ZFSHOME>' has been replaced with the file-system home directory, the result is saved only as the customised copy, never back into the template.
  - UP-BR-087: After '<DB2DBID>' has been replaced with the database name, the result is saved only as the customised copy, never back into the template.
  - UP-BR-088: After '<WSIMMSX>' has been replaced with the message-text library name, the result is saved only as the customised copy, never back into the template.
  - UP-BR-089: After '<DORAPPL>' has been replaced with the data-owning region application identifier, the result is saved only as the customised copy, never back into the template.
  - UP-BR-090: After '<CICSHLQ>' has been replaced with the transaction-server library prefix, the result is saved only as the customised copy, never back into the template.
  - UP-BR-119: The shipped template is never modified. Substitutions are made on a working copy, which is discarded once the customised output has been saved under its prefixed name.
  - UP-BR-120: After the customised copy is saved, the working edits are discarded, so the original template stays exactly as shipped and can be customised again.
  - _Requirements: UP-REQ-F-093, UP-REQ-F-095_
  - _Rules: UP-BR-115, UP-BR-116, UP-BR-119, UP-BR-120_
  - _After: UP-C12-T1_
- [ ] 3. UP-C12-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-093, UP-REQ-F-094, UP-REQ-F-095_
  - _Criteria: UP-C12-AC-01, UP-C12-AC-02, UP-C12-AC-03_
  - _After: UP-C12-T1, UP-C12-T2_
