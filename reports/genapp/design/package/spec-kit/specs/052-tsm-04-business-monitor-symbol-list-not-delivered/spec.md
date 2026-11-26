# Feature specification: Business-monitor symbol list (not delivered)

**Feature:** TSM-C04 · Transaction Statistics and Monitoring · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TSM-C04)

As a business monitor user, I want to know that the business-monitor symbol list is built but never delivered, so that I do not rely on it for error totals or the region's APPLID.

The legacy collector builds a business-monitor symbol list of the counter values and the region's APPLID, then ends without sending it or the 'GENAST3TEMP' template anywhere. That list is the only place the error total, the individual error counters and 'GENAOTHER' ever appear. The team must not assume any business monitor, queue or screen receives these values today, and must not treat the start-time entry as filled in.

**Acceptance scenarios:**

1. **Given** the GENA counters hold values and the region has an APPLID, **when** the Statistics Collector runs, **then** the symbol list it builds contains the counter values and the APPLID, and its start-time entry is empty (TSM-C04-AC-01)
2. **Given** the Statistics Collector has built the business-monitor symbol list, **when** the run ends, **then** neither the symbol list nor the template 'GENAST3TEMP' has been sent to any queue, screen, monitor or other system (TSM-C04-AC-02)
3. **Given** in this run the error total is 7, counter 'GENA01ICUS99' reads 3 and 'GENAOTHER' reads 2, **when** the Statistics Collector runs, **then** the values 7, 3 and 2 appear only in the unsent symbol list (S39), and no queue or screen receives the error total, any counter ending '99' or 'GENAOTHER' (TSM-C04-AC-03)

## Requirements

### Functional requirements

- **TSM-REQ-F-016** (historical artifact): The system shall build a business-monitor symbol list of the counter values and the region's APPLID, with the start-time entry never filled in. Rules: TSM-BR-015.
- **TSM-REQ-F-017** (historical artifact): The system shall end without sending the business-monitor symbol list or the template 'GENAST3TEMP' anywhere. Rules: TSM-BR-015.
- **TSM-REQ-F-018** (historical artifact): The system shall place the error total, the individual error counters and 'GENAOTHER' only in the unsent symbol list (S39), so that no queue or screen receives them. Rules: TSM-BR-013.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TSM-BR-015 | Business-monitor symbol list is built but never delivered | historical artifact | THE Statistics Collector SHALL build a business-monitor symbol list of the counter values and the region's APPLID, but SHALL end without sending it or the template 'GENAST3TEMP' anywhere. The start-time entry is never filled in. | medium | base/src/lgwebst5.cbl:57-62, base/src/lgwebst5.cbl:76-156, base/src/lgwebst5.cbl:703-709 |
| TSM-BR-013 | Total successful vs failed transaction counts | historical artifact | THE Statistics Collector SHALL publish the successful-transaction total to queue 'GENAX00V'. The error total, the individual error counters and 'GENAOTHER' are only placed in the unsent symbol list (S39), so no queue or screen receives them. | medium | base/src/lgwebst5.cbl:286, base/src/lgwebst5.cbl:301, base/src/lgwebst5.cbl:323, base/src/lgwebst5.cbl:657 |

### Key entities

None found in the source.

### Needs clarification

- SME-105: Should the 'GENAOTHER' transaction counter count as a success, as an error, or as neither? And should total errors also be published as a statistic? Today the total is calculated but never stored. (Operations) On TSM-BR-013.
- SME-106: The statistics transaction builds a symbol list and HTML template output (GENAST3TEMP / GENASTAT) but never delivers it, while its sibling web-statistics programs do publish theirs. Was this output meant to be published, or is it deliberately unused? (Application owner) On TSM-BR-015.
- DEF-053: Is this intended? The program counts errors but never publishes the total, so a monitor cannot see error volume. (Subject-matter expert) On TSM-BR-013.

### Decision table gaps

None.
