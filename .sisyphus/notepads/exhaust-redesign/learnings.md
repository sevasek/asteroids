# Learnings - Exhaust Redesign

## Task 1: Constants Migration

- Replaced 4 TRAIL_* constants with 12 EXHAUST_* constants in `constants.py`
- New constants cover: particle lifetime (min/max), size (min/max), spread angle, emission rate (min/max), max particles, particle speed (min/max), color palette, and intensity cap
- Import verified: `python3 -c "from constants import EXHAUST_PARTICLE_LIFETIME_MIN, ..."` works
- All 12 EXHAUST_* constants confirmed present, 0 TRAIL_* constants remain
- Python binary is `python3` on this system, not `python`
- Verdict: Task 1 complete, awaiting Task 2 before commit

## Task 2: ExhaustParticle Class

- Added `import random` to player.py for upcoming Task 3 emission logic
- Placed `ExhaustParticle` class BEFORE `Player` class in player.py (line 55)
- Class uses SRCALPHA surface technique (same pattern as starfield.py draw method)
- Alpha computed as `int(255 * (1 - elapsed / max_lifetime))` for linear fade
- `update()` returns boolean expiry flag — dual-purpose pattern (mutates + signals)
- `is_alive()` is a separate query method for external polling
- Velocity integration: `self.position += self.velocity * dt` in update()
- Particle doesn't wrap_position() — intended to die at edges or via expiry
- Verdict: Task 2 complete, awaiting Task 1/2 commit group

## 2026-05-04: Task 4 - Old trail system removal

- Old trail system (self.trail list, TRAIL_LENGTH, TRAIL_FADE_SPEED, TRAIL_COLOR, TRAIL_WIDTH constants) fully removed
- Exhaust particle system completely replaces it: ExhaustParticle class, exhaust_particles list, EXHAUST_* constants
- Verified via grep that no `self.trail` or `TRAIL_` references exist anywhere in codebase
- Game launches and runs without errors
- Commit: `refactor(player): remove old trail system completely` (4cb3672)
