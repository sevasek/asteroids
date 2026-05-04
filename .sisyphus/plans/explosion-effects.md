# Particle Explosion Effects for Asteroid Impacts

## TL;DR

> **Quick Summary**: Add blue ion particle explosion effects when bullets hit asteroids, with explosion size scaling to match asteroid size (large = big boom, small = tiny puff).
>
> **Deliverables**:
> - New EXPLOSION_* constants in `constants.py`
> - Explosion particle spawn logic in `main.py check_collisions()`
> - Reusable particle system (extend ExhaustParticle or create generic Particle class)
> - Visual result: Blue ion explosion bursts at bullet-asteroid collision points
>
> **Estimated Effort**: Short
> **Parallel Execution**: NO - sequential tasks (constants → particle class → integration)
> **Critical Path**: Task 1 (constants) → Task 2 (particle spawn logic) → Task 3 (QA)

---

## Context

### Original Request
"new feature. a particle explostion where asteroids collide, and where bullets hit the asteroids"

### Interview Summary
**Key Discussions**:
- Collision type: Bullets only (NOT asteroid-asteroid collisions)
- Visual style: Same blue ion glow as ship exhaust (visual consistency)
- Intensity: Scale with asteroid size (larger asteroids = bigger explosions)

**Research Findings**:
- `check_collisions()` in main.py:96-114 handles shot-asteroid collisions
- When collision detected: `a.split()` and `s.kill()` are called, score += 10
- `split()` in asteroid.py:20-43 kills asteroid and creates 2 smaller ones
- ExhaustParticle class already exists in player.py with position, velocity, lifetime, size, color, alpha fade
- Game uses pygame.draw.circle with SRCALPHA surfaces for particles
- Asteroid sizes: Large (~60px), Medium (~40px), Small (~20px) based on ASTEROID_MIN_RADIUS=20 and ASTEROID_KINDS=3

### Metis Review
N/A - Metis unavailable due to API credits. Proceeding with standard planning.

---

## Work Objectives

### Core Objective
Add satisfying particle explosion effects when bullets hit asteroids, with explosion intensity proportional to asteroid size.

### Concrete Deliverables
- `constants.py`: New EXPLOSION_* constants (particle counts, speeds, lifetime, colors)
- `main.py`: Modified `check_collisions()` to spawn explosion particles at collision point
- `player.py`: Extended or reused particle system for explosions (shared with exhaust)
- Visual result: Blue ion explosion bursts at bullet-asteroid collision points, sized to match asteroid

### Definition of Done
- [ ] Explosion particles spawn when bullet hits asteroid
- [ ] Explosion size scales with asteroid size (large > medium > small)
- [ ] Particles use blue ion color scheme (consistent with ship exhaust)
- [ ] Particles fly outward in all directions from collision point
- [ ] Particles fade over time and disappear
- [ ] Game runs without errors (`uv run python main.py`)

### Must Have
- Explosions trigger on bullet-asteroid collision (in check_collisions)
- Particle count scales with asteroid size:
  - Large (radius >= 40): 20-30 particles
  - Medium (20-39): 10-15 particles
  - Small (< 20): 5-8 particles
- Blue ion color scheme (same as ship exhaust: cornflower blue, deep sky blue, light sky blue)
- Particles emit from collision point (asteroid position at moment of impact)
- 360° spread (all directions, not just backward like exhaust)
- Higher speed than exhaust (200-400 px/s vs 80-200 px/s)
- Shorter lifetime (0.2-0.5s vs 0.3-0.8s) for snappy explosions
- Alpha fade over lifetime

### Must NOT Have (Guardrails)
- No asteroid-asteroid collision explosions (out of scope)
- No sound effects (visual only)
- No screen wrapping for explosion particles (fade naturally)
- No particle-to-particle interactions
- No particle-to-asteroid interactions
- No new files (reuse existing particle system in player.py)
- No modifications to CircleShape base class
- No gravity effects on particles
- No particle color changes over lifetime (simple alpha fade only)

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO (no test framework in project)
- **Automated tests**: None
- **Framework**: None
- **Agent-Executed QA**: ALWAYS (mandatory for all tasks)

### QA Policy
Every task MUST include agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.png`.

- **Frontend/UI**: Use Playwright (playwright skill) - Launch game, shoot asteroids, capture screenshots of explosions
- **Verification**: Visual inspection of screenshots for correct explosion behavior

---

## Execution Strategy

### Sequential Execution

```
Task 1: Add EXPLOSION_* constants to constants.py [quick]
  ↓
Task 2: Modify check_collisions() to spawn explosion particles [quick]
  ↓
Task 3: Agent QA verification [quick]
  ↓
COMPLETE
```

### Dependency Matrix

- **1**: - → 2
- **2**: 1 → 3
- **3**: 2 → COMPLETE

### Agent Dispatch Summary

- **Task 1**: `quick` category
- **Task 2**: `quick` category  
- **Task 3**: `quick` category with Playwright skill

---

## TODOs

- [x] 1. **Add EXPLOSION_* constants to constants.py**

  **What to do**:
  Add these constants after the EXHAUST_* constants (or in appropriate location):
  ```python
  # Explosion particle effects
  EXPLOSION_PARTICLE_LIFETIME_MIN = 0.2  # seconds
  EXPLOSION_PARTICLE_LIFETIME_MAX = 0.5  # seconds
  EXPLOSION_PARTICLE_SPEED_MIN = 200     # px/s
  EXPLOSION_PARTICLE_SPEED_MAX = 400     # px/s
  EXPLOSION_PARTICLE_SIZE_MIN = 1        # pixels
  EXPLOSION_PARTICLE_SIZE_MAX = 3        # pixels
  # Explosion particle counts by asteroid size
  EXPLOSION_COUNT_LARGE_MIN = 20         # large asteroids (radius >= 40)
  EXPLOSION_COUNT_LARGE_MAX = 30
  EXPLOSION_COUNT_MEDIUM_MIN = 10        # medium asteroids (radius 20-39)
  EXPLOSION_COUNT_MEDIUM_MAX = 15
  EXPLOSION_COUNT_SMALL_MIN = 5          # small asteroids (radius < 20)
  EXPLOSION_COUNT_SMALL_MAX = 8
  ```

  **Must NOT do**:
  - Do not modify any other constants
  - Do not remove EXHAUST_* constants

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple constant additions in a single file
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Task 2
  - **Blocked By**: None

  **References**:
  - `constants.py` - Current EXHAUST_* constants for reference

  **Acceptance Criteria**:
  - [ ] All 11 EXPLOSION_* constants present with correct values
  - [ ] File has no syntax errors (`python -c "import constants"`)
  - [ ] Can import all new constants: `python -c "from constants import EXPLOSION_COUNT_LARGE_MIN, EXPLOSION_PARTICLE_SPEED_MAX; print('OK')"`

  **QA Scenarios**:
  ```
  Scenario: Constants module imports without errors
    Tool: Bash
    Steps:
      1. Run: python -c "from constants import EXPLOSION_COUNT_LARGE_MIN, EXPLOSION_COUNT_MEDIUM_MIN, EXPLOSION_COUNT_SMALL_MIN; print('OK')"
      2. Verify output contains "OK"
    Expected Result: Import succeeds, prints "OK"
    Evidence: .sisyphus/evidence/task-1-explosion-constants.txt
  ```

  **Commit**: YES
  - Message: `feat(explosions): add explosion particle constants`
  - Files: `constants.py`

---

- [x] 2. **Modify check_collisions() to spawn explosion particles**

  **What to do**:
  
  ### Step 2.1: Add helper function for explosion count
  Add this function before `check_collisions()` in main.py:
  ```python
def get_explosion_particle_count(radius):
    """Get particle count for explosion based on asteroid size."""
    if radius >= 40:
        return random.randint(EXPLOSION_COUNT_LARGE_MIN, EXPLOSION_COUNT_LARGE_MAX)
    elif radius >= 20:
        return random.randint(EXPLOSION_COUNT_MEDIUM_MIN, EXPLOSION_COUNT_MEDIUM_MAX)
    else:
        return random.randint(EXPLOSION_COUNT_SMALL_MIN, EXPLOSION_COUNT_SMALL_MAX)
  ```
  
  ### Step 2.2: Add explosion spawn function
  Add this function before `check_collisions()` in main.py:
  ```python
def spawn_explosion(position, radius):
    """Spawn explosion particles at the given position."""
    from player import ExhaustParticle  # Import here to avoid circular import
    
    particle_count = get_explosion_particle_count(radius)
    
    for _ in range(particle_count):
        # Random direction (360 degrees)
        angle = random.uniform(0, 360)
        direction = pygame.Vector2(0, 1).rotate(angle)
        
        # Random speed
        speed = random.uniform(EXPLOSION_PARTICLE_SPEED_MIN, EXPLOSION_PARTICLE_SPEED_MAX)
        velocity = direction * speed
        
        # Random lifetime and size
        lifetime = random.uniform(EXPLOSION_PARTICLE_LIFETIME_MIN, EXPLOSION_PARTICLE_LIFETIME_MAX)
        size = random.randint(EXPLOSION_PARTICLE_SIZE_MIN, EXPLOSION_PARTICLE_SIZE_MAX)
        
        # Random blue ion color
        color = random.choice(EXHAUST_COLORS)  # Reuse ship exhaust colors
        
        # Create particle
        particle = ExhaustParticle(position.copy(), velocity, lifetime, size, color)
        
        # Add to a global/shared particle list - need to figure out how to track these
        # Option A: Add to a new explosion_particles list in main.py
        # Option B: Return particles and let caller manage them
  ```
  
  ### Step 2.3: Modify check_collisions()
  Update the shot-asteroid collision block (lines 106-112) to spawn explosion:
  ```python
  for s in shots.copy():
      if a.collides_with(s):
          log_event("asteroid_shot")
          # Spawn explosion BEFORE killing asteroid (to get position)
          spawn_explosion(a.position.copy(), a.radius)
          a.split()
          s.kill()
          score_delta += 10
          break
  ```
  
  ### Step 2.4: Manage explosion particles
  Need to track and update explosion particles. Options:
  
  **Option A (Recommended)**: Add explosion_particles list to main.py game loop
  - Add `explosion_particles = []` in run_game()
  - Modify spawn_explosion to accept the list and append particles
  - Update explosion particles each frame in the game loop
  - Draw explosion particles each frame
  
  **Option B**: Extend drawable/updatable groups to include particles
  - Particles become pygame Sprites
  - Add to drawable/updatable groups
  - Auto-handled by existing game loop
  
  I recommend **Option A** for simplicity and to avoid changing the sprite group architecture.

  **Implementation for Option A**:
  
  In `run_game()` after line 138:
  ```python
  explosion_particles = []
  ```
  
  Modify `spawn_explosion()` to accept the list:
  ```python
  def spawn_explosion(position, radius, explosion_particles):
      ...
      explosion_particles.append(particle)
  ```
  
  Update call in check_collisions():
  ```python
  spawn_explosion(a.position.copy(), a.radius, explosion_particles)
  ```
  
  Modify check_collisions signature to accept explosion_particles:
  ```python
  def check_collisions(asteroids, shots, player, explosion_particles):
  ```
  
  In game loop (in run_game()), add:
  ```python
  # Update explosion particles
  explosion_particles = [p for p in explosion_particles if not p.update(dt)]
  
  # Draw explosion particles (in draw function or inline)
  for particle in explosion_particles:
      if particle.is_alive():
          particle.draw(screen)
  ```

  **Must NOT do**:
  - Do not modify CircleShape
  - Do not add asteroid-asteroid collision detection
  - Do not change the existing sprite group architecture unless necessary
  - Do not add sound effects

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Integration work following existing patterns
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Task 3
  - **Blocked By**: Task 1

  **References**:
  - `main.py:96-114` - Current check_collisions() function
  - `main.py:138` - Where to add explosion_particles list
  - `main.py:144-168` - Game loop where particles need to be updated/drawn
  - `player.py:56-82` - ExhaustParticle class to reuse

  **Acceptance Criteria**:
  - [ ] Explosion particles spawn when bullet hits asteroid
  - [ ] Particle count scales with asteroid size (large > medium > small)
  - [ ] Particles fly outward in all directions (360° spread)
  - [ ] Particles use blue ion colors
  - [ ] Particles fade over time and disappear
  - [ ] No errors when running game

  **QA Scenarios**:
  ```
  Scenario: Explosion particles spawn when shooting large asteroid
    Tool: Playwright
    Preconditions: Game running, large asteroid visible
    Steps:
      1. Position ship to shoot large asteroid
      2. Press SPACE to shoot
      3. Wait for bullet to hit asteroid
      4. Take screenshot
      5. Verify blue explosion particles visible at collision point
    Expected Result: Screenshot shows blue ion explosion burst with many particles (20-30)
    Failure Indicators: No explosion, wrong color, too few particles
    Evidence: .sisyphus/evidence/task-2-large-explosion.png

  Scenario: Explosion particles spawn when shooting small asteroid
    Tool: Playwright
    Preconditions: Game running, small asteroid visible
    Steps:
      1. Position ship to shoot small asteroid
      2. Press SPACE to shoot
      3. Wait for bullet to hit
      4. Take screenshot
      5. Verify small blue explosion (fewer particles than large)
    Expected Result: Screenshot shows smaller explosion with 5-8 particles
    Failure Indicators: Same size explosion as large asteroid
    Evidence: .sisyphus/evidence/task-2-small-explosion.png

  Scenario: Explosion particles fade over time
    Tool: Playwright
    Preconditions: Game running, asteroid hit
    Steps:
      1. Shoot asteroid
      2. Wait 0.5 seconds
      3. Take screenshot
      4. Verify explosion has faded/disappeared
    Expected Result: Explosion particles no longer visible or greatly diminished
    Failure Indicators: Particles still at full intensity
    Evidence: .sisyphus/evidence/task-2-explosion-fade.png
  ```

  **Commit**: YES
  - Message: `feat(explosions): spawn explosion particles on bullet-asteroid collision`
  - Files: `main.py`

---

- [x] 3. **Agent QA verification**

  **What to do**:
  Run the game and verify explosions work correctly:
  1. Launch game
  2. Shoot different sized asteroids
  3. Verify explosions spawn with correct size
  4. Verify particles fade over time
  5. Verify no console errors

  **Must NOT do**:
  - Do not modify code during QA (report issues instead)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple verification task
  - **Skills**: `[]` (or `playwright` if available)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: None (final task)
  - **Blocked By**: Task 2

  **Acceptance Criteria**:
  - [ ] Game launches without errors
  - [ ] Explosions visible when shooting asteroids
  - [ ] Explosion size varies with asteroid size
  - [ ] Particles fade over time
  - [ ] No regressions in existing functionality

  **QA Scenarios**:
  ```
  Scenario: Game runs without errors
    Tool: Bash
    Steps:
      1. Run: cd /Users/paulseville/Documents/GitHub/asteroids && timeout 5 uv run python main.py 2>&1 || true
      2. Verify no Python errors in output
    Expected Result: Game runs, no errors
    Evidence: .sisyphus/evidence/task-3-game-runs.txt
  ```

  **Commit**: NO (QA only)

---

## Commit Strategy

- **Commit 1** (Task 1): `feat(explosions): add explosion particle constants`
  - Files: `constants.py`
  - Pre-commit: `python -c "from constants import EXPLOSION_COUNT_LARGE_MIN; print('OK')"`

- **Commit 2** (Task 2): `feat(explosions): spawn explosion particles on bullet-asteroid collision`
  - Files: `main.py`
  - Pre-commit: `python -c "from main import spawn_explosion, get_explosion_particle_count; print('OK')"`

---

## Success Criteria

### Verification Commands
```bash
python -c "from constants import EXPLOSION_COUNT_LARGE_MIN; print('OK')"  # Expected: OK
python -c "from main import spawn_explosion; print('OK')"  # Expected: OK
grep -r "EXPLOSION_" constants.py  # Expected: 11 matches
uv run python main.py  # Expected: game launches, explosions work
```

### Final Checklist
- [ ] All EXPLOSION_* constants present in constants.py
- [ ] spawn_explosion() function exists in main.py
- [ ] Explosions trigger on bullet-asteroid collision
- [ ] Explosion size scales with asteroid size
- [ ] Particles use blue ion colors
- [ ] Particles fade over time
- [ ] Game runs without errors
