# Feature specification: Page through an account's pending authorizations

**Feature:** CAFM-C10 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C10)

As a customer service operator, I want to page forward and back through an account's pending authorizations five at a time, with each shown as approved or declined, so that I can review every authorization on the account.

Lets customer service operators page forward (PF8) and back (PF7) through an account's pending authorizations five at a time. Each row shows 'A' for approved (response '00') or 'D' for declined, with amount, date, time, transaction id, type and match status. Paging must never skip or repeat authorizations, and the operator sees the stated message at the top or bottom of the list.

**Acceptance scenarios:**

1. **Given** pending authorizations for account: 7, **when** a page of authorizations is loaded and no error is flagged, **then** First page shows 5 rows and a next page is available (CAFM-C10-AC-01)
2. **Given** pending authorizations for account: 3, **when** a page of authorizations is loaded and no error is flagged, **then** 3 rows are shown and no next page is flagged (CAFM-C10-AC-02)
3. **Given** last authorization shown: key of row 5; key pressed: PF8, **when** the user pages forward (PF8), **then** Reading resumes after the fifth authorization shown (CAFM-C10-AC-03)
4. **Given** last authorization shown: none, **when** the user pages forward (PF8), **then** The start key is cleared and no repositioning is done (CAFM-C10-AC-04)
5. **Given** key pressed: PF8; next page exists: yes, **when** the user presses PF8 on the summary screen and a next page exists, **then** Next 5 pending authorizations are shown (CAFM-C10-AC-05)
6. **Given** key pressed: PF8; next page exists: 'Y', **when** the user pages forward (PF8) and a next page exists, **then** The list is cleared and refilled with the next authorizations (CAFM-C10-AC-06)
7. **Given** key pressed: PF8; more authorizations: none, **when** the user pages forward (PF8) and no further page of authorizations exists, **then** Message 'You are already at the bottom of the page...' is shown (CAFM-C10-AC-07)
8. **Given** Current page number: 3; Key: PF7, **when** the operator presses PF7 on the pending authorization summary screen and the current page number is greater than 1, **then** The list restarts at the first authorization saved for page 2 and shows up to five authorizations from there (CAFM-C10-AC-08)
9. **Given** Current page number: 2; Key: PF7, **when** the operator presses PF7 on the pending authorization summary screen and the current page number is greater than 1, **then** The first page of authorizations is shown again (CAFM-C10-AC-09)
10. **Given** Current page number: 1; Key: PF7, **when** the operator presses PF7 and the current page number is 1 or less, **then** Message 'You are already at the top of the page...' and the same list stays on screen (CAFM-C10-AC-10)
11. **Given** response code: '00', **when** an authorization is placed in the summary list, **then** Approval status shows 'A' (CAFM-C10-AC-11)
12. **Given** response code: '05', **when** an authorization is placed in the summary list, **then** Approval status shows 'D' (CAFM-C10-AC-12)
13. **Given** A pending authorization with approved amount 150.00, original date '240315' (YYMMDD) and original time '143005' (HHMMSS), **when** It is listed on the Pending authorizations screen, **then** Its row shows the approved amount as 150.00 with a sign and two decimals, the date as '03/15/24' and the time as '14:30:05', along with its transaction id, authorization type and match status (CAFM-C10-AC-13)

## Requirements

### Functional requirements

- **CAFM-REQ-F-101** (business rule): When a page of authorizations is loaded and no error is flagged, the system shall read up to 5 pending authorizations for the account into the list rows (on backward paging starting at the saved first key of that page), remember each page's first key and the last key shown, then read one more ahead to set whether a next page exists. Rules: CAFM-BR-105.
- **CAFM-REQ-F-102** (design note): When the user pages forward (PF8), the system shall re-read the account's authorization summary and reposition at the last authorization shown when one exists, otherwise clear the start key. Rules: CAFM-BR-106.
- **CAFM-REQ-F-103** (business rule): When the user presses PF8 and a next page exists, the system shall clear the five list rows, load the next page of up to 5 pending authorizations and redisplay the screen without a full erase. Rules: CAFM-BR-107, CAFM-BR-108.
- **CAFM-REQ-F-104** (business rule): When the user presses PF8 and no further page of authorizations exists, the system shall keep the current list and show 'You are already at the bottom of the page...'. Rules: CAFM-BR-109.
- **CAFM-REQ-F-105** (business rule): When the operator presses PF7 and the current page number is greater than 1, the system shall step the page number back by one, reposition to the saved first authorization key of that page, and redisplay up to five authorizations starting from that key without erasing the screen. Rules: CAFM-BR-110.
- **CAFM-REQ-F-106** (business rule): When the operator presses PF7 and the current page number is 1 or less, the system shall show 'You are already at the top of the page...' and leave the list unchanged. Rules: CAFM-BR-111.
- **CAFM-REQ-F-107** (business rule): When an authorization is placed in the summary list, the system shall show it as approved 'A' when its response code is '00' and as declined 'D' for any other response code. Rules: CAFM-BR-112.
- **CAFM-REQ-F-108** (formatting): When an authorization is listed, the system shall show its approved amount with a sign and two decimals, its original date held as YYMMDD as MM/DD/YY, and its original time held as HHMMSS as HH:MM:SS, along with transaction id, authorization type and match status. Rules: CAFM-BR-113, CAFM-BR-114.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-105 | Load a page of five authorizations | business rule | WHEN a page of authorizations is loaded and no error is flagged, THE Authorization List Builder SHALL read up to 5 pending authorizations for the account into the list rows (on backward paging starting at the saved first key of that page), remember each page's first key and the last key shown, then read one more ahead to set whether a next page exists. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:415-455, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:458-486 |
| CAFM-BR-106 | Position forward paging start key | design note | WHEN the user pages forward (PF8), THE Authorization List Paging SHALL re-read the account's authorization summary and reposition at the last authorization shown when one exists, otherwise clear the start key. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:386-402, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:488-520 |
| CAFM-BR-107 | Page forward on PF8 | business rule | WHEN the user presses PF8 on the summary screen and a next page exists, THE Authorization List Paging SHALL show the next page of up to 5 pending authorizations and redisplay the screen without a full erase. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:242-244, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:386-411 |
| CAFM-BR-108 | Show next authorization page | design note | WHEN the user pages forward (PF8) and a next page exists, THE Authorization List Paging SHALL clear the five list rows and load the next page of pending authorizations. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:404-407, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:608-662 |
| CAFM-BR-109 | Warn already at last page | business rule | WHEN the user pages forward (PF8) and no further page of authorizations exists, THE Authorization List Paging SHALL keep the current list and show 'You are already at the bottom of the page...'. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:404-411, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:446-451 |
| CAFM-BR-110 | Page backward on PF7 | business rule | WHEN the operator presses PF7 on the pending authorization summary screen and the current page number is greater than 1, THE Authorization List Paging SHALL step the page number back by one, reposition to the saved first authorization key of that page, and redisplay up to five authorizations starting from that key without erasing the screen. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:239-241, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:361-385, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:414-454, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:487-519 |
| CAFM-BR-111 | Warn already at first page | business rule | WHEN the operator presses PF7 and the current page number is 1 or less, THE Authorization List Paging SHALL show 'You are already at the top of the page...' and leave the list unchanged. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:239-241, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:361-385, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:414-454, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:487-519 |
| CAFM-BR-112 | Format authorization and derive approval status | business rule | WHEN an authorization is placed in the summary list, THE Authorization List SHALL show it as approved 'A' when its response code is '00' and as declined 'D' for any other response code. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:522-560, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:55, app/cpy/CSDAT01Y.cpy:30-35 |
| CAFM-BR-113 | Authorization origin date and time display conversion | formatting | WHEN an authorization is listed, THE Authorization List SHALL show its original date, held as YYMMDD, as MM/DD/YY and its original time, held as HHMMSS, as HH:MM:SS. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:525-534, app/cpy/CSDAT01Y.cpy:30-35, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:22-23 |
| CAFM-BR-114 | Format authorization and derive approval status | formatting | WHEN an authorization is placed in the summary list, THE Authorization List SHALL show its approved amount with a sign and two decimals, its original date as MM/DD/YY and its original time as HH:MM:SS, along with transaction id, authorization type and match status. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:522-560, app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl:55, app/cpy/CSDAT01Y.cpy:30-35 |

### Key entities

- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSMSG02Y (working storage)
- CVACT02Y (working storage)

### Needs clarification

- SME-137: On the pending-authorizations list screen, the PF3 (exit) key is accepted but nothing says what it does. Where should PF3 take the user? (Business analyst) On CAFM-BR-109, CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-106, CAFM-BR-114, CAFM-BR-110, CAFM-BR-111.
- SME-138: When an account typed on the pending-authorizations screen has no card cross-reference, account record or customer record, a 'not found' message appears but the inquiry carries on. Should a missing record stop the inquiry so no authorization list is shown, or should the screen still show whatever authorization data exists for that account ID? (Customer service operations lead) On CAFM-BR-109, CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-106, CAFM-BR-114, CAFM-BR-110, CAFM-BR-111.
- SME-139: When a page of pending authorizations is full, the system reads one more record ahead. What rule should decide that there is a next page, so that forward paging (PF8) is allowed? (Business analyst) On CAFM-BR-109, CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-106, CAFM-BR-114, CAFM-BR-110, CAFM-BR-111.
- SME-140: Please confirm: when the card cross-reference lookup succeeds, the account ID and customer ID it returns are the ones used to look up the account and the customer. (Business analyst) On CAFM-BR-109, CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-106, CAFM-BR-114, CAFM-BR-110, CAFM-BR-111.
- SME-141: Backward paging (PF7) seems unable to go back more than one page. Is that what happens in production? How many pages should be supported for accounts with more than 100 pending authorizations? (Customer service operations lead) On CAFM-BR-111.
- SME-142: An authorization shows as Approved ('A') only when its response code is '00'. Every other code shows as Declined ('D'), on both the list and the detail screens. Is this rule critical to the system's core purpose, and would getting it wrong be costly? (Card authorization product owner) On CAFM-BR-112.
- DEF-062: Is this intended? After PF7 has repositioned, the page-forward loop adds 1 to the page number again when it reads the first row, and it overwrites that page's saved first key with the key of the page just shown. Example: from page 2, PF7 shows page 1, but the stored page number goes back to 2. A second PF7 shows page 1 again instead of 'You are already at the top of the page...'. From page 3 or later, repeated PF7 presses keep showing the same page, so the operator can only go back one page. (Subject-matter expert) On CAFM-BR-110, CAFM-BR-111.

### Decision table gaps

None.
