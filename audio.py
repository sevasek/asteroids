import numpy as np
import pygame
from pygame import sndarray
from constants import (
    AUDIO_COMBO_TIMEOUT,
    AUDIO_SCALE_A_MINOR_PENTATONIC,
    AUDIO_COMBO_BASE_DURATION,
    AUDIO_COMBO_DURATION_STEP,
    AUDIO_DECAY_RATE,
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
            self.combo_position = self.combo_position + 1

        self.last_hit_time = current_time
        scale_index = self.combo_position % len(self.scale)
        frequency = self.scale[scale_index]
        return self.combo_position, frequency


class HitSound:
    def __init__(self, combo_position, root_frequency):
        self.position = combo_position
        self.frequency = root_frequency
        self.duration = AUDIO_COMBO_BASE_DURATION + (self.position * AUDIO_COMBO_DURATION_STEP)

    def _build_tones(self):
        return [(self.frequency, 0.8, "decay")]

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
