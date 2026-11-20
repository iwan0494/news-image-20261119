# poster.py — mesin layout poster R3 "The World in One Day".
# Menggambar poster 1024x1024 dari nol dengan primitif PIL saja:
# tanpa file gambar eksternal, tanpa network, tanpa randomness.

import os
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

from stories import (
    ATTRIBUTION,
    BRIEFS,
    FEATURES,
    LEFT_OUT,
    REGIONS,
    STATS,
    TILES,
)

CANVAS_W = 1024
CANVAS_H = 1024
MARGIN = 24

_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/local/share/fonts",
    os.path.expanduser("~/.fonts"),
]

_FONT_FILES = {
    "serif": ["DejaVuSerif.ttf", "DejaVuSerifCondensed.ttf"],
    "serif_bold": ["DejaVuSerif-Bold.ttf", "DejaVuSerifCondensed-Bold.ttf"],
    "sans": ["DejaVuSans.ttf", "DejaVuSansCondensed.ttf"],
    "sans_bold": ["DejaVuSans-Bold.ttf", "DejaVuSansCondensed-Bold.ttf"],
}

_cache = {}


def load_font(role, size):
    """Muat font DejaVu dari path sistem yang umum; fallback ke default."""
    key = (role, size)
    if key in _cache:
        return _cache[key]
    font = None
    for name in _FONT_FILES.get(role, []):
        for folder in _FONT_DIRS:
            path = os.path.join(folder, name)
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, size)
                except OSError:
                    font = None
                if font is not None:
                    break
        if font is not None:
            break
    if font is None:
        font = ImageFont.load_default()
    _cache[key] = font
    return font


def wrap_text(text, font, max_width):
    """Bungkus teks jadi beberapa baris yang muat dalam max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


@dataclass
class Style:
    paper: str = "#F7F3E8"
    ink: str = "#1A1A1A"
    navy: str = "#14263F"
    navy_soft: str = "#1F3A5F"
    red: str = "#A93226"
    red_dark: str = "#7E1F16"
    gold: str = "#C9A227"
    grey: str = "#5A5A5A"
    hairline: str = "#B8AE96"
    sea: str = "#D7E6F0"
    land: str = "#D9C89A"
    panel: str = "#FFFFFF"
    date_size: int = 46
    small_caps: int = 15
    badge_size: int = 13
    subhead_size: int = 18
    region_size: int = 11
    stat_num: int = 27
    stat_label: int = 11
    feat_kicker: int = 12
    feat_head: int = 19
    feat_body: int = 13
    feat_src: int = 10
    tile_kicker: int = 10
    tile_head: int = 13
    tile_body: int = 11
    tile_src: int = 9
    brief_title: int = 12
    brief_text: int = 10
    check_size: int = 11
    attrib_size: int = 9


# --- Peta dunia sederhana (lon/lat kasar, digambar sebagai poligon) --------

_CONTINENTS = {
    "north_america": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 60), (-80, 45), (-75, 35), (-80, 25), (-90, 20), (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-125, 48), (-140, 60), (-165, 60)],
    "south_america": [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5), (-40, -10), (-35, -20), (-40, -30), (-50, -35), (-60, -40), (-65, -50), (-70, -55), (-75, -45), (-75, -30), (-80, -15), (-80, -5)],
    "europe": [(-10, 36), (-5, 44), (0, 48), (5, 53), (10, 57), (18, 56), (25, 60), (30, 62), (25, 70), (15, 70), (5, 62), (0, 55), (-5, 50), (-10, 43)],
    "africa": [(-10, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 20), (45, 12), (50, 11), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (10, -5), (5, 5), (-5, 5), (-15, 10), (-17, 15), (-15, 25)],
    "asia": [(30, 70), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75), (100, 77), (110, 76), (120, 73), (130, 72), (140, 72), (150, 70), (160, 65), (160, 60), (155, 55), (145, 50), (140, 45), (135, 40), (130, 35), (127, 33), (120, 30), (110, 25), (105, 20), (100, 15), (95, 10), (90, 15), (85, 20), (80, 15), (75, 10), (70, 20), (65, 25), (60, 25), (55, 27), (50, 30), (45, 30), (40, 32), (35, 36), (30, 36)],
    "australia": [(113, -22), (120, -15), (130, -12), (135, -12), (142, -11), (145, -15), (150, -22), (153, -27), (150, -37), (145, -38), (140, -38), (135, -35), (130, -32), (125, -33), (120, -35), (115, -35), (113, -30)],
}

# Titik bernomor di peta: (nomor, lon, lat) — posisi disebar sedikit
# supaya pin yang berdekatan (Antalya/Crimea) tidak saling menutup.
_MAP_PINS = [
    (1, 114, 22), (2, 4, 52), (3, 28, 35), (4, 37, 47), (5, 47, 25),
    (6, 85, 20), (7, 127, 37), (8, -42, 72), (9, -74, 41), (11, -74, 5),
    (12, 37, -1),
]


def _project(lon, lat, box):
    """Petakan lon/lat ke dalam box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y1 - (lat + 55.0) / 135.0 * (y1 - y0)
    return x, y


def draw_map(draw, box):
    """Gambar peta dunia sederhana + titik merah bernomor."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill="#D7E6F0", outline="#B8AE96", width=1)
    for pts in _CONTINENTS.values():
        poly = [_project(lon, lat, box) for lon, lat in pts]
        draw.polygon(poly, fill="#D9C89A", outline="#A89468")
    for num, lon, lat in _MAP_PINS:
        cx, cy = _project(lon, lat, box)
        r = 6
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#A93226", outline="#FFFFFF", width=1)
        f = load_font("sans_bold", 9)
        tw = draw.textlength(str(num), font=f)
        draw.text((cx - tw / 2, cy - 5), str(num), font=f, fill="#FFFFFF")


def draw_summit(draw, box):
    """Ilustrasi summit: meja + tiga tokoh + tiga bendera."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle(box, fill="#1F3A5F")
    # backdrop panel
    draw.rectangle([x0, y0, x1, y0 + int(h * 0.52)], fill="#2A4A73")
    # tiga bendera di tiang
    flag_w = int(w * 0.16)
    flag_h = int(h * 0.22)
    flag_x = [x0 + int(w * 0.10), x0 + int(w * 0.42), x0 + int(w * 0.74)]
    # US: garis merah-putih + sudut biru
    fx, fy = flag_x[0], y0 + 8
    for i in range(5):
        draw.rectangle([fx, fy + i * (flag_h // 5), fx + flag_w, fy + (i + 1) * (flag_h // 5)],
                       fill="#B03A2E" if i % 2 == 0 else "#FFFFFF")
    draw.rectangle([fx, fy, fx + flag_w // 2, fy + flag_h // 2], fill="#1F3A5F")
    # China: merah + bintang kuning
    fx, fy = flag_x[1], y0 + 8
    draw.rectangle([fx, fy, fx + flag_w, fy + flag_h], fill="#DE2910")
    draw.ellipse([fx + 4, fy + 4, fx + 12, fy + 12], fill="#FFDE00")
    draw.ellipse([fx + flag_w - 12, fy + 4, fx + flag_w - 4, fy + 12], fill="#FFDE00")
    # Rusia: putih-biru-merah
    fx, fy = flag_x[2], y0 + 8
    for i, col in enumerate(["#FFFFFF", "#0039A6", "#D52B1E"]):
        draw.rectangle([fx, fy + i * (flag_h // 3), fx + flag_w, fy + (i + 1) * (flag_h // 3)], fill=col)
    # tiga tokoh di balik meja
    heads = [x0 + int(w * 0.18), x0 + int(w * 0.50), x0 + int(w * 0.82)]
    hy = y0 + int(h * 0.42)
    for cx, suit, tie in zip(heads, ["#20242A", "#1A1A1A", "#2A2A2A"], ["#B03A2E", "#DE2910", "#0039A6"]):
        draw.ellipse([cx - 13, hy - 13, cx + 13, hy + 13], fill="#E8C39E", outline="#8A6B4A")
        draw.rectangle([cx - 22, hy + 13, cx + 22, y0 + int(h * 0.78)], fill=suit)
        draw.polygon([(cx - 5, hy + 13), (cx + 5, hy + 13), (cx, hy + 30)], fill=tie)
    # meja
    draw.rectangle([x0 + 6, y0 + int(h * 0.78), x1 - 6, y1 - 8], fill="#6B4A2A", outline="#4A3018")
    draw.line([x0 + 6, y0 + int(h * 0.78), x1 - 6, y0 + int(h * 0.78)], fill="#C9A227", width=2)
    # pelat nama
    nf = load_font("sans_bold", 11)
    for cx, name in zip(heads, ["TRUMP", "XI", "PUTIN"]):
        tw = draw.textlength(name, font=nf)
        draw.rectangle([cx - tw / 2 - 4, y1 - 26, cx + tw / 2 + 4, y1 - 12], fill="#F7F3E8")
        draw.text((cx - tw / 2, y1 - 25), name, font=nf, fill="#14263F")


def draw_court(draw, box):
    """Ilustrasi pengadilan: gedung + timbangan, lencana 9–6."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle(box, fill="#E8E0CC")
    # gedung
    gx0, gy0 = x0 + int(w * 0.06), y0 + int(h * 0.30)
    gx1, gy1 = x0 + int(w * 0.62), y1 - 10
    draw.rectangle([gx0, gy0, gx1, gy1], fill="#B08D57", outline="#7A5C2E")
    draw.polygon([(gx0 - 6, gy0), ((gx0 + gx1) // 2, gy0 - int(h * 0.16)), (gx1 + 6, gy0)], fill="#8A6B3A")
    for i in range(4):
        cx = gx0 + int((gx1 - gx0) * (0.18 + 0.21 * i))
        draw.rectangle([cx - 5, gy0 + 8, cx + 5, gy1 - 14], fill="#F7F3E8")
    draw.rectangle([gx0, gy1 - 14, gx1, gy1], fill="#7A5C2E")
    # timbangan
    sx = x0 + int(w * 0.80)
    sy = y0 + int(h * 0.22)
    draw.line([sx, sy, sx, y1 - 22], fill="#3A3A3A", width=3)
    draw.line([sx - 26, sy + 12, sx + 26, sy + 12], fill="#3A3A3A", width=3)
    for dx in (-26, 26):
        draw.line([sx + dx, sy + 12, sx + dx, sy + 30], fill="#3A3A3A", width=2)
        draw.polygon([(sx + dx - 12, sy + 30), (sx + dx + 12, sy + 30), (sx + dx, sy + 46)], fill="#C9A227", outline="#8A6B3A")
    draw.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill="#C9A227", outline="#8A6B3A")
    # lencana 9–6
    bf = load_font("sans_bold", 15)
    label = "9–6"
    tw = draw.textlength(label, font=bf)
    draw.rectangle([x1 - int(tw) - 18, y0 + 8, x1 - 8, y0 + 30], fill="#A93226")
    draw.text((x1 - int(tw) - 13, y0 + 10), label, font=bf, fill="#FFFFFF")


def draw_climate(draw, box):
    """Ilustrasi iklim: globe + termometer + matahari."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle(box, fill="#0E5E52")
    # matahari
    sun_cx, sun_cy = x0 + int(w * 0.82), y0 + int(h * 0.20)
    draw.ellipse([sun_cx - 14, sun_cy - 14, sun_cx + 14, sun_cy + 14], fill="#F2C230")
    # globe
    gc_x, gc_y = x0 + int(w * 0.38), y0 + int(h * 0.52)
    gr = int(min(w, h) * 0.30)
    draw.ellipse([gc_x - gr, gc_y - gr, gc_x + gr, gc_y + gr], fill="#2E7AC2", outline="#FFFFFF", width=2)
    draw.polygon([(gc_x - gr + 8, gc_y - 6), (gc_x - 10, gc_y - gr + 12), (gc_x + 6, gc_y - gr + 18), (gc_x + 2, gc_y - 2), (gc_x - 18, gc_y + 4)], fill="#3E9B4F")
    draw.polygon([(gc_x + 4, gc_y + 10), (gc_x + gr - 10, gc_y + 2), (gc_x + gr - 6, gc_y + gr - 12), (gc_x + 12, gc_y + gr - 8), (gc_x - 2, gc_y + 22)], fill="#3E9B4F")
    # termometer
    tx = x0 + int(w * 0.78)
    draw.rounded_rectangle([tx - 7, y0 + int(h * 0.30), tx + 7, y1 - int(h * 0.28)], radius=7, fill="#FFFFFF", outline="#8A8A8A")
    draw.rounded_rectangle([tx - 4, y0 + int(h * 0.55), tx + 4, y1 - int(h * 0.30)], radius=4, fill="#D43A2A")
    draw.ellipse([tx - 13, y1 - int(h * 0.30), tx + 13, y1 - int(h * 0.16)], fill="#D43A2A", outline="#8A8A8A")
    for i, yy in enumerate([0.38, 0.48, 0.58]):
        draw.line([tx + 8, y0 + int(h * yy), tx + 14, y0 + int(h * yy)], fill="#FFFFFF", width=2)
    # garis bawah: COP31
    cf = load_font("sans_bold", 12)
    label = "COP31 · ANTALYA"
    tw = draw.textlength(label, font=cf)
    draw.text((x0 + (w - tw) / 2, y1 - 20), label, font=cf, fill="#FFFFFF")


def draw_icon(draw, box, kind):
    """Strip ilustrasi kecil untuk ubin, sesuai jenis cerita."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    if kind == "bridge":
        draw.rectangle(box, fill="#BFD9E8")
        draw.rectangle([x0, y1 - 10, x1, y1], fill="#3E7AA8")
        draw.arc([x0 + 10, y0 + 6, x1 - 10, y0 + h], start=180, end=360, fill="#5A4A3A", width=3)
        draw.line([x0 + 14, y0 + 8, x0 + 14, y1 - 10], fill="#5A4A3A", width=3)
        draw.line([x1 - 14, y0 + 8, x1 - 14, y1 - 10], fill="#5A4A3A", width=3)
    elif kind == "missile":
        draw.rectangle(box, fill="#2A2A3A")
        draw.polygon([(cx - 4, y0 + 6), (cx + 4, y0 + 6), (cx + 2, cy + 4), (cx - 2, cy + 4)], fill="#C0C0C0")
        draw.rectangle([cx - 3, cy + 2, cx + 3, cy + 12], fill="#8A8A8A")
        draw.polygon([(cx - 6, cy + 12), (cx + 6, cy + 12), (cx, y1 - 4)], fill="#E8641B")
        draw.ellipse([x0 + 8, y1 - 10, x0 + 16, y1 - 2], fill="#F2C230")
        draw.ellipse([x1 - 16, y1 - 12, x1 - 8, y1 - 4], fill="#F2C230")
    elif kind == "cyclone":
        draw.rectangle(box, fill="#CFE3EE")
        for r in (6, 12, 18):
            draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300, fill="#2E6E8E", width=3)
        draw.line([x0 + 10, y1 - 4, x0 + 16, y1 - 10], fill="#2E6E8E", width=2)
        draw.line([x1 - 16, y1 - 4, x1 - 10, y1 - 10], fill="#2E6E8E", width=2)
    elif kind == "gavel":
        draw.rectangle(box, fill="#E8DCC0")
        draw.rectangle([cx - 18, cy - 8, cx + 8, cy + 2], fill="#6B4A2A")
        draw.line([cx + 8, cy - 3, cx + 22, cy + 6], fill="#8A6B3A", width=4)
        draw.rectangle([cx - 16, cy + 10, cx + 16, cy + 14], fill="#4A3018")
    elif kind == "glacier":
        draw.rectangle(box, fill="#BFE0EA")
        draw.polygon([(x0 + 4, y1), (x0 + int(w * 0.30), y0 + 6), (x0 + int(w * 0.55), y1)], fill="#7A9AB0")
        draw.polygon([(x0 + int(w * 0.40), y1), (x0 + int(w * 0.68), y0 + 2), (x1 - 4, y1)], fill="#5A7A90")
        draw.polygon([(x0 + int(w * 0.24), y0 + 12), (x0 + int(w * 0.30), y0 + 6), (x0 + int(w * 0.36), y0 + 12)], fill="#FFFFFF")
        draw.rectangle([x0, y1 - 6, x1, y1], fill="#DFF2F7")
    elif kind == "chart":
        draw.rectangle(box, fill="#0E3A24")
        pts = [(x0 + 6, y1 - 8), (x0 + int(w * 0.3), y1 - 16), (x0 + int(w * 0.5), y1 - 12),
               (x0 + int(w * 0.7), y1 - 24), (x1 - 6, y1 - 30)]
        draw.line(pts, fill="#3ED97A", width=3)
        for px, py in pts:
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill="#F2C230")
    elif kind == "game":
        draw.rectangle(box, fill="#2A0E4A")
        for i, bh in enumerate([10, 18, 14, 22, 12]):
            bx = x0 + 8 + i * int(w * 0.18)
            draw.rectangle([bx, y1 - bh - 4, bx + int(w * 0.13), y1 - 4], fill="#4A2A7A")
        draw.ellipse([cx - 8, y0 + 4, cx + 8, y0 + 20], fill="#F2A93B")
    elif kind == "strike":
        draw.rectangle(box, fill="#E8D9A8")
        for i, hx in enumerate([0.18, 0.38, 0.58, 0.78]):
            px = x0 + int(w * hx)
            draw.ellipse([px - 6, cy - 8, px + 6, cy + 4], fill="#E8C39E", outline="#8A6B4A")
            draw.rectangle([px - 8, cy + 4, px + 8, y1 - 2], fill="#3A5A8A")
        draw.rectangle([x0 + int(w * 0.30), y0 + 2, x0 + int(w * 0.70), y0 + 10], fill="#A93226")
    elif kind == "runner":
        draw.rectangle(box, fill="#C25E10")
        draw.ellipse([x0 + 8, y0 + 6, x1 - 8, y1 - 6], outline="#FFFFFF", width=2)
        draw.line([x0 + 8, cy, x1 - 8, cy], fill="#FFFFFF", width=1)
        draw.ellipse([cx - 5, cy - 12, cx + 5, cy - 2], fill="#1A1A1A")
        draw.line([cx, cy - 2, cx - 8, cy + 8], fill="#1A1A1A", width=3)
        draw.line([cx, cy - 2, cx + 8, cy + 8], fill="#1A1A1A", width=3)
    else:
        draw.rectangle(box, fill="#D9D2C0")
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill="#8A8A8A")


_ART_DRAWERS = {"summit": draw_summit, "court": draw_court, "climate": draw_climate}


class Poster:
    """Satu poster: simpan Image + ImageDraw, bangun per seksi."""

    def __init__(self, style=None):
        self.style = style or Style()
        self.image = Image.new("RGB", (CANVAS_W, CANVAS_H), self.style.paper)
        self.draw = ImageDraw.Draw(self.image)

    # -- util ---------------------------------------------------------------
    def _wrapped(self, text, font, max_w, max_lines=None):
        lines = wrap_text(text, font, max_w)
        if max_lines is not None:
            lines = lines[:max_lines]
        return lines

    def _text_block(self, x, y, lines, font, fill, leading=1.25):
        for line in lines:
            self.draw.text((x, y), line, font=font, fill=fill)
            y += int(font.size * leading)
        return y

    # -- seksi --------------------------------------------------------------
    def banner(self):
        s = self.style
        d = self.draw
        d.rectangle([0, 0, CANVAS_W, 146], fill=s.navy)
        d.rectangle([0, 146, CANVAS_W, 149], fill=s.gold)
        # baris atas: label kiri + lencana kanan
        f_small = load_font("sans_bold", s.small_caps)
        d.text((MARGIN, 18), "THE WORLD IN ONE DAY", font=f_small, fill="#FFFFFF")
        badge = "25 STORIES · EVERY CONTINENT"
        f_badge = load_font("sans_bold", s.badge_size)
        bw = int(d.textlength(badge, font=f_badge)) + 20
        d.rounded_rectangle([CANVAS_W - MARGIN - bw, 14, CANVAS_W - MARGIN, 14 + 26], radius=4, fill=s.red)
        d.text((CANVAS_W - MARGIN - bw + 10, 19), badge, font=f_badge, fill="#FFFFFF")
        # tanggal besar di tengah
        f_date = load_font("serif_bold", s.date_size)
        date = "THURSDAY 19 NOVEMBER 2026"
        tw = d.textlength(date, font=f_date)
        d.text(((CANVAS_W - tw) / 2, 52), date, font=f_date, fill="#FFFFFF")
        # garis emas tipis di bawah tanggal
        d.line([MARGIN, 124, CANVAS_W - MARGIN, 124], fill=s.gold, width=1)

    def subhead(self):
        s = self.style
        f = load_font("serif", s.subhead_size)
        line = "Trump, Xi and Putin share one table · World Court finds genocide in Myanmar · COP31 draft drops fossil fuels"
        tw = self.draw.textlength(line, font=f)
        self.draw.text(((CANVAS_W - tw) / 2, 156), line, font=f, fill=s.red_dark)

    def regions(self):
        s = self.style
        f = load_font("sans_bold", s.region_size)
        line = "  ·  ".join(REGIONS)
        tw = self.draw.textlength(line, font=f)
        self.draw.text(((CANVAS_W - tw) / 2, 182), line, font=f, fill=s.grey)

    def stats(self):
        s = self.style
        d = self.draw
        y0, y1 = 202, 254
        d.rectangle([MARGIN, y0, CANVAS_W - MARGIN, y1], fill=s.panel, outline=s.hairline, width=1)
        cell_w = (CANVAS_W - 2 * MARGIN) / len(STATS)
        for i, stat in enumerate(STATS):
            x = MARGIN + i * cell_w
            if i > 0:
                d.line([x, y0 + 8, x, y1 - 8], fill=s.hairline, width=1)
            f_num = load_font("sans_bold", s.stat_num)
            num = stat["value"]
            tw = d.textlength(num, font=f_num)
            d.text((x + (cell_w - tw) / 2, y0 + 6), num, font=f_num, fill=stat["color"])
            f_lab = load_font("sans", s.stat_label)
            lines = self._wrapped(stat["label"], f_lab, cell_w - 12, max_lines=2)
            ly = y0 + 6 + s.stat_num + 2
            for line in lines:
                lw = d.textlength(line, font=f_lab)
                d.text((x + (cell_w - lw) / 2, ly), line, font=f_lab, fill=s.grey)
                ly += s.stat_label + 1

    def features(self):
        s = self.style
        d = self.draw
        y0, y1 = 262, 510
        gap = 10
        cell_w = (CANVAS_W - 2 * MARGIN - 2 * gap) / 3
        for i, feat in enumerate(FEATURES):
            x0 = MARGIN + i * (cell_w + gap)
            x1 = x0 + cell_w
            d.rectangle([x0, y0, x1, y1], fill=s.panel, outline=s.hairline, width=1)
            # ilustrasi ~55% tinggi panel
            art_h = int((y1 - y0) * 0.52)
            drawer = _ART_DRAWERS.get(feat["art"])
            if drawer is not None:
                drawer(d, (x0 + 1, y0 + 1, x1 - 1, y0 + art_h))
            d.line([x0, y0 + art_h, x1, y0 + art_h], fill=feat["accent"], width=3)
            # kicker
            f_k = load_font("sans_bold", s.feat_kicker)
            d.text((x0 + 10, y0 + art_h + 8), feat["kicker"], font=f_k, fill=feat["accent"])
            # headline 2 baris
            f_h = load_font("serif_bold", s.feat_head)
            head_lines = self._wrapped(feat["headline"], f_h, cell_w - 20, max_lines=2)
            hy = y0 + art_h + 8 + s.feat_kicker + 6
            hy = self._text_block(x0 + 10, hy, head_lines, f_h, s.ink, leading=1.12)
            # ringkasan 2 baris
            f_b = load_font("serif", s.feat_body)
            body_lines = self._wrapped(feat["body"], f_b, cell_w - 20, max_lines=2)
            hy = self._text_block(x0 + 10, hy + 4, body_lines, f_b, s.ink, leading=1.2)
            # sumber
            f_s = load_font("sans", s.feat_src)
            d.text((x0 + 10, y1 - 18), feat["source"], font=f_s, fill=s.grey)

    def tiles(self):
        s = self.style
        d = self.draw
        y0 = 518
        rows = 2
        cols = 4
        gap = 8
        cell_w = (CANVAS_W - 2 * MARGIN - (cols - 1) * gap) / cols
        cell_h = 110
        for idx, tile in enumerate(TILES[: rows * cols]):
            r = idx // cols
            c = idx % cols
            x0 = MARGIN + c * (cell_w + gap)
            x1 = x0 + cell_w
            ty0 = y0 + r * (cell_h + gap)
            ty1 = ty0 + cell_h
            d.rectangle([x0, ty0, x1, ty1], fill=s.panel, outline=s.hairline, width=1)
            # strip ilustrasi
            draw_icon(d, (x0 + 1, ty0 + 1, x1 - 1, ty0 + 33), tile["art"])
            # nomor urut + kicker
            f_n = load_font("sans_bold", 11)
            num = str(idx + 4)
            d.ellipse([x0 + 6, ty0 + 37, x0 + 22, ty0 + 53], fill=tile["accent"])
            tw = d.textlength(num, font=f_n)
            d.text((x0 + 14 - tw / 2, ty0 + 39), num, font=f_n, fill="#FFFFFF")
            f_k = load_font("sans_bold", s.tile_kicker)
            d.text((x0 + 26, ty0 + 40), tile["kicker"], font=f_k, fill=tile["accent"])
            # headline 2 baris
            f_h = load_font("serif_bold", 12)
            head_lines = self._wrapped(tile["headline"], f_h, cell_w - 12, max_lines=2)
            hy = ty0 + 56
            hy = self._text_block(x0 + 6, hy, head_lines, f_h, s.ink, leading=1.1)
            # ringkasan 1 baris
            f_b = load_font("serif", 10)
            body_lines = self._wrapped(tile["body"], f_b, cell_w - 12, max_lines=1)
            self._text_block(x0 + 6, hy + 2, body_lines, f_b, s.ink, leading=1.15)
            # sumber
            f_s = load_font("sans", s.tile_src)
            d.text((x0 + 6, ty1 - 12), tile["source"], font=f_s, fill=s.grey)

    def map_and_more(self):
        s = self.style
        d = self.draw
        y0, y1 = 754, 934
        # kiri: peta
        map_w = 470
        mx0, mx1 = MARGIN, MARGIN + map_w
        f_t = load_font("sans_bold", s.brief_title)
        d.text((mx0, y0), "WHERE IT HAPPENED", font=f_t, fill=s.ink)
        d.line([mx0, y0 + 18, mx1, y0 + 18], fill=s.red, width=2)
        draw_map(d, (mx0, y0 + 24, mx1, y1 - 22))
        f_cap = load_font("sans", 9)
        cap = "Red numbers mark stories 1–11. Positions are approximate."
        d.text((mx0, y1 - 18), cap, font=f_cap, fill=s.grey)
        # kanan: daftar ALSO ON — satu kolom 14 baris, tiap baris satu baris
        bx0 = mx1 + 16
        bx1 = CANVAS_W - MARGIN
        d.text((bx0, y0), "ALSO ON THURSDAY 19 NOVEMBER", font=f_t, fill=s.red_dark)
        d.line([bx0, y0 + 18, bx1, y0 + 18], fill=s.red, width=2)
        f_b = load_font("sans", s.brief_text)
        for i, brief in enumerate(BRIEFS):
            by = y0 + 26 + i * 11
            line = f"{brief['num']} {brief['place']} — {brief['text']} {brief['source']}."
            while f_b.getlength(line) > (bx1 - bx0) and len(line) > 20:
                line = line[:-4] + "…"
            d.text((bx0, by), line, font=f_b, fill=s.ink)

    def datecheck(self):
        s = self.style
        d = self.draw
        y0, y1 = 940, 988
        d.rectangle([MARGIN, y0, CANVAS_W - MARGIN, y1], fill=s.navy)
        # label di baris sendiri
        f_c = load_font("sans_bold", s.check_size)
        label = "DATE CHECK ✓  LEFT OUT — NOT 19 NOVEMBER NEWS:"
        d.text((MARGIN + 8, y0 + 4), label, font=f_c, fill="#F2C230")
        # daftar item di dua baris penuh
        f_i = load_font("sans", s.check_size)
        items = "  ·  ".join(LEFT_OUT)
        lines = self._wrapped(items, f_i, CANVAS_W - 2 * MARGIN - 16, max_lines=2)
        ly = y0 + 20
        for line in lines:
            d.text((MARGIN + 8, ly), line, font=f_i, fill="#FFFFFF")
            ly += s.check_size + 4

    def attribution(self):
        s = self.style
        f = load_font("sans", s.attrib_size)
        lines = self._wrapped(ATTRIBUTION, f, CANVAS_W - 2 * MARGIN, max_lines=2)
        y = 992
        for line in lines:
            tw = self.draw.textlength(line, font=f)
            self.draw.text(((CANVAS_W - tw) / 2, y), line, font=f, fill=s.grey)
            y += s.attrib_size + 3

    def render(self):
        self.banner()
        self.subhead()
        self.regions()
        self.stats()
        self.features()
        self.tiles()
        self.map_and_more()
        self.datecheck()
        self.attribution()
        return self.image


def build_poster():
    """Bangun poster lengkap dan kembalikan sebagai PIL Image."""
    poster = Poster()
    return poster.render()
