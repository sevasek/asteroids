# High Score Leaderboard Feature

## Overview
Add a persistent leaderboard displayed at the game start menu showing the top 10 high scores.

## Storage
- **File**: `asteroids/leaderboard.json` (local JSON file)
- **Format**:
```json
[
  {"name": "ABC", "score": 1500, "date": "2026-05-04"},
  ...
]
```
- **Max entries**: 10
- **Name length**: Up to 12 characters

## Implementation Notes

### Code Review Fixes
1. Added error handling in `_load()` for corrupted JSON files
2. Added empty list check in `is_high_score()` to prevent IndexError on empty leaderboard
3. Name entry screen redraws background each frame, avoiding visual artifacts

### Files Modified/Created
- `asteroids/constants.py` - Added leaderboard font sizes and max length constants
- `asteroids/leaderboard.py` - New module with `Leaderboard` class
- `asteroids/main.py` - Added start menu, name entry, and game over flow

### Constants Added
```python
LEADERBOARD_TITLE_SIZE = 50
LEADERBOARD_ENTRY_SIZE = 30
LEADERBOARD_PROMPT_SIZE = 25
LEADERBOARD_MAX_NAME_LENGTH = 12
LEADERBOARD_MAX_SCORES = 10
```

### Leaderboard Class API
- `Leaderboard(filepath)` - Initialize, loads from JSON file
- `get_top()` - Returns top 10 scores
- `is_high_score(score)` - Returns True if score qualifies for leaderboard
- `add_score(name, score)` - Adds score if qualified, saves to file

### User Flow
1. Game launches → Start menu displays with title + top 10 scores + "Press ENTER to start"
2. Player presses ENTER → Game begins
3. Player dies → If score is top 10, prompt for name entry (up to 12 chars)
4. Score saved → Show game over screen with retry option
5. On retry → Return to start menu with updated leaderboard