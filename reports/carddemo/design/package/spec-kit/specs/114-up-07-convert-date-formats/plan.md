# Implementation plan: Convert date formats (UP-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

None found in the source.

## Design notes

- UP-BR-033: A pure, reusable date-formatting function that takes YYYYMMDD and returns YYYY-MM-DD. Build it as a library function, not a separate service call.
- UP-BR-035: The same library function going the other way: it takes YYYY-MM-DD and returns YYYYMMDD by position (characters 1-4, 6-7 and 9-10). It does not validate the separators.
- UP-BR-037: The account extract calls the date-formatting function on the reissue date for every record it writes, so the extract carries the date as YYYYMMDD.

## Decision tables

#### Date format conversion routing

| Input type | Requested output type | Dash at fifth character of input | Conversion result | Rule |
|---|---|---|---|---|
| not '1' or '2' | any | any | Reject with 'INVALID INPUT'; output date unchanged | UP-BR-032 |
| '1' | not '2' | No | Return date as YYYY-MM-DD | UP-BR-033 |
| '1' | any | Yes | Reject with 'INVALID INPUT' | UP-BR-034 |
| '1' | '2' | any | Reject with 'INVALID INPUT' | UP-BR-034 |
| '2' | not '1' | any (not checked) | Return date as YYYYMMDD from characters 1-4, 6-7 and 9-10 | UP-BR-035 |
| '2' | '1' | any | Reject with 'INVALID INPUT' | UP-BR-036 |

