#!/usr/bin/env bash
set -euo pipefail

MODE="manual"
STAGED=0
AGAINST=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="$2"
      shift 2
      ;;
    --staged)
      STAGED=1
      shift
      ;;
    --against)
      AGAINST="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

changed_files() {
  if [[ "${STAGED}" -eq 1 ]]; then
    git diff --cached --name-only --diff-filter=ACMRTUXB
    return
  fi

  if [[ -n "${AGAINST}" ]]; then
    git diff --name-only "${AGAINST}"...HEAD
    return
  fi

  if [[ "${MODE}" == "pre-push" ]]; then
    if upstream="$(git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null)"; then
      git diff --name-only "${upstream}"...HEAD
      return
    fi
  fi

  git diff --name-only HEAD
}

mapfile -t FILES < <(changed_files)
if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No relevant changed files detected."
  exit 0
fi

has_docs=0
has_repo_map_docs=0
has_automation=0
needs_full_smoke=0

for file in "${FILES[@]}"; do
  [[ -z "${file}" ]] && continue

  case "${file}" in
    docs/*|.gitattributes|.github/*|.githooks/*)
      has_docs=1
      ;;
  esac

  case "${file}" in
    docs/repo-maps/*|docs/wiki/*|docs/design/*|docs/implementation-crosswalk.md)
      has_repo_map_docs=1
      ;;
  esac

  case "${file}" in
    scripts/*|automation/*|.github/workflows/*|.githooks/*)
      has_automation=1
      ;;
  esac

  case "${file}" in
    common/*|decisions/*|events/*|missions/*|localisation/*|automation/country_profiles/verne.json|scripts/verne_smoke_checks.*|scripts/country_smoke_runner.*)
      needs_full_smoke=1
      ;;
  esac
done

echo "Smart smoke router mode: ${MODE}"
printf 'Changed files:\n'
printf ' - %s\n' "${FILES[@]}"

if command -v python3 >/dev/null 2>&1; then
  python3 scripts/repo_doctor.py
else
  echo "Skipping repo_doctor.py: python3 not available."
fi

if [[ ${has_docs} -eq 1 || ${has_automation} -eq 1 || ${needs_full_smoke} -eq 1 ]]; then
  python3 scripts/text_hygiene_guard.py
fi

if [[ ${has_docs} -eq 1 || ${has_automation} -eq 1 ]]; then
  python3 scripts/docs_conflict_guard.py
fi

if [[ ${has_docs} -eq 1 ]]; then
  python3 scripts/checklist_link_audit.py
fi

if [[ ${has_repo_map_docs} -eq 1 || ${has_automation} -eq 1 ]]; then
  python3 scripts/verne_checklist_audit.py
fi

if [[ ${needs_full_smoke} -eq 1 ]]; then
  bash scripts/verne_smoke_checks.sh
fi

echo "Smart smoke router finished."
