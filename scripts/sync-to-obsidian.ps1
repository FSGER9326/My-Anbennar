#!/usr/bin/env pwsh
# sync-to-obsidian.ps1
# Syncs OpenClaw workspace knowledge to Obsidian vault
# Run via cron: every 30min, isolated session

param(
    [string]$ObsidianVault = "C:\Users\User\Documents\Crab Memory",
    [string]$Workspace = "C:\Users\User\.openclaw\workspace"
)

$ErrorActionPreference = "SilentlyContinue"

function Write-ObsidianNote {
    param($DestPath, $Content, [hashtable]$Frontmatter)
    $fullPath = Join-Path $ObsidianVault $DestPath
    $dir = Split-Path $fullPath -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    $lines = @()
    $lines += "---"
    $lines += "title: $($Frontmatter.title)"
    $lines += "type: $($Frontmatter.type)"
    $lines += "tags: [$($Frontmatter.tags -join ', ')]"
    $lines += "created: $($Frontmatter.created)"
    if ($Frontmatter.related) { $lines += "related: [$($Frontmatter.related -join ', ')]" }
    $lines += "---"
    $lines += ""
    $lines += $Content
    $allContent = $lines -join "`n"
    $allContent | Out-File -FilePath $fullPath -Encoding UTF8
    Write-Host "  [synced] $DestPath"
}

$today = Get-Date -Format "yyyy-MM-dd"
$now   = Get-Date -Format "HH:mm"

# 1. Daily notes
$srcDaily = Join-Path $Workspace "memory\$today.md"
if (Test-Path $srcDaily) {
    $content = Get-Content $srcDaily -Raw
    Write-ObsidianNote "01-Daily/$today.md" $content @{
        title = "OpenClaw $today"
        type = "daily"
        tags = "openclaw, daily"
        created = $today
    }
}

# 2. Learnings (merged)
$learningsSrc = Join-Path $Workspace ".learnings\LEARNINGS.md"
$errorsSrc    = Join-Path $Workspace ".learnings\ERRORS.md"
$featuresSrc = Join-Path $Workspace ".learnings\FEATURE_REQUESTS.md"

$mergedLines = @()
$mergedLines += "# OpenClaw Learnings"
$syncTime = Get-Date -Format "yyyy-MM-dd HH:mm"
$mergedLines += "_Synced from .learnings/ at $syncTime_`n`n"

if (Test-Path $learningsSrc) {
    $mergedLines += "## Lessons"
    $mergedLines += (Get-Content $learningsSrc -Raw)
}
if (Test-Path $errorsSrc) {
    $mergedLines += "`n## Errors"
    $mergedLines += (Get-Content $errorsSrc -Raw)
}
if (Test-Path $featuresSrc) {
    $mergedLines += "`n## Feature Requests"
    $mergedLines += (Get-Content $featuresSrc -Raw)
}

Write-ObsidianNote "05-Learnings/OPENCLAW-LEARNINGS.md" ($mergedLines -join "`n") @{
    title = "OpenClaw Learnings"
    type = "learning"
    tags = "openclaw, learnings, agent"
    created = $today
    related = "[[OPENCLAW.md]]"
}

# 3. Sync addon files to Systems
$addonFiles = @(
    "scripts\mission_truth_audit.py",
    "scripts\legacy_interaction_audit.py",
    "scripts\registry_expand.py",
    "scripts\anbennar-hotspot-explainer.py",
    "schemas\mod-spec.schema.json",
    "openclaw-plugin-anbennar\openclaw.plugin.json"
)

foreach ($relPath in $addonFiles) {
    $src = Join-Path $Workspace $relPath
    $fname = Split-Path $relPath -Leaf
    if (Test-Path $src) {
        $content = Get-Content $src -Raw
        Write-ObsidianNote "06-Systems/My-Anbennar-Addon/$fname" $content @{
            title = $fname
            type = "system"
            tags = "eu4, anbennar, automation, openclaw"
            created = $today
            related = "[[OPENCLAW.md]], [[Verne-Overhaul-MOC]]"
        }
    }
}

# 4. Write addon index
$idxLines = @()
$idxLines += "# My-Anbennar Autonomous Modding Addon"
$idxLines += "_Generated $syncTime_`n"
$idxLines += ""
$idxLines += "## What is this?"
$idxLines += "OpenClaw addon that turns your agent into an autonomous Anbennar/EU4 prose to playable gamefiles system."
$idxLines += ""
$idxLines += "## Components"
$idxLines += "| Component | Purpose |"
$idxLines += "|-----------|---------|"
$idxLines += "| openclaw-plugin-anbennar/ | Sheriff plugin: lane-aware prompt injection + anbennar.* tools |"
$idxLines += "| hooks/anbennar-preflight/ | Session-start preflight: repo_doctor + hotspot validation |"
$idxLines += "| scripts/mission_truth_audit.py | Mission ID graph + loc completeness + cross-file refs |"
$idxLines += "| scripts/legacy_interaction_audit.py | zzz stubs + orphan mission refs + coupling map |"
$idxLines += "| scripts/registry_expand.py | Markdown registry to JSON + fail-on-legacy-edit |"
$idxLines += "| scripts/anbennar-hotspot-explainer.py | Git diff to hotspot intersection report |"
$idxLines += "| schemas/mod-spec.schema.json | JSON Schema for structured mod specs |"
$idxLines += "| eu4-anbennar-autopilot skill | 7-step spec-to-PR loop |"
$idxLines += ""
$idxLines += "## Pre-PR Gate (8 steps)"
$idxLines += "1. Conflict hotspot audit"
$idxLines += "2. Branch overlap check"
$idxLines += "3. Docs conflict guard"
$idxLines += "4. Checklist link audit"
$idxLines += "5. Verne checklist audit"
$idxLines += "6. Country smoke runner"
$idxLines += "7. Registry expand + legacy check"
$idxLines += "8. Mission truth audit (if missions changed)"
$idxLines += ""
$idxLines += "## Quick Start"
$idxLines += '```bash'
$idxLines += 'python scripts/registry_expand.py --registry-md docs/wiki/verne-canonical-vs-legacy-file-registry.md --out automation/registries/verne_file_registry.json --fail-on-legacy-edit-risk'
$idxLines += 'python scripts/mission_truth_audit.py --missions missions/Verne_Missions.txt --loc localisation/verne_overhaul_l_english.yml'
$idxLines += 'bash scripts/pre_pr_gate.sh'
$idxLines += '```'
$idxLines += ""
$idxLines += "## Related"
$idxLines += "- [[OPENCLAW.md]]"
$idxLines += "- [[Verne-Overhaul-MOC]]"

Write-ObsidianNote "06-Systems/My-Anbennar-Addon/INDEX.md" ($idxLines -join "`n") @{
    title = "My-Anbennar Autonomous Addon"
    type = "system"
    tags = "eu4, anbennar, openclaw, addon"
    created = $today
    related = "[[OPENCLAW.md]], [[Verne-Overhaul-MOC]]"
}

Write-Host "[sync-to-obsidian] Done at $now"
