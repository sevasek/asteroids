# Hyperdrive Intro Effect

## Overview
Add a Star Wars-style hyperdrive animation as the intro before each game begins. Stars zoom from center outward creating a warp-speed tunnel effect, then the player ship flies in from a tiny spec to full size.

## Flow
1. Start menu (title + leaderboard + "Press ENTER to start")
2. Player presses ENTER
3. Hyperdrive animation plays for 3 seconds
4. Game starts immediately (player begins flying)

## Constants (constants.py)
Add new constants:
```python
# Hyperdrive
HYPERDRIVE_DURATION = 3.0       # seconds
HYPERDRIVE_STAR_COUNT = 300     # number of stars in tunnel
HYPERDRIVE_FOV = 400            # field of view for perspective
HYPERDRIVE_SHIP_FLY_IN_TIME = 0.2  # seconds for ship to scale up
HYPERDRIVE_COLOR = (255, 255, 255)  # star color
```

## Implementation

### New module: `hyperdrive.py`

**HyperdriveStar class:**
- x, y: initial random position
- z: depth (starts far, decreases each frame)
- On update: decrease z, calculate screen position using perspective projection:
  - `scale = FOV / z`
  - `screen_x = x * scale + center_x`
  - `screen_y = y * scale + center_y`
- Star grows larger and brighter as z decreases
- When z reaches near 0, respawn at far distance

**Hyperdrive class:**
- `stars`: list of HyperdriveStar objects
- `timer`: tracks elapsed time
- `update(dt)`: move stars, check if duration complete
- `draw(screen)`: render all stars with streaks (lines instead of dots when close)
- `is_complete()`: returns True after HYPERDRIVE_DURATION seconds

**Ship fly-in:**
- Player ship starts invisible (scale = 0)
- From t=2.5s to t=2.7s (last 200ms), scale from 0% to 100%
- Use pygame.transform.scale to scale up triangle

### Integration with main.py

**Modify `run_game()` to accept hyperdrive flag:**
```python
def run_game(screen, starfield, run_hyperdrive=True):
    if run_hyperdrive:
        hyperdrive = Hyperdrive()
        while not hyperdrive.is_complete():
            dt = clock.tick(60) / 1000
            starfield.update(dt)
            hyperdrive.update(dt)
            hyperdrive.draw(screen)
            # Also draw scaled player ship during fly-in
    # Then start actual game...
```

**Modify main.py start menu loop:**
```python
result, score = run_game(screen, starfield, run_hyperdrive=True)
```

## Visual Details

### Star Tunnel Effect
- Stars spawn at random x,y within a small center region
- All stars move outward from center (radial expansion)
- Far stars = tiny, dim points
- Close stars = large, bright streaks
- Use lines for stars close to camera, circles for distant

### Ship Fly-in
- At ~2.7 seconds into animation
- Start with player triangle scaled to ~2% size at screen center
- Rapidly scale up to 100% over 200ms
- Looks like ship warping into view

### Color
- Stars: white for classic look

## Timing Breakdown
- 0.0s - 2.5s: Star tunnel expands, no ship visible
- 2.5s - 2.7s: Ship scales up from spec to full size
- 2.7s - 3.0s: Brief moment at full speed before game starts
- 3.0s: Game begins immediately

## Testing Checklist
- [ ] Stars flow outward from center
- [ ] Stars stretch into lines when close
- [ ] 3 second duration is correct
- [ ] Player ship appears as tiny spec and scales up quickly
- [ ] Game starts immediately after animation completes
- [ ] No screen flicker or stuttering during animation