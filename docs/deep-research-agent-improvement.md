# Improving Jordan on OpenClaw for Autonomous, Long-Running Modding Work

## Context and target outcomes
Your current architecture already contains most of the “right ingredients” for a production-grade agent: multiple memory stores (daily files + Obsidian + a knowledge graph), a subagent swarm pattern, trial logging, and scheduled maintenance jobs. The main gaps you described are not about adding more components, but about tightening the control loop: turning experience into durable state, and turning durable state into better next actions.

Across modern agent stacks, the common pattern is to treat “memory” as multiple layers with different purposes (short-term thread state vs cross-session long-term memory), plus explicit rules about when memory is written, retrieved, summarized, and trusted. LangChain (LangGraph) frames this directly as short-term “thread-scoped” memory persisted via a “checkpointer” so a thread can be resumed, alongside “long-term memory” in custom namespaces shared across threads. citeturn8view0 CrewAI similarly emphasizes recording content with inferred scope/importance and retrieving it with a composite score that combines semantic similarity, recency, and importance. citeturn8view1 Letta (MemGPT lineage) makes the “always-visible, structured core memory” explicit via editable “memory blocks” pinned into the context window. citeturn8view2

The actionable goal for this week is to implement a small set of invariants that make every new Jordan session feel “continuous” without requiring full chat replay:
- A deterministic “session bootstrap” that always loads the same compact state (identity, project status, open decisions, active constraints).
- Automatic write-back of decisions, mistakes, and reusable procedures into durable stores (files + OpenViking KG), with minimal human intervention.
- An evaluation + tuning loop that upgrades spawn defaults (timeouts, prompts, routing, tool budgets) based on measured outcomes rather than manual interpretation.
- A compaction strategy where “lifeboat state” is preserved even when raw chat is summarized or truncated (because long contexts both cost more and often degrade model performance). citeturn8view0turn7search0

## Session continuity and memory persistence
### What works in successful agent memory systems
When agents “start blank,” the root cause is typically that they are only relying on ephemeral conversational context rather than a persistent state object. Frameworks that solve this either (a) resume an explicit thread state, or (b) rehydrate the agent by retrieving durable memories into a fixed scaffold.

Concrete best-practice patterns you can borrow:

**Thread state + checkpointing (session continuity).** LangGraph’s short-term memory is part of an agent’s “state,” persisted through a checkpointer so the same thread can be resumed later. citeturn8view0 Even if OpenClaw doesn’t natively implement a LangGraph-style checkpointer, you can emulate it with a session state file keyed by a stable thread/session ID.

**Tiered memory (core vs searchable history vs archival).** MemGPT proposes multiple memory tiers to work around limited context, and Letta operationalizes this into persistent “core memory blocks” pinned to the prompt, plus other memory mechanisms outside-context. citeturn0search0turn8view2turn6search7 The key insight: the agent must have a *small always-on* memory that contains identity + working commitments, and a *large searchable* memory for everything else.

**Scoring that blends similarity, recency, and importance.** CrewAI’s memory retrieval ranks results using a composite score blending semantic similarity, recency, and importance (and it uses an LLM during “remember” to infer scope/categories/importance). citeturn8view1 The “Generative Agents” architecture similarly retrieves memories using a blend of relevance, recency, and importance, and then synthesizes higher-level reflections over time. citeturn5search0turn5search4 This is a strong match for your use case because modding work has both long-lived facts (project rules, lore constraints, coding conventions) and short-lived working state (what you changed today, what you decided 2 hours ago).

**A knowledge-graph-backed memory context string.** Zep’s memory API is a practical “production memory” pattern: `memory.get()` uses the latest messages in a session to determine what’s relevant from a user’s knowledge graph and returns a context string for prompting; Zep also recommends including the last few raw messages because ingestion may lag. citeturn8view3 This “KG-derived context + last messages” split maps cleanly onto your OpenClaw compaction problem.

### A concrete persistence design for Jordan on OpenClaw
You already have three stores. The missing piece is making them behave like a *single coherent memory subsystem* with explicit roles:

**Core memory (lifeboat, always loaded).** Adopt the Letta-style “memory blocks” idea even if you implement it as plain text/YAML in your Obsidian vault or a dedicated OpenClaw file. Core memory blocks are explicitly “pinned,” structured/labeled, editable, and persistent across conversations. citeturn8view2 For Jordan, the minimal viable blocks are:
- `persona`: how Jordan should behave as an autonomous modding assistant (tone, rigor level, tool discipline).
- `human`: Falk’s preferences (decision style, file layout, “don’t do X” rules).
- `project_state`: current overhaul goals, design decisions, active branches, known constraints.
- `active_work`: current sprint goals + the next 3 highest-priority tasks.

**Recall memory (searchable interaction history).** Index OpenClaw daily files + selected Obsidian notes as retrieval docs, with metadata fields `{timestamp, session_id, task_id, outcome, tags, importance}`. Use an approach analogous to time-weighted retrieval where “last accessed” (or last relevant) affects rank, mirroring the idea behind time-aware retrievers. citeturn5search1turn5search5

**Archival memory (high-latency, deep history).** Anything not needed for routine work (full logs, long discussions, raw tool traces) should remain in files/KG but not be injected unless a query demands it. MemGPT’s underlying premise is that memory tiers mitigate limited context windows by only bringing in what’s needed. citeturn0search0turn0search16

### What to implement this week for “no more blank sessions”
Implement a deterministic bootstrap that always runs at session start:

1) Load core memory blocks (lifeboat). Inspired by Letta’s design: pinned, labeled blocks that persist and can be updated. citeturn8view2  
2) Load “last session handoff” (a compact, structured summary of the previous session’s outcomes). This is close to the ReSum idea of periodically compressing interaction history into a compact reasoning state so the agent can continue without full replay. citeturn4search3turn4search7  
3) Retrieve top-K relevant recall memories based on the current user request + active tasks, using scoring that blends semantic similarity, recency, and importance (CrewAI-style). citeturn8view1turn5search4  
4) (Optional but high leverage) Retrieve KG facts relevant to the current task, and inject them in a stable “facts” section (see KG section below). This mirrors Zep’s “context string from KG + last raw messages” recommendation. citeturn8view3

The behavioral nuance you’re missing (“how we were reasoning yesterday”) usually lives in the lifeboat + handoff layers. If those are always loaded, the agent doesn’t need raw chat continuity to feel continuous.

## Automated subagent learning loop and parameter tuning
### What production systems do instead of manual trial interpretation
Your current loop creates trial data but doesn’t *close the loop* automatically. Modern production practice treats agent outputs like software artifacts: trace everything, evaluate automatically, and promote improvements through a controlled gate.

Three concrete exemplars you can borrow from:

**Observability + evaluation harnesses.** LangSmith positions itself as an integrated platform for observability and evaluation of LLM apps, supporting experiment comparison and production monitoring. citeturn2search0 OpenAI’s Evals framework similarly exists to run repeatable tests against model outputs and catch regressions when prompts/models/parameters change. citeturn2search1turn2search5 DeepEval packages a “unit test” style approach for LLM outputs (Pytest-like), enabling regression-style checks. citeturn2search3turn2search7turn2search11

**Learning from linguistic feedback (no weight updates).** Reflexion shows a concrete method for improving an agent without fine-tuning: generate a reflection based on feedback signals and store it in an episodic memory buffer to influence subsequent trials. citeturn1search3turn1search11 This matches your environment well because most of your “failures” are operational (timeouts, bad scoping, missed constraints), not missing world knowledge.

**Automated prompt/parameter optimization in a modular pipeline.** DSPy is explicitly built around optimizing prompts and (optionally) weights for modular LM programs, and includes “optimizers” and meta-optimizers that combine prompt optimization and weight optimization. citeturn1search6turn1search2turn1search10 Even if you don’t adopt DSPy wholesale, its philosophy is directly applicable: define the program signature + metric, then let an optimizer search for better configurations.

### A concrete “closed loop” design for your subagent swarm
Treat each subagent spawn as an experiment run with a structured record, then automate three steps: **classify → propose fix → promote**.

**Structured run record (minimum viable).** For each subagent execution, write a JSON record:
- Inputs: task type, prompt template ID, model, temperature, timeout settings, tool budget
- Outputs: status (success/fail), elapsed time, tokens, artifacts produced
- Quality signals: your 10-dimension score + an LLM-judge score for correctness/helpfulness (optional)
- Failure taxonomy: timeout, tool error, hallucinated file path, missed constraint, incomplete output
- “Reflection stub”: one paragraph explaining what should change next time (Reflexion-style) citeturn1search3

**Automated failure taxonomy.** Make failure labeling deterministic. Start with rule-based classification (timeout if wall time exceeded, “tool error” if tool returned nonzero, etc.), then add LLM labeling only for ambiguous cases. This reduces noisy learning.

**Promotion policy (what changes automatically).** Each night (cron):
- Compute rolling metrics per subagent archetype (e.g., QA-fixer, doc-writer, analyzer).
- If a setting improves outcomes beyond a threshold (e.g., fewer timeouts with no quality regression), promote it to the default spawn profile.
- If quality drops, roll back.

This is the same conceptual discipline behind eval-driven development: you don’t “feel” that changes helped; you measure via repeatable tests. citeturn2search5turn2search3

### How to tune timeouts and other parameters without guesswork
You mentioned you documented timeouts in a table but manually apply changes. Automate this with a simple policy (good enough for week one):

- Record the distribution of runtimes per subagent type (p50/p90/p95).
- Set default timeout to `p95 + safety_margin` for that archetype.
- If timeouts still occur, create an “early-warning” mechanism: at 70% of timeout, the subagent must emit a partial result + a continuation plan, then optionally request an extension. This is conceptually aligned with long-horizon continuity approaches that preserve partial state rather than failing hard. citeturn4search3

Then add multi-objective tuning:
- Optimize for **success rate** subject to **cost** and **latency** bounds.
- Use your 10-dimension score as a weighted utility function.
- Run nightly A/B tests of 2–3 candidate profiles per archetype on a fixed mini-suite of tasks (Evals/DeepEval style). citeturn2search5turn2search7

## Skill creation from repeated patterns that actually triggers
### Why your current “3+ occurrences → create skill” likely never fires
In agent systems, “pattern repetition” rarely appears as exact string matches. Tasks look different on the surface (different province/event names, different bug symptoms) but share an underlying structure. So a rule like “3 identical patterns” will under-detect.

Two practical sources point to better approaches:

- Voyager succeeds at continual capability growth by maintaining an *ever-growing skill library* of executable code and using an iterative mechanism that incorporates feedback/errors/self-verification to improve programs. citeturn3search0turn3search12 The key is that skills are discovered as *repeatable procedures*, not as repeated text.
- Sequential pattern mining research (e.g., PrefixSpan) is explicitly designed to discover frequent subsequences in event/sequence data such as web access patterns—exactly the kind of “tool-call and action sequence” logs your agent produces. citeturn3search3turn3search7

### A workable pattern detector for agent “skills”
Instead of counting repeated *tasks*, count repeated *trajectories*.

Define an event stream for every run:
- `intent_class` (e.g., QA fix, doc update, map history research)
- `tools_used` sequence (file search → open file → patch → run tests)
- `artifact_type` produced
- `failure_modes` encountered
- `time/cost` stats

Then run detection on **abstracted sequences**:
- Normalize tool calls into categories (READ, SEARCH, PATCH, TEST, SUMMARIZE).
- Normalize task entities (replace “Province X” with `<PROVINCE>` tokens).
- Cluster semantically similar intents (embedding clustering) before counting.

Now your “3+ occurrences” rule triggers on invariants like:
- SEARCH → READ → PATCH → TEST → WRITELOG
even if the exact content differs.

PrefixSpan-style mining is a proven approach for discovering frequent subsequences in sequence databases. citeturn3search3 For a first-week implementation, you don’t need full data-mining sophistication; even a sliding-window n-gram frequency count over normalized tool/action tokens will produce candidates.

### How to validate a skill template is worth creating
Use a **value gate** and a **risk gate** before auto-generating a skill.

**Value gate (must save effort).**
- Estimated time saved ≥ X minutes *and/or* reduces failures (timeouts, missed constraints).
- Appears in ≥ N runs across ≥ M days (avoid same-day repetition bias).

**Risk gate (must be safe to reuse).**
- Has stable inputs/outputs (clear parameters).
- Has a test or “self-check” step.

This is consistent with modern “skills as packages” guidance: Microsoft’s Agent Skills guidance suggests using a skill when you want the AI to figure out *how* to accomplish a task, but using a workflow when you must guarantee exact steps/order. citeturn3search2 That maps directly onto your auto-skill creator: only generate “skills” for tasks where some flexibility is acceptable, and where self-checks can keep it safe.

## Making OpenViking a real knowledge-graph memory layer
### What a KG buys you that files and embeddings don’t
A knowledge graph becomes valuable when your agent needs to answer questions like:
- “What decisions depend on this other decision?”
- “Which files are affected by this mechanic?”
- “What did we change, when, and why?”
- “Which constraints override others?”

Plain text retrieval is good at relevance; graphs are good at *relational traversal* and *structured summarization*.

GraphRAG is a concrete example of this direction: it extracts a knowledge graph from raw text, builds a community hierarchy, generates summaries for communities, and uses these structures during retrieval-augmented generation—positioning itself as a structured alternative to naive vector-only RAG. citeturn8view4turn1search8 LlamaIndex likewise promotes a “Property Graph Index” approach for building richer knowledge graphs and querying them flexibly (including hybrid search + Cypher). citeturn0search3turn0search11

### A minimal “agent memory KG schema” that will work for you
Your OpenViking server has “search, relations, sessions” but nothing writes to it. Fix that by defining a small schema that mirrors how you actually work.

Use four node types and a few edges:

- **Entity nodes:** `File`, `Feature`, `Decision`, `Issue`, `Task`, `LoreConstraint`
- **Session nodes:** `Session` (with timestamps, subagents involved, outputs)
- **Edges:**  
  - `DECISION_IMPLIES_DECISION`  
  - `DECISION_AFFECTS_FILE`  
  - `TASK_TOUCHES_FILE`  
  - `ISSUE_REPRODUCED_IN_SESSION`  
  - `TASK_RESOLVES_ISSUE`  
  - `FEATURE_CONSTRAINED_BY_LORE`

Add temporal validity where possible. Zep’s underlying KG framework (“Graphiti”) emphasizes that facts can include valid/invalid timestamps so agents can understand how relationships evolve over time—exactly what modding projects need as decisions get revised. citeturn6search4

### Write-path: how to make the KG fill itself
Copy a proven ingestion pattern:

- On each session, store recent messages/events, then derive structured facts and relationships.
- At query time, retrieve a “context string” derived from the graph that is relevant to the newest messages.

Zep’s `memory.get()` is a practical blueprint: it uses the *latest messages of the session* to determine what’s relevant from the user’s KG and returns a context string for prompting; the session is used for relevance, but retrieval can draw from any session for that user. citeturn8view3

For OpenViking, implement two write triggers:
- **Hot-path writes (immediate):** after a decision is made, after a task is marked done, after a bug is confirmed resolved.
- **Background consolidation (cron):** nightly extraction of entities/relations from daily logs into the KG, plus dedup/merge.

This mirrors LangChain/LangGraph’s framing that memory updates can happen “on the hot path” (agent decides to remember before responding) or in background tasks, each with tradeoffs. citeturn8view0

## Context compression without losing key facts, decisions, and rules
### Why compaction causes real losses
There are two separate problems:
- **Token limits** can produce irrecoverable errors if you try to stuff too much history into a prompt. citeturn8view0
- Even when the context fits, models often use long context poorly: “Lost in the Middle” shows performance can degrade significantly when relevant information is placed in the middle of a long context, with best performance often when key info is at the beginning or end. citeturn7search0turn7search12

So “just keep more chat” is often the wrong strategy. The winning strategy is: keep less raw chat, but keep *better state*.

### Effective compression strategies you can implement immediately
**Structured rolling summary buffers.** LlamaIndex’s ChatSummaryMemoryBuffer iteratively summarizes older messages to keep the chat history within a token limit, preserving recent messages in full while condensing older context. citeturn5search2turn5search10 This is a direct fix for the “OpenClaw compacts and I lose info” failure mode: your compactor should not produce prose summaries alone; it should produce a structured state object.

**Periodic “reasoning state” snapshots.** ReSum demonstrates a plug-and-play paradigm where an agent periodically compresses interaction history into compact summaries and resumes from these states to enable unbounded exploration. citeturn4search3turn4search7 Even though ReSum is focused on web agents, the underlying technique—periodic state snapshots—is exactly what you need for long-running modding sessions.

**Query-aware compression for retrieval.** LangChain’s ContextualCompressionRetriever expresses the core idea: given a query, return only the relevant documents and only the relevant parts of those documents. citeturn4search4turn4search0 This is critical when you retrieve from large notes/logs: context should be compressed around *the current question*, not globally.

**Prompt compression methods.** LLMLingua introduces coarse-to-fine prompt compression with a “budget controller” to preserve semantic integrity under high compression. citeturn1search1turn1search9 LongLLMLingua extends this idea for long-context scenarios and is motivated by the fact that performance depends on density/position of key information. citeturn4search1 You don’t need to run these exact models to benefit—this research supports the operational principle: compression should preserve key constraints and decisions, not conversational filler.

**Reordering to fight “lost in the middle.”** Both LangChain and LlamaIndex include “LongContextReorder” utilities explicitly motivated by “lost in the middle” effects, reordering retrieved nodes so key items appear near the beginning or end. citeturn7search1turn7search2turn7search0

### The “lifeboat document” structure that survives compaction
Treat your lifeboat as *core memory* (Letta-style pinned blocks) plus an operational handoff. citeturn8view2 A robust template is:

- **Identity & rules:** Jordan persona + “how I operate” constraints
- **User profile:** Falk preferences, formatting standards, risk tolerances
- **Project invariants:** non-negotiable lore/design constraints, directory conventions
- **Current commitments:** active tasks, open questions, deadlines
- **Decision ledger:** last ~20 decisions with “why” and “reversal conditions”
- **Failure learnings:** last ~10 recurring failure modes + the mitigations

The key is that the lifeboat is not “a summary”; it’s an *operational state object* the agent can execute from.

## One-week concrete improvement plan
This plan is designed to produce visible improvements in continuity, fewer repeated failures, and your first auto-generated skills—without needing to replace OpenClaw or rebuild everything.

### Build the session bootstrap and lifeboat core
Create a single canonical “Jordan Core Memory” file (or a small set of labeled blocks) and ensure it is always injected at session start, mirroring Letta’s “pinned, structured, editable memory blocks.” citeturn8view2 Add a second file called “Last Session Handoff” that is overwritten at the end of each session with a ReSum-style compact reasoning state (structured summary + next actions). citeturn4search3turn4search7

Deliverable by end of day: starting a new session loads (a) core lifeboat blocks and (b) last session handoff before any new work begins.

### Turn trial logs into an automatic tuning loop
Add a nightly cron job that reads your trial logs and updates subagent spawn profiles:
- Compute p95 runtime per subagent archetype and set timeouts accordingly.
- Promote/demote prompt templates based on success rate and your 10-dimension score.
- For each failure class, append a Reflexion-style “reflection rule” into a per-archetype learnings file, so the next spawn includes “what to avoid.” citeturn1search3turn1search11

Back this with a small evaluation harness. If you want a direct, lightweight path: implement Pytest-like checks using DeepEval concepts, or build a tiny custom suite and treat it like OpenAI Evals does—repeatable tests that catch regressions when you change prompts or parameters. citeturn2search7turn2search5turn2search1

Deliverable by end of day: at least one parameter (timeouts or default prompt variant) updates automatically based on yesterday’s data.

### Make skill creation trigger using trajectory mining
Instrument subagent runs to log normalized action/tool sequences (SEARCH/READ/PATCH/TEST/WRITELOG). Mine frequent subsequences weekly or nightly; PrefixSpan is a canonical approach for sequential pattern mining, but a simpler n-gram frequency counter is enough to start. citeturn3search3

When a candidate pattern appears, auto-generate a skill *only if*:
- it saves time or reduces failures (value gate), and
- it has a self-check/test step (risk gate), consistent with the “skill vs workflow” distinction in Agent Skills guidance. citeturn3search2turn3search0

Deliverable by end of day: one candidate skill proposal is automatically generated (even if you still require manual approval to activate it).

### Wire OpenViking as a write-through memory layer
Implement a minimal write API client and start writing only four things:
- Decisions (with rationale and timestamp)
- Tasks (status transitions)
- File touches (file path + reason)
- Session summaries (handoff)

Then implement a read function that retrieves “relevant facts” for the current task/request and injects them as a stable “KG context” section (Zep-style “context string”). citeturn8view3turn6search4

If you later want to go further, GraphRAG provides a roadmap: extract a graph from text, build a hierarchy, summarize communities, and use that at query time—useful when your corpus grows beyond simple retrieval. citeturn8view4turn1search8

Deliverable by end of week: OpenViking contains at least 50–100 structured nodes/edges derived from real work, and Jordan can pull “decision context” from it at bootstrap.

### Replace lossy compaction with controlled compression
Update OpenClaw’s compaction behavior by layering:
- A rolling structured summary buffer (LlamaIndex ChatSummaryMemoryBuffer-style) to keep history within budget without deleting it. citeturn5search2turn5search10
- Query-aware contextual compression for retrieved notes (ContextualCompressionRetriever concept). citeturn4search4turn4search0
- Reordering of retrieved items so the most important constraints/decisions appear at the start/end to mitigate “lost in the middle” effects. citeturn7search0turn7search2

Deliverable by end of week: compaction events no longer remove decisions/constraints because those always live in the lifeboat + KG, and retrieval is compressed/reordered rather than naively appended.

### What “better next week” should look like if this is working
If you implement the above, you should see three measurable improvements quickly:
- New sessions stop feeling blank because bootstrap always loads lifeboat + handoff + targeted retrieval (LangGraph-style persistence concept + Letta-style pinned memory). citeturn8view0turn8view2
- Timeout fixes stop being manual because runtime distributions and failure taxonomies drive automatic spawn adjustments, and Reflexion-style learnings are injected into subsequent runs. citeturn1search3
- Skill creation starts firing because you are detecting repeated *trajectories* rather than repeated text, aligning more closely with how Voyager-style skill libraries grow (procedures, not phrases). citeturn3search0turn3search12