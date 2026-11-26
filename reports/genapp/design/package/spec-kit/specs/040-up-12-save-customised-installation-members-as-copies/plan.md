# Implementation plan: Save customised installation members as copies (UP-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as service.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as service.

## Data model

None found in the source.

## Design notes

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

## Decision tables

#### Name of the saved customised copy

| Member name | Name the customised copy is saved under | Rule |
|---|---|---|
| 'ONCICS' | '#ONCICS', replacing any existing member of that name | UP-BR-115 |
| Any other name | '@' followed by the original member name, replacing any existing member of that name | UP-BR-117 |

