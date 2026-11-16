# Agreed workflow implementation log

Branch `feature/agreed-workflow` from `develop` at `b534f85`. Specification: [docs/specifications](../specifications/README.md). Backlog: [Reframe Backlog](https://github.com/users/sknampally/projects/1).

Validation levels: L1 offline unit/contract · L2 independent AI user acceptance (offline, simulated actors) · L3 authorized live (not performed on this branch).

## Environment

- Disposable Python 3.12 virtual environment and an isolated `HOME`, `REFRAME_CONFIG_HOME`, and `TMPDIR`, outside the source checkout.
- Empty AWS configuration and no provider keys.
- Logging stubs refuse `aws`, `claude`, `codex`, `tofu`, `terraform`, `uvx`, `kiro`, `kiro-cli` and record any attempt in an external-call ledger, in addition to the in-process guard in `scripts/reframe_offline.py`.

## Log

| Date | Item | Result | Evidence |
| --- | --- | --- | --- |
| 2026-11-15 | #160 baseline | develop = main = `b534f85` (tree `ea8bbf6`); spec, amendments, manifest preserved with hashes; gap matrix reconciled | [baseline-and-gap-matrix.md](../specifications/baseline-and-gap-matrix.md) |
| 2026-11-15 | Test baseline | 411 tests, OK, 2 skips with named activation conditions; external-call ledger empty | baseline-and-gap-matrix.md § Test baseline |
| 2026-11-15 | #162 typed stops | Done (L1): cause + recovery class on every stop; last-stop.json beside project.json keeps refusals byte-identical; cancellation is an event | tests/test_m1_contracts.py |
| 2026-11-15 | #161 versions, #34 supersession | Done (L1): content-addressed version manifests written once; integrity failure without overwrite; approvals bound to versions and superseded into history | tests/test_m1_contracts.py |
| 2026-11-15 | #163 operation ledger | Done (L1): dispatched-before-call records; uncertain dispatch blocks until reconcile-operation; pre-start failures recorded as not dispatched | tests/test_m1_contracts.py |
| 2026-11-15 | #164 migration, #165 recovery plan | Done (L1): controller-only update at any phase with unchanged prompts, audited; wireframe prompt pinned; partial migration visible; read-only recovery-plan | tests/test_m1_contracts.py |
| 2026-11-15 | #166 call policy | Done (L1): per-role cap labeled; aggregate view; >256 uncapped | tests/test_m1_contracts.py |
| 2026-11-15 | #169–#173 requirements boundary | Offline done (L1/L2 fixtures); live generation NOT verified — needs Neptune/VPC reimagine connector and authorization (#197) | tests/test_requirements.py |
| 2026-11-15 | #174–#177 context and validation inputs | Done (L1): gate records incl. explicit none; FR-04 categories; scoped conflicts; requirements + admitted context in synthesis validation with provenance | tests/test_context_validation.py |
| 2026-11-15 | #181 links | Done (L1): recursive validator wired at every artifact write; found and fixed mode-package and future-state link defects | tests/test_links.py |
| 2026-11-15 | #187, #188, #190 acceptance | Done (L1): AWAITING_PACKAGE_ACCEPTANCE on build; hash-named acceptance in a chained ledger outside the archive; readiness from all blockers | tests/test_acceptance.py |
| 2026-11-15 | #195 isolation, AC-34 | Done (L1 + explicit wheel check 12/12): guard closes shell/wrapper/connect_ex gaps; wheel ships resources; installed pin is a content revision | tests/test_offline_guard.py, tests/test_installed_wheel.py |
| 2026-11-15 | #182–#186, #189, #191, #178–#180, #192 design, routes, coverage, guided journey | Done (L1/L2 journeys): design plan before detail; inventory saved before detail; shared definitions reconciled, never renamed; API completeness; Reimagine proposals only from accepted future-state context; feedback routed to design or specification; skip and review routes reach package review and acceptance | tests/test_design.py, tests/test_coverage_questions.py, tests/test_menu_journeys.py |
| 2026-11-15 | #44 CardDemo regressions | Done (L1): all 21 §10 failures indexed to tests; sanitized saved-scale fixture (452 questions, 54 deferrals, request over 600 KB) and exact-threshold checks | docs/validation/carddemo-regressions.md, tests/test_carddemo_scale.py, tests/test_regression_index.py |
| 2026-11-15 | #116 docs, #124 branch rule | Done (L1): README gates, scripted commands, package-contents table; CLI guide command reference generated from --help; recovery commands name --workspace; copied hint values (NAME, WHY, RATIONALE) are refused; CI runs on develop | tests/test_docs_consistency.py |
| 2026-11-15 | Skip-route package (FR-10) | Fixed: the skip route builds its own package after design approval with requirements provenance, human context, approval history, and the design plan; the draft ZIP stays unchanged | tests/test_menu_journeys.py |
| 2026-11-15 | Awaiting-verification items | Checked bullet by bullet by a separate verification agent; every GAP and PARTIAL then closed. Code fixes: #130 decisions on the destination screen, #140 finding area kept for correction focus, #144 repeated resume restates the stop, #108 per-case oracle | docs/validation/awaiting-verification.md |
| 2026-11-15 | #115 docstrings | Done (L1): every module-level function and method documented | tests/test_docstrings.py |
| 2026-11-15 | #194 harness, simulated labels | Done: acceptance/harness.py drives the real no-argument console; every simulated human record carries simulated: true | acceptance/harness.py, tests/test_menu_journeys.py |
| 2026-11-15 | SA-2 every route | Done (L1): fake secret and customer identifier refused on review, skip draft, and mode export without an archive | tests/test_package_safeguards.py |
| 2026-11-15 | Candidate `d65d86f` special checks | Full suite 543 OK (11 opt-in skips); installed wheel 12 of 12; clean-snapshot fresh start OK; external-call ledger empty | run logs; docs/validation/completion-matrix.md |
| 2026-11-15 | Post-merge migration | Verified in disposable uv tool folders: a workspace saved by `b534f85` migrates with `upgrade-framework`; approvals unchanged; one audit event | docs/validation/review-package.md |
| 2026-11-15 | Saved CardDemo | Read-only recovery plan; 3,217 files unchanged | docs/validation/carddemo-recovery-recommendation.md |
