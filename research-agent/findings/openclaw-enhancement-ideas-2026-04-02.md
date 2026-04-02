# OpenClaw Enhancement Ideas — Web Research 2026-04-02

*Researched by: Archivist (research-agent build session)*
*Sources: GitHub releases, dev.to, Medium, comparison articles*

---

## High-Impact Enhancements for This Workspace

### 1. Persistent Browser Sessions
**What:** Multi-step browser automation with tab state persistence.
**Why:** Current browser tool is useful but stateless between calls. Community reviews flag browser continuity as a key gap.
**How:** Use the existing CDP (Chrome DevTools Protocol) profile — `chrome-cdp` is already configured in openclaw.json. Could layer tab-snapshot and tab-restore on top.
**Effort:** Medium. Skill-sized project.
**Source:** dev.to review, comparison articles.

### 2. Vector Memory / Knowledge Base
**What:** RAG-style knowledge retrieval across EU4 modding docs.
**Why:** LanceDB is already in config (`plugins.entries.memory-lancedb`) but disabled. Re-enabling with nomic-embed-text (already configured for memory search) would give the agent long-term memory beyond files.
**How:** Enable memory-lancedb plugin, add docs/ folder to extraPaths, configure temporal decay.
**Effort:** Low. Config change + validation.
**Source:** openclaw.json config review.

### 3. Shared Knowledge Base for Multi-Agent
**What:** A shared `knowledge/` folder both main and research-agent can read/write.
**Why:** OpenClaw's agent isolation is a strength but makes cross-agent knowledge sharing awkward. A shared knowledge base would let research-agent write findings the main agent can retrieve contextually.
**How:** Add `knowledge/` to both agents' `memorySearch.extraPaths`.
**Effort:** Low. Config + directory setup.
**Source:** Architecture review.

### 4. Tailscale Remote Gateway
**What:** Change `gateway.bind` from `loopback` to `tailscale` mode.
**Why:** Currently gateway is loopback-only — can't access from phone/tablet remotely. Tailscale mode would enable secure remote companion pairing without exposing to internet.
**How:** Set `gateway.tailscale.mode: "on"` in openclaw.json. Requires Tailscale installed on host.
**Effort:** Low-Medium. Config + Tailscale installation.
**Security note:** Must keep `gateway.auth.token` strong; remote access = attack surface increase.
**Source:** openclaw.json config review.

### 5. /tasks Chat-Native Task Board
**What:** Use the new `/tasks` command (v2026.4.1) to track research agent todos.
**Why:** v2026.4.1 shipped `/tasks` as a chat-native background task board. The research agent could use this to surface its own pending work.
**How:** Explore `/tasks` interface; integrate into research cycle for tracking long-running research items.
**Effort:** Low. Exploration + documentation.
**Source:** GitHub release notes.

### 6. Clawhub.ai Skill Publishing
**What:** Package and publish workspace skills to clawhub.ai.
**Why:** clawhub.ai is live but empty. Publishing this workspace's skills (eu4-modding, self-improving-agent extensions) would help others and build discoverability.
**How:** `openclaw skills publish` or similar; requires researching clawhub publishing flow.
**Effort:** Medium. Research + package + publish.
**Source:** clawhub.ai audit.

### 7. Skills Auto-Discovery
**What:** Automated skill auditing and stale-skill detection.
**Why:** 52 npm skills + 23 workspace skills catalogued. No automated way to know which are broken, outdated, or superseded.
**How:** Script that runs `openclaw skills list` + checks each skill's SKILL.md exists and is non-empty; flags orphaned or empty skills.
**Effort:** Medium. Scripting + reporting.
**Source:** Skills audit findings.

---

## Findings from Community Reviews

### OpenClaw Strengths (cited across 6+ reviews)
- Channel routing is best-in-class (20+ channels)
- Self-hosted = predictable cost
- SOUL.md identity system is distinctive and powerful
- MIT license, no vendor lock-in
- Agent isolation prevents cross-contamination

### OpenClaw Weaknesses (cited consistently)
- Documentation gaps (especially multi-agent workflows)
- Multi-agent coordination requires manual setup
- Cron session management could be more visible
- Browser automation lacks persistent sessions
- Skills marketplace (clawhub.ai) underutilized

### AutoGPT Comparison
- AutoGPT has visual workflow builder (2025+)
- OpenClaw more stable and cost-predictable
- AutoGPT better for autonomous exploration; OpenClaw better for controlled, channel-integrated work
- AgentGPT = hosted AutoGPT (cloud, no self-host)

---

## Priority Recommendation

1. **Immediate:** Enable LanceDB memory (already configured, just disabled) — highest bang-for-buck
2. **This week:** Explore `/tasks` (v2026.4.1 new feature) for research tracking
3. **This week:** Set up Tailscale gateway mode for remote companion access
4. **Next sprint:** Browser tab persistence skill
5. **Later:** Clawhub.ai skill publishing
