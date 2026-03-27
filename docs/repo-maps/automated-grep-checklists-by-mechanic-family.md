# Automated Grep Checklists by Mechanic Family

Use these commands as a fast "did upstream change something important?" check.

## 1) Diplomatic actions

```bash
ls common/new_diplomatic_actions
rg -n "diplomatic|action|magic_duel|tributar" common/new_diplomatic_actions/*.txt
```

## 2) Peace treaty layer

```bash
ls common/peace_treaties
rg -n "verne|corin|raj|tribut|remove_evil|peace" common/peace_treaties/*.txt
```

## 3) Rebel systems

```bash
ls common/rebel_types
rg -n "corinite|mage|artific|hoard|goblin|patrician" common/rebel_types/*.txt
```

## 4) Unit families

```bash
ls common/units
rg -n "^type\s*=|unit_type|group|tech" common/units/*.txt
```

## 5) Government mechanics

```bash
ls common/government_mechanics
rg -n "anb_|government_ability|power|interaction" common/government_mechanics/*.txt
rg -n "government_abilities" common/government_reforms/*.txt
```

## 6) Religion behavior for Verne

```bash
rg -n "regent_court|corinite|add_reform_center|can_have_center_of_reformation_trigger" common/religions/00_anb_religion.txt
rg -n "change_religion = corinite|add_reform_center = corinite" events/Flavour_Verne_A33.txt
```

## Usage rule

- Run these before and after upstream sync.
- If output changed a lot, mark affected rows in the change ledger as `NEEDS_REVALIDATION`.
