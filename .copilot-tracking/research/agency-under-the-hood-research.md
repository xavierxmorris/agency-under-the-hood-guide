# Agency under the hood: research

## Scope

This research describes the released Agency product from observable behavior and
canonical documentation installed with Agency `2026.9.16.4`.

It intentionally excludes:

- proprietary implementation details;
- restricted support content;
- private service endpoints and repository URLs;
- credentials, local user data, and customer data;
- deprecated pre-Agency material;
- roadmap-only, internal-only, and unshipped systems.

Every public claim must be one of:

1. **Documented fact** — supported by a released `docs/agency` source.
2. **Interpretation** — a synthesis derived from documented facts.
3. **Recommendation** — guidance derived from facts and clearly labeled.

## Evidence base

Canonical sources reviewed:

- `docs/agency/index.md`
- `docs/agency/Overview/overview.md`
- `docs/agency/CLI/index.md`
- `docs/agency/CLI/agency-config.md`
- `docs/agency/CLI/agency-config-schema.md`
- `docs/agency/CLI/agency-config-profiles.md`
- `docs/agency/CLI/agency-config-remote.md`
- `docs/agency/GitHubCopilotApp/index.md`
- `docs/agency/AzureDevOps/Experiences/agent-hub.md`
- `docs/agency/AzureDevOps/Agency API/overview.md`
- `docs/agency/Tools/Plugins/plugins.md`
- `docs/agency/Tools/Plugins/marketplaces.md`
- `docs/agency/Tools/CustomAgents/creating-custom-agents.md`
- `docs/agency/Tools/CustomAgents/mcp-servers.md`
- `docs/agency/Tools/MCP/mcp.md`
- `docs/agency/Tools/Evals/index.md`
- `docs/agency/Tools/Evals/authoring.md`
- `docs/agency/Tools/Evals/harnesses.md`
- `docs/agency/Tools/BatchRuns/index.md`
- `docs/agency/Tools/Telemetry/overview.md`
- `docs/agency/Tools/Telemetry/querying-agency-telemetry.md`
- `docs/agency/Guidance/measuring-ai-readiness.md`
- `docs/agency/Support/faq.md`

Installed behavior checked:

- `agency --version`
- top-level and major command help;
- configuration discovery and validation;
- profile discovery;
- persistent plugin listing;
- Copilot and Claude adapter help;
- batch-run and plugin-evaluation command surfaces.

## Primary conclusion

**Documented fact:** Agency describes its client as a thin layer around supported
agent engines. The engine owns the conversational and model-driven tool loop.
Agency adds Microsoft identity, configuration, MCP integration, reusable
capabilities, hosted entry points, governance, telemetry, updates, and support.

**Interpretation:** Agency is best understood as an integration, governance, and
execution control plane around agent engines, not as a replacement model runtime.

## Six-layer architecture

1. **User and automation surfaces**
   - local CLI;
   - GitHub Copilot App Agency mode;
   - Azure DevOps browser experiences;
   - REST API and automation.
2. **Agency integration and control**
   - identity;
   - configuration and profiles;
   - capability resolution;
   - marketplace and service policy;
   - telemetry and support.
3. **Portable capability content**
   - custom agents;
   - skills;
   - plugins;
   - MCP declarations.
4. **Engine adapters**
   - supported conversational and tool-execution engines.
5. **Tools and resources**
   - MCP services;
   - repositories;
   - build systems;
   - external APIs.
6. **Execution environments**
   - local device;
   - Agency-managed hosted compute;
   - customer-controlled pipeline compute where supported.

## Local session lifecycle

The released documentation implies this sequence:

1. A user selects an engine and interaction mode.
2. Agency discovers global, repository, and nearer-directory configuration.
3. Remote base configuration is resolved within the declaring config layer.
4. Selected profiles are merged; isolated profiles can remove ambient config.
5. Agent, plugin, dependency, artifact, and MCP capabilities are resolved.
6. Plugins are materialized into session-specific working copies.
7. Agency launches the selected engine with the resolved context.
8. The engine runs its conversation and tool loop.
9. The process returns results and selected telemetry is emitted.

This ordering is a synthesis, not a direct quotation from one lifecycle document.

## Hosted job lifecycle

The released hosted surface separates job intent from execution environment:

1. A user or automation submits a prompt and optional agent/plugin configuration.
2. Agency validates identity, repository context, policy, and requested capability.
3. Agency selects or accepts the configured compute boundary.
4. The agent engine runs with service-resolved capabilities.
5. Results, logs, job state, and optional repository changes are returned.
6. Deterministic build, test, policy, and human-review gates remain authoritative.

**Recommendation:** Never treat an agent-reported success value alone as proof that
external acceptance criteria passed.

## Configuration model

Configuration is a provenance-aware merge graph rather than one flat file:

- global-to-local file discovery;
- remote bases resolved inside the file that declares them;
- named profiles layered in caller-specified order;
- isolated profiles that exclude ambient host configuration;
- MCP-specific source precedence;
- service-side plugin policy that can differ from local CLI behavior.

High-value operating practices:

- validate the effective configuration;
- inspect value provenance;
- use isolated profiles for reproducible runs;
- pin remote configuration and plugin refs where reproducibility matters;
- test local and hosted policy separately.

## Capability model

| Concept | Role |
| --- | --- |
| Plugin | Primary distribution and governance unit |
| Skill | Focused reusable instructions or knowledge |
| Custom agent | Named task-oriented instructions and tool contract |
| MCP server | External tool-provider boundary |
| Marketplace | Distribution and trust-maturity boundary |
| Profile | Named composition of configuration and capability choices |

An effective MCP permission is constrained by:

```text
implemented tools
∩ server-exposed tools
∩ agent-allowed tools
∩ backing-service authorization
```

Tool filtering improves least privilege but does not replace authentication or
authorization in the backing service.

## Evaluation model

Agency exposes two distinct measurement systems:

- **Plugin evals** answer whether a plugin, skill, or agent behaves correctly
  against authored tasks and withheld graders.
- **Batch runs** answer how reliably an agent succeeds across a dataset and
  repeated iterations using deterministic validation.

Plugin-evaluation guidance requires realistic prompts, independent tasks, fixtures
when context is needed, edge cases, and negative cases. The default container
harness provides an isolation boundary; the host harness does not.

## Improvement loop

The released mechanisms support this practical loop:

```text
Observe outcomes and friction
        ↓
Classify repeated failures or successful practices
        ↓
Encode the learning in the strongest available mechanism
        ↓
Validate with checks, tests, plugin evals, or batch runs
        ↓
Distribute through configuration or governed plugins
        ↓
Measure again
```

The strength ladder is:

1. analyzer or deterministic check;
2. regression test;
3. eval;
4. runtime policy;
5. skill or repository guidance.

## Trust boundaries

The guide must distinguish:

- user identity from engine behavior;
- agent tool allowlists from service authorization;
- plugin availability from plugin trust;
- marketplace maturity from code safety;
- local execution from hosted execution;
- job completion from independent validation;
- telemetry aggregation from raw session content;
- stable released surfaces from experimental command families.

## Documentation ambiguities observed

These are version-specific documentation gaps, not reverse-engineered product
defects:

1. Profile plugin-list merge descriptions are not fully consistent.
2. High-level telemetry wording and field-level default descriptions can be read
   differently.
3. Some plugin examples use a global-config shorthand different from the
   canonical platform-specific path.
4. Local and service-side plugin policy must be distinguished more clearly.
5. Technical job identity, initiating-user authorization, and contribution
   attribution deserve separate terminology.
6. Two browser experiences use similar Hub naming and require qualification.

The public guide should tell readers to verify effective runtime behavior for the
installed release instead of resolving these ambiguities by speculation.

## Public repository requirements

The repository must:

- lead with the six-layer architecture;
- provide local and hosted sequence diagrams;
- maintain a machine-readable claim ledger;
- label facts, interpretations, and recommendations;
- provide progressive learning labs;
- include safe black-box probes that do not read real user configuration;
- include an evidence-based readiness scorecard;
- validate links, JSON, claim relationships, generated output, and public safety;
- mark experimental commands explicitly;
- avoid private endpoints, internal repository links, proprietary code, and
  unshipped systems;
- receive independent GPT-6 Astra and Claude Opus 5 review before publication.

## Research decision

Proceed with a standalone public guide named `agency-under-the-hood-guide`. The
guide will explain observable architecture and improvement practices; it will not
claim access to Agency implementation internals.
