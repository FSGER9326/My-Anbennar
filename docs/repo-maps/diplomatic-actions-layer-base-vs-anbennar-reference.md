# Diplomatic Actions Layer (Base EU4 vs Anbennar)

## Quick verdict

Anbennar extends diplomacy with many custom action definitions and special-case integrations.

## Core anchors

- `common/new_diplomatic_actions/00_diplomatic_actions.txt`
- `common/new_diplomatic_actions/anb_tributaries.txt`
- `common/new_diplomatic_actions/anb_kalsyto_sphere.txt`
- `common/new_diplomatic_actions/anb_nsc_investigation.txt`
- `common/new_diplomatic_actions/zz_magic_duel.txt`

## Delta from vanilla-style baseline

- additional bespoke diplomatic actions
- tag/system-specific custom diplomatic options
- custom interactions tied to non-vanilla systems (including magic-linked action definitions)

## Verne adaptation note

Before adding new diplomatic actions for Verne, check whether an existing action type can be reused with narrower triggers/effects.

## Upstream risk

High risk in shared action definitions under `common/new_diplomatic_actions`.


## Object-ID appendix (first pass)

Representative action definition IDs/files to monitor:

- `00_diplomatic_actions.txt`
- `anb_tributaries.txt`
- `anb_kalsyto_sphere.txt`
- `anb_nsc_investigation.txt`
- `zz_magic_duel.txt`
