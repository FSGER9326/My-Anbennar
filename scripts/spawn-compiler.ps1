# spawn-compiler.ps1 — Task-specific context capsule generator
# Usage: .\spawn-compiler.ps1 -TaskType qa_verify -OutputPath capsule.json
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('researcher','coder','verifier','memory_writer','planner','worker')]
    [string]$TaskType,
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = "$env:TEMP\openclaw_spawn_manifest.json"
)

$WORKSPACE = "C:\Users\User\.openclaw\workspace"
$REPO      = "C:\Users\User\Documents\GitHub\My-Anbennar"

# Stable role pack — always included
$STABLE = @{
    repo_root     = $REPO
    workspace_root = $WORKSPACE
    constraints   = @('no raw exec without approval', 'use absolute paths', 'log all tool outputs')
    output_contract = 'Return: DONE | BLOCKED | NEED_CONTEXT(key) | RETRYABLE_FAILURE + artifact path'
}

# Task capsules — narrow, no fluff
$CAPSULES = @{
    researcher = @{
        goal       = 'Web search, fetch, summarize. Return artifact path + 3-line summary.'
        tools      = @('web_search','web_fetch','read','write')
        exclude    = @('exec','browser','cron','gateway','canvas','image')
        contexts   = @("$WORKSPACE\SOUL.md", "$WORKSPACE\USER.md")
        retrieval_keys = @()
        budgets    = @{ tool_calls = 12; time_s = 300 }
    }
    coder = @{
        goal       = 'Implement code/mod file changes from spec. Return artifact path + diff summary.'
        tools      = @('read','write','edit','exec')
        exclude    = @('browser','cron','gateway','canvas','image','web_search')
        contexts   = @("$WORKSPACE\SOUL.md", "$WORKSPACE\USER.md")
        retrieval_keys = @('diff:current-branch','active_work')
        budgets    = @{ tool_calls = 20; time_s = 600 }
    }
    verifier = @{
        goal       = 'Run checks, compare to acceptance criteria. Return PASS/FAIL + evidence artifact.'
        tools      = @('read','exec')
        exclude    = @('write','browser','cron','gateway','canvas','image','web_search')
        contexts   = @("$WORKSPACE\SOUL.md")
        retrieval_keys = @('diff:current-branch','acceptance_criteria')
        budgets    = @{ tool_calls = 8; time_s = 300 }
    }
    memory_writer = @{
        goal       = 'Compress trial result into ledger. Return DONE + entry summary.'
        tools      = @('read','write')
        exclude    = @('exec','browser','cron','gateway','canvas','image','web_search','web_fetch')
        contexts   = @("$WORKSPACE\SOUL.md")
        retrieval_keys = @('trial_log','ledger_path')
        budgets    = @{ tool_calls = 5; time_s = 120 }
    }
    planner = @{
        goal       = 'Decompose work into DAG, allocate slots. Return task list + priority scores.'
        tools      = @('read','write','web_search','web_fetch')
        exclude    = @('browser','gateway','canvas','image')
        contexts   = @("$WORKSPACE\SOUL.md", "$WORKSPACE\USER.md", "$WORKSPACE\MEMORY.md")
        retrieval_keys = @('active_work','roadmap','decisions')
        budgets    = @{ tool_calls = 15; time_s = 300; thinking = 'medium' }
    }
    worker = @{
        goal       = 'Execute one assigned task. No self-replanning. Return DONE + artifact.'
        tools      = @('read','write','edit','exec','web_search','web_fetch')
        exclude    = @('browser','gateway','canvas')
        contexts   = @("$WORKSPACE\SOUL.md")
        retrieval_keys = @()
        budgets    = @{ tool_calls = 10; time_s = 300 }
    }
}

$capsule = $CAPSULES[$TaskType]
if (-not $capsule) {
    Write-Error "Unknown task type: $TaskType"
    exit 1
}

$manifest = @{
    task_type    = $TaskType
    generated_at = (Get-Date -Format 'o')
    stable       = $STABLE
    goal         = $capsule.goal
    tools_allow  = $capsule.tools
    tools_deny   = $capsule.exclude
    contexts     = $capsule.contexts
    retrieval_keys = $capsule.retrieval_keys
    budgets      = $capsule.budgets
    output_contract = $STABLE.output_contract
}

$manifest | ConvertTo-Json -Depth 5 | Set-Content $OutputPath -Encoding UTF8
Write-Host "Spawn manifest written to: $OutputPath"
Write-Host "Tools allowed : $($capsule.tools -join ', ')"
Write-Host "Tools denied  : $($capsule.exclude -join ', ')"
Write-Host "Contexts      : $($capsule.contexts.Count) files"
Write-Host "Tool call cap : $($capsule.budgets.tool_calls)"
