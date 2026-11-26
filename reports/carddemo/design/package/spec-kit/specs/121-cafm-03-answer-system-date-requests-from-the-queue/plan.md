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

- CAFM-BR-031: Run the service as a consumer started when messages arrive on the date request queue. Read the request queue name from the start-up event, and always send replies to the fixed queue 'CARD.DEMO.REPLY.DATE'.
- CAFM-BR-032: Drain the queue: take requests one at a time, commit each read-and-reply as one transaction before taking the next, and stop once no message arrives within 5 seconds.
- CAFM-BR-034: Publish the reply as a text message to 'CARD.DEMO.REPLY.DATE' with the request's message id and correlation id, inside the same transaction as consuming the request. Ignore any reply-to address the request names.
- CAFM-BR-035: On shutdown, release every queue connection (request, reply, error) that was opened successfully and leave the others alone, so connections are not leaked across runs.

## Decision tables

None.
