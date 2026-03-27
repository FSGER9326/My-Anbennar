param(
    [string]$Manifest = "docs/repo-maps/checklist-status-manifest.json",
    [string[]]$IndexFile = @(
        "docs/repo-maps/README.md",
        "docs/repo-maps/anbennar-systems-master-index.md",
        "docs/repo-maps/anbennar-systems-scan-roadmap.md"
    ),
    [string[]]$AllowStatus = @("active", "draft", "archived", "needs_revalidation"),
    [switch]$NoSmokeTextRequired
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$manifestPath = Join-Path $root $Manifest
$requireSmokeText = -not $NoSmokeTextRequired
$requiredFields = @("id", "path", "category", "scanned", "mapped", "verified", "automation", "status")

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

if (-not (Test-Path $manifestPath)) {
    Write-Output "ERROR: missing manifest: $manifestPath"
    exit 1
}

$data = Get-Content $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$items = @($data.items)
if ($items.Count -eq 0) {
    Write-Output "ERROR: manifest has no items"
    exit 1
}

$indexFiles = @()
$indexTexts = @()
foreach ($file in $IndexFile) {
    $abs = Join-Path $root $file
    $indexFiles += $abs
    $indexTexts += (Get-Content $abs -Raw -Encoding UTF8)
}

$errors = New-Object System.Collections.Generic.List[string]

foreach ($item in $items) {
    $itemId = if ($null -ne $item.id) { [string]$item.id } else { "<missing-id>" }
    $propertyNames = @($item.PSObject.Properties.Name)

    foreach ($field in $requiredFields) {
        if ($propertyNames -notcontains $field) {
            $errors.Add("${itemId}: missing field '$field'")
        }
    }

    $status = [string]$item.status
    if ($AllowStatus -notcontains $status) {
        $errors.Add("${itemId}: invalid status '$status'")
    }

    if (-not ($item.scanned -is [bool]) -or -not ($item.mapped -is [bool]) -or -not ($item.verified -is [bool])) {
        $errors.Add("${itemId}: scanned/mapped/verified must be booleans")
    }

    $path = [string]$item.path
    if ([string]::IsNullOrWhiteSpace($path)) {
        continue
    }

    $absPath = Join-Path $root $path
    if (-not (Test-Path $absPath)) {
        if ($status -eq "draft") {
            continue
        }
        $errors.Add("${itemId}: missing file '$path'")
        continue
    }

    if ([string]$item.category -eq "repo_map") {
        $filename = [System.IO.Path]::GetFileName($path)
        for ($i = 0; $i -lt $indexFiles.Count; $i++) {
            if ($indexTexts[$i] -notlike "*$filename*") {
                $indexRel = Get-RelativeRepoPath -Root $root -FullPath $indexFiles[$i]
                $errors.Add("${itemId}: '$filename' not found in $indexRel")
            }
        }
    }

    if ($requireSmokeText -and [string]$item.category -eq "repo_map" -and $item.verified -eq $true -and [System.IO.Path]::GetExtension($absPath) -eq ".md") {
        $text = Get-Content $absPath -Raw -Encoding UTF8
        $hasSmoke = $false
        foreach ($phrase in @("Smoke-check", "smoke-check", "Smoke check", "Smoke-test", "smoke-test", "Smoke test")) {
            if ($text.Contains($phrase)) {
                $hasSmoke = $true
                break
            }
        }
        if (-not $hasSmoke) {
            $errors.Add("${itemId}: verified repo-map missing smoke-check section")
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Output "Checklist audit failed:"
    foreach ($error in $errors) {
        Write-Output " - $error"
    }
    exit 1
}

$active = @($items | Where-Object { $_.status -eq "active" }).Count
$verified = @($items | Where-Object { $_.verified -eq $true }).Count
Write-Output "Checklist audit passed: $($items.Count) items, $active active, $verified verified."
