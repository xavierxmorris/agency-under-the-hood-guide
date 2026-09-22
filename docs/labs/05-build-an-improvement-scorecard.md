# Lab 5: Build an improvement scorecard

## Objective

Measure whether a repository helps agents produce faster, verifiable work without
trading away quality.

Claims: F-014, F-015, I-006, R-006, R-008.

## Prerequisites

- A repository and representative workflow you are authorized to assess
- Access to its documented local and CI validation commands
- A small baseline of comparable tasks and outcome data

## Start from the template

Copy [`data/scorecard.template.json`](../../data/scorecard.template.json) and
score one repository from 0 through 4 across:

1. verification readiness;
2. repository understandability;
3. automation readiness;
4. agent operability;
5. outcome effectiveness.

Use [`examples/scorecard/sample-scorecard.json`](../../examples/scorecard/sample-scorecard.json)
as a synthetic example.

## Evidence rule

Do not award a score for file presence alone. Run the probe:

- clean restore, build, and test;
- locate ownership and dependencies;
- execute the CI-equivalent workflow;
- recover from a representative failure;
- compare outcomes with a baseline.

## Pair metrics

Every speed or adoption measure needs a quality partner:

| Speed or adoption | Quality partner |
| --- | --- |
| Cycle time | Defect and escape rate |
| Agent sessions | Verification success rate |
| Job completion | Accepted outcome rate |
| Plugin availability | Component use and task success |
| Autonomous duration | Human intervention and recovery rate |

## Choose one durable improvement

From the lowest-scoring dimension, convert one observed problem into:

1. a deterministic check;
2. a regression test;
3. an eval;
4. a runtime policy;
5. guidance only if stronger mechanisms are not practical.

## Success criteria

- Every score has observed evidence.
- Speed and quality are measured together.
- At least one improvement has an owner and a deterministic acceptance condition.
- The next assessment date is explicit.

## Cleanup

If you created the working copy under `.artifacts`, remove it:

```powershell
Remove-Item -LiteralPath .artifacts\scorecard.json -Force
```

Otherwise move the approved result into the repository's normal evidence
location. Do not commit raw telemetry exports or user-level data.
