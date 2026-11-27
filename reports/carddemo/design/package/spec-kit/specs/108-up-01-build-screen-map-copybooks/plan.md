# Implementation plan: Build screen map copybooks (UP-C01)

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

- UP-BR-001: A build-pipeline step that generates the screen's field-layout (view model / DTO) definition from the screen source. It produces only that definition, not an executable artefact. In the new stack this belongs in the UI build or code generation, not in a runtime job.
- UP-BR-002: Write the generated layout to the shared source location under the screen's name, replacing the previous version atomically so nothing else writes it at the same time. Keep the build log or listing as a build artefact named after the screen.

## Decision tables

None.
