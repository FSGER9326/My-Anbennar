# Verne Monument Object-ID Parity Check Reference

This is a focused deep-diff note for one immediate implementation dependency:

- the **Lament's Regatta** mission chain,
- its monument object IDs,
- and the New Hookfield -> Stingport spire relocation flow.

## Quick verdict

The chain is internally consistent, but it is easy to break if names are changed without preserving script IDs.

High-risk IDs that must stay stable:

- `kazakesh` (source monument in New Hookfield)
- `kazakesh_stingport` (moved monument in Stingport)
- `aur_kes_akasik` (Akasik checkpoint monument requirement)
- provinces `5763`, `376`, `383`, and `5793`

## Core files

| File | Why it matters |
|---|---|
| `missions/Verne_Missions.txt` | Defines mission `A33_laments_regatta` and trigger requirements using `kazakesh` + `aur_kes_akasik` tier checks. |
| `events/Flavour_Verne_A33.txt` | Implements event chain `verne.123` -> `verne.126` that physically moves/replaces the spire monument object. |
| `common/great_projects/anb_monuments_sarhal.txt` | Defines source monument object `kazakesh` and checkpoint monument `aur_kes_akasik`. |
| `common/great_projects/anb_monuments_missions.txt` | Defines destination monument object `kazakesh_stingport` gated by `verne_moved_spire`. |
| `localisation/anb_great_projects_l_english.yml` | Contains player-facing name for `aur_kes_akasik`. |
| `localisation/Flavour_Verne_A33_l_english.yml` | Contains event text for `verne.123-126` and localization key for `kazakesh_stingport`. |

## Object-ID parity matrix

| Gameplay concept | Script object ID | Location / province | Localization key |
|---|---|---|---|
| Original Zatsarya spire (pre-move) | `kazakesh` | `5763` (New Hookfield) | `kazakesh` (in great-project loc file) |
| Moved spire in Verne | `kazakesh_stingport` | `376` (Stingport) | `kazakesh_stingport` |
| Akasik palace checkpoint | `aur_kes_akasik` | `383` (Desh-al-Deshak) | `aur_kes_akasik` |
| Move-completion state gate | `verne_moved_spire` | country flag | n/a |
| Source-lock state gate | `verne_moved_this_spire` | province flag on source | n/a |

## Event-to-object flow (actual wiring)

1. `A33_laments_regatta` requires:
   - `5763` has `kazakesh` at tier 3,
   - `383` has `aur_kes_akasik` at tier 3,
   - and additional mage/estate/favor conditions.
2. Mission completion fires `verne.123` (Regatta), then `verne.124`, `verne.125`, `verne.126`.
3. In `verne.126`:
   - `5763` destroys great project `kazakesh` and sets `verne_moved_this_spire`,
   - country sets `verne_moved_spire`,
   - `376` instantly adds `kazakesh_stingport`.
4. `kazakesh_stingport` build trigger checks `owner = { has_country_flag = verne_moved_spire }`, which is the parity bridge between event logic and monument definition.

## Smoke-test checklist for this family

Use these checks after edits to Verne mission/event/monument naming:

1. ID existence:
   - `rg -n "^kazakesh\s*=|^kazakesh_stingport\s*=|^aur_kes_akasik\s*=" common/great_projects/*.txt`
2. Mission dependency check:
   - `rg -n "A33_laments_regatta|type = kazakesh|type = aur_kes_akasik" missions/Verne_Missions.txt`
3. Move-event wiring check:
   - `rg -n "verne\.126|destroy_great_project|add_great_project|verne_moved_spire|verne_moved_this_spire" events/Flavour_Verne_A33.txt`
4. Localization parity check:
   - `rg -n "kazakesh_stingport|aur_kes_akasik|verne\.123\.t|verne\.126\.t" localisation/*.yml`

## Safe extension notes

- If you rename player-facing monument titles, keep script IDs (`kazakesh`, `kazakesh_stingport`, `aur_kes_akasik`) unchanged.
- If you introduce a new destination monument variant, preserve `verne_moved_spire` or provide an explicit compatibility shim in both mission and monument triggers.
- Avoid changing province IDs in this chain unless all mission trigger blocks and event effects are migrated in one commit.
