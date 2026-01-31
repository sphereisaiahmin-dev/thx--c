#!/usr/bin/env python3
"""Build a single-file updater that flashes CircuitPython files via mpremote."""
from __future__ import annotations

import base64
import io
from pathlib import Path
import textwrap
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
OUTPUT_FILE = DIST_DIR / "thx_update.py"

TEMPLATE = '''#!/usr/bin/env python3
"""Single-click updater for the THX CircuitPython firmware."""
from __future__ import annotations

import base64
import io
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import zipfile

PAYLOAD_B64 = """{{PAYLOAD}}"""


def extract_payload(temp_dir: Path) -> None:
    payload = base64.b64decode(PAYLOAD_B64.encode("utf-8"))
    with zipfile.ZipFile(io.BytesIO(payload), "r") as archive:
        archive.extractall(temp_dir)


def list_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for base, _dirs, filenames in os.walk(root):
        for filename in filenames:
            files.append(Path(base) / filename)
    return sorted(files)


def run_mpremote(args: list[str]) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, "-m", "mpremote", "connect", "auto"] + args
    return subprocess.run(cmd, capture_output=True, text=True)


def ensure_mpremote() -> bool:
    if importlib.util.find_spec("mpremote") is not None:
        return True

    root = tk.Tk()
    root.withdraw()
    should_install = messagebox.askyesno(
        "Install updater helper",
        "This updater needs a small helper (mpremote) to talk to the device.\n"
        "Click Yes to install it automatically.",
    )
    if not should_install:
        root.destroy()
        return False

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", "mpremote"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        messagebox.showerror(
            "Install failed",
            result.stderr.strip() or result.stdout.strip() or "pip install failed.",
        )
        root.destroy()
        return False

    root.destroy()
    return importlib.util.find_spec("mpremote") is not None


def ensure_remote_dirs(files: list[Path], root: Path) -> list[str]:
    dirs: set[str] = set()
    for file_path in files:
        rel_parent = file_path.relative_to(root).parent
        if rel_parent == Path("."):
            continue
        dirs.add(rel_parent.as_posix())
    ordered = sorted(dirs)
    for remote_dir in ordered:
        run_mpremote(["fs", "mkdir", remote_dir])
    return ordered


def copy_files(files: list[Path], root: Path, progress_cb, status_cb) -> None:
    total = len(files)
    for index, file_path in enumerate(files, start=1):
        rel_path = file_path.relative_to(root)
        status_cb(f"Uploading {rel_path.as_posix()} ({index}/{total})")
        result = run_mpremote([
            "fs",
            "cp",
            str(file_path),
            f":{rel_path.as_posix()}",
        ])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
        progress_cb(index)


def build_gui() -> tuple[tk.Tk, ttk.Progressbar, tk.StringVar, ttk.Button]:
    root = tk.Tk()
    root.title("THX Firmware Updater")
    root.geometry("460x200")
    root.resizable(False, False)

    title = ttk.Label(root, text="THX Firmware Updater", font=("TkDefaultFont", 14, "bold"))
    title.pack(pady=(16, 4))

    status_var = tk.StringVar(value="Ready to update your device.")
    status = ttk.Label(root, textvariable=status_var)
    status.pack(pady=(0, 12))

    progress = ttk.Progressbar(root, length=380, mode="determinate")
    progress.pack(pady=(0, 12))

    button = ttk.Button(root, text="Update Device")
    button.pack()

    return root, progress, status_var, button


def main() -> int:
    if not ensure_mpremote():
        return 1

    root, progress, status_var, button = build_gui()

    def set_status(message: str) -> None:
        root.after(0, status_var.set, message)

    def set_progress(value: int) -> None:
        root.after(0, progress.configure, {"value": value})

    def perform_update() -> None:
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                temp_path = Path(tmp_dir)
                extract_payload(temp_path)
                files = list_files(temp_path)
                root.after(0, progress.configure, {"maximum": len(files), "value": 0})
                set_status("Preparing device...")
                ensure_remote_dirs(files, temp_path)
                copy_files(files, temp_path, set_progress, set_status)
            set_status("Update complete! You can unplug the device.")
            root.after(0, messagebox.showinfo, "Update complete", "Firmware update finished successfully.")
        except Exception as exc:  # noqa: BLE001
            set_status("Update failed. See details in the dialog.")
            root.after(0, messagebox.showerror, "Update failed", str(exc))
        finally:
            root.after(0, button.configure, {"state": "normal"})

    def on_click() -> None:
        button.configure(state="disabled")
        set_status("Connecting to device...")
        threading.Thread(target=perform_update, daemon=True).start()

    button.configure(command=on_click, text="Update Again")
    root.after(200, on_click)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def build_payload() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for relative in ["code.py", "boot.py", "settings.toml"]:
            path = ROOT / relative
            if path.exists():
                archive.write(path, arcname=relative)
        lib_dir = ROOT / "lib"
        for file_path in lib_dir.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, arcname=str(file_path.relative_to(ROOT)))
    return buffer.getvalue()


def main() -> int:
    DIST_DIR.mkdir(exist_ok=True)
    payload = base64.b64encode(build_payload()).decode("utf-8")
    wrapped_payload = "\n".join(textwrap.wrap(payload, width=88))
    OUTPUT_FILE.write_text(TEMPLATE.replace("{{PAYLOAD}}", wrapped_payload))
    OUTPUT_FILE.chmod(0o755)
    print(f"Wrote updater to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
