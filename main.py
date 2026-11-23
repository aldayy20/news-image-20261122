#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261122.

Writes one image summing up world news of Sunday 22 November 2026 to
``<output>/entry.png``. The image is the entry.png beside this file,
drawn by render.py (Pillow, run at build time); this program only copies
it, so it needs nothing but the Python standard library, makes no network
calls, and writes byte-identical output on every run.

Run it like the grader does (Python 3.13, no network):
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
Without MAKEFUN_OUTPUT_DIR it writes to /output/entry.png.
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576  # gate: at most 1 MiB
MAX_SIDE = 1_024  # gate: at most 1024 by 1024 pixels
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_size(data: bytes) -> tuple:
    """Width and height from the IHDR chunk (bytes 16..24 of a PNG)."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("not a PNG with an IHDR chunk")
    return struct.unpack(">II", data[16:24])


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    if not SOURCE.is_file():
        print(f"missing image: {SOURCE}", file=sys.stderr)
        return 1
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        print(f"image too large: {len(data)} bytes", file=sys.stderr)
        return 1
    if not data.startswith(PNG_MAGIC):
        print("image is not a PNG", file=sys.stderr)
        return 1
    try:
        width, height = png_size(data)
    except ValueError as exc:
        print(f"image is not a valid PNG: {exc}", file=sys.stderr)
        return 1
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"image too large: {width}x{height}", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({width}x{height}, {len(data)} bytes, "
          f"sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
