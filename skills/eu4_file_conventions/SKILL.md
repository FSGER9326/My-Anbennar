# eu4_file_conventions

## Purpose
Teach EU4 mod file structure, folder layout, encoding rules, and the "never freestyle" principle. This is the most foundational skill — breaking these rules produces broken mods that may not even launch.

## File Layout Rule

**Never invent file placement.** EU4 resolves mods by directory structure. If you create a file in the wrong folder, EU4 silently ignores it.

### Core Folder Map

| Folder | What goes here | Encoding |
|---|---|---|
| `common/` | Country tags, idea groups, government reforms, modifiers, trade companies, religions, cultures | Windows-1252 |
| `decisions/` | Decision files (`.txt`) | Windows-1252 |
| `events/` | Event files (`.txt`) | Windows-1252 |
| `gfx/` | Flags (`.tga`), interfaces, loadingscreens | Binary |
| `history/` | `countries/*.txt` — per-country history | Windows-1252 |
| `interface/` | `.gui` files | Windows-1252 |
| `localisation/` | `*_l_english.yml` — localisation | **UTF-8 with BOM** |
| `localisation/replace/` | Replacement loc (filename must end `_l_english.yml`) | **UTF-8 with BOM** |
| `map/` | Terrain, provinces, positions, trade nodes | Binary + Windows-1252 |
| `missions/` | Mission trees | Windows-1252 |
| `music/` | Music files | Binary |
| `sound/` | Sound definitions | Windows-1252 |
| `textures/` | Map textures | Binary |

### Mod Descriptor (`.mod` file)

Every mod needs a descriptor at the root:

```
name="My Submod"
version="1.0.0"
tags={
    "Gameplay"
    "UI"
}
picture="thumbnail.png"
supported_version="1.37.5"
```

The `.mod` file name must match the folder name. The descriptor must specify `supported_version`.

## Encoding Rules (Critical)

| File type | Encoding | BOM |
|---|---|---|
| `localisation/*.yml` | **UTF-8** | **YES — required** |
| `localisation/replace/*.yml` | **UTF-8** | **YES — required** |
| All `.txt` script files | **Windows-1252 (CP-1252)** | **NO — never** |
| `.gui` files | **Windows-1252** | **NO** |
| Binary (gfx, tga, dds) | Raw binary | N/A |

### How to Write UTF-8 BOM in PowerShell

```powershell
# Correct for localisation files
$bom = [byte[]](0xEF, 0xBB, 0xBF)
$content = Get-Content $path -Raw -Encoding UTF8
[System.IO.File]::WriteAllBytes($path, $bom + [System.Text.Encoding]::UTF8.GetBytes($content))

# Correct for script files
Set-Content -Path $path -Value $content -Encoding Default
```

### Common Encoding Mistakes

1. Opening a `.txt` file in VS Code and saving as UTF-8 → corrupts EU4 script parsing
2. `Get-Content | Set-Content` without `-Encoding Default` → converts to Unicode
3. Copy-pasting from browser (which injects UTF-8) into script files
4. Git autocrlf converting line endings unexpectedly

### How to Verify Encoding

```powershell
# Check UTF-8 BOM
$bytes = [System.IO.File]::ReadAllBytes($path)
if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    "UTF-8 BOM: YES"
} else {
    "UTF-8 BOM: NO (WRONG for localisation)"
}
```

## Country Tags and File Pairs

### Tag Rules
- Tags are **exactly 3 ASCII characters** (e.g., `VRN`, `MAS`, `GROM`)
- Must be unique across all loaded mods
- Registered in `common/country_tags/*.txt`

### Required File Pair for Every Tag
Every country tag MUST have ALL of:

| File | Path | Example |
|---|---|---|
| Tag definition | `common/countries/VRN.txt` | Country color, graphical culture |
| History | `history/countries/VRN.txt` | Rulers, development, starting tech |
| Localisation | `localisation/` | Country name, adjectives |
| Flag | `gfx/flags/VRN.tga` | 128x128 or 256x256 TGA |
| Ideas | `common/ideas/*.txt` | National ideas (7 + bonus) |
| Tag entry | `common/country_tags/*.txt` | `VRN="verne"` |

**Missing any of these → game can crash or silently fail to load the country.**

## History Files

- Path: `history/countries/{TAG}.txt`
- Contains: `monarch_name`, `technology`, `additive_development_cost`, `government_reform`, etc.
- Save-file style entries (like `monarch_consort`) are valid in history files
- Must start with country name matching the tag

## Localisation Rules

- File naming: `{ModName}_l_english.yml`
- First line must be: `l_english:`
- Key format: `KEY:0 "Value"` (note the space after colon)
- Replacement loc goes in `localisation/replace/` with same naming
- UTF-8 BOM required — EU4's localisation loader depends on it
- No smart quotes — use straight `"` only

### Key Naming Convention
```
{TAG}_{type}_{name}
VRN_ideas_mechanic_name:0 "Name"
VRN_mission_vernissage_title:0 "The Vernissage"
```

## Idea Groups

- Always **7 ideas + 1 bonus** = 8 total entries
- Each idea needs a `name` and `modifier`
- Bonus must match the idea group bonus
- Must be registered in `common/ideas/` and `common/idea_tags.txt`

## Overrides

- To override a vanilla file, place it at the same path in your mod
- To override Anbennar files, replicate the same relative path
- Flag high-blast-radius overrides in the mod-spec

## Repo Reference

For Verne-specific paths, see `design/registry/` for existing modifiers, namespaces, and IDs.
