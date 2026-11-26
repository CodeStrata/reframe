# Implementation plan: Reset the application environment (ADPLM-C18)

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

- ADPLM-BR-125: Reset is an admin operation. It clears the error log, the start-time records and the statistics records, and it rewrites the control record. Only the control record is recreated straight away; the other stores fill again as the application writes to them.
- ADPLM-BR-126: Replace the control record as a whole in one transaction with the header '**** GENAPP CNTL', the 10-digit low customer number and the 10-digit high customer number, so that no reader sees a partly rewritten record.
- ADPLM-BR-127: The legacy writes do not wait for space and never check the result. The new reset should check the write of the control record and report a failure to the operator; the fixed lengths of 20, 23 and 24 characters only matter where the old text format is kept.

## Decision tables

None.
