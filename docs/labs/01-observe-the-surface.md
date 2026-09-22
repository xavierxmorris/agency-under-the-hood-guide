# Lab 1: Observe the installed surface

## Objective

Capture the installed Agency command surface without reading real user
configuration, then classify what belongs to Agency and what belongs to the
selected engine.

Claims: F-001, F-002, F-016, F-017, I-001.

## Prerequisites

- Agency installed and available on `PATH`
- PowerShell 7
- Python 3.11+

## Run

From the repository root:

```powershell
.\go.ps1 -Probe -NoBrowser
```

The probe captures:

- Agency version;
- top-level help;
- Copilot and Claude adapter help;
- configuration and plugin help;
- batch-run help;
- an isolated synthetic configuration check.

It deliberately does not capture real configuration, plugin lists, tokens, or
environment values. Local paths are redacted.

## Inspect

Open `.artifacts\agency-surface\summary.json` and the generated text files.

Classify each command:

| Command or option | Agency control | Engine runtime | External system |
| --- | --- | --- | --- |
| configuration/profile option |  |  |  |
| model or conversation option |  |  |  |
| plugin acquisition option |  |  |  |
| MCP service option |  |  |  |
| hosted job command |  |  |  |

More than one column can participate, but identify the primary owner.

## Success criteria

- The captured version is explicit.
- No real configuration or private endpoint appears.
- You can explain why model conversation belongs to the engine while plugin and
  configuration resolution belong to Agency.
- You can identify at least one surface whose workflow differs while sharing the
  same Agency foundation.

## Cleanup

```powershell
Remove-Item -LiteralPath .artifacts\agency-surface -Recurse -Force
```
