#!/usr/bin/env python3
"""Verify fact paths and Markdown headings against an installed Agency docs tree."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def normalize_heading(value: str) -> str:
    value = MARKDOWN_LINK.sub(r"\1", value)
    value = value.replace("`", "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[^a-zA-Z0-9]+", " ", value)
    return " ".join(value.casefold().split())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root",
        required=True,
        type=Path,
        help="Path containing the installed docs/agency directory.",
    )
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    agency_docs_root = (source_root / "docs" / "agency").resolve()

    with (ROOT / "data" / "claims.json").open(encoding="utf-8") as handle:
        claims = json.load(handle)["claims"]

    errors: list[str] = []
    for claim in claims:
        if claim["kind"] != "fact":
            continue
        for evidence in claim["evidence"]:
            relative = PurePosixPath(evidence["path"])
            if ".." in relative.parts or "\\" in evidence["path"]:
                errors.append(
                    f"{claim['id']}: traversal and noncanonical separators are not allowed"
                )
                continue
            target = source_root.joinpath(*relative.parts).resolve()
            try:
                target.relative_to(agency_docs_root)
            except ValueError:
                errors.append(f"{claim['id']}: evidence escapes docs/agency")
                continue
            if not target.is_file():
                errors.append(f"{claim['id']}: missing evidence file {evidence['path']}")
                continue

            headings = {
                normalize_heading(match.group(1))
                for line in target.read_text(encoding="utf-8").splitlines()
                if (match := HEADING.match(line))
            }
            expected = normalize_heading(evidence["section"])
            if expected not in headings:
                errors.append(
                    f"{claim['id']}: section {evidence['section']!r} not found in "
                    f"{evidence['path']}"
                )

    if errors:
        print("installed evidence verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("installed evidence verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
