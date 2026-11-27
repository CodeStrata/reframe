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

- USPM-BR-100: The seed step must be repeatable. Remove any previous staged seed set first, keep the new one only if staging finishes successfully, and discard it if staging fails. A transactional load or a temporary table swapped in on success meets this.
- USPM-BR-101: Recreate the user store from scratch, with the user ID (8 characters) as its unique primary key, then bulk-insert every staged seed record into it. This is a full reset, not a merge.
- USPM-BR-104: The legacy job also copies the staged records, in arrival order, into an entry-sequenced copy of the user security file, whatever happened in earlier steps. The new application needs this only if something reads users in insertion order. Otherwise one keyed user store is enough. Confirm with the owner before building a second copy.
- USPM-BR-105: The legacy job also copies the staged records into a relative-record (slot-numbered) copy of the user security file, whatever happened in earlier steps. The new application needs this only if a consumer looks users up by record number. Otherwise the keyed user store covers it. Confirm with the owner before building it.

## Decision tables

None.
