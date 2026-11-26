# Design: Show statement header and holder details (ASGD-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The top of each statement tells the cardholder whose account it covers: the cardholder's name and address, the account ID, current balance and FICO score. The HTML version also shows the issuer, Bank of XYZ. Names, addresses and the balance must come from the right customer and account records, formatted exactly as specified, with negative balances clearly marked.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- COSTM01 (working storage of CBSTM03A): see data-contracts.md.
- CUSTREC (working storage of CBSTM03A): see data-contracts.md.
- CVACT01Y (working storage of CBSTM03A): see data-contracts.md.
- CVACT03Y (working storage of CBSTM03A): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-013 | Write statement header and account details | formatting | WHEN a statement is produced for a card, THE statement job SHALL write to the text statement, in order: the '*START OF STATEMENT*' banner, the holder name, three address lines, a dashed line, the 'Basic Details' heading, the Account ID, Current Balance and FICO Score lines, the 'TRANSACTION SUMMARY ' heading and the 'Tran ID', 'Tran Details', 'Tran Amount' column headings. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-014 | Assemble statement holder details | formatting | THE statement job SHALL form the holder name from the customer's first, middle and last name, keeping each name only up to its first space and joining them with single spaces. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-015 | Assemble statement holder details | formatting | THE statement job SHALL print address lines 1 and 2 as held on the customer record, and SHALL form address line 3 from address line 3, state code, country code and ZIP, each kept only up to its first space and joined with single spaces. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-016 | Write statement header and account details | formatting | THE statement job SHALL show the account ID and current balance from the account record and the FICO score from the customer record, with the balance printed as nine whole digits and two decimals with a trailing minus sign when negative. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-017 | Assemble statement holder details | formatting | WHEN a statement is produced for a card, THE statement job SHALL start the HTML statement with a page header holding the heading 'Statement for Account Number: ' with the account ID and the bank block 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999'. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |
| ASGD-BR-018 | Issuer branding and address hardcoded on HTML statements | formatting | THE HTML statement SHALL show the fixed issuer heading 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999' on every statement; the text statement shows no issuer block. | medium | app/cbl/CBSTM03A.CBL:167-172, app/cbl/CBSTM03A.CBL:537-544, app/cbl/CBSTM03A.CBL:458-503 |
| ASGD-BR-019 | Write holder name, address and basic details | formatting | THE statement job SHALL then write to the HTML statement the holder name (at most 50 characters, cut at the first double space), the three address lines, the 'Basic Details' heading, the Account ID, Current Balance and FICO Score lines, the 'Transaction Summary' heading and the 'Tran ID', 'Tran Details', 'Amount' column headings. | high | app/cbl/CBSTM03A.CBL:85-146, app/cbl/CBSTM03A.CBL:148-223, app/cbl/CBSTM03A.CBL:458-504, app/cbl/CBSTM03A.CBL:506-555 |

### Worked examples

- ASGD-BR-018: account = 00000000001 → The HTML statement header shows 'Bank of XYZ', '410 Terry Ave N', 'Seattle WA 99999'

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-016, ASGD-BR-017, ASGD-BR-019.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-016, ASGD-BR-017, ASGD-BR-019.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-016, ASGD-BR-017, ASGD-BR-019.
- DEF-090: Is this intended? Each name and address part is cut at its first space, so multi-word names and cities are shortened. When the middle name is blank, the text name has a double space, and the HTML name (cut at the first double space) shows only the first name. The balance field holds nine whole digits while the account balance holds ten, so the leading digit is lost on balances of 1,000,000,000 or more. (Subject-matter expert) On ASGD-BR-016, ASGD-BR-017, ASGD-BR-019.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).