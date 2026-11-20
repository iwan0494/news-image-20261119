# main.py — entry point bounty news-image-20261119 (ronde 3).
# Me-render poster dari nol setiap kali dijalankan (bukan menyalin PNG),
# lalu menulisnya ke /output/entry.png (atau --out).
# Python 3.13, stdlib + PIL saja. Tanpa network, tanpa randomness.

import argparse
import hashlib
import os
import sys
from pathlib import Path

from poster import build_poster

MAX_BYTES = 1_048_576


def build():
    parser = argparse.ArgumentParser(description="Render poster berita 19 November 2026.")
    parser.add_argument("--out", default=None, help="path file PNG output (default: $MAKEFUN_OUTPUT_DIR/entry.png)")
    args = parser.parse_args()

    if args.out:
        target = Path(args.out)
    else:
        out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
        target = out_dir / "entry.png"

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"main.py: cannot create output dir {target.parent}: {exc}", file=sys.stderr)
        sys.exit(1)

    image = build_poster()
    image.save(target, format="PNG")

    if not target.exists():
        print(f"main.py: output missing after render: {target}", file=sys.stderr)
        sys.exit(1)
    size = target.stat().st_size
    if size > MAX_BYTES:
        print(f"main.py: output too large: {size} bytes > {MAX_BYTES}", file=sys.stderr)
        sys.exit(1)

    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"main.py: OK — wrote {target} ({size} bytes, sha256 {digest})")


if __name__ == "__main__":
    build()
