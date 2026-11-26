# Start here

This package was written by Reframe from genapp's legacy source, its reconciled requirements and rules, and the reviewers' sign-offs. It holds what
those settle. What only your team can give is marked `[FILL IN: ...]`. These steps make it ready for forward engineering.

- Specifications: `specs/<nnn-capability>/` (spec.md, plan.md, tasks.md).
- Stack, technical context and house conventions: `.specify/memory/constitution.md`. Roles: `.claude/agents/`; skills: `.claude/skills/`.
- Every form: `data-contracts.md` (the copybooks as typed records) and `traceability.md` (every ID back to the legacy source).

## 1. Copy the package

`reframe design --package <empty folder> --form kiro|claude-code|spec-kit|all` (today: `python -m reframe.design.package --out <empty folder>`).
Work in the copy. Reframe will not copy over files you have filled in: when the design changes, copy the new version into a new folder and
carry your filled-in files across; `CHANGES.md` says what changed, by ID.

## 2. Give the target stack

The stack is not given yet. Give or change it with
`reframe design --stack "<front end>; <back end>; <data>"` (today: `python -m reframe.design.specs --stack ...`, then write the package again).
Reframe adds the stack's code and column types to the data contracts, with no model step. It never chooses a stack for you.

## 3. Fill in the placeholders

- **Target architecture:** versions, build, testing, hosting, security, integration and non-functional needs. Put them in `target-architecture.md`
  in the design context folder and write the package again with `--context <folder>`, or fill them where they are.
- **House conventions:** coding standards, naming, error handling and logging, style reference, review rules, definition of done.
- **Skills** (`.claude/skills/`): the build and test commands, frameworks and libraries each skill uses.
- **Roles** (`.claude/agents/`): the *On this stack* section of each role.

`personas.md` and `decisions.md` in the context folder are added to the product description the same way.

## 4. Settle what is still open

- **Draft capabilities:** 57 of 57 are draft because their function is not signed off. Sign off
  each function on the reconciliation page, read the review download with `reframe reconcile --context <folder>`, and write the design again.
  - Application Deployment and Policy Lifecycle Management: 21 draft
  - Customer Record Creation and Maintenance: 7 draft
  - Diagnostic and Error Message Logging: 2 draft
  - Transaction Statistics and Monitoring: 4 draft
  - Unassigned programs: 5 draft
  - Unassigned-Programs: 13 draft
  - Web Service Interface Generation: 5 draft
- **SME questions:** 188 open. Answer them in `reconcile/questions.csv` and run `reframe reconcile --context <folder>`.
- **Decision table gaps:** 24 combinations no rule covers, listed in each design. Decide each with the owner.
- **Historical artifacts:** rules to keep or drop with the owner before anyone builds them: ADPLM-BR-082, ADPLM-BR-114, ADPLM-BR-153, CRCM-BR-027, TSM-BR-013, TSM-BR-015, UP-BR-079, UP-BR-100, UP-BR-101, UP-BR-114, UP-BR-121.

## 5. Check what is left

`python -m reframe.design.package --check <your copy>` lists every `[FILL IN: ...]` still there and the draft capabilities. It is ready when no
placeholder is left and the capabilities you are building are final.

## 6. Prove it: build Sign in

In a scratch repository, with the Claude Code form and the stack filled in, ask Claude Code to build the sign-in slice:
  - UP2-C01 Customer add, update and menu (14 acceptance criteria; draft: confirm it with the owner first, or sign off its function)
  - UP2-C02 Motor policy inquire, add, delete and update (14 acceptance criteria; draft: confirm it with the owner first, or sign off its function)
  - UP2-C03 Endowment (life) policy inquire, add, delete and update (21 acceptance criteria; draft: confirm it with the owner first, or sign off its function)
  - UP2-C04 House policy add, delete and update (10 acceptance criteria; draft: confirm it with the owner first, or sign off its function)
  - UP2-C05 Commercial property policy inquire, add and delete (19 acceptance criteria; draft: confirm it with the owner first, or sign off its function)

Use the `build-capability` and `write-acceptance-tests` skills. Record whether it builds and which acceptance criteria pass, by ID. A failure
here is a gap in the package or the placeholders: fix it before the full build.

## 7. Build

Final capabilities first; each task names its role and the requirement, rule and criterion IDs it implements. Keep every ID in code and tests.
