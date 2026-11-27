# Implementation plan: List card master records (UP-C02)

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

#### CVACT02Y

File record of CBACT02C. Source: `app/cpy/CVACT02Y.cpy`.

Record `CARD-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| CARD-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| CARD-CVV-CD |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| CARD-EMBOSSED-NAME |  | X(50) | text, 50 characters |  |  |  |
| CARD-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| CARD-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| FILLER |  | X(59) | text, 59 characters |  |  |  |

#### CVACT03Y

File record of CBACT03C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |


## Design notes

- UP-BR-003: A scheduled or on-demand report job that reads the card store through a read-only connection, so it can run while online users are working. Its progress messages and the listing go to the job's log or report output.
- UP-BR-006: Each successful fetch of the next card in the ordered read is written to the report. The new application needs a sequential read of all cards, ordered by card number.
- UP-BR-007: When the cursor or stream runs out of cards, the job ends normally. End of data is the normal way to finish, not an error.
- UP-BR-008: Iterate until there are no more rows and write nothing for the empty fetch, so no blank or repeated line appears after the last card.

## Decision tables

#### Card master read outcome

| Card master read file status | Card Listing action | Rule |
|---|---|---|
| '00' | Treat read as successful and print the record | UP-BR-006 |
| '10' (end of file) | Stop reading, print nothing for that read, end the listing normally | UP-BR-007 |
| any other status | Print 'ERROR READING CARDFILE', file status and 'ABENDING PROGRAM', abend with code 999 | UP-BR-009 |

