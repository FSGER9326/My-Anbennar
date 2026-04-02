# eu4-encoding-rules

## Purpose
Enforce correct file encoding for EU4 mod files. Encoding errors cause "looks fine in editor, broken in game" failures that are very hard to debug.

## The Rule

| File type | Encoding | BOM |
|---|---|---|
| `localisation/*.yml` or `localisation/*_l_english.yml` | **UTF-8 with BOM** | Yes |
| All other EU4 text/script files | **Windows-1252 (CP-1252)** | No |
| Binary files ( gfx, music, etc.) | Raw binary | N/A |

## Why This Matters

- EU4's localization loader expects UTF-8 BOM for yml files
- Most EU4 script files (missions, events, decisions, triggers) are Windows-1252 / ANSI
- Writing UTF-8 without BOM to a script file causes encoding corruption visible only in-game
- Writing UTF-8 with BOM to a non-loc file can break the parser

## Operational Rules

### Localisation Files
- Path pattern: `localisation/*_l_english.yml`
- Always use UTF-8 with BOM
- Use `ConvertTo-Utf8BOM` helper or write with `-Encoding UTF8` + BOM header
- Example PowerShell write:
```powershell
$bom = [byte[]](0xEF, 0xBB, 0xBF)
$content = Get-Content $path -Raw -Encoding UTF8
[System.IO.File]::WriteAllBytes($path, $bom + [System.Text.Encoding]::UTF8.GetBytes($content))
```

### Script Files
- Extensions: `.txt`, `.yml` (non-loc), `.gui`
- Use Windows-1252 / ANSI
- In PowerShell: `-Encoding Default` or `-Encoding ASCII`
- Never use UTF8 for these files

### Validation

Before any write or after any edit:
1. Check file encoding with: `file --mime-encoding filename` (WSL) or inspect BOM bytes
2. Verify localisation files have UTF-8 BOM (bytes `EF BB BF` at start)
3. Reject files that have wrong encoding

### Quick Encoding Check Commands

```powershell
# Check if file has UTF-8 BOM
$bytes = [System.IO.File]::ReadAllBytes($path)
if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
  "UTF-8 BOM present"
}

# Check for UTF-8 without BOM (wrong for localisation)
if ($bytes[0] -eq 0xEF -and $bytes[1] -ne 0xBB) {
  "Possible UTF-8 without BOM - WRONG for localisation"
}
```

## Common Mistakes

1. Opening a `.yml` loc file in VS Code and saving as UTF-8 without BOM
2. Copy-pasting from a browser (which may inject UTF-8) into a script file
3. Using `Get-Content | Set-Content` which converts to Unicode
4. Git autocrlf converting line endings unexpectedly

## Repo-Specific Notes

- Verne mod uses `localisation/Flavour_Verne_A33_l_english.yml` — UTF-8 BOM required
- Mission/event files are Windows-1252
- Modifier definitions in `common/event_modifiers/` are Windows-1252
