param(
    [Parameter(Mandatory = $true)]
    [string]$Profile
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$profilePath = if ([System.IO.Path]::IsPathRooted($Profile)) { $Profile } else { Join-Path $repoRoot $Profile }

if (-not (Test-Path $profilePath)) {
    throw "Missing smoke profile: $Profile"
}

function Read-Text {
    param([Parameter(Mandatory = $true)][string]$Path)
    return Get-Content $Path -Raw -Encoding UTF8
}

$data = Get-Content $profilePath -Raw -Encoding UTF8 | ConvertFrom-Json
$name = if ($data.name) { [string]$data.name } else { [System.IO.Path]::GetFileNameWithoutExtension($profilePath) }

Write-Output "Running smoke profile: $name"
$errors = New-Object System.Collections.Generic.List[string]
$step = 0

foreach ($item in @($data.require_patterns)) {
    $step += 1
    $desc = [string]$item.description
    $regex = New-Object System.Text.RegularExpressions.Regex($item.pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
    $matched = $false

    Write-Output "[$step] require: $desc"
    foreach ($pathRel in @($item.paths)) {
        $path = Join-Path $repoRoot ([string]$pathRel)
        if (-not (Test-Path $path)) {
            $errors.Add("require '$desc': missing file $pathRel")
            continue
        }

        if ($regex.IsMatch((Read-Text -Path $path))) {
            $matched = $true
        }
    }

    if (-not $matched) {
        $errors.Add("require '$desc': pattern not found in any listed file")
    }
}

foreach ($item in @($data.forbid_patterns)) {
    $step += 1
    $desc = [string]$item.description
    $regex = New-Object System.Text.RegularExpressions.Regex($item.pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)

    Write-Output "[$step] forbid: $desc"
    foreach ($pathRel in @($item.paths)) {
        $path = Join-Path $repoRoot ([string]$pathRel)
        if (-not (Test-Path $path)) {
            $errors.Add("forbid '$desc': missing file $pathRel")
            continue
        }

        if ($regex.IsMatch((Read-Text -Path $path))) {
            $errors.Add("forbid '$desc': forbidden pattern found in $pathRel")
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Output "Smoke profile failed:"
    foreach ($error in $errors) {
        Write-Output " - $error"
    }
    throw "Smoke profile failed."
}

Write-Output "Smoke profile passed."
