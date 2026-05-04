# Menu System Feature

## Overview
Replace hardcoded screen drawing functions with a composable menu system where UI elements can be added or removed dynamically.

## Problem
Current screens have overlapping elements:
- Start menu: title + leaderboard + prompt
- Game over: "GAME OVER" + score + retry prompt
- High score entry: "NEW HIGH SCORE!" + score + name input + leaderboard

## Solution
Create a `Menu` class that manages a list of UI elements. Each element has:
- Text to render
- Position (y-offset from center)
- Font size
- Color (default white)

### API
```python
class MenuElement:
    def __init__(self, text, y_offset=0, font_size=None, color="white")

class Menu:
    def __init__(self)
    def add(self, element)
    def remove(self, element)  # by text
    def clear(self)
    def draw(screen)
```

### Usage Example
```python
menu = Menu()
menu.add(MenuElement("ASTEROIDS", -200, 50))
menu.add(MenuElement("HIGH SCORES", -130, 30))
for i, entry in enumerate(leaderboard.get_top()):
    menu.add(MenuElement(f"{i+1}. {entry['name']:<12} {entry['score']:>5}", -90 + i*30, 30))
menu.add(MenuElement("Press ENTER to start", 280, 25))
menu.draw(screen)
```

## Implementation

### Files Created/Modified
- New: `asteroids/menu.py` - Menu and MenuElement classes
- Modify: `asteroids/main.py` - Use Menu class for all screens
- Modify: `asteroids/constants.py` - Added MENU_DEFAULT_FONT_SIZE

### Constants Added
```python
MENU_DEFAULT_FONT_SIZE = 30
```

### Key Changes
1. `draw_game_over()` now uses Menu instead of direct blit calls
2. `draw_start_menu()` uses Menu, dynamically adds leaderboard entries
3. `draw_name_entry()` uses Menu, accepts name parameter for cursor rendering
4. Removed redundant `pygame.display.flip()` calls since Menu.draw() handles flip