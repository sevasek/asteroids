# Draft: Musical Sound Effects for Asteroid Hits - Combo System

## User Decisions (Confirmed)

### Scale: A Minor Pentatonic
Frequencies (Hz):
- A4 = 440.00 (root)
- C5 = 523.25 (minor third)
- D5 = 587.33 (fourth)
- E5 = 659.25 (fifth)
- G5 = 783.99 (minor seventh)

### Combo Behavior
- 0.5 second timeout between hits to maintain combo
- When reach position 7 (max), stay at top until combo breaks

### 7-Stage Combo Sound Design

| Position | Duration | Description | Tones |
|----------|----------|-------------|-------|
| 1 | 0.1s | Simple tone | Root note only |
| 2 | 0.2s | Simple tone, longer | Root note only |
| 3 | 2.0s | Sustained root | Root note sustained |
| 4 | 2.0s | Chord | Root + third + fifth (minor triad) |
| 5 | 0.3s | Short chord | Root + third + fifth (shorter) |
| 6 | 0.3s | Chord + bass | Chord + bass octave (A3 = 220Hz) |
| 7 | 0.3s | Full arrangement | Chord + bass + staccato high octave (A5 = 880Hz) |

## Technical Design

### Class Structure

```python
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
        # Returns list of (frequency, amplitude_ratio, envelope_type)
        # envelope_type: 'decay', 'sustain', 'staccato'
        pass
    
    def generate_waveform(self, sample_rate=44100):
        # Generate combined waveform from all tones
        # Apply envelopes
        pass

class ComboTracker:
    def __init__(self, timeout=0.5):
        self.last_hit_time = 0
        self.combo_position = 0
        self.timeout = timeout
        self.scale = [440.0, 523.25, 587.33, 659.25, 783.99]  # A minor pentatonic
    
    def on_hit(self, current_time):
        if current_time - self.last_hit_time > self.timeout:
            self.combo_position = 0
        else:
            self.combo_position = min(self.combo_position + 1, 6)
        
        self.last_hit_time = current_time
        return self.combo_position, self.scale[self.combo_position % len(self.scale)]
```

### Audio Generation with pygame.sndarray

```python
import numpy as np
import pygame
from pygame import sndarray

def generate_tone(frequency, duration, sample_rate=44100, envelope='decay'):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate sine wave
    wave = np.sin(2 * np.pi * frequency * t)
    
    # Apply envelope
    if envelope == 'decay':
        # Exponential decay
        env = np.exp(-t * 5)
    elif envelope == 'sustain':
        # Full volume then quick fade at end
        env = np.ones_like(t)
        fade_start = int(len(t) * 0.9)
        env[fade_start:] = np.linspace(1, 0, len(t) - fade_start)
    elif envelope == 'staccato':
        # Quick attack and decay
        env = np.exp(-t * 20)
    
    wave = wave * env
    
    # Convert to 16-bit PCM
    audio = (wave * 32767).astype(np.int16)
    
    return audio
```

## Implementation Plan

**Files to Create/Modify**:
- `audio.py`: New file with HitSound class, ComboTracker class, tone generation
- `constants.py`: Add AUDIO_* constants (sample rate, timeout, scale frequencies)
- `main.py`: 
  - Initialize pygame.mixer in run_game()
  - Create ComboTracker instance
  - Call audio generation on asteroid hit

**Guardrails**:
- Graceful fallback if audio initialization fails
- No blocking audio calls in game loop
- Minimal CPU impact (generate sounds on-demand, not every frame)

## Open Questions
None - all requirements specified by user.

## Acceptance Criteria
- [ ] Sound plays on each asteroid hit
- [ ] Combo position increments if hit within 0.5s of previous
- [ ] Combo resets to 0 if >0.5s between hits
- [ ] Each of 7 combo stages produces correct sound:
  - Pos 1: 0.1s simple tone
  - Pos 2: 0.2s simple tone
  - Pos 3: 2.0s sustained root
  - Pos 4: 2.0s minor triad chord
  - Pos 5: 0.3s minor triad chord
  - Pos 6: 0.3s chord + bass octave
  - Pos 7: 0.3s chord + bass + staccato high octave
- [ ] After pos 7, stays at pos 7 until combo breaks
- [ ] Uses A minor pentatonic scale
- [ ] Game runs without audio errors
