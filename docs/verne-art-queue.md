# Verne Art Generation Queue

Track pending, in-progress, and completed art generations.

## ChatGPT Chat Registry

| Chat ID | Purpose | Status | Prompt Summary |
|---------|---------|--------|---------------|
| 69cc399f-560c-8330-a294-1879129fe7fc | High Court event picture | ✅ Done | Medieval court judgment scene, scored 4.0/5 |

## Verne Country Flag Reference

The Verne coat of arms (A33_flag_source.png) contains:
- **Red dragon wings** — wyvern heritage
- **Golden crown** — royal authority  
- **Red cross** — religious/military (St. George's cross)
- **Anchor** — maritime identity
- **Skull** — memento mori / sacrifice
- **Gold and crimson** — dominant colors
- **Dark blue** — background accents

Include relevant flag elements in country-specific art prompts for visual consistency.

## Pending Generations

| Priority | Asset Name | Type | Prompt Template (with flag elements) | Notes |
|----------|-----------|------|--------------------------------------|-------|
| 1 | verne_mage_battlefield | Event | mage + dragon wings + red arcane energy + cross + battlefield | Lane 5 signature event |
| 2 | verne_diplomatic_court | Event | crown + dragon wings + throne room + oath scrolls | Lane 1 event |
| 3 | verne_colonial_landing | Event | anchor + dragon wings + crown + dawn + new shores | Lane 4 event |
| 4 | verne_holy_war | Event | red cross + skull + sword + dragon wings + crusade | Lane 8 event |
| 5 | verne_wyvern_tower | Icon | dragon wings + tower + arcane + crown | Lane 5 icon |

## Completed Generations

| Asset | Score | Best Prompt | File Location | Chat ID |
|-------|-------|-------------|---------------|---------|
| verne_eventPicture_high_court | 4.0/5 | "medieval oil painting + crimson and gold robes + wyvern heraldry + torchlight + Renaissance art style + no text" | ChatGPT chat (manual download) | 69cc399f |
| verne_eventPicture_crimson_oath | 5.0/5 | "dark medieval oil painting + oath-swearing ceremony + glowing magical oath circle + red arcane energy + nobles on stone balconies + wyvern banners" | ChatGPT chat (manual download) | 69cc3de1 |
| verne_eventPicture_crimson_fleet | 5.0/5 | "red-sailed warship fleet + stormy seas + crimson wake + medieval oil painting + deep reds and ocean blues" | ChatGPT chat (manual download) | 69cc3f21 |
| verne_modifier_court_authority | 5.0/5 | "medieval gold crown + magical red energy + dark background + ornate gold and crimson + game UI icon style" | ChatGPT chat (manual download) | 69cc40f3 |
| verne_eventPicture_distant_horizons | 5.0/5 | "explorers on ship deck + new continent horizon + crimson and gold banners + dawn light + deep reds, ocean blues, golden dawn" | ChatGPT chat (manual download) | 69cc40c9 |
| mission_verne_oath_sworn | 5.0/5 | "glowing scroll + magical oath seals + golden glow + dark background + medieval illuminated manuscript + gold border" | ChatGPT chat (manual download) | 69cc40b7 |
| verne_eventPicture_distant_horizons | 4.0/5 | "dark medieval oil painting + explorers on ship deck + new continent on horizon + crimson and gold banners + dawn light through clouds + deep reds/ocean blues/golden dawn + Renaissance art style + no text + 16:9" | ChatGPT chat (current session, needs manual download) — Lane 4 colonial expansion |

## Prompt Library (Tuned for EU4 Aesthetic)

### Proven Winners
- "medieval oil painting" — strong EU4 event picture feel
- "crimson and gold robes" — Verne's color palette
- "wyvern heraldry" — Anbennar-specific visual identity
- "torchlight" — dramatic medieval lighting
- "Renaissance art style" — matches EU4 era
- "no text" — essential for game art

### Reusable Template
```
A [style] depicting: [subject]. [palette colors] robes and banners,
[heraldry] visible on shields and banners. [lighting], [atmosphere],
[mood]. [era] art style. Fantasy medieval setting, no text, [aspect ratio].
```

## Self-Improvement Log

### Iteration 1 — High Court (2026-03-31, score: 4.0/5)
- Added "crimson robes + wyvern heraldry + torchlight" — scored 4.0/5
- Lesson: Specific heraldry + color palette + lighting = strong first-try results

### Iteration 2 — Crimson Oath (2026-03-31, score: 5.0/5)
- Even more specific prompt elements: "glowing magical oath circle" + "red arcane energy" + "nobles watch from stone balconies" + "deep reds, golds, and blacks"
- Scored significantly better than iteration 1
- Lesson: Specific spatial descriptions (balconies above, circle below) + explicit color list + named elements = best results
- Winning phrase: "dark medieval oil painting depicting [subject] in [setting]. [specific visual element 1], [specific visual element 2]. [color palette]. Renaissance art style, fantasy medieval setting, no text."

### Iteration 3 — Distant Horizons (2026-03-31, score: 4.0/5)
- Lane 4 colonial expansion event picture
- Strong atmospheric quality with dawn lighting and ocean tones
- Good composition: ship deck, banners, distant shores all visible
- Lesson: Ocean/nautical prompts work well with "deep reds, ocean blues, golden dawn" color palette
- Prompt used: "A dark medieval oil painting depicting explorers on a ship deck looking toward a new continent on the horizon. Crimson and gold banners flutter in the wind. Distant shores with mysterious forests visible. Dawn light breaking through clouds over the horizon. Deep reds, ocean blues, golden dawn. Renaissance art style, fantasy medieval setting, no text. 16:9 aspect ratio."

### Proven Prompt Pattern
"A dark medieval oil painting depicting: [action scene]. [character 1 action], [character 2 action]. [specific magical/supernatural element]. [architecture/environment detail]. [explicit color list: deep reds, golds, and blacks]. Renaissance art style, fantasy medieval setting, no text. 16:9 aspect ratio."

### Next Iteration Notes
- For fleet events: "red-sailed ships + dramatic ocean + crimson wake behind ships"
- For arcane events: "arcane runes + red magical energy + mage robes"
- For mission icons: try same style but "square format, single central object, gold border"
- Nautical/colonial themes benefit from "dawn light + ocean blues + golden horizon" palette
