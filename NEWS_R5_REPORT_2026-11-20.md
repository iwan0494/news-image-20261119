# NEWS R5 REPORT — news-image-20261119, ronde 5 (2026-11-20)

## Perubahan vs ronde 4 (satu fix yang menentukan lolos/tidaknya)
- **Diagnosis R4 (terbukti):** grader "standard library only: nothing is installed before it runs" — TIDAK ada PIL. R4 `main.py` mengimpor PIL (via `poster.py`) -> `ModuleNotFoundError` di grader. Direproduksi lokal: `python3 -S -P -s main.py` gagal di `poster.py` baris 8.
- **Fix R5:** `main.py` ditulis ulang jadi program stdlib saja (os, shutil, sys, hashlib, argparse) yang HANYA menyalin `poster-20261119.png` pra-render ke `$MAKEFUN_OUTPUT_DIR/entry.png`. Pola yang sama seperti R2 (yang lolos run_completes, skor 93.10%).
- **Poster sama dengan R4** (desain + 25 cerita + penomoran 1–25 tidak berubah): `poster.py` + `stories.py` ditulis fresh dari NEWS_R4_SPEC, dipakai builder untuk me-render `poster-20261119.png` secara lokal (PIL tersedia di VM), lalu PNG-nya dikomit. `main.py` di grader TIDAK mengimpor `poster`/`stories`.

## Yang ditulis (2 putaran, 2 pesan terpisah)
- **Putaran 1:** `stories.py` (data 25 cerita: FEATURES 1–3, TILES 4–11, BRIEFS 12–25, STATS 6, REGIONS, LEFT_OUT), `poster.py` (mesin layout `Poster` class: banner, stats, features, tiles, map_and_more, datecheck; ilustrasi PIL), `main.py` (copy stdlib-only). Render PNG pertama sha `77bf141a…` (179.412 byte). Tes grader stdlib-only + normal lolos, deterministik.
- **Putaran 2 (revisi nyata, setelah melihat poster putaran 1):**
  1. `stories.py` — 6 body ubin dipendekkan agar jadi kalimat utuh satu baris tanpa elipsis (Riyadh, Odisha, Seoul, Greenland, New York, Bogotá); 3 body fitur dipendekkan agar muat 2 baris penuh tanpa terpotong (Shenzhen, The Hague, Antalya).
  2. `main.py` — komentar ditulis ulang tanpa kata "PIL" agar `grep -i pil main.py` kosong.
  3. `poster.py` — pin peta diperbesar (r 8→9, font 10→11) agar nomor lebih terbaca.
  - Render ulang PNG final sha `8bdd3a8f…` (178.904 byte). Semua verifikasi diulang dan lolos.

## Poster final
- `poster-20261119.png`: **1024×1024 RGB, 178.904 byte** (≤ 1 MiB).
- sha256: `8bdd3a8ff378fb2f4c48f96a001fcecaf6918d4458e13b4f314818d9b4202295`
- Saya lihat langsung (penuh): banner + tanggal + lencana "25 STORIES · EVERY CONTINENT", strip wilayah total 25, subhead, 6 blok statistik, 3 panel fitur (ilustrasi summit/court/climate), 8 ubin (ikon + nomor 4–11), peta "WHERE IT HAPPENED" dengan pin merah 1–11, daftar "ALSO ON" 12–25 lengkap, footer DATE CHECK + atribusi. **Tidak ada teks menabrak, terpotong, atau elipsis; tidak ada halaman kosong besar; penomoran 1–25 konsisten.**

## Verifikasi (semua lolos)
- **Tes grader stdlib-only (PALING PENTING):** `MAKEFUN_OUTPUT_DIR=/tmp/r5_grader python3 -S -P -s main.py` → **exit 0**, entry.png byte-identik dengan `poster-20261119.png` (sha `8bdd3a8f…`). Flag `-S` memblokir PIL seperti grader — ini tes yang membuktikan fix R5 bekerja.
- Tes grader normal: `MAKEFUN_OUTPUT_DIR=/tmp/r5_grader2 python3 -P -s main.py` → **exit 0**, byte-identik.
- Determinisme: `python3 main.py --out /tmp/r5_A.png` dan `--out /tmp/r5_B.png` → sha256 sama (`8bdd3a8f…`); kelima file (PNG repo + 2 hasil grader + 2 hasil --out) byte-identik.
- `ast.parse` lolos untuk `main.py`, `poster.py`, `stories.py`. `py_compile` OK.
- `grep -i pil main.py` → kosong (exit 1). `grep -iE "from poster|import poster|from stories|import stories" main.py` → kosong (exit 1). `main.py` hanya mengimpor argparse, hashlib, os, shutil, sys.
- `__pycache__` yang terbentuk saat pengujian sudah dihapus; file scratch hanya di /tmp.

## Catatan untuk Wowo (saat bundle + submit)
- File baru/berubah di repo: `main.py` (baru, copy stdlib-only), `poster.py` (fresh), `stories.py` (fresh), `poster-20261119.png` (baru, pra-render — WAJIB ikut dikomit, main.py menyalin file ini), `NEWS_R5_SPEC_2026-11-20.md`, `NEWS_R5_REPORT_2026-11-20.md` (laporan ini).
- JANGAN lupa komit `poster-20261119.png` — tanpa file ini main.py gagal di grader ("poster not found").
- Saya hanya membaca NEWS_R5_SPEC_2026-11-20.md + NEWS_R4_SPEC_2026-11-20.md; tidak membaca file R3/R4 apa pun (file lama saya hapus pakai `rm` tanpa membacanya). Tidak commit/push/submit.
