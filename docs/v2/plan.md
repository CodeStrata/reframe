# Reframe re-scope plan

Status: 18 November 2026. Follows [specification.md](specification.md); change it only as [the change process](README.md) describes.

Reframe takes a mainframe repository through AWS Transform and produces an AI-DLC-ready package: verified business rules, a domain model, interactive wireframes, API specifications, and skills and guardrails for the tech stack chosen at the last gate. People add context at three gates instead of approving every stage and question. The engineering team then starts its own AI-DLC project from the package in Claude Code or Kiro. This plan follows [Reframe specification v2](specification.md) and was revised on 18 November 2026 after the AI-DLC spike.

## Why re-scope

The CardDemo run proved that source-checked specifications are valuable. It also proved that today's workflow needs a person at every stage and will not scale past a small codebase. CardDemo is 186 source files and about 50,000 lines.

| Finding | Evidence from the CardDemo run |
|---|---|
| Source checking catches real errors | One revalidation pass found 14 places where AWS's requirements disagree with the COBOL: account-number length, a rollback that does not exist, SSN masking, bill-payment error flags. |
| The reviewer adds value without re-reading source | Round 6 review returned 4 concrete consistency findings, none needing a new source read. |
| Humans are asked to approve everything | 5 approval gates. 461 open questions block validation approval. 670 implementation blockers. All 452 earlier questions were deferred in one batch, so the gate added ceremony, not review. |
| One synthesis covers the whole scope | Synthesis calls were 330K–390K tokens (538–925 KB) for one business function. Context limits were raised twice to fit. |
| Extraction is done twice | Reframe spent 306 calls extracting rules. AWS Transform separately produced 351 rules, 15 business functions and 397 traced requirements for one function. |
| Cost so far | 309 model calls, about 10 million input tokens, $75.62 as reported by the provider CLI. |
| Effort went into the controller | About 20 controller defects were found and fixed during live runs, mostly in gates, pins, limits and recovery rather than in specification quality. |

The run stopped at its round limit with a REWORK review, after 397 of 398 AWS requirements were cited. That result is the reference point for this plan.

## Target workflow

Scheduled reviews never hold the run. Reframe opens three review gates and carries on in the background while people review; work that needs a person's decision stays parked, and status says what it waits for; their context later reruns only what it changes. Everything before gate 3 is platform-neutral. The workflow diagram is in section 4 of the [specification](specification.md).

- **Gate 1, after AWS Transform:** scope, business context, corrections and the modernization goal, preserve or modernize.
- **Gate 2, after Claude's independent review:** stakeholders read the assessment report and return corrections and priorities.
- **Gate 3, after design:** stakeholders comment on the interactive wireframes, page rules and API specifications, or iterate on an exported copy outside Reframe and import it back. A draft package is built meanwhile; a named owner accepts the design and chooses the tech stack and the AI tool, Claude Code or Kiro.
- **After gate 3:** Reframe writes skills and guardrails for that stack and tool and hands the package to the engineering team, who start their own AI-DLC project.

## Package format: AI-DLC-ready

Reframe does not run AI-DLC. The package is what an engineering team copies into a new AI-DLC project (awslabs/aidlc-workflows, pinned release) before running `aidlc knowledge onboard` in Claude Code or Kiro. Today Reframe writes `specification.json`, `ai-dlc.json`, `AGENTS.md` and `SKILL.md`, and its specification forbids naming .NET; a test fails a handoff that mentions Blazor. Paths starting with `knowledge/` or `memory/` are under `aidlc/spaces/default/`; every other path, including dot folders, is at the package root.

| Reframe output | Lands in the AI-DLC project as | Used by |
|---|---|---|
| The chosen stack: languages and frameworks, type mappings, Keep/Migrate/Remove for mainframe parts | `knowledge/aidlc-shared/technical-environment.md` | Every stage; Code Generation |
| Guardrails: Tech Stack, Mandated and Forbidden | `memory/project.md` | Every stage, as rules it must follow |
| Requirements with verification status, business rules, domain model, screen specifications, OpenAPI contracts, backlog, acceptance scenarios, assumptions | `knowledge/documents/reframe/`, loaded by `aidlc knowledge onboard` | Requirements Analysis through Build and Test |
| Skills for the chosen stack | `.claude/skills/reframe-<name>/SKILL.md` or `.kiro/steering/reframe-<name>.md` | Claude Code or Kiro while AI-DLC runs |
| Interactive design site and assessment report | `design/`, outside the knowledge | Stakeholders and engineers |

The spike (18 November 2026, AI-DLC v2.11.4) settled the open points. AI-DLC onboarded eight Reframe files as knowledge, but its classic plan has 14 stages with 14 approval gates and its first stage asked seven team-practice questions, so running AI-DLC stays with the engineering team. There is no `codekb/`: the package starts a new build, so Reverse Engineering is skipped. AI-DLC kept only the first 200,000 characters of a longer file, so knowledge files are split per context to stay under that limit.

AI-DLC keeps its own gates and questions, and they are the engineering team's to answer. Reframe's part is to make those answers easy: the knowledge answers what the mainframe already says, and the project rules carry the guardrails into every stage. In the spike, Practices Discovery updated `project.md` after its questions were answered, so P2 checks that the guardrails Reframe writes survive it.

## AWS setup: optional

Provisioning is optional. In an account Reframe may manage, the first run with `--provision` creates everything it needs with HashiCorp Terraform, each resource with a least-privilege IAM policy, under one project name; later runs reuse what belongs to the same repo and create a new set for a new repo. In a client account, the client can create the resources with Reframe's Terraform module or its own, and the engineer passes their names (S3 bucket, role, Transform workspace, connectors, Neptune cluster) in a resources file. Reframe checks those read-only and never changes or deletes them. Reframe moves off OpenTofu entirely.

What `--provision` creates, and what Reframe does today:

| Resource | Today | Gap to close |
|---|---|---|
| S3 sandbox bucket: encrypted, versioned, public access blocked | Created by guided setup with OpenTofu (`infrastructure/main.tf`) | Move from OpenTofu to HashiCorp Terraform |
| Sandbox IAM role with a policy that denies reads outside the bucket | Created by OpenTofu | Move from OpenTofu to HashiCorp Terraform |
| AWS Transform workspace | Created by Reframe through the Transform MCP server | None |
| S3 connector for the assessment | Created by Reframe; a named person confirms it | Not created for the Assess and reimagine plan, which uses only the reimagine connector; AWS's documentation keeps the S3 connector for custom plans (20 November 2026) |
| Neptune knowledge-graph stack (cluster, subnets, security group, bulk-loader role) | Not created; Reframe requires an existing stack from AWS's `neptune-kg-setup.yaml` | First look for an existing Neptune Serverless cluster that meets the connector's needs and ask the person whether to use it, by name; otherwise create one with Terraform in its own private network, as AWS's template does (a VPC, two subnets, a route table and an S3 gateway endpoint, with no internet gateway or NAT), removed with the graph: one per repo until P2 proves two repos can share one safely, then one per account and region; read the six connector values from Terraform outputs or the chosen cluster instead of CloudFormation stack outputs |
| Reimagine connector and its IAM role (`N-reimagine`, `N-rmg`) | Created by a separate `requirements connector --create` command | Run it as part of first-run setup |
| AWS Transform enabled for the account and its users | Not handled | Check what can be automated; document the rest as a one-time admin step |
| Permissions for the person running setup | Not defined | Ship one bootstrap IAM policy and the Terraform module with a resources file template; the client chooses which to use |

Every resource is named from the project name N (`reframe-<repo>-<date>-<suffix>`) and tagged `ManagedBy=reframe, ReframeProject=N and ReframeRun, as the reimagine role already is. All project state (Terraform state, the resource manifest, the worker lease and the event log) lives in one Reframe state bucket per account and region`.

What later runs do:

| Situation | What Reframe does |
|---|---|
| Same repo, same commit | Reuses every resource. Starts a new `RUN-` job, or with `--replace` makes it the current one in place of the previous run, whose outputs stay as history. |
| Same repo, new commit | Reuses every resource. Uploads the new source version and starts a new job in the same workspace. |
| New repo | Creates a new bucket, roles, workspace and connectors named from the new repo, and its own Neptune graph until P2 proves shared graphs safe. |
| Run finished | `reframe teardown` deletes only resources that are both in the project's manifest and carry its tag, and only after a person confirms; a tagged resource missing from the manifest is listed, never deleted. The shared Neptune graph, the main ongoing cost, is removed only with `--shared` and only when no other project uses it. For testing, `reframe run --clean-start` removes earlier resources, after confirmation, and recreates them. A project marked disposable for a test is removed completely when the test ends, buckets and their contents included, with no final snapshot. |

AWS allows one reimagine connector per workspace, so one workspace per repo keeps those connectors separate.

## Keep, change, drop

Most of the code stays. What changes is the default route: blocking questions become recorded assumptions, five approval gates become three context gates, work is split by domain, and the output becomes an AI-DLC-ready package.

| Part of Reframe today | Decision | What it becomes |
|---|---|---|
| Source pinning, hashes, provenance, versioned artifacts | Keep | The audit trail behind every output. |
| AWS Transform integration (connector, jobs, chat answers, retrieval) | Keep | The extraction engine: business functions, business rules, requirements, traceability. |
| Evidence units with source anchors | Change | Verify AWS's claims against source instead of extracting rules a second time. |
| Independent reviewer | Change | Claude Opus, in a separate context, checks each domain's output and the design. A failed check marks the output; it does not stop the run. |
| SME questions that block approval | Change | An assumptions register: proposed answer, confidence, impact and owner, shipped in the package. |
| Five approval gates | Change | Three context gates: after AWS Transform, after the review, and after design. Package acceptance only in audit mode for regulated clients. |
| Specification feedback that withdraws the whole specification | Change | Context packs routed to the affected domains, with only those regenerated. |
| One synthesis over the whole scope | Drop | You still give the whole repo and get one package. Analysis covers all of it; the specification work then runs once per domain (CardDemo: 4 domains, 15 business functions), and a merge combines them. |
| Per-question decide and defer commands in the default route | Drop | Kept only for audit mode. |
| Manual allowances, pins and prompt migrations in the default route | Drop | Run budgets are set once at intake; migrations stay recorded but automatic. |
| Wireframe staging, API contracts, coverage views, package builder | Keep | Becomes the interactive design site, shaped by the modernization goal, with export and import for work outside Reframe; run per domain, then merged into one package. |
| Package format: specification.json, ai-dlc.json, AGENTS.md, SKILL.md | Change | An AI-DLC-ready package that engineers load into their own AI-DLC project (see Package format). |
| Language-neutral handoff; a test fails one that names Blazor | Change | A target profile chosen at gate 3 with the AI tool. .NET and Blazor is the default; Reframe writes skills and guardrails for it. |
| Kiro and Codex as Reframe's model providers | Drop | Claude only: Sonnet generates, Opus reviews. Engineers can still run AI-DLC in Kiro. |
| OpenTofu for the sandbox bucket and role | Change | HashiCorp Terraform for every AWS resource Reframe owns, the shared Neptune graph included. |

## Phases

Six phases, defined in section 15 of the specification, each ending in a measurable result. Code approach (agreed 18 November 2026): v2 is a new package alongside v1 on its own branch, built from the specification; proven v1 modules move across one at a time with their tests, each after review; v1 stays frozen on main as a pinned release and readable archive until v2 passes P3, which accepts v1 import and recovery.

Change control: the specification and this plan are kept in the v2 branch of the Reframe repository under `docs/v2/`, and every design and build decision is checked against them. Any change follows one order: update the specification, then this plan, then the epics and stories, and only then design and build. The Claude docs are reading copies, updated in the same change.

1. **P0, contracts.** Schemas for the canonical model, the state machine and exception table, the data policy with Bedrock destination rules, the disposition matrix, the worker and command contract, the CLI isolation and plan sign-in proof, the package manifest, semantic fixtures with seeded defects and thresholds, the port-or-drop inventory of v1 modules, the v2 package skeleton; v1 frozen on main.
  - Done when: two implementers would build the same thing from the spec, and v1's regression tests are carried forward.
2. **P1, prototype and external proof.** The design site renderer, generic for any canonical design, shown in both goals on three deliberately different sample journeys (online CICS, batch-only, and a message or file exchange), at least one not from CardDemo, and reviewed by an SME and an architect; expert-reviewed semantic fixtures for one sample journey; one authorized live path from function selection to requirements retrieval, for a bounded function from a repository the owner names (CardDemo by default). CardDemo is test data, never something the code is fitted to.
  - Done when: the design format is agreed and no unproven AWS behaviour is needed for the first route.
3. **P2, one domain.** "Account and Customer Profile Administration", once with `--provision --clean-start` and once with a resources file; two runs, one with every gate answered while the run carries on and one with a gate left to time out; model calls through the Claude Code CLI, with one context repeated on Bedrock to prove the switch; the package in Claude Code and Kiro; the Neptune isolation test; reviewer independence measured against seeded defects.
  - Done when: semantic fixtures pass, package retrieval is verified, and blockers are reported separately from completion. v2 can become the default; v1 stays until P3.
4. **P3, change and recovery.** Resume and reuse, late context, stale imports, provider failures, uncertain dispatch, budget exhaustion, concurrency across machines, teardown, v1 import, and one whole vertical slice on Bedrock. A client pilot follows this phase, and v1 is retired at its exit.
  - Done when: no paid work is repeated, no resource is duplicated, and invalidation reaches exactly the dependents.
5. **P4, whole CardDemo.** Every function at a pinned revision, including batch and shared data.
  - Done when: coverage is complete or every gap is labelled.
6. **P5, scale.** VirtualBank (github.com/mainframe-projects/VirtualBank) and mainframe-claim-modernization (github.com/lillycodebreaker/mainframe-claim-modernization), run one after another through the CLI after CardDemo, with nothing built for them; budget and thresholds set before each run.
  - Done when: results are within the thresholds and unsupported areas are labelled.

## Success measures

The re-scope succeeds when a package arrives with scheduled reviews never holding the run, at a cost that grows with the number of domains rather than with the whole codebase in one call. Targets are proposals; cost targets are set after P2 measures them.

| Measure | CardDemo today | Proposed target |
|---|---|---|
| Human stops before the package | 5 gates plus a decision or deferral on each of 461 questions | 3 context gates that never hold the run; package acceptance added only in audit mode |
| Largest single model call | 387K tokens (review, round 6) | At most 200K tokens |
| Requirements mapped or excluded with a reason | 23 of 398 (19 mapped, 4 excluded); 397 cited somewhere | At least 90% |
| Rule extraction calls | 306 by Reframe, plus AWS's own extraction | 0 by Reframe; verification calls only |
| Regeneration after one review note | The whole specification is withdrawn and rebuilt | Only the affected contexts and items |
| AWS errors caught against source | 14 for one business function | Tracked per domain; every one cited to a source line |
| Maps covered by the design site | No design site completed for CardDemo | Every map covered by a page or excluded with a reason |
| Cost per thousand source lines | Not measured per domain yet | Set after P2 |
| Package loads into AI-DLC | Spike: 8 Reframe files onboarded; one 253 KB file cut at 200,000 characters | Onboards with no errors in Claude Code and Kiro; no file over 200,000 characters |
| Guardrails after Practices Discovery | Not measured | Every Reframe guardrail still present after the team answers |

## Risks and decisions

The main risk is an unreviewed package being read as approved. Every output therefore carries its review status and the assumptions it rests on.

| Risk | Mitigation |
|---|---|
| A package resting on assumptions is read as approved | Every assumption carries confidence and status; readiness is computed, never declared. |
| Quality with only three gates | Automated review per domain and of the design, targeted source checks on every AWS claim used, and the P2 measures before scaling. |
| AWS Transform constraints: one reimagine connector per workspace, chat-driven steps, Neptune cost | Keep the requirements import path as a fallback. Record every setup answer at intake and answer AWS's setup chat with one message, then each recognized question within a polling interval, because AWS's job agent stops when a question waits too long (seen live, 20 November 2026). |
| Shared entities conflict across domains | The merge step records each conflict as an assumption with both definitions, instead of picking one silently. |
| Model window or cost at scale | Per-context calls with a token cap and a budget set at intake. |
| AI-DLC changes quickly (v2.11.4 on 13 Nov 2026) | Pin the AI-DLC release in the package and run a conformance check against each new release. |
| Gate 3 does not close | A named owner and a comment deadline; the goal set at gate 1 settles preserve against modernize before design starts. |
| Wireframes changed outside Reframe lose traceability | Import refuses a bundle that drops a verified rule without a reason or calls an operation with no contract. |
| Practices Discovery overwrites the guardrails | P2 checks it; if it does, the guardrails also go into a file AI-DLC does not rewrite, such as CLAUDE.md or a Kiro steering file. |
| Mainframe semantics lost in the target stack: packed decimals, EBCDIC, record layouts, CICS screen state | The technical environment fixes the type mappings, the guardrails require the rules' precision, and tests carry the oracles from verified rules. |
| Business rules published on a public GitHub Pages site | Publish only to a Pages site restricted to the customer's organization (GitHub Enterprise Cloud's private Pages); otherwise the sites are opened from the package. |
| Several repos write into one shared Neptune graph | P2 checks that reimagine jobs from two workspaces do not overwrite each other's graph data before more repos share it. |
| Work runs ahead of review on wrong assumptions | Each default is recorded as an assumption and nothing unreviewed counts as approved; context added later reruns only the affected steps, and reruns are counted against the budget. |

Owner decisions (the full record is in section 16 of the specification):

- [x] Adopt specification v2 as the product direction, with audit mode optional.
- [x] One Neptune graph per account and region is the target, per repo until P2 proves sharing is safe; the current test stack is removed and recreated on the first run with --clean-start.
- [x] HashiCorp Terraform for every AWS resource Reframe owns.
- [x] "atx" meant AI-DLC.
- [x] Scale test on VirtualBank and mainframe-claim-modernization.
- [ ] Delete or keep the unused IAM role from the first reimagine trial.
- [ ] What retiring v1 means at P3's exit. Proposed: v1's files (`scripts/`, the root `pyproject.toml`, v1's `tests/`, `prompts/` and `contracts/`, `README-v1.md`) leave the v2 branch in one commit before v2 merges to main; v1 stays readable in history and installable from tag `v0.3.0`. Until then both packages declare a `reframe` command, so v1 and v2 are installed in separate environments.
- [x] Client AWS accounts: the client gives a profile with the access Reframe needs, or we set the account up; Reframe cleans up only what it created and tagged.
- [ ] Choose the default modernization goal for CardDemo and who owns gate 3.
- [ ] Name the two scale-test repositories: VirtualBank and mainframe-claim-modernization. To confirm: the VirtualBank link returns not found, and mainframe-claim-modernization holds no COBOL of its own (the IBM sample it clones has 2 programs), so P5 still needs repositories larger than CardDemo.

## Next steps

The CardDemo run stops here as the reference result; no further gates are pursued on it.

- [x] Merge the open pull requests to main (done 18 November 2026).
- [x] Run the AI-DLC spike (done 18 November 2026; results are in the specification).
- [x] SME, architect and client review of the specification; revision 2 answers all 26 findings (18 November 2026).
- [x] Second review round of specification revision 2: it approved starting P0 and a bounded P1, and its 12 findings (U01 to U12) are answered in the specification's appendix B.
- [x] Specification and plan committed to the v2 branch under docs/v2/ (18 November 2026).
- [x] v2 epic and stories created in GitHub ([backlog.md](backlog.md)); the 20 open v1 issues closed as superseded (18 November 2026). Next: build P0, starting with P0-01.
- [ ] Seal the round-6 candidate, its review and the coverage numbers as the baseline.
- [ ] Answer the remaining owner decisions above, including the scale-test repositories.

## Sources

- [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) and its [v2.11.4 release](https://github.com/awslabs/aidlc-workflows/releases/tag/v2.11.4)
- [AI-DLC artifacts reference](https://awslabs.github.io/aidlc-workflows/guide/14-artifacts-reference/)
- [AI-DLC phases and stages](https://awslabs.github.io/aidlc-workflows/guide/04-phases-and-stages/)
- [AI-DLC knowledge documents](https://awslabs.github.io/aidlc-workflows/guide/08-knowledge/)
- [AI-DLC technical environment guide](https://awslabs.github.io/aidlc-workflows/guide/writing-inputs/technical-environment-guide/)
- [Reframe specification v2](specification.md)
