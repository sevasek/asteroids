# Player Propulsion Trail Feature

## Overview
Add a fading trail behind the player to simulate spacecraft propulsion when moving forward (W key pressed).

## Constants (asteroids/constants.py)
Add under Player settings:
```python
TRAIL_LENGTH = 20          # Number of trail segments
TRAIL_FADE_SPEED = 2.0     # Alpha reduction per segment (0-255)
TRAIL_COLOR = (255, 165, 0)  # Orange in RGB
TRAIL_WIDTH = 3           # Line width for trail
```

## Implementation (asteroids/player.py)

### 1. Trail Storage
Add to `__init__`:
```python
self.trail = []  # List of (position, alpha) tuples
```

### 2. Trail Update
In `move()` method - when W key moves forward:
- Add current position to front of trail list
- If trail exceeds `TRAIL_LENGTH`, remove oldest
- Decrease alpha of existing trail points

### 3. Trail Rendering
In `draw()` method - before drawing player:
- Draw trail as lines from oldest to newest
- Oldest = most faded (low alpha), newest = brightest (high alpha)
- Use pygame.draw.lines() with varying alpha colors

## Key Details
- Trail only appears when W key is pressed (moving forward)
- Trail rendered as lines connecting positions
- Color: Orange (255, 165, 0)
- Fade from bright to transparent based on position in list
- Trail clears on player death (new game)