# Implementation plan: Load disclosure group and category balance masters (DTPR-C12)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

No screens: it runs as scheduled job.

## Data model

None found in the source.

## Design notes

- DTPR-BR-074: Make the disclosure group load a full replace: clear or recreate the store, keyed on the 16-character key of group ID, type and category over 50-byte records, before loading. Treat an absent previous store as normal, not an error.
- DTPR-BR-075: Bulk-load every record of the disclosure group feed into the keyed disclosure group store. Load it as one unit (in a single transaction, or by swapping in a staging table) so the interest job never sees a partly loaded rate table.
- DTPR-BR-076: Bulk-load every category balance record from the flat feed into the category balance store, keyed on account ID, type and category. Hold exclusive write access during the load, and schedule it so it never overlaps the posting or interest jobs.

## Decision tables

None.
