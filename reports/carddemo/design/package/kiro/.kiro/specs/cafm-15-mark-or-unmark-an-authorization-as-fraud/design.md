# Design: Mark or unmark an authorization as fraud (CAFM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets a card operations user mark a pending authorization as fraud, or remove that mark, with a single action on the detail screen. The change is recorded in two places, the authorization itself and the fraud register, and they must never disagree: both are saved together or neither is. The user is told plainly whether the authorization was marked or cleared, or why the change failed.

Runs as online. Journeys: J13.

## Screens and components

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Report fraud / Remove fraud mark | **primary button** | Reads 'Report fraud' when the authorization is not marked fraud and 'Remove fraud mark' when it is. It opens a confirmation dialog that repeats what will change: the authorization, amount and merchant, and 'Fraud status: Not reported -> Fraud reported, dated today' or the reverse. On success it shows 'Authorization marked as fraud' or 'Fraud mark removed' and redisplays the same authorization with its new fraud status and date. The authorization and the fraud register change together or not at all. | Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.' |  | CAFM-REQ-F-133, CAFM-REQ-F-134, CAFM-REQ-F-135, CAFM-REQ-F-136, CAFM-REQ-F-137, CAFM-REQ-F-138, CAFM-REQ-F-139, CAFM-REQ-F-140, CAFM-REQ-F-141, CAFM-REQ-N-003 |


## Data models

- CIPAUDTY (working storage of COPAUS1C, COPAUS2C): see data-contracts.md.
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
| CAFM-BR-143 | Toggle fraud mark on selected authorization | business rule | WHEN the user presses PF5 on the authorization detail screen and the selected authorization is marked fraud ('F'), THE authorization detail screen SHALL set its fraud flag to 'R' (fraud removed) and request the fraud action 'R' (remove fraud). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-266, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:565-569, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-53 |
| CAFM-BR-144 | Route operator requests on re-entry | business rule | WHEN the user presses PF5 on the detail screen, THE Authorization Detail View SHALL toggle the fraud mark of the selected authorization and redisplay its details. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-145 | Mark or unmark an authorization as fraud (upsert to the fraud table) | business rule | WHEN a user presses PF5 on the authorization detail screen, THE authorization detail screen SHALL ask the fraud program to record action 'R' (remove fraud) if the authorization is already marked fraud, and action 'F' (report fraud) otherwise. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |
| CAFM-BR-146 | Toggle fraud mark on selected authorization | business rule | WHEN the user presses PF5 on the authorization detail screen and the selected authorization is not marked fraud (blank or 'R'), THE authorization detail screen SHALL set its fraud flag to 'F' (fraud confirmed) and request the fraud action 'F' (report fraud). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-266, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:565-569, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-53 |
| CAFM-BR-147 | Submit fraud action to fraud processor | design note | THE authorization detail screen SHALL send the whole authorization record, the account number, the customer number and the fraud action to the fraud update program (COPAUS2C), which stamps today's date (MM/DD/YY) as the fraud report date on the record. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-266, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:565-569, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-53 |
| CAFM-BR-148 | Stamp fraud report with current date | business rule | THE fraud recording program SHALL set the fraud report date on the authorization record it returns to the caller (PA-FRAUD-RPT-DATE) to today's CICS date in MM/DD/YY form with separators, which the detail screen then saves on the pending authorization and displays. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:91-139, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:141-216, app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl:221-244, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-262 |
| CAFM-BR-149 | Confirm fraud mark outcome | business rule | WHEN the fraud update program completes normally and reports success ('S'), THE authorization detail screen SHALL save the authorization detail with the new fraud flag and report date, commit, and show 'AUTH FRAUD REMOVED...' if the flag is 'R', otherwise 'AUTH MARKED FRAUD...'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-266, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:565-569, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-53 |
| CAFM-BR-150 | Save updated authorization fraud status | business rule | WHEN the user presses PF5 on the authorization detail screen and the fraud processor (COPAUS2C) reports update status 'S', THE authorization detail screen SHALL replace the pending authorization detail record in IMS (PAUTDTL1) with the record carrying the toggled fraud flag and the fraud report date set by the fraud processor. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:253-255, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:557-569, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:80 |
| CAFM-BR-151 | Fraud update is all-or-nothing across the Db2 fraud register and the IMS authorization record | business rule | WHEN the IMS replace succeeds (status blank or 'FW'), THE authorization detail screen SHALL commit the Db2 fraud register change and the IMS change together and show 'AUTH FRAUD REMOVED...' if the flag is now 'R', otherwise 'AUTH MARKED FRAUD...'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:253-255, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:557-569, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:80 |
| CAFM-BR-152 | Confirm fraud mark outcome | error handling | WHEN saving the updated authorization detail fails, THE authorization detail screen SHALL roll back and show ' System error while FRAUD Tagging, ROLLBACK\|\|' followed by the database status code. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-266, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:565-569, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-53 |
| CAFM-BR-153 | Fraud update is all-or-nothing across the Db2 fraud register and the IMS authorization record | error handling | WHEN the IMS replace returns any other status, THE authorization detail screen SHALL roll back both the Db2 fraud register change and the IMS change, set the error flag and show ' System error while FRAUD Tagging, ROLLBACK\|\|' followed by the IMS status code. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:253-255, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:557-569, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:80 |
| CAFM-BR-154 | Submit fraud update request | error handling | WHEN the fraud update program completes but reports failure, THE authorization detail screen SHALL roll back, leave the authorization detail unchanged and show the fraud program's message (for example ' SYSTEM ERROR DB2: CODE:…'). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-266, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:565-569, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-53 |
| CAFM-BR-155 | Submit fraud action to fraud processor | error handling | WHEN the link to the fraud update program does not complete normally, THE authorization detail screen SHALL roll back and leave the authorization detail unchanged, without setting any message. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-266, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:565-569, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-53 |
| CAFM-BR-156 | Submit fraud update request | formatting | WHEN a PF5 fraud action finishes, THE authorization detail screen SHALL redisplay the same authorization's details. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-266, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:520-552, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:565-569, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-53 |

### Worked examples

- CAFM-BR-143: key pressed = PF5; current fraud flag = F → The flag becomes 'R' and action 'R' (remove fraud) is requested.
- CAFM-BR-144: key = PF5; fraud flag = (blank) → The fraud marking process runs for the selected authorization and the screen is redisplayed.
- CAFM-BR-145: current fraud flag = 'F'; key = PF5 → Action 'R' is sent to the fraud program
- CAFM-BR-145: current fraud flag = blank; key = PF5 → Action 'F' is sent to the fraud program
- CAFM-BR-146: key pressed = PF5; current fraud flag = (blank) → The flag becomes 'F' and action 'F' (report fraud) is requested.
- CAFM-BR-146: key pressed = PF5; current fraud flag = R → The flag becomes 'F' again and action 'F' is requested.
- CAFM-BR-149: fraud update status = S; new fraud flag = F → The detail is saved and 'AUTH MARKED FRAUD...' is shown.
- CAFM-BR-149: fraud update status = S; new fraud flag = R → The detail is saved and 'AUTH FRAUD REMOVED...' is shown.
- CAFM-BR-150: key pressed = PF5; fraud processor update status = S; fraud flag before = blank → The IMS authorization detail record is rewritten with fraud flag 'F' and today's fraud report date.
- CAFM-BR-151: IMS replace status = blank; new fraud flag = F → Both changes are committed and 'AUTH MARKED FRAUD...' is shown.
- CAFM-BR-151: IMS replace status = FW; new fraud flag = R → Both changes are committed and 'AUTH FRAUD REMOVED...' is shown.
- CAFM-BR-154: fraud update status = F; fraud program message = UPDT ERROR DB2: CODE:-911, STATE: 40001 → The change is rolled back and that message is shown.
- CAFM-BR-155: link result = not NORMAL → The change is rolled back and no message is shown.
- CAFM-BR-156: key pressed = PF5 → The detail screen is shown again for the same authorization, with the result message.

## Decision tables

#### PF5 fraud toggle

| Current fraud flag | New fraud flag and fraud action requested | Rule |
|---|---|---|
| 'F' (fraud confirmed) | Flag set to 'R'; action 'R' (remove fraud) | CAFM-BR-143 |
| blank or 'R' | Flag set to 'F'; action 'F' (report fraud) | CAFM-BR-146 |

#### Outcome of a fraud update

| Link to fraud update program completes normally | Fraud update program status | Authorization detail replace status | Commit or roll back, and message | Rule |
|---|---|---|---|---|
| No | n/a | not attempted | Roll back; authorization detail unchanged; no message | CAFM-BR-155 |
| Yes | failure | not attempted | Roll back; authorization detail unchanged; show the fraud program's message | CAFM-BR-154 |
| Yes | 'S' | blank or 'FW' | Commit both changes; show 'AUTH FRAUD REMOVED...' if flag is 'R', otherwise 'AUTH MARKED FRAUD...' | CAFM-BR-151 |
| Yes | 'S' | any other status | Roll back both changes; set error flag; show ' System error while FRAUD Tagging, ROLLBACK\|\|' and status | CAFM-BR-153 |


## Design notes

- CAFM-BR-147: The fraud action is one synchronous call from the detail screen to a fraud-recording service, passing the full authorization, the account number, the customer number and the action ('F' report or 'R' remove). The service stamps today's date (MM/DD/YY) as the fraud report date on the authorization it returns and reports success or failure with a message. Both the fraud register write and the authorization update must run in one transaction (or an equivalent all-or-nothing mechanism), committed only after the authorization update succeeds.

## Open questions

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-144.
- SME-144: When the request to mark or unmark an authorization as fraud does not complete normally, what should the operator see, and what state should the authorization be left in? (Authorization business analyst) On CAFM-BR-146, CAFM-BR-155, CAFM-BR-152, CAFM-BR-156, CAFM-BR-148, CAFM-BR-150.
- SME-145: When adding or updating a fraud record fails for any reason other than a duplicate record, what status and message should go back to the operator? (Fraud management team) On CAFM-BR-152, CAFM-BR-156, CAFM-BR-148.
- SME-146: The fraud update is written to the fraud store first, then to the authorization detail record. If the second write fails after the first has succeeded, nothing is rolled back. Must both updates succeed or fail together? (Architecture team) On CAFM-BR-146, CAFM-BR-155, CAFM-BR-152, CAFM-BR-156, CAFM-BR-150.
- SME-147: When an authorization's fraud flag is changed, which data stores must hold the new fraud flag and fraud report date: the authorization detail record, the fraud store, or both? (Data architect) On CAFM-BR-152, CAFM-BR-156, CAFM-BR-148.
- SME-148: If the fraud update reports success but the authorization's database status is neither blank nor 'FW', what message should the system show? (Business analyst) On CAFM-BR-152, CAFM-BR-156, CAFM-BR-148.
- SME-149: Please confirm: after the fraud flag is changed, the system sends a fraud update request with the updated authorization record, the account ID and the customer ID, to be recorded in the authorization fraud store (CARDDEMO.AUTHFRDS). (Business analyst) On CAFM-BR-152, CAFM-BR-156, CAFM-BR-148.
- DEF-056: Is this intended? If the link to the fraud program itself fails, the screen rolls back the change but sets no message, so the user sees the detail screen again with no word that the fraud action was not recorded. (Subject-matter expert) On CAFM-BR-146, CAFM-BR-149, CAFM-BR-155, CAFM-BR-152, CAFM-BR-156.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (17 in all).