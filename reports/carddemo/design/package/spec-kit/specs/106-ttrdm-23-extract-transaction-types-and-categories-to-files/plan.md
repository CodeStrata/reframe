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

- TTRDM-BR-163: The first step of the scheduled extract job copies the current transaction type file to a new backup version, under the retention policy set up for these backups, before any new file is produced.
- TTRDM-BR-164: This step runs only if every earlier step of the job succeeded. It copies the current transaction category file to a new backup version. The job needs step-level success tracking so this step can be skipped.
- TTRDM-BR-167: This is a sorted extract of the transaction type table in a fixed-width layout. Each record is the 2-character type code, the description padded to 50 characters, and eight '0' filler characters, 60 characters in total. Downstream readers depend on this exact layout.
- TTRDM-BR-170: This is a sorted extract of the transaction category table in a fixed-width layout. Each record is the type code, the category code, the category description padded to 50 characters, and four '0' filler characters, 60 characters in total.

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

