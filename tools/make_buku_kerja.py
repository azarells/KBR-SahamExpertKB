# -*- coding: utf-8 -*-
"""Buku Kerja: panduan mengerjakan proyek langkah demi langkah dari awal sampai akhir -> PDF."""
import json, os, sys, subprocess, tempfile, html
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
SCR = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp()
import kb_geo as G
E = html.escape

CSS = """@page{size:A4;margin:15mm 14mm 17mm 14mm}
body{font-family:'DejaVu Sans',Arial;font-size:9.5pt;color:#1d2433;line-height:1.5}
h1{font-size:21pt;color:#0b3d6e;margin:0 0 4px}.sub{color:#555}
h2{font-size:13.5pt;color:#fff;background:#0b3d6e;padding:6px 10px;margin:20px 0 8px;break-after:avoid}
h2.pb{break-before:page;margin-top:0}
h3{font-size:11pt;color:#0b3d6e;margin:12px 0 4px;break-after:avoid;border-bottom:1px solid #c9d3e0;padding-bottom:2px}
table{border-collapse:collapse;width:100%;font-size:8.2pt;margin:6px 0 10px}
th{background:#174f86;color:#fff;padding:4px 6px;text-align:left}td{border-bottom:1px solid #d6dbe3;padding:3px 6px;vertical-align:top}
tr{break-inside:avoid}tr:nth-child(even) td{background:#f5f7fb}
.box{border:3px solid #0b3d6e;padding:14px;margin-bottom:10px}
.tip{background:#e9f6ee;border:1px solid #8fcca5;padding:7px 10px;border-radius:4px;margin:8px 0;break-inside:avoid}
.warn{background:#fff3e0;border:1px solid #f0b36b;padding:7px 10px;border-radius:4px;margin:8px 0;break-inside:avoid}
.ok{background:#eef3fb;border:1px solid #9fb6d8;padding:7px 10px;border-radius:4px;margin:8px 0;break-inside:avoid}
.s{border-left:4px solid #e0a100;background:#f7f9fc;padding:5px 10px;margin:4px 0;break-inside:avoid}
.n{display:inline-block;background:#e0a100;color:#fff;border-radius:50%;min-width:20px;height:20px;text-align:center;line-height:20px;margin-right:6px;font-size:8pt;font-weight:bold}
code{background:#eef1f6;padding:0 3px;border-radius:3px;font-size:8.3pt;font-family:'DejaVu Sans Mono',monospace}
pre{background:#1e2635;color:#e8edf5;padding:8px 10px;border-radius:4px;font-size:8.1pt;white-space:pre-wrap;break-inside:avoid;font-family:'DejaVu Sans Mono',monospace}
.tag{display:inline-block;font-size:7.5pt;font-weight:bold;padding:1px 6px;border-radius:8px;margin-right:4px}
.ta{background:#dce9f7;color:#0b5fa5}.tb{background:#f6e1ee;color:#a0407a}.tab{background:#e2f2e8;color:#2f7a50}
.cek{font-size:8.5pt;color:#2f7a50}
.toc td{border:none;padding:1px 6px}"""

H = []; w = H.append
def S(i, t):  # langkah bernomor
    w(f"<div class='s'><span class='n'>{i}</span>{t}</div>")
def steps(lst, start=1):
    for i, t in enumerate(lst, start): S(i, t)
TA, TB, TAB = "<span class='tag ta'>Peran A · Jonnathan</span>", "<span class='tag tb'>Peran B · Gloria</span>", "<span class='tag tab'>A + B</span>"

w(f"<!doctype html><html lang='id'><head><meta charset='utf-8'><style>{CSS}</style></head><body>")
w("<div class='box'><h1>Buku Kerja Proyek SahamExpertKB v2</h1><div class='sub'>Panduan mengerjakan langkah demi langkah dari awal sampai akhir: instalasi → data → membangun knowledge base → reasoning → pengujian → deployment → laporan & presentasi<br>Kelompok 9 KBR · Jonnathan Azarel Gunawan (L0224005) · Gloria Dana Praysilia (L0224043)</div></div>")
w("<div class='ok'><b>Cara memakai buku ini.</b> Kerjakan berurutan dari Tahap 0. Setiap tahap punya: <b>tujuan</b>, <b>siapa</b> (Peran A/B), <b>langkah bernomor</b>, dan <b>✔ tanda selesai</b> — jangan lanjut sebelum tanda selesai tercapai. Centang statusnya di sheet <code>CHECKLIST_TUGAS</code> pada <code>Template_Data_Emiten.xlsx</code>. Untuk konsep (apa itu kelas, SWRL, data mengalir ke mana) baca <i>Panduan Lengkap Proyek</i>; buku ini fokus pada <b>cara mengerjakan</b>.</div>")
w("<table class='toc'>" + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td style='color:#666'>{c}</td></tr>" for a, b, c in [
 ("Tahap 0", "Target akhir & pembagian kerja", "Hari 1"),
 ("Tahap 1", "Instalasi alat (Windows / macOS)", "Hari 1–2"),
 ("Tahap 2", "Uji jalan pertama: knowledge base yang sudah ada", "Hari 2"),
 ("Tahap 3", "Mengumpulkan data emiten (per kolom: sumber & rumus)", "Minggu 1–2"),
 ("Tahap 4", "Memperbarui berita, makro, kondisi pasar, tanggal acuan", "Minggu 1–2"),
 ("Tahap 5", "Validasi data & build ulang", "Minggu 2"),
 ("Tahap 6", "Membedah & menjalankan KB di Protégé (Pellet, DL Query, SWRLTab)", "Minggu 3"),
 ("Tahap 7", "Kalibrasi pengetahuan pakar & menambah aturan SWRL", "Minggu 3–4"),
 ("Tahap 8", "Pengujian: competency questions, uji teknis, validasi pakar", "Minggu 4–5"),
 ("Tahap 9", "Deployment Apache Jena Fuseki (SPARQL & what-if)", "Minggu 5"),
 ("Tahap 10", "Laporan akhir, slide, dan skrip demo", "Minggu 5–6"),
 ("Tahap 11", "Pemeliharaan & pengumpulan", "Minggu 6"),
 ("Lampiran", "Masalah umum & solusinya · daftar ID peristiwa · form validasi pakar", "")]) + "</table>")

# ---------------- TAHAP 0
w("<h2>Tahap 0 — Target Akhir & Pembagian Kerja</h2>")
w("<p><b>Tujuan:</b> berdua sepakat apa yang harus jadi di akhir, dan siapa mengerjakan apa.</p>")
w("<h3>Yang harus diserahkan di akhir proyek</h3><table><tr><th>#</th><th>Deliverable</th><th>File</th><th>PIC</th></tr>"
  "<tr><td>1</td><td>Ontologi OWL berisi knowledge base + aturan SWRL, konsisten di Pellet</td><td><code>output/SahamExpertKB_v2.owl</code></td><td>A</td></tr>"
  "<tr><td>2</td><td>Data terbaru 64 emiten + berita + makro dengan sumber tercatat</td><td><code>data/*.csv</code> + log sumber</td><td>B</td></tr>"
  "<tr><td>3</td><td>Hasil prediksi sektor 1–3 tahun & top-3 emiten per sektor</td><td><code>LAPORAN_HASIL_PREDIKSI_v2.pdf</code></td><td>A+B</td></tr>"
  "<tr><td>4</td><td>Bukti pengujian: 12 competency questions, uji teknis, validasi pakar</td><td>Tabel di laporan</td><td>B (CQ, pakar), A (teknis)</td></tr>"
  "<tr><td>5</td><td>Server SPARQL berjalan (demo)</td><td><code>output/fuseki/</code></td><td>A</td></tr>"
  "<tr><td>6</td><td>Laporan akhir (Bab I–V) & slide presentasi</td><td>Dokumen kelompok</td><td>B (utama), A (bab rancangan)</td></tr></table>")
w(f"<h3>Pembagian peran</h3><p>{TA} pengelola ontologi & sistem: instalasi, build, Protégé, SWRL, Fuseki, data teknikal/bandarmology/makro, uji teknis.<br>{TB} data, pakar domain & validasi: data fundamental/indeks, berita & label, parameter pakar, competency questions, validasi pakar, laporan & slide.<br>{TAB} kesepakatan, review silang, presentasi. Peran boleh ditukar — tetapi <b>keduanya wajib bisa menjalankan Tahap 2 dan Tahap 6 sendiri</b>, karena dosen bisa meminta siapa saja mendemokan.</p>")
w("<h3>Langkah</h3>")
steps(["Buat folder bersama (Google Drive atau repositori GitHub privat) bernama <code>KBR_Kelompok9</code>; unggah <code>KBR_Kelompok9_SahamExpertKB_v2.zip</code> yang sudah diekstrak.",
       "Buka <code>Template_Data_Emiten.xlsx</code> → sheet <code>CHECKLIST_TUGAS</code> → isi kolom <b>Tenggat</b> sesuai jadwal kuliah Anda (28 tugas sudah terisi dengan PIC).",
       "Sepakati <b>aturan kerja</b>: (a) data hanya diubah di <code>data/*.csv</code>/Excel, bukan di file <code>.owl</code>; (b) build hanya dijalankan Peran A, sekali per hari setelah B mengirim data; (c) setiap angka dicatat sumbernya.",
       "Jadwalkan pertemuan singkat 2× seminggu (15 menit): apa yang selesai, apa yang macet, serah-terima berikutnya."])
w("<p class='cek'>✔ Selesai bila: folder bersama ada, tenggat di checklist terisi, kedua anggota memahami deliverable.</p>")

# ---------------- TAHAP 1
w("<h2 class='pb'>Tahap 1 — Instalasi Alat</h2><p><b>Siapa:</b> " + TAB + " (masing-masing di laptop sendiri). <b>Waktu:</b> ±1 jam.</p>")
w("<table><tr><th>Alat</th><th>Untuk apa</th><th>Wajib?</th><th>Unduh</th></tr>"
  "<tr><td>Protégé 5.6.x Desktop</td><td>Membuka & menjalankan ontologi, Pellet, SWRLTab, DL Query</td><td>Wajib</td><td>protege.stanford.edu</td></tr>"
  "<tr><td>Python 3.10+</td><td>Validasi data & membangun ontologi (owlready2 sudah dibundel di <code>lib/</code>)</td><td>Wajib</td><td>python.org</td></tr>"
  "<tr><td>JDK 25 (atau 21+)</td><td>Reasoner Pellet di pipeline & Fuseki 6</td><td>Wajib</td><td>adoptium.net (Temurin) / oracle.com</td></tr>"
  "<tr><td>Apache Jena Fuseki 6.2.0</td><td>Server SPARQL (Tahap 9)</td><td>Wajib untuk demo server</td><td>jena.apache.org → Download</td></tr>"
  "<tr><td>Excel / Google Sheets</td><td>Mengisi data</td><td>Wajib</td><td>—</td></tr>"
  "<tr><td>Node.js + Playwright</td><td>Hanya untuk mencetak ulang laporan PDF otomatis</td><td>Opsional</td><td>nodejs.org; lalu <code>npm i playwright</code></td></tr></table>")
w("<h3>Windows</h3>")
steps(["Pasang Python dari python.org. Pada layar pertama installer <b>centang “Add python.exe to PATH”</b>, lalu Install Now.",
       "Pasang JDK 25 (Temurin, file <code>.msi</code>). Saat instalasi aktifkan opsi <b>Set JAVA_HOME</b> dan <b>Add to PATH</b>.",
       "Ekstrak Protégé (ZIP) ke <code>C:\\Protege</code> → jalankan <code>Protege.exe</code> (atau <code>run.bat</code>).",
       "Ekstrak proyek ke <code>C:\\KBR\\KBR_Kelompok9_SahamExpertKB_v2</code> (hindari folder dengan spasi panjang/OneDrive yang sedang sinkron).",
       "Buka <b>Command Prompt</b> → ketik:<pre>python --version\njava -version\ncd C:\\KBR\\KBR_Kelompok9_SahamExpertKB_v2</pre>Harus muncul Python 3.x dan versi Java 21+/25."])
w("<h3>macOS</h3>")
steps(["Pasang Python dari python.org (file <code>.pkg</code>) dan JDK 25 (Temurin <code>.pkg</code>, pilih arm64 untuk Mac M1/M2/M3, x64 untuk Intel).",
       "Buka <code>.dmg</code> Protégé → seret ke Applications. Bila diblokir: klik kanan → <i>Open</i>.",
       "Ekstrak proyek ke <code>~/KBR/</code>. Buka <b>Terminal</b>:<pre>python3 --version\njava -version\ncd ~/KBR/KBR_Kelompok9_SahamExpertKB_v2</pre>"])
w("<h3>Pasang plugin Pellet di Protégé</h3>")
steps(["Protégé → <b>File › Check for plugins…</b>",
       "Centang <b>Pellet</b> (bila tidak ada, pilih <b>Openllet</b>) → <b>Install</b> → tutup & buka lagi Protégé.",
       "Cek: menu <b>Reasoner</b> sekarang memuat <b>Pellet</b>. SWRLTab & SQWRLTab sudah bawaan Protégé 5.6 (Window › Tabs).",
       "Bila nanti reasoner lambat: naikkan memori. Windows: edit <code>Protege.l4j.ini</code>/<code>run.bat</code>, ubah <code>-Xmx…</code> menjadi <code>-Xmx4G</code>. macOS: <code>Protégé.app/Contents/Info.plist</code>, cari <code>-Xmx</code>."])
w("<p class='cek'>✔ Selesai bila: <code>python --version</code> dan <code>java -version</code> berjalan, Protégé terbuka, menu Reasoner memuat Pellet.</p>")

# ---------------- TAHAP 2
w("<h2>Tahap 2 — Uji Jalan Pertama (Knowledge Base yang Sudah Ada)</h2><p><b>Tujuan:</b> membuktikan semuanya berjalan di laptop Anda sebelum mengubah data. <b>Siapa:</b> " + TAB + "</p>")
w("<h3>2a. Jalankan pipeline sekali</h3>")
steps(["Di Command Prompt/Terminal, masuk folder proyek (Tahap 1).",
       "Jalankan <code>python run_all.py</code> (macOS: <code>python3 run_all.py</code>). Ini satu perintah yang sama untuk Windows, macOS, Linux.",
       "Tunggu 2–6 menit. Layar menampilkan langkah [1]…[9] dengan <b>OK</b>. Langkah 6 & 9 (PDF) boleh GAGAL bila Node.js tidak dipasang — file utama tetap jadi.",
       "Buka <code>output/validasi_owlapi_pellet.txt</code>: harus ada <code>CONSISTENT=true</code>, <code>SWRL_RULES=303</code>."])
w("<pre>[1] Validasi data (data/*.csv) ...            OK\n[2] Skor sentimen berita ...                  OK\n[3] Bangun ontologi + SWRL + reasoning Pellet OK\n[4] Ekspor hasil inferensi (OWLAPI) ...       OK\n[5] Validasi konsistensi (OWLAPI + Pellet)    OK\n...\nSELESAI. Buka folder output/</pre>")
w("<h3>2b. Buka di Protégé & jalankan reasoner</h3>")
steps(["Protégé → <b>File › Open</b> → <code>output/SahamExpertKB_v2.owl</code>.",
       "<b>Reasoner › Pellet</b> → <b>Reasoner › Start reasoner</b>. Tunggu sampai bilah progres selesai (±1–3 menit).",
       "Tab <b>Entities › Individuals by class</b> (atau Window › Tabs › Individuals by class) → di pohon kelas klik <code>KategoriInferensi › InferensiSektor › SektorPilihanInti</code>. Muncul <b>Sektor_BarangBaku</b> dan <b>Sektor_Kesehatan</b> berlatar kuning (= hasil inferensi).",
       "Klik <code>Sektor_BarangBaku</code> → panel <b>Property assertions</b>: lihat <code>skorOutlookAktif 10</code>, <code>memilikiTailwind</code>, <code>topPickSektor</code>.",
       "Klik ikon <b>?</b> di sebelah salah satu baris kuning → jendela <i>Explanation</i> menunjukkan aturan SWRL & fakta yang memicunya."])
w("<p class='cek'>✔ Selesai bila: kedua anggota bisa menampilkan SektorPilihanInti dan penjelasannya di laptop masing-masing.</p>")

# ---------------- TAHAP 3
w("<h2>Tahap 3 — Mengumpulkan Data Emiten</h2><p><b>Tujuan:</b> mengganti 64 baris data indikatif di <code>DATA_EMITEN</code> dengan data terbaru yang bisa dipertanggungjawabkan. <b>Siapa:</b> kolom fundamental, valuasi, indeks → " + TB + "; kolom teknikal & bandarmology → " + TA + ".</p>")
w("<div class='warn'><b>Prinsip:</b> (1) satu tanggal acuan untuk semua angka (mis. penutupan Jumat terakhir); (2) laporan keuangan terbaru yang sama untuk semua emiten (mis. LK Q3-2026, disetahunkan/TTM); (3) setiap angka dicatat sumbernya di sheet log; (4) kalau satu kolom tidak bisa didapat, <b>jangan mengarang</b> — tulis di log dan diskusikan.</div>")
w("<h3>3a. Cara kerja yang efisien</h3>")
steps(["Bagi 64 emiten: Gloria mengisi fundamental untuk semua emiten; Jonnathan mengisi teknikal & bandarmology untuk semua emiten. Kerjakan per sektor (11 sektor) agar konsisten.",
       "Buka <code>Template_Data_Emiten.xlsx</code>. Tambahkan sheet baru <code>LOG_SUMBER</code> dengan kolom: <i>kode · kolom · nilai · sumber/URL · tanggal diambil · catatan</i>.",
       "Kerjakan 5 emiten dulu (mis. BBCA, ANTM, TLKM, MIKA, ICBP) → validasi (Tahap 5) → build → pastikan berjalan. Baru lanjutkan sisanya.",
       "Kolom yang hanya boleh berisi nama tertentu (sektor, sub, indeks, komU, komB, pola) — pilih dari sheet <code>NILAI_VALID</code>. Beberapa nilai dipisah titik koma, mis. <code>LQ45;IDX30;MSCI_Indonesia</code>."])
w("<h3>3b. Kolom per kolom: arti, sumber, cara menghitung</h3>")
ROWS = [
 ("Identitas", "kode, nama", "Kode & nama emiten", "idx.co.id → Perusahaan Tercatat", "Salin apa adanya", "B"),
 ("Identitas", "sektor, sub", "Sektor & subsektor IDX-IC", "idx.co.id (profil emiten)", "Pilih dari NILAI_VALID (mis. Sektor_BarangBaku, Sub_LogamMineral)", "B"),
 ("Identitas", "bank, bumn, syariah", "Penanda 1/0", "Profil emiten; Daftar Efek Syariah OJK", "1 = ya, 0 = tidak", "B"),
 ("Pasar", "harga", "Harga penutupan (Rp)", "idx.co.id / aplikasi broker / TradingView", "Penutupan di tanggal acuan; tanpa pemisah ribuan", "A"),
 ("Pasar", "mcap", "Kapitalisasi pasar (Rp triliun)", "aplikasi broker / IDX", "harga × jumlah saham beredar ÷ 10<sup>12</sup>", "B"),
 ("Pasar", "likuid", "Nilai transaksi harian rata-rata (Rp miliar)", "aplikasi broker / IDX statistik", "rata-rata nilai transaksi 20 hari ÷ 10<sup>9</sup>", "A"),
 ("Pasar", "ff", "Free float (%)", "IDX (data pemegang saham) / KSEI", "saham publik non-pengendali ÷ total saham × 100", "B"),
 ("Valuasi", "per", "PER (x)", "aplikasi broker / dihitung", "harga ÷ EPS 12 bulan terakhir (TTM); rugi → isi nilai negatif", "B"),
 ("Valuasi", "per5", "Rata-rata PER 5 tahun (x)", "aplikasi broker (chart PER band) / hitung dari 5 LK tahunan", "rata-rata PER akhir tahun 2021–2025", "B"),
 ("Valuasi", "pbv", "PBV (x)", "aplikasi broker / dihitung", "harga ÷ (ekuitas ÷ jumlah saham)", "B"),
 ("Fundamental", "roe", "ROE (%)", "LK (PSAK) di idx.co.id", "laba bersih TTM ÷ ekuitas rata-rata × 100", "B"),
 ("Fundamental", "f2", "Non-bank: DER (x) · Bank: NPL (%)", "LK / laporan publikasi bank (OJK)", "DER = utang berbunga ÷ ekuitas; NPL gross dari laporan publikasi", "B"),
 ("Fundamental", "f3", "Non-bank: NPM (%) · Bank: NIM (%)", "LK", "NPM = laba bersih ÷ pendapatan × 100; NIM dari laporan publikasi bank", "B"),
 ("Fundamental", "epsg", "Pertumbuhan EPS yoy (%)", "LK", "(EPS periode ini ÷ EPS periode sama tahun lalu − 1) × 100", "B"),
 ("Fundamental", "f5", "Non-bank: CFO ÷ laba (x) · Bank: CAR (%)", "LK arus kas / laporan publikasi bank", "arus kas operasi ÷ laba bersih", "B"),
 ("Fundamental", "dy, dpr", "Dividend yield (%), payout (%)", "pengumuman dividen IDX / LK", "DY = DPS ÷ harga × 100; DPR = DPS ÷ EPS × 100 (tidak bagi dividen → 0)", "B"),
 ("Risiko", "altman", "Altman Z (non-bank; bank isi 0)", "dihitung dari LK", "Z = 1,2·WC/TA + 1,4·RE/TA + 3,3·EBIT/TA + 0,6·MVE/TL + 1,0·Sales/TA", "B"),
 ("Risiko", "beneish", "Beneish M-Score", "dihitung dari 2 LK tahunan", "model 8 rasio (DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA); M > −1,78 = indikasi manipulasi. Prioritas rendah — bila tidak sempat, tandai di log", "B"),
 ("Teknikal", "ma50, ma200", "Jarak harga ke MA50/MA200 (%)", "TradingView (indikator Moving Average 50 & 200)", "(harga ÷ MA − 1) × 100", "A"),
 ("Teknikal", "ma50v200", "Selisih MA50 vs MA200 (%)", "TradingView", "(MA50 ÷ MA200 − 1) × 100", "A"),
 ("Teknikal", "rsi", "RSI-14", "TradingView (Relative Strength Index, 14)", "Baca nilai di tanggal acuan (0–100)", "A"),
 ("Teknikal", "macd", "Histogram MACD", "TradingView (MACD 12,26,9)", "histogram &gt; 0 → 1; ≤ 0 → −1", "A"),
 ("Teknikal", "volr", "Volume relatif (x)", "TradingView / broker", "volume hari ini ÷ rata-rata volume 20 hari", "A"),
 ("Teknikal", "atr", "ATR-14 (% harga)", "TradingView (Average True Range 14)", "ATR ÷ harga × 100", "A"),
 ("Teknikal", "chg20", "Perubahan harga 20 hari (%)", "TradingView", "(harga ÷ harga 20 hari bursa lalu − 1) × 100", "A"),
 ("Teknikal", "vwap", "Jarak ke VWAP (%)", "aplikasi broker / TradingView (VWAP)", "(harga ÷ VWAP − 1) × 100", "A"),
 ("Teknikal", "pola", "Pola chart/candle", "Pengamatan chart harian", "Nama dari NILAI_VALID, mis. DoubleBottom;BullishEngulfing; kosongkan bila tidak ada", "A"),
 ("Bandarmology", "acc", "Skor Acc/Dist broker (−100..100)", "Broker summary 20 hari (aplikasi broker)", "(net buy top-5 pembeli − |net sell top-5 penjual|) ÷ (net buy top-5 + |net sell top-5|) × 100; atau nilai fitur ‘bandar detector’ aplikasi", "A"),
 ("Bandarmology", "for20", "Net asing 20 hari (Rp miliar)", "aplikasi broker / ringkasan perdagangan IDX", "Σ (beli asing − jual asing) 20 hari ÷ 10<sup>9</sup>", "A"),
 ("Bandarmology", "ret20", "Net broker ritel 20 hari (Rp miliar)", "Broker summary", "Σ net broker berbasis ritel (lihat daftar BROKER di KB)", "A"),
 ("Bandarmology", "bo", "Rasio bid/offer (x)", "Order book", "total lot bid ÷ total lot offer", "A"),
 ("Indeks & eksposur", "indeks", "Keanggotaan indeks", "idx.co.id (konstituen indeks) · msci.com (konstituen MSCI)", "Nama dari NILAI_VALID dipisah ;", "B"),
 ("Indeks & eksposur", "komU, komB", "Komoditas pendapatan / biaya", "Laporan tahunan (segmen usaha)", "mis. ANTM komU = Kom_Nikel;Kom_Emas", "B"),
 ("Indeks & eksposur", "grup", "Grup konglomerasi", "Profil pemegang saham", "Grup_* (bebas, konsisten), mis. Grup_BUMN", "B"),
 ("Ekspektasi", "revisi", "Revisi konsensus EPS 3 bulan (%)", "Konsensus analis (riset sekuritas / aplikasi broker)", "(konsensus EPS sekarang ÷ 3 bulan lalu − 1) × 100; tidak tersedia → 0 + catat di log", "B"),
]
w("<table><tr><th style='width:9%'>Kelompok</th><th style='width:9%'>Kolom</th><th style='width:16%'>Arti</th><th style='width:20%'>Sumber</th><th>Cara menghitung / mengisi</th><th style='width:4%'>PIC</th></tr>")
for g, c, a, s, h, p in ROWS:
    w(f"<tr><td>{g}</td><td><code>{c}</code></td><td>{a}</td><td>{s}</td><td>{h}</td><td>{p}</td></tr>")
w("</table>")
w("<h3>3c. Contoh pengisian satu emiten (ANTM, data contoh saat ini)</h3>")
w("<table><tr><th>harga</th><th>per</th><th>per5</th><th>roe</th><th>f2 (DER)</th><th>f3 (NPM)</th><th>epsg</th><th>f5</th><th>altman</th><th>ma50</th><th>ma200</th><th>rsi</th><th>macd</th><th>volr</th><th>acc</th><th>for20</th></tr>"
  "<tr><td>2 900</td><td>10</td><td>18</td><td>18</td><td>0,3</td><td>6</td><td>35</td><td>1,0</td><td>4,5</td><td>7</td><td>18</td><td>63</td><td>1</td><td>1,6</td><td>32</td><td>120</td></tr></table>")
w("<p>Dari baris ini KB menyimpulkan: <code>FundamentalKuat</code> (skor 9), <code>Undervalued</code> (PER 10 ÷ 18 = 0,56), <code>TrenNaik</code> (skor teknikal 7), <code>AkumulasiBandar</code> (acc 32 ≥ 20) → <code>KandidatTopPickAdaptif</code>.</p>")
w("<h3>3d. Menyimpan ke CSV</h3>")
steps(["Di Excel: klik sheet <code>DATA_EMITEN</code> → <b>File › Save As</b> (Simpan Sebagai) → jenis file <b>CSV UTF-8</b> → nama <code>emiten.csv</code> → simpan ke folder <code>data/</code> proyek (timpa yang lama). Excel memperingatkan hanya satu sheet yang disimpan → OK. Simpan juga .xlsx-nya agar sheet lain tidak hilang.",
       "Excel berbahasa Indonesia biasanya menyimpan dengan pemisah <code>;</code> dan koma desimal — <b>keduanya sudah diterima</b> oleh sistem. Yang tidak boleh: pemisah ribuan (5.400 → tulis 5400).",
       "Google Sheets: <b>File › Download › Comma-separated values (.csv)</b> → ganti nama jadi <code>emiten.csv</code>."])
w("<p class='cek'>✔ Selesai bila: 64 baris terisi data terbaru, sheet LOG_SUMBER terisi, <code>data/emiten.csv</code> tersimpan.</p>")

# ---------------- TAHAP 4
w("<h2 class='pb'>Tahap 4 — Memperbarui Berita, Makro, Kondisi Pasar & Tanggal Acuan</h2>")
w("<h3>4a. Tanggal acuan " + TA + "</h3>")
steps(["Buka <code>data/tanggal_acuan.txt</code> (Notepad/TextEdit) → ganti isinya dengan tanggal data Anda, format <code>YYYY-MM-DD</code>, mis. <code>2026-11-13</code>. Dipakai untuk menghitung umur berita (berita &gt; 180 hari tidak lagi mengaktifkan peristiwa) dan jarak ke katalis."])
w("<h3>4b. Berita — <code>data/berita.csv</code> " + TB + "</h3>")
w("<table><tr><th>Kolom</th><th>Isi</th><th>Contoh</th></tr>"
  "<tr><td>id</td><td>Kode unik, lanjutkan nomor terakhir</td><td>N54</td></tr>"
  "<tr><td>tanggal</td><td>Tanggal terbit (YYYY-MM-DD)</td><td>2026-11-05</td></tr>"
  "<tr><td>media, url, judul</td><td>Nama media, tautan, judul asli</td><td>Kontan · https://… · “BI Tahan Suku Bunga…”</td></tr>"
  "<tr><td>kelas</td><td><code>BeritaMakroGeopolitik</code> · <code>BeritaEmiten</code> · <code>BeritaRisetAnalis</code></td><td>BeritaMakroGeopolitik</td></tr>"
  "<tr><td>kredibilitas</td><td>0–1. Pedoman: rilis resmi (BI, BPS, OJK, IDX, The Fed) 0,95; Reuters/Bloomberg/Kontan/Bisnis/CNBC 0,85–0,9; portal umum 0,7; blog/medsos 0,3–0,5. <b>Hanya ≥ 0,7 yang bisa mengaktifkan peristiwa</b></td><td>0.9</td></tr>"
  "<tr><td>peristiwa</td><td>ID peristiwa yang dibicarakan (daftar di Lampiran B); boleh kosong untuk berita emiten</td><td>Ev_BI_RDG_Okt2026</td></tr>"
  "<tr><td>sektor, emiten</td><td>Sektor_* / kode saham yang disebut (pisah ;)</td><td>Sektor_Keuangan · BBRI;BMRI</td></tr>"
  "<tr><td>variabel</td><td>Variabel makro yang dibahas: <code>MINYAK, EMAS, BUNGA, USD, CPO, INFLASI, MSCI, PASAR</code> (boleh kosong)</td><td>BUNGA</td></tr>"
  "<tr><td>arah_manual</td><td>Label manusia bila judul ambigu: 1 = variabel naik/positif, −1 = turun/negatif, 0 = netral; kosong = biarkan sistem menilai</td><td>-1</td></tr></table>")
steps(["Setiap minggu kumpulkan 5–10 berita penting (makro: BI, Fed, inflasi, rupiah, minyak, emas, perang/geopolitik, MSCI; emiten: laba, aksi korporasi).",
       "Tambah satu baris per berita. Judul ditulis persis seperti aslinya (sistem membaca nada dari judul).",
       "Bila ada peristiwa besar <b>baru</b> yang belum ada di daftar Lampiran B, catat — Peran A menambahkannya di <code>kb_geo.py</code> (Tahap 7d).",
       "Setelah build, buka <code>output/log_sentimen.txt</code>: periksa skor per berita. Bila salah arah, isi <code>arah_manual</code>."])
w("<h3>4c. Indikator makro — <code>data/makro.csv</code> " + TA + "</h3>")
w("<p>Ubah hanya kolom <b>nilai, tanggal, url, keterangan</b> (jangan mengubah <code>id</code>). Sumber: BI-Rate & kurs JISDOR → bi.go.id; inflasi → bps.go.id; Fed funds → federalreserve.gov; Brent, emas, CPO, batu bara, nikel → Investing/Trading Economics; yield SBN & CDS → berita pasar obligasi (Bisnis, Kontan, worldgovernmentbonds).</p>")
w("<h3>4d. Kondisi pasar — <code>data/kondisi_pasar.csv</code> " + TA + "</h3>")
w("<p>16 variabel yang dipakai mendeteksi <b>regime pasar</b> (krisis likuiditas / risk-off / netral / risk-on). Kolom <code>keterangan</code> menjelaskan cara menghitung tiap variabel, mis. <code>drawdownIHSGPersen</code> = IHSG terakhir ÷ IHSG akhir 2025 − 1; <code>cds5YBps</code> = CDS Indonesia 5 tahun; tren (<code>trenCDS1Bulan</code> dll.) diisi 1 / 0 / −1.</p>")
w("<p class='cek'>✔ Selesai bila: tanggal acuan diperbarui, ≥ 10 berita baru masuk, nilai makro & kondisi pasar per tanggal acuan.</p>")

# ---------------- TAHAP 5
w("<h2>Tahap 5 — Validasi Data & Build Ulang</h2><p><b>Siapa:</b> " + TA + " menjalankan; " + TB + " memperbaiki data.</p>")
steps(["<code>python validasi_data.py</code> → baca hasil. <b>ERROR</b> wajib diperbaiki (build tidak jalan); <b>CEK</b> = peringatan, periksa kewajarannya.",
       "Perbaiki di Excel → simpan CSV lagi → ulangi sampai muncul <code>HASIL: LULUS</code>.",
       "<code>python run_all.py</code> → semua langkah OK.",
       "Bandingkan <code>output/LAPORAN_HASIL_PREDIKSI_v2.pdf</code> (atau <code>.md</code>) dengan versi sebelumnya: sektor mana yang berubah kelas, emiten mana yang masuk/keluar top pick. Catat alasannya (data apa yang berubah) — ini bahan Bab IV.",
       "Simpan salinan bertanggal di folder bersama: <code>hasil_2026-11-13/</code> berisi OWL, laporan, dan CSV yang dipakai."])
w("<table><tr><th>Pesan</th><th>Artinya</th><th>Perbaikan</th></tr>"
  "<tr><td>sektor 'X' tidak dikenal</td><td>Salah ketik nama sektor</td><td>Salin dari NILAI_VALID</td></tr>"
  "<tr><td>subsektor … bukan bagian dari …</td><td>Sub tidak cocok dengan sektor</td><td>Periksa pasangan sektor–sub</td></tr>"
  "<tr><td>indeks/komoditas/pola tidak dikenal</td><td>Nama tidak ada di KB</td><td>Pakai nama dari NILAI_VALID; pisahkan dengan ;</td></tr>"
  "<tr><td>kode … ganda</td><td>Emiten dua baris</td><td>Hapus salah satu</td></tr>"
  "<tr><td>rsi=… di luar rentang</td><td>Angka tidak wajar</td><td>Cek ulang sumber (RSI 0–100, ff 0–100, acc −100..100)</td></tr>"
  "<tr><td>Altman Z non-bank bernilai 0</td><td>Belum diisi</td><td>Hitung Altman Z</td></tr></table>")
w("<p class='cek'>✔ Selesai bila: validasi LULUS, run_all.py OK, CONSISTENT=true, perubahan hasil tercatat.</p>")

# ---------------- TAHAP 6
w("<h2 class='pb'>Tahap 6 — Membedah & Menjalankan Knowledge Base di Protégé</h2><p><b>Tujuan:</b> bisa menunjukkan dan menjelaskan setiap bagian KB. <b>Siapa:</b> " + TA + " memandu, " + TB + " ikut mempraktikkan.</p>")
w("<h3>6a. Melihat struktur (TBox)</h3>")
steps(["Tab <b>Entities › Classes</b>: 15 kelas akar di bawah <code>owl:Thing</code>. Buka <code>Emiten</code> → subclass <code>EmitenPerbankan</code>, <code>EmitenNonKeuangan</code>, dsb. Buka <code>KategoriInferensi</code> → semua kelas hasil (SektorBullish…, KandidatTopPick…).",
       "Tab <b>Object properties</b>: relasi antar-individu, mis. <code>termasukSektor</code> (Emiten → Sektor), <code>memicuPergerakan</code> (Peristiwa → Pergerakan makro).",
       "Tab <b>Data properties</b>: atribut angka/teks, mis. <code>roe</code>, <code>rsi14</code>, <code>skorOutlookAktif</code>.",
       "Tab <b>Individuals</b>: fakta (ABox). Klik <code>ANTM</code> → lihat semua nilai propertinya. Klik <code>PER</code> → anotasi <code>rumus</code> & <code>ambangBatas</code> (basic knowledge).",
       "Rujukan lengkap dengan gambar pohon kelas: <code>STRUKTUR_ONTOLOGI_v2.pdf</code>."])
w("<h3>6b. Reasoning dengan Pellet</h3>")
steps(["<b>Reasoner › Pellet</b> → <b>Start reasoner</b> (setelah mengubah apa pun: <b>Synchronize reasoner</b>).",
       "Hasil inferensi tampil kuning di <b>Individuals by class</b> dan di panel Description/Property assertions individu.",
       "Klik <b>?</b> pada hasil kuning → <i>Explanation</i>: aturan SWRL & fakta pemicunya. Pakai ini saat menjelaskan ke dosen."])
w("<h3>6c. DL Query (menjawab pertanyaan)</h3>")
steps(["<b>Window › Tabs › DL Query</b> (reasoner harus aktif).",
       "Ketik ekspresi kelas, centang <b>Instances</b>, klik <b>Execute</b>. Contoh:"])
w("<pre>SektorPilihanInti\nKandidatTopPickAdaptif and termasukSektor value Sektor_BarangBaku\nEmiten and FundamentalKuat and Undervalued\nRisikoGoingConcern\nPeristiwaAktif\nEmitenPerbankan and KandidatTopPick</pre>")
w("<h3>6d. SWRLTab & SQWRLTab</h3>")
steps(["<b>Window › Tabs › SWRLTab</b>: daftar 303 aturan; kolom <i>Name</i> = kode (R-FUND-01a…), <i>Comment</i> = penjelasan.",
       "Alternatif mesin Drools: tombol <b>OWL+SWRL→Drools</b> → <b>Run Drools</b> → <b>Drools→OWL</b>. Hasil sama dengan Pellet.",
       "<b>SQWRLTab</b>: tempel query dari <code>output/SQWRL_queries.txt</code>, mis. top-3 Barang Baku:<pre>termasukSektor(?e, Sektor_BarangBaku) ^ skorTotalEmiten(?e, ?t) -> sqwrl:select(?e, ?t) ^ sqwrl:orderByDescending(?t) ^ sqwrl:limit(3)</pre>",
       "Bila SWRLTab kosong/error: lihat <code>PANDUAN_FUSEKI_PELLET_SWRLTAB.pdf</code> dan uji dengan <code>output/uji_swrltab.owl</code>."])
w("<h3>6e. Latihan wajib (berdua)</h3>")
steps(["Jelaskan secara lisan perjalanan ANTM dari angka ke <code>KandidatTopPickAdaptif</code> sambil menunjuk Protégé (pakai <i>Explanation</i>).",
       "Jelaskan mengapa Sektor_BarangBaku menjadi <code>SektorPilihanInti</code> (skor tiga skenario & <code>SektorRobustLintasSkenario</code>).",
       "What-if di Protégé: individu <code>Skenario_Base_2027_2028</code> → ubah <code>statusAktif</code> 1 → 0, dan <code>Skenario_Bear_Stagflasi</code> 0 → 1 → Synchronize reasoner → lihat sektor mana yang berubah. (Kembalikan setelahnya; perubahan di Protégé tidak disimpan ke CSV.)"])
w("<p class='cek'>✔ Selesai bila: keduanya bisa menunjukkan kelas–subclass–properti–individu, menjalankan Pellet, DL Query, SWRLTab, dan menjelaskan 2 jejak penalaran.</p>")

# ---------------- TAHAP 7
w("<h2 class='pb'>Tahap 7 — Kalibrasi Pengetahuan Pakar & Menambah Aturan</h2><p><b>Siapa:</b> " + TB + " mengusulkan (dengan alasan & sumber), " + TA + " menerapkan di kode lalu build.</p>")
w("<h3>7a. Sensitivitas sektor terhadap 12 faktor makro — <code>kb_market.py</code>, daftar <code>SEKTOR</code></h3>")
w("<pre>(\"Sektor_BarangBaku\", \"Barang Baku\", \"IDXBASIC\", 12.0, 17.0, 0.5, 3, (0, 2, 2, -1),\n   [-1, 1, -1, 0, 2, 2, -1, 1, 0, -1, 0, 0]),\n#  PER, PER5th, asing 3bln (Rp T), skorTema, fase siklus (Early, Mid, Late, Resesi),\n#  sensitivitas: Energi, USD, SukuBunga, Inflasi, Emas, LogamChina, RiskOff, BelanjaPemerintah, DayaBeli, Tarif, CPO, Digital</pre>")
w("<p>Nilai sensitivitas −2..+2: berapa sektor diuntungkan (+) atau dirugikan (−) bila faktor itu naik. Contoh: Barang Baku Emas +2 (emiten emas diuntungkan harga emas naik). Gloria memeriksa tiap angka terhadap teori/riset dan menulis alasannya di tabel “Parameter Pakar”. PER, PER 5 th, dan aliran asing sektor juga diperbarui setiap pembaruan data.</p>")
w("<h3>7b. Skenario 2027–2028 — <code>kb_geo.py</code>, daftar <code>SKENARIO</code></h3>")
w("<p>Tiga skenario dengan probabilitas (Base 0,50 · Bull 0,25 · Bear 0,25) dan arah 12 faktor (−2..+2). Perbarui probabilitas dan arah bila pandangan makro berubah (mis. setelah keputusan FOMC). Jumlah probabilitas harus 1.</p>")
w("<h3>7c. Bobot regime & ambang — <code>kb_v2.py</code>, daftar <code>REGIME</code></h3>")
w("<p>Bobot sembilan pilar per regime (fundamental, valuasi, teknikal, bandar, sentimen, sektor, risiko, likuiditas, smart money), risiko per transaksi, dan pembagian tranche akumulasi. Contoh krisis likuiditas: fundamental ×1,5, teknikal ×0,5.</p>")
w("<h3>7d. Menambah peristiwa geopolitik baru — <code>kb_geo.py</code>, daftar <code>PERISTIWA</code></h3>")
w("<pre>(\"Ev_NamaPeristiwa_Nov2026\", [\"KebijakanMoneter\"], \"Label peristiwa\", \"2026-11-19\",\n  \"Deskripsi singkat.\", [\"Mv_SukuBungaBINaik\"], \"BankIndonesia\", 0, []),\n#  id, kelas, label, tanggal, deskripsi, memicu pergerakan makro (Mv_*), diputuskanOleh, statusBerjalan, indeks terdampak</pre>")
w("<p>Salin bentuk baris peristiwa yang mirip, ganti isinya, lalu tautkan berita di <code>berita.csv</code> lewat kolom <code>peristiwa</code>. Daftar node pergerakan <code>Mv_*</code> ada di daftar <code>PERGERAKAN</code> pada file yang sama.</p>")
w("<h3>7e. Menambah aturan SWRL baru — <code>rules_swrl.py</code> / <code>rules_v2.py</code></h3>")
w("<pre># Aturan tunggal: R(kode, pilar, penjelasan, \"badan -> kepala\")\nR(\"R-FUND-13\", \"Fundamental\", \"Dividen konsisten: DY ≥ 5% dan DPR ≤ 80% → DividenBerkelanjutan\",\n  \"Emiten(?e), dividendYield(?e, ?d), greaterThanOrEqual(?d, 5.0), dpr(?e, ?p), lessThanOrEqual(?p, 80.0) -> DividenBerkelanjutan(?e)\")\n\n# Aturan bertingkat (rentang tanpa celah) otomatis jadi a/b/c:\nbins(\"R-FUND-14\", \"Fundamental\", \"Poin PBV\", \"pbv\", \"poinPBV\", \"Emiten\",\n     [(None, 1.0, 2, None), (1.0, 3.0, 1, None), (3.0, None, 0, None)])</pre>")
steps(["Pastikan nama properti & kelas yang dipakai sudah ada (cek di Protégé). Kelas baru: tambahkan di <code>kb_taxonomy.py</code>; properti baru: di <code>build_ontology.py</code> (cari <code>dp(</code> untuk contoh).",
       "Maksimal 11 argumen per built-in <code>add</code> (batas SWRLTab/Drools) — pecah penjumlahan panjang menjadi dua aturan.",
       "Tanpa “jika tidak” (SWRL monoton): buat rentang yang saling lepas dan menutup semua kemungkinan.",
       "Build → cek <code>SWRL_RULES</code> bertambah dan <code>CONSISTENT=true</code> → uji di Protégé bahwa aturan terpicu pada emiten yang diharapkan.",
       "Kelas <code>DividenBerkelanjutan</code> dan properti <code>poinPBV</code> pada contoh belum ada — buat dulu (langkah 1) sebelum aturan dipakai."])
w("<p class='cek'>✔ Selesai bila: tabel Parameter Pakar (nilai lama → baru → alasan → sumber) lengkap, build konsisten, perubahan hasil tercatat.</p>")

# ---------------- TAHAP 8
w("<h2 class='pb'>Tahap 8 — Pengujian</h2>")
w("<h3>8a. Competency Questions " + TB + "</h3><p>Pertanyaan yang wajib bisa dijawab KB. Jalankan dengan DL Query (Tahap 6c) atau SPARQL (Tahap 9), isi kolom hasil. Jawaban diharapkan berikut sesuai data 26 Okt 2026 — <b>setelah data diperbarui, jawaban bisa berubah</b>; yang dinilai adalah KB mampu menjawab & jawabannya bisa dijelaskan.</p>")
CQ = [("CQ1", "Sektor apa yang diprediksi naik 1–3 tahun?", "SektorBullish · Q01", "Barang Baku, Kesehatan"),
      ("CQ2", "Sektor mana yang tahan di semua skenario?", "SektorPilihanInti · Q02", "Barang Baku, Kesehatan; satelit: Infrastruktur"),
      ("CQ3", "Apa 3 emiten teratas per sektor pilihan?", "SPARQL Q03 / SQWRL", "per sektor inti & satelit"),
      ("CQ4", "Mengapa sektor X diprediksi naik?", "memilikiTailwind, memilikiPreseden · Q06", "jalur peristiwa → makro → sektor"),
      ("CQ5", "Regime pasar apa yang sedang terjadi?", "RegimeAktif · Q05", "Krisis Likuiditas (stres 10/12)"),
      ("CQ6", "Emiten mana rawan collapse?", "RisikoGoingConcern · Q10", "daftar emiten Altman distress"),
      ("CQ7", "Kapan & di harga berapa masuk bertahap?", "KandidatAkumulasiBertahap · Q07", "harga tranche 1–3"),
      ("CQ8", "Beda pilihan analis biasa vs pakar?", "KandidatTopPick vs KandidatTopPickAdaptif · Q04", "yang dibuang & ditambah"),
      ("CQ9", "Peristiwa geopolitik apa yang aktif?", "PeristiwaAktif", "daftar peristiwa"),
      ("CQ10", "Tesis mana yang hampir gugur?", "TesisRapuh · Q08", "tesis + indikator kunci"),
      ("CQ11", "Saham apa cocok untuk investor konservatif?", "direkomendasikanUntuk · Q12", "daftar per persona"),
      ("CQ12", "Apa definisi & rumus PER?", "individu PER → rumus · Q15", "Harga ÷ EPS")]
w("<table><tr><th>Kode</th><th>Pertanyaan</th><th>Kelas DL Query / query SPARQL</th><th>Jawaban (26 Okt)</th><th>Hasil uji Anda</th><th>Lulus</th></tr>")
for c in CQ: w(f"<tr><td>{c[0]}</td><td>{c[1]}</td><td>{c[2]}</td><td>{c[3]}</td><td></td><td>☐</td></tr>")
w("</table>")
w("<h3>8b. Uji teknis " + TA + "</h3>")
w("<table><tr><th>Uji</th><th>Cara</th><th>Lulus bila</th></tr>"
  "<tr><td>Konsistensi</td><td>Pellet di Protégé + <code>validasi_owlapi_pellet.txt</code></td><td>CONSISTENT=true, tidak ada kelas merah (Nothing)</td></tr>"
  "<tr><td>Unit test aturan</td><td>Individu <code>UJI_GORENG</code>, <code>UJI_GADAI</code>, <code>UJI_INSIDER</code> (kelas EmitenUji)</td><td>masing-masing masuk kelas risiko tata kelola yang sesuai, mis. <code>IndikasiSahamGorengan</code></td></tr>"
  "<tr><td>Uji batas aturan</td><td>Tambah satu emiten fiktif <code>UJI_BATAS</code> di CSV dengan ROE tepat 15 & PER tepat 0,6×PER5</td><td>poinROE 2, skorValuasi sesuai rentang [ , )</td></tr>"
  "<tr><td>Kesetaraan mesin</td><td>Fuseki <code>/saham</code> (Jena) vs <code>/saham-pellet</code> dengan query Q01–Q03</td><td>hasil sama</td></tr>"
  "<tr><td>What-if</td><td><code>whatif_update.ru</code> di Fuseki (Tahap 9)</td><td>regime/tesis berubah sesuai logika</td></tr>"
  "<tr><td>Rasio KB</td><td>Hitung dari <code>validasi_owlapi_pellet.txt</code>: (aksioma − aksioma SWRL)/aksioma</td><td>≥ 80% (saat ini 98%)</td></tr></table>")
w("<div class='warn'>Hapus emiten <code>UJI_BATAS</code> dari CSV setelah uji agar tidak ikut di hasil prediksi.</div>")
w("<h3>8c. Validasi pakar " + TB + "</h3>")
steps(["Cari 1–3 penilai: dosen keuangan/investasi, analis sekuritas, atau anggota galeri investasi kampus.",
       "Kirim ringkasan 2 halaman (prediksi sektor + top-3 + alasan) dan form di Lampiran C.",
       "Hitung rata-rata skor per butir; butir dengan skor ≤ 2 → bahas, perbaiki parameter (Tahap 7), build ulang.",
       "Bandingkan dengan 2–3 riset sekuritas terbaru (outlook 2027): sektor mana yang sama/berbeda dan mengapa — masuk Bab IV."])
w("<p class='cek'>✔ Selesai bila: 12 CQ terisi, uji teknis lulus, rekap validasi pakar ada.</p>")

# ---------------- TAHAP 9
w("<h2 class='pb'>Tahap 9 — Deployment dengan Apache Jena Fuseki</h2><p><b>Siapa:</b> " + TA + ". Rincian lengkap di <code>PANDUAN_FUSEKI_PELLET_SWRLTAB.pdf</code>.</p>")
steps(["Unduh Fuseki 6.2.0 (jena.apache.org → Download → <i>apache-jena-fuseki-6.2.0.zip</i>) → ekstrak, mis. ke <code>C:\\fuseki</code> atau <code>~/fuseki</code>. Butuh Java 21+.",
       "Setelah <code>run_all.py</code>, folder <code>output/fuseki/</code> sudah berisi data, aturan Jena, config, dan skrip start.",
       "Windows: <code>output\\fuseki\\start_fuseki.bat C:\\fuseki\\apache-jena-fuseki-6.2.0</code> · macOS/Linux: <code>./output/fuseki/start_fuseki.sh ~/fuseki/apache-jena-fuseki-6.2.0</code>",
       "Buka browser <code>http://localhost:3030</code> → dataset <code>/saham</code> (penalaran aturan langsung) dan <code>/saham-pellet</code> (hasil Pellet).",
       "Tab <b>query</b> → tempel query dari <code>queries_sparql.rq</code> (Q01 prediksi sektor, Q03 top-3, Q04 analis biasa vs pakar, …) → Run.",
       "What-if: tab <b>update</b> → tempel <code>whatif_update.ru</code> (mis. CDS 99,73 → 75) → jalankan → ulangi Q05/Q08 dan lihat perubahan regime/tesis.",
       "Rekam layar demo (cadangan bila saat presentasi laptop bermasalah)."])
w("<p class='cek'>✔ Selesai bila: Q01–Q05 berjalan di /saham, hasil sama dengan Pellet, demo what-if terekam.</p>")

# ---------------- TAHAP 10
w("<h2>Tahap 10 — Laporan Akhir, Slide & Skrip Demo</h2>")
w("<h3>10a. Kerangka laporan</h3><table><tr><th>Bab</th><th>Isi</th><th>Bahan siap pakai</th><th>PIC</th></tr>"
  "<tr><td>I Pendahuluan</td><td>Latar belakang (kondisi pasar 2026, kebutuhan prediksi sektor), rumusan masalah, tujuan, batasan, stakeholder</td><td>Proposal, Dokumen Pengembangan §1</td><td>B</td></tr>"
  "<tr><td>II Landasan teori</td><td>Sistem pakar & KBR, ontologi OWL, SWRL, reasoner; analisis fundamental, teknikal, bandarmology, sentimen, geopolitik-makro, CBR</td><td>Dokumen Pengembangan, individu konsep di KB</td><td>B</td></tr>"
  "<tr><td>III Metodologi & rancangan</td><td>Alur SKKNI 299/2020 & Ontology Development 101; sumber data; struktur kelas–properti; kategori 303 aturan; arsitektur pipeline & Fuseki</td><td>Struktur Ontologi v2, Panduan Lengkap §3 & §8</td><td>A</td></tr>"
  "<tr><td>IV Hasil & pembahasan</td><td>Regime pasar, prediksi sektor 3 skenario, top-3 emiten, analis biasa vs pakar, jejak penalaran ANTM, hasil CQ, uji teknis, validasi pakar, perubahan setelah pembaruan data</td><td>Laporan Hasil Prediksi v2, tabel Tahap 8</td><td>A + B</td></tr>"
  "<tr><td>V Penutup</td><td>Kesimpulan, keterbatasan (data indikatif bagian tertentu, belum backtest), saran (backtest walk-forward, otomatisasi data)</td><td>—</td><td>B</td></tr></table>")
w("<h3>10b. Slide (10–12 halaman)</h3>")
steps(["Judul & anggota", "Masalah & tujuan (prediksi sektor 1–3 tahun, top-3 emiten)", "Arsitektur: sumber → CSV → OWL + SWRL → Pellet/Fuseki → hasil",
       "Struktur ontologi (gambar pohon kelas) & angka: 297 kelas, 285 properti, ±1.000 individu, 303 aturan, KB 98%", "Contoh aturan SWRL (R-GEO-01, R-SEK-12a, R-REG-01)",
       "Jejak penalaran ANTM", "Hasil: regime + prediksi sektor 3 skenario", "Top-3 emiten & analis biasa vs pakar", "Pengujian (CQ, konsistensi, Jena = Pellet, validasi pakar)",
       "DEMO langsung", "Keterbatasan & rencana lanjut", "Penutup & disclaimer (bukan nasihat investasi)"])
w("<h3>10c. Skrip demo 6 menit</h3><table><tr><th>Menit</th><th>Aksi</th><th>Ucapan kunci</th><th>Siapa</th></tr>"
  "<tr><td>0–1</td><td>Buka OWL di Protégé, tab Classes</td><td>“Ini knowledge base: kelas, subclass, properti, individu.”</td><td>A</td></tr>"
  "<tr><td>1–2</td><td>SWRLTab, tunjukkan R-SEK-12a</td><td>“Aturan pakar JIKA–MAKA, 303 aturan.”</td><td>A</td></tr>"
  "<tr><td>2–3</td><td>Start Pellet → SektorPilihanInti → Explanation</td><td>“Kesimpulan disimpulkan reasoner, bukan ditulis tangan.”</td><td>B</td></tr>"
  "<tr><td>3–4</td><td>Individu ANTM → skor & kelas</td><td>“Dari ROE 18, PER murah, akumulasi bandar → top pick.”</td><td>B</td></tr>"
  "<tr><td>4–5</td><td>DL Query: KandidatTopPickAdaptif and termasukSektor value Sektor_Kesehatan</td><td>“KB menjawab pertanyaan pengguna.”</td><td>B</td></tr>"
  "<tr><td>5–6</td><td>Fuseki Q01 → what-if CDS → Q05</td><td>“Data berubah, kesimpulan ikut berubah otomatis.”</td><td>A</td></tr></table>")
w("<p class='cek'>✔ Selesai bila: laporan Bab I–V lengkap, slide jadi, demo dilatih minimal 2 kali (masing-masing pernah membawakan semua bagian).</p>")

# ---------------- TAHAP 11
w("<h2>Tahap 11 — Pemeliharaan & Pengumpulan</h2>")
w("<table><tr><th>Frekuensi</th><th>Data</th><th>Siapa</th></tr>"
  "<tr><td>Harian/mingguan</td><td>Harga, teknikal, broker summary, berita penting, kondisi pasar</td><td>A (teknikal, pasar) · B (berita)</td></tr>"
  "<tr><td>Bulanan</td><td>Makro (BI-Rate, inflasi, Fed, kurs, komoditas), parameter skenario</td><td>A · B</td></tr>"
  "<tr><td>Kuartalan</td><td>Laporan keuangan → fundamental, valuasi, Altman, revisi konsensus; keanggotaan indeks (rebalancing)</td><td>B</td></tr>"
  "<tr><td>Setiap pembaruan</td><td>validasi_data.py → run_all.py → cek tesis & kill switch (Q08) → arsipkan hasil bertanggal</td><td>A</td></tr></table>")
steps(["Sebelum mengumpulkan: jalankan <code>python run_all.py</code> terakhir, pastikan CONSISTENT=true.",
       "Kumpulkan: folder proyek (zip, tanpa <code>__pycache__</code>), laporan akhir, slide, rekaman demo.",
       "Isi semua status di CHECKLIST_TUGAS menjadi <b>Selesai</b>."])

# ---------------- LAMPIRAN
w("<h2 class='pb'>Lampiran A — Masalah Umum & Solusinya</h2><table><tr><th>Gejala</th><th>Penyebab</th><th>Solusi</th></tr>"
  "<tr><td><code>'python' is not recognized</code></td><td>Python belum di PATH</td><td>Install ulang dengan centang “Add python.exe to PATH”, atau pakai <code>py run_all.py</code></td></tr>"
  "<tr><td><code>Java tidak ditemukan</code></td><td>JDK belum terpasang/PATH</td><td>Pasang JDK 25, buka terminal baru, cek <code>java -version</code></td></tr>"
  "<tr><td>Validasi GAGAL</td><td>Nama/angka tidak valid</td><td>Lihat Tahap 5 (tabel pesan)</td></tr>"
  "<tr><td>Langkah [6]/[9] GAGAL</td><td>Node.js/Playwright tidak ada</td><td>Abaikan; laporan <code>.md</code> & OWL tetap jadi. Atau pasang Node.js + <code>npm i playwright</code></td></tr>"
  "<tr><td>Menu Reasoner tidak ada Pellet</td><td>Plugin belum dipasang</td><td>Tahap 1 — Check for plugins</td></tr>"
  "<tr><td>Jangan pakai HermiT</td><td>HermiT tidak mendukung built-in SWRL</td><td>Pakai Pellet</td></tr>"
  "<tr><td>Reasoner sangat lambat / out of memory</td><td>Memori Java kecil</td><td>Naikkan -Xmx ke 4G (Tahap 1)</td></tr>"
  "<tr><td>Ontologi inconsistent (kelas merah)</td><td>Data bertentangan dengan aksioma, mis. emiten di dua sektor</td><td>Klik ? pada inconsistency → perbaiki baris CSV terkait</td></tr>"
  "<tr><td>SWRLTab error “at most 11 built-in arguments”</td><td>Aturan add terlalu panjang</td><td>Sudah diperbaiki; aturan baru: pecah penjumlahan</td></tr>"
  "<tr><td>Hasil tidak berubah setelah edit di Protégé lalu run_all</td><td>OWL dibangun ulang dari CSV</td><td>Edit CSV/.py, bukan .owl</td></tr>"
  "<tr><td>Fuseki: port 3030 dipakai</td><td>Fuseki lain masih berjalan</td><td>Tutup jendela Fuseki lama atau restart laptop</td></tr>"
  "<tr><td>Excel mengubah 0.6 menjadi tanggal</td><td>Format sel otomatis</td><td>Format kolom angka sebagai Number sebelum mengisi</td></tr></table>")
w("<h2>Lampiran B — Daftar ID Peristiwa (kolom <code>peristiwa</code> di berita.csv)</h2>")
w("<table><tr><th>ID</th><th>Label</th><th>Tanggal</th></tr>" + "".join(f"<tr><td><code>{p[0]}</code></td><td>{E(p[2])}</td><td>{p[3]}</td></tr>" for p in G.PERISTIWA) + "</table>")
w("<h2 class='pb'>Lampiran C — Form Validasi Pakar</h2><p>Nama penilai: ____________________ · Jabatan/keahlian: ____________________ · Tanggal: __________</p>"
  "<p>Skala: 1 = sangat tidak setuju · 2 = tidak setuju · 3 = netral · 4 = setuju · 5 = sangat setuju</p><table><tr><th>No</th><th>Pernyataan</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>Catatan</th></tr>"
  + "".join(f"<tr><td>{i}</td><td>{t}</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td><td></td></tr>" for i, t in enumerate([
    "Deteksi kondisi pasar (regime) sesuai situasi pasar saat ini",
    "Sektor yang diprediksi naik 1–3 tahun masuk akal",
    "Sektor yang diprediksi melemah masuk akal",
    "Alasan (jalur peristiwa → makro → sektor) logis",
    "Top-3 emiten per sektor pilihan layak dipertimbangkan",
    "Bobot pilar (fundamental, teknikal, bandarmology, sentimen) wajar",
    "Pembobotan berbeda saat krisis (adaptif) sesuai praktik analis berpengalaman",
    "Peringatan risiko (going concern, saham gorengan, kill switch tesis) bermanfaat",
    "Penjelasan sistem mudah dipahami investor pemula",
    "Sistem bermanfaat sebagai alat bantu riset/edukasi"], 1))
  + "</table><p>Saran perbaikan: ______________________________________________________________________________</p>"
  "<p>______________________________________________________________________________________________</p>")
w("<p style='margin-top:14px;color:#666;font-size:8pt'>Keluaran sistem adalah alat bantu riset & edukasi, bukan nasihat investasi.</p></body></html>")

hp = os.path.join(SCR, "buku_kerja.html"); open(hp, "w", encoding="utf-8").write("\n".join(H))
dst = os.path.join(OUT, "BUKU_KERJA_LANGKAH_DEMI_LANGKAH.pdf")
footer = '<div style="font-size:7pt;width:100%;text-align:center;color:#777">Buku Kerja SahamExpertKB v2 · Halaman <span class="pageNumber"></span>/<span class="totalPages"></span></div>'
js = os.path.join(SCR, "bk.js")
open(js, "w").write(f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}');await p.pdf({{path:{json.dumps(dst)},format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
footerTemplate:{json.dumps(footer)},margin:{{top:'15mm',bottom:'17mm',left:'14mm',right:'14mm'}}}});await b.close();}})();""")
subprocess.run(["node", js], check=True)
print("PDF:", dst)
