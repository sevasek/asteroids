import os
import pygame

MUSIC_DIR = os.path.join(os.path.dirname(__file__), "music")
MUSIC_FILES = [
    "0_drums.mp3",
    "1_bass.mp3",
    "2_percussion.mp3",
    "3_synth.mp3",
    "4_other.mp3",
]

_sounds = []
_music_started = False


def init_music():
    """Load all MP3 files from music/ directory."""
    global _sounds, _music_started

    _sounds = []
    _music_started = False

    for filename in MUSIC_FILES:
        filepath = os.path.join(MUSIC_DIR, filename)
        try:
            sound = pygame.mixer.Sound(filepath)
            _sounds.append(sound)
        except Exception as e:
            print(f"Failed to load {filename}: {e}")

    return len(_sounds) > 0


def start_music():
    """Play all loaded MP3 files simultaneously in a loop."""
    global _music_started

    if _music_started or not _sounds:
        return

    for sound in _sounds:
        sound.play(loops=-1)  # Loop forever

    _music_started = True


def stop_music():
    """Stop all music."""
    global _music_started

    for sound in _sounds:
        sound.stop()

    _music_started = False


def update_music(dt):
    """No-op for MP3 version - music runs continuously."""
    pass


def set_music_intensity(level):
    """No-op for MP3 version - intensity not implemented."""
    pass


def is_music_playing():
    """Check if music is playing."""
    return _music_started
