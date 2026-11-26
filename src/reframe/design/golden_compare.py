"""Compare a new system's answers with a golden dataset (docs/pipeline-4.md, section 4 D10, P4-11).

This file is copied as it is into the package (golden/compare.py), so it uses the Python standard library only and
imports nothing from Reframe. Run it on the stack you build with, or port it.

    python compare.py golden/<capability>.json actual.json [--report report.json]

actual.json holds what the new system answered for each case, by case ID:

    {"OATM-C16-GD-01": {"text": "the message or output the system showed", "values": {"<field>": "<value>"}}}

Each expected value is compared by its kind. Money, dates, status codes, IDs and counts are compared exactly by value;
a difference only in how the value is written (padding, case, an edited amount's layout, a date's layout) is reported
as formatting, apart from a difference in business behaviour. A message the rule quotes must appear word for word: the
same words in another case or spacing is formatting, and missing words are business.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from typing import Any

MATCH, FORMATTING, BUSINESS, MISSING = "match", "formatting", "business", "missing"
KINDS = ("money", "date", "status", "id", "count", "text")


def _money(text: str) -> Decimal | None:
    """An amount however the legacy system or the new one writes it: '+00000125.50', '125.50-', '$1,250.00', '(12.00)'."""
    t = text.strip().replace(",", "").replace("$", "").replace(" ", "")
    negative = t.endswith("-") or t.endswith("CR") or (t.startswith("(") and t.endswith(")"))
    t = t.rstrip("-").removesuffix("CR").removesuffix("DB").strip("()").lstrip("+")
    if t.startswith("-"):
        negative, t = True, t[1:]
    if not re.fullmatch(r"\d+(\.\d+)?|\.\d+", t):
        return None
    try:
        value = Decimal(t)
    except InvalidOperation:
        return None
    return -value if negative else value


DATE_LAYOUTS = ("%Y-%m-%d", "%Y%m%d", "%m/%d/%Y", "%d.%m.%Y", "%Y/%m/%d", "%m-%d-%Y", "%m/%d/%y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d-%H.%M.%S.%f", "%Y-%m-%d %H:%M:%S.%f")


def _date(text: str) -> datetime.datetime | None:
    t = text.strip().removesuffix("Z")
    for layout in DATE_LAYOUTS:
        try:
            return datetime.datetime.strptime(t, layout)
        except ValueError:
            continue
    return None


def _plain(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def compare_value(expected: Any, actual: Any, kind: str) -> str:
    """match, formatting (the same value written differently) or business (a different value)."""
    if actual is None:
        return MISSING
    e, a = str(expected), str(actual)
    if e == a:
        return MATCH
    if kind == "money":
        ev, av = _money(e), _money(a)
        if ev is not None and av is not None:
            return FORMATTING if ev == av else BUSINESS
    elif kind == "date":
        ed, ad = _date(e), _date(a)
        if ed is not None and ad is not None:
            return FORMATTING if ed == ad else BUSINESS
    elif kind in ("id", "count"):
        es, as_ = e.strip(), a.strip()
        if es.isdigit() and as_.isdigit():
            return FORMATTING if int(es) == int(as_) else BUSINESS
        return FORMATTING if es.lstrip("0").casefold() == as_.lstrip("0").casefold() else BUSINESS
    return FORMATTING if _plain(e) == _plain(a) else BUSINESS


def compare_literal(literal: str, text: str | None) -> str:
    """A message or code the rule quotes, looked for in what the system showed."""
    if text is None:
        return MISSING
    if literal in text:
        return MATCH
    return FORMATTING if _plain(literal) in _plain(text) else BUSINESS


def compare_case(case: dict[str, Any], actual: dict[str, Any] | None) -> dict[str, Any]:
    if actual is None:
        return {"case": case["id"], "result": MISSING, "checks": []}
    checks: list[dict[str, Any]] = []
    text = actual.get("text")
    if text is None and actual.get("values"):
        text = " ".join(str(v) for v in actual["values"].values())
    for literal in case["expected"].get("literals") or []:
        checks.append({"what": f"the message or code {literal!r}", "result": compare_literal(literal, text)})
    values = actual.get("values") or {}
    for v in case["expected"].get("values") or []:
        checks.append({"what": f"{v['field']} ({v['kind']})", "expected": v["value"], "actual": values.get(v["field"]),
                       "result": compare_value(v["value"], values.get(v["field"]), v["kind"])})
    if not checks:  # nothing machine-checkable: the outcome is for the test's author to assert
        return {"case": case["id"], "result": "unchecked", "checks": [], "outcome": case["expected"]["outcome"]}
    order = (BUSINESS, MISSING, FORMATTING, MATCH)
    worst = min((c["result"] for c in checks), key=order.index)
    return {"case": case["id"], "result": worst, "checks": checks}


def compare(dataset: dict[str, Any], actuals: dict[str, Any]) -> dict[str, Any]:
    results = [compare_case(c, actuals.get(c["id"])) for c in dataset["cases"]]
    counts = {k: sum(1 for r in results if r["result"] == k) for k in (MATCH, FORMATTING, BUSINESS, MISSING, "unchecked")}
    return {"dataset": dataset["dataset"], "capability": dataset["capability"], "expected_from": dataset["expected_from"],
            "counts": counts, "equivalent": counts[BUSINESS] == 0 and counts[MISSING] == 0, "results": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare a new system's answers with a golden dataset")
    parser.add_argument("dataset")
    parser.add_argument("actual")
    parser.add_argument("--report", help="write the full report here as JSON")
    args = parser.parse_args(argv)
    with open(args.dataset) as f:
        dataset = json.load(f)
    with open(args.actual) as f:
        actuals = json.load(f)
    report = compare(dataset, actuals)
    if args.report:
        with open(args.report, "w") as f:
            json.dump(report, f, indent=1)
    c = report["counts"]
    print(f"{dataset['capability']}: {c[MATCH]} match, {c[FORMATTING]} formatting only, {c[BUSINESS]} business differences, "
          f"{c[MISSING]} not answered, {c['unchecked']} for the test to assert")
    for r in report["results"]:
        if r["result"] in (BUSINESS, MISSING):
            print(f"  {r['case']}: {r['result']}" + "".join(f"; {x['what']}: {x['result']}" for x in r["checks"] if x["result"] != MATCH))
    if dataset["expected_from"] != "legacy outputs":
        print("The expected outputs come from the rules: equivalence is asserted from the rules, not proven against the legacy system.")
    return 0 if report["equivalent"] else 1


if __name__ == "__main__":
    sys.exit(main())
