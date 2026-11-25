"""P4-02: the screen inventory read from BMS with no model, and each screen drawn as a 3270 copy."""
import tempfile
import unittest
from pathlib import Path

from reframe.design import inventory as inv
from reframe.design import legacy


def card(label: str, op: str, operands: list[str]) -> str:
    """BMS lines as an assembler card deck: label in 1-8, operation from 10, operands from 16, a continuation mark in 72."""
    lines = []
    for i, operand in enumerate(operands):
        last = i == len(operands) - 1
        head = f"{label:<8} {op:<6} " if i == 0 else " " * 15
        text = head + operand + ("" if last else ",")
        while len(text) > 71:  # a long operand continues from column 16
            lines.append(text[:71] + "-")
            text = " " * 15 + text[71:]
        lines.append(text.ljust(71) + ("-" if not last else ""))
    return "\n".join(lines)


SOURCE = "\n".join([
    "******************************************************************",
    "*    CardDemo - Test Screen",
    "* Licensed under the Apache License, Version 2.0",
    "******************************************************************",
    card("TESTS00", "DFHMSD", ["CTRL=(ALARM,FREEKB)", "LANG=COBOL", "MODE=INOUT", "TYPE=&&SYSPARM"]),
    card("TESTS0A", "DFHMDI", ["COLUMN=1", "LINE=1", "SIZE=(24,80)"]),
    card("", "DFHMDF", ["ATTRB=(ASKIP,NORM)", "COLOR=BLUE", "LENGTH=6", "POS=(1,1)", "INITIAL='Tran :'"]),
    card("TRNNAME", "DFHMDF", ["ATTRB=(ASKIP,FSET,NORM)", "LENGTH=4", "POS=(1,8)"]),
    card("USERID", "DFHMDF", ["ATTRB=(FSET,IC,NORM,UNPROT)", "COLOR=GREEN", "LENGTH=8", "POS=(5,20)"]),
    card("", "DFHMDF", ["ATTRB=(ASKIP,NORM)", "LENGTH=0", "POS=(5,29)"]),
    card("PASSWD", "DFHMDF", ["ATTRB=(DRK,FSET,UNPROT)", "LENGTH=8", "POS=(6,20)"]),
    card("", "DFHMDF", ["ATTRB=(ASKIP,NORM)", "COLOR=YELLOW", "LENGTH=60", "POS=(24,1)",
                        "INITIAL='ENTER=Sign-on  F3=Exit  F12=Cancel, don''t save  this text runs long'"]),
    card("", "DFHMDF", ["ATTRB=(ASKIP,NORM)", "LENGTH=10", "POS=(1,5)", "INITIAL='ovl'"]),
    card("BEYOND", "DFHMDF", ["ATTRB=(ASKIP,NORM)", "LENGTH=10", "POS=(30,1)"]),
    card("", "DFHMSD", ["TYPE=FINAL"]),
    "         END",
])

SYMBOLIC = "       01 TESTS0AI.\n          02 TRNNAMEI PIC X(4).\n          02 USERIDI PIC X(8).\n          02 PASSWDI PIC X(8).\n"

PROGRAM = """       IDENTIFICATION DIVISION.
       PROGRAM-ID. TESTS00C.
       DATA DIVISION.
       COPY TESTS00.
       PROCEDURE DIVISION.
           EVALUATE EIBAID
               WHEN DFHENTER
                   PERFORM PROCESS-ENTER-KEY
               WHEN DFHPF3
                   MOVE 'COSGN00C' TO CDEMO-TO-PROGRAM
               WHEN OTHER
                   CONTINUE
           END-EVALUATE.
           IF CCARD-AID-PFK05
              PERFORM SAVE-IT
           END-IF
           SET CCARD-AID-PFK07 TO TRUE.
"""


class StatementsTest(unittest.TestCase):
    def test_continuation_inside_and_outside_quotes(self):
        found = inv.statements(SOURCE)
        self.assertEqual([s.op for s in found][:3], ["DFHMSD", "DFHMDI", "DFHMDF"])
        keys = next(s for s in found if "Sign-on" in str(s.operands.get("INITIAL", "")))
        self.assertEqual(keys.operands["INITIAL"], "ENTER=Sign-on  F3=Exit  F12=Cancel, don't save  this text runs long")
        self.assertEqual(keys.operands["POS"], ["24", "1"])
        self.assertEqual(found[0].operands["CTRL"], ["ALARM", "FREEKB"])

    def test_remarks_after_the_operands_are_dropped(self):
        found = inv.statements("TEST0A   DFHMDI SIZE=(24,80)                          a remark")
        self.assertEqual(found[0].operands, {"SIZE": ["24", "80"]})


class InventoryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        other = "       PROGRAM-ID. OTHER00C.\n      *COPY TESTS00.\n"
        for folder, name, text in (("app/bms", "TESTS00.bms", SOURCE), ("app/cpy-bms", "TESTS00.CPY", SYMBOLIC), ("app/cbl", "TESTS00C.cbl", PROGRAM),
                                   ("app/cbl", "OTHER00C.cbl", other)):
            (root / folder).mkdir(parents=True, exist_ok=True)
            (root / folder / name).write_text(text)
        self.found = inv.inventory(root)
        self.screen = self.found["screens"][0]

    def test_maps_fields_and_kinds(self):
        s = self.screen
        self.assertEqual((s["mapset"], s["map"], s["size"], s["title"]), ("TESTS00", "TESTS0A", [24, 80], "Test Screen"))
        by = {f["name"]: f for f in s["fields"] if f["name"]}
        self.assertEqual((by["USERID"]["kind"], by["USERID"]["line"], by["USERID"]["column"], by["USERID"]["attributes"]),
                         ("input", 5, 20, ["FSET", "IC", "NORM", "UNPROT"]))
        self.assertEqual(by["TRNNAME"]["kind"], "output")
        self.assertEqual(s["counts"], {"input": 2, "output": 2, "label": 3, "stopper": 1})
        self.assertEqual(s["symbolic"], "app/cpy-bms/TESTS00.CPY")
        self.assertEqual(s["programs"], [{"name": "TESTS00C", "file": "app/cbl/TESTS00C.cbl"}])  # not OTHER00C, whose COPY is a comment

    def test_checks_name_overlaps_fields_outside_and_the_symbolic_copybook(self):
        problems = self.screen["problems"]
        self.assertTrue(any("the label 'ovl'" in p and "covers the data of TRNNAME" not in p and "the label 'Tran :'" in p for p in problems))
        self.assertTrue(any(p.startswith("BEYOND at line 30") and "outside" in p for p in problems))
        self.assertIn("BEYOND is not in the symbolic map copybook", problems)
        self.assertFalse(any("line 5, column 29" in p for p in problems))  # a zero-length stopper is not an overlap

    def test_function_keys_shown_and_handled(self):
        keys = self.screen["keys"]
        self.assertEqual([(k["key"], k["says"]) for k in keys["shown"]], [("ENTER", "Sign-on"), ("F3", "Exit"), ("F12", "Cancel, don't save")])
        handled = {k["key"]: k for k in keys["handled"]}
        self.assertEqual(set(handled), {"ENTER", "F3", "F5"})  # SET CCARD-AID-PFK07 TO TRUE is not a test of the key
        self.assertEqual((handled["ENTER"]["line"], handled["ENTER"]["action"]), (7, "PERFORM PROCESS-ENTER-KEY"))
        self.assertEqual(handled["F5"]["action"], "PERFORM SAVE-IT")
        self.assertEqual(keys["shown_not_handled"], ["F12"])
        self.assertEqual(keys["handled_not_shown"], ["F5"])

    def test_key_names(self):
        self.assertEqual([inv.key_name(k) for k in ("PF3", "PFK03", "F12", "ENTER", "pa1")], ["F3", "F3", "F12", "ENTER", "PA1"])

    def test_the_3270_copy(self):
        text = legacy.grid(self.screen)
        self.assertEqual(text.count("\n"), 23)  # 24 lines
        self.assertIn('class="f in"', text)  # an input field is underlined
        self.assertIn("ENTER=Sign-on", text)
        page = legacy.page(self.screen, "demo")
        self.assertIn("shown, handling not found", page)
        self.assertIn("handled, not shown on the screen", page)
        self.assertNotIn("http", page.replace("http-equiv", ""))  # nothing loaded from outside


if __name__ == "__main__":
    unittest.main()
