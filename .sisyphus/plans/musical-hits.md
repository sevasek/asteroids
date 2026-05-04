# Musical Sound Effects - Asteroid Hit Combo System

## TL;DR

> **Quick Summary**: Add escalating musical combo sounds when hitting asteroids. 7-stage progression from simple tones to complex chords with bass and high octaves. Uses A minor pentatonic scale. Combo maintained if hits are within 0.5 seconds.
>
> **Deliverables**:
> - New `audio.py` module with HitSound class and ComboTracker class
> - AUDIO_* constants in `constants.py`
> - Integration in `main.py` to trigger sounds on asteroid hits
>
> **Estimated Effort**: Short-Medium
> **Parallel Execution**: NO - sequential tasks
> **Critical Path**: Task 1 (audio module) → Task 2 (integration) → Task 3 (QA)

---

## Context

### Original Request
"sound effects for when the player shoots an asteroid. there is a tone that plays if there is a hit. but if subsequent hits are within a certain number of seconds from the previous hit (lets say 0.5 seconds) then the tone goes up through the scale. can we use midi to do this?"

### Interview Summary
**User Decisions**:
- **Scale**: A Minor Pentatonic (A4=440, C5=523.25, D5=587.33, E5=659.25, G5=783.99)
- **Combo timeout**: 0.5 seconds between hits to maintain combo
- **Max combo**: 7 stages, then stays at top
- **Sound complexity progression**:
  1. 0.1s simple root tone
  2. 0.2s simple root tone
  3. 2.0s sustained root note
  4. 2.0s minor triad chord (root + third + fifth)
  5. 0.3s short minor triad chord
  6. 0.3s chord + bass octave (A3=220Hz)
  7. 0.3s chord + bass + staccato high octave (A5=880Hz)
- **Implementation**: Generate tones with pygame.sndarray (not MIDI)

### Technical Approach
Use `pygame.sndarray` and NumPy to generate sine wave tones programmatically. No external audio files needed. Each combo stage builds a composite waveform from multiple tones with different envelopes (decay, sustain, staccato).

---

## Work Objectives

### Core Objective
Create a satisfying musical combo system where rapid asteroid hits produce escalating musical complexity, rewarding skilled play with richer sounds.

### Concrete Deliverables
- `audio.py`: New module with HitSound class (generates composite waveforms) and ComboTracker class (manages combo state)
- `constants.py`: AUDIO_SAMPLE_RATE, AUDIO_COMBO_TIMEOUT, SCALE_A_MINOR_PENTATONIC frequencies
- `main.py`: Initialize audio, create ComboTracker instance, trigger sounds in check_collisions()

### Definition of Done
- [ ] Sound plays on each asteroid hit
- [ ] Combo increments if hit within 0.5s of previous
- [ ] Combo resets if >0.5s between hits
- [ ] All 7 combo stages produce correct sounds
- [ ] After stage 7, stays at stage 7 until combo breaks
- [ ] Uses A minor pentatonic scale
- [ ] Game runs without audio errors
- [ ] Graceful fallback if audio unavailable

### Must Have
- 7-stage combo system with specified durations and complexity
- A minor pentatonic scale (A4, C5, D5, E5, G5)
- 0.5s timeout between hits to maintain combo
- Sine wave generation via pygame.sndarray
- Proper envelopes: decay (quick fade), sustain (hold then fade), staccato (very quick)
- Combo stays at max (stage 7) until timeout

### Must NOT Have (Guardrails)
- No external audio files (WAV/MP3)
- No MIDI dependencies
- No blocking audio calls in game loop
- No performance degradation (<1ms audio generation time)
- No memory leaks (clean up sound objects)

---

## Execution Strategy

### Sequential Execution

```
Task 1: Create audio.py module [quick]
  ↓
Task 2: Add constants and integrate into main.py [quick]
  ↓
Task 3: Agent QA verification [quick]
  ↓
COMPLETE
```

### Agent Dispatch Summary

- **Task 1**: `quick` category
- **Task 2**: `quick` category
- **Task 3**: `quick` category

---

## TODOs

- [ ] 1. **Create audio.py module**

  **What to do**:
  Create new file `audio.py` with two classes:

  ### Class: ComboTracker
  ```python
  class ComboTracker:
      def __init__(self, timeout=0.5):
          self.last_hit_time = 0
          self.combo_position = 0  # 0-6 (represents stages 1-7)
          self.timeout = timeout
          # A minor pentatonic: A4, C5, D5, E5, G5
          self.scale = [440.0, 523.25, 587.33, 659.25, 783.99]
      
      def on_hit(self, current_time):
          """Call when asteroid is hit. Returns (combo_pos, root_frequency)."""
          if current_time - self.last_hit_time > self.timeout:
              self.combo_position = 0
          else:
              self.combo_position = min(self.combo_position + 1, 6)
          
          self.last_hit_time = current_time
          root_freq = self.scale[self.combo_position % len(self.scale)]
          return self.combo_position, root_freq
      
      def reset(self):
          self.combo_position = 0
          self.last_hit_time = 0
  ```

  ### Class: HitSound
  ```python
  import numpy as np
  import pygame
  from pygame import sndarray
  
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
          """Build list of (frequency, amplitude, envelope_type)."""
          tones = []
          
          if self.position == 0:
              # Stage 1: 0.1s simple root, decay envelope
              tones = [(self.root, 0.8, 'decay')]
          
          elif self.position == 1:
              # Stage 2: 0.2s simple root, decay envelope
              tones = [(self.root, 0.8, 'decay')]
          
          elif self.position == 2:
              # Stage 3: 2.0s sustained root
              tones = [(self.root, 0.7, 'sustain')]
          
          elif self.position == 3:
              # Stage 4: 2.0s minor triad chord (root + minor third + fifth)
              # A minor: root=1.0, third=1.2 (6:5 ratio), fifth=1.5 (3:2 ratio)
              tones = [
                  (self.root, 0.5, 'sustain'),
                  (self.root * 1.2, 0.3, 'sustain'),  # minor third
                  (self.root * 1.5, 0.3, 'sustain'),  # fifth
              ]
          
          elif self.position == 4:
              # Stage 5: 0.3s minor triad chord (shorter)
              tones = [
                  (self.root, 0.5, 'decay'),
                  (self.root * 1.2, 0.3, 'decay'),
                  (self.root * 1.5, 0.3, 'decay'),
              ]
          
          elif self.position == 5:
              # Stage 6: 0.3s chord + bass octave
              tones = [
                  (self.root, 0.4, 'decay'),
                  (self.root * 1.2, 0.25, 'decay'),
                  (self.root * 1.5, 0.25, 'decay'),
                  (self.root / 2, 0.6, 'decay'),  # bass octave
              ]
          
          elif self.position >= 6:
              # Stage 7: 0.3s chord + bass + staccato high octave
              tones = [
                  (self.root, 0.35, 'decay'),
                  (self.root * 1.2, 0.2, 'decay'),
                  (self.root * 1.5, 0.2, 'decay'),
                  (self.root / 2, 0.5, 'decay'),   # bass
                  (self.root * 2, 0.7, 'staccato'), # high octave, staccato
              ]
          
          return tones
      
      def generate_waveform(self, sample_rate=44100):
          """Generate composite waveform from all tones."""
          num_samples = int(sample_rate * self.duration)
          t = np.linspace(0, self.duration, num_samples, False)
          
          # Start with silence
          composite = np.zeros(num_samples)
          
          for freq, amp, env_type in self.tones:
              # Generate sine wave
              wave = np.sin(2 * np.pi * freq * t)
              
              # Apply envelope
              if env_type == 'decay':
                  # Exponential decay (tau=0.3 for quick fade)
                  envelope = np.exp(-t * 3)
              elif env_type == 'sustain':
                  # Full volume, then fade at end
                  envelope = np.ones_like(t)
                  fade_start = int(len(t) * 0.85)
                  if fade_start < len(t):
                      envelope[fade_start:] = np.linspace(1, 0, len(t) - fade_start)
              elif env_type == 'staccato':
                  # Very quick attack and decay
                  envelope = np.exp(-t * 15)
              
              # Add to composite
              composite += wave * envelope * amp
          
          # Normalize to prevent clipping
          max_val = np.max(np.abs(composite))
          if max_val > 0:
              composite = composite / max_val * 0.8
          
          # Convert to 16-bit PCM
          audio = (composite * 32767).astype(np.int16)
          
          return audio
      
      def play(self):
          """Generate and play the sound."""
          try:
              waveform = self.generate_waveform()
              # Make it stereo by duplicating
              stereo = np.column_stack((waveform, waveform))
              sound = sndarray.make_sound(stereo)
              sound.play()
          except Exception as e:
              # Graceful fallback - log but don't crash
              print(f"Audio error: {e}")
  ```

  **Must NOT do**:
  - Do not import pygame at module level (import inside functions to avoid circular imports)
  - Do not create external dependencies

  **Acceptance Criteria**:
  - [ ] ComboTracker class with on_hit() method
  - [ ] HitSound class with generate_waveform() and play() methods
  - [ ] All 7 combo stages build correct tone lists
  - [ ] No syntax errors

  **QA**:
  ```
  python -c "from audio import ComboTracker, HitSound; print('OK')"
  ```

  **Commit**: YES
  - Message: `feat(audio): add ComboTracker and HitSound classes for musical hit combo system`
  - Files: `audio.py`

---

- [ ] 2. **Add constants and integrate into main.py**

  **What to do**:

  ### Step 2.1: Add constants to constants.py
  Add after EXHAUST_INTENSITY_CAP:
  ```python
  # Audio settings
  AUDIO_SAMPLE_RATE = 44100
  AUDIO_COMBO_TIMEOUT = 0.5  # seconds between hits to maintain combo
  # A minor pentatonic scale frequencies (Hz)
  AUDIO_SCALE_A_MINOR_PENTATONIC = [440.0, 523.25, 587.33, 659.25, 783.99]
  ```

  ### Step 2.2: Initialize pygame mixer in main.py
  In `run_game()`, after `reset_logger()` and before creating groups:
  ```python
  # Initialize audio
  try:
      pygame.mixer.init(frequency=AUDIO_SAMPLE_RATE, size=-16, channels=2, buffer=512)
      audio_enabled = True
  except Exception as e:
      print(f"Audio initialization failed: {e}")
      audio_enabled = False
  
  # Create combo tracker
  from audio import ComboTracker
  combo_tracker = ComboTracker(timeout=AUDIO_COMBO_TIMEOUT)
  ```

  ### Step 2.3: Import HitSound in check_collisions
  At top of check_collisions():
  ```python
  from audio import HitSound
  ```

  ### Step 2.4: Trigger sound on asteroid hit
  In the shot-asteroid collision block, AFTER spawn_explosion():
  ```python
  for s in shots.copy():
      if a.collides_with(s):
          log_event("asteroid_shot")
          spawn_explosion(a.position.copy(), a.radius, explosion_particles)
          
          # Play combo sound
          if audio_enabled:
              combo_pos, root_freq = combo_tracker.on_hit(pygame.time.get_ticks() / 1000.0)
              hit_sound = HitSound(combo_pos, root_freq)
              hit_sound.play()
          
          a.split()
          s.kill()
          score_delta += 10
          break
  ```

  ### Step 2.5: Update check_collisions signature
  ```python
  def check_collisions(asteroids, shots, player, explosion_particles, combo_tracker, audio_enabled):
  ```

  ### Step 2.6: Update check_collisions call
  In run_game():
  ```python
  player_hit, delta = check_collisions(asteroids, shots, player, explosion_particles, combo_tracker, audio_enabled)
  ```

  **Must NOT do**:
  - Do not make audio blocking - sound.play() is non-blocking
  - Do not crash if audio fails to initialize

  **Acceptance Criteria**:
  - [ ] pygame.mixer initialized in run_game()
  - [ ] ComboTracker created and passed to check_collisions
  - [ ] Sound plays on asteroid hit
  - [ ] Combo increments/timeout works correctly

  **Commit**: YES
  - Message: `feat(audio): integrate musical hit combo system into main game loop`
  - Files: `constants.py`, `main.py`

---

- [ ] 3. **Agent QA verification**

  **What to do**:
  1. Launch game
  2. Shoot asteroids rapidly (<0.5s apart)
  3. Verify sounds escalate through combo stages
  4. Wait >0.5s between shots, verify combo resets
  5. Verify no audio errors

  **Acceptance Criteria**:
  - [ ] Game launches without audio errors
  - [ ] Sound plays on each hit
  - [ ] Rapid hits produce escalating sounds
  - [ ] Slow hits reset to simple tone
  - [ ] No performance issues

  **Commit**: NO (QA only)

---

## Commit Strategy

- **Commit 1** (Task 1): `feat(audio): add ComboTracker and HitSound classes for musical hit combo system`
  - Files: `audio.py`

- **Commit 2** (Task 2): `feat(audio): integrate musical hit combo system into main game loop`
  - Files: `constants.py`, `main.py`

---

## Success Criteria

### Verification Commands
```bash
python -c "from audio import ComboTracker, HitSound; print('OK')"  # Expected: OK
python -c "from constants import AUDIO_COMBO_TIMEOUT; print('OK')"  # Expected: OK
uv run python main.py  # Expected: game launches, sounds work
```

### Final Checklist
- [ ] audio.py created with ComboTracker and HitSound
- [ ] AUDIO_* constants in constants.py
- [ ] pygame.mixer initialized in main.py
- [ ] Sound triggers on asteroid hit
- [ ] 7-stage combo progression works
- [ ] 0.5s timeout resets combo
- [ ] Graceful fallback if audio unavailable
- [ ] Game runs without errors
