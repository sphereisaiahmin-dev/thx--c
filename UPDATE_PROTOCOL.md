# WebUSB/WebSerial Update Protocol

This document describes the update protocol used by `code.py` over the USB CDC data
channel (WebSerial) and, when supported by the CircuitPython build, WebUSB. The
protocol uses newline-delimited JSON control messages with optional binary chunks
for file data.

## Transport

- **Primary transport:** USB CDC data channel (`usb_cdc.data`). This is compatible
  with WebSerial in modern browsers.
- **Optional transport:** WebUSB (if the CircuitPython build exposes the `webusb`
  module). If the module is missing, WebUSB is unavailable and updates must use
  USB CDC/WebSerial.

## Device handshake

When a host connects to the data channel, the device sends:

```json
{"type":"hello","version":"<firmware-version>","capabilities":{"update_protocol":1,"supports_webserial":true}}
```

The host may also send `{ "type": "handshake" }` to request the hello message.

## Control framing

- **Control messages:** UTF-8 JSON, newline (`\n`) delimited.
- **Binary data:** Sent immediately after a `file_chunk` message, with a fixed byte
  length specified by the `length` field.

## Typical update flow

1. **Manifest** (optional but recommended):

   ```json
   {"type":"manifest","files":[{"path":"code.py","size":1234,"sha":"..."}]}
   ```

   Device replies: `{ "type": "ack", "status": "manifest_ok" }`

2. **File transfer** (per file):

   ```json
   {"type":"file_start","path":"code.py","size":1234,"sha":"..."}
   {"type":"file_chunk","length":512,"sha":"..."}
   <512 raw bytes>
   {"type":"file_chunk","length":512,"sha":"..."}
   <512 raw bytes>
   {"type":"file_end"}
   ```

   The device replies with `{ "type": "ack", "status": "file_started" }`,
   `{ "type": "ack", "status": "chunk_ok" }`, and `{ "type": "ack", "status": "file_ok" }`.

3. **Commit**

   ```json
   {"type":"commit","bundle_version":"<version>"}
   ```

   Device replies: `{ "type": "ack", "status": "commit_ok", "bundle_version":"<version>" }`
   and reboots to apply updates.

4. **Abort** (optional):

   ```json
   {"type":"abort"}
   ```

   Device replies: `{ "type": "ack", "status": "aborted" }`

## Safety guarantees

- Files are written to `*.tmp` paths first, validated with SHA-256, and then
  atomically renamed into place.
- If a file fails checksum verification, the update session aborts and the
  existing firmware remains intact.
- An update cannot commit while another file transfer is in progress.

## Error responses

The device replies with `{ "type": "nack", "error": "<reason>" }` when an error
occurs (e.g., `invalid_path`, `file_hash_mismatch`, `chunk_hash_mismatch`).

## Recommended bundle contents

- `code.py`
- `config.json`
- `firmware.version`
- Any additional library files required by the firmware

