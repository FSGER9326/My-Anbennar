# browser-lease-manager

**Plugin:** `browser-lease-manager`
**CLI:** `openclaw lease list | show <id> | release <id> | break <id> | status`

**Purpose:** Own hot-tab lifecycle, prevent session bleed, enable recovery.

---

## Why Leases?

Without leases, browser sessions leak across tasks:
- Task A opens chatgpt.com → gets a tab
- Task B also tries chatgpt.com → creates a second tab (same-origin conflict)
- Both tasks fight over both tabs → race conditions, stale refs, auth conflicts

**Lease model:** One tab per `{origin, account, proxyId, profile}`. Only one task can own a lease at a time.

---

## Lease Anatomy

```typescript
interface Lease {
  id: string;              // UUID — use to release/break
  origin: string;         // e.g. "chatgpt.com"
  account: string;        // e.g. "primary" or session hash
  profile: string;        // browser profile name
  proxyId?: string;       // optional proxy identifier
  targetId: string;       // actual browser tab targetId
  tabUrl: string;         // current URL in tab
  createdAt: number;      // Unix ms
  lastHealthAt: number;   // last healthy activity
  failureCount: number;    // consecutive failures on this lease
  state: 'active' | 'cooldown' | 'retired';
  cooldownUntil?: number; // if in cooldown, until when
  metadata?: Record<string, any>;
}
```

---

## State Machine

```
active ──(failure)──→ cooldown ──(timer)──→ active
   │                      │
   │                      └──(retire_lease)──→ retired
   │
   └──(retire_lease)──→ retired
   └──(close_tab)──→ retired
```

**States:**
- `active`: Tab is hot, healthy, ready for use
- `cooldown`: Tab had a transient failure (429, timeout). Wait N seconds before retry
- `retired`: Hard failure (hard_block, auth_expired). Tab is done. Create new lease

---

## Failure Handling (from browser-lease-recovery SKILL.md)

| Class | State Change | Retry? |
|-------|-------------|--------|
| stale_ref | active (resnapshot) | Yes — with fresh refs |
| soft_429 | → cooldown (30s) | Yes after cooldown |
| hard_block | → retired | **No** — retire immediately |
| auth_expired | → retired | **No** — retire immediately |
| overlay | active (dismiss overlay) | Yes after dismiss |
| app_busy | active (wait) | Yes after wait |
| completion_pending | active (more wait) | Yes with more time |

**Circuit breaker:** After 3 consecutive failures → auto-retire. Alert human.

---

## CLI Commands

```bash
# List all active leases
openclaw lease list

# Show detailed info for a lease
openclaw lease show <lease-id>

# Release a lease cleanly (close tab, mark retired)
openclaw lease release <lease-id>

# Break a lease (hard failure — no graceful close)
openclaw lease break <lease-id>

# Quick health status
openclaw lease status

# Acquire a new lease (acquireTab equivalent)
openclaw lease acquire --origin chatgpt.com --profile openclaw

# Release all leases for an origin
openclaw lease release-origin --origin chatgpt.com
```

---

## Session Handoff Integration

**Critical:** The lease `targetId` must survive session restarts.

At end of session (from SESSION_HANDOFF.md):
```yaml
browser:
  active_lease:
    id: "550e8400-e29b-41d4-a716-446655440000"
    origin: "chatgpt.com"
    account: "primary"
    profile: "openclaw"
    targetId: "CDPSession-1234"
    tabUrl: "https://chatgpt.com/c/abc123"
    createdAt: 1743544800000
    lastHealthAt: 1743544900000
    failureCount: 0
    state: "active"
```

On session start (from BOOTSTRAP.md):
```yaml
browser:
  resume_lease:
    id: "550e8400-e29b-41d4-a716-446655440000"
    origin: "chatgpt.com"
    targetId: "CDPSession-1234"
```

---

## Recovery Scenarios

### Scenario 1: Tab Crashed
```
Signal: targetId not found
Action:
  1. lease.show(<id>) → verify tab is gone
  2. If another tab on same origin exists → reassign targetId
  3. If no tab exists → acquireTab() → new targetId
  4. browser snapshot → fresh refs
  5. Resume task
```

### Scenario 2: Auth Expired
```
Signal: redirected to /login mid-task
Action:
  1. lease.break(<id>) → retire immediately (no retry)
  2. Alert human: "Session expired, need login"
  3. Human logs in
  4. lease.acquireTab() → new lease
  5. Resume task
```

### Scenario 3: Soft 429
```
Signal: HTTP 429 response
Action:
  1. lease.cooldown(30s) → state = cooldown, cooldownUntil = now + 30s
  2. Wait 30s
  3. lease.resume() → state = active
  4. Retry once
  5. If still 429 → lease.break() → retire, alert human
```

### Scenario 4: Circuit Break (3 failures)
```
Signal: failureCount >= 3
Action:
  1. lease.break(<id>) → retire immediately
  2. Alert human: "Circuit break on chatgpt.com lease — 3 consecutive failures"
  3. Log full failure signature to .learnings/browser-lease-failures.md
  4. Do NOT retry autonomously
```

---

## Storage

Leases are stored in:
```
~/.openclaw/state/browser-leases.json
```

Format:
```json
{
  "leases": {
    "<lease-id>": { ... Lease object ... }
  },
  "index": {
    "chatgpt.com:primary:openclaw": "<lease-id>"
  }
}
```

The index maps `{origin:account:profile}` → leaseId for fast lookup.

---

## Usage in OpenClaw Prompts

When the agent needs to use a browser tab:

```
Before browser action:
  1. Check lease for target origin → get targetId
  2. If no lease → acquireTab() → new lease
  3. browser snapshot profile=openclaw (validate tab is alive)
  4. Proceed with action

After browser action:
  1. Evaluate failure class
  2. If failure → apply lease state machine
  3. If retired → acquire new lease or alert human
  4. Update lastHealthAt on success
```

---

## Key Files

- `src/lease-store.ts` — Lease CRUD + persistence (JSON file)
- `src/lease-cli.ts` — CLI commands (list, show, release, break)
- `src/recovery.ts` — Failure classification + state machine
- `SKILL.md` — This file
