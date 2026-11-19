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

POSTER_NAME = "poster-20261119.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
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
