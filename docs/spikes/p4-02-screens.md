# Spike P4-02: the screen inventory (25 November 2026)

On CardDemo run fa1f61, with no model and no AWS:

```bash
python -m reframe.design.inventory --run fa1f61
```

It writes `design/screens.json` and one 3270 copy per map in `outputs/design/legacy/`, with an index. It takes 0.3 seconds.

## What it read

| | CardDemo |
|---|---|
| BMS sources, mapsets and maps | 21 each, the optional modules' 4 included |
| Fields | 1,166: 135 input, 451 output (the program fills them), 393 labels, 187 stoppers |
| Maps matched to their symbolic copybook | 21 of 21; every named field is in it |
| Maps matched to the program that sends them | 21 of 21, one program each |
| Function keys shown on the screens | 72 |
| Key tests in the programs | 139, each with its line and the statement it leads to |

Each screen page shows the 3270 copy, its keys (what the screen says, where the program handles it, and where the two differ), the checks and every field. Spot-checked against the BMS source: Login, Update Account, View Authorizations and Add User are drawn as the maps define them.

## What it found in the source

**Keys that differ** between what a screen shows and what its program tests:

| Screen | Key | Finding |
|---|---|---|
| Add User (`COUSR1A`) | F12 | Shown on the screen; `COUSR01C` tests only ENTER, F3 and F4 |
| Transaction Type Update (`CTRTUPA`) | F6 | The screen says `F6=Add`; `COTRTUPC` never tests F6 |
| Delete User (`COUSR3A`) | F12 | `COUSR03C` handles it; the screen does not show it |
| View Authorization Details, Maintain Transaction Type, View Account, List Credit Cards | ENTER | Handled, but the screen does not say so: ENTER is implied |

The first two are candidates for the SME list: a key the user is told to press that does nothing.

**Eight notes on the maps themselves**, none an error in reading them:
- **Three User screens:** the user type field's attribute byte falls on the last character (a space) of its label.
- **Two credit card screens:** the function key line's attribute byte falls on the last cell of an 80-column message line above it.
- **View Authorization Details:** the same as the User screens, on its transaction ID label.
- **Update Account and View Account:** an unnamed 9-character field at line 1, column 1 sits over the "Tran:" label, so 3270 shows neither.

The spec's check is therefore a report, not a stop. Overlaps are named by kind (data over data, an attribute byte on data, a shared attribute byte), and a zero-length stopper, which only ends the field before it, is not counted.

## What the reading had to handle

- **Continuation:** a non-blank in column 72 continues a statement from column 16. Inside a quoted string the text runs to column 71, blanks included. Outside one, the operand ends at its last non-blank. Strings such as `'ENTER=Continue  F3=Back  F7=Backward  F8=Forwar-` / `d'` span lines.
- **Keys tested two ways:**
  - directly: `EVALUATE EIBAID` / `WHEN DFHPF3`, as in `COSGN00C`;
  - through flags a shared copybook sets: `CCARD-AID-PFK03` from `CSSTRPFY`.

  A `SET ... TO TRUE` is an assignment, not a test, and is skipped.
- **Dark keys:** Update Account shows `F5=Save F12=Cancel` dark (`DRK`) until the program reveals them, so keys are read from every field with initial text, and the copy draws dark fields dim.
- **Commented-out code:** `COCRDLIC` has `*COPY COCRDSL.`. Lines with `*` or `/` in column 7 are skipped, or the list program would be counted as using the detail screen.
- **Titles:** most maps carry their title as a label; Login and Transaction Type Update set it from the program, so the title comes from the BMS file's opening comment.

## For P4-03, the screen flow

- **Map and program names held in variables:** `SEND MAP(CCARD-NEXT-MAP) MAPSET(CCARD-NEXT-MAPSET)` and `XCTL PROGRAM(CDEMO-TO-PROGRAM)` use variables set from `LIT-` constants, which have `VALUE` clauses in the same program. Resolving those statically should settle most links without a model.
- **Menus:** the menu options are tables in `COMEN02Y` and `COADM02Y`, each with the program name per option.
- **F3:** usually leads to `MOVE LIT-MENUTRANID TO CDEMO-TO-TRANID` or similar, so the "back" target comes from those constants too.
