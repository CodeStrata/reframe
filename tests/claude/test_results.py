import json
import tempfile
import unittest
from pathlib import Path

from reframe.claude import graph, requirements, retrieve

RULES = """# Business rules: demo

| ID | Name | Category | Priority | Source | Confidence |
|---|---|---|---|---|---|
| RULE-001 | Credit limit check | Validation | P0 | `app/cbl/PROG1.cbl:120-140` | High |

## Validation

### RULE-001: Credit limit check
**Category:** Validation
**Priority:** P0
**Source:** `app/cbl/PROG1.cbl:120-140`
**Plain English:** A purchase over the credit limit is declined.
**Specification:**
  Given an account with a credit limit
  When a purchase would take the balance over the limit
  Then the purchase is declined
**Parameters:** none
**Edge cases handled:** zero limit
**Confidence:** High — the code is direct

### RULE-002: Interest rounding
**Category:** Calculation
**Priority:** P1
**Source:** `app/cbl/PROG2.cbl:44`
**Plain English:** Interest is rounded to cents.
**Specification:**
  Given a monthly interest amount
  When it is posted
  Then it is rounded half up to two decimals
**Suspected defect:** rounds negative amounts toward zero
**Confidence:** Medium — which rounding mode? Ask the finance SME

## Rules requiring SME confirmation

| Rule | Question |
|---|---|
| RULE-002 | Which rounding mode does finance expect for negative interest? |
"""

RULES_WITH_BULLETS = RULES.split("## Rules requiring SME confirmation")[0] + """## Rules requiring SME confirmation

- **RULE-002** (Medium): Which rounding mode does finance expect for negative interest?
"""

TOPOLOGY = {"system": "demo", "root": {"id": "sys", "kind": "system", "children": [
    {"id": "dom:card", "name": "Cards", "kind": "domain", "children": [
        {"id": "PROG1", "name": "PROG1", "kind": "module", "language": "cobol", "loc": 300, "file": "app/cbl/PROG1.cbl"},
        {"id": "JOB1", "name": "JOB1", "kind": "job"}]},
    {"id": "dom:data", "name": "Data stores", "kind": "domain", "children": [{"id": "ds:ACCT", "name": "ACCT", "kind": "datastore"}]}]},
    "edges": [{"source": "PROG1", "target": "ds:ACCT", "kind": "read"}], "entryPoints": ["PROG1"],
    "flows": [{"name": "Buy", "persona": "Cardholder", "description": "A purchase", "steps": [{"label": "Check limit", "nodes": ["PROG1"]}]}]}


class RetrieveTest(unittest.TestCase):
    def test_rule_cards(self):
        cards = retrieve.parse_rules(RULES)
        self.assertEqual([c["id"] for c in cards], ["RULE-001", "RULE-002"])
        first, second = cards
        self.assertEqual((first["priority"], first["category"], first["program"], first["path"], first["line"], first["line_end"]),
                         ("P0", "Validation", "PROG1", "app/cbl/PROG1.cbl", 120, 140))
        self.assertEqual([s["clause"] for s in first["spec"]], ["Given", "When", "Then"])
        self.assertEqual((second["confidence"], second["defect"]), ("Medium", "rounds negative amounts toward zero"))
        questions = retrieve.sme_questions(RULES, cards)
        self.assertEqual([q["rule"] for q in questions], ["RULE-002"])
        self.assertIn("rounding mode", questions[0]["text"])
        bullets = retrieve.sme_questions(RULES_WITH_BULLETS, cards)
        self.assertEqual((bullets[0]["text"], bullets[0]["confidence"]), ("Which rounding mode does finance expect for negative interest?", "Medium"))

    def test_data_objects_at_either_heading_level(self):
        two = "# Data Objects\n\n## ACCOUNT-RECORD (Account master)\nfields\n\n## CARD-RECORD\nfields\n"
        self.assertEqual([s["title"] for s in retrieve.data_objects(two)], ["ACCOUNT-RECORD (Account master)", "CARD-RECORD"])
        three = "# Data Objects\n\n## Records\n\n### A\nx\n### B\ny\n### C\nz\n"
        self.assertEqual(len(retrieve.data_objects(three)), 3)

    def test_topology(self):
        out = {"domains": [], "modules": [], "jobs": [], "screens": [], "datastores": []}
        retrieve.walk(TOPOLOGY["root"], None, out)
        self.assertEqual([d["id"] for d in out["domains"]], ["dom:card", "dom:data"])
        self.assertEqual((out["modules"][0]["domain"], out["jobs"][0]["name"], out["datastores"][0]["domain"]), ("dom:card", "JOB1", "dom:data"))


class RequirementsTest(unittest.TestCase):
    def test_citations_are_checked_and_codes_numbered(self):
        raw = {"functions": [{"name": "Authorize", "description": "d", "capabilities": [{"title": "Check", "story": "As a ...", "requirements": [
            {"kind": "functional", "pattern": "event-driven", "text": "When ..., the system shall decline.", "rules": ["RULE-001"]},
            {"kind": "functional", "pattern": "ubiquitous", "text": "Made up.", "rules": ["RULE-999"]},
            {"kind": "non-functional", "pattern": "ubiquitous", "text": "Cites a line.", "rules": [], "sources": ["app/cbl/PROG1.cbl:2"]},
            {"kind": "functional", "pattern": "ubiquitous", "text": "Bad line.", "rules": [], "sources": ["app/cbl/PROG1.cbl:999"]}],
            "questions": [{"text": "Which mode?", "owner": "Finance", "rule": "RULE-002"}]}]}]}
        functions, dropped = requirements.check(raw, {"RULE-001", "RULE-002"}, {"app/cbl/PROG1.cbl": 300})
        self.assertEqual(dropped, 2)
        domains = [{"key": "card", "name": "Cards", "functions": functions}]
        requirements.number(domains)
        reqs = domains[0]["functions"][0]["capabilities"][0]["requirements"]
        self.assertEqual([r["code"] for r in reqs], ["REQ-F-001", "REQ-N-001"])
        self.assertEqual(reqs[0]["key"], "claude/card/01/REQ-F-001")
        self.assertEqual(domains[0]["functions"][0]["capabilities"][0]["questions"][0]["code"], "OQ-001")

    def test_domain_input_holds_only_the_plugins_results(self):
        model = {"modules": [{"name": "PROG1", "domain": "dom:card"}], "rules": retrieve.parse_rules(RULES),
                 "flows": TOPOLOGY["flows"], "sme_questions": [{"rule": "RULE-001", "text": "q"}]}
        for card in model["rules"]:
            card["domain"] = "dom:card" if card["program"] == "PROG1" else ""
        data = requirements.domain_input(model, {"id": "dom:card", "name": "Cards", "members": ["PROG1"]})
        self.assertEqual([r["id"] for r in data["rules"]], ["RULE-001"])
        self.assertEqual(len(data["flows"]), 1)
        self.assertNotIn("aws", json.dumps(data).casefold())


class GraphTest(unittest.TestCase):
    def test_n_quads_in_claudes_own_graph(self):
        model = {"domains": [{"id": "dom:card", "name": "Cards"}], "modules": [{"id": "PROG1", "name": "PROG1", "domain": "dom:card", "loc": 3}],
                 "jobs": [], "screens": [], "datastores": [{"id": "ds:ACCT", "name": "ACCT", "domain": "dom:data"}],
                 "edges": [{"source": "PROG1", "target": "ds:ACCT", "kind": "read"}], "entry_points": ["PROG1"], "flows": TOPOLOGY["flows"],
                 "rules": retrieve.parse_rules(RULES), "sme_questions": [{"rule": "RULE-002", "text": 'He said "half up"\nthen left'}]}
        q = graph.build("abc123", "f" * 64, model, None, {"version": "1.1.0", "commit": "c"})
        text = q.text()
        self.assertTrue(all(line.endswith("<urn:reframe:graph:claude:abc123> .") for line in text.splitlines()))
        self.assertIn('"He said \\"half up\\"\\nthen left"', text)
        self.assertIn("<urn:reframe:claude:abc123:rule:RULE-001> <urn:reframe:claude:ontology:citesModule> <urn:reframe:claude:abc123:module:PROG1>", text)
        self.assertIn("<urn:reframe:claude:ontology:reads>", text)
        self.assertIn('"' + "f" * 64 + '"', text)

    def test_loader_package_holds_the_handler(self):
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            path = graph.package(Path(tmp) / "loader.zip")
            with zipfile.ZipFile(path) as z:
                self.assertEqual(z.namelist(), ["handler.py"])
                self.assertIn(b"neptune-db", z.read("handler.py"))


class LoaderTest(unittest.TestCase):
    def test_calls_name_the_endpoint_and_read_the_reply(self):
        class Aws:
            def __init__(self):
                self.calls = []

            def read(self, *args, **kw):
                self.calls.append(args)
                if args[0] == "neptune":
                    return {"DBClusters": [{"Endpoint": "demo.cluster-x.us-east-1.neptune.amazonaws.com"}]}
                Path(args[-1]).write_text(json.dumps({"status": 200, "body": {"results": {"bindings": [{"t": {"value": "urn:reframe:claude:ontology:Module"}, "n": {"value": "3"}}]}}}))
                return {"StatusCode": 200}

            write = read
        with tempfile.TemporaryDirectory() as tmp:
            aws = Aws()
            loader = graph.Loader(aws, "fn", "arn:cluster", Path(tmp))
            self.assertEqual(graph.counts(loader, "abc123"), {"Module": 3})
            payload = json.loads(aws.calls[1][aws.calls[1].index("--payload") + 1])
            self.assertEqual(payload["endpoint"], "demo.cluster-x.us-east-1.neptune.amazonaws.com")
            self.assertIn("urn:reframe:graph:claude:abc123", payload["query"])


class NetworkTest(unittest.TestCase):
    def test_waits_until_the_loaders_interfaces_are_released(self):
        from reframe.infrastructure import network
        replies = [{"NetworkInterfaces": [{"Status": "in-use"}]}, {"NetworkInterfaces": [{"Status": "available"}]}, {"NetworkInterfaces": []}]

        class Aws:
            def read(self, *args, **kw):
                self.args = args
                return replies.pop(0)
        clock = iter(range(0, 1000, 30))
        aws = Aws()
        waited = network.wait_for_lambda_interfaces(aws, "vpc-1", "reframe-x-kgload", sleep=lambda s: None, clock=lambda: next(clock))
        self.assertEqual(waited, 90)
        self.assertIn("Name=description,Values=AWS Lambda VPC ENI-reframe-x-kgload*", aws.args)


if __name__ == "__main__":
    unittest.main()


class CommandTest(unittest.TestCase):
    def setUp(self):
        import os
        from unittest import mock
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_claude_and_compare_parse(self):
        from reframe.core import cli
        args = cli.parser().parse_args(["claude", "--run", "abc123", "--auth", "bedrock", "--max-agents", "700", "--graph-load", "yes"])
        self.assertEqual((args.command, args.run, args.auth, args.max_agents, args.graph_load), ("claude", "abc123", "bedrock", 700, "yes"))
        self.assertTrue(cli.parser().parse_args(["compare", "--open"]).open)

    def test_claude_waits_for_pipeline_1(self):
        import contextlib
        import io
        from reframe.core import cli
        from reframe.core.runfolder import new_run
        folder = new_run("demo")
        folder.update(project="demo", profile="p", region="us-east-1", mode="autonomous", status="RUNNING", stage="job")
        with contextlib.redirect_stderr(io.StringIO()) as err, contextlib.redirect_stdout(io.StringIO()):
            code = cli.main(["claude"])
        self.assertNotEqual(code, 0)
        self.assertIn("no AWS resources yet", err.getvalue())
        claude = folder.state["claude"]
        self.assertEqual((claude["auth"], claude["max_agents"], claude["mode"]), ("subscription", 600, "autonomous"))

    def test_a_pipeline_2_question_is_answered_by_number_or_text(self):
        import contextlib
        import io
        from reframe.core import cli
        from reframe.core.runfolder import new_run
        folder = new_run("demo")
        folder.save("claude-question.json", {"id": "claude-estimate", "kind": "claude", "text": "Run 37 shards?", "options": ["Run it", "Cancel"], "asked_at": "t"})
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cli.main(["answer"]), 0)
        self.assertIn("Run 37 shards?", out.getvalue())
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(["answer", "--text", "free"]), 2)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["answer", "1"]), 0)
        self.assertEqual(folder.load("claude-answer.json")["text"], "Run it")
        folder.save("claude-question.json", {"id": "claude-preflight-3", "kind": "claude", "text": "Bespoke build?", "options": ["Reframe's answer: Don't know"], "asked_at": "t"})
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["answer", "1"]), 0)
        self.assertEqual(folder.load("claude-answer.json")["text"], "Don't know")


class InstallTest(unittest.TestCase):
    def test_a_refresh_leaves_providers_and_state_alone(self):
        import os
        import stat
        from unittest import mock
        from reframe.core.runfolder import new_run
        from reframe.infrastructure.terraform_runner import Terraform
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"REFRAME_HOME": tmp}):
            folder = new_run("demo")
            tf = Terraform(folder, aws=None, binary="terraform")
            tf.install()
            provider = folder.path("terraform/project/.terraform/providers/x/terraform-provider-aws")
            provider.parent.mkdir(parents=True)
            provider.write_text("binary")
            provider.chmod(0o755)
            state = folder.path("terraform/bootstrap/terraform.tfstate")
            state.write_text("{}")
            tf.install(refresh=True)
            self.assertTrue(provider.stat().st_mode & stat.S_IXUSR)
            self.assertEqual(state.read_text(), "{}")
            self.assertTrue(folder.path("terraform/modules/graph_loader/main.tf").exists())
