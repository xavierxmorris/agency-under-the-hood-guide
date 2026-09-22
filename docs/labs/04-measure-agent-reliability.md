# Lab 4: Measure agent reliability

## Objective

Design a batch that measures success rate across repeated runs instead of hiding
flakiness behind retries.

Claims: F-010, F-013, R-003, R-004.

## Prerequisites

- Agency installed and configured
- A custom agent you are authorized to evaluate
- A valid model name for the selected engine
- Python 3.11+ for the synthetic preparation and validation scripts

## Start from the examples

- [`examples/batch/batch.csv`](../../examples/batch/batch.csv)
- [`examples/batch/eval-config.yaml`](../../examples/batch/eval-config.yaml)

Replace `agent-under-test`, `MODEL_PLACEHOLDER`, and the synthetic prompts with
an agent, installed model, and scenarios you are authorized to run.

Run from the example directory so the relative fixture and validation paths are
stable:

```powershell
Push-Location examples\batch
try {
    agency eval --config .\eval-config.yaml
} finally {
    Pop-Location
}
```

## Experiment design

Run two comparisons:

1. **Reliability:** five iterations, one attempt.
2. **Recovery:** five iterations, up to three attempts.

The first estimates first-try success. The second measures whether retry can
recover. Do not combine the two into one success percentage.

## Validation

Prefer deterministic pass/fail checks:

- expected exit code;
- expected file;
- script validation;
- build or test gate.

Avoid a pass condition based only on the agent saying it succeeded.

## Metrics

Capture:

- first-attempt success rate;
- eventual success rate;
- average attempts per successful iteration;
- failure category;
- validation duration;
- human interventions.

## Success criteria

- Iterations and attempts answer different questions.
- The dataset remains fixed between compared runs.
- Validation is independent of the agent's own conclusion.
- Failures are categorized rather than collapsed into one count.

## Cleanup

```powershell
Remove-Item -LiteralPath .artifacts\batch -Recurse -Force
```
