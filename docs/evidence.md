# Evidence model

The repository is designed to make unsupported architectural drift difficult.

## Claim types

| Type | Required fields | Meaning |
| --- | --- | --- |
| Fact | `evidence` with path and section | A released document explicitly supports the statement |
| Interpretation | `derived_from` claim IDs | A synthesis of documented facts |
| Recommendation | `derived_from` claim IDs | Operating guidance justified by the evidence chain |

See [`data/claims.json`](../data/claims.json).

## Why paths instead of copied documentation

Agency operational documentation is version-matched with the installed product.
This guide records relative `docs/agency` paths and sections so authorized users
can open the matching source tree without copying private documentation into a
public repository.

The source references are anchors, not external public links.

## Evidence workflow

1. Record the installed Agency version.
2. Open the canonical `docs/agency` document.
3. Confirm the section supports the proposed statement.
4. Add or update the fact claim.
5. Reference the fact from interpretations and recommendations.
6. Regenerate the visual guide.
7. Run deterministic validation.
8. Review the public diff for restricted or local content.

## Machine checks

[`scripts/validate.py`](../scripts/validate.py) verifies:

- claim ID uniqueness and shape;
- evidence requirements for facts;
- `derived_from` relationships;
- architecture and maturity data;
- scorecard structure;
- local Markdown links;
- generated-site freshness;
- common public-safety leakage patterns.

[`tests/test_repository.py`](../tests/test_repository.py) runs each validation
surface independently.

For an authorized local source tree,
[`scripts/verify_installed_evidence.py`](../scripts/verify_installed_evidence.py)
also verifies that every fact file and cited Markdown heading exists:

```text
python scripts/verify_installed_evidence.py --source-root <AGENCY_SOURCE_ROOT>
```

## What the ledger cannot prove

The ledger does not automatically prove that:

- the cited installed document remains unchanged in another release;
- the runtime exactly matches every document;
- a recommendation is the only reasonable design;
- an external service authorizes a tool call;
- a hosted job met acceptance criteria.

Those questions require release-specific runtime checks, service authorization,
deterministic validation, or review.
