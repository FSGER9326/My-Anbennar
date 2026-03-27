$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

function Assert-Pattern {
    param(
        [Parameter(Mandatory = $true)][string]$Pattern,
        [Parameter(Mandatory = $true)][string[]]$Paths,
        [Parameter(Mandatory = $true)][string]$ErrorMessage
    )

    $matched = $false
    foreach ($path in $Paths) {
        if (-not (Test-Path $path)) {
            continue
        }

        if (Select-String -Path $path -Pattern $Pattern -Quiet) {
            $matched = $true
            break
        }
    }

    if (-not $matched) {
        throw $ErrorMessage
    }
}

function Assert-NoPattern {
    param(
        [Parameter(Mandatory = $true)][string]$Pattern,
        [Parameter(Mandatory = $true)][string[]]$Paths,
        [Parameter(Mandatory = $true)][string]$ErrorMessage
    )

    foreach ($path in $Paths) {
        if (-not (Test-Path $path)) {
            continue
        }

        if (Select-String -Path $path -Pattern $Pattern -Quiet) {
            throw $ErrorMessage
        }
    }
}

Write-Output "[1/9] Check helper definitions exist"
Assert-Pattern `
    -Pattern "verne_overhaul_enable_adventure_network_tier_1|verne_overhaul_apply_regatta_spire_swap|verne_overhaul_laments_regatta_anchor_state_ready|verne_overhaul_akasik_access_ready" `
    -Paths @(
        "common/scripted_effects/verne_overhaul_effects.txt",
        "common/scripted_triggers/verne_overhaul_triggers.txt"
    ) `
    -ErrorMessage "Missing one or more Verne overhaul helper definitions."

Write-Output "[2/9] Check live call sites use helpers"
Assert-Pattern -Pattern "verne_overhaul_enable_adventure_network_tier_1" -Paths @("missions/Verne_Missions.txt") -ErrorMessage "Mission file is missing network-init helper call."
Assert-Pattern -Pattern "verne_overhaul_apply_regatta_spire_swap" -Paths @("events/Flavour_Verne_A33.txt") -ErrorMessage "Event file is missing monument-swap helper call."
Assert-Pattern -Pattern "verne_overhaul_laments_regatta_anchor_state_ready" -Paths @("missions/Verne_Missions.txt") -ErrorMessage "Mission file is missing Regatta anchor trigger helper call."
Assert-Pattern -Pattern "verne_overhaul_akasik_access_ready" -Paths @("missions/Verne_Missions.txt") -ErrorMessage "Mission file is missing Akasik access trigger helper call."

Write-Output "[3/9] Check helper still sets Port-of-Adventure unlock flag"
Assert-Pattern `
    -Pattern "set_country_flag\s*=\s*verne_unlock_port_of_adventure_button" `
    -Paths @("common/scripted_effects/verne_overhaul_effects.txt") `
    -ErrorMessage "Adventure-network helper no longer sets the Port-of-Adventure unlock flag."

Write-Output "[4/9] Check monument anchor IDs still exist"
Assert-Pattern `
    -Pattern "^kazakesh\s*=|^aur_kes_akasik\s*=|^kazakesh_stingport\s*=" `
    -Paths @(
        "common/great_projects/anb_monuments_sarhal.txt",
        "common/great_projects/anb_monuments_missions.txt"
    ) `
    -ErrorMessage "One or more monument anchor IDs are missing."

Write-Output "[5/9] Ensure no stale inline duplicate logic remains in mission/event call sites"
Assert-NoPattern `
    -Pattern "destroy_great_project|add_great_project|set_country_flag\s*=\s*verne_unlock_port_of_adventure_button|name\s*=\s*`"verne_network_of_adventure_tier_1`"" `
    -Paths @(
        "missions/Verne_Missions.txt",
        "events/Flavour_Verne_A33.txt"
    ) `
    -ErrorMessage "ERROR: stale inline logic found in mission/event call sites (should be in helper files)."

Write-Output "[6/9] Ensure key Verne repo-map docs are indexed"
foreach ($filename in @(
    "verne-monument-object-id-parity-check-reference.md",
    "verne-adventure-chain-mission-event-localization-parity-reference.md",
    "verne-cross-nation-mission-interaction-watchlist.md"
)) {
    Assert-Pattern `
        -Pattern $([regex]::Escape($filename)) `
        -Paths @(
            "docs/repo-maps/README.md",
            "docs/repo-maps/anbennar-systems-master-index.md",
            "docs/repo-maps/anbennar-systems-scan-roadmap.md"
        ) `
        -ErrorMessage "Indexed repo-map doc missing from required indexes: $filename"
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Output "[7/9] Run checklist status audit"
& (Join-Path $scriptDir "verne_checklist_audit.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "[8/9] Run checklist markdown link audit"
& (Join-Path $scriptDir "checklist_link_audit.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "[9/9] Run docs conflict guard"
& (Join-Path $scriptDir "docs_conflict_guard.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "All Verne smoke checks passed."
