$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

$hotspotFiles = @(
    "docs/README.md",
    "docs/implementation-crosswalk.md",
    "docs/references/README.md",
    "docs/references/reference-index.md",
    "docs/repo-maps/README.md",
    "docs/repo-maps/anbennar-systems-master-index.md",
    "docs/repo-maps/anbennar-systems-scan-roadmap.md"
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
}

$failed = $false

foreach ($relPath in $hotspotFiles) {
    $path = Join-Path $repoRoot $relPath
    if (-not (Test-Path $path)) {
        Write-Output "ERROR: missing hotspot file: $relPath"
        $failed = $true
        continue
    }

    $text = Get-Content $path -Raw -Encoding UTF8

    foreach ($marker in @("<<<<<<<", "=======", ">>>>>>>")) {
        if ($text.Contains($marker)) {
            Write-Output "ERROR: merge conflict marker '$marker' found in $relPath"
            $failed = $true
        }
    }

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
