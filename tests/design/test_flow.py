"""P4-03: how the screens connect, read from the source with no model, each link citing its lines."""
import tempfile
import unittest
from pathlib import Path

from reframe.design import flow, flowpage, inventory
from tests.design.test_inventory import card


def cobol(*lines: str) -> str:
    """Fixed-format COBOL: sequence area, then code from column 8."""
    return "\n".join(("      " + line) if line.startswith("*") else ("       " + line) for line in lines) + "\n"


def bms(mapset: str, mapname: str, keys: str) -> str:
    return "\n".join([card(mapset, "DFHMSD", ["LANG=COBOL", "TYPE=&&SYSPARM"]), card(mapname, "DFHMDI", ["SIZE=(24,80)"]),
                      card("OPTION", "DFHMDF", ["ATTRB=(UNPROT)", "LENGTH=2", "POS=(5,10)"]),
                      card("", "DFHMDF", ["ATTRB=(ASKIP)", "LENGTH=30", "POS=(24,1)", f"INITIAL='{keys}'"]), card("", "DFHMSD", ["TYPE=FINAL"])])


MENU_TABLE = cobol(
    "01 MENU-OPTIONS.",
    "  05 MENU-OPTIONS-DATA.",
    "    10 FILLER PIC 9(02) VALUE 1.",
    "    10 FILLER PIC X(20) VALUE 'Account View'.",
    "    10 FILLER PIC X(08) VALUE 'ACCTV00C'.",
    "    10 FILLER PIC 9(02) VALUE 2.",
    "    10 FILLER PIC X(20) VALUE 'Not built yet'.",
    "    10 FILLER PIC X(08) VALUE 'DUMMY'.",
    "  05 MENU-OPTIONS-TABLE REDEFINES MENU-OPTIONS-DATA.",
    "    10 MENU-OPT OCCURS 2 TIMES.",
    "      15 MENU-OPT-NUM PIC 9(02).",
    "      15 MENU-OPT-NAME PIC X(20).",
    "      15 MENU-OPT-PGMNAME PIC X(08).",
)

SIGNON = cobol(
    "IDENTIFICATION DIVISION.", "PROGRAM-ID. SIGN00C.", "DATA DIVISION.", "WORKING-STORAGE SECTION.", "COPY SIGN00.",
    "PROCEDURE DIVISION.",
    "    EVALUATE EIBAID",
    "        WHEN DFHENTER",
    "            EXEC CICS XCTL",
    "                 PROGRAM ('MENU00C')",
    "            END-EXEC",
    "        WHEN DFHPF3",
    "            PERFORM SEND-GOODBYE",
    "    END-EVALUATE.",
)

MENU = cobol(
    "IDENTIFICATION DIVISION.", "PROGRAM-ID. MENU00C.", "DATA DIVISION.", "WORKING-STORAGE SECTION.", "COPY MENU00.", "COPY MENU02Y.",
    "PROCEDURE DIVISION.",
    "    IF EIBCALEN = 0",
    "        MOVE 'SIGN00C' TO TO-PROGRAM",
    "        EXEC CICS XCTL PROGRAM(TO-PROGRAM) END-EXEC",
    "    END-IF",
    "    EXEC CICS XCTL",
    "         PROGRAM(MENU-OPT-PGMNAME(WS-OPTION))",
    "    END-EXEC.",
)

ACCOUNT = cobol(
    "IDENTIFICATION DIVISION.", "PROGRAM-ID. ACCTV00C.", "DATA DIVISION.", "WORKING-STORAGE SECTION.",
    "01 WS-LITERALS.",
    "   05 LIT-THISPGM PIC X(8) VALUE 'ACCTV00C'.",
    "   05 LIT-MENUPGM PIC X(8) VALUE 'MENU00C'.",
    "COPY ACCTV00.",
    "PROCEDURE DIVISION.",
    "    EVALUATE TRUE",
    "       WHEN CCARD-AID-PFK03",
    "       WHEN SOMETHING-ELSE",
    "*           back to the caller, or the menu",
    "            IF FROM-PROGRAM EQUAL SPACES",
    "               MOVE LIT-MENUPGM TO TO-PROGRAM",
    "            ELSE",
    "               MOVE FROM-PROGRAM TO TO-PROGRAM",
    "            END-IF",
    "            MOVE LIT-THISPGM TO FROM-PROGRAM",
    "            EXEC CICS XCTL",
    "                 PROGRAM (TO-PROGRAM)",
    "            END-EXEC",
    "       WHEN CCARD-AID-PFK07",
    "            PERFORM PAGE-BACK",
    "    END-EVALUATE.",
)

CSD = """ DEFINE TRANSACTION(SG00) GROUP(DEMO)
        PROGRAM(SIGN00C) TWASIZE(0)
 DEFINE TRANSACTION(MN00) GROUP(DEMO)
        PROGRAM(MENU00C) TWASIZE(0)
 DEFINE PROGRAM(SIGN00C) GROUP(DEMO)
"""


class FlowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        files = {"app/bms/SIGN00.bms": bms("SIGN00", "SIGN0A", "ENTER=Sign-on  F3=Exit"), "app/bms/MENU00.bms": bms("MENU00", "MENU0A", "ENTER=Go  F3=Exit"),
                 "app/bms/ACCTV00.bms": bms("ACCTV00", "ACCTV0A", "F3=Back  F7=Up"),
                 "app/cpy/MENU02Y.cpy": MENU_TABLE, "app/cbl/SIGN00C.cbl": SIGNON, "app/cbl/MENU00C.cbl": MENU, "app/cbl/ACCTV00C.cbl": ACCOUNT,
                 "app/csd/DEMO.csd": CSD}
        for name, text in files.items():
            (self.root / name).parent.mkdir(parents=True, exist_ok=True)
            (self.root / name).write_text(text)
        self.screens = inventory.inventory(self.root)
        self.found = flow.flow(self.root, self.screens)

    def links(self, kind):
        return {(l["from"], l["to"]) for l in self.found["links"] if l["kind"] == kind}

    def test_tables_filled_by_value_clauses(self):
        table = flow.tables(flow.data_items(MENU_TABLE, "MENU02Y.cpy"))
        self.assertEqual([(r["MENU-OPT-NUM"], r["MENU-OPT-NAME"], r["MENU-OPT-PGMNAME"]) for r in table["MENU-OPT-PGMNAME"]],
                         [("1", "Account View", "ACCTV00C"), ("2", "Not built yet", "DUMMY")])

    def test_transactions_transfers_and_menu_options(self):
        self.assertEqual(self.links("transaction"), {("SG00", "SIGN00C"), ("MN00", "MENU00C")})
        xctl = self.links("xctl")
        self.assertIn(("SIGN00C", "MENU00C"), xctl)  # a literal
        self.assertIn(("MENU00C", "SIGN00C"), xctl)  # moved into the variable
        self.assertIn(("MENU00C", "ACCTV00C"), xctl)  # a menu option, from the table; DUMMY is left out
        self.assertNotIn(("MENU00C", "DUMMY"), xctl)
        option = next(l for l in self.found["links"] if l["to"] == "ACCTV00C" and l["kind"] == "xctl")
        self.assertEqual(option["option"]["MENU-OPT-NAME"], "Account View")
        self.assertEqual(self.found["unresolved"], [])
        self.assertEqual(flow.check(self.found, self.root), [])  # every cited line exists

    def test_keys_lead_to_their_targets(self):
        to = {(k["screen"], k["key"]): k["to"] for k in self.found["keys"]}
        self.assertEqual(to[("SIGN0A", "ENTER")], ["MENU00C"])
        self.assertEqual(to[("SIGN0A", "F3")], [])  # it says goodbye: no transfer
        self.assertEqual(sorted(to[("ACCTV0A", "F3")]), [flow.CALLER, "MENU00C"])  # stacked WHENs and a nested IF
        self.assertEqual(to[("ACCTV0A", "F7")], [])

    def test_reach_and_the_map(self):
        self.assertEqual({r["screen"]: r["reached"] for r in self.found["reach"]},
                         {"SIGN0A": "navigated", "MENU0A": "navigated", "ACCTV0A": "navigated"})
        edges = flowpage.forward(self.found)
        self.assertEqual(flowpage.layers(["SIGN0A", "MENU0A", "ACCTV0A"], edges), [["SIGN0A"], ["MENU0A"], ["ACCTV0A"]])

    def test_branch_ends_at_the_closing_when(self):
        program = flow.read_program(self.root / "app/cbl/ACCTV00C.cbl", self.root, flow._copybooks(self.root))
        test = next(i for i, b in enumerate(program.lines, 1) if "CCARD-AID-PFK03" in b)
        first, last = flow._branch(program, test)
        self.assertIn("END-EXEC", program.lines[last - 1])
        self.assertIn("SPACES", " ".join(program.lines[first - 1:last]))


if __name__ == "__main__":
    unittest.main()
