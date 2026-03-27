# Fluff and Art Production Playbook (Plain-Language)

This page answers a simple question:

When we add gameplay content, how do we also make sure text and visuals feel like Anbennar?

## First, very clear: what the recent work did

Recent repo-map work **did not** create new monument IDs or new bonuses.

It did this instead:

- listed and verified the IDs that already exist,
- mapped where mission/event/localization are connected,
- made “don’t-break-this” checklists for later coding.

So yes: it prepared implementation safely, but it did not yet do value balancing or new content objects.

## Simple production rule for every new feature

Every feature should ship with 4 parts in the same slice:

1. **Mechanics** (the actual effect)
2. **Numbers** (the bonus values)
3. **Fluff text** (name + description)
4. **Visual choice** (reuse icon/art or mark as needs-new-art)

If one of these is missing, mark the feature `NOT READY`.

## How to keep fluff text in-style

Use a small style check before merge.

### Style checklist (quick)

- Is the tone consistent with nearby Verne/Anbennar loc writing?
- Does it mention the right culture/region/religious flavor for the thing?
- Is it written like in-game flavor text, not a dev note?
- Does the title match what the mechanic actually does?
- Does it avoid modern out-of-world wording?

### Practical way to do this

For each new text block, compare against 2-3 existing localizations from:

- `localisation/Flavour_Verne_A33_l_english.yml`
- `localisation/anb_great_projects_l_english.yml`

If it reads wildly different from those references, rewrite before merge.

## Art strategy: reuse first, new art second

### Tier 1: Reuse existing art (default)

For most idea/reform/modifier icons:

- pick the closest existing icon,
- prefer clarity over uniqueness,
- record the chosen icon in the implementation note.

Example: cavalry offense + cavalry cost reduction can reuse an existing cavalry-themed icon.

### Tier 2: Recolor or light edit (optional)

If reuse is too confusing but close:

- use a lightly edited/recolored variant,
- keep style close to existing icon set.

### Tier 3: New art (only when truly needed)

Use this only for major signature content (for example landmark monuments with unique presence).

When needed, create a prompt packet with:

1. subject (what it depicts),
2. mood/tone,
3. composition,
4. color direction,
5. explicit “fit Anbennar/EU4 UI style” note,
6. negative constraints (no modern objects, no sci-fi, etc.).

## Asset tracking mini-template

Use one row per feature in planning notes:

| Feature | Mechanics ready | Numbers ready | Fluff ready | Visual source | Status |
|---|---|---|---|---|---|
| Example: New Verne monument | yes/no | yes/no | yes/no | reused icon / new art needed | READY / NOT READY |

## “Done” definition for content quality

A feature is done only when:

- effect works,
- values are set,
- localization exists,
- icon/art source is selected,
- grep smoke checks pass for IDs and loc keys.

This keeps implementation and presentation moving together.


## Script commentary standard (new workflow rule)

When adding or changing a mission, monument, idea, reform, decision, or event, add short non-functional comments that answer:

1. Is this mainly **base Anbennar reused content** or **new Verne content**?
2. What does this do for the nation in plain language?
3. How does it support that nation's playstyle/story identity?
4. Which high-risk IDs/flags/tiers must not be renamed casually?

### Suggested comment format in script files

- `Commentary (plain-language):` one sentence of purpose.
- `Base vs new:` one line saying what is inherited vs newly added.
- `Playstyle effect:` one line saying what behavior this encourages.
- `Risk note:` one line naming fragile IDs/flags.
- `Province context:` if provinces are touched, include ID + province name + larger region/continent context.
- `Lore-fit note:` one line on whether mechanic aligns with nation fantasy/lore tone.

Keep comments short and practical so they stay maintainable.
