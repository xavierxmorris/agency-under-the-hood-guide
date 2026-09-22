# Capability model

Agents, skills, plugins, MCP servers, marketplaces, and profiles solve different
problems. Treating them as interchangeable makes design and review harder.

## Choose the right abstraction

| Abstraction | Use it for | Avoid using it as |
| --- | --- | --- |
| Skill | Focused instructions or knowledge activated for a task | A distribution or authorization boundary |
| Custom agent | A named task contract with instructions and tool choices | A guarantee of engine parity |
| Plugin | Packaging and distributing related agents, skills, MCPs, and metadata | Proof that the content is trusted |
| MCP server | Exposing callable tools from a process or service | A replacement for backing-service authorization |
| Marketplace | Discovery, ownership, curation, and distribution maturity | A runtime sandbox |
| Profile | Reproducible composition of settings and capabilities | A portable capability by itself |

Plugins are the primary Agency distribution unit
([F-006](../data/claims.json)); they can be ephemeral or persistent
([F-007](../data/claims.json)).

Local sessions also receive a version-matched built-in Agency plugin containing
support and pull-request completion skills; it is session-loaded rather than
written into user plugin configuration ([F-019](../data/claims.json)).

## Effective tool access

```text
tools implemented by the MCP
∩ tools exposed by the MCP declaration
∩ tools allowed to the agent
∩ permissions granted by the backing service
```

This is an interpretation of the published tool-filtering and authorization
contracts ([I-004](../data/claims.json)).

### Example

An MCP implements `read_item`, `update_item`, and `delete_item`.

- The plugin exposes `read_item` and `update_item`.
- The agent allows only `read_item`.
- The credential can read and update.

The effective result is **read only**. The credential does not expand the
agent's allowlist, and the allowlist does not grant permission that the service
credential lacks.

## Distribution is not trust

An installable plugin is executable content and should be reviewed as a
supply-chain input. Consider:

- source and ownership;
- pinning strategy;
- engine compatibility;
- review and scanning status;
- dependency and artifact provenance;
- marketplace maturity;
- local versus hosted support;
- rollback and update policy.

Marketplace scopes carry different curation and operational maturity
([F-021](../data/claims.json)). Use the trust decision from
[R-005](../data/claims.json): installability is not proof of trust.

## Engine compatibility

Agency supports portable custom-agent formats
([F-008](../data/claims.json)), but plugin compatibility is explicit
([F-022](../data/claims.json)).

For each supported engine:

1. validate manifest and file placement;
2. verify required tools exist;
3. run positive, edge, and negative scenarios;
4. compare failure behavior;
5. document engine-specific limitations.

## Packaging pattern

Package a workflow together when its pieces form one coherent capability:

```text
plugin/
|-- manifest
|-- agents/
|-- skills/
|-- MCP declaration or launcher
|-- evals/
`-- usage and support guidance
```

Keep authorization and mandatory dependency failures explicit. A plugin should
not silently invent data or return success when its required tool is absent.
