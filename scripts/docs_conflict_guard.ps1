$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

$hotspotFiles = @(
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

$headingSingletonRules = @{
    "docs/README.md" = @(
        "### Repo grounding maps",
        "### Local references",
        "### Maintenance wiki"
    )
    "docs/repo-maps/README.md" = @(
        "Core indexes:"
    )
    "docs/start-here.md" = @(
        "## Tiny glossary (modding terms, not GitHub terms)",
        "## What should we do right now? (Decision guide)"
    )
    "docs/repo-maps/anbennar-vs-eu4-mechanics-gap-register.md" = @(
        "## High-value gap queue"
    )
    "docs/wiki/checklist-automation-system.md" = @(
        "## Automation commands",
        "## Merge-conflict prevention (docs hotspots)"
    )
}

$failed = $false

function Get-RelativeRepoPath {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$FullPath
    )

    if ($FullPath.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $FullPath.Substring($Root.Length).TrimStart('\', '/').Replace('\', '/')
    }

    return $FullPath.Replace('\', '/')
}

$allDocs = Get-ChildItem -Path (Join-Path $repoRoot "docs") -Recurse -Filter *.md
foreach ($doc in $allDocs) {
    $relDocPath = Get-RelativeRepoPath -Root $repoRoot -FullPath $doc.FullName
    $text = Get-Content $doc.FullName -Raw -Encoding UTF8

    foreach ($marker in @("<<<<<<<", "=======", ">>>>>>>")) {
        if ($text -match "(?m)^$([regex]::Escape($marker))") {
            Write-Output "ERROR: merge conflict marker '$marker' found in $relDocPath"
            $failed = $true
        }
    }
}

foreach ($relPath in $hotspotFiles) {
    $path = Join-Path $repoRoot $relPath
    if (-not (Test-Path $path)) {
        Write-Output "ERROR: missing hotspot file: $relPath"
        $failed = $true
        continue
    }

    $text = Get-Content $path -Raw -Encoding UTF8

    if ($headingSingletonRules.ContainsKey($relPath)) {
        foreach ($heading in $headingSingletonRules[$relPath]) {
            $count = ([regex]::Matches($text, [regex]::Escape($heading))).Count
            if ($count -ne 1) {
                Write-Output "ERROR: heading '$heading' appears $count times in $relPath (expected exactly 1)"
                $failed = $true
            }
        }
    }
}

if ($failed) {
    Write-Output ""
    Write-Output "How to fix quickly:"
    Write-Output "1) Keep both sides only when both add unique content."
    Write-Output "2) Remove duplicate repeated sections in docs index files."
    Write-Output "3) Re-run: powershell -ExecutionPolicy Bypass -File .\scripts\docs_conflict_guard.ps1"
    exit 1
}

Write-Output "Docs conflict guard passed."
