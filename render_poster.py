"""Render the world-news poster for 19 November 2026.

A warm broadsheet: cream paper, a centred navy serif masthead under a
double navy-and-gold rule, a full-width lead, then five stories in a
three-column grid split by hairline rules, with a centred footer.
Deterministic: the same input always produces the same PNG bytes.
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 40
GAP = 28

CREAM = (252, 247, 235)
NAVY = (23, 48, 88)
GOLD = (176, 141, 60)
INK = (20, 20, 20)
SLATE = (90, 100, 112)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

DATE_LABEL = "Thursday 19 November 2026"

LEAD = (
    "Trump, Xi and Putin meet in Shenzhen for first three-way summit",
    "Nuclear arms, Ukraine and the Iran conflict on the agenda at APEC; no breakthrough expected as the three leaders sit down together.",
)

STORIES = [
    (
        "The Gulf",
        "Iran and US trade strikes across the Gulf",
        "Iran fires at a US base in Kuwait; the US hits a Guard missile site on Qeshm; a tanker is struck in Hormuz.",
    ),
    (
        "Culture",
        "GTA VI begins global rollout as gamers enter Vice City",
        "Grand Theft Auto VI launches worldwide, the biggest entertainment release of the year.",
    ),
    (
        "Ukraine",
        "Crimean Bridge hit for a third time this week",
        "Traffic closed as damage is assessed; drone attacks continue amid Abu Dhabi peace talks.",
    ),
    (
        "Africa",
        "Ethiopia and Eritrea mass troops on the border",
        "Forces gather within striking distance; unconfirmed clashes reported near Badme.",
    ),
    (
        "South Asia",
        "Bangladesh garment workers protest for a third week",
        "Police use tear gas as dozens of factories shut; workers want a 30,000-taka minimum wage.",
    ),
]

_fonts = {}


def font_for(path, size):
    key = (path, size)
    got = _fonts.get(key)
    if got is None:
        got = ImageFont.truetype(path, size)
        _fonts[key] = got
    return got


def line_height(font, extra=0):
    up, down = font.getmetrics()
    return up + down + extra


def wrap_lines(draw, text, font, max_w):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_masthead(d, date_label):
    title_font = font_for(SERIF_B, 64)
    date_font = font_for(SANS, 20)
    top = 28
    d.text((W // 2, top), "WORLD NEWS", font=title_font, fill=NAVY, anchor="mt")
    title_bottom = top + line_height(title_font)
    date_top = title_bottom + 6
    d.text((W // 2, date_top), date_label, font=date_font, fill=SLATE, anchor="mt")
    date_bottom = date_top + line_height(date_font)
    rule_top = date_bottom + 14
    d.rectangle([MARGIN, rule_top, W - MARGIN, rule_top + 2], fill=NAVY)
    gold_y = rule_top + 3 + 4
    d.rectangle([MARGIN, gold_y, W - MARGIN, gold_y], fill=GOLD)
    return gold_y + 1 + 22


def draw_lead(d, y, lead):
    headline, deck = lead
    head_font = font_for(SERIF_B, 44)
    deck_font = font_for(SANS, 20)
    content_w = W - 2 * MARGIN
    d.rectangle([MARGIN, y, W - MARGIN, y + 1], fill=GOLD)
    head_top = y + 2 + 16
    lines = wrap_lines(d, headline, head_font, content_w)
    lh = line_height(head_font, 8)
    for line in lines:
        d.text((MARGIN, head_top), line, font=head_font, fill=NAVY)
        head_top += lh
    deck_top = head_top + 14
    deck_lines = wrap_lines(d, deck, deck_font, content_w)
    dlh = line_height(deck_font, 8)
    for line in deck_lines:
        d.text((MARGIN, deck_top), line, font=deck_font, fill=SLATE)
        deck_top += dlh
    return deck_top + 36


def draw_story(d, x, y, width, story):
    kicker, headline, summary = story
    kick_font = font_for(SANS_B, 14)
    head_font = font_for(SERIF_B, 20)
    sum_font = font_for(SANS, 16)
    d.text((x, y), kicker.upper(), font=kick_font, fill=NAVY)
    cur = y + line_height(kick_font) + 7
    d.rectangle([x, cur, x + 27, cur + 2], fill=GOLD)
    cur += 3 + 10
    lines = wrap_lines(d, headline, head_font, width)
    lh = line_height(head_font, 5)
    for line in lines:
        d.text((x, cur), line, font=head_font, fill=INK)
        cur += lh
    cur += 6
    slines = wrap_lines(d, summary, sum_font, width)
    slh = line_height(sum_font, 5)
    for line in slines:
        d.text((x, cur), line, font=sum_font, fill=SLATE)
        cur += slh
    return cur


def draw_footer(d, y, date_label):
    foot_font = font_for(SANS, 14)
    d.rectangle([MARGIN, y, W - MARGIN, y], fill=NAVY)
    text_top = y + 1 + 12
    d.text((W // 2, text_top), date_label + " — World News", font=foot_font, fill=SLATE, anchor="mt")
    return text_top + line_height(foot_font)


def render(date_label, lead, stories, outfile):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d, date_label)
    y = draw_lead(d, y, lead)
    grid_top = y
    col_w = (W - 2 * MARGIN - 2 * GAP) // 3
    columns = [[0, 1], [2, 3], [4]]
    bottoms = []
    for ci, idxs in enumerate(columns):
        x = MARGIN + ci * (col_w + GAP)
        cy = grid_top
        for pos, si in enumerate(idxs):
            if pos > 0:
                cy += 48
            cy = draw_story(d, x, cy, col_w, stories[si])
        bottoms.append(cy)
    grid_bottom = max(bottoms)
    for dx in (MARGIN + col_w + GAP // 2, MARGIN + 2 * col_w + GAP + GAP // 2):
        d.rectangle([dx, grid_top, dx, grid_bottom], fill=NAVY)
    draw_footer(d, grid_bottom + 48, date_label)
    img.save(outfile, optimize=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 render_poster.py <outfile>", file=sys.stderr)
        sys.exit(2)
    render(DATE_LABEL, LEAD, STORIES, sys.argv[1])
