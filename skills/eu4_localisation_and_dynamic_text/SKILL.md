# eu4_localisation_and_dynamic_text

## Purpose
Teach EU4 localisation rules — encoding, key formats, bracket syntax, dynamic text, and the `localisation/replace/` system.

## Encoding (Non-Negotiable)

### UTF-8 with BOM — Required for ALL localisation files

```
localisation/Flavour_Verne_A33_l_english.yml
```

The first three bytes of every loc file MUST be: `EF BB BF` (UTF-8 BOM).

EU4's localisation loader depends on the BOM to identify UTF-8 encoded files. Without it, accented characters break silently.

### File Structure

```yaml
l_english:

 # First line is always exactly this
 # Blank lines are ignored

TAG_key_title:0 "The Display Title"
TAG_key_desc:0 "Description text."
TAG_key_tt:0 "Tooltip text."
```

Note: `l_english:` with NO space before the colon.

### PowerShell BOM Write

```powershell
$bom = [byte[]](0xEF, 0xBB, 0xBF)
$utf8 = [System.Text.Encoding]::UTF8
$bytes = $bom + $utf8.GetBytes($content)
[System.IO.File]::WriteAllBytes($path, $bytes)
```

### PowerShell BOM Read-Check

```powershell
$bytes = [System.IO.File]::ReadAllBytes($path)
$hasBom = $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF
if (-not $hasBom) { Write-Host "ERROR: No UTF-8 BOM" }
```

## Key Naming Convention

Format: `{PREFIX}_{type}_{specific_name}`

```
VRN_mission_slot3_colony_title:0 "Establish a Colony"
VRN_mission_slot3_colony_desc:0 "Fund an expedition to the New World."
VRN_mission_slot3_colony_tt:0 "Requires: 500 gold"
```

| Suffix | Meaning |
|---|---|
| `_title` | Display name / mission name |
| `_desc` | Description / tooltip body |
| `_tt` | Tooltip (often used for dynamic variable display) |
| `_option_N` | Decision/event option text |
| `_name` | Character/ruler names |
| `_adjective` | Country adjectives |

## Dynamic Text / Bracket Localisation

EU4 supports dynamic tokens in localisation strings:

### Variable Substitution
```
verne_network_tt:0 "£verne_world_network£ / 10 networks"
```
Shows the value of `verne_world_network` variable (from `change_variable`).

### Icon Substitution
```
my_loc_key:0 "£gold£ 500"
```
Shows the gold icon followed by "500".

### Color Codes
```
my_loc_key:0 "[Root.GetName] is growing"
```
`[Root.GetName]` calls a scripted effect to insert dynamic text.

### Common Dynamic Tokens (Verne)
```
£verne_world_network£     # Variable value
£verne_overseas_projection£  # Variable value
£prestige£               # Prestige icon + value
£legitimacy£             # Legitimacy icon + value
```

## Localisation Replace System

For overriding vanilla or Anbennar loc without editing the original file:

1. Create `localisation/replace/{MyMod}_l_english.yml`
2. Uses the SAME format as normal loc
3. Loaded AFTER all other loc — overrides existing keys

```yaml
# In localisation/replace/MySubmod_l_english.yml
l_english:

OLD_KEY:0 "My Overridden Text"
NEW_KEY:0 "Brand new text"
```

**Important:** Filename must end with `_l_english.yml`.

## Tooltip Localisation (TT Keys)

For mission tooltips that reference variables or conditions:

```bash
# In mission file
custom_tooltip = verne_world_network_tt

# In localisation file
verne_world_network_tt:0 "£verne_world_network£ / 10 trade networks established"
```

For conditional tooltips:
```bash
custom_tooltip = {
    text = verne_network_tt_1
    text = verne_network_tt_2
}
```

## Character / Ruler Name Localisation

Character names use their own key space:
```bash
# In history/countries/VRN.txt
monarch_name = {
    name = "verne_ruler_1_name"
    dynasty = "verne_dynasty_1"
}

# In localisation
verne_ruler_1_name:0 "Margrave Elric"
verne_ruler_1_female_name:0 "Margravine Elena"
verne_dynasty_1:0 "House Silvermoor"
```

## Common Mistakes

1. **Missing BOM** → accented characters break in-game
2. **Wrong key name in file** → `title = "vrn_mission_1"` but loc key is `VRN_mission_1`
3. **Smart quotes** → `"` instead of `"` — EU4 doesn't render these correctly
4. **Blank loc key** → `":0 "Something"` — no key before colon
5. **Duplicate keys** → same key defined twice (last one wins silently)
6. **Wrong locale suffix** → `_l_english` vs `_l_english.yml`
7. **Tab characters** → tabs in yml files break parsing — use spaces

## Placeholder Loc Rules

**Never ship placeholder text.** If a loc key is missing, the game shows the raw key (e.g., `verne_mission_1_title`).

- Every generated `title`, `desc`, `tt` key must have a real English value
- Every generated event/decision/mission must have matching loc entries
- Add a placeholder loc scan to the validation pipeline

```powershell
# Scan for missing loc references
$locFiles = Get-Content "localisation/*_l_english.yml" -Raw
$missingKeys = $generatedKeys | Where-Object { $locFiles -notmatch $_ }
if ($missingKeys) { Write-Host "MISSING LOC: $($missingKeys -join ', ')" }
```

## Verne-Specific Loc Patterns

```bash
# From Verne_Missions.txt — mission name/desc refs
name = "verne_mission_vernissage_title"
desc = "verne_mission_vernissage_desc"

# From events
title = "verne_liliac_war_1_title"
desc = "verne_liliac_war_1_desc"

# From modifiers (event_modifiers/)
verne_silver_oaths:0 "Silver Oaths of Grombar"
verne_court_of_oaths:0 "Court of Oaths"
```

## Encoding Scan Script

```powershell
# tools/validate/encoding-scan.ps1
param([string]$Path = ".")

$locFiles = Get-ChildItem -Recurse -Include "*_l_english.yml" -Path $Path
foreach ($file in $locFiles) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $hasBom = $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF
    if (-not $hasBom) {
        Write-Host "[ENCODING ERROR] $($file.FullName) — Missing UTF-8 BOM"
    }
}

$scriptFiles = Get-ChildItem -Recurse -Include "*.txt","*.gui" -Path $Path | Where-Object { $_.FullName -notmatch "localisation" }
foreach ($file in $scriptFiles) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Write-Host "[ENCODING ERROR] $($file.FullName) — UTF-8 BOM on script file (should be CP-1252)"
    }
}
```
