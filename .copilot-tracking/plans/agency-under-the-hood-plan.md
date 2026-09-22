# Agency under-the-hood guide: implementation plan

## Outcome

Publish a public-safe repository that teaches how Agency works from released
documentation and black-box behavior, then turns that understanding into
repeatable improvement practices.

## Non-goals

- Reproducing or explaining proprietary source code.
- Documenting private endpoints, internal repositories, or customer data.
- Presenting preview-only or roadmap systems as released architecture.
- Modifying Agency.
- Promising engine parity where the product documents adapter differences.

## Repository structure

```text
agency-under-the-hood-guide/
|-- README.md
|-- AGENTS.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- go.ps1
|-- .github/
|   |-- copilot-instructions.md
|   `-- workflows/validate.yml
|-- docs/
|   |-- architecture.md
|   |-- session-lifecycles.md
|   |-- configuration.md
|   |-- capability-model.md
|   |-- evaluation-and-improvement.md
|   |-- trust-boundaries.md
|   |-- known-gaps.md
|   |-- evidence.md
|   `-- labs/
|       |-- README.md
|       |-- 01-observe-the-surface.md
|       |-- 02-prove-config-precedence.md
|       |-- 03-design-a-plugin-eval.md
|       |-- 04-measure-agent-reliability.md
|       `-- 05-build-an-improvement-scorecard.md
|-- data/
|   |-- claims.json
|   |-- architecture.json
|   |-- maturity.json
|   `-- scorecard.template.json
|-- examples/
|   |-- isolated-profile/agency.toml
|   `-- scorecard/sample-scorecard.json
|-- scripts/
|   |-- capture-agency-surface.ps1
|   |-- generate_site.py
|   `-- validate.py
|-- site/index.html
`-- tests/test_repository.py
```

## Phase 1: evidence model

1. Create a claim ledger pinned to Agency `2026.9.16.4`.
2. Give each claim a stable ID and type: fact, interpretation, recommendation.
3. Require evidence for facts and `derived_from` relationships for synthesis.
4. Create architecture and maturity data consumed by both documentation and site.

Acceptance:

- Claim IDs are unique.
- Every fact has a released documentation source and section.
- Every interpretation/recommendation traces to existing claim IDs.
- No private URLs or local absolute paths are present.

## Phase 2: core guide

1. Write the executive README and product mental model.
2. Publish six-layer architecture and ownership map.
3. Publish local and hosted lifecycle sequence diagrams.
4. Explain configuration as a merge graph with provenance.
5. Differentiate plugin, skill, agent, MCP, marketplace, and profile.
6. Explain plugin evals versus batch runs.
7. Publish trust boundaries and version-specific documentation ambiguities.

Acceptance:

- Every major architectural assertion maps to the claim ledger.
- Stable and experimental behavior are visibly separated.
- The guide contains no implementation speculation.

## Phase 3: learning and improvement

1. Create five progressive labs.
2. Add a safe probe script limited to help/version output and isolated config.
3. Add an AI-readiness scorecard based on outcomes and deterministic validation.
4. Link the existing public plugin-evals workshop as the advanced companion lab.

Acceptance:

- Labs are runnable without modifying real user configuration.
- Commands use placeholders rather than private names or endpoints.
- Each lab defines objective, evidence, success criteria, and cleanup.

## Phase 4: generated visual guide

1. Generate a dependency-free static HTML dashboard from repository JSON.
2. Show architecture layers, claim counts, maturity, and improvement loop.
3. Commit generated output and verify it is reproducible.

Acceptance:

- `python scripts/generate_site.py --check` passes.
- The site uses no external scripts or remote assets.

## Phase 5: deterministic validation

Create standard-library validation for:

- JSON structure and cross-references;
- local Markdown links;
- required repository files;
- generated-site freshness;
- private URL, local path, token, and placeholder leakage;
- minimal unit tests on validator behavior.

Run on Windows and Ubuntu in GitHub Actions with read-only permissions.

## Phase 6: independent review

1. Run deterministic checks.
2. Request max-effort, long-context GPT-6 Astra review.
3. Request max-effort, long-context Claude Opus 5 review.
4. Reconcile disagreements against the installed documentation and runtime.
5. Fix all high-confidence correctness, safety, and usability findings.
6. Re-run checks and record review outcomes.

## Phase 7: publication

1. Configure repository-local Git identity.
2. Commit with the required Copilot co-author trailer.
3. Create `xavierxmorris/agency-under-the-hood-guide` as a public repository.
4. Push the default branch.
5. Verify hosted validation completes successfully.

## Final acceptance criteria

- Public GitHub repository exists and hosted CI passes.
- No restricted/internal-only material is present.
- Claims are traceable and version-pinned.
- Architecture, lifecycle, configuration, capability, evaluation, trust, and
  improvement topics are covered.
- Five runnable labs and a generated visual guide are included.
- Both required independent reviews completed and their accepted findings were
  remediated.
