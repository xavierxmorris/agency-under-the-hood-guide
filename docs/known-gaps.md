# Known gaps and version-sensitive areas

This page records documentation ambiguities observed in Agency `2026.9.16.4`.
They are not claims about undocumented implementation behavior.

## Configuration list merging

Profile documentation and schema-level plugin merge descriptions can be read as
different rules for some lists.

**Operational response:** inspect the effective configuration with source
provenance and add a small runtime test for the exact list being governed.

## Telemetry default wording

High-level wording about optional telemetry and field-level descriptions of
categorization defaults are not equally specific.

**Operational response:** treat the field-level installed schema as the starting
point, inspect effective config, and verify emitted behavior before making an
opt-in or opt-out assertion.

## Global configuration path examples

The canonical configuration guide uses platform-specific global locations while
some examples use a historical home-directory shorthand.

**Operational response:** rely on `agency config list --show-source` and the
installed configuration guide for the current platform.

## Local versus hosted plugin policy

Allow, block, and strict-mode controls can have service-side scope that is easy
to overgeneralize to local CLI runs.

**Operational response:** write policy statements with an explicit execution
surface and test local and hosted behavior separately.

## Isolated profiles and remote configuration

Profile-only activation removes the base configuration, while profile-level
`remote_config` is not fetched because remote resolution reads top-level
configuration earlier. Explicit agent and command-line MCP inputs can still
apply.

**Operational response:** declare pinned remote bases at the top level and
review every explicit capability input before calling a profile isolated.

## Identity and attribution terminology

The initiating user, authorization identity, technical job identity, commit
attribution, and pull-request creator are related but not interchangeable.

**Operational response:** document each identity separately in audit and support
material.

## Similar browser-surface naming

Agency documentation can use similar Hub terminology for different browser
experiences.

**Operational response:** qualify the surface by environment and maturity rather
than using "Hub" alone.

## Experimental plugin evals

Plugin-evaluation concepts are documented and supported, but the command family
is explicitly experimental ([F-020](../data/claims.json)).

**Operational response:** pin the Agency release in evidence, run `--help` for
the installed command family (`agency eval-new --help`), and keep deterministic
repository validation separate from model-scored execution.

## Rule for this guide

When documentation and observed behavior differ:

1. record the exact release;
2. preserve command output with private data removed;
3. prefer observable behavior for that release;
4. avoid generalizing it to later versions;
5. submit product feedback through the supported channel;
6. update the claim ledger only when evidence is clear.
