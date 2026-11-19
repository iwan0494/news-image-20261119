# news-image-20261119 — main.py entry program

Date: 2026-11-19
Repo: https://github.com/iwan0494/news-image-20261119
Commit: 5541b56

## What main.py does

Copies the poster PNG held in the repository (poster-20261119.png, 1024x1024) to
`/output/entry.png` byte-for-byte. Standard library only (`os`, `shutil`,
`sys`, `pathlib`). No network access, no randomness, no timestamps, so both
bounty runs produce identical bytes.

```python
#!/usr/bin/env python3
"""Bounty entry program: copy the repository poster to /output/entry.png.

Standard library only. No network, no randomness, no timestamps.
Deterministic by construction: the poster bytes are held in the repo and
copied verbatim on every run.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

POSTER_NAME = "poster-20261118.png"
OUTPUT_DIR = Path("/output")
OUTPUT_PATH = OUTPUT_DIR / "entry.png"


def locate_poster() -> Path:
    """Return the path of the poster PNG that sits next to this file."""
    here = Path(__file__).resolve().parent
    poster = here / POSTER_NAME
    if not poster.is_file():
        sys.exit(f"error: poster not found at {poster}")
    return poster


def main() -> None:
    poster = locate_poster()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(poster, OUTPUT_PATH)
    size = OUTPUT_PATH.stat().st_size
    print(f"wrote {OUTPUT_PATH} from {poster.name} ({size} bytes)")


if __name__ == "__main__":
    main()
```

## Verification (run twice, done locally)

- Run 1 sha256: `4ff15f792719e70422f03ac715645223f4c8c313aac1b8d41e5d8e8dcf0a332f`
- Run 2 sha256: `4ff15f792719e70422f03ac715645223f4c8c313aac1b8d41e5d8e8dcf0a332f`
- Identical: YES (`cmp` on the two output files: no difference)
- Output size: 106187 bytes (103.7 KiB) — under the 1 MiB (1048576 B) limit
- Output dimensions: 1024 x 1024 (read from the PNG IHDR header)
- Format: PNG
- Poster/render_poster.py/README/LICENSE left untouched; only `main.py` added
