#!/usr/bin/env python3
"""Render a 1024x1024 newspaper-style world-news poster (PIL, deterministic).
Usage: python3 render_poster.py <date_label> <outfile>   (stories are defined below per date)
Fonts: DejaVu Serif Bold (headlines) + DejaVu Sans (body). No network.
"""
import sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 245, 238)   # off-white paper
INK = (17, 17, 17)        # near-black
RED = (185, 28, 28)       # accent red
GREY = (90, 86, 78)       # muted grey
RULE = (200, 192, 178)    # hairline rule

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, font, max_w):
    """Wrap text to a pixel width; returns list of lines."""
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
    M = 48  # margin
    x0, x1 = M, W - M
    content_w = x1 - x0

    # --- masthead ---
    f_mast = F(SERIF_B, 62)
    d.text((W // 2, 44), "WORLD NEWS", font=f_mast, fill=INK, anchor="ma")
    # red rule under masthead
    d.rectangle([x0, 118, x1, 122], fill=RED)
    f_date = F(SANS_B, 26)
    d.text((W // 2, 138), date_label, font=f_date, fill=INK, anchor="ma")
    d.line([x0, 178, x1, 178], fill=RULE, width=2)

    y = 196
    # --- lead story ---
    f_kick = F(SANS_B, 20)
    d.text((x0, y), "TOP STORY", font=f_kick, fill=RED)
    y += 30
    f_lead = F(SERIF_B, 40)
    for ln in wrap(d, lead["headline"], f_lead, content_w):
        d.text((x0, y), ln, font=f_lead, fill=INK)
        y += 48
    y += 6
    f_sum = F(SANS, 21)
    for ln in wrap(d, lead["summary"], f_sum, content_w):
        d.text((x0, y), ln, font=f_sum, fill=GREY)
        y += 29
    y += 12
    d.line([x0, y, x1, y], fill=RULE, width=2)
    y += 14

    # --- supporting stories ---
    f_skick = F(SANS_B, 18)
    f_shead = F(SERIF_B, 28)
    f_ssum = F(SANS, 19)
    for st in stories:
        d.text((x0, y), st["kicker"], font=f_skick, fill=RED)
        y += 26
        for ln in wrap(d, st["headline"], f_shead, content_w):
            d.text((x0, y), ln, font=f_shead, fill=INK)
            y += 34
        for ln in wrap(d, st["summary"], f_ssum, content_w):
            d.text((x0, y), ln, font=f_ssum, fill=GREY)
            y += 26
        y += 12
        if st is not stories[-1]:
            d.line([x0, y, x1, y], fill=RULE, width=1)
            y += 12

    img.save(outfile, "PNG", optimize=True)
    print(f"wrote {outfile} ({img.size[0]}x{img.size[1]})")

POSTERS = {
    "20261118": {
        "date": "WEDNESDAY  18  NOVEMBER  2026",
        "lead": {
            "headline": "Iran strikes Kuwait and Bahrain after US hits Qeshm Island",
            "summary": "Tehran fires drones at a US air base in Kuwait and targets Bahrain, a day after US aircraft struck a missile site on Qeshm Island. A tanker is hit in the Strait of Hormuz.",
        },
        "stories": [
            {"kicker": "UKRAINE", "headline": "Kerch Bridge partly collapses under Ukrainian attack",
             "summary": "Kyiv hits the bridge to Crimea for a second day; part of the road span falls."},
            {"kicker": "DIPLOMACY", "headline": "Xi and Putin meet in Shenzhen ahead of Trump summit",
             "summary": "The two leaders coordinate before Thursday's three-way talks with the US president at APEC."},
            {"kicker": "US POLITICS", "headline": "Democrats take the Senate as Peltola wins Alaska",
             "summary": "Mary Peltola beats Dan Sullivan; Democrats now hold a 56-44 majority."},
            {"kicker": "ISRAEL", "headline": "Knesset elects Matan Kahana as speaker",
             "summary": "A win for PM-elect Eisenkot's Yashar party over Netanyahu's Likud."},
            {"kicker": "HEALTH", "headline": "Ebola in DR Congo passes 11,000 cases",
             "summary": "Three in four infected children under five do not survive; the US loses measles-free status."},
        ],
    },
    "20261119": {
        "date": "THURSDAY  19  NOVEMBER  2026",
        "lead": {
            "headline": "Trump, Xi and Putin meet in Shenzhen for first three-way summit",
            "summary": "Nuclear arms, Ukraine and the Iran conflict on the agenda at APEC; no breakthrough expected as the three leaders sit down together.",
        },
        "stories": [
            {"kicker": "THE GULF", "headline": "Iran and US trade strikes across the Gulf",
             "summary": "Iran fires at a US base in Kuwait; the US hits a Guard missile site on Qeshm; a tanker is struck in Hormuz."},
            {"kicker": "CULTURE", "headline": "GTA VI begins global rollout as gamers enter Vice City",
             "summary": "Grand Theft Auto VI launches worldwide, the biggest entertainment release of the year."},
            {"kicker": "UKRAINE", "headline": "Crimean Bridge hit for a third time this week",
             "summary": "Traffic closed as damage is assessed; drone attacks continue amid Abu Dhabi peace talks."},
            {"kicker": "AFRICA", "headline": "Ethiopia and Eritrea mass troops on the border",
             "summary": "Forces gather within striking distance; unconfirmed clashes reported near Badme."},
            {"kicker": "SOUTH ASIA", "headline": "Bangladesh garment workers protest for a third week",
             "summary": "Police use tear gas as dozens of factories shut; workers want a 30,000-taka minimum wage."},
        ],
    },
}

if __name__ == "__main__":
    key = sys.argv[1]
    out = sys.argv[2]
    p = POSTERS[key]
    draw_poster(p["date"], p["lead"], p["stories"], out)
