# NEWS-IMAGE 20261119 — R4 REPORT (ronde 4, "The World in One Day")

**Ditulis:** 2026-11-20 ~13:30 WIB, oleh builder/reviser ronde 4.
**Tujuan:** ronde 4 news-image-20261119, target TOP 10. Deadline submit Sabtu 2026-11-21 07:00 WIB.
**Konfirmasi:** saya TIDAK membaca file lama ronde 3 atau file lama lainnya (main.py/poster.py/stories.py ronde 3, render_poster.py, poster PNG lama). Saya hanya membaca spec `NEWS_R4_SPEC_2026-11-20.md` dan ketiga file R4 putaran 1 (revisi atas karya putaran 1, diizinkan). File lama ronde 3 sudah dihapus putaran 1 dengan `rm` tanpa dibaca.

## Putaran 1 — ringkasan (selesai + terverifikasi)

- Menulis fresh dari spec: `stories.py` (25 cerita: FEATURES 3, TILES 8, BRIEFS 14, STATS 6, REGIONS total 25, LEFT_OUT 7), `poster.py` (`Poster` class + `Style` dataclass + `load_font` + helper gambar), `main.py` (bootstrap `sys.path` PALING ATAS sebelum impor `poster`, `build()` pakai argparse `--out`, output dari `MAKEFUN_OUTPUT_DIR`).
- Verifikasi putaran 1: tes grader `MAKEFUN_OUTPUT_DIR=/tmp/grader_out python3 -P -s main.py` exit 0; determinisme byte-identik; poster 1024×1024 RGB, 174.502 byte, sha256 `43d9b77c2e456019ad784665687b8b14ed787ead1d7949507581ff55f54e6cec`; `ast.parse` lolos.
- Cacat yang saya temukan saat melihat poster putaran 1 (diperbaiki di putaran 2, lihat bawah): (1) body baris ke-2 menabrak sumber di 3 panel fitur; (2) body menabrak sumber di 8 ubin; (3) brief ALSO ON terpotong di tepi kanan (Canberra, Gaza, Frankfurt).

## Putaran 2 — perubahan (revisi NYATA, dua file)

### poster.py — spasi vertikal panel fitur (cacat 1)
- Ilustrasi panel dipendekkan dari 52% menjadi 46% tinggi panel (`art_h = int((y1 - y0) * 0.46)`), memberi ruang teks di bawah.
- Jarak setelah ilustrasi 10 → 8; jarak setelah kicker 18 → 17; tinggi baris headline 23 → 22; jeda sebelum body 2 → 3; tinggi baris body 15 → 14.
- Sumber dipindah dari `y1 - 20` ke `y1 - 16` (posisi tetap di bawah).
- Hasil hitung: body baris ke-2 berakhir y≈475, sumber di y=484 — jarak 9px, tidak menabrak.

### poster.py — spasi vertikal ubin (cacat 2)
- Strip ilustrasi dipendekkan (yy0+4–yy0+30 → yy0+3–yy0+27); teks mulai yy0+34 → yy0+30.
- Jarak setelah kicker 14 → 12; tinggi baris headline 15 → 14; tinggi baris body 12 → 11.
- Sumber dipindah dari `yy1 - 13` ke `yy1 - 11` (posisi tetap di bawah).
- Hasil hitung: body berakhir ≈yy0+80, sumber di yy0+85 — jarak 5px, tidak menabrak.

### poster.py — potong aman ALSO ON (cacat 3, jaring pengaman)
- Baris brief kini diukur dengan `textlength` terhadap lebar tersedia (`max_w = x1 - text_x - 8` ≈ 482px). Kalau baris kepanjangan, kata dibuang dari ujung isi sampai muat, lalu diberi elipsis "…" — jadi tidak ada lagi teks yang terpotong di tepi kanan.

### stories.py — pendekkan 5 brief terpanjang (cacat 3, perbaikan isi)
- Gaza 12: "Israeli tanks cross the Yellow Line in a rare raid; Hamas calls it a truce breach." → "Israeli tanks cross the Yellow Line; Hamas calls it a truce breach."
- London 13: "Van Gogh sells for a record $190.4m after a row over its Nazi history." → "Van Gogh sells for a record $190.4m despite its Nazi history."
- Canberra 15: "Three people killed and four groups hit by fresh sanctions over West Bank settlers." → "Three killed, four groups sanctioned over West Bank settlers."
- Mogadishu 16: "Somalia accuses the UAE of secret military bases on its soil." → "Somalia accuses UAE of secret bases on its soil."
- Frankfurt 17: "Deutsche Bank handled $582m in Epstein-linked deals, the FT reports." → "Deutsche Bank handled $582m in Epstein-linked deals."
- Hasil ukur: semua 14 baris brief ≤ 442px (batas 482px) — jaring pengaman elipsis tidak sampai terpicu.

### stories.py — pendekkan 8 body ubin (temuan saat verifikasi putaran 2)
- Saat mengukur, SEMUA 8 body ubin ternyata lebih lebar dari 226px sehingga terpotong di tengah kalimat (mis. "halts rail traffic to", "priced at $83 a"). Saya pendekkan semuanya agar muat satu baris utuh (hasil ukur: 150–221px, batas 226px):
- Crimea: "Third attack in a week halts rail to Russia." / Riyadh: "Debris falls on the capital; no casualties." / Odisha: "100,000 evacuated ahead of Friday landfall." / Seoul: "Martial-law verdict on ex-PM Han void." / Greenland: "Parliament backs Greenland pact 109-0." / New York: "Record $81bn IPO, priced at $83 a share." / Worldwide: "Midnight launch draws praise." / Bogotá: "Marches in three cities oppose reform."

## Verifikasi putaran 2 — semua lolos

- **TES GRADER (wajib):** `MAKEFUN_OUTPUT_DIR=/tmp/grader_out python3 -P -s main.py` → **exit 0**, menghasilkan `entry.png` yang benar. Fix `sys.path` tetap bekerja setelah revisi.
- **Determinisme:** `python3 main.py --out /tmp/outA.png` dan `--out /tmp/outB.png` byte-identik dengan hasil tes grader.
- **Poster final:** 1024×1024, RGB, **172.452 byte** (≤ 1 MiB), sha256 **`153a2df283d38eeb7d5cf628b8bc897a119b36318f94ddcfeb6d9392417da046`**.
- **ast.parse:** lolos untuk `main.py`, `poster.py`, `stories.py`.
- **Ukur lebar teks:** semua body ubin ≤ 221px (batas 226px); semua baris brief ≤ 442px (batas 482px).
- **LIHAT poster langsung (final):** banner + tanggal + badge "25 STORIES · EVERY CONTINENT" + strip wilayah (total 25) + subhead + strip statistik 6 blok + 3 panel fitur + 8 ubin + peta + daftar ALSO ON 12–25 + footer DATE CHECK — semua tampil. **Ketiga cacat HILANG:** (1) body dan sumber di 3 panel fitur terpisah jelas; (2) body dan sumber di 8 ubin terpisah jelas, tiap body kini kalimat utuh satu baris; (3) semua 14 brief ALSO ON tampil utuh, tidak ada yang terpotong di tepi kanan. Penomoran 1–25 konsisten, tidak ada teks tumpang tindih, tidak ada halaman kosong besar.

## Serah terima

Poster final siap diserahkan ke Wowo untuk commit/push/submit ronde 4. Saya tidak commit, push, atau submit. File scratch hanya di /tmp (outA/outB/grader_out + crop pemeriksaan); tidak ada file scratch di repo.
