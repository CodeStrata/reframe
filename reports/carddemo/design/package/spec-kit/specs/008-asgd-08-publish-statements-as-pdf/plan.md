# Implementation plan: Publish statements as PDF (ASGD-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

None found in the source.

## Design notes

- ASGD-BR-039: A scheduled follow-on step that starts when statement creation completes. It renders the plain-text statement report to PDF and stores the result as the published statement document (legacy name AWS.M2.CARDDEMO.STATEMNT.PS.PDF), for example in document storage. Any text-to-PDF renderer works. The legacy job uses the TXT2PDF utility with BROWSE Y.

## Decision tables

None.
