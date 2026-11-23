import tempfile
import unittest
from pathlib import Path

from reframe.transform import documents

DOCUMENT = """# Account Statements — Requirements


## Global Preconditions

- All operations require valid input data.


## Job Dependencies

### MONTHLY-Statements

**Schedule:** Monthly, completes by 23:00


## 1. Statement Generation
As a reporting team, I want a statement for every card
so that each customer receives one.

**Schedule:** Monthly, completes by 23:00
**Restart/Recovery:** Outputs are discarded if the run fails.

### Requirements

REQ-F-001: [Event-driven] When a card is read, the system shall write
its statement line.

REQ-F-002: [Unwanted] If the card is unknown, then the system shall skip it.

### Non-Functional Requirements

REQ-N-001: [Ubiquitous] The system shall finish by 23:00.

### Open Questions

OQ-001: Which date is the statement date? — Owner: reporting business owner

OQ-002: Is the cutoff a business rule? (Owner: batch operations team)

OQ-003: Should a failed run alert someone? Owner: batch operations team.

OQ-004: [Unverified — content not supported by its cited rule; confirm] The system shall sort by card number.


---


## 2. PDF Conversion
As a reporting team, I want a PDF copy.

### Requirements

REQ-F-003: [Ubiquitous] The system shall convert the statement to PDF.
"""


class DocumentsTest(unittest.TestCase):
    def test_every_part_of_a_requirements_document(self):
        parsed = documents.parse(DOCUMENT)
        self.assertEqual(parsed["title"], "Account Statements")
        self.assertEqual([n["heading"] for n in parsed["notes"]], ["Global Preconditions", "Job Dependencies"])
        self.assertIn("MONTHLY-Statements", parsed["notes"][1]["markdown"])
        first, second = parsed["capabilities"]
        self.assertEqual((first["number"], first["title"]), (1, "Statement Generation"))
        self.assertEqual(first["story"], "As a reporting team, I want a statement for every card so that each customer receives one.")
        self.assertEqual(first["fields"], {"Schedule": "Monthly, completes by 23:00", "Restart/Recovery": "Outputs are discarded if the run fails."})
        self.assertEqual([(r["code"], r["kind"], r["pattern"]) for r in first["requirements"]],
                         [("REQ-F-001", "F", "Event-driven"), ("REQ-F-002", "F", "Unwanted"), ("REQ-N-001", "N", "Ubiquitous")])
        self.assertEqual(first["requirements"][0]["text"], "When a card is read, the system shall write its statement line.")
        self.assertEqual([(q["code"], q["owner"], q["unverified"]) for q in first["questions"]],
                         [("OQ-001", "reporting business owner", False), ("OQ-002", "batch operations team", False),
                          ("OQ-003", "batch operations team", False), ("OQ-004", "", True)])
        self.assertEqual(first["questions"][0]["text"], "Which date is the statement date?")
        self.assertEqual(first["questions"][3]["text"], "The system shall sort by card number.")
        self.assertEqual([r["code"] for r in second["requirements"]], ["REQ-F-003"])
        self.assertEqual(documents.count_questions(DOCUMENT), 4)

    def test_catalog_names_and_descriptions(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "catalog"
            catalog.mkdir()
            (catalog / "business_domains.json").write_text('{"domains": [{"name": "Credit Card Account Management", "description": "Manage accounts."}]}')
            (catalog / "business_function.csv").write_text(
                "bf_name,bf_id,bf_description,bd_id,bd_name,bd_description,path_name\n"
                "Account and Statement Reporting,BF-1,Produces statements.,BD-1,Credit Card Account Management,Manage accounts.,p1\n"
                "Account and Statement Reporting,BF-1,Produces statements.,BD-1,Credit Card Account Management,Manage accounts.,p2\n"
                "Application Navigation,BF-2,Sign-on and menus.,BD-2,Technical,Technical functions.,p3\n")
            found = documents.catalog(Path(tmp))
        self.assertEqual(found["functions"][documents.squeeze("AccountandStatementReporting")]["description"], "Produces statements.")
        self.assertEqual(list(found["domains"]), ["creditcardaccountmanagement", "technical"])
        self.assertEqual(documents.spaced("UserAccessControl"), "User Access Control")


if __name__ == "__main__":
    unittest.main()
