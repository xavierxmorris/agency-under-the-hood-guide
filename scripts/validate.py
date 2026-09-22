#!/usr/bin/env python3
"""Validate evidence, links, generated output, and public-safety boundaries."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

import generate_site


ROOT = Path(__file__).resolve().parents[1]
CLAIM_ID = re.compile(r"^[FIR]-\d{3}$")
CLAIM_REFERENCE = re.compile(r"\b[FIR]-\d{3}\b")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TEXT_SUFFIXES = {
    ".csv",
    ".html",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
}


def host_url_pattern(*parts: str) -> re.Pattern[str]:
    host = ".".join(parts)
    return re.compile(r"(?i)https?://[^/\s]*" + re.escape(host))


PUBLIC_SAFETY_PATTERNS = {
    "local Windows user path": re.compile(
        r"(?i)[a-z]:(?:\\{1,2})users(?:\\{1,2})"
    ),
    "local POSIX home path": re.compile(r"(?i)/(?:home|users)/[^/\s\"']+/"),
    "private Azure DevOps URL": host_url_pattern("dev", "azure", "com"),
    "private documentation URL": host_url_pattern("eng", "ms"),
    "private SharePoint URL": host_url_pattern("share" + "point", "com"),
    "private Visual Studio URL": host_url_pattern("visualstudio", "com"),
    "private marketplace repository": re.compile(
        re.escape("." + "github" + "-" + "private"), re.IGNORECASE
    ),
    "private documentation path": re.compile(
        re.escape("docs" + "/" + "internal" + "/"), re.IGNORECASE
    ),
    "private corporate identity": re.compile(
        re.escape("@" + "microsoft" + ".com"), re.IGNORECASE
    ),
    "non-public Microsoft host": re.compile(
        r"(?i)\b(?!learn\.)[a-z0-9.-]+\."
        + re.escape("microsoft" + "." + "com")
        + r"\b"
    ),
    "bearer token": re.compile(r"(?i)authorization:\s*bearer\s+\S+"),
    "GitHub token": re.compile(
        r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"
    ),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "go.ps1",
    ".gitattributes",
    ".github/copilot-instructions.md",
    ".github/workflows/validate.yml",
    "data/claims.json",
    "data/architecture.json",
    "data/maturity.json",
    "data/scorecard.template.json",
    "docs/architecture.md",
    "docs/session-lifecycles.md",
    "docs/configuration.md",
    "docs/capability-model.md",
    "docs/evaluation-and-improvement.md",
    "docs/trust-boundaries.md",
    "docs/known-gaps.md",
    "docs/evidence.md",
    "docs/labs/README.md",
    "scripts/verify_installed_evidence.py",
    "site/index.html",
]


def load_json(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_required_files() -> list[str]:
    return [
        f"missing required file: {relative_path}"
        for relative_path in REQUIRED_FILES
        if not (ROOT / relative_path).is_file()
    ]


def validate_claims() -> list[str]:
    errors: list[str] = []
    data = load_json("data/claims.json")
    claims = data.get("claims", [])
    ids = [claim.get("id") for claim in claims]
    known_ids = set(ids)
    claims_by_id = {claim.get("id"): claim for claim in claims}
    if len(ids) != len(known_ids):
        errors.append("claim IDs must be unique")

    for claim in claims:
        claim_id = claim.get("id", "")
        if not CLAIM_ID.fullmatch(claim_id):
            errors.append(f"invalid claim ID: {claim_id!r}")
        if claim.get("kind") not in {"fact", "interpretation", "recommendation"}:
            errors.append(f"{claim_id}: invalid kind")
        if claim.get("status") not in {"released", "experimental"}:
            errors.append(f"{claim_id}: invalid status")
        if not claim.get("statement"):
            errors.append(f"{claim_id}: statement is required")

        if claim.get("kind") == "fact":
            evidence = claim.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"{claim_id}: facts require evidence")
                continue
            for source in evidence:
                path = source.get("path", "")
                section = source.get("section", "")
                path_parts = PurePosixPath(path).parts
                if (
                    not path.startswith("docs/agency/")
                    or not path.endswith(".md")
                    or ".." in path_parts
                    or "\\" in path
                ):
                    errors.append(f"{claim_id}: invalid evidence path {path!r}")
                if not section:
                    errors.append(f"{claim_id}: evidence section is required")
        else:
            derived_from = claim.get("derived_from")
            if not isinstance(derived_from, list) or not derived_from:
                errors.append(f"{claim_id}: derived claims require derived_from")
                continue
            missing = sorted(set(derived_from) - known_ids)
            if missing:
                errors.append(f"{claim_id}: unknown derived_from IDs {missing}")

    visiting: set[str] = set()
    visited: set[str] = set()
    reaches_fact_cache: dict[str, bool] = {}

    def visit(claim_id: str, trail: tuple[str, ...]) -> bool:
        if claim_id in visiting:
            cycle = " -> ".join((*trail, claim_id))
            errors.append(f"claim derivation cycle: {cycle}")
            return False
        if claim_id in visited:
            return reaches_fact_cache[claim_id]

        claim = claims_by_id[claim_id]
        if claim.get("kind") == "fact":
            visited.add(claim_id)
            reaches_fact_cache[claim_id] = True
            return True

        visiting.add(claim_id)
        reaches_fact = False
        for dependency in claim.get("derived_from", []):
            if dependency in claims_by_id:
                reaches_fact = visit(dependency, (*trail, claim_id)) or reaches_fact
        visiting.remove(claim_id)
        visited.add(claim_id)
        reaches_fact_cache[claim_id] = reaches_fact
        if not reaches_fact:
            errors.append(f"{claim_id}: derivation does not reach a fact")
        return reaches_fact

    for claim_id in known_ids:
        visit(claim_id, ())

    return errors


def validate_architecture() -> list[str]:
    errors: list[str] = []
    data = load_json("data/architecture.json")
    claim_ids = {
        claim["id"] for claim in load_json("data/claims.json").get("claims", [])
    }
    layers = data.get("layers", [])
    if len(layers) != 6:
        errors.append("architecture must contain exactly six layers")
    ids = {layer.get("id") for layer in layers}
    if len(ids) != len(layers):
        errors.append("architecture layer IDs must be unique")
    if sorted(layer.get("order") for layer in layers) != list(range(1, 7)):
        errors.append("architecture layer order must be 1 through 6")
    for layer in layers:
        if layer.get("owner") not in {"agency", "engine", "shared", "external"}:
            errors.append(f"{layer.get('id')}: invalid owner")
        if not layer.get("responsibilities") or not layer.get("examples"):
            errors.append(f"{layer.get('id')}: responsibilities and examples required")
        references = layer.get("claims")
        if not references:
            errors.append(f"{layer.get('id')}: claim references are required")
        elif unknown := sorted(set(references) - claim_ids):
            errors.append(f"{layer.get('id')}: unknown claim references {unknown}")
    for edge in data.get("edges", []):
        if edge.get("from") not in ids or edge.get("to") not in ids:
            errors.append(f"architecture edge references unknown layer: {edge}")
    return errors


def validate_maturity() -> list[str]:
    errors: list[str] = []
    data = load_json("data/maturity.json")
    claim_ids = {
        claim["id"] for claim in load_json("data/claims.json").get("claims", [])
    }
    surfaces = data.get("surfaces", [])
    ids = [surface.get("id") for surface in surfaces]
    if len(ids) != len(set(ids)):
        errors.append("maturity IDs must be unique")
    for surface in surfaces:
        if surface.get("status") not in {"released", "experimental", "excluded"}:
            errors.append(f"{surface.get('id')}: invalid maturity status")
        if not surface.get("guide_policy"):
            errors.append(f"{surface.get('id')}: guide_policy is required")
        references = surface.get("claims", [])
        if surface.get("status") != "excluded" and not references:
            errors.append(f"{surface.get('id')}: claim references are required")
        elif unknown := sorted(set(references) - claim_ids):
            errors.append(f"{surface.get('id')}: unknown claim references {unknown}")
    return errors


def validate_scorecards() -> list[str]:
    errors: list[str] = []
    template = load_json("data/scorecard.template.json")
    dimensions = template.get("dimensions", [])
    dimension_ids = {item.get("id") for item in dimensions}
    expected = {
        "verification",
        "understandability",
        "automation",
        "operability",
        "effectiveness",
    }
    if dimension_ids != expected:
        errors.append("scorecard template must contain the five readiness dimensions")

    sample = load_json("examples/scorecard/sample-scorecard.json")
    sample_ids = {item.get("id") for item in sample.get("dimensions", [])}
    if sample_ids != expected:
        errors.append("sample scorecard dimensions must match the template")
    for dimension in sample.get("dimensions", []):
        score = dimension.get("score")
        if not isinstance(score, int) or not 0 <= score <= 4:
            errors.append(f"{dimension.get('id')}: sample score must be 0 through 4")
        if not dimension.get("evidence"):
            errors.append(f"{dimension.get('id')}: sample evidence is required")
    return errors


def validate_markdown_links() -> list[str]:
    errors: list[str] = []
    for markdown_file in ROOT.rglob("*.md"):
        if any(part in {".git", ".artifacts"} for part in markdown_file.parts):
            continue
        text = markdown_file.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if (
                not target
                or target.startswith("#")
                or target.startswith(("http://", "https://", "mailto:"))
            ):
                continue
            path_part = unquote(target.split("#", 1)[0])
            resolved = (
                ROOT / path_part.lstrip("/")
                if path_part.startswith("/")
                else markdown_file.parent / path_part
            ).resolve()
            if not resolved.exists():
                relative = markdown_file.relative_to(ROOT)
                errors.append(f"{relative}: broken local link {raw_target!r}")
    return errors


def validate_claim_references() -> list[str]:
    errors: list[str] = []
    claim_ids = {
        claim["id"] for claim in load_json("data/claims.json").get("claims", [])
    }
    referenced: set[str] = set()
    public_files = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
    for markdown_file in public_files:
        text = markdown_file.read_text(encoding="utf-8")
        found = set(CLAIM_REFERENCE.findall(text))
        referenced.update(found)
        unknown = sorted(found - claim_ids)
        for claim_id in unknown:
            errors.append(
                f"{markdown_file.relative_to(ROOT)}: unknown claim reference {claim_id}"
            )

    orphaned = sorted(claim_ids - referenced)
    if orphaned:
        errors.append(f"claim ledger entries are not referenced in public prose: {orphaned}")
    return errors


def batch_example_errors(text: str) -> list[str]:
    errors: list[str] = []
    lines = text.splitlines()
    top_level_validation = any(line == "validation:" for line in lines)
    if top_level_validation:
        errors.append("batch validation must be nested under job")
    if "  validation:" not in lines or "    exitCode: 0" not in lines:
        errors.append("batch example requires job.validation.exitCode")
    iteration_lines = [line.strip() for line in lines if line.strip().startswith("iterations:")]
    if iteration_lines != ["iterations: 5"]:
        errors.append("batch example iterations must be the numeric value 5")
    if "hooks:" not in lines or "  beforeIteration:" not in lines:
        errors.append("batch example must create its working directory in beforeIteration")
    if "expectedExitCode" in text:
        errors.append("batch example uses unsupported expectedExitCode")
    return errors


def validate_batch_example() -> list[str]:
    errors = batch_example_errors(
        (ROOT / "examples" / "batch" / "eval-config.yaml").read_text(encoding="utf-8")
    )
    required = [
        ROOT / "examples" / "batch" / "prepare_workspace.py",
        ROOT / "examples" / "batch" / "validate_result.py",
        ROOT / "examples" / "batch" / "fixtures" / "validated.txt",
        ROOT / "examples" / "batch" / "fixtures" / "unverified.txt",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing batch example file: {path.relative_to(ROOT)}")
    return errors


def validate_labs() -> list[str]:
    errors: list[str] = []
    required_sections = {
        "## Objective",
        "## Prerequisites",
        "## Success criteria",
        "## Cleanup",
    }
    for lab in sorted((ROOT / "docs" / "labs").glob("[0-9][0-9]-*.md")):
        text = lab.read_text(encoding="utf-8")
        for section in sorted(required_sections):
            if section not in text:
                errors.append(f"{lab.relative_to(ROOT)}: missing {section}")
    return errors


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", ".artifacts", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
            ".editorconfig",
            ".gitignore",
            "LICENSE",
        }:
            yield path


def public_safety_findings(text: str) -> list[str]:
    return [
        label for label, pattern in PUBLIC_SAFETY_PATTERNS.items() if pattern.search(text)
    ]


def validate_public_safety() -> list[str]:
    errors: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        for label in public_safety_findings(text):
            errors.append(f"{path.relative_to(ROOT)}: contains {label}")
    return errors


def validate_generated_site() -> list[str]:
    target = ROOT / "site" / "index.html"
    if not target.exists():
        return ["site/index.html is missing"]
    expected = generate_site.render()
    actual = target.read_text(encoding="utf-8")
    return [] if actual == expected else ["site/index.html is out of date"]


def run_all() -> list[str]:
    checks = [
        validate_required_files,
        validate_claims,
        validate_architecture,
        validate_maturity,
        validate_scorecards,
        validate_markdown_links,
        validate_claim_references,
        validate_batch_example,
        validate_labs,
        validate_public_safety,
        validate_generated_site,
    ]
    errors: list[str] = []
    for check in checks:
        errors.extend(check())
    return errors


def main() -> int:
    try:
        errors = run_all()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"validation aborted: {error}", file=sys.stderr)
        return 2

    if errors:
        print("repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
