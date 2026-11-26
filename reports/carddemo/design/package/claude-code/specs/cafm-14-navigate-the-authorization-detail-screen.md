# Navigate the authorization detail screen (CAFM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk medium

## Introduction

Lets a card operations user move around the authorization detail screen: step to the next pending authorization of the same account, go back to the pending authorization list, or refresh the current one. It must stay within the same account when stepping forward and keep the current selection when there is nothing further. It must never show details from a failed read.

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
2. GIVEN an authorization is selected on the detail screen and reading the next authorization of the account returns database status 'AJ' (not success, not found or end of data) WHEN the user presses PF8 THEN an error is flagged, the message ' System error while reading next Auth: Code:' followed by AJ is shown, and the authorization detail fields are not filled in (CAFM-C14-AC-08; CAFM-BR-140)

### Requirement 6: CAFM-REQ-F-132 (business rule)

#### Acceptance criteria

1. When the user presses any key other than Enter, PF3, PF5 or PF8, the system shall re-read and redisplay the selected authorization as for Enter, with the message 'Invalid key pressed. Please see below...'. (rules CAFM-BR-141, CAFM-BR-142)
2. GIVEN key pressed: PF7; selected authorization key: K1 WHEN the user presses a key other than Enter, PF3, PF5 or PF8 THEN Authorization K1 is shown again with 'Invalid key pressed. Please see below...'. (CAFM-C14-AC-06; CAFM-BR-141)
3. GIVEN key: PF7 WHEN the user presses any key other than Enter, PF3, PF5 or PF8 THEN Details are redisplayed with 'Invalid key pressed. Please see below...'. (CAFM-C14-AC-07; CAFM-BR-142)

## Screens and components

### Pending authorizations (S-PENDING-AUTHS)

Look up an account and see its customer, limits, balances and approved/declined totals together with a paged table of its pending authorizations; open any authorization from its row.

Prototype: `ui-reference/index.html#/S-PENDING-AUTHS`. Replaces the legacy screens COPAU0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Authorization details (S-AUTH-DETAIL)

Review one pending authorization — card, amount, response and reason, POS, merchant and fraud status — move to the account's next authorization, and mark or clear fraud on it.

Prototype: `ui-reference/index.html#/S-AUTH-DETAIL`. Replaces the legacy screens COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Authorization could not be shown | message | Error or information when the authorization cannot be read; detail fields stay blank | If the account is not numeric or no authorization is selected, details are left blank and the user is sent back to choose an authorization from the list. System errors: ' System error while reading Auth Summary: Code:<code>', ' System error while reading Auth Details: Code:<code>', ' System error while reading next Auth: Code:<code>'. | S-PENDING-AUTHS | CAFM-REQ-F-127, CAFM-REQ-F-131 |
| Shortcut not available | message | Warning when a keyboard shortcut not offered on this screen is used; the selected authorization is re-read and redisplayed | Unsupported shortcut: 'Invalid key pressed. Please see below...' — use Refresh, Next authorization, Mark/Remove fraud or Back. |  | CAFM-REQ-F-132 |
| Next authorization | button | Moves to the account's next authorization; at the last one keeps the current one and shows 'Already at the last Authorization...' |  |  | CAFM-REQ-F-129, CAFM-REQ-F-130 |
| Back to pending authorizations | link |  |  | S-PENDING-AUTHS | CAFM-REQ-F-128 |


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

- CAFM-BR-135: The detail view can only be reached with an account and a selected authorization supplied by the pending authorization list. If it is opened directly without that context (e.g. a deep link or a fresh session), the application must redirect the user to the pending authorization list instead of showing an empty detail page.

## Open questions

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-139, CAFM-BR-140, CAFM-BR-138, CAFM-BR-142.
- DEF-026: Is this intended? When the summary or the selected detail is not found ('GE'/'GB'), the error flag stays off, so the screen is filled from whatever detail record is in memory, with no 'not found' message; and on a read error the screen is sent once inside the read routine and again by the main flow. (Subject-matter expert) On CAFM-BR-141.
- DEF-063: Is this intended? When a database read fails, the error paragraph sends the detail screen itself and then the main routine sends it a second time, so the screen is sent twice in one task. (Subject-matter expert) On CAFM-BR-139, CAFM-BR-140.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
