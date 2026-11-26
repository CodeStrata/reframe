# Implementation plan: Pick a customer number within the control range (ADPLM-C16)

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

- ADPLM-BR-100: Expose one operation that two callers share: a service call that returns the result in its response, and an interactive or terminal entry point that shows the result. Choose the presentation by the entry point, not by checking a start code at run time.
- ADPLM-BR-101: The customer range starts at 1000001 to 1000001 before the control record is read. Reading and repairing the control record must be serialized with an exclusive lock, such as a row lock or a lock held for the transaction, and the lock must be released before the random customer is chosen.
- ADPLM-BR-102: Store the control data as a small configuration record with a header, a low customer and a high customer, instead of an ordered queue. If the record is absent, treat all three entries as missing. If it is present, read every entry.
- ADPLM-BR-105: If the header is missing, write the header marker '**** GENAPP CNTL' as part of the same locked repair of the control record.
- ADPLM-BR-106: If the low customer value is missing, store it as the low end of the range in use, a 10-digit zero-padded number (0001000001 by default), within the same locked repair.
- ADPLM-BR-107: If the high customer value is missing, store it as the high end of the range in use, a 10-digit zero-padded number (0001000001 by default), within the same locked repair.
- ADPLM-BR-111: For service callers, return a response that holds only the label 'HIGH CUSTOMER=' and the chosen 10-digit customer number, with no data left over from the request.

## Decision tables

#### Control queue read and repair

| Control queue entry | Entry found | Customer inquiry action | Rule |
|---|---|---|---|
| Header (first entry) | Yes | Treat header as present and read every later entry until no more are returned | ADPLM-BR-102 |
| Header (first entry) | No | Treat header, low and high customer entries as missing; add header '**** GENAPP CNTL' | ADPLM-BR-105 |
| LOW CUSTOMER | Yes | Take the 10-digit number after 'LOW CUSTOMER=' as the low end of the range | ADPLM-BR-103 |
| LOW CUSTOMER | No | Add 'LOW CUSTOMER=' with the low end in use (0001000001 by default) | ADPLM-BR-106 |
| HIGH CUSTOMER | Yes | Take the 10-digit number after 'HIGH CUSTOMER=' as the high end of the range | ADPLM-BR-104 |
| HIGH CUSTOMER | No | Add 'HIGH CUSTOMER=' with the high end in use (0001000001 by default) | ADPLM-BR-107 |

