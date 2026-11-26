"""P4-11: golden datasets (docs/pipeline-4.md, section 4 D10). No model.

Per capability, the cases the new system must answer as the legacy one does: one for each worked example of its rules,
and one for each row of its decision tables. Each case names its rule and the legacy source, the input and the expected
output, whether it is an edge case, what it is run against, and how each value is compared (golden_compare.py).

Until P4-13 captures real outputs from the legacy programs, the expected outputs come from the rules, and every dataset
says so: equivalence is asserted from the rules, not proven against the running legacy system.
"""

from __future__ import annotations

import re
from typing import Any

FROM_RULES = "the rules"  # until P4-13: "legacy outputs"
NOTE = ("The expected outputs come from the reconciled rules and their worked examples, not from running the legacy programs: "
        "equivalence is asserted from the rules, not proven against the legacy system (P4-13 may capture real outputs).")

# A field's kind, from words in its name; the first that matches wins. Money, dates, status codes, IDs and counts are
# compared exactly by value; text is compared as written, with case and spacing set apart as formatting.
NAME_KINDS = (
    ("text", r"\b(name|names|description|message|address|text|label|title|comment)\b"),
    ("date", r"\b(date|dt|day|time|timestamp|ts|year|month|expiry|expiration)\b"),
    ("money", r"\b(amount|amt|balance|bal|limit|fee|fees|interest|price|payment|credit|debit|charge|cash|cost|apr|rate)\b"),
    ("count", r"\b(count|cnt|quantity|qty|records|attempts|lines|times|total)\b|\bnumber of\b"),
    ("status", r"\b(status|code|cd|flag|indicator|ind|type|result|return|response|resp|option|aid|key|keys|pf\d+|mode|action|reason|state|decision)\b"),
    ("id", r"\b(id|number|num|no|account|acct|card|customer|cust|transaction|tran|user|merchant|ssn|phone|zip)\b"),
)
EDGE_WORDS = re.compile(r"\berror|invalid|not found|reject|abend|fail|denied|exceed|cannot|missing|blank|empty|over the|too (many|long|short)|"
                        r"must be|not (valid|allowed|numeric)|declin", re.I)
# a quote opens after a space or punctuation and closes before one, so "card 4111's transaction" holds no quote
QUOTED = re.compile(r"(?<![A-Za-z0-9])'([^'\n]{1,120}?)'(?![A-Za-z0-9])|(?<![A-Za-z0-9])\"([^\"\n]{1,120}?)\"(?![A-Za-z0-9])")


def kind_of(field: str, value: str = "") -> str:
    name = field.replace("_", " ").replace("-", " ").lower()
    for kind, pattern in NAME_KINDS:
        if re.search(pattern, name):
            return kind
    v = str(value).strip()
    if re.fullmatch(r"[+-]?\d{1,13}\.\d{2}[-]?", v):
        return "money"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return "date"
    return "text"


def literals(text: str) -> list[str]:
    """The messages and codes an outcome quotes, which the new system must show word for word."""
    found = [a or b for a, b in QUOTED.findall(text or "")]
    return list(dict.fromkeys(f for f in found if f.strip()))


def target(s: dict[str, Any], rule: dict[str, Any] | None) -> dict[str, Any]:
    """What a case is run against: the modern screens whose components cite the rule (online), else every screen of the
    capability; the legacy program's job (a scheduled job); or the capability's service."""
    runs = s["runs_as"]
    if "online" in runs and s["screens"]:
        key = rule["key"] if rule else None
        citing = [x["id"] for x in s["screens"] if key and any(key in (c.get("rules") or []) for c in x["components"])]
        return {"kind": "screen", "names": citing or [x["id"] for x in s["screens"]], "runs_as": runs}
    if "scheduled job" in runs:
        return {"kind": "job", "names": [rule["program"]] if rule and rule.get("program") else [], "runs_as": runs}
    return {"kind": "service", "names": [s["id"]], "runs_as": runs}


def _fields(pairs: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"field": f, "value": str(v), "kind": kind_of(f, str(v))} for f, v in pairs]


def dataset(s: dict[str, Any]) -> dict[str, Any]:
    """The golden dataset of one labelled specification (package.label): its cases and the gaps no case covers."""
    rules = {r["key"]: r for r in s["rules"]}
    by_example = {(k, x.get("from")): s["ac_ids"][x["id"]] for x in s["acceptance"] for k in x.get("rules") or []}
    cases: list[dict[str, Any]] = []

    def add(rule: dict[str, Any], source: str, given: list[tuple[str, str]], outcome: str, criteria: list[str], edge: bool) -> None:
        cases.append({"id": f"{s['id']}-GD-{len(cases) + 1:02d}", "capability": s["id"], "rule": s["rule_ids"].get(rule["key"], rule["key"]),
                      "rule_class": rule.get("class", ""), "from": source, "program": rule.get("program", ""), "source": list(rule.get("evidence") or []),
                      "input": _fields(given), "expected": {"outcome": outcome, "literals": literals(outcome), "values": []},
                      "edge": edge, "target": target(s, rule), "criteria": criteria,
                      "compare": {"literals": "word for word; case or spacing alone is formatting",
                                  "values": "exact by value for money, dates, status codes, IDs and counts; layout alone is formatting",
                                  "tolerance": "none"}})

    for r in s["rules"]:
        if r.get("class") == "design note":
            continue  # a technical step is built from its design note, not checked as behaviour
        for n, e in enumerate(r.get("examples") or [], 1):
            given = [(g["field"], g["value"]) for g in e.get("given") or []]
            edge = r.get("kind") in ("validation", "error_handling") or bool(EDGE_WORDS.search(e.get("then", "")))
            add(r, f"worked example {n} of {s['rule_ids'].get(r['key'], r['key'])}", given, e.get("then", ""),
                [by_example[k] for k in [(r["key"], f"worked example {n} of the rule")] if k in by_example], edge)
    uncovered: list[dict[str, Any]] = []
    for t, table in enumerate(s.get("tables") or [], 1):
        for i, row in enumerate(table.get("rows") or [], 1):
            rule = rules.get(row.get("rule")) or {"key": row.get("rule", ""), "class": "business rule", "program": "", "evidence": []}
            given = list(zip(table.get("conditions") or [], row.get("values") or []))
            outcome = row.get("outcome", "")
            add(rule, f"decision table {t}, row {i}", given, outcome, [], bool(EDGE_WORDS.search(outcome)))
        for gap in table.get("gaps") or []:
            uncovered.append({"table": t, "input": _fields(list(zip(table.get("conditions") or [], gap.get("values") or []))), "note": gap.get("note", "")})
    return {"dataset": f"{s['id']}-GD", "capability": s["id"], "title": s["title"], "status": s["status"], "runs_as": s["runs_as"],
            "expected_from": FROM_RULES, "note": NOTE, "cases": cases, "uncovered": uncovered,
            "counts": {"cases": len(cases), "edge": sum(1 for c in cases if c["edge"]), "from_examples": sum(1 for c in cases if c["from"].startswith("worked")),
                       "from_tables": sum(1 for c in cases if c["from"].startswith("decision")), "uncovered": len(uncovered)}}


def readme(datasets: list[dict[str, Any]]) -> str:
    total = sum(d["counts"]["cases"] for d in datasets)
    lines = ["# Golden datasets", "",
             "One dataset per capability: the cases the new system must answer as the legacy one does. Each case comes from a worked example "
             "of a rule or a row of a decision table, and names its rule (`<CODE>-BR-<n>`), the legacy source lines and the acceptance criteria it backs.", "",
             f"**{NOTE}**", "",
             "## A case", "",
             "| Field | What it holds |", "|---|---|",
             "| `id` | `<capability>-GD-<n>`, kept with the capability's other IDs |",
             "| `rule`, `from`, `source`, `program` | The rule it covers, the example or table row it comes from, and the legacy lines behind it |",
             "| `input` | Each input field and value, with its kind: money, date, status, id, count or text |",
             "| `expected` | The outcome in words, the messages and codes it quotes (`literals`), and any values to compare |",
             "| `edge` | True for the failing or exceptional path: a validation or error-handling rule, or an outcome that rejects, fails or abends |",
             "| `target` | What it is run against: a modern screen by its ID, the scheduled job that replaces a legacy program, or the capability's service |",
             "| `criteria` | The acceptance criteria the case backs |", "",
             "`uncovered` lists the input combinations a decision table leaves to no rule: each is a question for the owner, not a case.", "",
             "## Running them", "",
             "Run each case's input through the target on your stack, record what the system answered by case ID, then compare:", "",
             "```bash", "python golden/compare.py golden/<capability>.json actual.json --report report.json", "```", "",
             "`actual.json` maps each case ID to `{\"text\": \"<what the system showed>\", \"values\": {\"<field>\": \"<value>\"}}`. "
             "A quoted message must appear word for word, and money, dates, status codes, IDs and counts must have the same value. "
             "A difference only in how something is written (padding, case, spacing, an amount's or a date's layout) is reported as *formatting*, "
             "apart from a *business* difference. `compare.py` uses the Python standard library only; port it if your tests run elsewhere.", "",
             f"## The datasets ({len(datasets)}, {total} cases)", "",
             "| Capability | Status | Cases | Edge cases | Uncovered |", "|---|---|---|---|---|"]
    lines += [f"| [{d['capability']}]({d['capability']}.json) {d['title']} | {d['status']} | {d['counts']['cases']} | {d['counts']['edge']} | "
              f"{d['counts']['uncovered']} |" for d in datasets]
    return "\n".join(lines) + "\n"
