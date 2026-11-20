# main.py — entry point bounty news-image-20261119 (ronde 4).
# Me-render poster dari nol setiap kali dijalankan (bukan menyalin PNG),
# lalu menulisnya ke /output/entry.png (atau --out).
# Python 3.13, stdlib + PIL saja. Tanpa network, tanpa randomness.

# --- BOOTSTRAP sys.path (WAJIB, inti fix ronde 4) ---
# Grader menjalankan `python3 -P -s /bot/main.py`. Flag -P membuat Python
# TIDAK menambahkan direktori script ke sys.path, sehingga `from poster
# import ...` gagal dengan ModuleNotFoundError. Sisipkan direktori file
# ini ke depan sys.path SEBELUM impor modul saudara.
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
# --- akhir bootstrap ---

import argparse
import hashlib

from poster import build_poster

MAX_BYTES = 1_048_576


def build():
    parser = argparse.ArgumentParser(
        description="Render poster berita 19 November 2026.")
    parser.add_argument("--out", default=None,
                        help="path file PNG output "
                             "(default: $MAKEFUN_OUTPUT_DIR/entry.png)")
    args = parser.parse_args()

    if args.out:
        target = Path(args.out)
    else:
        out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
        target = out_dir / "entry.png"

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print("cannot create output dir: %s" % exc, file=sys.stderr)
        sys.exit(1)

    img = build_poster()
    img.save(target, format="PNG")

    if not target.is_file():
        print("output missing: %s" % target, file=sys.stderr)
        sys.exit(1)
    size = target.stat().st_size
    if size > MAX_BYTES:
        print("output too large: %d bytes" % size, file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (target, size, digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
