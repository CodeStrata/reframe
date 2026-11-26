# Feature specification: Confirm and save the account update

**Feature:** OATM-C06 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C06)

As an operator, I want to confirm validated changes and have them saved only if nobody else has changed the record meanwhile, so that I do not overwrite another user's update.

Lets the operator confirm validated changes and saves them to the account and customer records. The save goes through only if nobody else has changed those records since they were shown. It must never overwrite another user's update. Every confirmed value, including the account group, must be saved to its own field and never into another field.

**Acceptance scenarios:**

1. **Given** key pressed: PF5; update state: changes not yet validated (not 'N'), **when** the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched, **then** PF5 is not allowed; the request is treated as Enter and the screen is processed again (OATM-C06-AC-01)
2. **Given** key pressed: PF5; update state: 'N' (changes OK, awaiting confirmation), **when** the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched, **then** PF5 is valid and the save goes ahead (OATM-C06-AC-02)
3. **Given** key pressed: PF12; account details: not yet fetched, **when** the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched, **then** PF12 is not allowed; the request is treated as Enter (OATM-C06-AC-03)
4. **Given** credit limit when details were shown: 5000.00; credit limit in file at save (PF5): 7000.00, **when** any stored account or customer value differs from the value fetched when the details were shown, **then** Save stops, nothing is rewritten, the details are shown again with 'Record changed by some one else. Please review' (OATM-C06-AC-04)
5. **Given** customer last name when shown: SMITH; customer last name in file at save: smith, **when** any stored account or customer value differs from the value fetched when the details were shown, **then** Treated as unchanged (case is ignored) and the save continues (OATM-C06-AC-05)
6. **Given** all account and customer values: same as when shown, **when** any stored account or customer value differs from the value fetched when the details were shown, **then** Save continues to rewrite the account and customer records (OATM-C06-AC-06)
7. **Given** account 00000000099 has stored ZIP and account group values, and the operator has changed the account group to 'GOLDGROUP1' and confirmed the update, **when** the update is saved, **then** legacy behaviour to reconcile against: the stored ZIP position (offsets 103-112) holds 'GOLDGROUP1', and the stored group-ID position holds the content of the unset filler area instead of the entered group (OATM-C06-AC-07)

## Requirements

### Functional requirements

- **OATM-REQ-F-059** (business rule): When the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation ('N'), and not PF12 after the account details are fetched, the system shall reject the requested key operation and treat the request as Enter, while allowed keys keep their requested operation. Rules: OATM-BR-058.
- **OATM-REQ-F-060** (error handling): If any stored account or customer value differs from the value fetched when the details were shown, then the system shall flag 'Record changed by some one else. Please review' and stop the save. Rules: OATM-BR-059.
- **OATM-REQ-F-061** (design note): When a confirmed account update is saved, the system shall rewrite the account record from a layout that has no ZIP field, so that the entered account group ID goes into the stored ZIP position (offsets 103-112) and the stored group-ID position is overwritten with whatever the unset filler area holds. Rules: OATM-BR-060.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-058 | Restrict permitted keys by update state | business rule | WHEN the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched, THE Account Update Key Permission SHALL reject the requested key operation and treat the request as Enter; allowed keys are marked valid and keep their requested operation | medium | app/cbl/COACTUPC.cbl:898-899,905-912,914-916, app/cbl/COACTUPC.cbl:905-959 |
| OATM-BR-059 | Detect changes made by another user | error handling | IF any stored account or customer value differs from the value fetched when the details were shown, THEN THE Account Update Concurrency Check SHALL flag 'Record changed by some one else. Please review' and stop the save | medium | app/cbl/COACTUPC.cbl:4109,4115,4117,4119,4121,4123,4125,4127-4129,4131-4133,4135-4137,4139-4145,4152-4179,4181-4191, app/cbl/COACTUPC.cbl:4109-4192 |
| OATM-BR-060 | Persisted record formatting and account record layout | design note | WHEN a confirmed account update is saved, THE account update program SHALL rewrite the account record from a layout that has no ZIP field, so the account group ID entered goes into the stored ZIP position (offsets 103-112), and the stored group-ID position is overwritten with whatever the unset filler area holds. | medium | app/cbl/COACTUPC.cbl:418-433, app/cpy/CVACT01Y.cpy:4-16, app/cbl/COACTUPC.cbl:3956, app/cbl/COACTUPC.cbl:4002 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSLKPCDY (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDPY (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-062: What should the account update screen do in each of these cases: exit (PF3), first entry before any details are fetched, arriving from the menu, a completed save, a failed save, cancel (PF12), details shown, and answering 'N' to confirmation (PF5)? (Business analyst) On OATM-BR-058.
- SME-066: When account update saves changes, the account record is written before the customer record. Must both be saved together, so that if the customer save fails the account change is rolled back? How critical is this, given it changes balances, limits and regulated customer data? (Account servicing SME / architecture team) On OATM-BR-059.
- DEF-159: Is this intended? The account update record layout leaves out the account ZIP field, so every save shifts the group ID into the ZIP position and overwrites the real group ID with filler. The next read then shows a wrong group ID, and the account ZIP is lost. (Subject-matter expert) On OATM-BR-060.

### Decision table gaps

None.
