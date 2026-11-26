"""A small Excel workbook (.xlsx) writer, with the standard library only (docs/sharing.md, section 7).

Each sheet is one table: a bold header row, frozen, with filters on, and wrapped text. Every value is written as text
(an inline string) or as a whole number, never as a formula, so a value that starts with "=" stays text.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

MAX_CELL = 32767  # Excel's limit on the characters in a cell
ILLEGAL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f￾￿]")
SHEET_NAME = re.compile(r"[\[\]:*?/\\]")
STAMP = (1980, 1, 1, 0, 0, 0)  # every part gets the same date, so the same results give the same file

NS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet {NS}>
<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFDDEBF7"/><bgColor indexed="64"/></patternFill></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="3">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


def column(n: int) -> str:
    """The column letters for a 0-based index: 0 is A, 26 is AA."""
    letters = ""
    n += 1
    while n:
        n, rest = divmod(n - 1, 26)
        letters = chr(65 + rest) + letters
    return letters


def text(value: Any) -> str:
    """A value as cell text: lists one item per line, characters XML cannot hold removed, cut to Excel's limit."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        value = "\n".join(text(v) for v in value)
    value = ILLEGAL.sub("", str(value))
    return value if len(value) <= MAX_CELL else value[:MAX_CELL - 1] + "…"


def _cell(ref: str, value: Any, style: int) -> str:
    if isinstance(value, int) and not isinstance(value, bool):
        return f'<c r="{ref}" s="{style}" t="n"><v>{value}</v></c>'
    body = text(value)
    if not body:
        return ""
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{escape(body)}</t></is></c>'


def _width(header: str, rows: list[list[Any]], i: int, wide: int) -> int:
    longest = max([len(header)] + [max((len(line) for line in text(r[i]).split("\n")), default=0) for r in rows[:500] if i < len(r)])
    return max(8, min(wide, longest + 2))


def _sheet(headers: list[str], rows: list[list[Any]], widths: dict[str, int] | None) -> str:
    widths = widths or {}
    cols = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{widths.get(h) or _width(h, rows, i, 60)}" customWidth="1"/>'
                   for i, h in enumerate(headers))
    last = column(len(headers) - 1)
    lines = ['<row r="1">' + "".join(_cell(f"{column(i)}1", h, 1) for i, h in enumerate(headers)) + "</row>"]
    for n, row in enumerate(rows, start=2):
        lines.append(f'<row r="{n}">' + "".join(_cell(f"{column(i)}{n}", v, 2) for i, v in enumerate(row[:len(headers)])) + "</row>")
    view = ('<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
            '<selection pane="bottomLeft" activeCell="A2" sqref="A2"/></sheetView></sheetViews>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet {NS} xmlns:r="{REL}">'
            f'<dimension ref="A1:{last}{len(rows) + 1}"/>{view}<sheetFormatPr defaultRowHeight="15"/><cols>{cols}</cols>'
            f'<sheetData>{"".join(lines)}</sheetData><autoFilter ref="A1:{last}{len(rows) + 1}"/></worksheet>')


def sheet_name(name: str) -> str:
    return SHEET_NAME.sub(" ", name).strip()[:31] or "Sheet"


def write(path: Path, sheets: list[dict[str, Any]], *, title: str = "", active: str | None = None) -> Path:
    """Write the workbook. Each sheet is {"name", "headers", "rows", optional "widths" by header}; `active` names the
    sheet it opens on."""
    names = [sheet_name(s["name"]) for s in sheets]
    if len(set(n.lower() for n in names)) != len(names):
        raise ValueError("two sheets have the same name")
    tab = names.index(sheet_name(active)) if active and sheet_name(active) in names else 0
    parts = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
            + "".join(f'<Override PartName="/xl/worksheets/sheet{i + 1}.xml" '
                      'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(len(sheets)))
            + "</Types>"),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" Type="{REL}/officeDocument" Target="xl/workbook.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            f'<Relationship Id="rId3" Type="{REL}/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>"),
        "docProps/core.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + escape(text(title)) + "</dc:title><dc:creator>Reframe</dc:creator>"
            "</cp:coreProperties>"),
        "docProps/app.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Reframe</Application></Properties>'),
        "xl/workbook.xml": (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook {NS} xmlns:r="{REL}">'
            f'<bookViews><workbookView activeTab="{tab}" firstSheet="0"/></bookViews><sheets>'
            + "".join(f'<sheet name="{escape(n, {chr(34): "&quot;"})}" sheetId="{i + 1}" r:id="rId{i + 1}"/>' for i, n in enumerate(names))
            + "</sheets><definedNames>"
            + "".join(f'<definedName name="_xlnm._FilterDatabase" localSheetId="{i}" hidden="1">\'{n.replace(chr(39), chr(39) * 2)}\'!$A$1:${column(len(s["headers"]) - 1)}${len(s["rows"]) + 1}</definedName>'
                      for i, (n, s) in enumerate(zip(names, sheets)))
            + "</definedNames></workbook>"),
        "xl/_rels/workbook.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(f'<Relationship Id="rId{i + 1}" Type="{REL}/worksheet" Target="worksheets/sheet{i + 1}.xml"/>' for i in range(len(sheets)))
            + f'<Relationship Id="rId{len(sheets) + 1}" Type="{REL}/styles" Target="styles.xml"/></Relationships>'),
        "xl/styles.xml": STYLES,
    }
    for i, s in enumerate(sheets):
        parts[f"xl/worksheets/sheet{i + 1}.xml"] = _sheet(list(s["headers"]), [list(r) for r in s["rows"]], s.get("widths"))
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".partial")
    with zipfile.ZipFile(partial, "w", zipfile.ZIP_DEFLATED) as z:
        for name, body in parts.items():
            info = zipfile.ZipInfo(name, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, body.encode("utf-8"))
    partial.replace(path)
    return path
