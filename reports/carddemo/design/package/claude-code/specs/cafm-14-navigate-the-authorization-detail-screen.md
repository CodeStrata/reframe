# Navigate the authorization detail screen (CAFM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk medium

## Introduction

Lets a card operations user move through an account's pending authorizations one at a time from the detail screen: step to the next one, go back to the list, or refresh the current one. It must stay inside the same account, never lose the current selection when there is no next authorization, and never show part-filled details when the next read fails.

**User story:** As a card operations user, I want to use function keys on the authorization detail screen to move to the next authorization or return to the list, so that I can work through an account's pending authorizations.

## Requirements

### Requirement 1: CAFM-REQ-F-127 (design note)

#### Acceptance criteria

1. When the detail program starts with no data passed from a calling screen, the system shall transfer control to the authorization summary program (COPAUS0C). (rules CAFM-BR-135)
2. GIVEN transaction CPVD started directly: no commarea WHEN the detail program starts with no data passed from a calling screen THEN Control passes to COPAUS0C. (CAFM-C14-AC-01; CAFM-BR-135)

### Requirement 2: CAFM-REQ-F-128 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the detail screen, the system shall return to the authorization summary list (COPAUS0C). (rules CAFM-BR-136)
2. GIVEN key: PF3 WHEN the user presses PF3 on the detail screen THEN The pending authorization summary screen is shown. (CAFM-C14-AC-02; CAFM-BR-136)

### Requirement 3: CAFM-REQ-F-129 (business rule)

#### Acceptance criteria

1. When the user presses PF8 on the detail screen, the system shall re-read the selected authorization of the account, fetch the next authorization under the same account, make it the selected authorization and display its details. (rules CAFM-BR-137, CAFM-BR-138)
2. GIVEN account: 00000012345; selected authorization: K1; authorizations under account: K1, K2 WHEN the user presses PF8 THEN K2 becomes the selected authorization and its details are shown. (CAFM-C14-AC-03; CAFM-BR-137)
3. GIVEN key: PF8 WHEN the user presses PF8 on the detail screen THEN The next authorization of the account is displayed. (CAFM-C14-AC-04; CAFM-BR-138)

### Requirement 4: CAFM-REQ-F-130 (business rule)

#### Acceptance criteria

1. When the user presses PF8 and there is no further authorization for the account, the system shall keep the current selection and show 'Already at the last Authorization...' without erasing the screen. (rules CAFM-BR-139)
2. GIVEN selected authorization: K2 (last); key: PF8 WHEN the user presses PF8 and there is no further authorization for the account THEN 'Already at the last Authorization...' is shown and K2 stays selected. (CAFM-C14-AC-05; CAFM-BR-139)

### Requirement 5: CAFM-REQ-F-131 (error handling)

#### Acceptance criteria

1. If reading the next authorization fails with any database status other than success, not found or end of data, then the system shall flag an error, show ' System error while reading next Auth: Code:' followed by the status code, and not fill in the authorization details. (rules CAFM-BR-140)
2. GIVEN the detail screen shows a selected authorization for an account, and reading the next authorization under that account returns a database status other than success, not found or end of data, for example 'AI' WHEN the user presses PF8 THEN an error is flagged, the message ' System error while reading next Auth: Code:' followed by AI is shown, and the authorization detail fields are not filled in (CAFM-C14-AC-08; CAFM-BR-140)

### Requirement 6: CAFM-REQ-F-132 (business rule)

#### Acceptance criteria

1. When the user presses any key other than Enter, PF3, PF5 or PF8, the system shall re-read and redisplay the selected authorization as for Enter, with the message 'Invalid key pressed. Please see below...'. (rules CAFM-BR-141, CAFM-BR-142)
2. GIVEN key pressed: PF7; selected authorization key: K1 WHEN the user presses a key other than Enter, PF3, PF5 or PF8 THEN Authorization K1 is shown again with 'Invalid key pressed. Please see below...'. (CAFM-C14-AC-06; CAFM-BR-141)
3. GIVEN key: PF7 WHEN the user presses any key other than Enter, PF3, PF5 or PF8 THEN Details are redisplayed with 'Invalid key pressed. Please see below...'. (CAFM-C14-AC-07; CAFM-BR-142)

## Screens and components

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Authorizations | **data table** | Columns: transaction ID, date (26 Nov 2026), time (HH:MM:SS), type, an Approved/Declined badge (Approved when the response code is 00), status, fraud status, and amount right-aligned with sign and two decimals. Sortable, newest first, 20 rows a page with Previous page and Next page controls. Click a row or press Enter on it to open its details beside the table. Empty state: 'No pending authorizations for this account. They appear here once the card is used.' | Previous page is disabled on the first page, with 'You are already on the first page'. Next page is disabled on the last page, with 'You are already on the last page'. Next authorization on the last one says 'Already at the last authorization' and keeps the current one open. Rows open directly, so no selection code is typed and 'Invalid selection. Valid value is S' cannot arise. There are no unsupported keys to warn about. |  | CAFM-REQ-F-128, CAFM-REQ-F-129, CAFM-REQ-F-130, CAFM-REQ-F-131, CAFM-REQ-F-132 |
| Authorization | **summary card** | Card number, date (26 Nov 2026), time (HH:MM:SS), amount right-aligned with two decimals and a leading '-' when negative, decline reason as '<code> - <description>' ('9999 - ERROR' when the code is unknown), authorization code, POS entry mode, source, merchant category code, card expiry (MM/YY), authorization type, transaction ID and match status. Read afresh each time a row opens. With no row selected the panel says 'Select an authorization to see its details.' | Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed. |  | CAFM-REQ-F-127 |


## Data models

- CIPAUDTY (working storage of COPAUS1C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-135 | Authorization detail screen key handling and navigation | design note | WHEN the detail program starts with no data passed from a calling screen, THE Authorization Detail View SHALL transfer control to the authorization summary program (COPAUS0C). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-136 | Authorization detail screen key handling and navigation | business rule | WHEN the user presses PF3 on the detail screen, THE Authorization Detail View SHALL return to the authorization summary list (COPAUS0C). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-137 | Show next authorization | business rule | WHEN the user presses PF8, THE Authorization Detail View SHALL re-read the selected authorization of the account, fetch the next authorization under the same account, make it the selected authorization and display its details. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:268-289, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:493-518, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:380-395 |
| CAFM-BR-138 | Route operator requests on re-entry | business rule | WHEN the user presses PF8 on the detail screen, THE Authorization Detail View SHALL show the next authorization of the same account. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-139 | Show next authorization | business rule | WHEN the user presses PF8 and there is no further authorization for the account, THE Authorization Detail View SHALL keep the current selection and show 'Already at the last Authorization...' without erasing the screen. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:268-289, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:493-518, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:380-395 |
| CAFM-BR-140 | Read next authorization detail | error handling | WHEN reading the next authorization fails with any database status other than success, not found or end of data, THE Authorization Detail View SHALL flag an error, show ' System error while reading next Auth: Code:' followed by the status code, and not fill in the authorization details. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:268-289, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:493-518, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:380-395 |
| CAFM-BR-141 | Authorization detail can only be shown for a numeric account and a selected authorization | business rule | WHEN the user presses a key other than Enter, PF3, PF5 or PF8, THE Authorization Detail View SHALL reload and show the selected authorization as for Enter, with the message 'Invalid key pressed. Please see below...'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:165-197, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491 |
| CAFM-BR-142 | Warn on invalid key | business rule | WHEN the user presses any key other than Enter, PF3, PF5 or PF8, THE Authorization Detail View SHALL re-read and redisplay the selected authorization with the message 'Invalid key pressed. Please see below...'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |

### Worked examples

- CAFM-BR-135: transaction CPVD started directly = no commarea → Control passes to COPAUS0C.
- CAFM-BR-136: key = PF3 → The pending authorization summary screen is shown.
- CAFM-BR-137: account = 00000012345; selected authorization = K1; authorizations under account = K1, K2 → K2 becomes the selected authorization and its details are shown.
- CAFM-BR-138: key = PF8 → The next authorization of the account is displayed.
- CAFM-BR-139: selected authorization = K2 (last); key = PF8 → 'Already at the last Authorization...' is shown and K2 stays selected.
- CAFM-BR-141: key pressed = PF7; selected authorization key = K1 → Authorization K1 is shown again with 'Invalid key pressed. Please see below...'.
- CAFM-BR-142: key = PF7 → Details are redisplayed with 'Invalid key pressed. Please see below...'.

## Decision tables

#### Detail screen key handling

| Entry | Key pressed | What the detail view does | Rule |
|---|---|---|---|
| No data passed from a calling screen | any | Transfer to the authorization summary program (COPAUS0C) | CAFM-BR-135 |
| First entry from summary list | n/a | Read and display the selected authorization |  |
| Re-entry | Enter | Re-read and redisplay the selected authorization |  |
| Re-entry | PF3 | Return to the authorization summary list (COPAUS0C) | CAFM-BR-136 |
| Re-entry | PF5 | Toggle the fraud mark and redisplay the details |  |
| Re-entry | PF8 | Show the next authorization of the same account | CAFM-BR-138 |
| Re-entry | any other key | Re-read and redisplay with 'Invalid key pressed. Please see below...' | CAFM-BR-142 |

#### PF8 next authorization outcome

| Next authorization read result | What the detail view does | Rule |
|---|---|---|
| Next authorization found | Make it the selected authorization and display its details | CAFM-BR-137 |
| No further authorization | Keep current selection; show 'Already at the last Authorization...' without erasing the screen | CAFM-BR-139 |
| Any other database status | Flag error; show ' System error while reading next Auth: Code:' and status; details not filled | CAFM-BR-140 |


## Design notes

- CAFM-BR-135: The detail view can only be reached with an account and a selected authorization from the pending authorization list. If it is opened directly, with no account or selection carried in (a bare URL, an expired session), it must redirect to the account's pending authorization list instead of showing an empty or default detail page.

## Open questions

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-139, CAFM-BR-140, CAFM-BR-138, CAFM-BR-142.
- DEF-026: Is this intended? When the summary or the selected detail is not found ('GE'/'GB'), the error flag stays off, so the screen is filled from whatever detail record is in memory, with no 'not found' message; and on a read error the screen is sent once inside the read routine and again by the main flow. (Subject-matter expert) On CAFM-BR-141.
- DEF-063: Is this intended? When a database read fails, the error paragraph sends the detail screen itself and then the main routine sends it a second time, so the screen is sent twice in one task. (Subject-matter expert) On CAFM-BR-139, CAFM-BR-140.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
