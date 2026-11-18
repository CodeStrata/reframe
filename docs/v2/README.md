# Reframe v2

This folder is the reference for Reframe v2. Every design and build decision is checked against it.

| File | What it holds |
|---|---|
| [specification.md](specification.md) | What v2 does: scope, workflow, requirements, data model, AWS resources, package, security, commands, acceptance, phases and owner decisions |
| [plan.md](plan.md) | Why v2 exists, what changes from v1, phases, success measures, risks, remaining owner decisions and next steps |
| [backlog.md](backlog.md) | Index of the v2 epic and stories in GitHub |

## Change process

Any change to v2's behaviour, scope or plan follows this order. Each step lands before the next one starts.

1. Update [specification.md](specification.md). When a decision changes, update its row in section 16.
2. Update [plan.md](plan.md) where phases, measures, risks, decisions or next steps change.
3. Update the v2 epic and stories in GitHub to match.
4. Then design and build.

A pull request into `v2` names the specification sections and the stories it implements. A pull request that does something the specification does not describe waits until steps 1 to 3 are done.

## Checking alignment

- Each story names the specification sections it implements and the acceptance cases from section 14 that prove it.
- A phase is done only when its exit in section 15 is met.
- Section 16 records every owner decision; the appendices record how each review finding was answered.

## Branches

v2 is built on the `v2` branch, created from `develop`, alongside v1 (specification section 15). Work on v2 uses feature branches from `v2` and pull requests back into `v2`. v1 stays frozen on `main` until v2 passes P3. [CONTRIBUTING.md](../../CONTRIBUTING.md) still applies to identity, review and publication.

## Reading copies

The same documents are kept as shared docs for review and comments. They are updated in the same change as these files. When they differ, these files win.

These documents were prepared with AI assistance. The owner's decisions are recorded in specification section 16.
