# Reframe specification: the reconciliation of the two assessments (pipeline 3)

Status: agreed by the owner; stories are built from it ([the plan](plan.md), pipeline 3). The owner's decisions of 24 November 2026 are written in: the agent works on everything except identical pairs; the source code decides; rules first, then requirements; three kinds of human context. The spike P3-01 settled the decision step: what it found is in [spikes/p3-01-reconcile.md](spikes/p3-01-reconcile.md) and is written into stages R3 to R5.

## 1. Goal

After pipelines 1 and 2 have assessed the same source snapshot, and the comparison has paired their rules, Reframe:

1. accepts, without an agent, the rules both tools describe the same way;
2. has an agent reconcile every other rule against **the source code**: it merges overlapping pairs, decides conflicting ones, and checks rules only one tool found;
3. backs every decision with source lines that Reframe checks exist, and turns what the code cannot settle into a question for a subject-matter expert (SME);
4. writes one set of **recommended business rules**, each saying where it came from and why;
5. derives **recommended requirements** from those rules, in the same shape as the other two;
6. gathers the open questions of both tools and its own into **one SME list**, answering what the code or the person's context can;
7. shows it all on a reconciliation page, in the same review layout, that `reframe publish` includes.

The result is still model output. It is a recommendation for people to review; pipeline 4 makes it final.

What CardDemo gives pipeline 3 (run fa1f61): 87 identical pairs; 541 overlapping and 6 conflicting pairs, which link 547 AWS rules to only 160 Claude rules (Claude's are broader); 220 rules only AWS Transform found and 50 only Claude found, across 92 programs; 261 AWS open questions and 85 Claude rules flagged for an SME.

## 2. Scope

In scope:

- a run where pipelines 1 and 2 are done and the comparison's AI pairing is complete;
- the run's snapshot in its read-only Claude workspace, which stays in the run folder after `reframe teardown`. **Pipeline 3 needs no AWS resources**, so it can run after a teardown;
- Claude Code run headless, signed in as in pipeline 2 (the Claude subscription by default, or Amazon Bedrock);
- the person's context: documents, review marks and answered SME questions (section 4, stage R1).

Out of scope:

- changing AWS Transform's or Claude's results: they stay as they were written, and the reconciled set is a new layer beside them;
- the final rules and requirements, and wireframes: pipeline 4;
- loading the reconciled rules into Neptune (a later story, if wanted).

## 3. Commands

| Command | What it does |
|---|---|
| `reframe reconcile [--run <id>] [--context <folder>] [--auth subscription\|bedrock] [--max-batches <n>] [--foreground]` | Runs stages R0 to R7 on a run, in a background worker. `--context` is the folder of human context (stage R1). `--max-batches` is the limit for stage R4 (default 120): Reframe stops and asks if its estimate is higher. |
| `reframe reconcile --open` | Opens the reconciliation page. |

Run it again, with more context or answered questions, and only the rules whose inputs changed are decided again (stage R4, *Running again*). `reframe status`, `events`, `resume` and `publish` cover pipeline 3; the home screen shows its status per run and gets a menu entry.

## 4. Stages

Each stage records an intent before it starts and a receipt when it ends, in the run folder, so a stopped reconciliation resumes where it stopped. A Claude usage limit stops it with the reason, as in pipeline 2; `reframe resume` continues.

### Stage R0: preflight

Checked before anything runs, each failure stopping with the exact fix:

- pipelines 1 and 2 are done, and the comparison's AI pairing is complete (`complete: true`);
- the snapshot in `claude/legacy/<project>/` has the SHA-256 both pipelines assessed;
- Claude Code is installed and signed in for the chosen way;
- the context folder, if given, exists and can be read.

### Stage R1: inputs

Reframe gathers, into `reconcile/inputs/`:

- **The items.** From the comparison: every pair (with its relation: same, overlapping, conflicting), every AWS rule in no pair and every Claude rule in no pair. Each rule keeps its tool, ID, text, program and its source citation: AWS Transform's program and `traceability_lines`, or the plugin's `file:line` range.
- **The open questions** of both tools: AWS Transform's open questions and the plugin's rules marked as needing an SME.
- **The context folder**, read by kind:
  - **Documents:** Markdown and text as they are; PDF read by Claude Code; Word (`.docx`) turned into text by Reframe. Each is listed with its name and size, and none is sent anywhere but to the reconcile steps.
  - **Review marks:** the JSON files people download from the business reviews (*Download as JSON*). A file whose `source.sha256` is not this run's snapshot is ignored, and the report says so. A mark of *Needs change* or *Question*, with its comment, goes to the rule it was made on.
  - **Answered questions:** the SME list (stage R5) with its `answer` column filled in, as CSV or JSON.

### Stage R2: identical pairs

A group (stage R3) whose pairs the comparison all marked `same` becomes recommended rules without an agent: for each pair, AWS Transform's text, citing both rules and both tools' source citations, with the decision **agreed by both tools**. A *Needs change* or *Question* mark on any of its rules sends the group to stage R4 instead, and so does any pair in it that is not `same`: an identical pair whose Claude rule is also paired with other AWS rules is decided with its group. On fa1f61, 53 groups are agreed this way; the other 34 identical pairs are in groups with overlapping or conflicting pairs.

### Stage R3: estimate

The items left become **units of decision**:

- a **group**: one Claude rule with every AWS rule the comparison paired with it (overlapping or conflicting). The pairs are many-to-one, so deciding pair by pair would merge the same Claude rule again for every pair (spike finding 2). CardDemo has 160 groups, the largest with 30 AWS rules;
- a **one-sided rule**: an AWS or Claude rule in no pair.

Units are batched by program, so a batch reads one program's code once: up to 12 input rules a batch, and programs with fewer than six packed together, up to three a batch. Reframe shows the units of each kind and the batches, and goes ahead only within `--max-batches`. Four batches run at once.

On CardDemo (fa1f61): 160 groups and 270 one-sided rules, 1,011 input rules, in 113 batches. A batch takes 1 to 3 minutes and about $0.50 to $1.15 at API prices (spike P3-01), so 30 to 90 minutes four at a time, and $56 to $130 at API prices. On the Claude subscription a run can reach the five-hour usage limit; it stops with the reason and `reframe resume` continues.

### Stage R4: decisions against the source

One headless Claude step per batch, with Reframe's prompt and a JSON schema for the answer. The step can read the snapshot (read-only) and the context, and nothing else. For each unit it reads the cited source lines and what is around them, following a PERFORM, CALL or copybook where the decision depends on it, and answers with:

| Field | What it holds |
|---|---|
| `decision` | One of: `merged` (a group, made into the rules the code supports), `aws` or `claude` (one side is right), `rewritten` (both are partly wrong; the code says otherwise), `kept` (a one-sided rule the code supports), `rejected` (a one-sided rule the code does not support), `needs_sme` (the code cannot settle it) |
| `rules` | The recommended rules, each with the input rules it `covers`; as many as the behaviour needs; empty for `rejected` |
| `changed` | For `kept`: whether the rule corrects the tool's wording or facts |
| `evidence` | The `file:line` ranges in the snapshot that support the decision; at least one, except for `needs_sme` |
| `reason` | One or two sentences naming what in the code decided it |
| `confidence` | high, medium or low |
| `question` | For `needs_sme`: the question an SME can answer |
| `defect` | Code behaviour that looks unintended (a case reported wrongly, a check skipped), if any; it goes to the SME list (stage R5) |
| `context` | The context items used, if any: a document's name, a review mark, an answered question |

**How rules are written.** For business reviewers who do not read COBOL: plain business language, one sentence each in the form *WHEN <condition>, THE <system part> SHALL <behaviour>*, at most about 50 words. Values, codes and messages are given as the code has them; a field, flag or paragraph is named only in parentheses, and only where a reviewer needs it to check the rule. A behaviour with separate conditions becomes several rules, not one long one. (In the spike, merged rules written without these limits ran to 178 words with 12 code names; with them, 21 to 48 words and none.)

**The checks.** Reframe checks every answer before keeping it:

- **evidence:** every `file:line` exists in the snapshot (in the spike, all 94 citations did);
- **coverage:** every input rule of a unit is covered by at least one recommended rule, unless the decision is `rejected` or `needs_sme`;
- **keys:** every unit is answered once, with its own key.

An answer that fails is asked once more with the reason; if it still fails, the unit becomes `needs_sme`, counted and shown as such.

**Running again.** Each decision is stored with a hash of its inputs: the rules, their marks, and the context and answers it was given. On another `reframe reconcile`, a unit whose inputs are unchanged keeps its decision; only the rest are decided again. The page shows which round decided each rule.

What a unit is given is narrowed so that new context redoes only what it bears on:

- an answered question that names rules (the SME list's `rules` column) is given only to the units holding those rules; one that names no rule Reframe knows is given to every unit;
- a review mark is given to the unit holding its rule. A mark made on the reconciliation page is on a recommended rule, so it goes to every input rule that rule covers; a *Needs change* or *Question* mark on a rule agreed by both tools sends its group to an agent;
- documents are given to every unit, so a new or changed document redoes them all.

### Stage R5: one SME list

The open questions of AWS Transform, the plugin and stage R4 are merged into one list:

- questions that ask the same thing are made one, keeping where each came from (a headless step, checked so that every original question is in exactly one merged question);
- a question the context or an answered question already settles is marked answered, citing that source;
- each question names the rules it holds up;
- the possible defects stage R4 found are listed with them, as their own kind, each with its evidence, for an SME to confirm or dismiss.

It is written as `reconcile/questions.csv` (for a spreadsheet, with an empty `answer` column) and `questions.json`. Put the answered file in the context folder and run `reframe reconcile` again.

How it is built:

- **What a question holds up:** the plugin's question its rule card; an AWS Transform question the rules behind its capability's requirements; a stage R4 question the rules of its unit.
- **Merging:** questions are batched by the program of the rules they hold up (up to 40 a batch, four batches at once), so questions about the same code meet. The step reads only the questions, the documents and the answered questions, not the code. Reframe checks that every original is in exactly one merged question and that a settlement names a document or answer the step was given; a failed answer is asked once more, and if it fails again Reframe repairs it (an original in no question stands alone, one in two stays in the first, a settlement citing nothing given is removed). A batch whose questions and context are unchanged keeps its merge.
- **The columns:** `id` (SME-001, or DEF-001 for a possible defect), `kind`, `question`, `owner`, `status` (open, settled by the context, or answered), `rules` (the rules it holds up), `originals` (the original questions it stands for), `from`, `evidence` (for a defect), `settled_by`, `settled_answer`, `answer`.
- **Answers back:** an answered row is matched to a merged question by its `originals`, or by its `id` in the previous list. Its `rules` column is what stage R4 uses to give the answer only to the units it bears on (*Running again*).

### Stage R6: recommended requirements

From the recommended rules, a headless step writes requirements in the same shape as the other two: domain → business function → capability (a user story) → requirements (functional and non-functional, with their EARS pattern) → the rules behind each.

- **The frame** is AWS Transform's domains and business functions. A rule only Claude found goes where its program sits in that frame, using the comparison's alignment of programs; a program in neither tool's frame goes under *Unassigned programs*.
- Every requirement cites at least one recommended rule; one that cites none is dropped and counted.
- Rules still `needs_sme` are carried as open questions on their requirement, not left out.
- Everything is marked **recommended by Reframe from both assessments**.

How it is built: a recommended rule goes to the AWS function of the AWS rules it covers, else of the AWS rules in its unit, else the function whose programs hold its program. One headless step per function (in parts of up to 60 rules) writes capabilities and requirements from that function's rules only, without reading the code. A unit still `needs_sme` is carried as an open question on the capability the step places it on, with its SME list ID; one the step does not place is carried on a capability *Waiting for a subject-matter expert*. A function whose rules and open units are unchanged keeps its requirements. The rules are written to `outputs/reconcile/rules.json` and the requirements to `outputs/reconcile/requirements.json`.

### Stage R7: reconciliation page

`outputs/reconcile/index.html`, in the review layout:

- **Overview:** how many rules were agreed, merged, decided for each tool, rewritten, kept, rejected and waiting for an SME, the possible defects, and the rounds that decided them;
- **Each rule:** the recommended text; the AWS and Claude originals side by side; the decision, reason, confidence and evidence (the cited lines shown from the snapshot); the context it used;
- **Requirements**, as in the other reviews;
- **The SME list**, with what each question holds up;
- Agree / Needs change / Question marks, and the same CSV and JSON downloads. These are the review marks the next round, or pipeline 4, reads.

The comparison page links to it. `reframe publish` includes it as `reconciled/` in the copy, cleaned the same way, and the copy's index page gets a fourth card.

How it is built: the page uses the same template as the two reviews, so marks, search, the technical tables and the downloads work the same way; its marks are kept apart from theirs. A recommended rule's key is `rec/<unit>/<n>`, which is how a mark made here reaches the next round (*Running again*). Each cited range is shown from the snapshot, up to 40 lines. The SME list is a tab of the technical detail, with a filter by kind and status and a CSV download in the shape of `reconcile/questions.csv`. When the page is built, the AWS Transform review, Claude's review and the comparison are built again so that each links to it. The home screen gets two entries, *Reconcile the two assessments* and *Open the reconciliation*, and a Reconcile column.

## 5. Run folder

In addition to pipelines 1 and 2:

- `reconcile/inputs/`: the items, open questions and the context as read (stage R1);
- `reconcile/decisions.json`: each unit's decision, with its input hash and round; `reconcile/steps.json`, the decision steps' time and usage; `reconcile/agreed.json`;
- `reconcile/questions.csv`, `questions.json`, and the merges they came from (`sme-merges.json`, `sme-steps.json`);
- `outputs/reconcile/`: the recommended rules, the recommended requirements and the page.

## 6. Code layout

`src/reframe/reconcile/`: inputs and context reading, the identical pairs, batching and the estimate, the decision step and evidence check, the SME list, the requirements, the page. It uses pipeline 2's Claude Code runner and workspace. `src/reframe/report/` gains the reconciliation page and its place in `publish`.

## 7. Acceptance

Pipeline 3 is done when, from the CLI only, on CardDemo run fa1f61 (already torn down):

- `reframe reconcile` with a context folder holding one document, one review export and one answered question runs to the end, within its estimate;
- every recommended rule has a decision; every decision other than `needs_sme` has evidence that exists in the snapshot, and every input rule is covered, rejected or waiting for an SME;
- groups of identical pairs only are agreed without an agent, and the 6 conflicts are each decided or turned into a question;
- the snapshot's SHA-256 is unchanged at the end;
- the SME list holds every original open question exactly once, merged or not;
- running it again with one more answered question decides only the affected rules again;
- the reconciliation page opens, links to both reviews, and is in a `reframe publish` copy.

### Results (P3-10, 24 November 2026)

Every point passed on fa1f61, from the CLI, on the Claude subscription. The context folder held a glossary, a review export with one *Question* mark on a Claude rule whose group the two tools describe the same way, and an answered AWS Transform question (OQ-008).

| Point | Result |
|---|---|
| Runs to the end within its estimate | Round 1: estimate 113 batches, 29 to 87 minutes, $56 to $130 at API prices; it stopped once at the usage limit during the requirements and `reframe resume` finished it. About $52 for the decisions (120 steps with retries) and $15 for the SME list and requirements, about $67 in all |
| Decisions, evidence and coverage | 431 units decided: 158 merged, 266 kept, 3 rejected, 2 rewritten, 1 for Claude's plugin, 1 waiting for an SME. 26 needed a second ask and 1 fell back to an SME question. Every cited range exists in the snapshot; all 1,111 input rules are covered, rejected or waiting for an SME |
| Identical pairs; the conflicts | 51 rules in 46 groups agreed without an agent; the marked group was sent to an agent instead. The 6 conflicts: 5 merged, 1 rewritten from the code |
| The snapshot | Its SHA-256 unchanged |
| The SME list | 349 original questions, each exactly once, in 313 questions, with 187 possible defects; the glossary settled one |
| Running again | With one more answered question (OQ-005), round 2 decided again only the 5 units holding the rules the answer names, in 2 batches (about $1), and kept 426; both answers are marked answered on the SME list and cited in the decisions |
| The page | 1,204 recommended rules and 1,153 requirements (none dropped); it opens with `reframe reconcile --open`, links to both reviews and the comparison, and is `reconciled/` in a `reframe publish` copy with a fourth card |

Found and fixed in the run: an answer giving the tool's question code (OQ-008) was not matched to its question, since codes repeat from one function to the next (it now matches by code and one of the question's rules); a resumed round replaced its estimate with what was left of it (a round now keeps its first estimate); and the header said "no context folder" when a request kept the one given before.

