# Requirements: Page through an account's pending authorizations (CAFM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Lets customer service operators page forward (PF8) and back (PF7) through an account's pending authorizations five at a time. Each row shows 'A' for approved (response '00') or 'D' for declined, with amount, date, time, transaction id, type and match status. Paging must never skip or repeat authorizations, and the operator sees the stated message at the top or bottom of the list.

**User story:** As a customer service operator, I want to page forward and back through an account's pending authorizations five at a time, with each shown as approved or declined, so that I can review every authorization on the account.

## Requirements

### Requirement 1: CAFM-REQ-F-101 (business rule)

#### Acceptance criteria

1. When a page of authorizations is loaded and no error is flagged, the system shall read up to 5 pending authorizations for the account into the list rows (on backward paging starting at the saved first key of that page), remember each page's first key and the last key shown, then read one more ahead to set whether a next page exists. (rules CAFM-BR-105)
2. GIVEN pending authorizations for account: 7 WHEN a page of authorizations is loaded and no error is flagged THEN First page shows 5 rows and a next page is available (CAFM-C10-AC-01; CAFM-BR-105)
3. GIVEN pending authorizations for account: 3 WHEN a page of authorizations is loaded and no error is flagged THEN 3 rows are shown and no next page is flagged (CAFM-C10-AC-02; CAFM-BR-105)

### Requirement 2: CAFM-REQ-F-102 (design note)

#### Acceptance criteria

1. When the user pages forward (PF8), the system shall re-read the account's authorization summary and reposition at the last authorization shown when one exists, otherwise clear the start key. (rules CAFM-BR-106)
2. GIVEN last authorization shown: key of row 5; key pressed: PF8 WHEN the user pages forward (PF8) THEN Reading resumes after the fifth authorization shown (CAFM-C10-AC-03; CAFM-BR-106)
3. GIVEN last authorization shown: none WHEN the user pages forward (PF8) THEN The start key is cleared and no repositioning is done (CAFM-C10-AC-04; CAFM-BR-106)

### Requirement 3: CAFM-REQ-F-103 (business rule)

#### Acceptance criteria

1. When the user presses PF8 and a next page exists, the system shall clear the five list rows, load the next page of up to 5 pending authorizations and redisplay the screen without a full erase. (rules CAFM-BR-107, CAFM-BR-108)
2. GIVEN key pressed: PF8; next page exists: yes WHEN the user presses PF8 on the summary screen and a next page exists THEN Next 5 pending authorizations are shown (CAFM-C10-AC-05; CAFM-BR-107)
3. GIVEN key pressed: PF8; next page exists: 'Y' WHEN the user pages forward (PF8) and a next page exists THEN The list is cleared and refilled with the next authorizations (CAFM-C10-AC-06; CAFM-BR-108)

### Requirement 4: CAFM-REQ-F-104 (business rule)

#### Acceptance criteria

1. When the user presses PF8 and no further page of authorizations exists, the system shall keep the current list and show 'You are already at the bottom of the page...'. (rules CAFM-BR-109)
2. GIVEN key pressed: PF8; more authorizations: none WHEN the user pages forward (PF8) and no further page of authorizations exists THEN Message 'You are already at the bottom of the page...' is shown (CAFM-C10-AC-07; CAFM-BR-109)

### Requirement 5: CAFM-REQ-F-105 (business rule)

#### Acceptance criteria

1. When the operator presses PF7 and the current page number is greater than 1, the system shall step the page number back by one, reposition to the saved first authorization key of that page, and redisplay up to five authorizations starting from that key without erasing the screen. (rules CAFM-BR-110)
2. GIVEN Current page number: 3; Key: PF7 WHEN the operator presses PF7 on the pending authorization summary screen and the current page number is greater than 1 THEN The list restarts at the first authorization saved for page 2 and shows up to five authorizations from there (CAFM-C10-AC-08; CAFM-BR-110)
3. GIVEN Current page number: 2; Key: PF7 WHEN the operator presses PF7 on the pending authorization summary screen and the current page number is greater than 1 THEN The first page of authorizations is shown again (CAFM-C10-AC-09; CAFM-BR-110)

### Requirement 6: CAFM-REQ-F-106 (business rule)

#### Acceptance criteria

1. When the operator presses PF7 and the current page number is 1 or less, the system shall show 'You are already at the top of the page...' and leave the list unchanged. (rules CAFM-BR-111)
2. GIVEN Current page number: 1; Key: PF7 WHEN the operator presses PF7 and the current page number is 1 or less THEN Message 'You are already at the top of the page...' and the same list stays on screen (CAFM-C10-AC-10; CAFM-BR-111)

### Requirement 7: CAFM-REQ-F-107 (business rule)

#### Acceptance criteria

1. When an authorization is placed in the summary list, the system shall show it as approved 'A' when its response code is '00' and as declined 'D' for any other response code. (rules CAFM-BR-112)
2. GIVEN response code: '00' WHEN an authorization is placed in the summary list THEN Approval status shows 'A' (CAFM-C10-AC-11; CAFM-BR-112)
3. GIVEN response code: '05' WHEN an authorization is placed in the summary list THEN Approval status shows 'D' (CAFM-C10-AC-12; CAFM-BR-112)

### Requirement 8: CAFM-REQ-F-108 (formatting)

#### Acceptance criteria

1. When an authorization is listed, the system shall show its approved amount with a sign and two decimals, its original date held as YYMMDD as MM/DD/YY, and its original time held as HHMMSS as HH:MM:SS, along with transaction id, authorization type and match status. (rules CAFM-BR-113, CAFM-BR-114)
2. GIVEN A pending authorization with approved amount 150.00, original date '240315' (YYMMDD) and original time '143005' (HHMMSS) WHEN It is listed on the Pending authorizations screen THEN Its row shows the approved amount as 150.00 with a sign and two decimals, the date as '03/15/24' and the time as '14:30:05', along with its transaction id, authorization type and match status (CAFM-C10-AC-13; CAFM-BR-113, CAFM-BR-114)
