# Trust boundaries

Agency composes several systems. Each boundary solves a different problem; no
single allowlist or marketplace label replaces the others.

## Boundary map

| Boundary | Primary controls | Residual question |
| --- | --- | --- |
| User to local engine | Sign-in, invocation, engine permission flow | What can the local account reach? |
| Agency to engine | Resolved config, profiles, capability adapters | Does engine behavior match the declared support? |
| Agent to MCP | Exposed-tool and agent-tool filters | What does the service credential authorize? |
| Plugin to session | Source, pinning, cache, working copy | Is the content trusted and reviewed? |
| Marketplace to consumer | Ownership, curation, scanning, support | What maturity and rollback guarantees exist? |
| Eval task to host | Container isolation or host execution | Is the task trusted with host access? |
| Hosted job to compute | Identity, network, image, and pipeline policy | Who controls dependencies and egress? |
| Job to repository | Repository permissions, branch policy, review | Did independent acceptance criteria pass? |
| Telemetry to analysis | Scrubbing, access control, aggregation grain | What data is absent or delayed? |

## Tool filtering is not authorization

The effective-access model is:

```text
implemented ∩ exposed ∩ agent-allowed ∩ service-authorized
```

The last term is authoritative. Hiding a tool from an agent narrows access; it
does not create permission in the service or revoke permission from another
client using the same credential.

## Plugin trust is multidimensional

Review:

1. **Source:** where did the content come from?
2. **Identity:** who owns and supports it?
3. **Immutability:** is the exact revision pinned?
4. **Dependencies:** what else is acquired or executed?
5. **Compatibility:** which engines and surfaces are tested?
6. **Evaluation:** are positive, edge, and negative cases present?
7. **Update policy:** can a stale cache or background refresh change behavior?
8. **Rollback:** can the last known-good revision be restored?

## Hosted success needs independent proof

A hosted agent result is one signal. Acceptance should combine:

- deterministic build and tests;
- policy checks;
- artifact inspection;
- repository diff review;
- human approval when required.

This protects against plausible-but-wrong output and against success values that
represent how the agent concluded rather than an external verdict.

## Telemetry is not a transcript archive

Agency Telemetry exposes selected, privacy-scrubbed events
([F-014](../data/claims.json)). It is appropriate for aggregated trends and
reliability analysis. It is not a complete, real-time record of every
interaction and should not be used to rank individual engineers.

## Public-guide boundary

This repository deliberately excludes:

- private endpoints and internal repository locations;
- proprietary source and support routing;
- credentials and customer content;
- roadmap-only and unshipped systems;
- claims that cannot be tied to the released evidence ledger.
