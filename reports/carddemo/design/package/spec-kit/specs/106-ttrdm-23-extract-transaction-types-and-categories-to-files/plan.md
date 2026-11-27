# Implementation plan: Extract transaction types and categories to files (TTRDM-C23)

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

- TTRDM-BR-163: The extract job's first step copies the current transaction type extract, unchanged and in its 60-character records, into a new version in the versioned transaction type backup location before anything is overwritten.
- TTRDM-BR-164: A conditional job step that runs only when every earlier step succeeded. It copies the current transaction category extract, unchanged and in its 60-character records, into a new version in the category backup location. The orchestrator must skip it after any earlier failure.
- TTRDM-BR-167: A fixed-width writer for the sorted transaction type extract (ordered by type code). Each record has the 2-character type code, the description right-padded with spaces to 50 characters, then the literal '00000000', 60 characters in all. Downstream consumers depend on this exact layout.
- TTRDM-BR-170: A fixed-width writer for the sorted transaction category extract (ordered by type code, then category code). Each record has the type code, the category code, the category description right-padded with spaces to 50 characters, then the literal '0000', 60 characters in all.

## Decision tables

#### Extract job steps by earlier return codes

| Highest return code of earlier steps | Step action | Rule |
|---|---|---|
| 0 | Back up transaction category file | TTRDM-BR-164 |
| 0 | Unload transaction types to new file | TTRDM-BR-166 |
| 0 to 4 | Unload transaction categories to new file | TTRDM-BR-169 |
| Other than 0 | Skip transaction category backup | TTRDM-BR-165 |
| Other than 0 | **Gap:** No rule states what happens to the transaction type unload when an earlier step ended with a non-zero return code. | |
| Above 4 | **Gap:** No rule states explicitly that the transaction category unload is skipped when an earlier step ended above 4. | |

