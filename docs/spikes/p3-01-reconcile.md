# Spike P3-01: deciding rules against the source

Story P3-01, 24 November 2026. The question: can a headless Claude step decide pipeline 3's items against the source code, with evidence Reframe can check, at a cost a CardDemo run can bear? Run on CardDemo run fa1f61, with the script [p3-01-reconcile.py](p3-01-reconcile.py), on the Claude subscription. It is not product code.

## What was run

Three batches, chosen from fa1f61's 817 pipeline 3 items (541 overlapping pairs, 6 conflicting pairs, 220 AWS-only rules, 50 Claude-only rules, across 92 programs):

| Batch | Program | Items | Kinds |
|---|---|---|---|
| 1 | CBTRN03C | 6 | the conflict, overlapping pairs, one rule from each tool alone |
| 2 | COACTUPC | 12 | overlapping pairs |
| 3 | COCRDUPC | 12 | 6 Claude-only and 6 AWS-only rules |

Each batch was one `claude -p` step in pipeline 2's workspace (the snapshot read-only), with a prompt and a JSON schema for the answer, then Reframe's evidence check: every cited `file:line` must exist in the snapshot. Batch 2 was run twice, the second time with the prompt and schema revised after round 1.

## Results

| Batch | Time | Tokens (output / cache read / cache write) | API-equivalent cost | Decisions | Evidence check |
|---|---|---|---|---|---|
| 1 | 56 s | 5.0k / 187k / 47k | $0.51 | 3 merged, 1 AWS right, 2 kept | all exist |
| 2 | 128 s | 12.6k / 439k / 67k | $0.88 | 11 merged, 1 AWS right | all exist |
| 3 | 74 s | 7.3k / 254k / 39k | $0.51 | 12 kept, each corrected | all exist |
| 2, round 2 | 171 s | 16.9k / 522k / 89k | $1.15 | 12 merged, as 36 rules | all exist |

Every item was answered with its own key, and the 94 citations of round 1 all exist. No item needed an SME: the code settled all 30.

**The decisions are right where they were checked by hand.**

- The one conflict is decided correctly and from the code. AWS Transform says an out-of-range transaction ends CBTRN03C's report loop; Claude's plugin says it is only not printed. The step found that `NEXT SENTENCE` (line 177) jumps to the first period, which is `END-PERFORM.` at line 206, so the loop ends: AWS Transform is right. Reading lines 160 to 212 confirms it.
- The merges keep both tools' details and are true to the code.
- No one-sided rule was wrong. In batch 3 all 12 were supported by the code; each was corrected in a detail. A rule only one tool found is, here, a gap in the other tool's coverage, not an error.

## Findings

1. **Rules must be written for business readers.** Round 1's rules were correct, but merged rules ran to 178 words and named up to 12 COBOL fields or paragraphs each. Round 2 asked for plain business language, at most about 50 words, code names only in parentheses, and allowed a merge to become up to three rules: the rules came out at 21 to 48 words with no code names, and still right.
2. **Decide by group, not by pair.** The comparison's pairs are many-to-one: 547 non-identical pairs link 547 AWS rules to only 160 Claude rules, which are broader (one Claude rule is in 30 pairs). Deciding pair by pair merges the same Claude rule again for every pair: in round 2, 12 AWS rules sharing 5 Claude rules became 36 rules that overlap. The unit of decision should be the group: one Claude rule with every AWS rule paired with it, answered with as many rules as the behaviour needs, each saying which input rules it covers.
3. **The code shows possible defects, and they are worth keeping.** Asked to report code behaviour that looks unintended, round 2 named eight in COACTUPC (not checked by hand in this spike). Among them: a failure to lock the customer record is reported as "Changes committed to database" although nothing was saved; negative credit limits pass validation; a change only in letter case can never be saved. They are not business rules, but an SME should see them: they belong on the SME list as possible defects.
4. **One-sided rules are mostly coverage.** With none rejected in 18 one-sided rules, the default expectation is "kept", with the evidence check guarding against a rule the code does not support.
5. **AWS Transform cites source in two shapes**: line numbers in the program's own file, or a list of `{file, lines}` for another file (a JCL procedure, a copybook). Inputs must read both.
6. **Batching.** One program per batch gives 129 batches, because 50 of the 92 programs have three items or fewer. Packing programs with fewer than six items together, up to 12 items and three programs a batch, gives 89.

## Cost of a CardDemo run

A batch takes 1 to 3 minutes and about $0.50 to $1.15 at API prices, almost all of it reading code (cache reads of 190k to 520k tokens). For about 90 batches:

- one at a time: 2 to 4 hours, about $50 to $100 at API prices;
- four at a time: about an hour.

On the Claude subscription this is a large share of a five-hour window, so a run may stop at the usage limit and continue with `reframe resume`, as pipeline 2 does.

## Changes to the specification

Written into [pipeline-3.md](../pipeline-3.md):

- stage R3: the unit is a group (a Claude rule with its paired AWS rules) or a one-sided rule; small programs are packed; four batches run at once; CardDemo's estimate is about 90 batches;
- stage R4: the answer's schema (rules with what each covers, `changed`, `defect`), the writing rules, and a coverage check beside the evidence check;
- stage R5: possible defects join the SME list;
- section 1: CardDemo's numbers.
