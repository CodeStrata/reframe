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
| `reframe review [--run <id>] --context <folder>` | Reads the review downloads in a folder and shows each reviewer's coverage, sign-offs and where reviewers disagree (section 8.11); runs nothing. |

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
- `reconcile/decisions.json`: each unit's decision, with its input hash and round; `reconcile/steps.json`, the decision steps' time and usage; `reconcile/agreed.json`, and `reconcile/described.json`, the agreed rules' description (section 8.4);
- `reconcile/reviews.json`: the review downloads `reframe review` read (section 8.11);
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


## 8. Part 2: accuracy and the review loop

Part 2 (P3-11 to P3-24 in the plan) starts by measuring how accurate the recommended rules are (section 8.1). The other stories, specified from what the audit found, are in sections 8.2 to 8.12.

### 8.1 The accuracy audit (P3-11)

The evidence check of R4 proves that the cited lines exist, not that they support the rule. The audit measures that, on a sample, with two judges that did not decide the rules and do not see how they were decided.

**Command.** `python -m reframe.reconcile.audit [--run <run>] [--size 60] [--seed 1]`, on a run whose reconciliation is done. It needs no AWS resources and reads the snapshot only. It writes to `reconcile/audit/` in the run folder; a second run reuses the sample and every judgment already made, so it continues after a usage limit and costs nothing once complete.

**The sample.** Drawn once, with a fixed seed, across the decision kinds, so that the rare kinds are checked at all:

| Kind | Items |
|---|---|
| Agreed without an agent | 8 |
| Merged | 20 |
| Kept, found only by AWS Transform | 12 |
| Kept, found only by Claude | 8 |
| Rewritten from the code | 6 |
| Claude's rule chosen | all (2 on CardDemo) |
| Rejected (the input rule that was rejected) | all (3 on CardDemo) |

A kind with fewer rules than its share gives all it has. The `needs_sme` units are left to the SME. A possible-defect note belongs to a unit, not a rule, so it is judged once, with the first sampled rule of its unit.

**The judges.** Two headless Claude Code steps judge every item on their own, each with read-only access to the snapshot: the model that decided the rules (Opus 5.5 on CardDemo) in a fresh session, and a different model (Sonnet 5.5). Each judge is given an item's rule, the source lines it cites, the input rules it stands for and the other rules made from them (its siblings). It is not given the decision, reason, confidence or the other judge's answer. Items are judged in batches of up to 6, a program's items together and small programs packed, at most 4 batches at a time. The judge answers:

- `verdict`, on how the system behaves when it runs: `correct` (every statement is true of what the code does), `minor` (true in substance, with a wrong or missing detail: a value, a condition, a message), `wrong` (the code does not do this, a condition or behaviour is materially different, or the code the rule describes can never run) or `unsure` (the source cannot settle it);
- `evidence`: `supports`, `partly` or `no`, for the rule's cited lines;
- `lost`: a true detail of the input rules that neither the rule nor its siblings states, or empty;
- `defect` (where the item has a note): `real`, `not_a_defect` or `unsure`;
- a reason and the lines it read, which Reframe checks exist in the snapshot. An answer that fails the check is asked for once more, then recorded as `unsure`.

For a rejected item the input rule itself is judged: a `wrong` or `unsure` verdict means the rejection stands.

**Settling.** Where the two judges give different verdicts, or different defect answers, the item goes to `reconcile/audit/settle.csv` with both answers and an empty `owner` column for the owner to fill in. Items the judges agree on take their shared answer.

**The figures** (`reconcile/audit/audit.json`, and the results below): per decision kind and overall, the share of items `correct`, `correct` or `minor`, and `wrong`; how often the judges agreed; the confidence of the items found `minor` or `wrong`; the share of defect notes found `real`; and the time and cost of each judge.

### Results (P3-11, 25 November 2026)

On CardDemo run fa1f61: 59 items (56 recommended rules and the 3 rejected input rules), judged by Opus 5.5 in a fresh session and by Sonnet 5.5, on the Claude subscription. Both judges took about 7 to 9 minutes; together they cost about $8 at API prices. Seven items wait for the owner's settling, so the figures below give the judges' shared answers and, for the disputed items, a range.

| Kind | Items | Both judges: correct | Disputed | Both judges: wrong |
|---|---|---|---|---|
| Agreed without an agent | 8 | 6 | 2 | 0 |
| Merged | 20 | 20 | 0 | 0 |
| Kept, found only by AWS Transform | 12 | 10 | 2 | 0 |
| Kept, found only by Claude | 8 | 7 | 1 | 0 |
| Rewritten from the code | 6 | 6 | 0 | 0 |
| Claude's rule chosen | 2 | 2 | 0 | 0 |
| **Recommended rules** | **56** | **51 (91%)** | **5** | **0** |
| Rejected input rules | 3 | – | 0 | 3: every rejection upheld |

- **Accuracy.** Between 51 and 56 of the 56 recommended rules are correct (91% to 100%), and no rule was judged wrong by both judges. The 5 disputed rules are a wrong or missing detail in 3 cases and, in 2, behaviour that does not happen when the code runs: a menu branch no menu entry reaches, and a load job whose job card carries `TYPRUN=SCAN`, so it is only syntax-checked. With 56 items this is a sample: the share of correct rules in the whole set could be lower by about 10 points.
- **Where the errors are.** Merged and rewritten rules, the ones an agent decided against the code with both tools' rules in front of it, were all correct (26 of 26). The disputed rules are rules both tools described the same way, which no agent checked, and rules only one tool found. Two tools agreeing is not proof.
- **Rejections.** All 3 were right: each rejected rule describes code that can never run.
- **Confidence.** Every sampled rule is rated high, the disputed ones included, so confidence says nothing about which rules to check (P3-12).
- **Possible defects.** Of the 27 unit notes judged, both judges found 24 real, 1 not a defect, and 2 are disputed. The notes are mostly right. The earlier count of 636 rules with a note came from each unit's note being repeated on every rule of the unit; 187 of the 431 units have one. P3-13 therefore becomes showing each note once, on its unit, and telling real defects from deliberate behaviour, rather than cutting their number.
- **The judges.** They agreed on 54 of the 59 verdicts and on 25 of the 27 defect answers. Both are Claude models, so they are independent of the decisions but not of each other's training; a judge from another model family would be a stronger check.
- **The audit's own questions.** A first pass, kept as `reconcile/audit-v1/`, showed three ways the questions misled the judges: a rule describing code that can never run was judged `correct`, which made right rejections look wrong; one rule of a unit split in two was said to lose the other half; and a unit's defect note was judged on every sampled rule of the unit. The method above fixes all three.

**Settled (25 November 2026).** The owner settled the 7 disputed items in `settle.csv`. Of the 56 recommended rules, 51 are correct (91%), 3 have a wrong or missing detail and 2 are wrong; 54 of 56 (96%) are correct in substance. The 3 with a wrong detail are one rule agreed without an agent and two kept from one tool. The 2 wrong rules both describe code that never runs: a rule agreed without an agent about a menu branch no menu entry reaches, and a kept AWS Transform rule about a load job whose job card carries `TYPRUN=SCAN`. Of the 27 defect notes, 25 are real, 1 is not a defect and 1 is unsure. Every sampled rule was rated high. Sections 8.2 to 8.11 follow from these figures.

### 8.2 What part 2 changes, and where the ideas came from

The audit shows three things the review needs: which rules to check first (confidence says nothing today), whether the code a rule describes ever runs, and fewer, clearer items for an SME (1,204 rules and 2,358 items to mark). Part 2 adds, to every recommended rule, what a reviewer needs to judge it quickly: how far to trust it, what kind of rule it is, and worked examples. It adds decision tables and a risk level to each capability, a *Review first* view, sign-off by function, and a review loop that reads marks on every item, from any number of reviewers, in either download.

The rule kinds, worked examples, decision tables and risk levels come from public demonstrations of spec-driven mainframe modernization, whose business-rule, test and UI role files ask for each rule's kind, examples and decision table, and rank capabilities by risk. Reframe keeps what those demonstrations lack: every statement is checked against the source.

Every rule is decided again in the first round after part 2: the decision step's prompt and schema change, so Reframe adds a method version to each unit's input hash (stage R4, *Running again*) and to each function's (stage R6). On CardDemo that is one full round (stage R3's estimate: about 113 batches).

### 8.3 The decision step's answer (P3-12, P3-13, P3-21, P3-22)

Stage R4's answer for each unit gains these fields; the checks in stage R4 apply to them, and an answer that fails is asked once more as before.

| Field | What it holds | Checked |
|---|---|---|
| `reachable` | Whether the code the unit's rules describe runs: `yes`, `no` or `unknown` | `yes` needs `entry` |
| `entry` | The lines that show how the code is reached: the menu entry, transaction, `XCTL`/`LINK`/`CALL`, or the job step (not `TYPRUN=SCAN`, not commented out) that runs it | Every range exists in the snapshot |
| `depends` | What the behaviour depends on outside the source (data, configuration, a program not in the source), or empty | – |
| `defect` | `{text, call, evidence}`: the possible defect, whether it looks `unintended` or `deliberate`, and the lines that show which | A `text` needs a `call` and evidence that exists |
| `rules[].kind` | Each recommended rule's kind (section 8.6) | One of the kinds |
| `rules[].examples` | One to three worked examples per rule (section 8.7) | Section 8.7 |

The prompt says: check that the code can run. A paragraph is reached from the program's entry, a program from a menu entry, transaction or a job step that runs. A rule describing code that can never run is `rejected`. A group may now be `rejected` when the code both tools describe never runs. A unit whose answer says `reachable: no` with any other decision fails the check.

### 8.4 Rules both tools describe the same way

The owner's decision stands: identical pairs are agreed without an agent deciding them (stage R2). They still need the description every other rule has, and the audit found one of them wrong. So one more step, **R2b**, describes them without deciding them. Agreed rules are batched by program, up to 12 a batch and four batches at once, and a headless step reads each rule's cited lines and answers `reachable`, `entry`, `depends`, `kind` and `examples`. It answers no `decision` and does not change the wording. The checks of section 8.3 apply. A rule the step finds `reachable: no` stays agreed, is rated low (section 8.5), and is listed first in *Review first*. On CardDemo: 51 rules, about 5 batches, about $5 at API prices.

### 8.5 Confidence that means something (P3-12)

Reframe sets each recommended rule's confidence from facts it can check, not from the model's word. The model's own rating is kept as `model_confidence`.

| Confidence | When |
|---|---|
| **high** | An agent decided it against the code with both tools' rules in front of it (`merged`, `aws`, `claude`, `rewritten`), and the code is `reachable: yes` with an `entry` that exists |
| **medium** | It was kept from one tool (`kept`), or agreed without an agent (section 8.4), or `reachable` is `unknown` |
| **low** | An agreed rule whose code never runs (section 8.4), or a unit that fell back to an SME question |

Why these lines: in the audit every rule an agent decided with both tools' rules was correct (26 of 26), and every error was a rule agreed without an agent or kept from one tool. The two wrong rules described code that never runs.

What the behaviour depends on outside the source (`depends`) is shown with the rule. It does not lower the confidence of a rule whose code is shown to run. The first round after part 2 rated 70% of CardDemo's rules medium, and 580 of those were medium only because the step named a dependency, often ordinary input data. The prompt now asks only for what decides the behaviour from outside the source: configuration, a control or reference table loaded at run time that chooses the path, or a program not in the source.

**Done when** the units of the five audit items that were not correct (A02, A03, A31, A32, A41) are rated medium or low, or are rejected, in the first round after part 2. The audit's figures by confidence (section 8.12) show the errors in the lower levels.

### 8.6 What kind of rule (P3-21)

Each recommended rule has one kind, so a business reader can start with business rules and leave formatting and technical steps to developers.

| Kind | What it is |
|---|---|
| `business` | A business decision, policy or calculation: who may do what, how an amount is worked out |
| `validation` | A check on input data, with the message given when it fails |
| `error_handling` | What happens when something fails: a file status, an abend, a rollback |
| `display` | What a screen or report shows and how: layout, formatting, messages that are not validation |
| `technical` | A technical step: opening a file, moving data between records, sorting, restart and checkpoint |
| `side_effect` | A record of what happened: an audit or log record, a counter, a file written for another system |
| `compliance` | Security and access control, the handling of card or personal data, a regulatory record |
| `leftover` | Behaviour that runs but serves no purpose today: a field never read, an option that leads nowhere |

The page shows the kind on each rule and can filter by it. *Review first* and the business pages list `business`, `validation` and `compliance` rules first.

### 8.7 Worked examples (P3-22)

Each recommended rule has one to three worked examples, each a `given` (the inputs, as field and value) and a `then` (the outcome). They use the values, codes and messages the code has, so a reviewer can check a rule against a case they know. The same examples become acceptance criteria in the exports (S-13) and test data in pipeline 4.

**The check.** Every quoted value in an example (a message, a code in quotes) must appear in a file the decision cites. Numbers are not checked: an example may use any amount. An example that fails is removed and counted on its own rule (P3-27), so a rule with no examples always says how many were removed. A rule whose examples all fail keeps its decision, with no examples, so a bad example never sends a unit to an SME. The decision step must give every rule at least one example. Decisions made before P3-27 keep their unit's count on the unit's first rule until the unit is decided again.

The page shows the examples under each rule as *For example*: given → then.

### 8.8 Possible defects once, real or deliberate (P3-13)

A possible defect belongs to the unit that found it, not to each of its rules. The page shows each note once, on the unit's first rule, with *applies to the N rules of this decision*. It shows the call, *looks unintended* or *looks deliberate*, and the lines that show it.

On the SME list a defect becomes one entry of kind `defect`, with its call. An unintended one asks "Is this intended?". A deliberate one asks "Confirm this is deliberate". The entry cites the defect's evidence. The audit judges the call: `real` means unintended, `not_a_defect` means deliberate or not happening.

### 8.9 Decision tables and risk, per capability (P3-23, P3-24)

Stage R6's step writes two more things for each capability, from the rules it was given:

- **Decision tables (P3-23).** Where three or more of a capability's rules share their conditions, a table with the conditions as columns and one row per combination, each row giving its outcome and the rule it comes from. A combination no rule covers is listed under the table as a gap, for an SME. Reframe checks that every row cites a rule the step was given; a row that cites none is dropped, and a table left with no rows is dropped.
- **Risk (P3-24).** What the capability touches, from a fixed list: `money` (amounts, balances, interest, fees), `card_data`, `personal_data`, `security` (sign-on, access), `audit`, `updates_records` (writes to master data), `reporting_only`. Reframe sets the risk from these, not the model: **high** if it touches money, security or audit, or holds a `compliance` rule; **medium** if it holds card or personal data or updates records; **low** otherwise. A function's risk is its highest capability's. (Card and personal data were high at first, which rated every CardDemo function high: in a card system nearly everything holds card data.)

The capability page shows its tables, gaps and risk. The function and domain cards show the risk, and the overview counts functions by risk. *Review first* and sign-off take high-risk functions first. Pipeline 4 uses the order to propose what to modernize first.

### 8.10 Review first (P3-14)

The reconciled review opens with a *Review first* view. It lists the items an SME should check before the rest, in this order:

1. rules whose code never runs (low);
2. conflicts: rules from a unit with a conflicting pair;
3. rules rewritten from the code;
4. units waiting for an SME;
5. possible defects that look unintended;
6. rules kept from one tool;
7. the other medium-confidence rules.

Within each group, items from high-risk capabilities come first (a rule takes the risk of the first capability whose requirements cite it), and `business`, `validation` and `compliance` rules before the other kinds. Capability risk is used rather than function risk because a function takes its riskiest capability's: on CardDemo 10 of 11 functions are high, against 74 of 153 capabilities. Each group shows its count and how many are marked. Filters choose decision kind, rule kind, confidence and capability risk. On CardDemo, after the recalibration, the view lists the 467 medium and low rules and the open items. The 718 high-confidence rules need not be opened to finish it.

### 8.11 The review loop (P3-15 to P3-19, P3-25)

**Sign-off by function (P3-15).** Every review page (AWS Transform's, Claude's and the reconciled review) has a *Sign off this function* button on each function, with an optional comment. A sign-off records the reviewer's name and the time. The downloads carry the sign-offs: the JSON has a `signoffs` list, and the CSV has one row of type `sign-off` per function. The reconciliation reads them from the context folder. `reframe status` lists the signed-off functions, by page, with who signed and when. The reconciled review shows a *Signed off by* tag on the function and its card. A sign-off on another snapshot's review is ignored, like its marks. Pipeline 4 takes signed-off functions as final.

**Marks on requirements and capabilities (P3-16).** The reconciled review's capabilities can be marked too. A *Needs change* or *Question* mark on a requirement or a capability, with its comment, goes to the requirements step of its function in the next round. The step is given the marked item's previous text and the comment, and told to address it where the rules support it. That function's requirements are written again; no unit is decided again for such a mark, and no other function changes.

**The CSV download read (P3-17).** The CSV download gains a `key` column. A CSV with the review columns (`key`, `status`, `source_sha256`) in the context folder is read like the JSON download. One whose `source_sha256` is another snapshot's is ignored with that reason. One without a `key` column (downloaded before part 2) is ignored, with the reason "download it again from the page".

**Agree keeps a rule (P3-18).** A recommended rule marked *Agree* on the reconciled review is kept as agreed:

- A unit whose recommended rules were all marked *Agree* keeps its decision in later rounds, even when a document changes. Only a later *Needs change* or *Question* mark on one of its rules, or a change to its input rules or to an answer that names them, reopens it.
- A unit decided again with some rules agreed gives those rules to the step as *agreed by a reviewer: keep this wording unless the code contradicts it*.
- A requirement marked *Agree* is kept word for word by Reframe while the rules it cites are unchanged. The step is told those rules are already covered.

**What nobody marked is kept (P3-26).** When a function's requirements are written again, for a mark or because its rules changed, every requirement of the previous version that no reviewer marked *Needs change* or *Question*, and that is not in a capability so marked, is kept word for word with its code, in its capability with that capability's story, touches and decision tables, while every rule it cites is unchanged and still in the function. The step is told those rules are already covered and writes requirements only for the rest: the marked items, the marked capabilities' requirements, and rules that are new or changed. A reviewer's earlier marks therefore still point at the text they marked. On CardDemo in P3-20, before this, a function written again for one requirement and one capability reworded 34 of its 36 requirements. Replayed on the same round, P3-26 keeps 30 word for word and writes 6 again: the 5 of the capability asked about, and the one whose rule round 4 decided again.

The page shows *Agreed by <name>, <date>* on each agreed item.

**Several reviewers (P3-19).** `reframe review [--run <id>] --context <folder>` reads every review download in the folder, without running anything, and shows:

- each reviewer's file, page and snapshot;
- their marks by status;
- their coverage of that page's items;
- their sign-offs;
- the items two reviewers marked differently, with each mark and comment.

It writes `reconcile/reviews.json`. The next round combines every reviewer's marks. *Needs change* and *Question* take precedence over *Agree*. Comments from every reviewer are kept, each prefixed with the reviewer's name.

**Reviews of a published copy (P3-25).** A reviewer who has no Reframe marks the copy that `reframe publish` made. That copy replaces each AWS Transform ID with a stand-in (`id-` and ten hex digits), and the IDs appear in keys: AWS Transform's rule keys, and the reconciled review's keys built from them (`rec/aws:<domain>/<function>/<ID>/1`). So the download names those items differently from the run. The next round and `reframe review` read such downloads: before combining, each mark's key and each sign-off's function are named as the run names them, for every item on AWS Transform's, Claude's and the reconciled review (requirements, rules, open questions, capabilities and functions). A mark or sign-off made on a published copy then counts exactly as the same one made on the run's own page: it reaches the next round, it shows as *Agreed by* or *Signed off by* on the reconciled review, and `reframe review` counts it in the reviewer's coverage.

### 8.12 Acceptance of part 2 (P3-20)

Part 2 is done when, from the CLI only, on CardDemo run fa1f61:

- **Round 3** (the first after part 2) decides every unit again within its estimate. Every recommended rule has a kind, a confidence set by Reframe, and examples that passed their check or a count of those removed. Every unit has `reachable` with an `entry` that exists, or a reason.
- **The audit**, re-run on a new sample (`--seed 2`), with the P3-11 audit kept as `reconcile/audit-p3-11/`, shows:
  - no fewer correct rules than P3-11's 91%;
  - no wrong rule rated high;
  - the five P3-11 items that were not correct (section 8.5) now medium, low or rejected;
  - the judges agreeing with the defect calls.
- **Possible defects**: each is shown once on the page, and the SME list's defect entries match the units' notes one to one.
- **Two reviewers' files**, one JSON and one CSV, carry marks, sign-offs, a *Needs change* on a requirement, a disagreement and an *Agree* on a whole unit. `reframe review` shows their coverage and the disagreement. **Round 4** decides again only the marked units, writes again only the marked function's requirements, keeps the agreed unit, and shows the sign-offs in `reframe status` and on the page.
- The README and `docs/cli.md` describe part 2 from the tested commands.

### Results (P3-20, 25 November 2026)

On CardDemo run fa1f61, from the CLI, on the Claude subscription, with no AWS resources.

**Round 3**, the first after part 2, decided all 431 units again. The estimate was 113 batches, 29 to 87 minutes and $56 to $130 at API prices. The round stopped once at Claude's usage limit and `reframe resume` finished it: about 52 minutes of work, and about $32 at API prices by the step logs.

| | Round 3 |
|---|---|
| Recommended rules | 1,185 from 1,014 input rules (P3-10: 1,204 from 1,111) |
| Confidence set by Reframe | 718 high, 463 medium, 4 low (P3-10: 1,182 high). The model's own rating is kept beside it: 1,140 high, 45 medium |
| Kinds | validation 268, business 267, technical 256, error handling 169, display 167, compliance 30, leftover 16, side effect 12 |
| Code runs | 1,166 rules reached from lines that exist, 4 never run, 15 not shown by the source |
| Worked examples | 1,273 kept, 330 removed by the check |
| Possible defects | 182 unit notes (P3-10: 187), each shown once, matching the SME list's 182 defect entries one to one |
| Requirements | 1,131 in 153 capabilities, 114 decision tables; 10 functions high risk, 1 medium |

A unit's count of removed examples is kept on its first rule only. So in 115 units, a later rule whose examples were all removed shows neither examples nor a count; in 5 more, the step gave a rule no example.

**The five P3-11 errors** are all lower now: A02 (agreed, wrong detail) medium; A03 (a menu branch no entry reaches) low, with the code found never to run; A31 and A41 (kept from one tool, wrong detail) medium; A32 (a job under `TYPRUN=SCAN`) rejected.

**The audit** on a new sample (`--seed 2`, the P3-11 audit kept as `reconcile/audit-p3-11/`) judged 76 items: 65 recommended rules and 11 rejected input rules. Opus 5.5 and Sonnet 5.5 took about 10 minutes and $10 at API prices.

| Kind | Items | Both judges: correct | Minor | Disputed |
|---|---|---|---|---|
| Agreed without an agent | 8 | 6 | 1 | 1 |
| Merged | 20 | 19 | 0 | 1 |
| Kept, found only by AWS Transform | 12 | 8 | 2 | 2 |
| Kept, found only by Claude | 8 | 7 | 0 | 1 |
| Rewritten from the code | 6 | 6 | 0 | 0 |
| Claude's rule chosen | 11 | 10 | 0 | 1 |
| **Recommended rules** | **65** | **56 (86%)** | **3** | **6** |
| Rejected input rules | 11 | 10 upheld | | 1 |

- No rule was judged wrong by both judges. Between 56 and 62 of the 65 are correct (86% to 95%), and 59 to 65 correct or minor; the target of 91% needs 4 of the 6 disputed rules settled correct.
- Every rule with a minor error is rated medium. Of the 6 disputed, 2 are rated high and 4 medium; P3-11 had every sampled rule rated high.
- The judges agreed on 20 of 21 defect calls (22 notes real, 2 not a defect, 3 disputed).
- Nine items wait for the owner in `reconcile/audit/settle.csv`; running the audit again then gives the final figures at no cost.

**Two reviewers.** Pat's JSON download agrees with every rule of one merged unit (4 rules) and with one kept rule, marks a requirement *Needs change* and signs off a function. Sam's CSV download asks a *Question* on the same kept rule and on a capability, and signs off another function. All the marks are in one function, Account Statement Generation and Delivery. `reframe review` showed both reviewers, their sign-offs and the one disagreement, combined as a *Question*.

**Round 4** estimated 1 batch for 1 unit and decided only the disputed unit again, keeping 430. The unit agreed in full kept its round 3 decision word for word. Only the marked function's requirements were written again: its 7 capabilities became 8 (the one asked about was split in two), 36 requirements became 41, and the requirement marked *Needs change* kept its text, since its rules (a sort step with no screen) do not support the comment. The other 34 were reworded although nobody marked them. Both sign-offs show in `reframe status` and on the page.

**Open after P3-20.** The owner settles the nine audit items. Two changes follow from the figures: keep the unmarked requirements of a function that is written again word for word while their rules are unchanged, so reviewers' earlier marks still apply; and keep the count of removed examples on each rule.
