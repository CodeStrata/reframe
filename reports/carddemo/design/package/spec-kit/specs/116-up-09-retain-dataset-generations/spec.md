# Feature specification: Retain dataset generations

**Feature:** UP-C09 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C09)

As a CardDemo operator, I want transaction, reject, report and backup files kept as limited generation groups, so that recent history is kept and old generations are removed automatically.

Keeps a limited, rolling history of the batch files: daily transactions, rejects, combined and system-generated transactions, backups and the transaction report. Old copies are removed automatically. Operators rely on it to keep the most recent runs (five, or ten for the report history set-up) and never to let old copies pile up. Re-running the set-up must be harmless.

**Acceptance scenarios:**

1. **Given** existing generations: 5; event: transaction posting writes a new rejects generation (+1), **when** Daily Rejects setup job runs, **then** The oldest generation is removed from the group and scratched, leaving the 5 newest. (UP-C09-AC-01)
2. **Given** combined transaction files already kept: 5; event: combine job writes a new combined file (+1), **when** CardDemo setup job (DEFGDGB) runs, **then** The new combined file is kept and the oldest is removed and erased, leaving 5 generations. (UP-C09-AC-02)
3. **Given** generations of AWS.M2.CARDDEMO.TRANSACT.DALY already kept: 5; event: transaction report job writes a new daily file (+1), **when** CardDemo setup job (DEFGDGB) runs, **then** The new daily file is kept and the oldest is removed and erased, leaving 5 generations. (UP-C09-AC-03)
4. **Given** transaction reports already kept: 5; event: transaction report job writes a new report (+1), **when** CardDemo setup job (DEFGDGB) runs, **then** The new report is kept and the oldest report is removed and erased, leaving 5 reports. (UP-C09-AC-04)
5. **Given** catalogued report generations: 10; new daily transaction report: written as generation (+1), **when** Transaction Report History setup job runs, **then** The new report is catalogued and the oldest of the 10 earlier generations is no longer kept in the group. (UP-C09-AC-05)
6. **Given** category balance backups already kept: 5; event: category balance print job writes a new backup (+1), **when** CardDemo setup job (DEFGDGB) runs, **then** The new backup is kept and the oldest is removed and erased, leaving 5 generations. (UP-C09-AC-06)
7. **Given** generations of AWS.M2.CARDDEMO.TRANSACT.BKUP already kept: 5; event: transaction backup job writes a new generation (+1), **when** CardDemo setup job (DEFGDGB) runs, **then** The new backup is kept and the oldest of the five is removed from the catalog and its data erased, leaving 5 generations. (UP-C09-AC-07)
8. **Given** generations already kept: 3; event: new backup written, **when** CardDemo setup job (DEFGDGB) runs, **then** All 4 generations are kept; nothing is deleted. (UP-C09-AC-08)
9. **Given** system transaction files already kept: 5; event: interest calculation job writes a new file (+1), **when** CardDemo setup job (DEFGDGB) runs, **then** The new file is kept and the oldest is removed and erased, leaving 5 generations. (UP-C09-AC-09)
10. **Given** AWS.M2.CARDDEMO.TRANSACT.BKUP: already defined; DEFINE return code: 12, **when** a generation group definition in the setup job ends with return code 12 (for example because the group already exists), **then** The job's return code is set back to 0 and it goes on to define AWS.M2.CARDDEMO.TRANSACT.DALY. (UP-C09-AC-10)

## Requirements

### Functional requirements

- **UP-REQ-F-038** (design note): The system shall define the generation group for the daily rejected transactions (AWS.M2.CARDDEMO.DALYREJS) so that at most 5 generations are kept and each generation that ages out of the group is scratched. Rules: UP-BR-041.
- **UP-REQ-F-039** (design note): The system shall define the combined transaction file (AWS.M2.CARDDEMO.TRANSACT.COMBINED, the transaction backup merged with system-generated transactions) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. Rules: UP-BR-042.
- **UP-REQ-F-040** (design note): The system shall define the daily transaction file (AWS.M2.CARDDEMO.TRANSACT.DALY) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. Rules: UP-BR-043.
- **UP-REQ-F-041** (design note): The CardDemo setup job (DEFGDGB) shall define the transaction report (AWS.M2.CARDDEMO.TRANREPT) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest report's data when a new one pushes it past the limit. Rules: UP-BR-044.
- **UP-REQ-F-042** (design note): The Transaction Report History setup job shall define the transaction report generation group (AWS.M2.CARDDEMO.TRANREPT) so that at most 10 generations of the daily transaction report are kept catalogued, the oldest dropping off when an eleventh is created. Rules: UP-BR-045.
- **UP-REQ-F-043** (design note): The system shall define the transaction category balance backup (AWS.M2.CARDDEMO.TCATBALF.BKUP) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. Rules: UP-BR-046.
- **UP-REQ-F-044** (design note): The system shall define the transaction master backup file (AWS.M2.CARDDEMO.TRANSACT.BKUP) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. Rules: UP-BR-047.
- **UP-REQ-F-045** (design note): The system shall define the system-generated transaction file (AWS.M2.CARDDEMO.SYSTRAN) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. Rules: UP-BR-048.
- **UP-REQ-F-046** (error handling): If a generation group definition in the setup job ends with return code 12 (for example because the group already exists), then the system shall reset the job's highest return code to 0 and continue with the next definition. Rules: UP-BR-049.

### Business rules

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

### Key entities

None found in the source.

### Needs clarification

- SME-279: Two definitions of the transaction report history set different limits (10 generations vs 5). Which limit applies, and should generations that roll off be erased? (Batch operations team) On UP-BR-044, UP-BR-045.
- DEF-144: Is this intended? The step comment says it deletes the transaction master VSAM file, but the step only defines the report generation group; the comment was copied from another job. (Subject-matter expert) On UP-BR-045.
- DEF-146: Confirm this is deliberate: After each define the job resets any return code 12 to 0, not only 'already defined', so a genuine severity-12 failure to create a generation group is hidden and the job still ends with return code 0. (Subject-matter expert) On UP-BR-049.

### Decision table gaps

None.
