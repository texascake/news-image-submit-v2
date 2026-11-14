"""news-image-01 entry v2: reproduce the bundled news image as the output.

The image beside this program (entry.png) is an editorial infographic
summing up the world news of Friday 13 November 2026 in 26 stories:
an asymmetric front page with three large illustrated panels on the
left (the FAA grounding all US departures, the US downing two Iranian
drones, the Trump-Xi-Putin summit), eight more illustrated stories in
a list on the right, and fifteen one-line stories in a band along the
bottom, with the day's sources credited underneath. The file holds
JPEG bytes under a .png name, which the competition allows.

Running this program writes those exact bytes to /output/entry.png (or
to $MAKEFUN_OUTPUT_DIR when that is set). The run is deterministic:
the output is always an exact copy of the source, so two runs agree
byte for byte. Before writing, the source is checked against the
competition limits (at most 1 MiB); after writing, the output is read
back and compared with the source, bytes and size.

Python 3.13, standard library only. No network access.
"""

import hashlib
import os
import shutil
import struct
from pathlib import Path

BYTE_LIMIT = 1_048_576
PIXEL_LIMIT = 1024

SOURCE = Path(__file__).resolve().parent / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT_FILE = OUT_DIR / "entry.png"


def _dimensions(data: bytes) -> tuple[int, int]:
    """Read width/height from a PNG IHDR or a JPEG SOF marker; (0, 0) if unknown."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                break
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                height, width = struct.unpack(">HH", data[i + 5:i + 9])
                return width, height
            length = struct.unpack(">H", data[i + 2:i + 4])[0]
            i += 2 + length
    return 0, 0


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"entry image missing: {SOURCE}")
    data = SOURCE.read_bytes()
    if len(data) > BYTE_LIMIT:
        raise SystemExit(f"entry image too large: {len(data)} bytes")
    width, height = _dimensions(data)
    if width > PIXEL_LIMIT or height > PIXEL_LIMIT:
        raise SystemExit(f"entry image too big: {width}x{height}")
    print(f"source sha256: {hashlib.sha256(data).hexdigest()}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUT_FILE)
    written = OUT_FILE.read_bytes()
    if written != data:
        raise SystemExit("copy verification failed: output differs from source")
    out_width, out_height = _dimensions(written)
    if (out_width, out_height) != (width, height):
        raise SystemExit("copy verification failed: output dimensions differ")
    print(f"wrote {OUT_FILE} ({len(written)} bytes, {width}x{height})")


if __name__ == "__main__":
    main()
