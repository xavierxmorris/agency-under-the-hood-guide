# Contributor contract

This repository explains Agency from released documentation and safe black-box
behavior. It does not document proprietary implementation internals.

## Evidence rules

- Add factual claims to `data/claims.json` before relying on them in prose.
- Facts require a `docs/agency` path and section from the pinned release.
- Interpretations and recommendations require `derived_from` claim IDs.
- Label experimental behavior and avoid promising command stability.
- If documentation is ambiguous, record the ambiguity in `docs/known-gaps.md`;
  do not resolve it by guessing.

## Public-safety rules

- Never add credentials, tokens, customer data, private endpoints, internal
  repository URLs, proprietary source excerpts, or local absolute paths.
- Do not document internal-only, private-preview, roadmap-only, or unshipped
  systems.
- Use placeholders and synthetic examples.
- Keep local probes under `.artifacts/`; never commit their output.

## Generated content

`site/index.html` is generated from `data/*.json`.

```text
python scripts/generate_site.py
python scripts/generate_site.py --check
```

Do not hand-edit the generated site.

## Validation

Use Python 3.11+ and the standard library.

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

Or run the complete PowerShell gate:

```powershell
.\go.ps1 -Check
```
