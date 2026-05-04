import numpy as np
import pygame
from pygame import sndarray
from constants import (
    AUDIO_COMBO_TIMEOUT,
    AUDIO_SCALE_A_MINOR_PENTATONIC,
    AUDIO_COMBO_DURATIONS,
    AUDIO_CHORD_MINOR_THIRD,
    AUDIO_DECAY_RATE,
    AUDIO_SUSTAIN_FADE_START,
    AUDIO_AMP_ROOT_PRIMARY,
    AUDIO_AMP_ROOT_SECONDARY,
    AUDIO_AMP_ROOT_CHORD,
    AUDIO_AMP_THIRD,
)


class ComboTracker:
    def __init__(self, timeout=None):
        self.last_hit_time = 0
        self.combo_position = 0
        self.timeout = timeout if timeout is not None else AUDIO_COMBO_TIMEOUT
        self.scale = AUDIO_SCALE_A_MINOR_PENTATONIC

    def on_hit(self, current_time):
        if current_time - self.last_hit_time > self.timeout:
            self.combo_position = 0
        else:
            self.combo_position = min(self.combo_position + 1, 6)

        self.last_hit_time = current_time
        root_freq = self.scale[self.combo_position % len(self.scale)]
        return self.combo_position, root_freq


class HitSound:
    def __init__(self, combo_position, root_frequency):
        self.position = combo_position
        self.root = root_frequency
        self.duration = self._get_duration()
        self.tones = self._build_tones()

    def _get_duration(self):
        return AUDIO_COMBO_DURATIONS[self.position]

    def _build_tones(self):
        if self.position == 0:
            tones = [(self.root, AUDIO_AMP_ROOT_PRIMARY, "decay")]
        elif self.position == 1:
            tones = [(self.root, AUDIO_AMP_ROOT_PRIMARY, "decay")]
        elif self.position == 2:
            tones = [(self.root, AUDIO_AMP_ROOT_SECONDARY, "sustain")]
        elif self.position >= 3:
            tones = [
                (self.root, AUDIO_AMP_ROOT_CHORD, "decay"),
                (self.root * AUDIO_CHORD_MINOR_THIRD, AUDIO_AMP_THIRD, "decay"),
            ]
        return tones

    def generate_waveform(self, sample_rate=44100):
        num_samples = int(sample_rate * self.duration)
        t = np.linspace(0, self.duration, num_samples, False)
        composite = np.zeros(num_samples)

        for freq, amp, env_type in self.tones:
            wave = np.sin(2 * np.pi * freq * t)

            if env_type == "decay":
                envelope = np.exp(-t * AUDIO_DECAY_RATE)
            elif env_type == "sustain":
                envelope = np.ones_like(t)
                fade_start = int(len(t) * AUDIO_SUSTAIN_FADE_START)
                if fade_start < len(t):
                    envelope[fade_start:] = np.linspace(1, 0, len(t) - fade_start)

            composite += wave * envelope * amp

        max_val = np.max(np.abs(composite))
        if max_val > 0:
            composite = composite / max_val * 0.8

        audio = (composite * 32767).astype(np.int16)
        return audio

    def play(self):
        try:
            waveform = self.generate_waveform()
            stereo = np.column_stack((waveform, waveform))
            sound = sndarray.make_sound(stereo)
            sound.play()
        except Exception as e:
            print(f"Audio error: {e}")
