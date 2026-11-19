#!/usr/bin/env python3
"""Render a 1024x1024 world-news poster (PIL, deterministic) — distinctive editorial design.
Design (frontend-design skill, two-pass): NOT a generic broadsheet. A solid black masthead
bar (white sans type), one red accent used sparingly, a single dominant serif lead headline,
and the supporting stories in a clean two-column grid separated by whitespace — no hairline
rules everywhere, no ALL-CAPS labels, no warm-cream paper. One bold element (the black bar
+ huge lead headline); everything else quiet and disciplined.
Usage: python3 render_poster.py <date_key> <outfile>   (stories defined below per date)
Fonts: DejaVu Serif Bold (lead headline only) + DejaVu Sans (everything else). No network.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (255, 255, 255)   # pure white, not warm cream
INK = (14, 27, 44)        # deep ink navy, not near-black grey
RED = (217, 43, 43)       # single signal-red accent, used sparingly
SLATE = (90, 100, 112)    # muted slate for summaries
FAINT = (226, 230, 235)   # faint vertical divider

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_poster(date_label, lead, stories, outfile):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 48
    x0, x1 = M, W - M
    cw = x1 - x0

    # --- masthead: solid black bar, white sans type (the bold element) ---
    d.rectangle([0, 0, W, 96], fill=(10, 10, 10))
    f_mast = F(SANS_B, 42)
    d.text((x0, 48), "WORLD NEWS", font=f_mast, fill=(255, 255, 255), anchor="lm")
    f_date = F(SANS, 22)
    d.text((x1, 48), date_label, font=f_date, fill=(210, 210, 210), anchor="rm")
    # thin red accent bar under the masthead
    d.rectangle([0, 96, W, 102], fill=RED)

    y = 132
    # --- lead story: red tag (sentence case) + huge serif headline ---
    f_tag = F(SANS_B, 18)
    tag = "Top story"
    tw = d.textlength(tag, font=f_tag)
    d.rectangle([x0, y, x0 + tw + 24, y + 32], fill=RED)
    d.text((x0 + 12, y + 16), tag, font=f_tag, fill=(255, 255, 255), anchor="lm")
    y += 48
    f_lead = F(SERIF_B, 50)
    for ln in wrap(d, lead["headline"], f_lead, cw):
        d.text((x0, y), ln, font=f_lead, fill=INK)
        y += 60
    y += 8
    f_sum = F(SANS, 21)
    for ln in wrap(d, lead["summary"], f_sum, cw):
        d.text((x0, y), ln, font=f_sum, fill=SLATE)
        y += 29
    y += 18
    # one thick ink rule under the lead (a single strong divider, not hairlines)
    d.rectangle([x0, y, x1, y + 4], fill=INK)
    y += 28

    # --- supporting stories: two-column grid, whitespace separates ---
    gap = 32
    col_w = (cw - gap) // 2
    col_x = [x0, x0 + col_w + gap]
    # no vertical divider: the column gap + whitespace is the separator
    # (a rule would hang into empty space below the shorter column)
    f_head = F(SANS_B, 23)
    f_ssum = F(SANS, 18)
    f_kick = F(SANS_B, 16)
    left = stories[:3]
    right = stories[3:]
    for col, lst in enumerate([left, right]):
        cy = y
        for st in lst:
            # small red square marker + topic in sentence case (no ALL-CAPS)
            d.rectangle([col_x[col], cy + 4, col_x[col] + 10, cy + 14], fill=RED)
            d.text((col_x[col] + 20, cy), st["kicker"], font=f_kick, fill=RED)
            cy += 26
            for ln in wrap(d, st["headline"], f_head, col_w):
                d.text((col_x[col], cy), ln, font=f_head, fill=INK)
                cy += 29
            for ln in wrap(d, st["summary"], f_ssum, col_w):
                d.text((col_x[col], cy), ln, font=f_ssum, fill=SLATE)
                cy += 24
            cy += 26

    img.save(outfile, "PNG", optimize=True)
    print(f"wrote {outfile} ({img.size[0]}x{img.size[1]})")

POSTERS = {
    "20261118": {
        "date": "Wednesday 18 November 2026",
        "lead": {
            "headline": "Iran strikes Kuwait and Bahrain after US hits Qeshm Island",
            "summary": "Tehran fires drones at a US air base in Kuwait and targets Bahrain, a day after US aircraft struck a missile site on Qeshm Island. A tanker is hit in the Strait of Hormuz.",
        },
        "stories": [
            {"kicker": "Ukraine", "headline": "Kerch Bridge partly collapses under Ukrainian attack",
             "summary": "Kyiv hits the bridge to Crimea for a second day; part of the road span falls."},
            {"kicker": "Diplomacy", "headline": "Xi and Putin meet in Shenzhen ahead of Trump summit",
             "summary": "The two leaders coordinate before Thursday's three-way talks with the US president at APEC."},
            {"kicker": "US politics", "headline": "Democrats take the Senate as Peltola wins Alaska",
             "summary": "Mary Peltola beats Dan Sullivan; Democrats now hold a 56-44 majority."},
            {"kicker": "Israel", "headline": "Knesset elects Matan Kahana as speaker",
             "summary": "A win for PM-elect Eisenkot's Yashar party over Netanyahu's Likud."},
            {"kicker": "Health", "headline": "Ebola in DR Congo passes 11,000 cases",
             "summary": "Three in four infected children under five do not survive; the US loses measles-free status."},
        ],
    },
    "20261119": {
        "date": "Thursday 19 November 2026",
        "lead": {
            "headline": "Trump, Xi and Putin meet in Shenzhen for first three-way summit",
            "summary": "Nuclear arms, Ukraine and the Iran conflict on the agenda at APEC; no breakthrough expected as the three leaders sit down together.",
        },
        "stories": [
            {"kicker": "The Gulf", "headline": "Iran and US trade strikes across the Gulf",
             "summary": "Iran fires at a US base in Kuwait; the US hits a Guard missile site on Qeshm; a tanker is struck in Hormuz."},
            {"kicker": "Culture", "headline": "GTA VI begins global rollout as gamers enter Vice City",
             "summary": "Grand Theft Auto VI launches worldwide, the biggest entertainment release of the year."},
            {"kicker": "Ukraine", "headline": "Crimean Bridge hit for a third time this week",
             "summary": "Traffic closed as damage is assessed; drone attacks continue amid Abu Dhabi peace talks."},
            {"kicker": "Africa", "headline": "Ethiopia and Eritrea mass troops on the border",
             "summary": "Forces gather within striking distance; unconfirmed clashes reported near Badme."},
            {"kicker": "South Asia", "headline": "Bangladesh garment workers protest for a third week",
             "summary": "Police use tear gas as dozens of factories shut; workers want a 30,000-taka minimum wage."},
        ],
    },
}

if __name__ == "__main__":
    key = sys.argv[1]
    out = sys.argv[2]
    p = POSTERS[key]
    draw_poster(p["date"], p["lead"], p["stories"], out)
