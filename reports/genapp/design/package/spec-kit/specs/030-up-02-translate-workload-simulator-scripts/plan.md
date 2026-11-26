# Implementation plan: Translate workload simulator scripts (UP-C02)

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

- UP-BR-003: One independent step of the translation job translates script 'WSC1I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-004: One independent step of the translation job translates script 'STOP' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-005: One independent step of the translation job translates script 'SSP4D1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-006: One independent step of the translation job translates script 'SSP2I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-007: One independent step of the translation job translates script 'SSC1A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-008: One independent step of the translation job translates script 'SSP4A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-009: One independent step of the translation job translates script 'SSP1I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-010: One independent step of the translation job translates script 'SSP3D1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-011: One independent step of the translation job translates script '#SSVARS' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator. The job must accept a script name that starts with '#'.
- UP-BR-012: One independent step of the translation job translates script 'SSP2U1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-013: One independent step of the translation job translates script 'SSP3I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-014: One independent step of the translation job translates script 'SSC1I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-015: One independent step of the translation job translates script 'SSP2A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-016: One independent step of the translation job translates script 'SSP2D1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-017: One independent step of the translation job translates script 'SSP1U1' from the script library, using that library as its include library and taking message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-018: One independent step of the translation job translates script 'SSP3A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-019: One independent step of the translation job translates script 'SSP4I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is not kept after the step, and keeps its listing and sequential output for the operator.
- UP-BR-020: One independent step of the translation job translates script 'SSP1A1', read as the step's control input, from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-021: One independent step of the translation job translates script 'SSP1D1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and writes its listing and sequential output to the job's default output.
- UP-BR-022: One independent step of the translation job translates script 'WSC1A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its report and sequential output for the operator.

## Decision tables

None.
