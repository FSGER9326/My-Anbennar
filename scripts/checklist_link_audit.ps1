$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$targetDirs = @(
    (Join-Path $root "docs/repo-maps"),
    (Join-Path $root "docs/wiki"),
    (Join-Path $root "docs/theorycrafting")
)
$linkRegex = [regex]"\[[^\]]+\]\((\.?\.?/[^)]+\.md)\)"

$errors = New-Object System.Collections.Generic.List[string]
$checked = 0

foreach ($base in $targetDirs) {
    if (-not (Test-Path $base)) {
        continue
    }

    Get-ChildItem $base -Recurse -File -Filter *.md | ForEach-Object {
        $md = $_
        $text = Get-Content $md.FullName -Raw -Encoding UTF8
        foreach ($match in $linkRegex.Matches($text)) {
            $checked++
            $rel = $match.Groups[1].Value
            $target = [System.IO.Path]::GetFullPath((Join-Path $md.DirectoryName $rel))
            if (-not (Test-Path $target)) {
                $relMd = [System.IO.Path]::GetRelativePath($root, $md.FullName)
                $errors.Add("$relMd -> missing link target: $rel")
            }
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Output "Checklist link audit failed:"
    foreach ($error in $errors) {
        Write-Output " - $error"
    }
    exit 1
}

Write-Output "Checklist link audit passed: $checked local markdown links checked."
