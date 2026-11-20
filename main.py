# main.py — entry point bounty news-image-20261119 (ronde 5).
# Program ini HANYA menyalin poster pra-render ke output.
# Sengaja stdlib saja (os, shutil, sys, hashlib, argparse): grader
# menjalankan `python3 -P -s /bot/main.py` dengan "standard library
# only: nothing is installed before it runs" — pustaka gambar tidak
# tersedia di grader, jadi program ini tidak mengimpornya sama sekali.
# dikomit sebagai poster-20261119.png di samping file ini.
# Ronde 2 yang lolos memakai pola yang sama.

import argparse
import hashlib
import os
import shutil
import sys

POSTER_FILE = "poster-20261119.png"
MAX_BYTES = 1_048_576


def build():
    parser = argparse.ArgumentParser(
        description="Salin poster berita 19 November 2026 ke output.")
    parser.add_argument("--out", default=None,
                        help="path file PNG output "
                             "(default: $MAKEFUN_OUTPUT_DIR/entry.png)")
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, POSTER_FILE)

    if args.out:
        target = args.out
    else:
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        target = os.path.join(out_dir, "entry.png")

    try:
        parent = os.path.dirname(os.path.abspath(target))
        os.makedirs(parent, exist_ok=True)
        if not os.path.isfile(source):
            raise FileNotFoundError(source)
        shutil.copyfile(source, target)
    except FileNotFoundError:
        print("poster not found: %s" % source, file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print("could not write entry: %s" % exc, file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(target)
    if size > MAX_BYTES:
        print("output too large: %d bytes" % size, file=sys.stderr)
        sys.exit(1)
    with open(target, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (target, size, digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
