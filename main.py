"""Entry point for the news-image-20261119 bounty.

The poster itself is a finished artifact built by render_poster.py. This
program only puts a verbatim copy of it where the bounty harness looks
for the entry image, so the harness can score the poster as submitted.
It does no drawing, no fetching and no guessing: it finds the poster
beside this file, makes the output folder if needed, copies the file,
and reports the copy it made.
"""

import os
import shutil
import sys

POSTER_FILE = "poster-20261119.png"
DEFAULT_OUTDIR = "/output"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, POSTER_FILE)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTDIR)
    target = os.path.join(outdir, "entry.png")
    try:
        os.makedirs(outdir, exist_ok=True)
        if not os.path.isfile(source):
            raise FileNotFoundError(source)
        shutil.copyfile(source, target)
    except FileNotFoundError:
        print("poster not found: " + source, file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print("could not write entry: " + str(exc), file=sys.stderr)
        sys.exit(1)
    source_size = os.path.getsize(source)
    size = os.path.getsize(target)
    if size != source_size:
        print("copy incomplete: " + target, file=sys.stderr)
        sys.exit(1)
    print("copied " + POSTER_FILE + " -> " + target + " (" + str(size) + " bytes)")


if __name__ == "__main__":
    main()
