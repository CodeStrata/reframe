# Implementation plan: Build and deploy online programs (UP-C06)

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

- UP-BR-027: A CI/CD deploy step. When the build succeeds (warnings allowed, no errors), roll out the new version to the running online service, for example by a rolling restart or a hot reload, so new requests use the new code.
- UP-BR-028: Run this only when every build step succeeded without warnings. It registers or refreshes the program's database access against the CARDDEMO schema, replacing the previous version, using read-committed isolation. In a modern stack this is usually a schema migration or a step that grants database permissions, gated on a green build.
- UP-BR-029: After the database access step succeeds (warnings allowed), refresh the application-level database binding that covers all CARDDEMO programs. Keep the existing permissions and use the same CARDDEMO schema and isolation. In a modern stack this is the deploy-time database configuration or role setup, and it must not reset grants.

## Decision tables

#### CICS-Db2 build bind steps

| Precompile, translation, compile and link-edit result | Package bind result | Bind action | Rule |
|---|---|---|---|
| all return code 0 | not yet run | Bind package into collection 'CARDDEMO' | UP-BR-028 |
| all return code 0 | return code 4 or less | Bind application plan over 'CARDDEMO.*' keeping authorizations ('RETAIN') | UP-BR-029 |
| link-edit failed | did not run | Plan bind still runs | UP-BR-030 |
| all return code 0 | return code above 4 | **Gap:** No rule states whether the plan bind is skipped or run when the package bind fails. | |
| precompile, translation or compile failed | did not run | **Gap:** No rule states whether the plan bind runs when an earlier step than link-edit fails. | |

