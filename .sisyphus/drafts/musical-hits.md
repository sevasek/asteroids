# Draft: Musical Sound Effects for Asteroid Hits

## Feature Request
Add sound effects when player shoots an asteroid:
- Base tone plays on hit
- If subsequent hits within 0.5 seconds, tone goes up through the scale
- Question: Use MIDI or generate tones programmatically?

## Technical Analysis

### Sound Options

**Option A: Pygame Mixer with Generated Tones**
- Use `pygame.mixer` and `pygame.sndarray` to generate sine waves
- Pros: No external files, programmatic control of pitch
- Cons: Requires audio generation code

**Option B: Pre-made Sound Files**
- Create/load WAV files for each scale note
- Pros: Simple playback with `pygame.mixer.Sound()`
- Cons: Need multiple files, less flexible

**Option C: MIDI**
- Pygame has `pygame.midi` module
- Pros: Native musical scale support
- Cons: More complex, may require MIDI setup on user's machine

**Recommendation**: Option A (generated tones) - gives most control, no external files needed

### Implementation Requirements

**State Tracking**:
- Track last hit timestamp
- Track current scale position (0-7 for C major scale: C-D-E-F-G-A-B-C)
- Reset scale position if >0.5s since last hit

**Scale Selection**:
- C Major pentatonic (C-D-E-G-A) - sounds "spacey"/ethereal
- C Major (C-D-E-F-G-A-B-C) - full scale
- User preference needed

**Audio Generation**:
- Generate sine wave tones at specific frequencies
- Apply envelope (attack/decay) for better sound
- Keep sounds short (0.1-0.2 seconds)

### Musical Scale Frequencies (Hz)
C4 = 261.63
D4 = 293.66
E4 = 329.63
F4 = 349.23
G4 = 392.00
A4 = 440.00
B4 = 493.88
C5 = 523.25

### Open Questions

1. **Scale choice**: C Major pentatonic or full C Major?
2. **Tone duration**: How long should each hit sound? (0.1s? 0.2s?)
3. **Reset behavior**: After reaching top of scale, start over or stay at top?
4. **Multiple rapid hits**: Should we queue sounds or interrupt previous?
5. **Volume**: Constant or fade with combo length?

## Implementation Approach

**Files to Modify**:
- `constants.py`: SOUND_* constants (scale frequencies, hit timeout, tone duration)
- `main.py`: 
  - Add sound initialization in `run_game()`
  - Track hit timing and combo state
  - Generate/play tone in `check_collisions()` when asteroid is hit
- New file (optional): `audio.py` - Sound generation utilities

**Logic Flow**:
```
On asteroid hit:
  current_time = now
  if current_time - last_hit_time > 0.5:
    scale_position = 0  # Reset to base note
  else:
    scale_position = (scale_position + 1) % len(scale)
  
  frequency = scale_frequencies[scale_position]
  play_tone(frequency, duration)
  last_hit_time = current_time
```

**Guardrails**:
- Must work on macOS (brew install sdl2 might be needed)
- Graceful fallback if audio unavailable
- No performance impact on game loop
