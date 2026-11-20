# News-image 20261119 — R3 FIXUP (perbaikan hitungan 33 → 25)

**Ditulis:** 2026-11-20 ~09:20 WIB, oleh subagent Muse (sesi ini).
**Tugas:** perbaiki inkonsistensi hitungan pada poster final R3 (sha256 `7770a50c…`) —
lencana + strip wilayah mengklaim 33 cerita, padahal yang tampil cuma 25
(3 fitur + 8 ubin + 14 brief), dan penomoran melompat dari 11 ke 13 (nomor 12 hilang).

## Yang saya baca

Hanya `NEWS_R3_REPORT_2026-11-20.md` dan `NEWS_R3_SPEC_2026-11-20.md`, plus
`stories.py` dan `poster.py` — hanya untuk menemukan string yang diubah.
Tidak membaca file lama lain (main.py lama, render_poster.py, poster-20261119.png,
file .md lama). Tidak ada cerita yang ditambah/dikurangi — hanya angka/label.

## Perubahan (4 edit)

1. **Lencana banner** `33 STORIES · EVERY CONTINENT` → `25 STORIES · EVERY CONTINENT`.
   Catatan: string ini ternyata ada di `poster.py` (baris 370, method `banner()`),
   bukan di `stories.py` seperti tertulis di tugas — diubah di tempatnya yang benar.
2. **`stories.py` — REGIONS** menjadi `ASIA 3 · MIDDLE EAST 2 · EUROPE 6 · AFRICA 4 ·
   AMERICAS 6 · OCEANIA 2 · GLOBAL 2` (jumlah = 25). Pemetaan: Asia = Shenzhen/Odisha/
   Seoul; Middle East = Riyadh/Gaza; Europe = Hague/Antalya/Crimea/London/Frankfurt/Rome;
   Africa = Mogadishu/Sudan/Pretoria/Canaries; Americas = Greenland/New York/Bogotá/
   Mexico City/Washington/Florida; Oceania = Canberra/Wellington; Global = GTA/Space.
3. **`stories.py` — BRIEFS** penomoran 13–26 → **12–25** (12=Gaza, 13=London,
   14=Mexico City, 15=Canberra, 16=Mogadishu, 17=Frankfurt, 18=Washington, 19=Rome,
   20=Sudan, 21=Pretoria, 22=Canaries, 23=Florida, 24=Wellington, 25=Space).
   Urutan dan isi brief TETAP sama, hanya nomornya.
4. **`poster.py` — caption peta** (baris 503) `Red numbers mark stories 1–12` →
   `Red numbers mark stories 1–11` (pin peta menandai 11 cerita fitur+ubin).

## Verifikasi (semua lolos)

- `ast.parse` lolos untuk `stories.py`, `poster.py`, `main.py`.
- Determinisme: `python3 main.py --out /tmp/r3fixA` dan `--out /tmp/r3fixB` —
  kedua file **byte-identik**, sha256
  `ca3a2d3b550acc34f8e409df38afb64e3b94508e712c05cdd3f69c89e8565104`
  (BERBEDA dari `7770a50c…` — perubahan masuk ke poster).
- Poster: **1024×1024, RGB, 170.883 byte (≤ 1 MiB)**.
- **Lihat langsung poster baru — semua konsisten:**
  - lencana kanan atas: "25 STORIES · EVERY CONTINENT";
  - strip wilayah: ASIA 3 · MIDDLE EAST 2 · EUROPE 6 · AFRICA 4 · AMERICAS 6 ·
    OCEANIA 2 · GLOBAL 2 = 25;
  - fitur 1–3 + ubin 4–11 + brief 12–25 = 25 cerita, penomoran berurutan tanpa lompatan;
  - caption peta: "Red numbers mark stories 1–11";
  - tidak ada teks tumpang tindih atau terpotong; halaman terisi penuh.

## Catatan untuk Wowo (saat bundle + submit)

- Poster final baru sha256 `ca3a2d3b…` (bukan lagi `7770a50c…`).
- Perubahan ini HANYA angka/label — isi cerita, desain, dan kode tidak berubah.
  Bundle tetap memakai sesi R3 (yang menulis ketiga file dalam dua putaran);
  fixup ini sesi terpisah yang hanya mengedit 4 string.
- Saya tidak commit/push/submit.
