# Requirements: Business-monitor symbol list (not delivered) (TSM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Transaction Statistics and Monitoring · runs as scheduled job · risk low

## Introduction

The legacy collector builds a business-monitor symbol list of the counter values and the region's APPLID, then ends without sending it or the 'GENAST3TEMP' template anywhere. That list is the only place the error total, the individual error counters and 'GENAOTHER' ever appear. The team must not assume any business monitor, queue or screen receives these values today, and must not treat the start-time entry as filled in.

**User story:** As a business monitor user, I want to know that the business-monitor symbol list is built but never delivered, so that I do not rely on it for error totals or the region's APPLID.

## Requirements

### Requirement 1: TSM-REQ-F-016 (historical artifact)

#### Acceptance criteria

1. The system shall build a business-monitor symbol list of the counter values and the region's APPLID, with the start-time entry never filled in. (rules TSM-BR-015)
2. GIVEN the GENA counters hold values and the region has an APPLID WHEN the Statistics Collector runs THEN the symbol list it builds contains the counter values and the APPLID, and its start-time entry is empty (TSM-C04-AC-01; TSM-BR-015)

### Requirement 2: TSM-REQ-F-017 (historical artifact)

#### Acceptance criteria

1. The system shall end without sending the business-monitor symbol list or the template 'GENAST3TEMP' anywhere. (rules TSM-BR-015)
2. GIVEN the Statistics Collector has built the business-monitor symbol list WHEN the run ends THEN neither the symbol list nor the template 'GENAST3TEMP' has been sent to any queue, screen, monitor or other system (TSM-C04-AC-02; TSM-BR-015)

### Requirement 3: TSM-REQ-F-018 (historical artifact)

#### Acceptance criteria

1. The system shall place the error total, the individual error counters and 'GENAOTHER' only in the unsent symbol list (S39), so that no queue or screen receives them. (rules TSM-BR-013)
2. GIVEN in this run the error total is 7, counter 'GENA01ICUS99' reads 3 and 'GENAOTHER' reads 2 WHEN the Statistics Collector runs THEN the values 7, 3 and 2 appear only in the unsent symbol list (S39), and no queue or screen receives the error total, any counter ending '99' or 'GENAOTHER' (TSM-C04-AC-03; TSM-BR-013)
