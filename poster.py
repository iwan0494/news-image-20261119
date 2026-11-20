# poster.py — mesin layout poster "The World in One Day" (ronde 4).
# Menggambar poster 1024x1024 dari nol dengan primitif PIL saja:
# tanpa file gambar eksternal, tanpa network. Data berita dari stories.py.

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


# ---------------------------------------------------------------- style ---

@dataclass
class Style:
    paper: tuple = (247, 243, 232)
    navy: tuple = (16, 32, 64)
    navy_light: tuple = (28, 52, 96)
    red: tuple = (178, 34, 34)
    dark_red: tuple = (139, 0, 0)
    ink: tuple = (26, 26, 26)
    grey: tuple = (110, 110, 105)
    line: tuple = (200, 192, 175)
    white: tuple = (255, 255, 255)
    cream: tuple = (250, 246, 236)
    gold: tuple = (201, 162, 39)
    teal: tuple = (18, 130, 130)
    green: tuple = (34, 120, 60)
    sky: tuple = (70, 130, 180)


# ---------------------------------------------------------------- poster --

class Poster:
    """Menggambar satu poster 1024x1024."""

    W = 1024
    H = 1024
    MARGIN = 16

    def __init__(self):
        self.style = Style()
        self.img = Image.new("RGB", (self.W, self.H), self.style.paper)
        self.draw = ImageDraw.Draw(self.img)

    # ------------------------------------------------------------ banner --
    def banner(self):
        d = self.draw
        s = self.style
        d.rectangle([0, 0, self.W, 148], fill=s.navy)
        d.rectangle([0, 148, self.W, 151], fill=s.gold)
        # kiri: nama koran kecil
        f_small = load_font("sans_bold", 17)
        d.text((self.MARGIN + 4, 18), "THE WORLD IN ONE DAY",
               font=f_small, fill=s.white)
        # tengah: tanggal serif sangat besar
        f_date = load_font("serif_bold", 46)
        date = "THURSDAY 19 NOVEMBER 2026"
        tw = d.textlength(date, font=f_date)
        d.text(((self.W - tw) / 2, 52), date, font=f_date, fill=s.white)
        # kanan: lencana merah
        badge = "25 STORIES \u00b7 EVERY CONTINENT"
        f_badge = load_font("sans_bold", 15)
        bw = d.textlength(badge, font=f_badge) + 24
        bx0 = self.W - self.MARGIN - bw
        d.rounded_rectangle([bx0, 14, bx0 + bw, 42], radius=14, fill=s.red)
        d.text((bx0 + 12, 21), badge, font=f_badge, fill=s.white)
        # garis bawah pita: ringkasan wilayah
        f_reg = load_font("sans", 13)
        regions = "  \u00b7  ".join("%s %d" % (name, n) for name, n in REGIONS)
        rw = d.textlength(regions, font=f_reg)
        d.text(((self.W - rw) / 2, 118), regions, font=f_reg,
               fill=(190, 200, 220))

    # ----------------------------------------------------------- subhead --
    def subhead(self):
        d = self.draw
        s = self.style
        f = load_font("serif_italic", 19)
        tw = d.textlength(SUBHEAD, font=f)
        d.text(((self.W - tw) / 2, 156), SUBHEAD, font=f, fill=s.dark_red)

    # ------------------------------------------------------------- stats --
    def stats(self):
        d = self.draw
        s = self.style
        y0, y1 = 182, 252
        n = len(STATS)
        avail = self.W - 2 * self.MARGIN
        bw = avail // n
        for i, st in enumerate(STATS):
            x0 = self.MARGIN + i * bw
            x1 = x0 + bw - 8
            d.rounded_rectangle([x0, y0, x1, y1], radius=6,
                                fill=s.cream, outline=s.line, width=1)
            f_val = load_font("sans_bold", 26)
            val = st["value"]
            vw = d.textlength(val, font=f_val)
            d.text((x0 + (bw - 8 - vw) / 2, y0 + 8), val,
                   font=f_val, fill=st["color"])
            f_lab = load_font("sans", 11)
            for j, line in enumerate(wrap_text(st["label"], f_lab, bw - 16)):
                lw = d.textlength(line, font=f_lab)
                d.text((x0 + (bw - 8 - lw) / 2, y0 + 40 + j * 13),
                       line, font=f_lab, fill=s.ink)

    # ---------------------------------------------------------- features --
    def features(self):
        d = self.draw
        s = self.style
        y0, y1 = 262, 500
        avail = self.W - 2 * self.MARGIN
        gap = 10
        pw = (avail - 2 * gap) // 3
        for i, feat in enumerate(FEATURES):
            x0 = self.MARGIN + i * (pw + gap)
            x1 = x0 + pw
            d.rounded_rectangle([x0, y0, x1, y1], radius=6,
                                fill=s.white, outline=s.line, width=1)
            # nomor cerita
            self._num_badge(x0 + 8, y0 + 8, feat["num"])
            # ilustrasi ~46% tinggi panel (dulu 52%: teks bawah menabrak sumber)
            art_h = int((y1 - y0) * 0.46)
            art = (x0 + 6, y0 + 6, x1 - 6, y0 + 6 + art_h)
            if feat["art"] == "summit":
                self.draw_summit(art)
            elif feat["art"] == "court":
                self.draw_court(art)
            else:
                self.draw_climate(art)
            ty = y0 + 6 + art_h + 8
            # kicker
            f_kick = load_font("sans_bold", 12)
            d.text((x0 + 10, ty), "%s \u00b7 %s" % (feat["place"], feat["kicker"]),
                   font=f_kick, fill=s.red)
            ty += 17
            # headline 2 baris
            f_head = load_font("serif_bold", 19)
            for line in wrap_text(feat["headline"], f_head, pw - 20)[:2]:
                d.text((x0 + 10, ty), line, font=f_head, fill=s.ink)
                ty += 22
            ty += 3
            # ringkasan 2 baris (jarak aman ke sumber di bawah)
            f_body = load_font("sans", 12)
            for line in wrap_text(feat["body"], f_body, pw - 20)[:2]:
                d.text((x0 + 10, ty), line, font=f_body, fill=s.ink)
                ty += 14
            # sumber di posisi tetap, jauh di bawah baris body terakhir
            f_src = load_font("sans_italic", 10)
            d.text((x0 + 10, y1 - 16), feat["source"], font=f_src, fill=s.grey)

    # ------------------------------------------------------------- tiles --
    def tiles(self):
        d = self.draw
        s = self.style
        y0 = 510
        avail = self.W - 2 * self.MARGIN
        gap = 8
        tw = (avail - 3 * gap) // 4
        th = 96
        for idx, tile in enumerate(TILES):
            row, col = divmod(idx, 4)
            x0 = self.MARGIN + col * (tw + gap)
            x1 = x0 + tw
            yy0 = y0 + row * (th + gap)
            yy1 = yy0 + th
            d.rounded_rectangle([x0, yy0, x1, yy1], radius=5,
                                fill=s.white, outline=s.line, width=1)
            # strip ilustrasi kecil di atas (dipendekkan: beri ruang teks)
            self.draw_icon(tile["art"], (x0 + 4, yy0 + 3, x1 - 4, yy0 + 27))
            self._num_badge(x0 + 6, yy0 + 5, tile["num"], small=True)
            ty = yy0 + 30
            f_kick = load_font("sans_bold", 10)
            d.text((x0 + 8, ty), "%s \u00b7 %s" % (tile["place"], tile["kicker"]),
                   font=f_kick, fill=s.red)
            ty += 12
            f_head = load_font("serif_bold", 13)
            for line in wrap_text(tile["headline"], f_head, tw - 16)[:2]:
                d.text((x0 + 8, ty), line, font=f_head, fill=s.ink)
                ty += 14
            f_body = load_font("sans", 10)
            for line in wrap_text(tile["body"], f_body, tw - 16)[:1]:
                d.text((x0 + 8, ty), line, font=f_body, fill=s.ink)
                ty += 11
            # sumber di posisi tetap, jauh di bawah baris body
            f_src = load_font("sans_italic", 9)
            d.text((x0 + 8, yy1 - 11), tile["source"], font=f_src, fill=s.grey)

    # -------------------------------------------------------- map + more --
    def map_and_more(self):
        d = self.draw
        s = self.style
        y0, y1 = 718, 928
        mid = self.MARGIN + 452
        # ---- kiri: peta dunia
        d.rounded_rectangle([self.MARGIN, y0, mid, y1], radius=6,
                            fill=s.white, outline=s.line, width=1)
        f_title = load_font("sans_bold", 13)
        d.text((self.MARGIN + 10, y0 + 8), "WHERE IT HAPPENED",
               font=f_title, fill=s.navy)
        self.draw_map((self.MARGIN + 8, y0 + 30, mid - 8, y1 - 28))
        f_cap = load_font("sans_italic", 10)
        d.text((self.MARGIN + 10, y1 - 22),
               "Red numbers mark stories 1-11.",
               font=f_cap, fill=s.grey)
        # ---- kanan: ALSO ON
        x0 = mid + 12
        x1 = self.W - self.MARGIN
        d.rounded_rectangle([x0, y0, x1, y1], radius=6,
                            fill=s.cream, outline=s.line, width=1)
        d.text((x0 + 10, y0 + 8), "ALSO ON THURSDAY 19 NOVEMBER",
               font=f_title, fill=s.navy)
        f_num = load_font("sans_bold", 11)
        f_txt = load_font("sans", 11)
        ty = y0 + 30
        text_x = x0 + 38
        max_w = x1 - text_x - 8
        for b in BRIEFS:
            num = "%d." % b["num"]
            d.text((x0 + 10, ty), num, font=f_num, fill=s.red)
            # potong aman: buang kata dari ujung isi sampai baris muat
            body = b["text"]
            line = "%s - %s (%s)" % (b["place"], body, b["source"])
            if d.textlength(line, font=f_txt) > max_w:
                words = body.split()
                while (len(words) > 1 and d.textlength(
                        "%s - %s\u2026 (%s)" % (b["place"], " ".join(words),
                                               b["source"]),
                        font=f_txt) > max_w):
                    words.pop()
                line = "%s - %s\u2026 (%s)" % (b["place"], " ".join(words),
                                              b["source"])
            d.text((text_x, ty), line, font=f_txt, fill=s.ink)
            ty += 13
        # garis pemisah halus di bawah judul
        d.line([(x0 + 10, y0 + 26), (x1 - 10, y0 + 26)], fill=s.line, width=1)

    # --------------------------------------------------------- datecheck --
    def datecheck(self):
        d = self.draw
        s = self.style
        y0, y1 = 936, 1024
        d.rectangle([0, y0, self.W, y1], fill=s.navy)
        f_lab = load_font("sans_bold", 12)
        d.text((self.MARGIN, y0 + 8), "DATE CHECK", font=f_lab, fill=s.gold)
        f_head = load_font("sans_bold", 12)
        d.text((self.MARGIN + 96, y0 + 8),
               "LEFT OUT - NOT 19 NOVEMBER NEWS:", font=f_head, fill=s.white)
        f_item = load_font("sans", 11)
        items = "   |   ".join(LEFT_OUT)
        for j, line in enumerate(wrap_text(items, f_item, self.W - 2 * self.MARGIN)):
            d.text((self.MARGIN, y0 + 28 + j * 14), line, font=f_item,
                   fill=(205, 210, 225))
        f_attr = load_font("sans_italic", 10)
        attr = ("Every story here happened, or was first reported, on Thursday "
                "19 November 2026. Sources: Reuters, AP, AFP, BBC, Al Jazeera, "
                "UN News, Euronews, ABC, RNZ, Xinhua, Nature.")
        d.text((self.MARGIN, y1 - 18), attr, font=f_attr, fill=(170, 180, 200))

    # ------------------------------------------------------------- render --
    def render(self):
        self.banner()
        self.subhead()
        self.stats()
        self.features()
        self.tiles()
        self.map_and_more()
        self.datecheck()
        return self.img

    # ------------------------------------------------------------ helpers --
    def _num_badge(self, x, y, num, small=False):
        d = self.draw
        r = 11 if not small else 9
        d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=self.style.red)
        f = load_font("sans_bold", 12 if not small else 10)
        t = str(num)
        tw = d.textlength(t, font=f)
        th = f.size
        d.text((x + r - tw / 2, y + r - th / 2 - 1), t, font=f,
               fill=self.style.white)

    # ------------------------------------------------------- illustrations --
    def draw_summit(self, box):
        """Meja summit + 3 bendera (AS, China, Rusia)."""
        d = self.draw
        x0, y0, x1, y1 = box
        d.rectangle(box, fill=(214, 226, 240))
        # langit + lantai
        d.rectangle([x0, y0, x1, y0 + (y1 - y0) // 2], fill=(140, 175, 210))
        # tiga bendera
        flags = [(196, 30, 38), (222, 41, 16), (255, 255, 255)]
        fw = (x1 - x0) // 5
        for i, col in enumerate(flags):
            fx = x0 + (x1 - x0) // 4 * (i + 1) - fw // 2
            d.rectangle([fx, y0 + 10, fx + fw, y0 + 34], fill=col,
                        outline=(90, 90, 90))
            d.line([(fx + fw // 2, y0 + 34), (fx + fw // 2, y0 + 58)],
                   fill=(60, 60, 60), width=2)
        # meja
        my = y0 + (y1 - y0) * 2 // 3
        d.rectangle([x0 + 14, my, x1 - 14, my + 14], fill=(120, 72, 32))
        d.rectangle([x0 + 22, my + 14, x0 + 34, y1 - 6], fill=(90, 55, 25))
        d.rectangle([x1 - 34, my + 14, x1 - 22, y1 - 6], fill=(90, 55, 25))
        # tiga kursi / kepala
        for cx in (x0 + (x1 - x0) // 4, (x0 + x1) // 2, x0 + 3 * (x1 - x0) // 4):
            d.ellipse([cx - 13, my - 26, cx + 13, my], fill=(240, 210, 180))
            d.rectangle([cx - 16, my, cx + 16, my + 8], fill=(40, 60, 90))

    def draw_court(self, box):
        """Gedung pengadilan + timbangan keadilan."""
        d = self.draw
        x0, y0, x1, y1 = box
        d.rectangle(box, fill=(226, 222, 210))
        # gedung: kolom + atap segitiga
        cx = (x0 + x1) // 2
        d.polygon([(cx - 70, y0 + 34), (cx + 70, y0 + 34), (cx, y0 + 8)],
                  fill=(150, 140, 120))
        d.rectangle([cx - 62, y0 + 34, cx + 62, y1 - 8], fill=(200, 192, 172))
        for i in range(4):
            px = cx - 52 + i * 34
            d.rectangle([px, y0 + 42, px + 14, y1 - 8], fill=(240, 236, 224))
        # timbangan kecil di tengah depan
        sx = cx
        sy = y1 - 34
        d.line([(sx, sy - 22), (sx, sy)], fill=(60, 50, 30), width=2)
        d.line([(sx - 20, sy - 22), (sx + 20, sy - 22)], fill=(60, 50, 30), width=2)
        d.arc([sx - 28, sy - 22, sx - 12, sy - 6], 0, 180, fill=(60, 50, 30), width=2)
        d.arc([sx + 12, sy - 22, sx + 28, sy - 6], 0, 180, fill=(60, 50, 30), width=2)

    def draw_climate(self, box):
        """Globe + termometer."""
        d = self.draw
        x0, y0, x1, y1 = box
        d.rectangle(box, fill=(200, 226, 214))
        cx = (x0 + x1) // 2 - 20
        cy = (y0 + y1) // 2
        r = min((x1 - x0) // 4, (y1 - y0) // 2 - 8)
        # globe
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 220),
                  outline=(30, 90, 140), width=2)
        d.ellipse([cx - r // 2, cy - r // 2, cx, cy], fill=(60, 160, 90))
        d.ellipse([cx + r // 4, cy + r // 4, cx + r // 2, cy + r // 2],
                  fill=(60, 160, 90))
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
        # termometer
        tx = x1 - 34
        d.rounded_rectangle([tx - 6, y0 + 12, tx + 6, y1 - 18], radius=6,
                            fill=(255, 255, 255), outline=(150, 40, 40), width=2)
        d.ellipse([tx - 12, y1 - 30, tx + 12, y1 - 6], fill=(200, 40, 40))
        d.rectangle([tx - 3, y0 + 22, tx + 3, y1 - 20], fill=(220, 60, 60))
        # matahari kecil
        d.ellipse([x0 + 14, y0 + 12, x0 + 34, y0 + 32], fill=(255, 200, 60))

    def draw_map(self, box):
        """Peta dunia sederhana: benua sebagai poligon + titik merah bernomor."""
        d = self.draw
        s = self.style
        x0, y0, x1, y1 = box
        d.rectangle(box, fill=(222, 232, 240))
        w, h = x1 - x0, y1 - y0
        # benua (koordinat relatif 0-100 x 0-60)
        continents = [
            [(6, 12), (20, 8), (26, 16), (18, 24), (8, 22)],       # N Amerika
            [(24, 30), (32, 28), (34, 40), (28, 46), (23, 36)],    # S Amerika
            [(46, 10), (56, 8), (58, 18), (50, 20), (45, 14)],     # Eropa
            [(46, 24), (58, 22), (62, 34), (52, 42), (46, 32)],    # Afrika
            [(62, 8), (82, 6), (90, 16), (78, 26), (64, 20)],      # Asia
            [(82, 42), (92, 40), (94, 48), (84, 50)],              # Oseania
        ]
        for poly in continents:
            pts = [(x0 + px * w / 100, y0 + py * h / 60) for px, py in poly]
            d.polygon(pts, fill=(150, 190, 140), outline=(90, 140, 90))
        # garis khatulistiwa putus-putus
        for gx in range(x0, x1, 12):
            d.line([(gx, y0 + h // 2), (gx + 6, y0 + h // 2)], fill=(160, 160, 160), width=1)
        # pin bernomor 1-11
        pins = [
            (1, 78, 12), (2, 50, 14), (3, 74, 10), (4, 55, 14), (5, 66, 20),
            (6, 80, 16), (7, 58, 10), (8, 40, 8), (9, 18, 18), (10, 55, 30),
            (11, 30, 34),
        ]
        f_pin = load_font("sans_bold", 9)
        for num, px, py in pins:
            cx = x0 + px * w / 100
            cy = y0 + py * h / 60
            d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=s.red,
                      outline=s.white, width=1)
            t = str(num)
            tw = d.textlength(t, font=f_pin)
            d.text((cx - tw / 2, cy - 5), t, font=f_pin, fill=s.white)

    def draw_icon(self, kind, box):
        """Ikon kecil untuk strip atas tiap ubin."""
        d = self.draw
        x0, y0, x1, y1 = box
        palettes = {
            "bridge": (200, 220, 240), "missile": (240, 210, 200),
            "storm": (210, 215, 235), "court": (226, 222, 210),
            "ice": (215, 235, 245), "chart": (210, 235, 215),
            "game": (235, 215, 240), "march": (240, 230, 200),
        }
        d.rectangle(box, fill=palettes.get(kind, (230, 230, 230)))
        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2
        if kind == "bridge":
            d.line([(x0 + 6, cy + 6), (x1 - 6, cy + 6)], fill=(60, 60, 90), width=2)
            d.arc([cx - 18, cy - 12, cx + 18, cy + 12], 180, 360, fill=(60, 60, 90), width=2)
            d.line([(x0 + 14, cy - 10), (x0 + 14, cy + 6)], fill=(60, 60, 90), width=2)
            d.line([(x1 - 14, cy - 10), (x1 - 14, cy + 6)], fill=(60, 60, 90), width=2)
        elif kind == "missile":
            d.polygon([(cx, y0 + 3), (cx + 7, cy), (cx - 7, cy)], fill=(150, 40, 40))
            d.rectangle([cx - 7, cy, cx + 7, y1 - 4], fill=(120, 30, 30))
            d.line([(cx - 12, y1 - 4), (cx - 6, y1 - 8)], fill=(200, 120, 40), width=2)
            d.line([(cx + 12, y1 - 4), (cx + 6, y1 - 8)], fill=(200, 120, 40), width=2)
        elif kind == "storm":
            d.ellipse([cx - 14, cy - 8, cx + 2, cy + 8], fill=(120, 140, 180))
            d.ellipse([cx - 2, cy - 10, cx + 14, cy + 6], fill=(90, 110, 160))
            d.line([(cx - 6, cy + 8), (cx - 12, y1 - 3)], fill=(240, 200, 60), width=2)
            d.line([(cx + 4, cy + 8), (cx - 2, y1 - 3)], fill=(240, 200, 60), width=2)
        elif kind == "court":
            d.polygon([(cx - 16, cy - 4), (cx + 16, cy - 4), (cx, cy - 12)],
                      fill=(150, 140, 120))
            d.rectangle([cx - 13, cy - 4, cx + 13, cy + 8], fill=(200, 192, 172))
        elif kind == "ice":
            d.polygon([(cx - 14, cy + 8), (cx - 8, cy - 10), (cx, cy + 4),
                       (cx + 8, cy - 10), (cx + 14, cy + 8)], fill=(200, 230, 245),
                      outline=(120, 170, 200))
        elif kind == "chart":
            pts = [(x0 + 8, cy + 6), (cx - 8, cy - 4), (cx + 2, cy + 2),
                   (x1 - 8, cy - 8)]
            d.line(pts, fill=(40, 140, 60), width=2)
            for px, py in pts:
                d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(40, 140, 60))
        elif kind == "game":
            d.rounded_rectangle([cx - 16, cy - 8, cx + 16, cy + 8], radius=5,
                                fill=(90, 60, 120))
            d.ellipse([cx - 9, cy - 3, cx - 3, cy + 3], fill=(255, 255, 255))
            d.ellipse([cx + 3, cy - 3, cx + 9, cy + 3], fill=(255, 200, 60))
        else:  # march
            for i, px in enumerate((cx - 14, cx, cx + 14)):
                d.ellipse([px - 4, cy - 10, px + 4, cy - 2], fill=(60, 60, 90))
                d.rectangle([px - 3, cy - 2, px + 3, cy + 9], fill=(60, 60, 90))
                d.line([(px - 8, cy - 12), (px + 8, cy - 12)], fill=(180, 40, 40), width=2)
                d.line([(px, cy - 12), (px, cy - 2)], fill=(120, 40, 40), width=1)


def build_poster():
    """Render poster lengkap, kembalikan PIL Image."""
    return Poster().render()
