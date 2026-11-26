# Implementation plan: Update transaction type descriptions from the list (TTRDM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

### Transaction types (S-TRANTYPE-LIST)

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT | TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046 |


## Data model

- COCOM01Y (working storage of COTRTLIC): see data-contracts.md.
- COTTL01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RPY (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RWY (working storage of COTRTLIC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTLIC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTLIC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTLIC): see data-contracts.md.
- CVACT02Y (working storage of COTRTLIC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTLIC): see data-contracts.md.

## Design notes

- TTRDM-BR-048: The list form submits the two filters and, for each of up to 7 rows, the action code, type code and description. The server binds these into a request model, treating a description of '*' or only spaces as not entered and trimming any other description.
- TTRDM-BR-049: Normalise each submitted row description on input: blank or a lone '*' becomes 'not entered' (null); any other value is trimmed of leading and trailing spaces before comparison and validation.

## Decision tables

#### Updated description check for a row marked 'U'

| Entered description vs stored (ignoring case and leading/trailing spaces) | Description entered (not blank or '*') | Only letters, digits and spaces | Validation result | Rule |
|---|---|---|---|---|
| Same | - | - | Show 'No change detected with respect to database values.'; skip remaining checks | TTRDM-BR-050 |
| Different | No | - | Reject; show 'Transaction Desc must be supplied.' unless an earlier message is set | TTRDM-BR-052 |
| Different | Yes | No | Reject; show 'Transaction Desc can have numbers or alphabets only.' unless an earlier message is set | TTRDM-BR-053 |
| Different | Yes | Yes | Treat row as changed; first 50 characters checked as required 'Transaction Desc' | TTRDM-BR-051 |
| Different | Yes | Yes | **Gap:** No rule states what happens next for a valid changed description (how the update is confirmed and saved), nor how a row marked 'D' is confirmed and deleted online. | |
| Different | Yes | Yes (over 50 characters) | **Gap:** Only the first 50 characters are checked; rules do not say what happens to text beyond 50 characters. | |

