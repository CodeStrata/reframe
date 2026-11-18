"""Check that a pull request into v2 fills in the specification-alignment section.

docs/v2/README.md requires every pull request into `v2` to name the
specification sections and the stories it implements, and to confirm that the
specification, plan, epics and stories already describe the change. The pull
request body is read from the PR_BODY environment variable and treated as data.
"""

from __future__ import annotations

import os
import re
import sys

CONFIRMATION = "The specification, plan, epics and stories already describe this change"


def problems(body: str) -> list[str]:
    found: list[str] = []
    text = body.replace("\r\n", "\n")
    if "## Specification alignment (v2)" not in text:
        return ["The pull request body has no '## Specification alignment (v2)' section (.github/pull_request_template.md)."]

    sections = re.search(r"^- Specification sections:[ \t]*(.*)$", text, re.MULTILINE)
    if not sections or not sections.group(1).strip():
        found.append("Name the specification sections this change implements on the 'Specification sections:' line.")

    stories = re.search(r"^- Stories:[ \t]*(.*)$", text, re.MULTILINE)
    if not stories or not re.search(r"#\d+", stories.group(1)):
        found.append("Name at least one story issue (for example #216) on the 'Stories:' line.")

    ticked = re.search(r"^- \[[xX]\] " + re.escape(CONFIRMATION), text, re.MULTILINE)
    if not ticked:
        found.append(
            "Tick the confirmation that the specification, plan, epics and stories already describe this change. "
            "If they do not, update them first (docs/v2/README.md)."
        )
    return found


def main() -> int:
    found = problems(os.environ.get("PR_BODY", ""))
    for item in found:
        print(f"::error::{item}")
    if not found:
        print("Specification alignment section is complete.")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
