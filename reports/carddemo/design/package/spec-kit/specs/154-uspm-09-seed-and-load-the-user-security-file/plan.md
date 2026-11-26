# Implementation plan: Seed and load the user security file (USPM-C09)

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

- USPM-BR-100: The seed step should be idempotent: remove any earlier seed data before staging, keep the new staging set only if staging completes, and discard it if staging fails. A transaction or a write-then-rename of the seed file gives this.
- USPM-BR-101: Provide a setup or migration job that drops and recreates the user table keyed on an 8-character User ID, then bulk-loads every staged seed record into it. It runs on demand at environment setup, not as part of normal operation.
- USPM-BR-104: The legacy job also copies the staged records into an entry-sequenced copy of the user file, without regard to whether earlier steps succeeded. The new application needs this only if some consumer reads users in load order. Otherwise one keyed user table covers it, and the copy should be confirmed as unneeded rather than rebuilt.
- USPM-BR-105: The legacy job also copies the staged records into a relative-record (record-number addressed) copy of the user file, without regard to whether earlier steps succeeded. Rebuild this only if some consumer looks users up by position. Otherwise the keyed user table is enough.

## Decision tables

None.
