# Firmware updater workflow

This repo now ships a single-file GUI updater that flashes the CircuitPython
filesystem over USB serial (no BOOTSEL or drag-and-drop required). The updater
auto-runs when opened, so non-technical users can just double-click it.

## Build the updater

1. Install mpremote: `pip install mpremote`.
2. Run the build script:
   ```bash
   python tools/build_update.py
   ```
3. The output updater will be created at `dist/thx_update.py`.

## Distribute the updater

Give end users the single `thx_update.py` file. When they open it, it:

- Opens a simple GUI with a progress bar and starts updating automatically.
- Installs the small `mpremote` helper automatically if needed.
- Detects the Pico via `python -m mpremote connect auto`.
- Pushes `code.py`, `boot.py`, `settings.toml`, and the entire `lib/` folder.

If users need to run it again, there is an "Update Again" button in the window.

## Device behavior

`boot.py` disables the CIRCUITPY drive and leaves the serial console enabled,
so the device feels like a finished product while still being updateable from
the GUI updater.
