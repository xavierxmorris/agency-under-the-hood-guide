# Repository guidance

Treat `data/claims.json` as the source of truth for architectural assertions.
Separate documented fact, interpretation, and recommendation.

The guide is pinned to Agency `2026.9.16.4`. Do not silently generalize
version-sensitive commands, engine behavior, or experimental eval output.

Keep the repository public-safe:

- no private URLs, credentials, customer data, local absolute paths, proprietary
  source excerpts, or restricted support material;
- no roadmap-only, private-preview, or internal-only product descriptions;
- no claim that tool filtering replaces backing-service authorization;
- no claim that a completed agent job proves its acceptance criteria.

Use Python 3.11+, the standard library, and `unittest`. After changing repository
data, regenerate `site/index.html` and run:

```text
python scripts/generate_site.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
```
