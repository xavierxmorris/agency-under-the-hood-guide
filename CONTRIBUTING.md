# Contributing

Contributions should improve the accuracy, teachability, or verifiability of the
guide without expanding beyond its public-safe scope.

## Change a claim

1. Verify the statement against the version-matched installed `docs/agency`
   documentation.
2. Update `data/claims.json`.
3. Update the related prose.
4. Regenerate `site/index.html`.
5. Run the complete repository gate.

Facts need a documentation path and section. Interpretations and recommendations
need `derived_from` IDs.

## Change architecture or maturity data

Update the matching JSON file under `data/`, regenerate the site, and check that
the diagrams and prose still describe the same boundary.

## Change a lab

Every lab must include:

- an objective;
- the claim IDs it demonstrates;
- prerequisites;
- commands or a worksheet;
- observable evidence;
- success criteria;
- targeted cleanup.

Labs must not read or modify real user configuration unless the user explicitly
chooses to do so. Prefer isolated configuration paths and `.artifacts/`.

## Validate

```powershell
.\go.ps1 -Check
```

The gate checks evidence relationships, JSON structure, local links, generated
output, and public-safety patterns on Windows and Ubuntu.
