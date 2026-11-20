# poster.py — mesin layout poster "The World in One Day" (ronde 5).
# Menggambar poster 1024x1024 dari nol dengan primitif PIL saja:
# tanpa file gambar eksternal, tanpa network. Data berita dari stories.py.
# File ini dipakai builder untuk me-render poster-20261119.png secara
# lokal; main.py (yang jalan di grader) TIDAK mengimpor file ini.

import os
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

from stories import BRIEFS, FEATURES, LEFT_OUT, REGIONS, STATS, SUBHEAD, TILES

# ---------------------------------------------------------------- fonts ---

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/local/share/fonts",
    "/usr/share/fonts/truetype",
    os.path.expanduser("~/.fonts"),
]

FONT_FILES = {
    "serif": ["DejaVuSerif.ttf"],
    "serif_bold": ["DejaVuSerif-Bold.ttf"],
    "sans": ["DejaVuSans.ttf"],
    "sans_bold": ["DejaVuSans-Bold.ttf"],
    "sans_italic": ["DejaVuSans-Oblique.ttf", "DejaVuSans.ttf"],
    "serif_italic": ["DejaVuSerif-Italic.ttf", "DejaVuSerif.ttf"],
}

_font_cache = {}


def load_font(role, size):
    """Muat font DejaVu dari path sistem yang umum; fallback ke default."""
    key = (role, size)
    if key in _font_cache:
        return _font_cache[key]
    font = None
    for name in FONT_FILES.get(role, ["DejaVuSans.ttf"]):
        for d in FONT_DIRS:
            path = os.path.join(d, name)
            if os.path.isfile(path):
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
    _font_cache[key] = font
    return font


def wrap_text(text, font, max_width):
    """Pecah teks menjadi baris-baris yang muat dalam max_width (pixel)."""
    words = text.split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        trial = current + " " + word
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def fit_one_line(text, font, max_width):
    """Pendekkan teks dari ujung sampai muat satu baris, pakai elipsis."""
    if font.getlength(text) <= max_width:
        return text
    words = text.split()
    while len(words) > 1 and font.getlength(" ".join(words) + " …") > max_width:
        words.pop()
    return " ".join(words) + " …"


# --------------------------------------------------------------- style ---

@dataclass
class Style:
    paper: str = "#F7F3E8"
    navy: str = "#1A2340"
    navy_soft: str = "#232C4E"
    ink: str = "#1F2937"
    muted: str = "#6B7280"
    red: str = "#C53030"
    red_dark: str = "#9B2C2C"
    gold: str = "#D9A441"
    line: str = "#D8D2C0"
    card: str = "#FFFFFF"
    map_land: str = "#8FB996"
    map_sea: str = "#DCE9F5"


# -------------------------------------------------------------- poster ---

class Poster:
    W = 1024
    H = 1024

    def __init__(self):
        self.style = Style()
        self.img = Image.new("RGB", (self.W, self.H), self.style.paper)
        self.d = ImageDraw.Draw(self.img)

    # -- helpers ------------------------------------------------------
    def text(self, xy, s, font, fill, anchor="la"):
        self.d.text(xy, s, font=font, fill=fill, anchor=anchor)

    def center(self, y, s, font, fill, cx=512):
        self.d.text((cx, y), s, font=font, fill=fill, anchor="ma")

    def rrect(self, box, radius, fill=None, outline=None, width=1):
        self.d.rounded_rectangle(box, radius=radius, fill=fill,
                                 outline=outline, width=width)

    # -- banner -------------------------------------------------------
    def banner(self):
        s = self.style
        d = self.d
        d.rectangle([0, 0, 1024, 148], fill=s.navy)
        # kiri: nama koran
        self.text((20, 20), "THE WORLD IN ONE DAY",
                  load_font("sans_bold", 16), "#FFFFFF")
        # tengah: tanggal besar
        self.center(42, "THURSDAY 19 NOVEMBER 2026",
                    load_font("serif_bold", 44), "#FFFFFF")
        # kanan: lencana merah
        badge = "25 STORIES · EVERY CONTINENT"
        bf = load_font("sans_bold", 14)
        bw = int(bf.getlength(badge)) + 28
        self.rrect([1024 - 20 - bw, 16, 1024 - 20, 44], 14, fill=s.red)
        self.center(22, badge, bf, "#FFFFFF", cx=1024 - 20 - bw // 2)
        # strip wilayah di bawah pita
        regions = " · ".join("%s %d" % (name, n) for name, n in REGIONS)
        self.center(118, regions, load_font("sans", 14), "#B9C0D8")
        # garis emas di bawah banner
        d.rectangle([0, 148, 1024, 151], fill=s.gold)

    def subhead(self):
        self.center(158, SUBHEAD, load_font("serif_italic", 17),
                    self.style.red_dark)

    # -- stats --------------------------------------------------------
    def stats(self):
        s = self.style
        y0, y1 = 180, 248
        gap = 8
        w = (1024 - 24 - gap * 5) // 6
        for i, st in enumerate(STATS):
            x0 = 12 + i * (w + gap)
            x1 = x0 + w
            self.rrect([x0, y0, x1, y1], 8, fill=s.card, outline=s.line)
            vf = load_font("sans_bold", 30)
            self.center(y0 + 8, st["value"], vf, st["color"],
                        cx=(x0 + x1) // 2)
            self.center(y0 + 44, st["label"], load_font("sans", 12),
                        s.muted, cx=(x0 + x1) // 2)

    # -- feature illustrations ----------------------------------------
    def draw_summit(self, box):
        x0, y0, x1, y1 = box
        d = self.d
        d.rectangle(box, fill="#BFD9EE")
        # meja
        d.rectangle([x0 + 20, y1 - 34, x1 - 20, y1 - 18], fill="#7B4A2B")
        d.rectangle([x0 + 30, y1 - 18, x1 - 30, y1 - 8], fill="#5D3620")
        # tiga bendera + kepala
        cols = ["#C53030", "#C53030", "#F5F5F5"]
        for i, c in enumerate(cols):
            cx = x0 + 60 + i * 100
            d.line([cx, y0 + 18, cx, y0 + 62], fill="#4A3728", width=3)
            d.rectangle([cx, y0 + 18, cx + 44, y0 + 40], fill=c,
                        outline="#4A3728")
            d.ellipse([cx - 13, y0 + 66, cx + 13, y0 + 92], fill="#F2C9A0",
                      outline="#4A3728")

    def draw_court(self, box):
        x0, y0, x1, y1 = box
        d = self.d
        d.rectangle(box, fill="#EDE6D6")
        cx = (x0 + x1) // 2
        # atap segitiga
        d.polygon([(cx - 90, y0 + 34), (cx + 90, y0 + 34), (cx, y0 + 8)],
                  fill="#8A7B5C")
        # kolom
        for i in range(4):
            px = x0 + 52 + i * 58
            d.rectangle([px, y0 + 38, px + 18, y1 - 16], fill="#C9BFA6",
                        outline="#8A7B5C")
        # timbangan kecil
        d.line([cx, y0 + 44, cx, y0 + 62], fill="#4A3728", width=2)
        d.line([cx - 22, y0 + 50, cx + 22, y0 + 50], fill="#4A3728", width=2)
        d.arc([cx - 30, y0 + 50, cx - 14, y0 + 66], 0, 180, fill="#4A3728",
              width=2)
        d.arc([cx + 14, y0 + 50, cx + 30, y0 + 66], 0, 180, fill="#4A3728",
              width=2)

    def draw_climate(self, box):
        x0, y0, x1, y1 = box
        d = self.d
        d.rectangle(box, fill="#D3EAD9")
        # matahari
        d.ellipse([x0 + 16, y0 + 12, x0 + 44, y0 + 40], fill="#F6C445")
        # globe
        cx, cy, r = (x0 + x1) // 2 - 10, (y0 + y1) // 2 + 6, 42
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#5B9BD5",
                  outline="#2B6CB0", width=2)
        d.ellipse([cx - 22, cy - 26, cx + 2, cy - 6], fill="#5FA86A")
        d.ellipse([cx + 6, cy + 8, cx + 26, cy + 28], fill="#5FA86A")
        # termometer
        tx = x1 - 34
        d.rounded_rectangle([tx, y0 + 14, tx + 14, y1 - 18], 7,
                            fill="#FFFFFF", outline="#9B2C2C", width=2)
        d.rectangle([tx + 4, y0 + 34, tx + 10, y1 - 26], fill="#C53030")
        d.ellipse([tx - 3, y1 - 30, tx + 17, y1 - 10], fill="#C53030")

    # -- features -----------------------------------------------------
    def features(self):
        s = self.style
        y0, y1 = 254, 496
        gap = 10
        w = (1024 - 24 - gap * 2) // 3
        art = {"summit": self.draw_summit, "court": self.draw_court,
               "climate": self.draw_climate}
        for i, f in enumerate(FEATURES):
            x0 = 12 + i * (w + gap)
            x1 = x0 + w
            self.rrect([x0, y0, x1, y1], 8, fill=s.card, outline=s.line)
            # ilustrasi 46% tinggi panel
            ill_h = int((y1 - y0) * 0.46)
            art[f["art"]]([x0 + 1, y0 + 1, x1 - 1, y0 + ill_h])
            ty = y0 + ill_h + 8
            # kicker
            self.text((x0 + 12, ty), "%s · %s" % (f["place"], f["kicker"]),
                      load_font("sans_bold", 13), s.red)
            # headline 2 baris
            hf = load_font("serif_bold", 19)
            lines = wrap_text(f["headline"], hf, w - 24)
            hy = ty + 18
            for ln in lines[:2]:
                self.text((x0 + 12, hy), ln, hf, s.ink)
                hy += 22
            # body 2 baris
            bf = load_font("sans", 13)
            blines = wrap_text(f["body"], bf, w - 24)
            by = hy + 4
            for ln in blines[:2]:
                self.text((x0 + 12, by), ln, bf, "#374151")
                by += 16
            # sumber di dasar panel (jarak aman dari body)
            self.text((x0 + 12, y1 - 16), f["source"],
                      load_font("sans", 11), s.muted)

    # -- tile icons ---------------------------------------------------
    def draw_icon(self, kind, box):
        x0, y0, x1, y1 = box
        d = self.d
        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2
        if kind == "bridge":
            d.arc([x0 + 8, y0 - 6, x1 - 8, y1 + 14], 180, 360,
                  fill="#4A5568", width=3)
            d.line([x0 + 8, y1 - 4, x1 - 8, y1 - 4], fill="#4A5568", width=3)
            for px in (x0 + 30, cx, x1 - 30):
                d.line([px, y0 + 8, px, y1 - 4], fill="#4A5568", width=2)
        elif kind == "missile":
            d.polygon([(cx, y0 + 2), (cx + 8, y0 + 14), (cx - 8, y0 + 14)],
                      fill="#9B2C2C")
            d.line([cx, y0 + 14, cx, y1 - 2], fill="#9B2C2C", width=3)
        elif kind == "storm":
            for r, ox in ((7, -14), (9, 0), (7, 14)):
                d.ellipse([cx + ox - r, cy - r, cx + ox + r, cy + r],
                          fill="#718096")
        elif kind == "court":
            d.polygon([(cx - 26, y0 + 4), (cx + 26, y0 + 4), (cx, y0 - 6)],
                      fill="#8A7B5C")
            for px in (cx - 22, cx - 6, cx + 10):
                d.rectangle([px, y0 + 6, px + 6, y1 - 2], fill="#C9BFA6")
        elif kind == "ice":
            d.polygon([(x0 + 6, y1 - 2), (cx - 8, y0 + 4), (cx + 4, y1 - 2)],
                      fill="#BEE3F8", outline="#2B6CB0")
            d.polygon([(cx - 2, y1 - 2), (cx + 14, y0 + 8), (x1 - 6, y1 - 2)],
                      fill="#EBF8FF", outline="#2B6CB0")
        elif kind == "chart":
            d.line([(x0 + 8, y1 - 6), (cx - 8, y0 + 12), (cx + 8, y0 + 16),
                    (x1 - 8, y0 + 2)], fill="#2F855A", width=3)
            for px, py in ((x0 + 8, y1 - 6), (cx - 8, y0 + 12), (x1 - 8, y0 + 2)):
                d.ellipse([px - 3, py - 3, px + 3, py + 3], fill="#2F855A")
        elif kind == "game":
            d.rounded_rectangle([x0 + 10, y0 + 4, x1 - 10, y1 - 4], 6,
                                fill="#6B46C1")
            d.ellipse([cx + 8, cy - 3, cx + 14, cy + 3], fill="#F6E05E")
            d.ellipse([cx + 16, cy - 3, cx + 22, cy + 3], fill="#F6E05E")
        elif kind == "march":
            for px in (cx - 22, cx, cx + 22):
                d.ellipse([px - 4, y0 + 2, px + 4, y0 + 10], fill="#1F2937")
                d.rectangle([px - 2, y0 + 11, px + 2, y1 - 2], fill="#1F2937")

    # -- tiles --------------------------------------------------------
    def tiles(self):
        s = self.style
        gap = 10
        w = (1024 - 24 - gap * 3) // 4
        rows = [(504, 612), (618, 726)]
        strip_colors = ["#DCE9F5", "#FDE8E8", "#E6F4EA", "#EDE9FE",
                        "#DCE9F5", "#E6F4EA", "#F3E8FF", "#FEF3C7"]
        for idx, t in enumerate(TILES):
            row = idx // 4
            col = idx % 4
            y0, y1 = rows[row]
            x0 = 12 + col * (w + gap)
            x1 = x0 + w
            self.rrect([x0, y0, x1, y1], 8, fill=s.card, outline=s.line)
            # strip ilustrasi 24px
            self.d.rectangle([x0 + 1, y0 + 1, x1 - 1, y0 + 24],
                             fill=strip_colors[idx])
            self.draw_icon(t["art"], [x0 + w - 52, y0 + 2, x1 - 8, y0 + 23])
            # lencana nomor
            self.d.ellipse([x0 + 6, y0 + 4, x0 + 24, y0 + 22], fill=s.red)
            nf = load_font("sans_bold", 11)
            tw = nf.getlength(str(t["num"]))
            self.d.text((x0 + 15 - tw / 2, y0 + 6), str(t["num"]),
                        font=nf, fill="#FFFFFF")
            # kicker
            self.text((x0 + 10, y0 + 29), "%s · %s" % (t["place"], t["kicker"]),
                      load_font("sans_bold", 11), s.red)
            # headline 2 baris
            hf = load_font("sans_bold", 15)
            lines = wrap_text(t["headline"], hf, w - 20)
            hy = y0 + 43
            for ln in lines[:2]:
                self.text((x0 + 10, hy), ln, hf, s.ink)
                hy += 16
            # body 1 baris (sudah dipendekkan agar jadi kalimat utuh)
            bf = load_font("sans", 12)
            body = fit_one_line(t["body"], bf, w - 20)
            self.text((x0 + 10, y0 + 77), body, bf, "#374151")
            # sumber di dasar ubin (jarak aman dari body)
            self.text((x0 + 10, y1 - 11), t["source"],
                      load_font("sans", 10), s.muted)

    # -- map + also on ------------------------------------------------
    def map_and_more(self):
        s = self.style
        y0, y1 = 732, 918
        # panel peta (kiri)
        mx0, mx1 = 12, 502
        self.rrect([mx0, y0, mx1, y1], 8, fill=s.card, outline=s.line)
        self.text((mx0 + 12, y0 + 8), "WHERE IT HAPPENED",
                  load_font("sans_bold", 14), s.ink)
        self.draw_map([mx0 + 12, y0 + 30, mx1 - 12, y1 - 22])
        self.text((mx0 + 12, y1 - 18), "Red numbers mark stories 1–11.",
                  load_font("sans", 11), s.muted)
        # panel ALSO ON (kanan)
        ax0, ax1 = 514, 1012
        self.rrect([ax0, y0, ax1, y1], 8, fill=s.card, outline=s.line)
        self.text((ax0 + 12, y0 + 8), "ALSO ON THURSDAY 19 NOVEMBER",
                  load_font("sans_bold", 14), s.ink)
        bf = load_font("sans", 11)
        by = y0 + 30
        for b in BRIEFS:
            line = "%d. %s — %s (%s)" % (b["num"], b["place"], b["text"],
                                         b["source"])
            line = fit_one_line(line, bf, ax1 - ax0 - 24)
            self.text((ax0 + 12, by), line, bf, s.ink)
            by += 11

    def draw_map(self, box):
        x0, y0, x1, y1 = box
        d = self.d
        s = self.style
        d.rectangle(box, fill=s.map_sea)
        # garis lintang putus-putus
        midy = (y0 + y1) // 2
        for x in range(x0, x1, 12):
            d.line([x, midy, x + 6, midy], fill="#9DB8D2", width=1)
        # benua (poligon kasar, hijau)
        land = s.map_land
        d.polygon([(x0 + 10, y0 + 28), (x0 + 90, y0 + 10), (x0 + 150, y0 + 23),
                   (x0 + 145, y0 + 58), (x0 + 110, y0 + 83), (x0 + 50, y0 + 78),
                   (x0 + 15, y0 + 53)], fill=land)
        d.polygon([(x0 + 130, y0 + 6), (x0 + 152, y0 + 2), (x0 + 162, y0 + 12),
                   (x0 + 140, y0 + 22)], fill=land)  # Greenland
        d.polygon([(x0 + 120, y0 + 93), (x0 + 160, y0 + 88), (x0 + 175, y0 + 113),
                   (x0 + 155, y0 + 143), (x0 + 130, y0 + 128)], fill=land)
        d.polygon([(x0 + 220, y0 + 13), (x0 + 260, y0 + 6), (x0 + 280, y0 + 20),
                   (x0 + 255, y0 + 38), (x0 + 225, y0 + 33)], fill=land)
        d.polygon([(x0 + 230, y0 + 48), (x0 + 280, y0 + 43), (x0 + 295, y0 + 83),
                   (x0 + 265, y0 + 118), (x0 + 235, y0 + 98)], fill=land)
        d.polygon([(x0 + 290, y0 + 8), (x0 + 400, y0 + 3), (x0 + 440, y0 + 28),
                   (x0 + 420, y0 + 68), (x0 + 360, y0 + 83), (x0 + 310, y0 + 58),
                   (x0 + 285, y0 + 33)], fill=land)
        d.polygon([(x0 + 380, y0 + 108), (x0 + 430, y0 + 103), (x0 + 440, y0 + 123),
                   (x0 + 400, y0 + 133)], fill=land)  # Australia
        # pin bernomor 1-11
        pins = {
            1: (x0 + 405, y0 + 53), 2: (x0 + 235, y0 + 20),
            3: (x0 + 250, y0 + 43), 4: (x0 + 275, y0 + 26),
            5: (x0 + 300, y0 + 53), 6: (x0 + 370, y0 + 58),
            7: (x0 + 420, y0 + 33), 8: (x0 + 145, y0 + 12),
            9: (x0 + 90, y0 + 43), 10: (x0 + 190, y0 + 68),
            11: (x0 + 140, y0 + 106),
        }
        nf = load_font("sans_bold", 11)
        for num, (px, py) in pins.items():
            d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=s.red,
                      outline="#FFFFFF", width=1)
            label = str(num)
            tw = nf.getlength(label)
            d.text((px - tw / 2, py - 6), label, font=nf, fill="#FFFFFF")

    # -- footer -------------------------------------------------------
    def datecheck(self):
        s = self.style
        y0, y1 = 924, 1024
        d = self.d
        d.rectangle([0, y0, 1024, y1], fill=s.navy)
        self.text((20, y0 + 10), "DATE CHECK",
                  load_font("sans_bold", 13), s.gold)
        self.text((128, y0 + 10), "LEFT OUT — NOT 19 NOVEMBER NEWS:",
                  load_font("sans_bold", 13), "#FFFFFF")
        # daftar left-out, dibungkus 2 baris
        lf = load_font("sans", 12)
        joined = "  |  ".join(LEFT_OUT)
        lines = wrap_text(joined, lf, 1024 - 40)
        ly = y0 + 30
        for ln in lines[:2]:
            self.text((20, ly), ln, lf, "#C7CEDD")
            ly += 16
        self.text((20, y1 - 18),
                  "Every story here happened, or was first reported, on "
                  "Thursday 19 November 2026. Sources: Reuters, AP, AFP, "
                  "BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, "
                  "Nature.",
                  load_font("sans", 10), "#8A93AD")

    def render(self):
        self.banner()
        self.subhead()
        self.stats()
        self.features()
        self.tiles()
        self.map_and_more()
        self.datecheck()
        return self.img


def build_poster():
    """Render poster 1024x1024, kembalikan PIL Image."""
    return Poster().render()


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "poster-20261119.png"
    build_poster().save(out, format="PNG")
    print("wrote %s" % out)
