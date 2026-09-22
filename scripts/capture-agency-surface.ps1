#requires -Version 7.0
[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\.artifacts\agency-surface')
)

$ErrorActionPreference = 'Stop'
$outputRoot = [System.IO.Path]::GetFullPath($OutputDirectory)
$agency = Get-Command agency -ErrorAction SilentlyContinue
if (-not $agency) {
    throw 'Agency CLI was not found on PATH.'
}

New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null

function Assert-NoAncestorAgencyConfig {
    param([Parameter(Mandatory)][string]$StartDirectory)

    $current = [System.IO.DirectoryInfo]::new([System.IO.Path]::GetFullPath($StartDirectory))
    while ($current) {
        foreach ($name in @('agency.toml', 'agency.yaml', 'agency.yml')) {
            $candidate = Join-Path $current.FullName $name
            if (Test-Path -LiteralPath $candidate) {
                throw "Cannot prove configuration isolation because an ancestor Agency config exists: $candidate"
            }
        }
        $current = $current.Parent
    }
}

function Remove-LocalPaths {
    param([string]$Text)

    $result = $Text
    foreach ($path in @($HOME, $env:LOCALAPPDATA, $env:APPDATA)) {
        if ($path) {
            $result = $result -replace [regex]::Escape($path), '<LOCAL_PATH>'
        }
    }
    return $result
}

$sandbox = Join-Path ([System.IO.Path]::GetTempPath()) "agency-surface-$([guid]::NewGuid().ToString('N'))"
$globalConfig = Join-Path $sandbox 'global'
$workingDirectory = Join-Path $sandbox 'work'
Assert-NoAncestorAgencyConfig -StartDirectory (Split-Path $sandbox -Parent)
New-Item -ItemType Directory -Path $globalConfig, $workingDirectory -Force | Out-Null

$configText = @'
[profiles.learning.mcps.builtins]
ado = false
'@
[System.IO.File]::WriteAllText(
    (Join-Path $globalConfig 'agency.toml'),
    $configText,
    [System.Text.UTF8Encoding]::new($false)
)

$commands = @(
    @{ Name = 'version'; Arguments = @('--version') },
    @{ Name = 'top-level-help'; Arguments = @('--help') },
    @{ Name = 'copilot-help'; Arguments = @('copilot', '--help') },
    @{ Name = 'claude-help'; Arguments = @('claude', '--help') },
    @{ Name = 'config-help'; Arguments = @('config', '--help') },
    @{ Name = 'plugin-help'; Arguments = @('plugin', '--help') },
    @{ Name = 'batch-help'; Arguments = @('eval', '--help') }
)

$previousConfigPath = $env:AGENCY_GLOBAL_CONFIG_PATH
try {
    $env:AGENCY_GLOBAL_CONFIG_PATH = $globalConfig
    Push-Location $workingDirectory
    $results = foreach ($command in $commands) {
        $text = (& agency @($command.Arguments) 2>&1 | Out-String)
        if ($LASTEXITCODE -ne 0) {
            throw "agency $($command.Arguments -join ' ') failed."
        }

        $safeText = Remove-LocalPaths $text
        $safeText = $safeText -replace [regex]::Escape($sandbox), '<ISOLATED_SANDBOX>'
        $target = Join-Path $outputRoot "$($command.Name).txt"
        [System.IO.File]::WriteAllText($target, $safeText, [System.Text.UTF8Encoding]::new($false))
        [pscustomobject]@{
            name = $command.Name
            arguments = $command.Arguments
            file = [System.IO.Path]::GetFileName($target)
        }
    }

    $configCheck = (& agency config check --skip-remotes 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) {
        throw 'Isolated Agency config validation failed.'
    }
    [System.IO.File]::WriteAllText(
        (Join-Path $outputRoot 'isolated-config-check.txt'),
        (Remove-LocalPaths $configCheck),
        [System.Text.UTF8Encoding]::new($false)
    )
} finally {
    Pop-Location
    $env:AGENCY_GLOBAL_CONFIG_PATH = $previousConfigPath
    if (Test-Path -LiteralPath $sandbox) {
        Remove-Item -LiteralPath $sandbox -Recurse -Force
    }
}

$summary = [ordered]@{
    capturedAtUtc = [DateTimeOffset]::UtcNow.ToString('O')
    safety = 'Help and version surfaces only; ancestor config absence was verified before an isolated synthetic config check.'
    commands = $results
}
$summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outputRoot 'summary.json') -Encoding utf8NoBOM
Write-Host "Safe Agency surface captured at $outputRoot" -ForegroundColor Green
