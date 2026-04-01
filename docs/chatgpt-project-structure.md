# ChatGPT Project Organization for Verne Mod

## Recommended Projects

### 1. Modding (already exists ✅)
**Purpose:** EU4 modding strategy, architecture, code review
**URL:** https://chatgpt.com/g/g-p-69cb9f6f4efc819188e90b492c235334-modding/project
**Current chats:** 5 (Strategy, VSCode, Agent mode, Anbennar Analysis, Codex Efficiency)

**Upload as Sources:**
- `docs/design/lanes/lane1-court.txt` through lane8-faith.txt
- `docs/eu4-modding-reference.md`
- `docs/modding-qa-protocol.md`
- `missions/Verne_Missions.txt`
- `events/Flavour_Verne_A33.txt`

### 2. Verne Art (CREATE — click "New project" in sidebar)
**Purpose:** All art generation for EU4 assets
**Suggested icon:** 🎨 or 🗡️

**Upload as Sources:**
- `art/` directory with existing VerneArtPack (10 files)
- `docs/art-pipeline.md` (EU4 style guide)
- `docs/verne-gfx-index.md` (what's needed)
- `docs/verne-gfx-catalog.md` (what exists)
- Example high-scoring generated images as style references

**Chats to move here:** Medieval Court Scandal, Oath-Swearing Ceremony, Warship Fleet, Medieval Icon Generation, and future art chats

### 3. Verne Research (CREATE — click "New project" in sidebar)
**Purpose:** Deep research, lore analysis, mod inspiration
**Suggested icon:** 🔬 or 📚

**Upload as Sources:**
- `docs/eu4-wiki-scrape.md` (33KB modding reference)
- `docs/eu4-game-reference.md` (25KB game mechanics)
- `docs/inspiration-bank.md` (community mod ideas)

**Chats to move here:** Any Deep Research chats, lore analysis chats

## How to Create a Project

1. In ChatGPT sidebar, click "Projects" → "New project"
2. Name it (e.g., "Verne Art")
3. Upload reference files via "Sources" tab → "Add files"
4. When starting new chats, navigate to the project first, then type in the project textbox

## How to Move a Chat to a Project

1. Click the chat in "Recents"
2. Click conversation options (⋯)
3. Select "Move to project"
4. Choose the target project

## Auto-Org Protocol (for subagents)

When a subagent generates art:
- Chat is created in Recents, NOT in a project
- After generation, subagent should NOT move it (can't automate reliably)
- Instead, document the chat ID in verne-art-queue.md
- Falk can manually move chats to the "Verne Art" project when convenient

## Context Files Priority

Upload these FIRST to get best results:

| Project | Most impactful files |
|---------|---------------------|
| Verne Art | VerneArtPack icons + art-pipeline.md (style guide) |
| Modding | Verne_Missions.txt + eu4-modding-reference.md |
| Verne Research | eu4-wiki-scrape.md + eu4-game-reference.md |

The AI reads project Sources for context, so uploaded files directly improve generation quality.
