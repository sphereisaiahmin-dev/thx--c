import hashlib
import json
import math
import os
import time

import supervisor
import usb_cdc
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

from keybow2040 import Keybow2040
# from keybow_hardware.pim56x import PIM56X as Hardware # for Keybow 2040
from keybow_hardware.pim551 import PIM551 as Hardware  # for Pico RGB Keypad Base


time.sleep(5)

FIRMWARE_VERSION_PATH = "firmware.version"
CONFIG_PATH = "config.json"

DEFAULT_CONFIG = {
    "schema_version": 1,
    "chords": {
        "default": [0],
        "12": [0, 3, 10],
        "13": [0, 4, 11],
        "14": [0, 3, 7],
        "15": [0, 4, 7],
    },
    "velocity_levels": [127, 80, 40],
    "velocity_colors": [
        [255, 0, 0],
        [0, 255, 0],
        [0, 0, 255],
    ],
    "leds": {
        "brightness_scale": 0.9,
        "base_note_color": [150, 150, 150],
        "alt_active_color": [0, 0, 255],
        "alt_inactive_color": [150, 150, 150],
        "modifier_oscillate_min": 10,
        "modifier_oscillate_max": 140,
        "modifier_oscillate_speed": 2.2,
        "static_key_colors": {},
    },
    "notes": {
        "base_notes": list(range(60, 72)),
        "base_note_offset": 0,
        "min_octave_offset": -36,
        "max_octave_offset": 36,
    },
    "alt_toggle_window": 0.45,
}


def read_text_file(path):
    try:
        with open(path, "r") as handle:
            return handle.read()
    except OSError:
        return ""


def read_json_file(path):
    try:
        with open(path, "r") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {}


def merge_config(defaults, overrides):
    if not isinstance(overrides, dict):
        return defaults
    merged = {}
    for key, value in defaults.items():
        override = overrides.get(key)
        if isinstance(value, dict):
            merged[key] = merge_config(value, override)
        else:
            merged[key] = override if override is not None else value
    for key, value in overrides.items():
        if key not in merged:
            merged[key] = value
    return merged


def read_firmware_version():
    version = read_text_file(FIRMWARE_VERSION_PATH).strip()
    return version or "unknown"


CONFIG = merge_config(DEFAULT_CONFIG, read_json_file(CONFIG_PATH))
FIRMWARE_VERSION = read_firmware_version()

BRIGHTNESS_SCALE = float(CONFIG["leds"]["brightness_scale"])

NOTE_KEY_INDICES = tuple(range(12))
MODIFIER_KEY_INDICES = (12, 13, 14, 15)
ALT_TOGGLE_KEY_INDEX = 12
VELOCITY_KEY_INDEX = 13
OCTAVE_DOWN_KEY_INDEX = 14
OCTAVE_UP_KEY_INDEX = 15

OSCILLATE_MIN = int(CONFIG["leds"]["modifier_oscillate_min"])
OSCILLATE_MAX = int(CONFIG["leds"]["modifier_oscillate_max"])
OSCILLATE_SPEED = float(CONFIG["leds"]["modifier_oscillate_speed"])

BASE_NOTE_COLOR = tuple(CONFIG["leds"]["base_note_color"])
ALT_ACTIVE_COLOR = tuple(CONFIG["leds"]["alt_active_color"])
ALT_INACTIVE_COLOR = tuple(CONFIG["leds"]["alt_inactive_color"])

BASE_NOTES = tuple(CONFIG["notes"]["base_notes"])
BASE_NOTE_OFFSET = int(CONFIG["notes"]["base_note_offset"])
MIN_OCTAVE_OFFSET = int(CONFIG["notes"]["min_octave_offset"])
MAX_OCTAVE_OFFSET = int(CONFIG["notes"]["max_octave_offset"])

ALT_TOGGLE_WINDOW = float(CONFIG["alt_toggle_window"])

VELOCITY_LEVELS = tuple(CONFIG["velocity_levels"])
VELOCITY_COLORS = tuple(tuple(color) for color in CONFIG["velocity_colors"])

MAX_CHORD_INTERVAL = 11
EMERGENCY_NOTE_MIN = min(BASE_NOTES) + BASE_NOTE_OFFSET + MIN_OCTAVE_OFFSET
EMERGENCY_NOTE_MAX = (
    max(BASE_NOTES) + BASE_NOTE_OFFSET + MAX_OCTAVE_OFFSET + MAX_CHORD_INTERVAL
)
EMERGENCY_NOTE_RANGE = range(EMERGENCY_NOTE_MIN, EMERGENCY_NOTE_MAX + 1)

STATIC_KEY_COLORS = {
    int(index): tuple(value)
    for index, value in CONFIG["leds"].get("static_key_colors", {}).items()
}

CHORD_INTERVALS = {"default": tuple(CONFIG["chords"].get("default", [0]))}
for key, value in CONFIG["chords"].items():
    if key == "default":
        continue
    CHORD_INTERVALS[int(key)] = tuple(value)


keybow = Keybow2040(Hardware())
keys = keybow.keys

active_chord_notes = []
active_notes = {}
last_alt_press_time = None
alt_mode_active = False
octave_offset = 0
velocity_index = 0


class UpdateSession:
    def __init__(self, data_channel):
        self.data = data_channel
        self.line_buffer = bytearray()
        self.binary_remaining = 0
        self.chunk_hash = None
        self.chunk_hash_expected = None
        self.active_file = None
        self.pending_files = {}
        self.manifest = None
        self.greeted = False
        self.error_state = None

    def reset(self):
        if self.active_file:
            self._close_active_file()
        self.line_buffer = bytearray()
        self.binary_remaining = 0
        self.chunk_hash = None
        self.chunk_hash_expected = None
        self.active_file = None
        self.pending_files = {}
        self.manifest = None
        self.greeted = False
        self.error_state = None

    def send(self, payload):
        if not self.data:
            return
        self.data.write((json.dumps(payload) + "\n").encode("utf-8"))

    def send_hello(self):
        self.send(
            {
                "type": "hello",
                "version": FIRMWARE_VERSION,
                "capabilities": {
                    "update_protocol": 1,
                    "supports_webserial": True,
                },
            }
        )

    def poll(self):
        if not self.data or not self.data.connected:
            if self.greeted:
                self.reset()
            return
        if not self.greeted:
            self.send_hello()
            self.greeted = True
        if self.error_state:
            return
        if self.binary_remaining:
            self._read_binary()
        else:
            self._read_lines()

    def _read_lines(self):
        if not self.data.in_waiting:
            return
        chunk = self.data.read(min(self.data.in_waiting, 256))
        if not chunk:
            return
        self.line_buffer.extend(chunk)
        while b"\n" in self.line_buffer:
            line, _, rest = self.line_buffer.partition(b"\n")
            self.line_buffer = bytearray(rest)
            line = line.strip()
            if not line:
                continue
            try:
                message = json.loads(line.decode("utf-8"))
            except ValueError:
                self._set_error("invalid_json")
                return
            self._handle_message(message)
            if self.error_state or self.binary_remaining:
                return

    def _read_binary(self):
        if not self.data.in_waiting:
            return
        to_read = min(self.data.in_waiting, self.binary_remaining)
        chunk = self.data.read(to_read)
        if not chunk:
            return
        self.active_file["handle"].write(chunk)
        self.active_file["hash"].update(chunk)
        self.chunk_hash.update(chunk)
        self.binary_remaining -= len(chunk)
        self.active_file["received"] += len(chunk)
        if self.binary_remaining:
            return
        if self.chunk_hash_expected:
            digest = self.chunk_hash.hexdigest()
            if digest != self.chunk_hash_expected:
                self._set_error("chunk_hash_mismatch")
                return
        self.chunk_hash = None
        self.chunk_hash_expected = None
        self.send({"type": "ack", "status": "chunk_ok"})

    def _set_error(self, reason):
        self.error_state = reason
        self.send({"type": "nack", "error": reason})
        self._cleanup_active_file()

    def _cleanup_active_file(self):
        if not self.active_file:
            return
        temp_path = self.active_file.get("temp_path")
        self._close_active_file()
        if temp_path:
            remove_if_exists(temp_path)
        self.active_file = None
        self.binary_remaining = 0

    def _close_active_file(self):
        handle = self.active_file.get("handle")
        if handle:
            handle.close()

    def _handle_message(self, message):
        message_type = message.get("type")
        if message_type == "handshake":
            self.send_hello()
            return
        if message_type == "ping":
            self.send({"type": "pong"})
            return
        if message_type == "manifest":
            self.manifest = message.get("files", [])
            self.send({"type": "ack", "status": "manifest_ok"})
            return
        if message_type == "file_start":
            self._begin_file(message)
            return
        if message_type == "file_chunk":
            self._begin_chunk(message)
            return
        if message_type == "file_end":
            self._finish_file(message)
            return
        if message_type == "commit":
            self._commit_update(message)
            return
        if message_type == "abort":
            self._abort_update()
            return
        self._set_error("unknown_message")

    def _begin_file(self, message):
        if self.active_file:
            self._set_error("file_in_progress")
            return
        path = message.get("path")
        if not is_safe_path(path):
            self._set_error("invalid_path")
            return
        size = int(message.get("size", 0))
        expected_hash = message.get("sha")
        temp_path = f"{path}.tmp"
        ensure_dir(path)
        remove_if_exists(temp_path)
        try:
            handle = open(temp_path, "wb")
        except OSError:
            self._set_error("open_failed")
            return
        self.active_file = {
            "path": path,
            "temp_path": temp_path,
            "size": size,
            "expected_hash": expected_hash,
            "received": 0,
            "hash": hashlib.sha256(),
            "handle": handle,
        }
        self.send({"type": "ack", "status": "file_started", "path": path})

    def _begin_chunk(self, message):
        if not self.active_file:
            self._set_error("no_active_file")
            return
        if self.binary_remaining:
            self._set_error("chunk_in_progress")
            return
        length = int(message.get("length", 0))
        if length <= 0:
            self._set_error("invalid_chunk_length")
            return
        self.chunk_hash_expected = message.get("sha")
        self.chunk_hash = hashlib.sha256()
        self.binary_remaining = length

    def _finish_file(self, message):
        if not self.active_file:
            self._set_error("no_active_file")
            return
        if self.binary_remaining:
            self._set_error("chunk_in_progress")
            return
        size = self.active_file["size"]
        if size and self.active_file["received"] != size:
            self._set_error("size_mismatch")
            return
        if self.active_file["expected_hash"]:
            digest = self.active_file["hash"].hexdigest()
            if digest != self.active_file["expected_hash"]:
                self._set_error("file_hash_mismatch")
                return
        self._close_active_file()
        self.pending_files[self.active_file["path"]] = self.active_file["temp_path"]
        self.active_file = None
        self.send({"type": "ack", "status": "file_ok"})

    def _commit_update(self, message):
        if self.binary_remaining or self.active_file:
            self._set_error("file_in_progress")
            return
        for path, temp_path in self.pending_files.items():
            if not is_safe_path(path):
                self._set_error("invalid_path")
                return
            ensure_dir(path)
            replace_file(temp_path, path)
        bundle_version = message.get("bundle_version")
        self.send({"type": "ack", "status": "commit_ok", "bundle_version": bundle_version})
        time.sleep(0.2)
        supervisor.reload()

    def _abort_update(self):
        if self.active_file:
            self._cleanup_active_file()
        for temp_path in self.pending_files.values():
            remove_if_exists(temp_path)
        self.pending_files = {}
        self.send({"type": "ack", "status": "aborted"})


def is_safe_path(path):
    if not path or path.startswith("/"):
        return False
    for part in path.split("/"):
        if part in ("", ".", ".."):
            return False
    return True


def ensure_dir(path):
    if "/" not in path:
        return
    parts = path.split("/")[:-1]
    current = ""
    for part in parts:
        current = f"{current}/{part}" if current else part
        try:
            os.stat(current)
        except OSError:
            os.mkdir(current)


def remove_if_exists(path):
    try:
        os.remove(path)
    except OSError:
        return


def replace_file(temp_path, path):
    remove_if_exists(path)
    os.rename(temp_path, path)


def base_color_for_index(index):
    return STATIC_KEY_COLORS.get(index, BASE_NOTE_COLOR)


def set_led_scaled(index, red, green, blue):
    keybow.set_led(
        index,
        int(red * BRIGHTNESS_SCALE),
        int(green * BRIGHTNESS_SCALE),
        int(blue * BRIGHTNESS_SCALE),
    )


def oscillating_channel(time_value, phase):
    span = OSCILLATE_MAX - OSCILLATE_MIN
    return OSCILLATE_MIN + int(span * (math.sin(time_value + phase) + 1) / 2)


def note_to_key_index(note):
    return (note - 60) % 12


def current_note_offset():
    return BASE_NOTE_OFFSET + octave_offset


def adjust_octave_offset(step):
    global octave_offset
    octave_offset = max(MIN_OCTAVE_OFFSET, min(MAX_OCTAVE_OFFSET, octave_offset + step))


def send_midi(message):
    if isinstance(message, list):
        for msg in message:
            midi.send(msg)
    else:
        midi.send(message)


def any_note_pressed():
    for index in NOTE_KEY_INDICES:
        if keys[index].pressed:
            return True
    return False


def set_active_chord_notes(notes):
    previous_notes = list(active_chord_notes)
    active_chord_notes.clear()
    for note in notes:
        index = note_to_key_index(note)
        if index not in active_chord_notes:
            active_chord_notes.append(index)
    for index in previous_notes:
        if index not in active_chord_notes:
            set_led_scaled(index, *base_color_for_index(index))


def clear_active_chord_notes():
    for index in active_chord_notes:
        set_led_scaled(index, *base_color_for_index(index))
    active_chord_notes.clear()


def refresh_active_chord_notes():
    notes = []
    for note_list in active_notes.values():
        notes.extend(note_list)
    set_active_chord_notes(notes)


def update_modifier_leds(time_value):
    if alt_mode_active:
        up_color = (
            ALT_ACTIVE_COLOR if keys[OCTAVE_UP_KEY_INDEX].pressed else ALT_INACTIVE_COLOR
        )
        down_color = (
            ALT_ACTIVE_COLOR if keys[OCTAVE_DOWN_KEY_INDEX].pressed else ALT_INACTIVE_COLOR
        )
        exit_color = (
            ALT_ACTIVE_COLOR if keys[ALT_TOGGLE_KEY_INDEX].pressed else ALT_INACTIVE_COLOR
        )
        set_led_scaled(OCTAVE_UP_KEY_INDEX, *up_color)
        set_led_scaled(OCTAVE_DOWN_KEY_INDEX, *down_color)
        set_led_scaled(VELOCITY_KEY_INDEX, *VELOCITY_COLORS[velocity_index])
        set_led_scaled(ALT_TOGGLE_KEY_INDEX, *exit_color)
        return

    for offset, index in enumerate(MODIFIER_KEY_INDICES):
        set_led_scaled(
            index,
            oscillating_channel(time_value, 0.6 + offset),
            oscillating_channel(time_value, 2.7 + offset),
            oscillating_channel(time_value, 4.8 + offset),
        )


def update_note_leds(time_value):
    if active_chord_notes:
        for offset, index in enumerate(active_chord_notes):
            set_led_scaled(
                index,
                oscillating_channel(time_value, 0.0 + offset),
                oscillating_channel(time_value, 2.1 + offset),
                oscillating_channel(time_value, 4.2 + offset),
            )
    update_modifier_leds(time_value)


def roll_chord(messages, delay=0.012):
    for message in messages:
        send_midi(message)
        time.sleep(delay)


def emergency_note_off():
    send_midi([NoteOff(note, 0) for note in EMERGENCY_NOTE_RANGE])
    active_notes.clear()
    clear_active_chord_notes()


def chord_intervals():
    if alt_mode_active:
        return (0,)
    pressed_modifiers = [
        index for index in MODIFIER_KEY_INDICES if keys[index].pressed
    ]
    if len(pressed_modifiers) == 1:
        return CHORD_INTERVALS.get(pressed_modifiers[0], CHORD_INTERVALS["default"])
    return CHORD_INTERVALS["default"]


def handle_note_press(key_index, base_note):
    global last_alt_press_time
    last_alt_press_time = None
    intervals = chord_intervals()
    note_offset = current_note_offset()
    note_numbers = [base_note + note_offset + interval for interval in intervals]
    velocity = VELOCITY_LEVELS[velocity_index]
    if len(note_numbers) == 1:
        send_midi(NoteOn(note_numbers[0], velocity))
    else:
        roll_chord([NoteOn(note, velocity) for note in note_numbers])
    active_notes[key_index] = note_numbers
    refresh_active_chord_notes()


def handle_note_release(key_index):
    note_numbers = active_notes.pop(key_index, None)
    if not note_numbers:
        return
    messages = [NoteOff(note, 0) for note in note_numbers]
    send_midi(messages if len(messages) > 1 else messages[0])
    refresh_active_chord_notes()


def handle_alt_toggle():
    global alt_mode_active, last_alt_press_time
    now = time.monotonic()
    if alt_mode_active:
        alt_mode_active = False
        last_alt_press_time = None
        return
    if last_alt_press_time and now - last_alt_press_time <= ALT_TOGGLE_WINDOW and not any_note_pressed():
        alt_mode_active = True
        last_alt_press_time = None
        emergency_note_off()
        return
    last_alt_press_time = now


def handle_alt_modifier_press(index):
    global velocity_index
    if not alt_mode_active:
        return
    if index == OCTAVE_UP_KEY_INDEX:
        adjust_octave_offset(12)
    elif index == OCTAVE_DOWN_KEY_INDEX:
        adjust_octave_offset(-12)
    elif index == VELOCITY_KEY_INDEX:
        velocity_index = (velocity_index + 1) % len(VELOCITY_LEVELS)


for index in NOTE_KEY_INDICES:
    set_led_scaled(index, *base_color_for_index(index))
for index in MODIFIER_KEY_INDICES:
    set_led_scaled(index, 0, 0, 0)

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
update_session = UpdateSession(usb_cdc.data)

for index, base_note in enumerate(BASE_NOTES):
    key = keys[index]

    @keybow.on_press(key)
    def press_handler(key, index=index, base_note=base_note):
        handle_note_press(index, base_note)

    @keybow.on_release(key)
    def release_handler(key, index=index):
        handle_note_release(index)


for index in MODIFIER_KEY_INDICES:
    key = keys[index]

    @keybow.on_press(key)
    def press_handler(key, index=index):
        if index == ALT_TOGGLE_KEY_INDEX:
            handle_alt_toggle()
            return
        handle_alt_modifier_press(index)

    @keybow.on_release(key)
    def release_handler(key):
        if not alt_mode_active:
            emergency_note_off()


while True:
    keybow.update()
    update_note_leds(time.monotonic() * OSCILLATE_SPEED)
    update_session.poll()
