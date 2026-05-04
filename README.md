# Asteroids

A classic Asteroids arcade game clone built with Pygame and Python 3.13+.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Logging](#logging)

## Description
A fully functional clone of the classic 1979 Asteroids arcade game, featuring authentic gameplay mechanics including destructible asteroids, ship thrust and rotation, and score tracking.

## Features
- Authentic Asteroids gameplay with Pygame rendering
- Player ship with rotation and thrust controls
- Projectile shooting with cooldown mechanics
- Destructible asteroids that split into smaller pieces on impact
- Screen wrapping for all game objects
- Score tracking for destroyed asteroids
- Game over screen with retry functionality
- JSONL-based game state and event logging
- **Hyperdrive intro**: Star Wars-style warp tunnel animation before each game (3 seconds)
- **Twinkling starfield**: Dynamic background with animated stars
- **High score leaderboard**: Persistent top 10 scores with player names (up to 12 characters)
- **Dynamic menu system**: Auto-layout menus that work with any resolution

## Installation

### Prerequisites
- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (recommended package manager) or pip

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/asteroids.git
   cd asteroids
   ```

2. Install dependencies using uv (recommended):
   ```bash
   cd asteroids
   uv sync
   ```
   Or using pip:
   ```bash
   cd asteroids
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

### Running the Game
Launch the game from the `asteroids` subdirectory:
```bash
# With uv
uv run python main.py

# With pip (activate venv first)
python main.py
```

## How to Play

### Controls
| Key | Action |
|-----|--------|
| `A` | Rotate ship left |
| `D` | Rotate ship right |
| `W` | Thrust forward (with propulsion trail effect) |
| `S` | Thrust backward |
| `SPACE` | Shoot projectiles (0.3s cooldown) |
| `ENTER` | Start game / Restart after game over |
| `ESC` | Return to menu / Quit game |

## Game Rules
- Destroy asteroids by shooting them to earn 10 points per asteroid
- Asteroids come in 3 sizes:
  - Large: Splits into 2 medium asteroids when shot
  - Medium: Splits into 2 small asteroids when shot
  - Small: Disappears when shot
- Colliding with any asteroid ends the game
- All game objects wrap around the screen edges (reappear on the opposite side)
- The game spawns new asteroids every 0.8 seconds at random screen edges

## Project Structure
```
asteroids/                  # Repository root
├── README.md               # This file
├── .gitignore              # Ignored files (game logs, venv)
└── asteroids/              # Game package
    ├── main.py             # Entry point, game loop, event handling
    ├── player.py           # Player ship logic and controls
    ├── asteroids.py        # Asteroid class, splitting behavior
    ├── asteroidfield.py    # Asteroid spawning logic
    ├── shot.py             # Projectile logic and rendering
    ├── circleshape.py      # Base class for circular game objects
    ├── constants.py        # Game configuration and tunable settings
    ├── logger.py           # JSONL game state and event logging
    ├── hyperdrive.py       # Star Wars-style warp tunnel intro
    ├── starfield.py        # Twinkling star background
    ├── menu.py             # Dynamic menu system with auto-layout
    ├── leaderboard.py      # Persistent high score leaderboard
    ├── pyproject.toml      # Project metadata and dependencies
    ├── uv.lock             # Dependency lock file
    └── .venv/              # Virtual environment (gitignored)
```

## Configuration
All tunable game settings are defined in `asteroids/constants.py`, including:

### Core Settings
- Screen dimensions (default: 1280x720)
- Player speed, rotation speed, and shoot cooldown
- Asteroid spawn rate, sizes, and split behavior

### Visual Effects
- Line width for ship and asteroid rendering
- Font sizes for menus and game over screens
- Starfield: count, size, color, and twinkle speed
- Hyperdrive: duration, star count, field of view, ship fly-in time
- Propulsion trail: length, fade speed, color, width

### Leaderboard
- Maximum scores to keep (default: 10)
- Maximum name length (default: 12 characters)

### Menu System
- Section padding and element spacing
- Default font size for menu elements

Modify these constants to adjust gameplay behavior and visual effects.

## Logging
The game automatically generates two log files (gitignored by default):
- `asteroids/game_state.jsonl`: Periodic snapshots of game state (player position, asteroids, shots) every second for up to 16 seconds per session
- `asteroids/game_events.jsonl`: Event logs for asteroid destruction, splits, and player hits

These files are excluded from version control via `.gitignore`.
