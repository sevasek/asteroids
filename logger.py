import json
import math
from constants import LOG_MAX_SECONDS, LOG_FPS, LOG_SPRITE_SAMPLE_LIMIT
from datetime import datetime

__all__ = ["log_state", "log_event", "reset_logger"]

_frame_count = 0
_state_log_initialized = False
_event_log_initialized = False
_start_time = datetime.now()


def reset_logger():
    global _frame_count, _state_log_initialized, _event_log_initialized, _start_time
    _frame_count = 0
    _state_log_initialized = False
    _event_log_initialized = False
    _start_time = datetime.now()


def log_state(player, drawable, asteroids, shots):
    global _frame_count, _state_log_initialized

    if _frame_count > LOG_FPS * LOG_MAX_SECONDS:
        return

    _frame_count += 1
    if _frame_count % LOG_FPS != 0:
        return

    now = datetime.now()

    game_state = {}

    if player is not None:
        player_info = {"type": player.__class__.__name__}
        player_info["pos"] = [round(player.position.x, 2), round(player.position.y, 2)]
        if hasattr(player, "velocity"):
            player_info["vel"] = [round(player.velocity.x, 2), round(player.velocity.y, 2)]
        if hasattr(player, "radius"):
            player_info["rad"] = player.radius
        if hasattr(player, "rotation"):
            player_info["rot"] = round(player.rotation, 2)
        game_state["player"] = player_info

    for key, value in [("drawable", drawable), ("asteroids", asteroids), ("shots", shots)]:
        sprites_data = []
        for i, sprite in enumerate(value):
            if i >= LOG_SPRITE_SAMPLE_LIMIT:
                break
            sprite_info = {"type": sprite.__class__.__name__}
            if hasattr(sprite, "position"):
                sprite_info["pos"] = [round(sprite.position.x, 2), round(sprite.position.y, 2)]
            if hasattr(sprite, "velocity"):
                sprite_info["vel"] = [round(sprite.velocity.x, 2), round(sprite.velocity.y, 2)]
            if hasattr(sprite, "radius"):
                sprite_info["rad"] = sprite.radius
            if hasattr(sprite, "rotation"):
                sprite_info["rot"] = round(sprite.rotation, 2)
            sprites_data.append(sprite_info)
        game_state[key] = {"count": len(value), "sprites": sprites_data}

    entry = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        **game_state,
    }

    mode = "w" if not _state_log_initialized else "a"
    with open("game_state.jsonl", mode) as f:
        f.write(json.dumps(entry) + "\n")

    _state_log_initialized = True


def log_event(event_type, **details):
    global _event_log_initialized

    now = datetime.now()

    event = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,
    }

    mode = "w" if not _event_log_initialized else "a"
    with open("game_events.jsonl", mode) as f:
        f.write(json.dumps(event) + "\n")

    _event_log_initialized = True
