#!/bin/bash
# OpenClaw Health Analyzer
# Collects diagnostics and outputs a structured health report
# Used by cron jobs and heartbeat checks

echo "=== OpenClaw Health Report ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# 1. Gateway status
echo "--- Gateway Status ---"
openclaw gateway status --json 2>&1 || echo "GATEWAY_OFFLINE"

# 2. System status
echo ""
echo "--- System Status ---"
openclaw status --json 2>&1 || echo "STATUS_FAILED"

# 3. Gateway probe
echo ""
echo "--- Gateway Probe ---"
openclaw gateway probe 2>&1 || echo "PROBE_FAILED"

# 4. Channel health
echo ""
echo "--- Channel Health ---"
openclaw channels status --probe 2>&1 || echo "CHANNEL_CHECK_FAILED"

# 5. Task audit
echo ""
echo "--- Task Audit ---"
openclaw tasks audit --json 2>&1 || echo "TASKS_FAILED"

# 6. Running tasks
echo ""
echo "--- Active Tasks ---"
openclaw tasks list --json 2>&1 || echo "TASK_LIST_FAILED"

# 7. Cron status
echo ""
echo "--- Cron Status ---"
openclaw cron status 2>&1 || echo "CRON_FAILED"

# 8. Memory status
echo ""
echo "--- Memory Status ---"
openclaw memory status 2>&1 || echo "MEMORY_FAILED"

# 9. Plugin status
echo ""
echo "--- Plugin Status ---"
openclaw plugins list 2>&1 || echo "PLUGINS_FAILED"

# 10. Recent errors from logs
echo ""
echo "--- Recent Errors (last 50 lines, filtered) ---"
openclaw logs 2>&1 | tail -50 | grep -iE "error|fatal|warn|fail|denied|timeout|crash" || echo "NO_ERRORS_FOUND"

# 11. Resource usage
echo ""
echo "--- Resource Usage ---"
echo "Node processes:"
ps aux | grep -i "openclaw\|node" | grep -v grep | head -10 2>/dev/null || echo "PS_FAILED"
echo ""
echo "Ollama processes:"
ps aux | grep -i ollama | grep -v grep | head -5 2>/dev/null || echo "NO_OLLAMA"

echo ""
echo "=== End Health Report ==="
