# Spaceship Exhaust Particle System Redesign

## TL;DR

> **Quick Summary**: Replace the current lame propulsion trail with a particle-based blue ion exhaust effect that emits from the ship's engine nozzle, fades over time, and scales intensity with thrust duration.
>
> **Deliverables**:
> - New `ExhaustParticle` class in `player.py` with position, velocity, lifetime, and alpha fade
> - Thrust duration tracking that scales particle count, size, and brightness
> - Complete removal of old trail system (self.trail, TRAIL_* constants, trail drawing code)
> - New EXHAUST_* constants in `constants.py`
>
> **Estimated Effort**: Short
> **Parallel Execution**: YES - 2 waves (constants + particle class, then integration + cleanup)
> **Critical Path**: Task 1 (constants) → Task 2 (ExhaustParticle class) → Task 3 (integration) → Task 4 (cleanup + QA)

---

## Context

### Original Request
"The effect coming out of the back of the players spaceship looks lame. the animation comes from the centre of the trianle, it only fades as the player moves (not over time after the w key is pressed), and if you turn the ship, then the trail is coming out the side of the vessel. plan an update to this animation so its much cooler and realistic"

### Interview Summary
**Key Discussions**:
- Visual style: Particle flame with individual particles from engine nozzle
- Color scheme: Blue ion glow (cornflower blue to deep sky blue range)
- Dynamic intensity: Scale with thrust duration (longer W = bigger flame)
- Screen wrapping: Particles fade naturally, no wrapping
- Test strategy: Agent QA only (Playwright screenshots)

**Research Findings**:
- Current trail records `self.position` (ship center) not engine nozzle
- Trail only shrinks when exceeding TRAIL_LENGTH (20), no time decay
- Game uses pygame.draw.circle with SRCALPHA surfaces for particles (starfield, hyperdrive)
- Engine nozzle position = midpoint of triangle vertices b and c = `self.position - forward * self.radius`
- Player created fresh on each game start (init_game), so particle cleanup on death is automatic

### Metis Review
**Identified Gaps** (addressed):
- S key behavior: Decided NO exhaust for backward thrust
- Particle draw order: Draw before ship (behind visually)
- Hyperdrive: No particles during warp-in
- Death cleanup: Auto-handled by new Player instance
- Particle physics constants: Defined all values (lifetime, size, speed, spread, max count)
- Thrust intensity formula: `min(thrust_time / 2.0, 1.0)`, caps at 2 seconds

---

## Work Objectives

### Core Objective
Replace the current position-history trail with a particle-based exhaust system that emits from the ship's engine nozzle, fades over time, and provides visual feedback proportional to thrust duration.

### Concrete Deliverables
- `player.py`: New `ExhaustParticle` class, integrated into `Player.update()` and `Player.draw()`
- `constants.py`: 12 new EXHAUST_* constants, 4 removed TRAIL_* constants
- Visual result: Blue ion particles streaming from ship back, fanning correctly on rotation, fading over time

### Definition of Done
- [ ] Old trail system completely removed (no references to `self.trail`, `TRAIL_*` in codebase)
- [ ] Particles emit from engine nozzle (back of triangle), not ship center
- [ ] Particles fade over time after W released (not just when moving)
- [ ] Particle trail follows ship direction when turning (not from side)
- [ ] Exhaust intensity scales with thrust duration
- [ ] `uv run python main.py` runs without errors

### Must Have
- Particles emit from correct position (engine nozzle at back of triangle)
- Time-based particle decay (particles fade and disappear after W released)
- Rotation-correct emission (particles always stream from back of ship)
- Blue ion color scheme with alpha blending
- Thrust intensity scaling (more thrust = more/bigger/brighter particles)
- Hard cap on particle count (150 max)

### Must NOT Have (Guardrails)
- No modifications to `CircleShape` base class
- No new files (particle system lives in `player.py`)
- No particle-to-particle or particle-to-asteroid interactions
- No sound effects
- No screen wrapping for particles
- No particles during hyperdrive sequence
- No exhaust from backward thrust (S key)
- No particle color changes over lifetime (simple alpha fade only)
- No multiple particle types (single blue ion particle)

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO (no test framework in project)
- **Automated tests**: None
- **Framework**: None
- **Agent-Executed QA**: ALWAYS (mandatory for all tasks)

### QA Policy
Every task MUST include agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.png`.

- **Frontend/UI**: Use Playwright (playwright skill) - Launch game, interact with controls, capture screenshots
- **Verification**: Visual inspection of screenshots for correct particle behavior

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - foundation):
├── Task 1: Update constants.py (add EXHAUST_*, remove TRAIL_*) [quick]
└── Task 2: Create ExhaustParticle class in player.py [quick]

Wave 2 (After Wave 1 - integration):
├── Task 3: Integrate exhaust into Player.update() and Player.draw() [quick]
└── Task 4: Remove old trail system + Agent QA verification [quick]

Wave FINAL (After ALL tasks — 2 parallel reviews):
├── Task F1: Plan compliance audit (oracle)
└── Task F2: Real manual QA via Playwright (unspecified-high)
-> Present results -> Get explicit user okay

Critical Path: Task 1 → Task 2 → Task 3 → Task 4 → F1-F2 → user okay
Parallel Speedup: ~50% faster than sequential
Max Concurrent: 2 (Waves 1 & 2)
```

### Dependency Matrix

- **1**: - → 3
- **2**: - → 3
- **3**: 1, 2 → 4
- **4**: 3 → F1, F2
- **F1, F2**: 4 → user okay

### Agent Dispatch Summary

- **Wave 1**: **2** - T1 → `quick`, T2 → `quick`
- **Wave 2**: **2** - T3 → `quick`, T4 → `quick`
- **FINAL**: **2** - F1 → `oracle`, F2 → `unspecified-high`

---

## TODOs

- [x] 1. **Update constants.py — Add EXHAUST_* constants, remove TRAIL_* constants**

  **What to do**:
  - Remove these 4 constants: `TRAIL_LENGTH`, `TRAIL_FADE_SPEED`, `TRAIL_COLOR`, `TRAIL_WIDTH`
  - Add these 12 new constants:
    ```python
    # Exhaust particle system
    EXHAUST_PARTICLE_LIFETIME_MIN = 0.3  # seconds
    EXHAUST_PARTICLE_LIFETIME_MAX = 0.8  # seconds
    EXHAUST_PARTICLE_SIZE_MIN = 1        # pixels
    EXHAUST_PARTICLE_SIZE_MAX = 4        # pixels
    EXHAUST_SPREAD_ANGLE = 30            # degrees from backward vector
    EXHAUST_EMISSION_RATE_MIN = 2        # particles per frame (low thrust)
    EXHAUST_EMISSION_RATE_MAX = 5        # particles per frame (full thrust)
    EXHAUST_MAX_PARTICLES = 150          # hard cap on simultaneous particles
    EXHAUST_PARTICLE_SPEED_MIN = 80      # px/s
    EXHAUST_PARTICLE_SPEED_MAX = 200     # px/s
    EXHAUST_COLORS = [(100, 149, 237), (0, 191, 255), (135, 206, 250)]  # blue ion range
    EXHAUST_INTENSITY_CAP = 2.0          # seconds to reach full intensity
    ```

  **Must NOT do**:
  - Modify any other constants
  - Change SCREEN_WIDTH, SCREEN_HEIGHT, or player settings

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple constant additions/removals in a single file
  - **Skills**: `[]`
  - **Skills Evaluated but Omitted**: None needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 2)
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: Task 3
  - **Blocked By**: None (can start immediately)

  **References**:
  - `constants.py:10-13` - Current TRAIL_* constants to remove
  - `constants.py` - Full file for context on constant organization

  **Acceptance Criteria**:
  - [ ] No references to TRAIL_* in constants.py
  - [ ] All 12 EXHAUST_* constants present with correct values
  - [ ] File has no syntax errors (`python -c "import constants"`)

  **QA Scenarios**:
  ```
  Scenario: Constants module imports without errors
    Tool: Bash
    Steps:
      1. Run: cd /Users/paulseville/Documents/GitHub/asteroids && python -c "from constants import EXHAUST_PARTICLE_LIFETIME_MIN, EXHAUST_PARTICLE_LIFETIME_MAX, EXHAUST_MAX_PARTICLES; print('OK')"
      2. Verify output contains "OK"
    Expected Result: Import succeeds, prints "OK"
    Evidence: .sisyphus/evidence/task-1-constants-import.txt
  ```

  **Commit**: YES (groups with 2)
  - Message: `refactor(player): replace trail constants with exhaust particle constants`
  - Files: `constants.py`

---

- [x] 2. **Create ExhaustParticle class in player.py**

  **What to do**:
  - Create `ExhaustParticle` class with:
    - `__init__(self, position, velocity, lifetime, size, color)`: Initialize particle with position (pygame.Vector2), velocity (pygame.Vector2), lifetime (float seconds), size (int pixels), color (tuple RGB)
    - `self.elapsed = 0.0`: Track time since creation
    - `self.max_lifetime = lifetime`: Store original lifetime for fade calculation
    - `update(self, dt)`: Increment elapsed, return True if expired (elapsed >= max_lifetime)
    - `draw(self, screen)`: Draw particle with alpha based on remaining life: `alpha = int(255 * (1 - self.elapsed / self.max_lifetime))`, use `pygame.draw.circle` on SRCALPHA surface
    - `is_alive(self)`: Return `self.elapsed < self.max_lifetime`

  **Must NOT do**:
  - Add collision detection
  - Add screen wrapping
  - Modify CircleShape or Player class yet
  - Add sound effects

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple class with 4 methods, follows existing patterns (Star, HyperdriveStar)
  - **Skills**: `[]`
  - **Skills Evaluated but Omitted**: None needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1)
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: Task 3
  - **Blocked By**: None (can start immediately)

  **References**:
  - `starfield.py:7-14` - Star class pattern (simple particle with position, size, phase)
  - `hyperdrive.py:17-45` - HyperdriveStar class pattern (particle with update/draw lifecycle)
  - `starfield.py:31-41` - Alpha blending pattern using SRCALPHA surface
  - `player.py:54-68` - Player class structure and triangle() method for understanding ship geometry

  **Acceptance Criteria**:
  - [ ] ExhaustParticle class defined in player.py before Player class
  - [ ] `update(dt)` correctly tracks elapsed time and returns expired status
  - [ ] `draw(screen)` renders with correct alpha fade
  - [ ] Particles expire correctly when elapsed >= max_lifetime

  **QA Scenarios**:
  ```
  Scenario: Particle lifecycle - creates, updates, expires
    Tool: Bash
    Steps:
      1. Run Python REPL test:
         ```python
         import pygame
         pygame.init()
         from player import ExhaustParticle
         p = ExhaustParticle(pygame.Vector2(100, 100), pygame.Vector2(0, -50), 0.5, 3, (100, 149, 237))
         assert p.is_alive() == True
         assert p.elapsed == 0.0
         p.update(0.3)
         assert p.is_alive() == True
         assert p.elapsed == 0.3
         p.update(0.3)
         assert p.is_alive() == False
         print("PASS")
         ```
      2. Verify output contains "PASS"
    Expected Result: All assertions pass, particle expires after lifetime
    Evidence: .sisyphus/evidence/task-2-particle-lifecycle.txt
  ```

  **Commit**: YES (groups with 1)
  - Message: `refactor(player): replace trail constants with exhaust particle constants`
  - Files: `player.py` (ExhaustParticle class only)

---

- [x] 3. **Integrate exhaust system into Player.update() and Player.draw()**

  **What to do**:
  - Add to `Player.__init__`:
    - `self.exhaust_particles = []` - list of active ExhaustParticle instances
    - `self.thrust_time = 0.0` - tracks continuous thrust duration
  - Add `get_exhaust_nozzle_position()` method:
    - Compute forward vector: `pygame.Vector2(0, 1).rotate(self.rotation)`
    - Nozzle position: `self.position - forward * self.radius` (back of triangle)
    - Return pygame.Vector2
  - Add `emit_exhaust(dt)` method:
    - Only called when W key is pressed (in move())
    - Calculate intensity: `intensity = min(self.thrust_time / EXHAUST_INTENSITY_CAP, 1.0)`
    - Calculate particles to emit: `rate = int(EXHAUST_EMISSION_RATE_MIN + intensity * (EXHAUST_EMISSION_RATE_MAX - EXHAUST_EMISSION_RATE_MIN))`
    - For each particle:
      - Compute backward direction: `-forward` (opposite of ship facing)
      - Add random angular spread: `random.uniform(-EXHAUST_SPREAD_ANGLE, EXHAUST_SPREAD_ANGLE)`
      - Compute velocity: `backward_vector.rotate(spread) * random.uniform(EXHAUST_PARTICLE_SPEED_MIN, EXHAUST_PARTICLE_SPEED_MAX)`
      - Create ExhaustParticle at nozzle position with computed velocity
      - Random lifetime: `random.uniform(EXHAUST_PARTICLE_LIFETIME_MIN, EXHAUST_PARTICLE_LIFETIME_MAX)`
      - Random size: `random.randint(EXHAUST_PARTICLE_SIZE_MIN, EXHAUST_PARTICLE_SIZE_MAX)`
      - Random color from EXHAUST_COLORS
      - Enforce max cap: if `len(self.exhaust_particles) >= EXHAUST_MAX_PARTICLES`, remove oldest (pop from end)
  - Modify `move(dt)`:
    - After position update, call `self.thrust_time += dt`
    - Call `self.emit_exhaust(dt)`
  - Modify `update(dt)`:
    - If W key NOT pressed: `self.thrust_time = 0.0` (reset thrust timer)
    - Update all particles: `self.exhaust_particles = [p for p in self.exhaust_particles if not p.update(dt)]`
  - Modify `draw(screen)`:
    - Draw exhaust particles BEFORE ship polygon (behind ship visually)
    - Use SRCALPHA surface for alpha blending (same pattern as current trail)
    - Draw each alive particle

  **Must NOT do**:
  - Modify CircleShape
  - Add particles for S key (backward thrust)
  - Add particles during hyperdrive (handled by separate Player instance)
  - Change ship movement logic

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Integration work following clear patterns from existing code
  - **Skills**: `[]`
  - **Skills Evaluated but Omitted**: None needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (sequential after Wave 1)
  - **Blocks**: Task 4
  - **Blocked By**: Task 1, Task 2

  **References**:
  - `player.py:88-103` - Current update() method with key handling
  - `player.py:106-116` - Current move() method with trail recording
  - `player.py:71-81` - Current draw() method with trail rendering
  - `player.py:62-68` - triangle() method for understanding forward vector computation
  - `starfield.py:31-41` - SRCALPHA surface pattern for alpha-blended drawing
  - `constants.py` (after Task 1) - New EXHAUST_* constants

  **Acceptance Criteria**:
  - [ ] Particles emit from engine nozzle (back of triangle) when W pressed
  - [ ] Particles fade over time after W released
  - [ ] Particle trail follows ship direction when turning
  - [ ] Exhaust intensity increases with thrust duration
  - [ ] No particles emitted when W not pressed
  - [ ] No particles emitted when S pressed (backward thrust)
  - [ ] Particle count capped at EXHAUST_MAX_PARTICLES

  **QA Scenarios**:
  ```
  Scenario: Particles emit from engine nozzle during forward thrust
    Tool: Playwright
    Preconditions: Game running, ship at center of screen
    Steps:
      1. Press and hold W for 0.5 seconds
      2. Take screenshot
      3. Verify blue particles visible streaming from BACK of ship triangle (not center)
    Expected Result: Screenshot shows blue ion particles originating from the base of the ship triangle
    Failure Indicators: Particles coming from ship center, no particles, wrong color
    Evidence: .sisyphus/evidence/task-3-nozzle-emission.png

  Scenario: Particles fade after W released
    Tool: Playwright
    Preconditions: Game running, ship thrusting for 1 second
    Steps:
      1. Hold W for 1 second
      2. Release W
      3. Wait 0.5 seconds
      4. Take screenshot
      5. Verify particles are fading (fewer/dimmer than during thrust)
    Expected Result: Screenshot shows diminishing particles, no new particles being created
    Failure Indicators: Particles still at full intensity, no particles at all
    Evidence: .sisyphus/evidence/task-3-time-decay.png

  Scenario: Particle trail follows ship direction when turning
    Tool: Playwright
    Preconditions: Game running, ship thrusting
    Steps:
      1. Hold W
      2. Press A to rotate left for 0.5 seconds
      3. Take screenshot
      4. Verify particles stream from the BACK of the rotated ship (not from the side)
    Expected Result: Particles fan out correctly behind ship's new orientation
    Failure Indicators: Particles coming from side of ship, particles not aligned with ship direction
    Evidence: .sisyphus/evidence/task-3-rotation-correct.png
  ```

  **Commit**: YES (groups with 4)
  - Message: `feat(player): integrate particle exhaust system with thrust intensity scaling`
  - Files: `player.py`

---

- [x] 4. **Remove old trail system + Final verification**

  **What to do**:
  - Remove from `Player.__init__`: `self.trail = []`
  - Remove from `move(dt)`: The entire trail recording block:
    ```python
    if dt > 0:
        self.trail.insert(0, self.position.copy())
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop()
    ```
  - Remove from `draw(screen)`: The entire trail rendering block (lines 72-79):
    ```python
    if self.trail:
        trail_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (1 - i / len(self.trail)))
            if alpha > 0:
                color = (*TRAIL_COLOR, alpha)
                pygame.draw.circle(trail_surface, color, (int(pos.x), int(pos.y)), TRAIL_WIDTH)
        screen.blit(trail_surface, (0, 0))
    ```
  - Remove from imports in player.py: `TRAIL_LENGTH, TRAIL_FADE_SPEED, TRAIL_COLOR, TRAIL_WIDTH`
  - Verify no remaining references to `self.trail` or `TRAIL_*` anywhere in codebase
  - Run game to verify it works end-to-end

  **Must NOT do**:
  - Remove any other Player functionality
  - Modify exhaust particle system
  - Change any other game objects

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Clean removal of dead code, straightforward deletions
  - **Skills**: `[]`
  - **Skills Evaluated but Omitted**: None needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (sequential after Task 3)
  - **Blocks**: F1, F2
  - **Blocked By**: Task 3

  **References**:
  - `player.py:2` - Import line to clean up
  - `player.py:59` - self.trail initialization
  - `player.py:72-79` - Trail drawing code to remove
  - `player.py:113-116` - Trail recording in move() to remove

  **Acceptance Criteria**:
  - [ ] No references to `self.trail` in player.py
  - [ ] No references to `TRAIL_*` in player.py or constants.py
  - [ ] No references to `TRAIL_*` anywhere in codebase (grep confirms)
  - [ ] Game runs without errors (`uv run python main.py` starts successfully)
  - [ ] Ship renders correctly as white triangle
  - [ ] Exhaust particles work correctly (from Task 3 QA)

  **QA Scenarios**:
  ```
  Scenario: No trail references remain in codebase
    Tool: Bash
    Steps:
      1. Run: grep -r "self\.trail\|TRAIL_" /Users/paulseville/Documents/GitHub/asteroids/*.py
      2. Verify no output (no matches found)
    Expected Result: Empty output (no matches)
    Failure Indicators: Any file:line output showing trail references
    Evidence: .sisyphus/evidence/task-4-no-trail-references.txt

  Scenario: Game launches and runs without errors
    Tool: Playwright
    Steps:
      1. Launch game: uv run python main.py
      2. Wait for hyperdrive sequence to complete
      3. Wait 2 seconds for gameplay to start
      4. Take screenshot
      5. Verify ship is visible as white triangle at screen center
      6. Verify no console errors
    Expected Result: Screenshot shows ship at center, no errors in output
    Failure Indicators: Black screen, error messages, ship not visible
    Evidence: .sisyphus/evidence/task-4-game-launches.png
  ```

  **Commit**: YES
  - Message: `refactor(player): remove old trail system completely`
  - Files: `player.py`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 2 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle` — ✅ APPROVE (Must Have 6/6, Must NOT Have 9/9)

- [x] F2. **Real Manual QA** — `unspecified-high` (+ `playwright` skill) — ⚠️ SKIPPED
  - Playwright MCP is for web browser automation, cannot automate pygame desktop games
  - Code verified via F1 oracle audit: Must Have 6/6, Must NOT Have 9/9 ✅
  - Automated checks pass: imports work, 0 TRAIL_* references, game launches successfully

---

## Commit Strategy

- **Commit 1** (Tasks 1+2): `refactor(player): replace trail system with exhaust particle constants and class`
  - Files: `constants.py`, `player.py` (ExhaustParticle class only)
  - Pre-commit: `python -c "from constants import EXHAUST_MAX_PARTICLES; from player import ExhaustParticle; print('OK')"`

- **Commit 2** (Tasks 3+4): `feat(player): integrate particle exhaust with thrust intensity, remove old trail`
  - Files: `player.py` (integration + cleanup)
  - Pre-commit: `grep -r "TRAIL_\|self\.trail" *.py | wc -l` (should be 0)

---

## Success Criteria

### Verification Commands
```bash
grep -r "TRAIL_\|self\.trail" *.py  # Expected: no output (0 matches)
python -c "from constants import EXHAUST_MAX_PARTICLES; print('OK')"  # Expected: OK
uv run python main.py  # Expected: game launches, ship visible, exhaust works
```

### Final Checklist
- [x] All "Must Have" present (nozzle emission, time decay, rotation-correct, blue ion, intensity scaling, particle cap)
- [x] All "Must NOT Have" absent (no CircleShape changes, no new files, no interactions, no sound, no wrapping, no S-key exhaust)
- [x] All TRAIL_* references removed
- [x] Game runs without errors
- [x] F1 Plan Compliance Audit: APPROVE (6/6 Must Have, 9/9 Must NOT Have)
- [x] F2 QA: SKIPPED (Playwright is for web, not pygame desktop game; code verified via F1 oracle audit)
