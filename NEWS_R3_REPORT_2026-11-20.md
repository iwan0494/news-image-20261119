# News-image 20261119 — R3 REPORT (ronde 3, target TOP 10)

**Ditulis:** 2026-11-20 ~09:25 WIB, oleh subagent Muse (sesi ini).
**Tujuan:** ronde 3 news-image-20261119, dari spec `NEWS_R3_SPEC_2026-11-20.md` (Wowo).
Deadline submit Sabtu 2026-11-21 07:00 WIB.

## Konfirmasi penting

Saya **TIDAK membaca file lama apa pun** — tidak `main.py`, tidak `render_poster.py`,
tidak `poster-20261119.png`, tidak satu pun file .md lama (NEWS_FIX_SPEC,
NEWS_FIX_REPORT, NEWS_FIX_2026-11-19, NEWS_MAINPY_2026-11-19), tidak repo
20261118. Satu-satunya sumber yang saya baca adalah `NEWS_R3_SPEC_2026-11-20.md`.
File lama saya hapus (`rm main.py render_poster.py poster-20261119.png`) sebelum
menulis yang baru, tanpa membacanya. File lain di repo (README, LICENSE, laporan
.md lama, folder top/) tidak saya ubah. Tidak ada file scratch di repo (uji hanya
di /tmp/outA dan /tmp/outB).

## Putaran 1 — tulis fresh dari spec

Arsitektur R3 (beda total dari Level Eclipse yang menyalin PNG pra-render):
`main.py` me-render poster dari nol setiap kali dijalankan.

**`stories.py`** (6.842 byte) — data berita sebagai list of dict (bukan tuple):
`FEATURES` (3 dict), `TILES` (8 dict + 1 cadangan `TILES_EXTRA`), `BRIEFS` (14 dict),
`STATS` (6 dict), `REGIONS` (7 string), `LEFT_OUT` (7 string), `ATTRIBUTION`.
Semua teks ditulis dengan kata-kata sendiri dari fakta spec.

**`poster.py`** (25.270 byte) — mesin layout sebagai class `Poster` (Image +
ImageDraw) + dataclass `Style`. Method: `banner()`, `subhead()`, `regions()`,
`stats()`, `features()`, `tiles()`, `map_and_more()`, `datecheck()`,
`attribution()`, `render()`. Helper `load_font` (cache dict, cari DejaVu di path
sistem, fallback `load_default`), `wrap_text`, dan gambar dari primitif PIL:
`draw_summit()` (meja + 3 tokoh + 3 bendera + pelat nama TRUMP/XI/PUTIN),
`draw_court()` (gedung + timbangan + lencana 9–6), `draw_climate()` (globe +
termometer), `draw_map()` (6 benua sebagai poligon + 11 pin merah bernomor),
`draw_icon(kind)` (8 ikon ubin: bridge, missile, cyclone, gavel, glacier,
chart, game, strike; + runner cadangan).

**`main.py`** (1.565 byte) — memakai `pathlib` + `argparse` (`--out` opsional),
output dari `MAKEFUN_OUTPUT_DIR` (default `/output`) ke `entry.png`. Setelah
menulis, verifikasi file ada dan ≤ 1 MiB, lalu cetak ukuran + sha256. Gagal →
stderr + `sys.exit(1)`.

**Verifikasi putaran 1 (semua lolos):**
- `ast.parse` lolos untuk ketiga file.
- Determinisme (2 run, 2 dir /tmp berbeda): kedua `entry.png` **byte-identik**,
  sha256 `fc062a4213098f917f56013f82c640435348cd57e35eceb339c16c076dc65224`.
- Poster: 1024×1024, RGB, 159.012 byte (≤ 1 MiB).
- **Lihat langsung poster putaran 1 — ditemukan 4 cacat nyata** (inilah yang
  diperbaiki putaran 2): (1) teks ringkasan ubin menabrak baris sumber di
  bawahnya; (2) daftar ALSO ON terpotong parah ("…") karena 2 kolom sempit;
  (3) footer DATE CHECK terpotong — item ke-7 hilang; (4) ringkasan fitur
  terpotong di tengah kalimat (max 2 baris, teks terlalu panjang).

## Putaran 2 — revisi nyata (pesan terpisah, setelah putaran 1 terverifikasi)

Revisi dilakukan sebagai langkah edit terpisah pada **dua file** (`poster.py` +
`stories.py`), mengubah layout/spasi/nilai — bukan komentar:

**`poster.py`** (25.270 → 24.973 byte):
- `tiles()`: strip ilustrasi 40 → 32px; headline 13 → 12px; ringkasan 11 → 10px;
  posisi kicker/headline/ringkasan/sumber dirapatkan ulang; baris ubin mulai
  y=518 (dari 524).
- `features()`: tinggi panel 254 → 248px (y1 516 → 510).
- `map_and_more()`: daftar ALSO ON diubah dari 2 kolom × 7 baris menjadi
  **satu kolom 14 baris** (tiap brief satu baris penuh, tidak terpotong lagi);
  y0/y1 758/936 → 754/934.
- `datecheck()`: label pindah ke baris sendiri, daftar item di dua baris
  selebar penuh (y0/y1 942/986 → 940/988) — ketujuh item kini tampil.
- `draw_map()`: radius pin 7 → 6; pin Antalya (30,37) → (28,35) dan Crimea
  (34,45) → (37,47) supaya tidak saling menutup.

**`stories.py`** (6.842 → 6.647 byte): ringkasan fitur 1 dan 2 dipersingkat
supaya muat 2 baris utuh; keenam ringkasan ubin dipersingkat supaya muat 1
baris utuh (mis. "Third strike in a week halts trains to Russia." →
"Third strike in a week halts trains."); tiga brief terpanjang dipersingkat
(Gaza, London, Frankfurt).

**Verifikasi putaran 2 (semua lolos):**
- `ast.parse` lolos untuk ketiga file.
- Determinisme (2 run, 2 dir /tmp berbeda): kedua `entry.png` **byte-identik**,
  sha256 `7770a50c6d30f34064b107bb215ab8292f8d0055dbb123291711132e177b47bf`
  (BERBEDA dari putaran 1 — revisi mengubah poster).
- Poster final: **1024×1024, RGB, 170.752 byte (≤ 1 MiB)**,
  sha256 `7770a50c6d30f34064b107bb215ab8292f8d0055dbb123291711132e177b47bf`.
- **Lihat langsung poster final — semua tampil:** banner navy + tanggal besar +
  lencana 33 STORIES; subhead 3 cerita; garis wilayah; strip 6 statistik;
  3 panel fitur bergambar (summit/court/climate) dengan ringkasan utuh +
  sumber; 8 ubin bergambar dengan ringkasan + sumber tanpa tumpang tindih;
  peta dunia + 11 pin bernomor; daftar ALSO ON 14 brief lengkap satu baris
  tiap brief; footer DATE CHECK dengan ketujuh item LEFT OUT (termasuk
  "18 NOV: Iran fires on Kuwait and Bahrain" yang sengaja dikeluarkan);
  baris atribusi. Tidak ada teks tumpang tindih, terpotong, atau ruang kosong
  besar — halaman terisi penuh dari atas sampai bawah.

## Catatan untuk Wowo (saat bundle + submit)

- Bundle **wajib** menyertakan sesi ini via `--session` (sesi subagent ini yang
  menulis ketiga file dalam dua putaran).
- Poster final sha256 `7770a50c…` — beda dari putaran 1 `fc062a42…` dan dari
  poster Level Eclipse `8eb45951…`.
- File baru di repo: `main.py`, `poster.py`, `stories.py`,
  `NEWS_R3_REPORT_2026-11-20.md` (laporan ini). Tidak ada PNG pra-render di
  repo — `main.py` me-render saat jalan.
- Saya tidak commit/push/submit.
