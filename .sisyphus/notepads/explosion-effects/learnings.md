# Explosion Effects - Learnings

## 2026-05-04: Explosion particles implemented

- Added `get_explosion_particle_count(radius)` — size-based particle count (large >= 40px, medium >= 20px, small < 20px)
- Added `spawn_explosion(position, radius, explosion_particles)` — creates ExhaustParticle instances with 360° random direction, random speed/lifetime/size, blue ion colors
- Modified `check_collisions()` to accept `explosion_particles` list and call `spawn_explosion()` before `a.split()` + `s.kill()`
- Updated `draw()` to render explosion particles behind other drawables
- Updated `run_game()` to track/manage explosion particle lifecycle
- Key insight: ExhaustParticle class from `player.py` was reusable for explosions — just needed its own position/velocity/lifetime/size/color params
- Import pattern: used local import `from player import ExhaustParticle` inside `spawn_explosion()` to avoid circular imports
