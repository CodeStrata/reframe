# Spike P2-01: the code-modernization plugin, headless, on CardDemo

22 and 23 November 2026, on the owner's Mac with their Claude subscription:

- **Plugin:** code-modernization 1.1.0.
- **Claude Code:** 2.1.327; every step ran on the default model (Opus 5.5).
- **Source:** the CardDemo snapshot pipeline 1 assessed, with the same SHA-256: 329 files, read-only.

No identifiers are recorded here. Costs are what Claude Code reports at API prices; on a subscription they count against the plan's usage limits instead of being billed.

## How it was run

- **Workspace:** a folder with `legacy/carddemo/` (the snapshot, unpacked read-only) and `analysis/carddemo/` for the plugin's outputs. `INTENT.md` was written beforehand ("understand it first"), so the plugin's front door wasn't needed.
- **Each step:** one `claude -p "/code-modernization:modernize-<step> carddemo"`, in an environment built from nothing, with the plugin's usage counts off (`CODE_MODERNIZATION_TELEMETRY=0`) and `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` (as the plugin's README says for headless runs), and stream-json output kept as the step's log.

## Results

| Step | Time | Turns | Tokens | Cost at API prices | What it wrote |
|---|---|---|---|---|---|
| preflight | 2.0 min | 16 | 0.69M | $0.74 | `PREFLIGHT.md`: the five questions as open items (see finding 2), stack, tooling, build, completeness, scope, protection, a verdict per command |
| assess | 3.5 min | 9 | 0.94M | $6.08 | `ASSESSMENT.md` (nine sections), `ARCHITECTURE.mmd`, `SECRETS.local.md` (masked credentials, one flagged as real), `REPORT.html` |
| map (second attempt; see finding 1) | 13.6 min | 85 | 4.80M | $6.94 | `topology.json` (12 domains plus data stores, 46 modules, 48 jobs, 21 screens, 74 data stores, 371 edges, 70 entry points, 4 persona flows), `TOPOLOGY.html`, three Mermaid diagrams, node descriptions checked against the source by a second agent |
| extract-rules (stopped by the usage limit, then resumed; see finding 8) | 21 + 6 min | 9 | about 8.3M across 441 agents | $51.26 for the whole session | `BUSINESS_RULES.md`: 273 rules confirmed of 285 candidates (8 merged, 4 refuted by the referee), 32 P0, 207 P1, 34 P2; 173 High, 98 Medium, 2 Low confidence; 100 questions for subject-matter experts. `rules_result.json`, `DATA_OBJECTS.md` (28 records) |

## Findings

1. **A workspace's own permissions are ignored headless when Claude Code hasn't been told to trust it.**
   - Claude Code looks up trust by the folder's Git root. On the owner's Mac that is their home folder, which is a Git repository. It printed "Ignoring 6 permissions.allow entries … this workspace has not been trusted".
   - So file writes were refused. `assess` wrote its files through the shell; the first `map` attempt stopped and wrote nothing.
   - Passing the rules on the command line with relative paths (`--allowedTools "Write(analysis/**)"`) didn't match either.
   - **What works:** `--settings <file>` with the rules as absolute paths (`//<workspace>/analysis/**`) and the shell sandbox on. A probe confirmed four things: a file-tool write into `analysis/` is allowed, a shell write into `analysis/` is allowed, a shell write to `/tmp` is blocked by the sandbox, and a write into `legacy/` is refused.
   - Reframe keeps this policy file outside the workspace, so the plugin can't change it, and never changes the person's own Claude Code settings or trust.
2. **The five preflight questions can't be asked headless.** With no question pop-up, the plugin wrote each as an open item for a person, as its command says it should. Reframe gives the answers in the step's prompt instead: its own in autonomous mode, recorded as decisions, or the person's, collected with `reframe answer`. The plugin then writes them word for word.
3. **The plugin can be pinned.**
   - Installing from the marketplace gives the newest version.
   - `claude --plugin-dir <folder>` loads a plugin from a folder, with the same `/code-modernization:` command names, including the `modernize-extract-rules-mine` workflow.
   - Reframe fetches the plugin's folder from Anthropic's repository at one commit (`d7d3279`, version 1.1.0) into `~/.reframe/tools`, and nothing is installed into the person's Claude Code.
4. **The rule-extraction estimate comes from the plugin's own shard builder.**
   - `scripts/make_shards.py carddemo ""` gave "37 shards from 46 map modules, 46 files, 22979 lines".
   - By the plugin's rule of thumb (10 to 15 agents per shard, about 16,000 tokens per agent), that is 370 to 555 agents and up to about 9 million tokens.
   - The plugin asks before more than 12 shards, but can't ask headless. Reframe says in the prompt that the estimate was confirmed against the person's agent limit, and the plugin launched all shards without asking.
5. **Structured output works for Reframe's own steps.** `--json-schema` returns the answer in the result line's `structured_output`, which Reframe uses for the generated requirements and the AI pairing of rules.
6. **The plugin's other questions don't block a headless run.** The map step noted it used the default where it would have asked about size. Nothing waited for input.
7. **Only a few shell commands were refused** under the policy: heredoc scripts and some pipelines that the sandbox's command check didn't recognise. In each case the plugin found another way.
8. **Claude's usage limit can stop a long step, and the step can be resumed.**
   - Extraction reached the subscription's 5-hour limit after 21 minutes (about 420 of 441 agents). The step's result line said "You've hit your 5-hour limit · resets …", with `is_error` true but subtype `success`.
   - After the reset, `claude -p --resume <session>` asked the plugin to resume its workflow by run ID. The plugin replayed the 423 finished agents from its journal and re-ran only the 18 that were cut off: 6 minutes and about 0.4 million more tokens.
   - Reframe treats the limit as a stop that waits (`reframe resume`), and resumes rule extraction in its own session in the same way. The pipeline was then run on a second run (bcc1e3); its preflight stopped on the same limit and was continued with `reframe resume`.
9. **Two runs on the same source differ, as expected.** On the second run, the shard builder made 38 shards (the first made 37), and `map` took 37 minutes instead of 14. The comparison page says both tools' results are model output.
