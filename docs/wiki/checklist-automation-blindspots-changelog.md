# Checklist Automation Blindspots Changelog

Purpose: historical log of high-impact blindspots that were fixed in checklist automation.

## 2026-03 — baseline blindspot hardening

### Fixed

- Guard scope expanded beyond docs to include Python/PowerShell/Bash scripts, workflows, and `.gitattributes` conflict markers.
- Workflow path assumptions corrected where paths incorrectly prefixed the repo root (`My-Anbennar/...`).
- Wrapper script execution made explicit (`python`/`bash` invocation) instead of relying on executable-bit assumptions.
- Windows-native scaffold/profile entrypoints added where only Unix-like paths existed.
- PR sync helpers stopped creating merge commits when already up to date.
- Duplicated smoke logic moved toward JSON profile-driven checks as a clearer source of truth.

### Why this mattered

- Reduced silent CI drift and false-green outcomes.
- Improved cross-platform reliability for contributors.
- Lowered noisy merge churn from unnecessary sync commits.
- Kept smoke behavior consistent with tracked profile expectations.

## Usage note

For current operational commands, use the concise index:

- [checklist-automation-system.md](./checklist-automation-system.md)

For merge decision policy and fallback flow, use:

- [merge-conflict-prevention-playbook.md](./merge-conflict-prevention-playbook.md)
