import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from reframe.core.runfolder import new_run
from reframe.core.shell import Aws, Result
from reframe.report import build
from reframe.source.s3 import Bucket
from reframe.transform import retrieve

from tests.fakes import FakeRunner

REQUIREMENTS = """# Card Payments — Requirements


## Global Preconditions

- The payment store is available.


## 1. Payment Entry
As a payments clerk, I want each payment recorded so that the account balance is right.

**Restart/Recovery:** A failed run leaves no partial output.

### Requirements

REQ-F-001: [Event-driven] When the operator enters a payment, the system shall record it in `PAYFILE`.

REQ-F-002: [Unwanted] If the amount is zero, then the system shall reject it with 'Amount required'.

### Non-Functional Requirements

REQ-N-001: [Ubiquitous] The system shall respond within two seconds.

### Open Questions

OQ-001: Is a negative amount ever valid? — Owner: payments business owner

OQ-002: [Unverified — content not supported by its cited rule; confirm] The system shall print a receipt.


---


## Generation Notes

Generated from 3 rules.
"""
TRACEABILITY = """function: CardPayments
summary:
  total_rules: 3
  captured: 2
  not_applicable: 1
requirements:
- req_id: REQ-F-001
  rule_ids: [r1]
rules:
- rule_id: r1
  program: PAY01C
  disposition: captured
  rule_name: Record a payment
  rule_text: WHEN a payment is entered THE system SHALL record it
  req_ids: "['REQ-F-001']"
"""


def spec_zip():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("spec/Payments/CardPayments/requirements.md", REQUIREMENTS)
        z.writestr("spec/Payments/CardPayments/traceability.yaml", TRACEABILITY)
        z.writestr("spec/Payments/CardPayments/discovery/programs.yaml", "programs:\n- name: PAY01C\n  type: COBOL\n  execution: online\n")
        z.writestr("spec/data-model.md", "# Data Model\n\n| Data Store | Type |\n|---|---|\n| PAYFILE | VSAM |\n")
        z.writestr("spec/Unassigned-Programs/requirements.md", "# Unassigned Programs — Requirements\n\n## 1. Date Utility\nAs a team, I want dates checked.\n\n"
                   "### Requirements\n\nREQ-F-001: [Ubiquitous] The system shall check dates.\n")
    return buffer.getvalue()


class RetrieveAndReportTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = new_run("demo", {"REFRAME_HOME": self.tmp.name})
        self.folder.update(project="demo")
        self.folder.save("decisions.json", [{"at": "t", "question": "how would you like to proceed?", "answer": "2. Assess and reimagine.", "reason": "r"}])
        root = "transform-output/job-1/"
        objects = {root + "spec_gen/spec_gen_specs_1.zip": b"old", root + "spec_gen/spec_gen_specs_2.zip": spec_zip(),
                   root + "results/classification_1.json": json.dumps([{"path": "a.cbl", "fileType": "COBOL"}]).encode(),
                   root + "results/codebase_issues_1.json": json.dumps([{"item": {"severity": "ERROR", "name": "Missing copybook"}}]).encode(),
                   "transform-output/neptune-quads/job-1/x.nq": b"graph", root + "business-functions/Internal-DO-NOT-TOUCH/s.msgpack": b"x"}
        self.objects = objects
        fake = FakeRunner().add(["aws", "s3api", "list-objects-v2"], 0, {"Contents": [{"Key": k, "Size": len(v)} for k, v in objects.items()
                                                                                    if k.startswith(root)]})

        def get(argv, env, data):
            key = argv[argv.index("--key") + 1]
            Path(argv[argv.index("--expected-bucket-owner") + 2]).write_bytes(objects[key])
            return Result(0, "{}", "")
        fake.script.append((("aws", "s3api", "get-object"), get))
        self.fake = fake

    def tearDown(self):
        self.tmp.cleanup()

    def test_retrieve_then_report(self):
        summary = retrieve.retrieve(Aws("p", "us-east-1", self.fake), self.folder, Bucket("b", "000000000000"), "job-1")
        downloaded = [argv[argv.index("--key") + 1] for argv in self.fake.ran("aws", "s3api", "get-object")]
        self.assertNotIn("transform-output/job-1/spec_gen/spec_gen_specs_1.zip", downloaded)
        self.assertFalse(any("Internal-DO-NOT-TOUCH" in k or "neptune-quads" in k for k in downloaded))
        self.assertEqual(summary["totals"]["by_type"], {"REQ-F": 3, "REQ-N": 1})  # two functions
        self.assertEqual(summary["totals"]["captured_rules"], 2)
        self.assertEqual(summary["totals"]["open_questions"], 2)
        catalog = self.folder.path("outputs/catalog")
        catalog.mkdir(parents=True, exist_ok=True)
        (catalog / "business_domains.json").write_text(json.dumps({"domains": [{"name": "Payments", "description": "Take and post payments."}]}))
        (catalog / "business_function.csv").write_text("bf_name,bf_id,bf_description,bd_id,bd_name,bd_description\n"
                                                       "Card Payments,BF-1,Records card payments.,BD-1,Payments,Take and post payments.\n")
        page = build.build(self.folder).read_text()
        data = json.loads(page.split('<script id="data" type="application/json">')[1].split("</script>")[0].replace("<\\/", "</"))
        self.assertEqual([(d["name"], d["kind"]) for d in data["domains"]], [("Payments", "business"), ("Programs not in a business function", "unassigned")])
        function = data["functions"][0]
        self.assertEqual((function["name"], function["description"]), ("Card Payments", "Records card payments."))
        self.assertEqual([n["heading"] for n in function["notes"]], ["Global Preconditions", "Generation Notes"])
        capability = data["capabilities"][0]
        self.assertEqual(capability["story"], "As a payments clerk, I want each payment recorded so that the account balance is right.")
        self.assertEqual(capability["fields"], {"Restart/Recovery": "A failed run leaves no partial output."})
        self.assertEqual([r["code"] for r in data["requirements"][:3]], ["REQ-F-001", "REQ-F-002", "REQ-N-001"])
        first = data["requirements"][0]
        self.assertEqual((first["key"], first["programs"], first["rules"]), ("Payments/CardPayments/REQ-F-001", ["PAY01C"], ["Payments/CardPayments/r1"]))
        self.assertEqual(data["rules"][0]["requirements"], ["REQ-F-001"])
        questions = [(q["code"], q["owner"], q["unverified"]) for q in data["questions"]]
        self.assertEqual(questions, [("OQ-001", "payments business owner", False), ("OQ-002", "", True)])
        self.assertEqual(data["questions"][0]["text"], "Is a negative amount ever valid?")
        self.assertIn("<table>", data["data_model"])
        self.assertEqual(data["classification"], [["COBOL", 1]])
        self.assertIn("Business review: demo", page)
        self.assertNotIn("http://", page.replace("http://www.w3.org", ""))  # nothing loaded from the network
        self.assertNotIn("https://", page)

    def test_markdown_escapes_html(self):
        self.assertNotIn("<script>", build.render_markdown("# T\n\n<script>alert(1)</script>"))



class PageScriptTest(unittest.TestCase):
    def test_the_pages_scripts_parse(self):
        import re
        import shutil
        import subprocess
        node = shutil.which("node")
        if not node:
            self.skipTest("node is not installed")
        from reframe.report import compare
        for name, page in (("template.html", build.TEMPLATE), ("compare.html", compare.TEMPLATE)):
            for n, script in enumerate(re.findall(r"<script>\n(.*?)</script>", page, re.S)):
                with tempfile.NamedTemporaryFile("w", suffix=".js") as f:
                    f.write(script)
                    f.flush()
                    checked = subprocess.run([node, "--check", f.name], capture_output=True, text=True)
                self.assertEqual(checked.returncode, 0, f"{name} script {n}: {checked.stderr[-500:]}")


if __name__ == "__main__":
    unittest.main()
