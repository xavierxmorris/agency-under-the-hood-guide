#requires -Version 7.0
[CmdletBinding()]
param(
    [switch]$Check,
    [switch]$Probe,
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    & python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 2)"
    if ($LASTEXITCODE -ne 0) {
        throw 'Python 3.11+ is required.'
    }

    if ($Probe) {
        & (Join-Path 'scripts' 'capture-agency-surface.ps1')
        if ($LASTEXITCODE -ne 0) {
            throw 'Agency surface probe failed.'
        }
    }

    if ($Check -or $Probe) {
        & python (Join-Path 'scripts' 'generate_site.py') --check
    } else {
        & python (Join-Path 'scripts' 'generate_site.py')
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'Generated site validation failed.'
    }

    & python (Join-Path 'scripts' 'validate.py')
    if ($LASTEXITCODE -ne 0) {
        throw 'Repository validation failed.'
    }

    & python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) {
        throw 'Unit tests failed.'
    }

    Write-Host 'All repository checks passed.' -ForegroundColor Green

    if (-not $Check -and -not $NoBrowser) {
        $site = (Resolve-Path -LiteralPath (Join-Path 'site' 'index.html')).Path
        Start-Process -FilePath $site | Out-Null
    }
} finally {
    Pop-Location
}
