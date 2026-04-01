# Subagent Patterns — Self-Improving Spawning Guide

Lessons learned from spawning 20+ subagents in the 2026-03-31 session.
The main agent MUST read this before spawning any new subagent.

## What Works ✅

### Browser automation (do in main session)
- **Problem:** Subagents are too slow for ChatGPT browser UI (snapshot → think → act cycles burn 5+ min)
- **Solution:** Art generation, ChatGPT interactions = main session only
- **Lesson:** NEVER spawn subagents for browser-heavy tasks

### File writing with absolute paths
- **Problem:** Subagents writing to relative paths (`docs/design/lanes/`) lose files to ephemeral dirs
- **Solution:** Always use `C:\Users\User\.openclaw\workspace\` prefix
- **Lesson:** Always give absolute paths in subagent task descriptions

### 5-minute timeout is too short for complex tasks
- **Problem:** Many subagents timed out at 5min (art generation, wiki scraping, cross-reference audit)
- **Solution:** Set timeout via `runTimeoutSeconds: 300` for simple tasks, `600` for complex ones
- **Lesson:** Always specify timeout in spawn call. Default may be too short.

### Specific task descriptions beat vague ones
- **Problem:** Vague subagent tasks produce vague results, then need re-spawning
- **Solution:** Give exact file paths, exact format, exact write tool usage
- **Lesson:** More context in task = less rework

## What Doesn't Work ❌

### Subagents for ChatGPT browser interaction
- Browser snapshot → think → act cycle takes ~45s per turn
- A 5-minute timeout gives ~6 turns — barely enough to navigate and type
- Subagents also compete for the same browser tab, causing chaos
- **Rule: Browser tasks = main session only. ALWAYS.**

### Multiple subagents sharing same resources
- 4 art subagents all tried to use the same ChatGPT browser tab
- Result: conflicts, confused state, timeouts
- **Rule: If subagents need shared resources, stagger them (run serially). If parallel, give each its own resource.**

### Spawning without reading subagent-patterns.md
- Each spawn should reference this file for latest lessons
- The main agent sometimes forgets past lessons
- **Rule: ALWAYS read this file before spawning.**

## Spawning Checklist

Before spawning ANY subagent:

- [ ] Read `docs/subagent-patterns.md` (this file)
- [ ] Is this a browser-heavy task? → Do it in main session instead
- [ ] Using absolute paths in task description? → `C:\Users\User\.openclaw\workspace\...`
- [ ] Set appropriate timeout? → `runTimeoutSeconds: 300` (simple) or `600` (complex)
- [ ] Does it need shared resources? → Stagger or give separate resources
- [ ] Clear, specific task with expected output format?

## Timeout Guidelines

| Task Type | Timeout | Notes |
|-----------|---------|-------|
| Simple write/read | 180s | File ops, config edits |
| Web search + write | 300s | Search + compile + write |
| Multi-page scrape | 600s | 10+ web_fetch calls |
| Cross-reference audit | 600s | Reads multiple large files |
| Image generation | 300s | Browser + wait for DALL-E |
| Design + implementation | 900s | Complex multi-step |

## Error Patterns (logged to .learnings/ERRORS.md)

| Error | Root Cause | Fix |
|-------|-----------|-----|
| Files not in workspace | Relative paths | Use absolute paths |
| Subagent timeout at 5min | Complex task, short timeout | Set runTimeoutSeconds |
| Browser tab conflicts | Multiple subagents sharing tab | Stagger or use main session |
| ChatGPT not logged in | Wrong browser profile | Always profile=openclaw |
| Pro mode has no DALL-E | Wrong model selected | Thinking 5.4 = DALL-E |
| Menuitem not found | UI menu closed before click | Use JS retry with delays |

## Subagent Trial & Evaluation Protocol

After each subagent run, evaluate these dimensions (1-5):

### Evaluation Criteria
| Criterion | What to Measure | 1 (Bad) | 5 (Good) |
|-----------|----------------|---------|----------|
| **Speed** | Finished within timeout? vs main session speed? | Timed out | Faster than main session |
| **Quality** | Output comparable to main session work? | Needs full rewrite | As good or better |
| **Correctness** | Right path, right format, no errors? | Wrong path/format | Perfect output |
| **Self-sufficiency** | Needed steering or autonomous? | Constant babysitting | Fire and forget |
| **Output reusability** | How much editing before usable? | Total rewrite | Copy-paste ready |
| **Coordination overhead** | Time spent checking/steering/fixing? | More time than doing it | Zero oversight needed |
| **Trust/autonomy** | Could I walk away and trust it? | Had to watch every step | Completely trustworthy |
| **Scope fit** | Right size for subagent? | Too small (overhead waste) or too big (timeout) | Perfect size |
| **Token efficiency** | Tokens used vs main session equivalent? | 2x+ main session cost | Equal or less than main |
| **Repeatability** | Could same task be reliably delegated again? | One-off fluke | Templatable pattern |

### Scoring
- **5/5** → Perfect delegation. Subagent was faster or equal to main session.
- **3-4/5** → Workable but suboptimal. Note what could improve.
- **1-2/5** → Wrong choice. Should have done in main session. Note why.

### Log Format
Append to this file under Trial Log:

```
### Trial N — [task description]
- Score: X/5 (Speed: X, Quality: X, Correctness: X, Self-sufficiency: X, Tokens: X)
- Scope: [small/medium/large] — [description]
- Main session alternative: [would have been faster/slower/better/worse]
- Lesson: [what to do differently next time]
```

### Trial Log

#### Trial 1 — 8 lane design writers (parallel spawn)
- Score: 3/5 (Speed: 4, Quality: 4, Correctness: 1, Self-sufficiency: 4, Tokens: 3)
- Scope: Large — each wrote a 200-line design file. All 8 completed.
- Issue: Files written to relative paths → lost to ephemeral dirs. Had to rewrite all in main session.
- Lesson: ALWAYS use absolute paths. This is now Rule #1 in patterns file.
- Verdict: Right task for subagents (big parallel work), wrong execution (paths).

#### Trial 2 — GFX indexer (directory scanner)
- Score: 2/5 (Speed: 2, Quality: 3, Correctness: 3, Self-sufficiency: 1, Tokens: 2)
- Scope: Large — scanning entire Anbennar repo for icon references
- Issue: Timed out at 5min (too many dirs to scan). Had to re-spawn with smaller scope.
- Lesson: Don't spawn subagents for recursive directory scanning. Give specific files instead.
- Verdict: Should have done in main session or with much larger timeout.

#### Trial 3 — GFX indexer v2 (specific files only)
- Score: 5/5 (Speed: 5, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 4)
- Scope: Medium — scan 5 specific files for icon references
- Issue: None. Completed in 1m38s.
- Lesson: Narrow, specific file list → fast, correct subagent work.
- Verdict: Perfect delegation.

#### Trial 4 — Art generator (ChatGPT browser)
- Score: 2/5 (Speed: 1, Quality: 4, Correctness: 2, Self-sufficiency: 1, Tokens: 2)
- Scope: Medium — navigate ChatGPT, select model, type prompt, wait, screenshot, evaluate
- Issue: Pro mode had no DALL-E (subagent wasted 6min). All 4 timed out.
- Lesson: NEVER spawn subagents for browser-heavy tasks. Main session only.
- Verdict: Wrong tool. Browser = main session. ALWAYS.

#### Trial 5 — Continuous planner
- Score: 4/5 (Speed: 4, Quality: 5, Correctness: 4, Self-sufficiency: 5, Tokens: 4)
- Scope: Large — read all design docs + codebase, write roadmap
- Issue: None. Completed in 2m16s. Discovered critical design-implementation gap.
- Lesson: Good delegation for analysis tasks. Clear input (files), clear output (roadmap).
- Verdict: Ideal subagent task — reads multiple files, writes summary.

#### Trial 6 — Cross-reference audit
- Score: 5/5 (Speed: 5, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 4)
- Scope: Large — read Verne_Missions.txt + all design docs, cross-reference
- Issue: None. Found 5 issues in 2m24s.
- Lesson: Multi-file analysis is the sweet spot for subagents. Fast, thorough, correct.
- Verdict: Best delegation type.

#### Trial 7 — Wiki scrapers (modding + game)
- Score: 4/5 (Speed: 4, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 4)
- Scope: Large — 10+ web pages fetched, compiled into 2 reference files
- Issue: First attempt (50 pages) too big. Second attempt (10+20 pages) worked perfectly.
- Lesson: Split large scrapes into smaller batches. 10-20 pages per subagent is optimal.
- Verdict: Good delegation. Web fetching is pure I/O — no browser UI needed.

#### Trial 8 — Chat move to project (6× iterations)
- Score: 1/5 (Speed: 1, Quality: 5, Correctness: 5, Self-sufficiency: 1, Tokens: 1)
- Scope: Small — click menu, select project
- Issue: Ref-based clicks timed out. JS retry with delays worked but took 6 iterations.
- Lesson: UI interactions that need precise timing = main session. Too many moving parts for subagents.
- Verdict: Should have done all 6 moves in main session in ~2 minutes.

#### Trial 10 — QA S02 variable tooltips
- Score: 4/5 (Speed: 4, Quality: 4, Correctness: 5, Self-sufficiency: 4, Tokens: 4)
- Scope: Medium — read missions, add custom_tooltip to 15+ variable-changing effects
- Issue: None significant. Completed in 5min. Added tooltips for verne_world_network, verne_overseas_projection.
- Lesson: QA compliance fixes are well-suited to subagents. Clear pattern: find effect blocks changing variables, add custom_tooltip.
- Verdict: Good delegation. Repeatable pattern — could become a skill.

### Trial 11 — QA S05 typo batch fix
- Score: 5/5 (Speed: 5, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 5)
- Scope: Medium — find and replace 13 typos across localisation + modifier files
- Issue: None. Completed quickly. Handled modifier renaming cascading correctly.
- Lesson: Find-and-replace across known patterns = perfect subagent task.
- Verdict: Ideal delegation. Templatable pattern.

### Trial 12 — QA S06 modifier _desc fix
- Score: 5/5 (Speed: 5, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 5)
- Scope: Small — add 2 missing _desc keys to localisation
- Issue: None. Completed in 3min.
- Lesson: Simple localization additions are trivially delegable.
- Verdict: Perfect delegation.

### Trial 13 — Design docs reconciliation (killed, replaced)
- Score: 2/5 (Speed: 2, Quality: N/A, Correctness: 1, Self-sufficiency: 3, Tokens: 2)
- Scope: Large — read all 6 design docs + full mission file, rewrite docs
- Issue: Spawned with outdated 9-slot info. Had to be killed and replaced with correct 10-column instructions.
- Lesson: Always verify current architecture before spawning design work. Check MEMORY.md and recent decisions.
- Verdict: Wrong instructions wasted a spawn. Check memory first.

### Trial 14 — Design docs lanes 5-10 rewrite
- Score: 4/5 (Speed: 4, Quality: 4, Correctness: 4, Self-sufficiency: 5, Tokens: 3)
- Scope: Large — rewrite 6 lane docs, create 4 new, update roadmap
- Status: partial_success (timeout after 4/10 lanes, but per-lane commits preserved work)
- Failure taxonomy: timeout (900s was not enough, needed ~1500s)
- Reflection: 900s got 4 lanes. Each lane takes ~3.5min. Remaining 6 needed 1500s. Second spawn at 1500s completed successfully.
- Lesson: Per-lane commits are the right strategy — work survives timeouts.

### Trial 15 — Design docs lanes 5-10 (retry)
- Score: 5/5 (Speed: 4, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 3)
- Scope: Large — rewrite 6 remaining lane docs + roadmap update
- Status: success
- Reflection: 1500s was sufficient. Per-lane commits worked perfectly.

### Trial 16 — Design docs IMPLEMENTED/DESIGN GOAL tagging
- Score: 5/5 (Speed: 5, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 5)
- Scope: Medium — tag all 10 lane docs with [IMPLEMENTED] vs [DESIGN GOAL]
- Status: success
- Reflection: Clean, self-sufficient. ChatGPT now reads tagged docs via @GitHub for implementation guidance.

### Trial 17 — Vault restructuring
- Score: 5/5 (Speed: 5, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 4)
- Scope: Large — restructure Obsidian vault, create 5+ new files, move 13 files, create OPENCLAW.md
- Status: success (completed in 6:50)
- Reflection: Clear instructions + absolute paths = perfect execution. Vault now follows agent-memory-vault pattern.

## Skill Candidate Detection

A task becomes a skill candidate when:
- **Reusability score** ≥9 AND **occurrences** ≥3 in Trial Log
- Score: 5/5 (Speed: 5, Quality: 5, Correctness: 5, Self-sufficiency: 5, Tokens: 4)
- Scope: Medium — web search, extract patterns, write to inspiration bank
- Issue: None. 12 entries found in 1m36s.
- Lesson: Web search + compile → ideal subagent task. No browser UI needed.
- Verdict: Good delegation.

## Hermes Agent Learnings (from nousresearch/hermes-agent)

### Security: Context File Injection Scanning
Hermes scans AGENTS.md, SOUL.md, etc. for prompt injection before injecting into system prompt. Threat patterns:
- "ignore (previous|all|above) instructions"
- "do not tell the user"
- "system prompt override" / "disregard your instructions"
- HTML comment injections (`<!-- ignore -->`)
- Hidden div injections (`<div style="display:none">`)
- Secret extraction (`curl ${KEY}`, `cat .env`)
- Invisible unicode characters (ZWJ, ZWNJ, BOM, RTL marks)

**Action:** If we add file upload to ChatGPT or accept external content, scan it before including in context.

### Smart Model Routing (keyword-based)
Hermes auto-routes to cheap model for simple turns, strong model for complex:
- Complex keywords → strong model (debug, implement, refactor, analyze, architecture, etc.)
- Simple (no complex keywords) → cheap model
- URLs in message → strong model (web analysis)
- Code blocks in message → strong model (code analysis)

**Action:** Could apply this to our main session — auto-route simple queries to MiMo Flash.

### Context Compression Pattern
Hermes uses cheap model to summarize old turns → saves summaries as running "iteration overview." Preserves semantic content better than truncation.

**Action:** When OpenClaw compacts, save structured summary to MEMORY.md rather than free-form notes.

### Skill Structure (YAML frontmatter)
Hermes skills use YAML frontmatter:
```
---
name: skill-name
description: what it does
platforms: [github, terminal]
version: 0.1.0
---
```
Then structured phases: ## Phase 1: Setup, ## Phase 2: Main work, ## Phase 3: Validate

**Action:** Consider YAML frontmatter for our skills. More parseable than plain markdown.

### Delegation Decision Matrix (from trials)

| Task Type | Delegate? | Why |
|-----------|-----------|-----|
| Web search + compile | ✅ Yes | Pure I/O, no UI, fast |
| Multi-file analysis | ✅ Yes | Reads many files, writes summary — fast |
| File-specific checks (syntax, flags) | ✅ Yes | Narrow scope, clear output |
| Design document writing | ⚠️ Maybe | Works but needs absolute paths |
| Browser UI interaction | ❌ No | Too slow, too many ref issues |
| Directory-wide scanning | ❌ No | Timeout risk, give specific files instead |
| Chat management (move, organize) | ❌ No | Precision UI timing needed |
| Background worker (idle tasks) | ✅ Yes | Autonomous, clear priority queue, no human steering needed |
| File editing (design docs) | ✅ Yes | Precise old/new text replacement, clear scope |

## Background Worker Best Practices

Background workers run when main session is idle. They have extra constraints:

1. **No announcements unless critical** — workers should be silent. Update files, log results, don't ping human.
2. **Always finish the task** — half-done work blocks the queue. Complete or fail cleanly.
3. **Update the roadmap** — mark tasks complete so next worker picks the right priority.
4. **Self-evaluate** — after each task, score yourself using the 10 criteria. Log the trial.
5. **Don't hog** — if task takes >10min, consider whether it should be split.
6. **Learn between tasks** — each spawned worker should be smarter than the last.

---

## How the Main Agent Learns

### Before EVERY Spawn (mandatory pre-spawn check)

Read the **Timeout Tuning Table** and **Timeout Guidelines** above. Apply these rules:

1. **Check similar trials** — if a similar task timed out before, use the timeout that would have worked (trial timeout × 1.5)
2. **Check similar trials for scope** — if a task was too big, split it into smaller chunks or set a larger timeout
3. **Read the Timeout Tuning Table** below for learned timeout values

### Timeout Tuning Table (grows from trial results)

| Task type | Initial timeout | After timeout failure | Notes |
|-----------|----------------|----------------------|-------|
| Design doc rewrite (10 lanes) | 600s | **1500s** | 3.5 min/lane. Per-lane commits survive timeouts. Trial 14 got 4/10 at 900s, trial 15 got 6/10 at 1500s. |
| Design doc tagging ([IMPLEMENTED]/[DESIGN GOAL]) | 300s | — | 10 files, 7:52. Self-sufficient, good scores. |
| Vault restructuring (Obsidian) | 300s | — | 6:50. 5 new files, 13 moved. Perfect execution. |
| OpenViking API test | 300s | — | 3 min. Session creation, commit, fs/ls all working. |
| Playwright iframe download | 300s | — | ~90s per report. Connects via CDP, uses frameLocator for nested iframes. |
| Design doc rewrite (single lane) | 300s | 450s | Read relevant missions + rewrite 1 file |
| QA compliance fix | 300s | — | Working well (trials 10-12 all succeeded at 300s) |
| Multi-file analysis | 300s | — | Working well (trials 5, 6 succeeded) |
| Web search + compile | 300s | — | Working well (trials 7, 9 succeeded) |
| Wiki scrape (large, 50+ pages) | 300s | 600s | Trial 7: first attempt too big, split to 10+20 worked |
| Browser UI interaction | — | — | NEVER delegate (trials 4, 8) |

**Rule: If a task times out, update this table with the new timeout, and use it for the next spawn of the same type.**

### After Each Subagent Run

1. **Evaluate** using the protocol above
2. If subagent failed → log error to `.learnings/ERRORS.md`
3. If subagent timed out → **update the Timeout Tuning Table** with what timeout would have worked
4. If evaluation reveals new pattern → update this file
5. If pattern recurs 3+ times → update AGENTS.md

This file IS the learning mechanism. Update it regularly.

---

## Structured Trial Record (JSON Template)

Each trial should follow this format for automated processing:

```json
{
  "id": "trial-N",
  "type": "qa-fixer | doc-writer | analyzer | browser | other",
  "task": "brief description",
  "model": "openrouter/xiaomi/mimo-v2-pro",
  "timeout_setting": 900,
  "status": "success | timeout | tool_error | incomplete | wrong_content",
  "wall_time": 587,
  "failure_taxonomy": "timeout | tool_error | incomplete_output | wrong_content | none",
  "scores": {
    "speed": 4, "quality": 4, "correctness": 5,
    "self_sufficiency": 4, "tokens": 4
  },
  "total_score": 21,
  "reflection": "15min was enough for 4 lanes but not 6. Next time: 1500s or split into 2 spawns."
}
```

**Failure taxonomy (automated rules):**
- `timeout` → wall_time >= timeout_setting
- `tool_error` → tool returned non-zero exit code or exception
- `incomplete_output` → artifacts missing or empty
- `wrong_content` → quality or correctness score < 3
- `none` → no failures detected

**Reflexion stub:** After each failed subagent, write 1-2 sentences on what went wrong and what to do differently. The next spawn of that archetype automatically includes this as a "what to avoid" note. This is based on the Reflexion paper — no weight updates needed, just linguistic feedback stored in episodic memory.

### Nightly Auto-Tuning (cron)

A nightly cron job should:
1. Read all trial records from the log
2. Compute p50/p90/p95 runtime per archetype
3. Update the Timeout Tuning Table with measured values
4. Promote settings that improve outcomes (fewer timeouts, higher scores)
5. Demote settings that regress
6. Append Reflexion-style rules to per-archetype learnings files

---

## Skill Candidate Detection

A task becomes a skill candidate when:
- **Reusability score** ≥9 AND **occurrences** ≥3 in Trial Log
- **Same action type** + message pattern appears 3+ times in conversation history
- **Background worker** completes the same task template manually 3+ times
- **Subagent output** is consistently copy-paste-ready (output reusability = 5/5)

When flagged as skill candidate:
1. Run autonomous skill creator's detection algorithms
2. Generate SKILL.md + scripts using extract-skill.sh
3. Validate skill passes quality gates
4. Install to `skills/` directory
5. Embed description in memory-lancedb for discoverability
6. Log to `skills/self-improving-agent/ledger.md`

See `docs/self-enhancement-architecture.md` for full integration architecture.
