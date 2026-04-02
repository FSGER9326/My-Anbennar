# Research Agent Error Log

<!-- Auto-written by research-agent. Append only, never delete. -->

## Errors Encountered

### 2026-04-02 — research-agent run 1
- **Error**: GitHub URL guessed wrong (github.com/openclaw/openclaw was correct but agent tried a different path)
- **Error**: clawhub.ai returned empty/no content on initial visit
- **Error**: Thread=true unavailable — "no channel plugin registered subagent_spawning hooks"
- **Fix**: Use isolated cron sessions instead of thread-based persistent sessions

### 2026-04-02 — research-agent run 3
- **Error**: Timeout after 2m12s — "Good progress. Let me fetch the releases page…"
- **Cause**: Subagent ran out of time before completing web fetches
- **Fix**: Spawn with longer runTimeoutSeconds or break work into smaller cycles

### 2026-04-02 — mkdir via PowerShell
- **Error**: `mkdir -p path1 path2` fails on Windows (positional param error)
- **Fix**: Use PowerShell `New-Item -ItemType Directory -Path X -Force` for each directory separately

### 2026-04-02 — Gateway Status Exec
- **Error**: SIGKILL on the status exec probe itself
- **Cause**: The exec was killed, not the gateway
- **Status**: Gateway itself was healthy throughout (RPC probe: ok)
