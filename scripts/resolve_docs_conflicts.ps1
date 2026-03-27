$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

$hotspots = @(
    ".gitattributes",
    "docs/README.md",
    "docs/start-here.md",
    "docs/implementation-crosswalk.md",
    "docs/references/README.md",
    "docs/references/reference-index.md",
    "docs/repo-maps/README.md",
    "docs/repo-maps/anbennar-vs-eu4-mechanics-gap-register.md",
    "docs/repo-maps/anbennar-systems-master-index.md",
    "docs/repo-maps/anbennar-systems-scan-roadmap.md",
    "docs/wiki/checklist-automation-system.md"
)

$canonicalGitattributes = @'
# Normalize repository text files consistently.
* text=auto

# Keep docs, automation, and workflow files on LF so merges stay predictable
# across desktop Codex, cloud Codex, GitHub, and local Windows tooling.
.gitattributes text eol=lf
automation/** text eol=lf
docs/** text eol=lf
scripts/** text eol=lf
.github/workflows/** text eol=lf

# Prefer additive auto-merge in documentation hotspot files to reduce manual
# conflict resolution in shared indexes and hub docs.
docs/README.md merge=union
docs/start-here.md merge=union
docs/implementation-crosswalk.md merge=union
docs/references/README.md merge=union
docs/references/reference-index.md merge=union
docs/repo-maps/README.md merge=union
docs/repo-maps/anbennar-vs-eu4-mechanics-gap-register.md merge=union
docs/repo-maps/anbennar-systems-master-index.md merge=union
docs/repo-maps/anbennar-systems-scan-roadmap.md merge=union
docs/wiki/checklist-automation-system.md merge=union
'@

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & git @Arguments 2>&1
        $code = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousPreference
    }
    [pscustomobject]@{
        Code = $code
        Output = @($output) -join "`n"
    }
}

function Get-UnmergedFiles {
    $result = Invoke-Git -Arguments @("diff", "--name-only", "--diff-filter=U")
    if ($result.Code -ne 0) {
        if (-not [string]::IsNullOrWhiteSpace($result.Output)) {
            Write-Error $result.Output
        }
        return @()
    }

    return @(
        $result.Output -split "`r?`n" |
        Where-Object {
            -not [string]::IsNullOrWhiteSpace($_) -and
            $_ -notmatch '^\s*warning:'
        }
    )
}

function Get-StageText {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][int]$Stage
    )

    $result = Invoke-Git -Arguments @("show", ":$Stage`:$Path")
    if ($result.Code -ne 0) {
        return ""
    }

    return $result.Output
}

function Dedupe-ConsecutiveLines {
    param(
        [Parameter(Mandatory = $true)][string]$Text
    )

    $out = New-Object System.Collections.Generic.List[string]
    foreach ($line in ($Text -split "`r?`n")) {
        if ($out.Count -gt 0 -and $out[$out.Count - 1] -eq $line) {
            continue
        }
        $out.Add($line)
    }

    return (($out -join "`n").TrimEnd("`r", "`n") + "`n")
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Resolve-File {
    param(
        [Parameter(Mandatory = $true)][string]$Path
    )

    if ($Path -eq ".gitattributes") {
        Write-Utf8NoBom -Path (Join-Path $repoRoot $Path) -Content $canonicalGitattributes
        $add = Invoke-Git -Arguments @("add", $Path)
        return ($add.Code -eq 0)
    }

    $ours = Get-StageText -Path $Path -Stage 2
    $theirs = Get-StageText -Path $Path -Stage 3
    if ([string]::IsNullOrEmpty($ours) -and [string]::IsNullOrEmpty($theirs)) {
        return $false
    }

    $merged = Dedupe-ConsecutiveLines -Text (($ours.TrimEnd("`r", "`n")) + "`n`n" + ($theirs.TrimEnd("`r", "`n")) + "`n")
    Write-Utf8NoBom -Path (Join-Path $repoRoot $Path) -Content $merged

    $add = Invoke-Git -Arguments @("add", $Path)
    return ($add.Code -eq 0)
}

$unmerged = Get-UnmergedFiles
if ($unmerged.Count -eq 0) {
    Write-Output "No unmerged files found."
    return
}

$target = @($unmerged | Where-Object { $hotspots -contains $_ })
$skipped = @($unmerged | Where-Object { $hotspots -notcontains $_ })

if ($skipped.Count -gt 0) {
    Write-Output "Skipped non-hotspot conflicts (manual resolution required):"
    foreach ($file in $skipped) {
        Write-Output "- $file"
    }
}

$resolved = New-Object System.Collections.Generic.List[string]
foreach ($path in $target) {
    if (Resolve-File -Path $path) {
        $resolved.Add($path)
    }
}

if ($resolved.Count -gt 0) {
    Write-Output "Auto-resolved hotspot files:"
    foreach ($file in $resolved) {
        Write-Output "- $file"
    }
}

$remaining = Get-UnmergedFiles
if ($remaining.Count -gt 0) {
    Write-Output "Remaining unresolved files:"
    foreach ($file in $remaining) {
        Write-Output "- $file"
    }
    throw "Some merge conflicts remain after hotspot auto-resolution."
}

Write-Output "All hotspot conflicts resolved."
