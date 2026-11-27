# Implementation plan: Answer system date requests from the queue (CAFM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as online.

## Data model

None found in the source.

## Design notes

- CAFM-BR-031: Run the date inquiry as a consumer on the queue whose arrival started it. It always replies on the fixed date reply queue ('CARD.DEMO.REPLY.DATE') and ignores any reply-to queue the requester names.
- CAFM-BR-032: Process requests one at a time until the queue is empty: wait up to 5 seconds for each, and stop when none arrives. Take a request and send its reply in one transaction, committed before the next request is taken.
- CAFM-BR-034: Send the reply as a text message in the broker's standard character set, carrying the request's message ID and correlation ID, inside the same transaction that consumed the request.
- CAFM-BR-035: On shutdown, normal or after an error, release every queue connection that was opened (request, reply and error). Release only the ones that opened successfully, then end the task.

## Decision tables

None.
