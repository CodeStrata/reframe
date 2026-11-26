"""Pipeline 4, stage D6: data contracts from the copybooks (docs/pipeline-4.md, section 4, P4-07).

Read from the source with no model. Every copybook a program copies (COPY, or EXEC SQL INCLUDE) becomes a contract:
its records, each field with its level, the group it sits in, its PIC and USAGE, and a neutral type:

- `PIC X(n)` or `A(n)` is text of n characters;
- `PIC 9(n)` is an unsigned integer of n digits, `S9(n)` a signed one;
- `PIC S9(7)V99` is a signed decimal with 7 integer and 2 fraction digits; COMP-3 stores it packed, COMP in binary;
- an edited PIC (`Z`, `$`, `,`, `.`, `-`, `CR`) is formatted text, a display of a number;
- OCCURS, REDEFINES and the 88-level condition names (their values) are kept.

The screen copybooks (`cpy-bms`) are screens, read in stage D1, not contracts.

The target stack's types are added from a table when the engineer has given the stack (`--stack "<front end>; <back
end>; <data>"`): the back end's language gives the code type, the data store the column type. Reframe never guesses a
stack; without one, or for a language or store the table does not know, the neutral types stand, and the contract says so.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from reframe.design.flow import NAME, data_items
from reframe.design.inventory import code_only

STORAGE = {"COMP-3": "packed decimal", "COMPUTATIONAL-3": "packed decimal", "PACKED-DECIMAL": "packed decimal", "COMP": "binary", "COMP-4": "binary",
           "COMPUTATIONAL": "binary", "COMPUTATIONAL-4": "binary", "BINARY": "binary", "COMP-5": "native binary", "COMPUTATIONAL-5": "native binary",
           "COMP-1": "single float", "COMPUTATIONAL-1": "single float", "COMP-2": "double float", "COMPUTATIONAL-2": "double float"}


# ---- copybooks ---------------------------------------------------------------------------------------------------------

def copybooks(legacy: Path) -> dict[str, Path]:
    """Data copybooks by name: every .cpy file wherever it is (GenApp keeps them beside the programs), and the files
    without an extension in cpy folders. The screen copybooks are left out: those in a cpy-bms folder, and those named
    after a BMS mapset in the snapshot."""
    files = sorted(p for p in legacy.rglob("*") if p.is_file())
    maps = {p.stem.upper() for p in files if p.suffix.lower() == ".bms"}
    found: dict[str, Path] = {}
    for p in files:
        folder = p.parent.name.lower()
        if "bms" in folder or p.stem.upper() in maps:
            continue
        if p.suffix.lower() == ".cpy" or (p.suffix == "" and folder.startswith("cpy")):
            found.setdefault(p.stem.upper(), p)
    return found


def programs(legacy: Path) -> dict[str, Path]:
    return {p.stem.upper(): p for p in sorted(legacy.rglob("*")) if p.is_file() and p.suffix.lower() in (".cbl", ".cob")}


def copied(text: str) -> list[str]:
    """The copybooks a source copies, in order, once each: COPY name and EXEC SQL INCLUDE name."""
    code = code_only(text)
    found = re.findall(rf"\bCOPY\s+['\"]?({NAME})['\"]?", code, re.I) + re.findall(rf"\bINCLUDE\s+({NAME})\b", code, re.I)
    return list(dict.fromkeys(n.upper() for n in found if n.upper() not in ("SQLCA", "SQLDA")))


def _record_names(path: Path) -> list[str]:
    items = [i for i in data_items(path.read_text(errors="replace"), path.name) if i.level not in (66, 77, 88)]
    top = min((i.level for i in items), default=1)
    return [i.name for i in items if i.level == top and i.name != "FILLER"]


def role(text: str, book: str, names: list[str]) -> str:
    """"file record" when the program copies the copybook in its FILE SECTION, or reads into, writes or rewrites one of
    its records (EXEC CICS READ ... INTO, READ ... INTO, WRITE, REWRITE, FROM); otherwise "working storage"."""
    code = code_only(text)
    section = re.search(r"\bFILE\s+SECTION\b(.*?)\bWORKING-STORAGE\s+SECTION\b", code, re.I | re.S)
    if section and re.search(rf"\bCOPY\s+['\"]?{re.escape(book)}\b", section.group(1), re.I):
        return "file record"
    for name in names:
        if re.search(rf"\b(?:INTO|FROM)\s*\(?\s*{re.escape(name)}\b|\b(?:WRITE|REWRITE)\s+{re.escape(name)}\b", code, re.I):
            return "file record"
    return "working storage"


def uses(legacy: Path) -> dict[str, dict[str, str]]:
    """For each program, the data copybooks it copies (those in the snapshot), each with its role there."""
    books = copybooks(legacy)
    names = {b: _record_names(p) for b, p in books.items()}
    found = {}
    for program, path in programs(legacy).items():
        text = path.read_text(errors="replace")
        found[program] = {b: role(text, b, names[b]) for b in copied(text) if b in books}
    return found


# ---- types -------------------------------------------------------------------------------------------------------------

def _expand(pic: str) -> str:
    return re.sub(r"(.)\((\d+)\)", lambda m: m.group(1) * int(m.group(2)), pic.upper())


def neutral(pic: str, usage: str) -> dict[str, Any]:
    """The neutral type of a PIC and USAGE: {"type": text | integer | decimal | formatted | float, "length" or "digits"
    and "scale", "signed", "storage", "bytes"}."""
    storage = STORAGE.get(usage.upper(), "")
    if not pic:
        if "float" in storage:
            return {"type": "float", "storage": storage, "bytes": 4 if storage.startswith("single") else 8}
        return {"type": "group"}
    x = _expand(pic)
    if re.fullmatch(r"[XA9]*[XA][XA9]*", x):
        return {"type": "text", "length": len(x), "storage": "characters", "bytes": len(x)}
    if re.search(r"[Z$,.*+\-B/0]|CR|DB", x.lstrip("S")) and not re.fullmatch(r"S?9*V?9*P*", x):
        digits = len(re.findall(r"[9Z*]", x))
        return {"type": "formatted", "length": len(x.replace("V", "")), "digits": digits, "storage": "characters", "bytes": len(x.replace("V", ""))}
    signed = x.startswith("S")
    body = x.lstrip("S")
    whole, _, fraction = body.partition("V")
    digits, scale = whole.count("9") + fraction.count("9"), fraction.count("9")
    storage = storage or "zoned decimal"
    size = (digits // 2 + 1) if storage == "packed decimal" else (2 if digits <= 4 else 4 if digits <= 9 else 8) if "binary" in storage else digits
    return {"type": "decimal" if scale else "integer", "digits": digits, "scale": scale, "signed": signed, "storage": storage, "bytes": size}


def _n(count: int, word: str) -> str:
    return f"{count} {word}" + ("" if count == 1 else "s")


def describe(t: dict[str, Any]) -> str:
    """A neutral type in words: "signed decimal, 7 integer and 2 fraction digits (packed decimal)"."""
    kind = t.get("type")
    if kind == "text":
        return f"text, {_n(t['length'], 'character')}"
    if kind == "formatted":
        return f"formatted text, {_n(t['length'], 'character')} (a number shown with {_n(t['digits'], 'digit')})"
    if kind in ("integer", "decimal"):
        sign = "signed" if t.get("signed") else "unsigned"
        if kind == "integer":
            return f"{sign} integer, {_n(t['digits'], 'digit')} ({t['storage']})"
        return f"{sign} decimal, {t['digits'] - t['scale']} integer and {t['scale']} fraction digits ({t['storage']})"
    if kind == "float":
        return f"floating point ({t['storage']})"
    return "group"


# The target stack's types: the back end's language for code, the data store for columns. Matched by words in the stack.
LANGUAGES = [
    (("kotlin",), {"text": "String", "int": "Int", "long": "Long", "big": "BigInteger", "decimal": "BigDecimal", "float": "Double"}),
    (("java", "spring", "quarkus", "micronaut", "jakarta"), {"text": "String", "int": "int", "long": "long", "big": "BigInteger", "decimal": "BigDecimal", "float": "double"}),
    (("c#", ".net", "dotnet", "asp.net", "csharp"), {"text": "string", "int": "int", "long": "long", "big": "decimal", "decimal": "decimal", "float": "double"}),
    (("python", "django", "fastapi", "flask"), {"text": "str", "int": "int", "long": "int", "big": "int", "decimal": "Decimal", "float": "float"}),
    (("typescript", "node", "nestjs", "express", "javascript"), {"text": "string", "int": "number", "long": "number", "big": "string (exact integer)",
                                                                 "decimal": "string (exact decimal)", "float": "number"}),
    (("go", "golang"), {"text": "string", "int": "int32", "long": "int64", "big": "string (exact integer)", "decimal": "string (exact decimal)", "float": "float64"}),
]
STORES = [
    (("postgres", "postgresql"), {"text": "VARCHAR({n})", "int": "INTEGER", "long": "BIGINT", "big": "NUMERIC({p})", "decimal": "NUMERIC({p},{s})", "float": "DOUBLE PRECISION"}),
    (("mysql", "mariadb", "aurora mysql"), {"text": "VARCHAR({n})", "int": "INT", "long": "BIGINT", "big": "DECIMAL({p})", "decimal": "DECIMAL({p},{s})", "float": "DOUBLE"}),
    (("sql server", "mssql", "azure sql"), {"text": "VARCHAR({n})", "int": "INT", "long": "BIGINT", "big": "DECIMAL({p})", "decimal": "DECIMAL({p},{s})", "float": "FLOAT"}),
    (("oracle",), {"text": "VARCHAR2({n})", "int": "NUMBER({p})", "long": "NUMBER({p})", "big": "NUMBER({p})", "decimal": "NUMBER({p},{s})", "float": "BINARY_DOUBLE"}),
    (("db2",), {"text": "VARCHAR({n})", "int": "INTEGER", "long": "BIGINT", "big": "DECIMAL({p})", "decimal": "DECIMAL({p},{s})", "float": "DOUBLE"}),
]


def parse_stack(stack: str) -> dict[str, str]:
    """"<front end>; <back end>; <data>" as its three parts (any missing are empty)."""
    parts = [p.strip() for p in stack.split(";")] + ["", "", ""]
    return {"front_end": parts[0], "back_end": parts[1], "data": parts[2]}


def _match(table, text: str):
    words = text.lower()
    for names, types in table:
        if any(re.search(rf"(?<![a-z]){re.escape(n)}(?![a-z])", words) for n in names):
            return names[0], types
    return None, None


def stack_types(stack: dict[str, str] | None) -> dict[str, Any]:
    """The code and column type tables the stack names, and what the table does not know."""
    if not stack:
        return {"code": None, "column": None, "notes": ["The target stack is not given yet, so the neutral types stand; the engineer gives it with --stack."]}
    language, code = _match(LANGUAGES, stack.get("back_end", ""))
    store, column = _match(STORES, stack.get("data", ""))
    notes = []
    if not code:
        notes.append(f'Reframe has no code types for the back end "{stack.get("back_end", "")}"; the neutral types stand.')
    if not column:
        notes.append(f'Reframe has no column types for the data store "{stack.get("data", "")}"; the neutral types stand.')
    return {"code": code, "column": column, "language": language, "store": store, "notes": notes}


def on_stack(t: dict[str, Any], types: dict[str, Any]) -> dict[str, str]:
    kind = t.get("type")
    if kind in ("text", "formatted"):
        slot, n = "text", t.get("length", 0)
    elif kind == "integer":
        slot, n = ("int" if t["digits"] <= 9 else "long" if t["digits"] <= 18 else "big"), 0
    elif kind == "decimal":
        slot, n = "decimal", 0
    elif kind == "float":
        slot, n = "float", 0
    else:
        return {}
    found = {}
    for side in ("code", "column"):
        table = types.get(side)
        if table:
            found[side] = table[slot].format(n=n, p=t.get("digits", 0), s=t.get("scale", 0))
    return found


# ---- contracts ---------------------------------------------------------------------------------------------------------

def contract(name: str, path: Path, legacy: Path, types: dict[str, Any]) -> dict[str, Any]:
    """A copybook as records of typed fields."""
    rel = path.relative_to(legacy).as_posix()
    items = data_items(path.read_text(errors="replace"), rel)
    records: list[dict[str, Any]] = []
    top = min((i.level for i in items if i.level not in (66, 77, 88)), default=1)
    groups: list[tuple[int, str]] = []
    last: dict[str, Any] | None = None
    for item in items:
        if item.level == 88:
            if last is not None:
                last.setdefault("conditions", []).append({"name": item.name, "value": item.value if item.value is not None else ""})
            continue
        if item.level == top or not records:
            records.append({"name": item.name if item.level == top else name, "line": item.line, "fields": []})
            groups = []
            if item.level == top and not item.pic:
                last = None
                continue
        while groups and groups[-1][0] >= item.level:
            groups.pop()
        t = neutral(item.pic, item.usage)
        field = {"name": item.name, "level": item.level, "group": "/".join(g for _, g in groups), "pic": item.pic,
                 "usage": item.usage, **t, "says": describe(t), "line": item.line}
        if item.occurs:
            field["occurs"] = item.occurs
        if item.redefines:
            field["redefines"] = item.redefines
        typed = on_stack(t, types)
        if typed:
            field["stack"] = typed
        records[-1]["fields"].append(field)
        last = field
        if not item.pic and t["type"] == "group":
            groups.append((item.level, item.name))
    return {"copybook": name, "file": rel, "records": records}


def contracts(legacy: Path, wanted: set[str], types: dict[str, Any]) -> dict[str, Any]:
    books = copybooks(legacy)
    return {name: contract(name, books[name], legacy, types) for name in sorted(wanted) if name in books}
