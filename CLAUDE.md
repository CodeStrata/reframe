# Working on Reframe v2

- The source of truth is [docs/v2/specification.md](docs/v2/specification.md) and [docs/v2/plan.md](docs/v2/plan.md).
- Before designing or writing code, find the specification section and the story the work implements.
- If no section or story covers the change, stop. Update the specification, then the plan, then the epics and stories ([docs/v2/README.md](docs/v2/README.md)), and only then design and build.
- Do not change expected behaviour or narrow scope to make tests pass. A test that disagrees with the specification is a finding, not something to edit away.
- v1 on `main` is frozen. Port v1 modules only as specification section 15 describes: one at a time, with their tests, after review.
- Follow [CONTRIBUTING.md](CONTRIBUTING.md) for branches, identity, review and publication.
