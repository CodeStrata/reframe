# Design: View authorization detail and mark fraud (CAFM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Shows a fraud analyst one authorization in full: approved 'A' in green or declined 'D' in red, with the decline reason as '<code>-<description>'. One key toggles its fraud mark, reporting the authorization as fraud ('F') or withdrawing the report ('R'), and passes it on to fraud processing. The toggle must always work from the freshly read record. An unknown reason code must show as '9999-ERROR', never blank.

Runs as online. Journeys: J13.

## Screens and components

### Account authorizations (S-ACCOUNT-AUTHORIZATIONS)

Look up an account and see everything on one screen: the customer, limits and balances, pending authorization totals, the authorizations in a paged table, and the selected authorization's full details. Fraud can be reported or cleared without leaving the list.

Prototype: `ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS`. Replaces the legacy screens COPAU0A, COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Response | **status badge** | Approved (green) when the response code is 00, otherwise Declined (red), always with the word |  |  | CAFM-REQ-F-113 |
| Authorization | **summary card** | Card number, date (26 Nov 2026), time (HH:MM:SS), amount right-aligned with two decimals and a leading '-' when negative, decline reason as '<code> - <description>' ('9999 - ERROR' when the code is unknown), authorization code, POS entry mode, source, merchant category code, card expiry (MM/YY), authorization type, transaction ID and match status. Read afresh each time a row opens. With no row selected the panel says 'Select an authorization to see its details.' | Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed. |  | CAFM-REQ-F-112 |
| Report fraud / Remove fraud mark | **primary button** | Reads 'Report fraud' when the authorization is not marked fraud and 'Remove fraud mark' when it is. It opens a confirmation dialog that repeats what will change: the authorization, amount and merchant, and 'Fraud status: Not reported -> Fraud reported, dated today' or the reverse. On success it shows 'Authorization marked as fraud' or 'Fraud mark removed' and redisplays the same authorization with its new fraud status and date. The authorization and the fraud register change together or not at all. | Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.' |  | CAFM-REQ-F-114 |


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
| CAFM-BR-118 | Look up decline reason description | formatting | WHEN authorization details are being populated, THE Authorization Detail View SHALL show the reason as '<code>-<description>' from the decline reason table, or as '9999-ERROR' when the code is not in the table | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:319-328, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:319-328 |
| CAFM-BR-119 | Classify authorization as approved or declined | formatting | WHEN the authorization detail screen shows an authorization, THE authorization detail screen SHALL show response 'A' in green when the response code is '00', otherwise 'D' in red. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:311-317 |
| CAFM-BR-120 | Toggle authorization fraud mark | business rule | WHEN the user presses PF5 on the selected authorization, THE authorization detail screen SHALL re-read the authorization and, if its fraud flag is 'F', set it to 'R' with a remove-fraud action ('R'), otherwise set it to 'F' with a report-fraud action ('F'), and pass the record with account and customer number to the fraud processor (COPAUS2C). | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-252, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:93-104, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-52 |

### Worked examples

- CAFM-BR-119: response code = 00 → 'A' shown in green.
- CAFM-BR-119: response code = 05 → 'D' shown in red.
- CAFM-BR-120: fraud flag = F → Flag becomes 'R' and the fraud processor is asked to remove the fraud report.
- CAFM-BR-120: fraud flag = blank → Flag becomes 'F' and the fraud processor is asked to report fraud.
- CAFM-BR-120: fraud flag = R → Flag becomes 'F' and the fraud processor is asked to report fraud.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-118, CAFM-BR-119.
- SME-144: When the request to mark or unmark an authorization as fraud does not complete normally, what should the operator see, and what state should the authorization be left in? (Authorization business analyst) On CAFM-BR-120.
- SME-145: When adding or updating a fraud record fails for any reason other than a duplicate record, what status and message should go back to the operator? (Fraud management team) On CAFM-BR-120.
- SME-146: The fraud update is written to the fraud store first, then to the authorization detail record. If the second write fails after the first has succeeded, nothing is rolled back. Must both updates succeed or fail together? (Architecture team) On CAFM-BR-120.
- SME-147: When an authorization's fraud flag is changed, which data stores must hold the new fraud flag and fraud report date: the authorization detail record, the fraud store, or both? (Data architect) On CAFM-BR-120.
- SME-148: If the fraud update reports success but the authorization's database status is neither blank nor 'FW', what message should the system show? (Business analyst) On CAFM-BR-120.
- SME-149: Please confirm: after the fraud flag is changed, the system sends a fraud update request with the updated authorization record, the account ID and the customer ID, to be recorded in the authorization fraud store (CARDDEMO.AUTHFRDS). (Business analyst) On CAFM-BR-120.
- DEF-137: Is this intended? If the LINK to the fraud processor fails, the change is rolled back with no message; and on any rollback the screen still shows the toggled fraud flag that was not saved. (Subject-matter expert) On CAFM-BR-120.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).