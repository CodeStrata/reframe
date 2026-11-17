# Reframe specification amendments

**Applies to:** `Reframe-Complete-Workflow-Specification.md` (2026-11-15)
**Status:** Accepted by the owner on 2026-11-15 during backlog reconciliation. Kept separate from the approved specification; where an amendment and the specification differ, the amendment adds to FR-01 or FR-10 and does not relax any existing requirement.
**Code baseline:** `main` / `develop` at `b534f85b7854720ec5ac08c78e08c483211300b9`

## SA-1 — Handoff records are part of FR-10

**Problem.** FR-10 lists the package's logical contents but not the handoff records the code already writes. An implementer could treat them as unspecified and drop them.

**Code evidence.** `scripts/reframe_handoff.py:documents()` and `SKILLS` write `modernization-sequence.json`, `capability-map.json`, `parallel-validation.json`, `field-inventory.json`, `batch-inventory.json`, `api-boundary.json`, `governance.json`, `extraction-reading.json`, `rule-coverage.json`, `legacy-requirements.json`, and one `skill-*.md` per job. Both `scripts/reframe_preview.py` (skip draft) and `scripts/reframe.py:package()` (approved package) call `handoff.write_into`.

**Requirement.** Every package route (approved, skip draft, mode export) includes these records or an explicit absence statement.

**Acceptance criteria.**
- Each record is present in every route's ZIP, or the manifest states why it is absent.
- Sequence steps stay `NOT_STARTED`, comparison cases `NOT RUN`, capability boundaries `PROPOSAL` with disposition `unassigned`, and retirement `NOT_READY`, until a person records a change.
- Records name no target language or toolkit.

## SA-2 — Package safeguards apply to every route

**Problem.** NR-06 says to retain existing safeguards, but FR-10 does not require the credential, customer-identifier, and local-path checks on every package route.

**Code evidence.** `scripts/reframe.py:refuse_packaged_secrets()` (approved package); `_scan` and the workspace-path check in `scripts/reframe_optional.py:package_export()` (mode export).

**Requirement.** The approved, skip-draft, and mode-export packages all run the credential, customer-identifier, and local workspace-path checks before the archive is written.

**Acceptance criteria.**
- A fixture with a fake secret is refused on each route, and no archive is written.
- The refusal names the file and the kind of match, never the matched value.
- A clean fixture still packages on each route.

## SA-3 — Per-source sandbox identity

**Problem.** FR-01 covers project and run identity but not the AWS sandbox identity that guided setup already derives and reuses. G02 reuse verification needs that link to be explicit.

**Code evidence.** `scripts/reframe_setup.py:sandbox_identity()` derives `reframe-<repository>-<UTC date>-<id>` for the bucket, workspace, and connector, with `-role` for the IAM role; OpenTofu state stays in that source's private assessment folder.

**Requirement.** A source's sandbox identity is derived, recorded with the project, and verified on reuse.

**Acceptance criteria.**
- Continuing a source reuses its own sandbox state and does not create a second bucket or role.
- A different source never reuses another source's bucket, role, workspace, or connector.
- The person never types the sandbox name; long repository names are shortened so the role name fits.
