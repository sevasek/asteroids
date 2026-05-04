# Starfield Background Feature

## Overview
Add a twinkling starfield background that appears behind both the menu and game.

## Constants (asteroids/constants.py)
```python
# Stars
STAR_COUNT = 100            # Number of stars
STAR_COLOR = (180, 180, 180)  # Light grey RGB
STAR_MIN_SIZE = 1
STAR_MAX_SIZE = 3
STAR_TWINKLE_SPEED = 2.0    # How fast stars fade in/out
```

## Implementation (asteroids/starfield.py)

### Class Design (managed separately, not sprite system)

```python
import pygame
import random
from constants import STAR_COUNT, STAR_COLOR, STAR_MIN_SIZE, STAR_MAX_SIZE, STAR_TWINKLE_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Star:
    def __init__(self):
        self.position = pygame.Vector2(
            random.uniform(0, SCREEN_WIDTH),
            random.uniform(0, SCREEN_HEIGHT)
        )
        self.size = random.randint(STAR_MIN_SIZE, STAR_MAX_SIZE)
        self.phase_offset = random.uniform(0, 2 * 3.14159)  # Random start phase for twinkling

class StarField:
    def __init__(self):
        self.stars = [Star() for _ in range(STAR_COUNT)]

    def update(self, dt, time_elapsed):
        pass  # Brightness calculated at draw time

    def draw(self, screen, time_elapsed):
        for star in self.stars:
            # Calculate brightness using sine wave
            brightness = (math.sin(time_elapsed * STAR_TWINKLE_SPEED + star.phase_offset) + 1) / 2
            # Map to alpha range (80-255 for visible but subtle)
            alpha = int(80 + brightness * 175)
            color = (*STAR_COLOR, alpha)
            # Draw star with alpha
```

## Integration

### 1. main.py - Import and create
```python
from starfield import StarField

# In main():
starfield = StarField()
time_elapsed = 0
```

### 2. main.py - Update and draw
```python
# In game loop:
time_elapsed += dt

# In draw() or Menu.draw():
# Remove screen.fill("black") - starfield provides background
starfield.draw(screen, time_elapsed)
for d in drawable:
    d.draw(screen)
```

### 3. menu.py - Modify draw()
```python
def draw(self, screen, starfield=None):
    if starfield:
        starfield.draw(screen, time_elapsed)  # Need to pass time
    else:
        screen.fill("black")

    # ... rest of menu drawing
```

### 4. Constants - Add import
```python
import math  # For sine wave
```

## Key Details
- Stars use sine wave for smooth twinkling
- Alpha range: 80-255 (never fully invisible)
- Light grey color: (180, 180, 180)
- Star positions generated once at init (static, no drift)
- Starfield draws behind all game elements