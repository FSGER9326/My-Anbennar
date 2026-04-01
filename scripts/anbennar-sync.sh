#!/bin/bash
# Anbennar Upstream Sync Analyzer
# Fetches recent upstream commits and categorizes changes
# Safe to pull vs needs review

UPSTREAM_URL="https://gitlab.com/Sando13/anbennar-eu4-dev.git"
UPSTREAM_BRANCH="new-master"
LOCAL_DIR="C:/Users/User/Documents/GitHub/My-Anbennar"
WORKSPACE="C:/Users/User/.openclaw/workspace"
REPORT="$WORKSPACE/docs/anbennar-upstream-report.md"

cd "$LOCAL_DIR"

echo "=== Anbennar Upstream Sync Report ===" > "$REPORT"
echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$REPORT"
echo "" >> "$REPORT"

# Get latest upstream commit hash
echo "## Latest Upstream Commits" >> "$REPORT"
echo "" >> "$REPORT"

# Use GitLab API to get last 20 commits
curl -s "https://gitlab.com/api/v4/projects/Sando13%2Fanbennar-eu4-dev/repository/commits?ref_name=new-master&per_page=20" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for c in data:
    print(f\"- [{c['short_id']}] {c['title']} ({c['created_at'][:10]}) by {c['author_name']}\")
    print(f\"  URL: {c['web_url']}\")
" >> "$REPORT"

echo "" >> "$REPORT"
echo "## File Change Summary (Last 20 Commits)" >> "$REPORT"
echo "" >> "$REPORT"

# Get file changes from each commit
for commit_id in $(curl -s "https://gitlab.com/api/v4/projects/Sando13%2Fanbennar-eu4-dev/repository/commits?ref_name=new-master&per_page=20" | python3 -c "import json,sys; [print(c['id']) for c in json.load(sys.stdin)]"); do
    title=$(curl -s "https://gitlab.com/api/v4/projects/Sando13%2Fanbennar-eu4-dev/repository/commits/$commit_id" | python3 -c "import json,sys; print(json.load(sys.stdin)['title'])" 2>/dev/null)
    files=$(curl -s "https://gitlab.com/api/v4/projects/Sando13%2Fanbennar-eu4-dev/repository/commits/$commit_id/diff?per_page=50" | python3 -c "
import json, sys
data = json.load(sys.stdin)
files = [d['new_path'] for d in data]
# Categorize
gfx = [f for f in files if 'gfx/' in f.lower() or '.dds' in f.lower() or '.tga' in f.lower()]
ui = [f for f in files if 'custom_gui' in f.lower() or 'interface' in f.lower() or '.gui' in f.lower()]
localisation = [f for f in files if 'localisation' in f.lower() or '.yml' in f.lower()]
common = [f for f in files if 'common/' in f.lower()]
events = [f for f in files if 'events/' in f.lower()]
missions = [f for f in files if 'missions/' in f.lower()]
verne = [f for f in files if 'verne' in f.lower() or 'a33' in f.lower()]

parts = []
if gfx: parts.append(f'GFX({len(gfx)})')
if ui: parts.append(f'UI({len(ui)})')
if localisation: parts.append(f'LOC({len(localisation)})')
if common: parts.append(f'COMMON({len(common)})')
if events: parts.append(f'EVENTS({len(events)})')
if missions: parts.append(f'MISSIONS({len(missions)})')
if verne: parts.append(f'VERNE_TOUCHED⚠️')
print(', '.join(parts) if parts else f'OTHER({len(files)})')
" 2>/dev/null)
    echo "- **$title** → $files" >> "$REPORT"
done

echo "" >> "$REPORT"
echo "## Recommended Merges" >> "$REPORT"
echo "" >> "$REPORT"
echo "Files safe to cherry-pick (non-Verne, non-country-specific):" >> "$REPORT"
echo "- common/ancestor_personalities/" >> "$REPORT"
echo "- common/ruler_personalities/00_core.txt" >> "$REPORT"
echo "- common/event_modifiers/anb_misc_modifiers.txt" >> "$REPORT"
echo "- common/estate_privileges/anb_privileges.txt (if no Verne estates)" >> "$REPORT"
echo "- common/on_actions/00_on_actions.txt (if no Verne events)" >> "$REPORT"
echo "" >> "$REPORT"
echo "**Always review:**" >> "$REPORT"
echo "- common/scripted_effects/ (may affect Verne spells/effects)" >> "$REPORT"
echo "- common/custom_gui/magic_menu.txt (province ID changes)" >> "$REPORT"
echo "- common/mercenary_companies/ (check for Verne mercs)" >> "$REPORT"
echo "" >> "$REPORT"
echo "## Integration Command" >> "$REPORT"
echo "" >> "$REPORT"
echo '```' >> "$REPORT"
echo 'cd C:/Users/User/Documents/GitHub/My-Anbennar' >> "$REPORT"
echo 'git fetch upstream' >> "$REPORT"
echo '# Safe cherry-pick (example):' >> "$REPORT"
echo 'git cherry-pick <commit-hash>  # Review first!' >> "$REPORT"
echo '# Or merge specific files:' >> "$REPORT"
echo 'git checkout upstream/new-master -- common/ancestor_personalities/' >> "$REPORT"
echo 'git checkout upstream/new-master -- common/ruler_personalities/00_core.txt' >> "$REPORT"
echo '```' >> "$REPORT"

echo "Report written to $REPORT"
