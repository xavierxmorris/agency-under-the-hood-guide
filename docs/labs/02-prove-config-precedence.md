# Lab 2: Prove configuration precedence

## Objective

Observe global and local precedence with source provenance, without reading or
changing real Agency configuration. The lab refuses to run when its temporary
directory has an ancestor Agency config.

Claims: F-003, F-004, F-005, I-003, R-001.

## Prerequisites

- Agency installed and available on `PATH`
- PowerShell 7

## Build an isolated sandbox

```powershell
function Assert-NoAncestorAgencyConfig {
    param([Parameter(Mandatory)][string]$StartDirectory)

    $current = [System.IO.DirectoryInfo]::new(
        [System.IO.Path]::GetFullPath($StartDirectory)
    )
    while ($current) {
        foreach ($name in @('agency.toml', 'agency.yaml', 'agency.yml')) {
            $candidate = Join-Path $current.FullName $name
            if (Test-Path -LiteralPath $candidate) {
                throw "Ancestor Agency config found: $candidate"
            }
        }
        $current = $current.Parent
    }
}

$lab = Join-Path ([System.IO.Path]::GetTempPath()) "agency-config-lab-$([guid]::NewGuid().ToString('N'))"
Assert-NoAncestorAgencyConfig -StartDirectory (Split-Path $lab -Parent)
$global = Join-Path $lab 'global'
$work = Join-Path $lab 'work'
New-Item -ItemType Directory -Path $global, $work -Force | Out-Null

@'
[mcps.builtins]
ado = false
'@ | Set-Content -LiteralPath (Join-Path $global 'agency.toml') -Encoding utf8NoBOM

@'
[mcps.builtins]
ado = true

[profiles.isolated.mcps.builtins]
ado = false
'@ | Set-Content -LiteralPath (Join-Path $work 'agency.toml') -Encoding utf8NoBOM
```

## Inspect effective values

```powershell
$previous = $env:AGENCY_GLOBAL_CONFIG_PATH
try {
    $env:AGENCY_GLOBAL_CONFIG_PATH = $global
    Push-Location $work
    agency config check --skip-remotes
    agency config list --show-source
    agency config profiles --json
} finally {
    Pop-Location
    $env:AGENCY_GLOBAL_CONFIG_PATH = $previous
}
```

## Questions

1. Which file supplies the effective `ado` value?
2. Does the source annotation match the expected local override?
3. Which profile is discoverable?
4. Why would `--profile-only isolated` be more reproducible than a normal
   overlay for a tightly controlled workflow?
5. Which additional inputs would you pin before using a remote config?

## Success criteria

- Configuration validation passes.
- Source provenance shows the local file overriding the isolated global file.
- The ancestor preflight found no other Agency config.
- No real global or ancestor config is read or modified.
- You can explain why the configuration model is a merge graph.

## Cleanup

```powershell
Remove-Item -LiteralPath $lab -Recurse -Force
```
