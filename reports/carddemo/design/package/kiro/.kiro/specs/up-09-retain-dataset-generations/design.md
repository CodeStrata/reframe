# Design: Retain dataset generations (UP-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Keeps a limited, rolling history of the batch files: daily transactions, rejects, combined and system-generated transactions, backups and the transaction report. Old copies are removed automatically. Operators rely on it to keep the most recent runs (five, or ten for the report history set-up) and never to let old copies pile up. Re-running the set-up must be harmless.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-041 | Retain five generations of daily rejects | design note | THE Daily Rejects setup job SHALL define the generation group for the daily rejected transactions (AWS.M2.CARDDEMO.DALYREJS) so that at most 5 generations are kept and each generation that ages out of the group is scratched. | medium | app/jcl/DALYREJS.jcl:21-28, app/jcl/POSTTRAN.jcl:34-38 |
| UP-BR-042 | Retain five transaction report generations | design note | THE CardDemo setup job (DEFGDGB) SHALL define the combined transaction file (AWS.M2.CARDDEMO.TRANSACT.COMBINED, the transaction backup merged with system-generated transactions) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. | medium | app/jcl/DEFGDGB.jcl:54-59, app/jcl/COMBTRAN.jcl:22-37 |
| UP-BR-043 | Retain five transaction report generations | design note | THE CardDemo setup job (DEFGDGB) SHALL define the daily transaction file (AWS.M2.CARDDEMO.TRANSACT.DALY) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. | medium | app/jcl/DEFGDGB.jcl:30-35, app/jcl/TRANREPT.jcl:55 |
| UP-BR-044 | Retain five transaction report generations | design note | THE CardDemo setup job (DEFGDGB) SHALL define the transaction report (AWS.M2.CARDDEMO.TRANREPT) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest report's data when a new one pushes it past the limit. | medium | app/jcl/DEFGDGB.jcl:36-41, app/jcl/TRANREPT.jcl:76-80 |
| UP-BR-045 | Retain ten transaction report generations | design note | THE Transaction Report History setup job SHALL define the transaction report generation group (AWS.M2.CARDDEMO.TRANREPT) so that at most 10 generations of the daily transaction report are kept catalogued, the oldest dropping off when an eleventh is created. | medium | app/jcl/REPTFILE.jcl:22-28 |
| UP-BR-046 | Retain five transaction report generations | design note | THE CardDemo setup job (DEFGDGB) SHALL define the transaction category balance backup (AWS.M2.CARDDEMO.TCATBALF.BKUP) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. | medium | app/jcl/DEFGDGB.jcl:42-47, app/jcl/PRTCATBL.jcl:39 |
| UP-BR-047 | Retain five transaction report generations | design note | THE CardDemo setup job (DEFGDGB) SHALL define the transaction master backup file (AWS.M2.CARDDEMO.TRANSACT.BKUP) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. | medium | app/jcl/DEFGDGB.jcl:24-29, app/jcl/TRANBKP.jcl:33, app/jcl/COMBTRAN.jcl:24 |
| UP-BR-048 | Retain five transaction report generations | design note | THE CardDemo setup job (DEFGDGB) SHALL define the system-generated transaction file (AWS.M2.CARDDEMO.SYSTRAN) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. | medium | app/jcl/DEFGDGB.jcl:48-53, app/jcl/INTCALC.jcl:41 |
| UP-BR-049 | Retain five transaction report generations | error handling | WHEN a generation group definition in the setup job ends with return code 12 (for example because the group already exists), THE setup job SHALL reset the job's highest return code to 0 and continue with the next definition. | medium | app/jcl/DEFGDGB.jcl:24-29, app/jcl/TRANBKP.jcl:33, app/jcl/COMBTRAN.jcl:24 |

### Worked examples

- UP-BR-041: existing generations = 5; event = transaction posting writes a new rejects generation (+1) → The oldest generation is removed from the group and scratched, leaving the 5 newest.
- UP-BR-042: combined transaction files already kept = 5; event = combine job writes a new combined file (+1) → The new combined file is kept and the oldest is removed and erased, leaving 5 generations.
- UP-BR-043: generations of AWS.M2.CARDDEMO.TRANSACT.DALY already kept = 5; event = transaction report job writes a new daily file (+1) → The new daily file is kept and the oldest is removed and erased, leaving 5 generations.
- UP-BR-044: transaction reports already kept = 5; event = transaction report job writes a new report (+1) → The new report is kept and the oldest report is removed and erased, leaving 5 reports.
- UP-BR-045: catalogued report generations = 10; new daily transaction report = written as generation (+1) → The new report is catalogued and the oldest of the 10 earlier generations is no longer kept in the group.
- UP-BR-046: category balance backups already kept = 5; event = category balance print job writes a new backup (+1) → The new backup is kept and the oldest is removed and erased, leaving 5 generations.
- UP-BR-047: generations of AWS.M2.CARDDEMO.TRANSACT.BKUP already kept = 5; event = transaction backup job writes a new generation (+1) → The new backup is kept and the oldest of the five is removed from the catalog and its data erased, leaving 5 generations.
- UP-BR-047: generations already kept = 3; event = new backup written → All 4 generations are kept; nothing is deleted.
- UP-BR-048: system transaction files already kept = 5; event = interest calculation job writes a new file (+1) → The new file is kept and the oldest is removed and erased, leaving 5 generations.
- UP-BR-049: AWS.M2.CARDDEMO.TRANSACT.BKUP = already defined; DEFINE return code = 12 → The job's return code is set back to 0 and it goes on to define AWS.M2.CARDDEMO.TRANSACT.DALY.

## Decision tables

None.

## Design notes

- UP-BR-041: Keep each run's daily rejected-transactions output as a versioned object, for example a dated file in object storage. A retention policy keeps the latest 5 and deletes older ones.
- UP-BR-042: Version the combined transaction file (the transaction backup merged with system-generated transactions) per run. Keep the latest 5 and delete the data of older versions automatically.
- UP-BR-043: Version the daily transaction input per run. Keep the latest 5 and delete older versions automatically.
- UP-BR-044: Version the transaction report per run and keep the latest 5. Another set-up job defines the same report history with 10 versions (rule bc474731…), so the team must choose one limit.
- UP-BR-045: A retention policy for the daily transaction report that keeps the latest 10 versions; the oldest goes when an eleventh is created. This conflicts with the 5-version definition in the main set-up (rule 1b564856…), so the team must decide which one applies.
- UP-BR-046: Take a versioned backup of the transaction category balances on each run. Keep the latest 5 and delete older ones automatically.
- UP-BR-047: Take a versioned backup of the transaction master on each run. Keep the latest 5 and delete older ones automatically.
- UP-BR-048: Version the system-generated transaction file per run. Keep the latest 5 and delete older ones automatically.

## Open questions

- SME-279: Two definitions of the transaction report history set different limits (10 generations vs 5). Which limit applies, and should generations that roll off be erased? (Batch operations team) On UP-BR-044, UP-BR-045.
- DEF-144: Is this intended? The step comment says it deletes the transaction master VSAM file, but the step only defines the report generation group; the comment was copied from another job. (Subject-matter expert) On UP-BR-045.
- DEF-146: Confirm this is deliberate: After each define the job resets any return code 12 to 0, not only 'already defined', so a genuine severity-12 failure to create a generation group is hidden and the job still ends with return code 0. (Subject-matter expert) On UP-BR-049.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).