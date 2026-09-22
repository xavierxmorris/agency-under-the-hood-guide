#!/usr/bin/env python3
"""Validate the batch output independently of the agent's conclusion."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("expected", choices=["VALIDATED", "UNVERIFIED"])
    args = parser.parse_args()

    result = Path("result.txt")
    if not result.is_file():
        print("result.txt was not produced")
        return 1
    actual = result.read_text(encoding="utf-8").strip()
    if actual != args.expected:
        print(f"expected {args.expected}, got {actual!r}")
        return 1
    print(f"validated result: {actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
