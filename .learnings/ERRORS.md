# Errors

Command failures, integration errors, and modding bugs.

**EU4 Paradox Scripting Errors** (recurring patterns to check automatically):

## Syntax Errors
- **Unbalanced braces** — every { needs a }. Most common in long modifier blocks.
- **Semicolons** — Paradox script doesn't use semicolons. Removing them fixes parse errors.
- **Spaces instead of tabs** — EU4 uses tabs for indentation. YAML uses spaces.
- **Wrong comment syntax** — Paradox uses # only. // and /* */ don't work.

## Logic Errors
- **Missing flag propagation** — Mission A sets flag X, Mission B needs flag X, but nobody checks it. Check with: `set_country_flag` must have matching `has_country_flag` in next mission.
- **Modifier not defined** — `add_country_modifier = { name = foo }` but `foo` doesn't exist in common/event_modifiers/. Game silently ignores it.
- **Wrong duration** — duration = 0 means "expires next month", not "permanent". Use -1 for permanent.
- **Wrong scope** — Using country-scope triggers in province scope or vice versa. `owns = X` (country) vs `is_colony = yes` (province).

## Localisation Errors
- **Missing _title or _desc** — Mission has key `A33_my_mission_title` but no localisation entry. Game shows raw key.
- **YAML format** — Key:0 "value" (colon-zero required). Wrong indentation breaks the whole file.
- **Duplicate keys** — Two missions with same title key. Second one overwrites silently.

## Mission Chain Errors
- **Orphan missions** — Mission not required by anything and doesn't require anything. Floats alone in the tree.
- **Broken required_missions** — Mission requires "A33_foo" but that mission ID doesn't exist (typo).
- **Position overflow** — More than ~10 missions in one slot causes overlap. Check position values.

## Cross-Lane Errors
- **Flag not set before check** — Lane 4 checks a flag Lane 2 was supposed to set, but Lane 2's mission was skipped.
- **Reform doesn't exist** — Mission requires `verne_my_reform_reform` but that reform isn't in government_reforms/.

## Subagent Errors (2026-03-31 session)

- **Browser automation too slow** — Subagents can't handle ChatGPT UI (45s/turn, 5min timeout). FIX: Browser = main session only.
- **Relative file paths lost** — Subagent writes to ephemeral dirs. FIX: Always use absolute workspace paths.
- **Parallel subagents competed** — 4 art subagents shared one browser tab. FIX: Stagger or separate tabs.
- **Default timeout too short** — Complex tasks (wiki scrape, audit) need 5-10min. FIX: Always set runTimeoutSeconds.
- **Chat move UI too fast** — Browser refs go stale before clicks land. FIX: JS retry with 200ms polling for menu items.
- **Pro mode = no DALL-E** — Subagent wasted 6min trying Pro. FIX: Thinking 5.4 only for image gen.

---

