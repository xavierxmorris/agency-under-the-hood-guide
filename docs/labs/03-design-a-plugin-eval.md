# Lab 3: Design a plugin eval

## Objective

Design a capability-quality suite that tests routing and behavior without leaking
the answer into user prompts.

Claims: F-010, F-011, F-012, F-020, R-004.

## Prerequisites

- An Agency plugin, skill, or custom agent you own
- The installed plugin-evaluation command family and a configured harness
- A synthetic or approved test workspace

## Pick one capability

Choose a plugin, skill, or custom agent you own. Write one sentence describing
the user outcome, not the implementation:

```text
When a user supplies a deployment log, the capability identifies the failing
stage and produces a concise handoff with evidence.
```

## Build the scenario matrix

| Scenario | User-shaped prompt | Expected behavior | Type |
| --- | --- | --- | --- |
| 1 |  |  | happy |
| 2 |  |  | happy |
| 3 |  |  | happy |
| 4 |  |  | edge |
| 5 |  |  | negative |

Rules:

- Do not name the expected tool in the prompt.
- Do not include answer keywords or rubric text in the prompt.
- Seed a synthetic fixture when the task needs files.
- Keep every task independent.
- The negative case should prove the capability does not fire indiscriminately.

## Choose a harness

Use the container-based harness for third-party or untrusted tasks. Use a host
harness only for tasks you trust with your local account.

## Validate the design

For an existing plugin and the installed release:

```text
agency eval-new doctor --plugin . --strict
agency eval-new generate --plugin . --out .artifacts/generated-evals
```

The command family is experimental. Confirm the installed help before relying on
specific flags with `agency eval-new --help`.

## Success criteria

- At least five scenarios exist.
- One scenario is negative.
- Prompts sound like users, not test specifications.
- Grading information is separate from prompts.
- Harness choice is justified by the trust boundary.

## Advanced companion

Use the complete
[Agency plugin eval workshop](https://github.com/xavierxmorris/ghcp-demo-17-agency-plugin-evals)
for skill, MCP, and custom-agent examples.

## Cleanup

```powershell
Remove-Item -LiteralPath .artifacts\generated-evals -Recurse -Force
```
