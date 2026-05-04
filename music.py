import numpy as np
import pygame
from pygame import sndarray

# Constants for music system
try:
    from constants import (
        MUSIC_BPM,
        MUSIC_STEPS_PER_BAR,
        MUSIC_SAMPLE_RATE,
        MUSIC_BASS_A2,
        MUSIC_BASS_C3,
        MUSIC_BASS_D3,
        MUSIC_BASS_E3,
        MUSIC_BASS_G3,
        MUSIC_BASS_A3,
        MUSIC_CHORD_AM,
        MUSIC_CHORD_EM,
    )
except ImportError:
    # Fallback defaults
    MUSIC_BPM = 120
    MUSIC_STEPS_PER_BAR = 16
    MUSIC_SAMPLE_RATE = 44100
    MUSIC_BASS_A2 = 110.0
    MUSIC_BASS_C3 = 130.81
    MUSIC_BASS_D3 = 146.83
    MUSIC_BASS_E3 = 164.81
    MUSIC_BASS_G3 = 196.00
    MUSIC_BASS_A3 = 220.0
    MUSIC_CHORD_AM = 110.0
    MUSIC_CHORD_EM = 164.81


# === INSTRUMENT SYNTHESIS ===


def synth_kick_808(duration=0.5, pitch_start=150, pitch_end=50):
    """808 kick - sine wave with pitch envelope (150Hz -> 50Hz)."""
    t = np.linspace(0, duration, int(MUSIC_SAMPLE_RATE * duration), False)
    pitch_env = np.exp(-t * 10)
    pitch = pitch_start * pitch_env + pitch_end
    phase = np.cumsum(2 * np.pi * pitch / MUSIC_SAMPLE_RATE)
    wave = np.sin(phase)
    envelope = np.exp(-t * 0.005)
    return (wave * envelope * 0.9).astype(np.float32)


def synth_snare(duration=0.2, tone_freq=180):
    """Snare - white noise burst + 180Hz tone."""
    t = np.linspace(0, duration, int(MUSIC_SAMPLE_RATE * duration), False)
    noise = np.random.uniform(-1, 1, len(t))
    tone = np.sin(2 * np.pi * tone_freq * t)
    wave = noise * 0.7 + tone * 0.3
    envelope = np.exp(-t * 30)
    return (wave * envelope * 0.8).astype(np.float32)


def synth_bass(freq, duration=0.3):
    """Bass - sawtooth wave with envelope."""
    t = np.linspace(0, duration, int(MUSIC_SAMPLE_RATE * duration), False)
    wave = 2 * (t * freq - np.floor(t * freq + 0.5))  # Sawtooth
    envelope = np.exp(-t * 5)
    return (wave * envelope * 0.6).astype(np.float32)


def synth_guitar_chord(root_freq, duration=0.4, detune=0.02):
    """Guitar chord - detuned sawtooths with soft-clipping distortion."""
    t = np.linspace(0, duration, int(MUSIC_SAMPLE_RATE * duration), False)
    freqs = [root_freq, root_freq * 1.2, root_freq * 1.5]  # Minor triad
    wave = np.zeros(len(t))
    for freq in freqs:
        for offset in [-detune, 0, detune]:
            wave += np.sin(2 * np.pi * freq * (1 + offset) * t) * 0.15
    wave = np.tanh(wave * 2)  # Soft clipping
    envelope = np.exp(-t * 3)
    return (wave * envelope * 0.5).astype(np.float32)


def make_stereo(mono):
    """Convert mono array to stereo."""
    return np.column_stack((mono, mono))


# === MUSIC SEQUENCER ===


class MusicSequencer:
    def __init__(self, bpm=120, steps_per_bar=16):
        self.bpm = bpm
        self.steps_per_bar = steps_per_bar
        self.step_duration = 60.0 / bpm / (steps_per_bar / 4)
        self.patterns = []
        self.current_step = 0
        self.playing = False
        self._step_timer = 0

    def add_pattern(self, pattern, loop=True):
        """Add a pattern: list of (instrument, note, step) tuples."""
        self.patterns.append({'pattern': pattern, 'loop': loop, 'step': 0})

    def _play_sound(self, sound_array):
        """Play a sound array through pygame."""
        try:
            stereo = make_stereo(sound_array)
            sound = sndarray.make_sound(stereo)
            sound.play()
        except Exception as e:
            print(f"Music error: {e}")

    def update(self, dt):
        """Update sequencer - call every frame with delta time."""
        if not self.playing:
            return
        self._step_timer += dt
        if self._step_timer >= self.step_duration:
            self._step_timer = 0
            self._play_step(self.current_step)
            self.current_step = (self.current_step + 1) % self.steps_per_bar

    def _play_step(self, step):
        """Play all sounds for a given step."""
        for pattern_data in self.patterns:
            for instrument, note, pattern_step in pattern_data['pattern']:
                if pattern_step % self.steps_per_bar == step:
                    self._trigger(instrument, note)

    def _trigger(self, instrument, note):
        """Trigger an instrument with a note."""
        if instrument == 'kick':
            self._play_sound(synth_kick_808())
        elif instrument == 'snare':
            self._play_sound(synth_snare())
        elif instrument == 'bass':
            freqs = {
                'A2': MUSIC_BASS_A2,
                'C3': MUSIC_BASS_C3,
                'D3': MUSIC_BASS_D3,
                'E3': MUSIC_BASS_E3,
                'G3': MUSIC_BASS_G3,
                'A3': MUSIC_BASS_A3,
            }
            freq = freqs.get(note, MUSIC_BASS_A2)
            self._play_sound(synth_bass(freq, duration=self.step_duration * 2))
        elif instrument == 'guitar':
            freqs = {
                'Am': MUSIC_CHORD_AM,
                'Em': MUSIC_CHORD_EM,
            }
            freq = freqs.get(note, MUSIC_CHORD_AM)
            self._play_sound(synth_guitar_chord(freq, duration=self.step_duration * 2))


# === PRESET PATTERNS ===


def create_main_riff():
    """Main musical pattern - driving rhythm with bass and guitar."""
    pattern = []
    # Kick on 0, 4, 8, 12 (four on the floor)
    for i in [0, 4, 8, 12]:
        pattern.append(('kick', None, i))
    # Snare on 4, 12 (backbeat)
    for i in [4, 12]:
        pattern.append(('snare', None, i))
    # Bass riff - A minor pentatonic groove
    bass_notes = [
        ('A2', 0), ('A2', 2), ('C3', 4), ('D3', 6),
        ('E3', 8), ('E3', 9), ('D3', 10), ('C3', 12), ('A2', 14)
    ]
    for note, step in bass_notes:
        pattern.append(('bass', note, step))
    # Guitar chord stabs on 1 and 9
    pattern.append(('guitar', 'Am', 0))
    pattern.append(('guitar', 'Em', 8))
    return pattern


def create_intensity_riff():
    """Intense pattern - faster kick, driving bass, more guitar."""
    pattern = []
    # Faster kick (every 2 steps)
    for i in range(0, 16, 2):
        pattern.append(('kick', None, i))
    # Snare on 4, 8, 12
    for i in [4, 8, 12]:
        pattern.append(('snare', None, i))
    # Driving bass (every step)
    bass_notes = [
        ('A2', 0), ('C3', 2), ('D3', 4), ('E3', 6),
        ('A2', 8), ('C3', 10), ('D3', 12), ('E3', 14)
    ]
    for note, step in bass_notes:
        pattern.append(('bass', note, step))
    # Guitar on every downbeat
    for i in [0, 4, 8, 12]:
        pattern.append(('guitar', 'Am', i))
    return pattern


# === GLOBAL MANAGER ===

_music = None


def init_music():
    """Initialize the music system."""
    global _music
    _music = MusicSequencer(bpm=MUSIC_BPM)
    _music.add_pattern(create_main_riff())
    _music.playing = True
    return _music


def update_music(dt):
    """Update music sequencer - call every frame."""
    if _music:
        _music.update(dt)


def set_music_intensity(level):
    """Set music intensity (0 = normal, 1 = intense)."""
    if _music:
        _music.patterns.clear()
        if level >= 1:
            _music.add_pattern(create_intensity_riff())
        else:
            _music.add_pattern(create_main_riff())


def is_music_playing():
    """Check if music is playing."""
    return _music is not None and _music.playing
