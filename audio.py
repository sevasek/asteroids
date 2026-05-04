import numpy as np
import pygame
from pygame import sndarray


class ComboTracker:
    def __init__(self, timeout=0.5):
        self.last_hit_time = 0
        self.combo_position = 0  # 0-6 (represents stages 1-7)
        self.timeout = timeout
        # A minor pentatonic: A4, C5, D5, E5, G5
        self.scale = [440.0, 523.25, 587.33, 659.25, 783.99]

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
        durations = [0.1, 0.2, 2.0, 2.0, 0.3, 0.3, 0.3]
        return durations[self.position]

    def _build_tones(self):
        if self.position == 0:
            tones = [(self.root, 0.8, "decay")]
        elif self.position == 1:
            tones = [(self.root, 0.8, "decay")]
        elif self.position == 2:
            tones = [(self.root, 0.7, "sustain")]
        elif self.position == 3:
            tones = [
                (self.root, 0.5, "sustain"),
                (self.root * 1.2, 0.3, "sustain"),
                (self.root * 1.5, 0.3, "sustain"),
            ]
        elif self.position == 4:
            tones = [
                (self.root, 0.5, "decay"),
                (self.root * 1.2, 0.3, "decay"),
                (self.root * 1.5, 0.3, "decay"),
            ]
        elif self.position == 5:
            tones = [
                (self.root, 0.4, "decay"),
                (self.root * 1.2, 0.25, "decay"),
                (self.root * 1.5, 0.25, "decay"),
                (self.root / 2, 0.6, "decay"),
            ]
        elif self.position >= 6:
            tones = [
                (self.root, 0.35, "decay"),
                (self.root * 1.2, 0.2, "decay"),
                (self.root * 1.5, 0.2, "decay"),
                (self.root / 2, 0.5, "decay"),
                (self.root * 2, 0.7, "staccato"),
            ]
        return tones

    def generate_waveform(self, sample_rate=44100):
        num_samples = int(sample_rate * self.duration)
        t = np.linspace(0, self.duration, num_samples, False)
        composite = np.zeros(num_samples)

        for freq, amp, env_type in self.tones:
            wave = np.sin(2 * np.pi * freq * t)

            if env_type == "decay":
                envelope = np.exp(-t * 3)
            elif env_type == "sustain":
                envelope = np.ones_like(t)
                fade_start = int(len(t) * 0.85)
                if fade_start < len(t):
                    envelope[fade_start:] = np.linspace(1, 0, len(t) - fade_start)
            elif env_type == "staccato":
                envelope = np.exp(-t * 15)

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
