# Configuration

The firmware loads configuration from `config.json` at boot. If the file is missing
or invalid, defaults are used.

## Schema overview

```json
{
  "schema_version": 1,
  "chords": {
    "default": [0],
    "12": [0, 3, 10],
    "13": [0, 4, 11],
    "14": [0, 3, 7],
    "15": [0, 4, 7]
  },
  "velocity_levels": [127, 80, 40],
  "velocity_colors": [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
  "leds": {
    "brightness_scale": 0.9,
    "base_note_color": [150, 150, 150],
    "alt_active_color": [0, 0, 255],
    "alt_inactive_color": [150, 150, 150],
    "modifier_oscillate_min": 10,
    "modifier_oscillate_max": 140,
    "modifier_oscillate_speed": 2.2,
    "static_key_colors": {"0": [255, 128, 0]}
  },
  "notes": {
    "base_notes": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71],
    "base_note_offset": 0,
    "min_octave_offset": -36,
    "max_octave_offset": 36
  },
  "alt_toggle_window": 0.45
}
```

### Chords

- `chords.default`: interval list used when no modifier key is pressed.
- `chords.12`-`chords.15`: intervals used when that key is the *only* modifier held.

### LEDs

- `static_key_colors` allows per-key overrides for idle LEDs.
- Oscillation values control the pulsing modifier LEDs.

### Velocity

- `velocity_levels` are cycled when using the velocity modifier in alt mode.
- `velocity_colors` map to the levels above for LED feedback.

## Recovery key

The recovery key index is controlled via `settings.toml`:

```
RECOVERY_KEY_INDEX = 15
```

Hold that key while booting to re-enable the `CIRCUITPY` USB drive.

