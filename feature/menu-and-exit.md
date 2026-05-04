# Menu and Exit Flow Refactor

## Current Problems
1. ESC at game over immediately quits instead of returning to menu
2. High score entry goes to game over without leaderboard
3. Font caching inefficiency in menu.py

## Proposed Flow

**Game End:**
- High score → prompt name → save → game over + leaderboard
- Not high score → game over + leaderboard
- ENTER = restart
- ESC = go to start menu

**Start Menu:**
- ENTER = play
- ESC = quit

## Changes Required

### 1. menu.py - Font Caching
Add `_font_cache` dict to cache fonts by size.

### 2. constants.py
Add event constants:
```python
EVENT_QUIT = "quit"
EVENT_RETRY = "retry"
EVENT_MENU = "menu"
```

### 3. poll_events()
Add `menu_mode` param - ESC returns "menu" when True, "quit" otherwise.

### 4. draw_game_over()
Add optional `leaderboard` param to display top scores.

### 5. main()
- Start menu: ESC quits game
- Game over: ESC returns to start menu
- Show leaderboard on game over when score qualifies

## Implementation Order
1. Font caching (menu.py)
2. Constants (constants.py)
3. poll_events() update
4. draw_game_over() update
5. main() loop refactor