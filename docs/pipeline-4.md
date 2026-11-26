# Reframe specification: the design (pipeline 4)

Status: agreed by the owner on 25 November 2026 (P4-01). The owner's decisions of that day are written in (section 9): the engineer gives the target stack; signed-off functions are final and the rest draft; Reframe's own design system, which a context file replaces; the name *the design*, run with `reframe design`. Stories are in [the plan](plan.md), pipeline 4.

## 1. Goal

After the reconciliation (pipeline 3) has given one reviewed set of recommended rules and requirements, Reframe designs the modernized application, not a lift and shift of the 3270 screens:

1. reads every legacy screen (BMS map) into its fields, positions, attributes and function keys, with no model, and draws each as a faithful 3270 copy;
2. reads how the screens and programs connect, from the source, each link citing its lines;
3. groups the screens into the journeys people do, each linked to its capabilities and requirements;
4. designs modern screens for each journey, with a mapping table that takes every legacy screen and field to what replaces it (kept, merged, dropped or new) and why;
5. draws an interactive, clickable prototype of the modern screens, each beside the legacy screens it replaces, that reviewers can mark;
6. writes the final specifications per capability: requirements, business rules with worked examples, screen specifications, data contracts, acceptance criteria and open questions, each citing its sources;
7. writes an AI-DLC package, in a form Kiro loads and a form Claude Code loads, for the forward build on the engineer's target stack;
8. keeps all of it up to date as people add context, redoing only what the context touches and saying what changed.

Model steps write structured results that cite requirements, rules, screens and source lines. Reframe checks every citation and draws every page, the prototype and the package itself, as in pipelines 2 and 3.

## 2. Scope

| In | Out |
|---|---|
| Online screens: every BMS map in the snapshot (21 on CardDemo, including the optional modules' 4) | Generating the application's code: the package is for the forward build. P4-08 builds one journey from it only to check it loads and is complete |
| Batch functions: specifications and data contracts, with jobs described as services or scheduled jobs; no screens or journeys | Deploying anything, and data migration |
| The reconciled requirements and rules, the SME list and its answers, the reviewers' marks and sign-offs | Deciding rules again: a change to rules goes through `reframe reconcile` first, and the design reads its results |
| Copybooks, as the shape of sample data and data contracts | Any AWS resource: the design, like the reconciliation, needs none |

## 3. Commands

| Command | What it does |
|---|---|
| `reframe design` | Guided: checks the reconciliation is done, asks for the target stack if the run has none, shows the estimate, and runs in the background. Stops above the batch limit |
| `reframe design --stack "<front end>; <back end>; <data>"` | Gives the target stack without asking, for example `"React with TypeScript; Java 21 with Spring Boot; PostgreSQL"` |
| `reframe design --context <folder>` | Adds design context (section 5). The folder is remembered for later rounds |
| `reframe design --max-batches <n>` | Goes ahead with a larger estimate |
| `reframe design --open` | Opens the design page, with the prototype |
| `reframe design --package <folder> [--form kiro\|claude-code\|both]` | Copies the latest package into a folder, cleaned as `reframe publish` cleans its copy (default: both forms) |
| `reframe status`, `reframe resume`, `reframe review`, `reframe publish`, `reframe export` | As today, with the design added: its stage and round, resuming after Claude's usage limit, reading prototype review downloads, including the design page and prototype in a published copy, and S-13's backlog files taking the final specifications when they exist |

**The target stack** is the engineer's input. It is never guessed: the guided command asks, offering common stacks as numbered choices and *something else* typed in, and `reframe design` without a terminal stops and names `--stack`. It is recorded in the run with who gave it and when. A `target-architecture.md` in the context folder adds the detail (versions, services, integration, non-functional requirements); the stack line still comes from the engineer. Changing the stack starts a new round that redoes only what depends on it: the data contracts' types, the screen specifications' component notes, and the package (section 4, stage D9).

## 4. Stages

| Stage | What it does | Model |
|---|---|---|
| D0 Preflight | The reconciliation is DONE for this snapshot; the snapshot's SHA-256 matches; the target stack is given; Claude is signed in; the context folder exists | No |
| D1 Screen inventory | Every BMS mapset, map and field read | No |
| D2 Screen flow | How screens and programs connect | Only for what the source leaves open |
| D3 Journeys | Screens grouped into tasks | Yes |
| D4 Modern screens and mapping | New screens per journey, and the mapping table | Yes |
| D5 Prototype | The clickable app | No |
| D6 Final specifications | Per capability | Yes |
| D7 Package | Kiro and Claude Code forms | No |
| D8 Design page | One page over all of it | No |
| D9 Rounds | Only what new context touches is redone | – |

### D1 Screen inventory (P4-02)

Reframe parses every `DFHMSD`, `DFHMDI` and `DFHMDF` macro, with continuation lines, into: mapset and map names, size, and each field's name, line, column, length, attributes (`ASKIP`, `PROT`, `UNPROT`, `NUM`, `BRT`, `NORM`, `DRK`, `IC`, `FSET`), colour, highlight, `INITIAL` text, `PICIN` and `PICOUT`, and whether it is a label (unnamed, with initial text) or a data field. The symbolic map copybook (`cpy-bms/`) is matched to each map. Function keys come from the programs that send the map: Reframe reads `EIBAID` and `DFHPFn`, `DFHENTER` and `DFHCLEAR` conditions and the paragraph each leads to, with their lines. A key whose handling the source does not show is listed as *unknown*, not guessed.

Each screen is drawn as a faithful 3270 copy: a 24 × 80 grid, the field colours and intensities, protected and input fields told apart, and a list of the function keys. Results: `design/screens.json` and `outputs/design/legacy/<map>.html`.

**Checked:** every map in the snapshot is read and matched to the program that sends it; every field lies inside the map; every named field appears in the symbolic map copybook. Fields that overlap in the source are reported by kind (data over data, an attribute byte on data, a shared attribute byte), not treated as errors: CardDemo's own maps have eight such notes. A key the screen shows but no program tests, or one a program tests but the screen does not show, is listed for review. The spike (P4-02) did this on all 21 CardDemo maps; what it found is in [spikes/p4-02-screens.md](spikes/p4-02-screens.md).

### D2 Screen flow (P4-03)

Read from the source, each link citing its lines:

- transaction to program, from the CSD (`DEFINE TRANSACTION`);
- program to map, from `EXEC CICS SEND MAP` and `RECEIVE MAP`;
- program to program, from `XCTL`, `LINK` and `RETURN TRANSID`;
- menu options to programs, from option tables such as `COMEN02Y` and `COADM02Y`;
- function keys to targets, from D1.

Where a target is held in a variable that the source sets in more than one place, a model step reads the code and names the targets, each with its lines, which Reframe checks exist. A target still unknown is shown as such. Result: `design/flow.json` and a map on the design page, screens as nodes, links labelled by key or option.

**Checked:** every cited line exists; every screen is reached from a transaction or a menu, or is listed as *not reached*, with what was looked for.

**Command:** `python -m reframe.design.flow [--run <run>]` writes `design/flow.json` and `outputs/design/flow.html`, the map and each screen's links.

**How targets are read.** A transfer's target is resolved from a literal, a `VALUE` constant, the `MOVE`s into its variable, or a table filled by `VALUE` clauses and redefined with `OCCURS`, such as a menu's options; in that case every program in the table is a target, with its option. A variable the program only ever sets to its own name before transferring stands for the screen the user came from, which the source records at run time; it is shown as such. A key leads to what its branch moves into a transfer's variable, or transfers to by a name the program never changes, reading nested `IF`s and `EVALUATE`s and `WHEN`s stacked on one another, and one paragraph down.

**On CardDemo** (25 November 2026), in about one second:
- 25 transactions, 65 transfers, 1 call and 36 key links, every cited line checked;
- nothing left open, so no model step ran;
- all 21 screens are reached by navigation;
- F3 leads somewhere on 20 screens (the menu, or the screen the user came from). On Login it ends the session.
- **The map** is drawn from the most-entered screen, the sign-on, which every program transfers to when it starts without a session. It shows Login, then the two menus, then the 15 function screens, then View Authorization Details. Transfers back to the sign-on, F3, F12 and returns to the caller are listed under each screen, not drawn.

The model step for targets the source leaves open is built when a codebase needs it.

### D3 Journeys (P4-04)

One model step per domain groups the screens into journeys: the tasks people do (for example *Sign in*, *Find and view an account*, *Update a card*). Each journey has a name, the role who does it (from `personas.md` if given, otherwise from the requirements' user stories), its steps in order (screen and action), and the capabilities and requirements it serves, by key.

**Checked:** every screen is in at least one journey, or is listed as unused with the reason; every step follows a link in D2 (or stays on its screen, or goes back the way it came); every capability and requirement key exists, and each requirement belongs to one of the journey's capabilities. A failed answer is asked once more with the reasons, as in pipeline 3; what still fails is kept and listed. A screen belongs to the domain of the business function holding most of its programs' recommended rules. Each step is given its domain's screens (inputs with their labels, outputs, keys), capabilities and requirements, and the whole screen flow, so a journey can start at the sign-on or a menu of another domain.

**Command:** `python -m reframe.design.journeys [--run <run>] [--context <folder>]` writes `design/journeys.json` and `outputs/design/journeys.html`.

**On CardDemo** (25 November 2026):
- **Steps:** 4, one per domain with screens. They ran on the Claude subscription in about 4 minutes, for $4.10 at API prices.
- **Journeys:** 20, covering all 21 screens. Every answer passed Reframe's checks the first time, and no screen was left unused.
- **Examples:** *Find and view an account* (sign-on, Main Menu option 1, View Account, then F3 back to the menu), *Add a transaction type* (Admin Menu, the type list, then F2 to the update screen), and *Report or clear fraud on an authorization*.
- **Coverage:** 86 of the 154 capabilities and 742 of the 1,136 requirements. The rest are mostly batch and background functions, which section 2 gives specifications but no journeys; P4-07 checks that none of them is a screen's.

### D4 Modern screens and mapping (P4-05)

One model step per domain (not per journey, so that a screen many journeys share, such as the sign-on or a menu, is designed once, and a list and its detail can become one screen) designs the modern screens for the domain's journeys as a structured tree of components from the design system's list (section 5): page, section, form, field, table, list, tabs, button, link, message, dialog. Each component says what it shows or does, the requirements and rules it serves (by key), its validation and messages taken from the rules, and its keyboard access.

The mapping table takes **every legacy screen and field** to what replaces it:

| Legacy | Becomes | How | Why |
|---|---|---|---|
| a screen | one or more modern screens | kept, merged, split, dropped | from the journey and requirements |
| a data field | a component | kept, merged, dropped | for example the date and time in the header become the app's own header |
| a label | a component's label, or dropped | kept, dropped | |
| a function key | a button, link or shortcut | kept, merged, dropped | PF3 *Exit* becomes *Back* |
| – | a new component | new | a need the 3270 screen could not meet, citing the requirement |

The steps follow the UI guardrails from the research behind part 2 of the reconciliation ([pipeline-3.md](pipeline-3.md), section 8.2): do not recreate poor 3270 usability; never hide a validation in the screen only, every validation keeps its rule; keep keyboard-heavy flows fast for the people who use them; meet WCAG 2.2 AA.

**On CardDemo** (25 November 2026), 4 steps and one links pass took about 25 minutes, $19.60 at API prices.
- **Screens:** 20 modern screens and one shared application shell. The main and admin menus became one Home screen; card view and update became one card detail.
- **Mapping:** all 683 legacy screens, fields and keys mapped: 234 kept, 347 merged, 52 split, 50 dropped.
- **Checks:** every validation rule is shown, and no check failed.
- **Links pass:** the domains ran in parallel, so the menu domain first guessed other domains' screen ids. Reframe now merges screens of one id that replace no legacy screen (the shell) into one shared screen. It then asks a domain that links to screens nobody designed once more, giving it every other domain's screens.

**Per screen** (added 25 November 2026, from the research's UI modernization template), each modern screen also records what the design step does not yet carry:
- the role who uses it;
- the data it depends on: the files, tables and copybooks its legacy programs read and write;
- the services it will call, by name;
- the legacy screen's pain points the design removes, such as typed option codes, paging keys or errors shown one at a time;
- test scenarios for user acceptance: one per journey step, written from the worked examples.

It already records its purpose, fields, validations, rules and the programs behind it. One more guardrail joins the four above: every screen is checked with the people who use it, in the prototype, before it is final.

**Checked:** no legacy field is left unmapped and none is mapped twice; every component is from the design system; every key cited exists; every rule of kind *validation* that a screen's program applies is shown by a component of that screen.

### D5 Prototype (P4-06)

Reframe draws one static HTML app, with no build step and nothing loaded from outside, in `outputs/design/prototype/`:

- a route per modern screen, and navigation that follows the journeys;
- sample data shaped by the copybooks: each field's type, length and format from its `PIC`, filled from a fixed seed so every round shows the same data, with values from the rules' worked examples where they exist;
- messages and validations written from the rules, in the code's own words where the rule quotes them;
- on each screen, *Show the legacy screen* opens the 3270 copies it replaces, with the mapping;
- marks, as on the review pages: *Agree*, *Needs change* or *Question* with a comment, on each screen and component, and sign-off by journey, downloaded as JSON or CSV in the `reframe-review/1` format with the tool *Reframe's design*.

### D6 Final specifications (P4-07)

Per capability, one model step writes the parts that need words, and Reframe assembles the rest:

| Part | From |
|---|---|
| Final requirements | The reconciled requirements, with the reviewers' marks applied and *Agree* kept word for word |
| Business rules | The recommended rules, with their kind, confidence, worked examples and evidence |
| Screen specifications | D4's screens and mapping for the journeys that serve the capability |
| Data contracts | The copybooks the capability's programs use, as records with typed fields (a `PIC S9(7)V99 COMP-3` becomes a signed decimal with 7 integer and 2 fraction digits), on the target stack's types |
| Acceptance criteria | Given/When/Then written from the worked examples, each citing its rule; the same criteria S-13 exports |
| Open questions | The SME list's open entries for the capability's rules |

Each specification also carries (added 25 November 2026, from the research's business-rule template):
- **Decision tables:** the capability's decision tables from the reconciliation (P3-23), each row citing its rule, and the combinations no rule covers listed as gaps for an SME.
- **Classes:** each rule and requirement classed as a *business rule*, *formatting*, *error handling*, *side effect* or *historical artifact*, taken from the rule's kind (P3-21): business, validation and compliance rules are business rules; display is formatting; error handling stays; side effect stays; leftover is a historical artifact; technical steps go to the design notes. The forward build keeps business rules exactly, may restyle formatting, and asks before carrying a historical artifact.

A capability in a signed-off function is **final**; every other one is **draft**, marked so in the specification, the page and the package. **Checked:** every requirement, rule, screen and copybook cited exists; every requirement of the capability is in its specification.

### D7 Package (P4-08)

Written by Reframe from D6, in `outputs/design/package/v<round>/`, in three forms:

- **Kiro:** `.kiro/specs/<capability>/requirements.md` (EARS requirements and acceptance criteria), `design.md` (screens, components, data contracts, the flow) and `tasks.md` (build tasks, each citing requirement and rule IDs); `.kiro/steering/product.md`, `tech.md` (from the target stack and `target-architecture.md`) and `structure.md`.
- **Claude Code:** `CLAUDE.md` (the product, the stack, the conventions and how to use the specs), `specs/<capability>.md`, `tasks.md`, and the prototype in `ui-reference/` as the UI to build to.
- **Spec Kit** (added 25 November 2026):
  - **The constitution:** `.specify/memory/constitution.md`, with the non-negotiables. The legacy source is read-only; data is synthetic only, with no personal data; every item keeps its requirement and rule IDs; the target stack; final versus draft; and the order of replacement (P4-12).
  - **Per capability:** `specs/<capability>/spec.md`, `plan.md` and `tasks.md`.
  - **Role files:** `.claude/agents/<role>.md` for business rules, UI modernization, data, API, test generation (the golden datasets, P4-11) and compliance, each with its template and guardrails.

  Each task names the role that does it.

Every requirement, rule, acceptance criterion and task keeps its ID, so the forward build stays traceable to the legacy source. Draft capabilities are marked draft. `CHANGES.md` says what changed since the last version. **Checked:** by loading the Claude Code form into Claude Code in a scratch folder and building one journey (*Sign in* on CardDemo) on the target stack, recording whether it builds and which acceptance criteria pass.

### D8 Design page (P4-07, P4-10)

`outputs/design/index.html`, in the review layout: overview first (screens, journeys, mapping counts, final and draft capabilities); then the flow map, each journey with its screens side by side (legacy and modern), the mapping table with filters, and each capability's specification. The reconciliation page links to it, and `reframe publish` includes it with the prototype.

### D9 Rounds with more context (P4-09)

Each part is kept with a hash of what it was made from, as in pipeline 3. A new round redoes only the parts whose inputs changed:

| What changed | What is redone |
|---|---|
| The reconciliation (a new round of pipeline 3) | The journeys, screens, specifications and package parts of the functions whose requirements or rules changed |
| The target stack or `target-architecture.md` | Data contract types, screen specifications' component notes, the package |
| The design system | The modern screens' components and the prototype |
| `style-reference/` | The modern screens, the prototype and the package's conventions |
| `personas.md` | The journeys' roles, and what follows from them |
| Prototype marks | The marked screens and components; *Agree* keeps them |
| `decisions.md` | Whatever the decisions name |
| A sign-off | That function's capabilities become final |

Each round writes `design/changes-<round>.md`: what changed, why, and what was kept, and the package's `CHANGES.md` from it.

### D10 Golden datasets and equivalence tests (P4-11)

Per capability, Reframe writes a golden dataset from the worked examples and decision tables: cases the new system must answer as the legacy one does. Each case has:
- a dataset ID and its capability;
- the legacy source it comes from, and the rule it covers;
- the input and the expected output;
- whether it is an edge case;
- the service or screen it is run against;
- the comparison method and tolerance.

Comparisons are exact for money, dates, status codes, IDs and counts, and a difference in formatting (padding, case, an edited amount's layout) is reported apart from a difference in business behaviour. The datasets go into the package as test fixtures with the test-generation role's tasks. Until P4-13 captures real legacy outputs, the expected outputs come from the rules and say so: equivalence is then asserted from the rules, not proven against the running legacy system.

### D11 Risk and replacement order (P4-12)

Each capability already has a risk (P3-24) and touches a list of things (money, card data, personal data, security, audit, record updates, reporting only). Reframe orders the capabilities for replacement: low risk and read-only first (reporting, inquiry screens), then updates, and money, security and adjudication last. Within that order, a capability that shares data stores or screens with another follows it. The order is shown on the design page and written into the package's constitution and tasks, each with its reason.

### D12 Spike: real legacy outputs (P4-13, low priority)

Whether real outputs can be captured from the legacy programs without a mainframe: the batch programs compiled and run under GnuCOBOL on the golden datasets' inputs, with the files they read built from the copybooks. CICS screens are out of reach this way. The spike records which CardDemo batch programs compile and run, what they need (files, sort, utilities), and whether their outputs can replace the rules' expected outputs in D10.

## 5. Design context

Read from the context folder, by name:

| File | What it gives |
|---|---|
| `target-architecture.md` | Detail of the target: versions, services, integration, non-functional requirements |
| `design-system/tokens.json` and `design-system/components.md` | Replace Reframe's own design tokens (colour, type, spacing) and component list. Without them, Reframe's own plain, accessible set is used |
| `style-reference/` | The house's own examples to follow: screenshots or pages of existing applications, and code samples. The modern screens follow their look and patterns where the design system does not say, and the package's steering and constitution carry the code conventions |
| `personas.md` | Who uses the system and what they need |
| `decisions.md` | Decisions to follow, one per heading |
| Prototype review downloads | Marks and journey sign-offs on the prototype |

Pipeline 3's context (documents, its review downloads, the answered SME list) stays with `reframe reconcile`. The design reads the reconciliation's results, not its context.

## 6. Estimate

Before any model step, Reframe shows the steps by stage (journeys per domain, screens per journey, specifications per capability), minutes and cost at API prices, and stops above the batch limit, as the reconciliation does. On CardDemo the model steps are about 7 for journeys, 15 to 25 for screens, 153 for specifications (batched by function) and a few for the flow. The spike and the first live run set the figures.

## 7. Run folder and code

| Path | What it holds |
|---|---|
| `design/` | Working results: `screens.json`, `flow.json`, `journeys.json`, `screens-modern.json`, `mapping.json`, `specs/`, step logs, `changes-<round>.md` |
| `outputs/design/` | `index.html`, `legacy/`, `prototype/`, `package/v<round>/` |

Code in `src/reframe/design/`: `inventory.py` (BMS), `flow.py`, `journeys.py`, `screens.py`, `prototype.py` with its template, `specs.py`, `package.py`, `pipeline.py`, and the page in `src/reframe/report/design.html`.

## 8. Acceptance (P4-10)

On CardDemo run fa1f61, from the CLI only, with no AWS resources:

- all 21 maps are read and drawn, and every flow link cites lines that exist;
- every screen is in a journey or listed unused with its reason; every legacy field is mapped once;
- the prototype covers every modern screen, and every journey can be clicked from start to end;
- every capability has a specification whose citations Reframe checked; signed-off functions are final and the rest draft;
- the Claude Code form builds *Sign in* on the target stack, with its acceptance criteria recorded;
- a second round, adding a design system, one persona and a prototype download with a *Needs change*, redoes only what those touch and writes what changed;
- the README and `docs/cli.md` describe pipeline 4 from the tested commands.

## 9. The owner's decisions (25 November 2026)

| Decision | Choice |
|---|---|
| The target stack, and where it comes from | **The engineer gives it**, in the guided command or with `--stack`; Reframe never defaults one. `target-architecture.md` adds detail. |
| Which functions go final | Signed-off functions are final; every other function is included and marked draft |
| The default design system | Reframe's own plain, accessible set, drawn with no outside files; `design-system/` in the context folder replaces it. *Proposed addition for the owner's agreement (25 November 2026, from the research):* a `style-reference/` folder of house screens and code samples, which the screens and the package follow where the design system is silent |
| The name | *The design*, run with `reframe design` |

## 10. Stories

| Story | Sections |
|---|---|
| P4-01 Specification and the owner's decisions | this document |
| P4-02 Spike: the screen inventory | 4 D1 |
| P4-03 How the screens connect | 4 D2 |
| P4-04 User journeys | 4 D3 |
| P4-05 Modern screens and their mapping | 4 D4, 5 |
| P4-06 The clickable prototype | 4 D5 |
| P4-07 Final specifications | 4 D6, D8 |
| P4-08 The AI-DLC package | 4 D7 |
| P4-09 Rounds with more context | 4 D9 |
| P4-10 Live acceptance and README | 8 |
| P4-11 Golden datasets and equivalence tests | 4 D10 |
| P4-12 Risk and replacement order | 4 D11 |
| P4-13 Spike: real legacy outputs under GnuCOBOL | 4 D12 |
