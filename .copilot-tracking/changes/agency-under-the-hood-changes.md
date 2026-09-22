# Agency under-the-hood guide: changes log

## Implemented

- Added a six-layer architecture model and machine-readable graph.
- Added a 36-claim evidence ledger:
  - 22 documented facts;
  - 6 architectural interpretations;
  - 8 operating recommendations.
- Added local and hosted lifecycle sequence diagrams.
- Added configuration, capability, evaluation, trust-boundary, known-gap, and
  evidence chapters.
- Added five progressive labs:
  - installed-surface observation;
  - isolated config precedence;
  - plugin-eval design;
  - batch reliability;
  - outcome scorecard.
- Added synthetic configuration, batch, and scorecard examples.
- Added a safe PowerShell probe that captures only version/help surfaces and
  validates an isolated synthetic config.
- Added a dependency-free HTML guide generated from repository JSON.
- Added standard-library validation for evidence relationships, JSON, links,
  generated output, required files, scorecards, and public-safety patterns.
- Added fifteen unit tests and cross-platform GitHub Actions validation.
- Added repository contributor and Copilot guidance.

## Validation completed

```text
python scripts/generate_site.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
.\go.ps1 -Check
.\go.ps1 -Probe -NoBrowser
```

Results:

- generated site current;
- repository validation passed;
- 15 unit tests passed;
- complete PowerShell gate passed;
- safe Agency probe passed without reading real user configuration.

## Remaining

No implementation work remains.

## Publication

- Repository: https://github.com/xavierxmorris/agency-under-the-hood-guide
- Initial commit: `3cc4b6d`
- Hosted validation:
  https://github.com/xavierxmorris/agency-under-the-hood-guide/actions/runs/35715518636
- Ubuntu validation passed.
- Windows validation passed.
