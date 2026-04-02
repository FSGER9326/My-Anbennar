# browser-lease-recovery

**When to use:** Browser action fails, tab crashes, navigation breaks, auth expires, rate limit hit.

**Recovery ladder — try in order. Never retry without a strategy.**

---

## Recovery Ladder (in order)

### Step 1: Stale ref after navigation
```
Problem: browser act fails because refs changed after nav/render
Signal: element not found, ref invalid
Action: 
  1. browser snapshot (get fresh refs)
  2. re-resolve target element
  3. retry action
```
✅ **Resolve rate: ~60% of failures**

---

### Step 2: Tab targetId gone / tab crashed
```
Problem: tab closed, crashed, or navigation lost targetId
Signal: targetId not found error
Action:
  1. browser tabs → list current tabs
  2. find tab on same URL or re-navigate
  3. lease.acquireTab() → new targetId
  4. browser snapshot → fresh refs
  5. retry from step 1
```
✅ **Resolve rate: ~20% of failures**

---

### Step 3: Soft 429 (rate limit, try again shortly)
```
Problem: server throttled the request
Signal: HTTP 429, "too many requests", retry-after header present
Action:
  1. Read Retry-After header if available
  2. If no header: wait 30s
  3. Retry once only
  4. If still 429 → escalate to Step 4
```
⚠️ **Escalate after 1 retry. Never spin loop on 429.**

---

### Step 4: Hard block / challenge / CAPTCHA
```
Problem: server blocked the session, not just throttled
Signal: CAPTCHA iframe, challenge page, 403/451, login redirect
Action:
  1. Log failure class: 'hard_block'
  2. browser screenshot → capture challenge
  3. RETIRE LEASE immediately (session is cooked)
  4. If human present: alert and wait
  5. If autonomous: acquire new lease and retry from start
```
🚨 **Never retry a blocked session. Retire immediately.**

---

### Step 5: Auth expired / session invalid
```
Problem: cookies expired, session invalidated, re-login required
Signal: redirected to /login, auth token 401, session cookie gone
Action:
  1. Log failure class: 'auth_expired'
  2. If human present: alert with login needed
  3. If autonomous: attempt re-auth if credentials available
  4. Otherwise: retire lease, alert human
```
🚨 **Session is invalid. Do not continue with stale auth.**

---

### Step 6: 3+ failures in a row / circuit break
```
Problem: same action failed 3 times
Signal: failure_count >= 3 on current lease
Action:
  1. Open circuit breaker
  2. Log full failure signature to .learnings/
  3. Alert human with diagnostic info
  4. Stop autonomous retry
```
🔴 **Circuit open = stop. Human must assess.**

---

## Failure Classification (llm-task)

For ambiguous failures, use llm-task to classify:

```javascript
// Input: failure context (error message, screenshot text, URL)
{
  "error": "403 Forbidden",
  "url": "https://chatgpt.com/api/chat",
  "hasCaptcha": false,
  "redirectedToLogin": false,
  "responseBody": "..."
}

// Output (JSON-only, no tools):
{
  "class": "hard_block", // stale_ref | soft_429 | hard_block | auth_expired | overlay | app_busy | completion_pending
  "confidence": 0.9,
  "action": "retire_lease",
  "retry": false
}
```

**Use llm-task for this — it's a micro-decision, not a full reasoning loop.**

---

## Per-Failure-Class Actions

| Class | Session | Retry | Action |
|-------|---------|-------|--------|
| stale_ref | Keep | Yes (with resnapshot) | Re-snapshot and retry |
| soft_429 | Keep | Yes (30s delay) | Backoff and retry once |
| hard_block | **Retire** | No | New lease + alert |
| auth_expired | **Retire** | No | Re-auth or alert |
| overlay | Keep | Yes (dismiss overlay) | Click away + retry |
| app_busy | Keep | Yes (wait) | Wait + retry |
| completion_pending | Keep | Yes | More wait time |

---

## Alert Conditions

Always alert human (don't自治) when:
- hard_block detected
- auth_expired
- 3+ consecutive failures (circuit open)
- Rate limit hit on a critical flow (can't complete job)

Alert format:
```
🚨 [Browser Failure] class: hard_block
   URL: https://chatgpt.com/api/chat
   Action: Lease retired
   Next: Need human to verify they're not blocked at chatgpt.com
```

---

## Quick Reference

```
RECOVERY LADDER (always in order):

1. Stale ref    → resnapshot → retry           (~60% of failures)
2. Tab gone     → re-acquire tab → retry      (~20%)
3. Soft 429     → 30s backoff → retry once    (escalate if persists)
4. Hard block   → RETIRE lease → alert         (NEVER retry)
5. Auth expired → RETIRE lease → alert        (NEVER retry)
6. 3 failures   → circuit open → alert         (STOP autonomous retry)

Never spin loop. Never retry a hard_block or auth failure.
```
