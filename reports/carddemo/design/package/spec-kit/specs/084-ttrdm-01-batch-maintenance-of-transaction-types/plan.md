# Implementation plan: Batch maintenance of transaction types (TTRDM-C01)

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

None.

## Decision tables

#### Batch record outcome by action code

| Action code | Transaction type code exists | Categories refer to the type | Database accepts the change | Batch result for the record | Rule |
|---|---|---|---|---|---|
| '*' | - | - | - | Show 'IGNORING COMMENTED LINE'; change nothing | TTRDM-BR-002 |
| Other than 'A', 'U', 'D', '*' | - | - | - | Show 'ERROR: TYPE NOT VALID'; return code 4; table unchanged; continue | TTRDM-BR-003 |
| 'A' | - | - | Yes | Add type; show 'RECORD INSERTED SUCCESSFULLY' | TTRDM-BR-004 |
| 'A' | - | - | No (e.g. code already exists, -803) | Show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with code; return code 4; continue | TTRDM-BR-005 |
| 'U' | Yes | - | Yes | Replace description; show 'RECORD UPDATED SUCCESSFULLY' | TTRDM-BR-006 |
| 'U' | No | - | - | Show 'No records found.'; return code 4; continue | TTRDM-BR-007 |
| 'U' | - | - | No (database error) | Show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with code; return code 4; continue | TTRDM-BR-009 |
| 'D' | Yes | No | Yes | Delete type; show 'RECORD DELETED SUCCESSFULLY' | TTRDM-BR-010 |
| 'D' | Yes | Yes | No (refused) | Show 'Error accessing: TRANSACTION_TYPE table. SQLCODE:' with code; return code 4; continue | TTRDM-BR-011 |
| 'D' | No | - | - | Show 'No records found.'; return code 4; continue | TTRDM-BR-008 |
| 'D' | Yes | No | No (other database error) | **Gap:** R1 says any database error gives return code 4, but no rule states the message shown when a delete fails for a reason other than referring categories. | |

