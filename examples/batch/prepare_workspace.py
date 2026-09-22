#!/usr/bin/env python3
"""Create a clean synthetic workspace for one batch iteration."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--fixture", required=True, type=Path)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    fixture = args.fixture.resolve()
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    shutil.copyfile(fixture, workspace / "input.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
