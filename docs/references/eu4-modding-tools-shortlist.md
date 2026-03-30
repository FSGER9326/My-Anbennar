# EU4 Modding Tools Shortlist

This is a practical shortlist of external tools worth knowing for this repo.

The goal is not to replace repo-local checks. The goal is to pair the right external tool with the right kind of task.

## 1. CWTools

- Site: <https://cwtools.github.io/>
- GitHub org: <https://github.com/cwtools>
- GitHub Action: <https://github.com/cwtools/cwtools-action>
- EU4 rules/config: <https://github.com/cwtools/cwtools-eu4-config>

### Why it matters

CWTools is the strongest general-purpose validator here for Clausewitz/Paradox script work.

It helps with:
- syntax and scope validation
- cross-reference checking
- missing or broken localisation
- event/reference consistency
- IDE assistance in VS Code
- PR annotations in GitHub Actions

### Best use in this repo

- Use as a CI layer in GitHub Actions
- Use locally in VS Code for authoring feedback
- Treat it as a broad Clausewitz validator, not a replacement for repo-specific Verne checks

### Repo note

This repo now includes a CWTools validation job in `.github/workflows/verne-validation.yml`.

## 2. The Validator

- Wiki reference: <https://eu4.paradoxwikis.com/The_Validator>
- Project page referenced by the wiki: <https://codeberg.org/Aetherial-Mods/Audax-Validator-EU4>

### Why it matters

This is a more classic EU4-specific error finder. It is useful as a secondary check when something still feels broken after repo-local checks and CWTools.

### Best use in this repo

- Use as a manual or optional deep-dive validation pass
- Good candidate for later documentation, but not the first CI integration target

### Caution

Prefer proving it is stable and automation-friendly before trying to add it to CI.

## 3. Clausewitz Scenario Editor

- Wiki page: <https://eu4.paradoxwikis.com/Clausewitz_Scenario_Editor>

### Why it matters

Useful for:
- map/history inspection
- province lookup
- scenario/bookmark and setup-oriented work

### Best use in this repo

- Manual support tool for province/history-heavy tasks
- Not a repo CI tool

## 4. EU4 Mod Editing Tool

- Wiki page: <https://eu4.paradoxwikis.com/EU4_Mod_Editing_Tool>
- Releases: <https://github.com/CzerstfyChlep/Eu4-Mod-Editing-Tool/releases>

### Why it matters

Useful for:
- editing provinces
- countries
- trade nodes
- some broader data-oriented mod tasks

### Best use in this repo

- Manual support tool for map/history/common editing
- Especially useful if future work expands beyond Verne scripted systems into heavier map/data work

## 5. JoroDox mod making tool

- Wiki page: <https://eu4.paradoxwikis.com/JoroDox_mod_making_tool>

### Why it matters

Historically notable, but lower priority for this repo than CWTools and the newer EU4 editing tools.

### Best use in this repo

- Reference only for now
- Do not prioritize integration work around it

## 6. EU4 Localisation Generator

- Wiki reference from modding tools page
- GitHub releases: <https://github.com/theolaa/EU4-Localisation-Converter/releases/latest/>

### Why it matters

Potentially useful if this repo starts needing broad multi-language placeholder duplication.

### Best use in this repo

- Optional helper later
- Not important right now because the immediate need is correctness, not multilingual rollout

## Recommended tool stack for this repo

### Core stack

1. Repo-local Python/PowerShell checks
2. CWTools in CI
3. CWTools in VS Code locally
4. Repo-local smoke checks and PR artifact generation

### Secondary/manual stack

5. The Validator for extra bug hunting
6. Clausewitz Scenario Editor for province/history inspection
7. EU4 Mod Editing Tool for map/common editing support

## Recommendation

For near-term workflow improvement, prioritize:

1. stabilizing repo-local validation on Windows
2. keeping CWTools integrated and documented
3. using The Validator only after the current CI/local flow is settled

That gives the best return without turning the workflow into tool soup.
