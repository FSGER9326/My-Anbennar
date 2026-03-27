# Upstream Update Adaptation Playbook

Use this whenever Anbennar dev updates and your branch must catch up.

## 1) Sync and open an adaptation branch

```bash
git checkout work
git fetch origin
git merge origin/main
# or: git rebase origin/main
```

If conflicts appear, resolve them, then:

```bash
git add <resolved-files>
git commit
```

## 2) Revalidate highest-risk systems first

Start with systems marked `High` in:

- `docs/wiki/anbennar-base-vs-verne-change-ledger.md`

Typical high-risk files:

- shared idea files
- shared on_actions
- shared Verne flavor events
- shared mercenary/monument definitions

## 3) Update ledger statuses

For each touched system:

- set status to `NEEDS_REVALIDATION` during review
- move back to `IMPLEMENTED` after quick tests pass
- mark `BROKEN` with a short failure note if still unresolved

## 4) Conflict resolution tips for noob-friendly workflow

- Resolve one file at a time.
- Keep base Anbennar logic unless your mod explicitly replaces it.
- Prefer appending clearly marked Verne blocks over rewriting large shared sections.
- After each resolved file, run:

```bash
git diff --check
```

## 5) Final checklist before push

- [ ] No merge markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- [ ] Ledger updated for every mechanic change
- [ ] PR description includes what changed because of upstream update
