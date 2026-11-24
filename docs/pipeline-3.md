# Reframe specification: pipeline 3, reconciling the two assessments

Status: draft for the owner's agreement. Stories are built from it ([the plan](plan.md), pipeline 3). The owner's decisions of 24 November 2026 are written in: the agent works on everything except identical pairs; the source code decides; rules first, then requirements; three kinds of human context.

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

What CardDemo gives pipeline 3 (run fa1f61): 87 identical pairs, 541 overlapping pairs, 6 conflicting pairs, about 220 rules only AWS Transform found, about 50 only Claude found, 261 AWS open questions and 85 Claude rules flagged for an SME.

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
| `reframe reconcile [--run <id>] [--context <folder>] [--auth subscription\|bedrock] [--max-batches <n>]` | Runs stages R0 to R7 on a run, in a background worker. `--context` is the folder of human context (stage R1). `--max-batches` is the limit for stage R4 (default 120): Reframe stops and asks if its estimate is higher. |
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

A pair the comparison marked `same` becomes one recommended rule without an agent: AWS Transform's text, citing both rules and both source citations, with the decision **agreed by both tools**. A *Needs change* or *Question* mark on either rule moves the pair to stage R4 instead.

### Stage R3: estimate

The items left are grouped by program, about 12 to a batch, so a batch reads one program's code once. Reframe shows the number of items of each kind and the batches, and goes ahead only within `--max-batches`. On CardDemo that is about 820 items in about 70 batches.

### Stage R4: decisions against the source

One headless Claude step per batch, with Reframe's prompt and a JSON schema for the answer. The step can read the snapshot (read-only) and the context, and nothing else. For each item it reads the cited source lines and what is around them, then answers with:

| Field | What it holds |
|---|---|
| `decision` | One of: `merged` (an overlapping pair, made one), `aws` or `claude` (one side is right), `rewritten` (both are partly wrong; the code says otherwise), `kept` (a one-sided rule the code supports), `rejected` (a one-sided rule the code does not support), `needs_sme` (the code cannot settle it) |
| `rule` | The recommended rule text, in the EARS style AWS Transform uses; empty for `rejected` |
| `evidence` | The `file:line` ranges in the snapshot that support the decision; at least one, except for `needs_sme` |
| `reason` | One or two sentences naming what in the code decided it |
| `confidence` | high, medium or low |
| `question` | For `needs_sme`: the question an SME can answer |
| `context` | The context items used, if any: a document's name, a review mark, an answered question |

**The evidence check.** Reframe checks every `file:line` exists in the snapshot. A decision whose evidence does not exist is asked once more with the reason; if it still fails it becomes `needs_sme`, counted and shown as such.

**Running again.** Each decision is stored with a hash of its inputs: the rules, their marks, and the context and answers it was given. On another `reframe reconcile`, a batch whose items' inputs are unchanged keeps its decisions; only the rest are decided again. The page shows which round decided each rule.

### Stage R5: one SME list

The open questions of AWS Transform, the plugin and stage R4 are merged into one list:

- questions that ask the same thing are made one, keeping where each came from (a headless step, checked so that every original question is in exactly one merged question);
- a question the context or an answered question already settles is marked answered, citing that source;
- each question names the rules it holds up.

It is written as `reconcile/questions.csv` (for a spreadsheet, with an empty `answer` column) and `questions.json`. Put the answered file in the context folder and run `reframe reconcile` again.

### Stage R6: recommended requirements

From the recommended rules, a headless step writes requirements in the same shape as the other two: domain → business function → capability (a user story) → requirements (functional and non-functional, with their EARS pattern) → the rules behind each.

- **The frame** is AWS Transform's domains and business functions. A rule only Claude found goes where its program sits in that frame, using the comparison's alignment of programs; a program in neither tool's frame goes under *Unassigned programs*.
- Every requirement cites at least one recommended rule; one that cites none is dropped and counted.
- Rules still `needs_sme` are carried as open questions on their requirement, not left out.
- Everything is marked **recommended by Reframe from both assessments**.

### Stage R7: reconciliation page

`outputs/reconcile/index.html`, in the review layout:

- **Overview:** how many rules were agreed, merged, decided for each tool, rewritten, kept, rejected and waiting for an SME, with the rounds that decided them;
- **Each rule:** the recommended text; the AWS and Claude originals side by side; the decision, reason, confidence and evidence (the cited lines shown from the snapshot); the context it used;
- **Requirements**, as in the other reviews;
- **The SME list**, with what each question holds up;
- Agree / Needs change / Question marks, and the same CSV and JSON downloads. These are the review marks the next round, or pipeline 4, reads.

The comparison page links to it. `reframe publish` includes it as `reconciled/` in the copy, cleaned the same way, and the copy's index page gets a fourth card.

## 5. Run folder

In addition to pipelines 1 and 2:

- `reconcile/inputs/`: the items, open questions and the context as read (stage R1);
- `reconcile/decisions/`: each batch's answer, with its input hash and round;
- `reconcile/questions.csv`, `questions.json`;
- `outputs/reconcile/`: the recommended rules, the recommended requirements and the page.

## 6. Code layout

`src/reframe/reconcile/`: inputs and context reading, the identical pairs, batching and the estimate, the decision step and evidence check, the SME list, the requirements, the page. It uses pipeline 2's Claude Code runner and workspace. `src/reframe/report/` gains the reconciliation page and its place in `publish`.

## 7. Acceptance

Pipeline 3 is done when, from the CLI only, on CardDemo run fa1f61 (already torn down):

- `reframe reconcile` with a context folder holding one document, one review export and one answered question runs to the end, within its estimate;
- every recommended rule has a decision; every decision other than `needs_sme` has evidence that exists in the snapshot;
- the 87 identical pairs are agreed without an agent, and the 6 conflicts are each decided or turned into a question;
- the snapshot's SHA-256 is unchanged at the end;
- the SME list holds every original open question exactly once, merged or not;
- running it again with one more answered question decides only the affected rules again;
- the reconciliation page opens, links to both reviews, and is in a `reframe publish` copy.
