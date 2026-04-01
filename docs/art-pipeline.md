# EU4 Art Generation Pipeline

Automated art creation for the Verne mod using ChatGPT's DALL-E image generation.
Self-improving: prompts evolve based on evaluation feedback.

---

## Pipeline Flow

```
GFX Index identifies missing asset
         ↓
Generate prompt (EU4-style description)
         ↓
Send to ChatGPT DALL-E via browser
         ↓
Download generated image
         ↓
Evaluate against EU4 style guide
         ↓
  ┌──── PASS ────┐   ┌──── FAIL ────┐
  Save to repo    │   Refine prompt  │
  Update index    │   Try again      │
                  │   (max 3 tries)  │
                  └──────────────────┘
```

## EU4 Style Guide for DALL-E Prompts

### Mission Icons (ideas_EU4 / missions_EU4)
- Small square icons (64x64 or 128x128 px)
- Gold/bronze border with dark background
- Single central object (sword, scroll, compass, crown, ship, etc.)
- Painterly/illustrative style, not photorealistic
- Warm color palette (golds, browns, reds, deep greens)
- No text or letters
- Style reference: "medieval illuminated manuscript icon, gold border, dark background"

### Event Pictures
- 16:9 aspect ratio
- Oil painting style, medieval/Renaissance aesthetic
- Dramatic lighting, rich colors
- Scene depicts the event's content
- Style reference: "medieval oil painting, dramatic lighting, renaissance art style"

### Government Reform Icons
- Same as mission icons but typically crown/throne/gavel themed
- Gold/ornate border

### Modifier Icons
- Small icons representing the modifier's effect
- Simple, clear symbolism
- Match EU4's existing modifier icon style

## Prompt Templates

### Mission Icon
```
Create a small medieval-style icon for a game interface. Subject: {subject}.
Style: gold and bronze tones on dark background, medieval illuminated manuscript aesthetic,
single central object, ornate but clean, no text. Square format, painterly illustration.
```

### Event Picture
```
A medieval oil painting depicting: {scene}. Renaissance art style, dramatic lighting,
rich deep colors, no text or letters. Painterly brushstrokes, historical fantasy setting.
```

### Modifier Icon
```
A small game icon representing: {effect}. Gold and dark tones, medieval aesthetic,
clean simple design, no text, square format, UI element style.
```

### Verne Country Flag (COA) — Include in Country-Specific Art

The Verne coat of arms contains: **red dragon wings, golden crown, red cross, anchor, skull, gold-and-crimson palette, dark blue accents**

Use flag elements when generating country-specific art:

| Theme | Flag Elements to Include |
|-------|------------------------|
| Maritime events | anchor + dragon wings + crimson sails + dark ocean |
| Military events | red cross + sword + skull + dragon wings + crimson |
| Court events | golden crown + dragon wings + gold robes + red banners |
| Religious events | red cross + golden elements + cathedral/gothic windows |
| Arcane events | dragon wings + red arcane energy + golden runes |
| Colonial events | anchor + dragon wings + golden crown + dawn light |
| Dynastic events | golden crown + dragon wings + silver/chains + red velvet |

Example flag-aware prompt:
```
A dark medieval oil painting depicting [subject]. In the scene, crimson and gold
banners display the Verne coat of arms — dragon wings, red cross, and golden crown.
[prompt-specific details]. Renaissance art style, no text, 16:9.
```

## Evaluation Criteria

Each generated image is scored 1-5 on:
1. **Style match** — Does it look like EU4/vanilla Anbennar art?
2. **Clarity** — Is the subject immediately recognizable?
3. **Quality** — No artifacts, clean execution
4. **Consistency** — Matches other Verne mod assets
5. **Usability** — Works at actual game resolution

**Threshold:** Average ≥ 3.5 to accept. Below → regenerate with refined prompt.

## Auto-Resize Script

Use `scripts/convert-art.py` to convert DALL-E PNGs to EU4 formats:

```bash
# Event pictures (800x600 PNG)
python scripts/convert-art.py input.png --type event --output output.png

# Mission icons (128x128 DDS/PNG)
python scripts/convert-art.py input.png --type mission_icon --output icon.png

# Modifier icons (64x64)
python scripts/convert-art.py input.png --type modifier_icon --output mod_icon.png

# Flags (128x81 TGA)
python scripts/convert-art.py input.png --type flag --output A33.tga
```

## Multi-Generation Workflow

For batch art creation, use multi-tab parallel generation:
1. Read verne-art-queue.md for pending assets
2. Open 3 ChatGPT tabs (max)
3. In each tab: select Thinking 5.4 → type prompt → submit
4. Wait ~60s for all 3 to generate
5. Screenshot + evaluate each, log results
6. Close extra tabs, keep 1 main tab
7. Repeat for remaining assets

ChatGPT Projects provide context across generations. Upload reference files to the "Verne Art" project for better first-try results. Create the project via sidebar → "New project" → upload Sources → start chats within the project.

## Self-Improvement

After each generation cycle:
1. Log the prompt → result → evaluation score in verne-art-queue.md
2. Identify which prompt elements produced high-scoring results
3. Update prompt templates with successful phrasing
4. Track which subjects are hardest to generate well
5. Update winning phrases in the Prompt Library

Over time, prompts become tuned to produce EU4-consistent art.

## Rate Limit Protocol

When ChatGPT hits message limits during generation:
1. **Detect:** Look for "limit reached", "X messages remaining", or "resets at" in UI
2. **Log:** Record the limit and reset time in this file
3. **Wait:** Stop all generation, check back at reset time
4. **Resume:** Continue with remaining assets after reset

**Detection tip:** Before starting a batch, check chat footer for remaining messages. If < 3, wait for reset first.

**Example log entry:**
```
### Rate Limit Hit — 2026-03-31
- Time: 23:49 CET
- Reset: 00:15 CET (25 min wait)
- Remaining assets: 11
- Action: Resume at 00:15
```

---

## Generation Log

### 2026-03-31 — verne_eventPicture_high_court (Medieval Court Judgment)
- **Prompt:** "Generate an image: A medieval oil painting depicting a dramatic court scene in a grand stone hall. Nobles in crimson and gold robes judge a kneeling figure. Wyvern heraldry banners hang from stone pillars. Torchlight, dark dramatic atmosphere, deep reds and shadows, Renaissance art style. Fantasy medieval setting, no text, 16:9."
- **Model:** ChatGPT DALL-E (Thinking 5.4 model — Pro 5.4 has no DALL-E!)
- **Result:** 1536x1024 PNG, ~3.9MB
- **Evaluation:**
  - Style match: 4/5 (oil painting, medieval, dramatic lighting — very EU4)
  - Clarity: 4/5 (clear judgment scene, recognizable figures)
  - Quality: 4/5 (clean, no artifacts)
  - Consistency: 4/5 (crimson/red palette matches Verne, wyvern heraldry visible)
  - Usability: 4/5 (good resolution, works at game scale)
  - **Average: 4.0/5 — ACCEPTED ✅**
- **Best prompt:** "medieval oil painting" + "crimson and gold robes" + "wyvern heraldry" + "torchlight" + "Renaissance art style" + "no text" = strong EU4 aesthetic
- **Download note:** Manual download needed — browser automation can't save ChatGPT blobs directly. Use "Download this image" button or screenshot crop.

---
*This file is updated by the art-generator subagent as it learns what works.*
