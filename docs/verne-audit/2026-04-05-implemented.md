# Verne implementation audit — 2026-04-05

## Implemented this pass

Added the missing localisation entries for the live trade-lane mission reward modifiers `verne_trade_network` and `verne_merchant_marine` in `localisation/verne_overhaul_l_english.yml`.

## Scope

- Added modifier name/description coverage for two already-scripted permanent rewards.
- Kept all new loc inside Verne overhaul localisation files.
- Updated `docs/status/verne-live-implementation-status.md` to record the change.
- Did not alter mission triggers, rewards, or any vanilla Anbennar files.

## Why this was chosen

The cron prompt's older candidate list is behind the repo's authoritative live-status file: the major missing Lane 5/7/8/9 missions listed there are already live. A real remaining high-value gap was missing visible modifier localisation for live Verne rewards, which matches the roadmap guidance to prioritize missing modifier tooltip coverage.

## Files changed

- `localisation/verne_overhaul_l_english.yml`
- `docs/status/verne-live-implementation-status.md`
- `docs/verne-audit/2026-04-05-implemented.md`

## Validation

- Verified both modifiers exist in `common/event_modifiers/verne_overhaul_modifiers.txt`.
- Verified the loc additions are inside Verne overhaul localisation only.
- Localisation-only change, so no mission-script brace risk was introduced.

---

## Implemented this pass (evening flavour follow-through)

Added a new lightweight Verne flavour event, `verne_overhaul_flavour.1`, for the already-live `A33_vernissage_secretariat` reward state.

## Scope

- Added `events/verne_overhaul_flavour_events.txt` with a one-time event that fires for Verne after gaining the live `verne_vernissage_secretariat` modifier.
- Added `common/event_modifiers/verne_overhaul_flavour_modifiers.txt` with three temporary follow-through modifiers:
  - `verne_secretariat_of_charts`
  - `verne_secretariat_of_curators`
  - `verne_secretariat_of_audiences`
- Added all related localisation in `localisation/verne_overhaul_flavour_l_english.yml`.
- Updated `docs/status/verne-live-implementation-status.md` to record the live addition.

## Why this was chosen

The roadmap candidate list is behind the repo's current state, but one safe high-value gap remained: adding extra Verne lore/flavour around already-live mission rewards without touching vanilla Anbennar files or colliding with planned mission-lane expansion. The Vernissage Secretariat was a clean target because the reward modifier already exists in live mission content and had no bespoke narrative follow-through.

## Files changed

- `events/verne_overhaul_flavour_events.txt`
- `common/event_modifiers/verne_overhaul_flavour_modifiers.txt`
- `localisation/verne_overhaul_flavour_l_english.yml`
- `docs/status/verne-live-implementation-status.md`
- `docs/verne-audit/2026-04-05-implemented.md`

## Validation

- Verified `A33_vernissage_secretariat` already grants `verne_vernissage_secretariat` in `missions/Verne_Missions.txt`.
- Kept all new visible loc keys inside Verne overhaul localisation files only.
- Event is isolated under its own namespace and uses a one-time country flag to avoid repeat firing.
- No vanilla Anbennar files were touched.
