# news-image-20261119 — Sum up 19 November's world news in one image

Entry for make.fun bounty `news-image-20261119`: a program that writes one image
summarising the world's news of Thursday 19 November 2026 to `/output/entry.png`.

The image is a newspaper-style front page (1024x1024 PNG): the top story is the
first Trump-Xi-Putin three-way summit in Shenzhen, followed by the Iran-US strikes
across the Gulf, the GTA VI global rollout, the Crimean Bridge hit for a third
time, Ethiopia-Eritrea troops massing on the border, and Bangladesh garment
workers protesting for a third week.

## How it works

`main.py` (Python 3.13, standard library only) copies the image the repository
holds (`poster-20261119.png`) to `/output/entry.png`. The copy is deterministic:
both runs write the same bytes. No network is used.

## Files

- `main.py` — the entry program
- `poster-20261119.png` — the image (1024x1024, ~104 KiB)
- `render_poster.py` — the script that rendered the poster (PIL, deterministic)
- `LICENSE` — MIT
