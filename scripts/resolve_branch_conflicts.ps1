#!/usr/bin/env pwsh
[CmdletBinding()]
param(
    [string]$BaseRef = "origin/main",
    [switch]$SkipMissingBase,
    [switch]$NoFetch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

if (git status --porcelain) {
    Write-Error "Working tree is dirty. Commit/stash first."
}

$branch = (git branch --show-current).Trim()
if ([string]::IsNullOrWhiteSpace($branch) -or $branch -eq "main") {
    Write-Error "Run this from a non-main feature branch."
}

$baseExists = $true
try {
    git rev-parse --verify $BaseRef | Out-Null
} catch {
    $baseExists = $false
}

if (-not $baseExists -and -not $NoFetch) {
    try {
        git remote get-url origin | Out-Null
        Write-Output "Fetching origin before conflict resolution..."
        git fetch origin | Out-Null
    } catch {
        # ignore missing origin
    }
}

$baseExists = $true
try {
    git rev-parse --verify $BaseRef | Out-Null
} catch {
    $baseExists = $false
}

if (-not $baseExists) {
    if ($SkipMissingBase) {
        Write-Output "Skip: Base ref '$BaseRef' is unavailable in this clone."
        exit 0
    }
    Write-Error "Base ref '$BaseRef' is unavailable. Pass explicit base (e.g. upstream/main)."
}

Write-Output "Merging $BaseRef into $branch (no auto-commit yet)..."
$mergeOutput = $null
$mergeOutput = git merge --no-ff --no-commit $BaseRef 2>&1
$mergeCode = $LASTEXITCODE

if ($mergeCode -eq 0) {
    $staged = (git diff --cached --name-only)
    if ($staged) {
        git commit -m "Merge $BaseRef into $branch" | Out-Null
        Write-Output "Merge completed with commit."
    } else {
        Write-Output "Already up to date; no merge commit needed."
        git merge --abort 2>$null | Out-Null
    }
    exit 0
}

Write-Output "Merge reported conflicts. Running auto-resolvers..."
python scripts/resolve_docs_conflicts.py 2>$null | Out-Null
python scripts/resolve_content_conflicts.py 2>$null | Out-Null

$unmerged = git diff --name-only --diff-filter=U
if ($unmerged) {
    Write-Error "Unresolved conflicts remain:`n$($unmerged -join "`n")`nResolve manually, then git add <files> && git commit"
}

git commit -m "Merge $BaseRef into $branch (auto-resolved hotspots)" | Out-Null
Write-Output "Merge conflicts resolved and merge commit created."
