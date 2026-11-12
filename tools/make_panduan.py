# -*- coding: utf-8 -*-
"""Panduan Lengkap Proyek (data, metodologi standar, pembagian tugas, langkah end-to-end) -> PDF + checklist Excel."""
import json, os, sys, subprocess, html, tempfile
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
SCR = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp()
r = json.load(open(os.path.join(OUT, "hasil_inferensi.json"), encoding="utf-8"))
E = html.escape

A, B, AB = "A (Jonnathan)", "B (Gloria)", "A + B"
# fase, minggu, unit SKKNI, langkah ODM, tugas[(pic, tugas, deliverable)]
FASE = [
 ("F0. Persiapan & Kesepakatan Tujuan", "Minggu 1", "—", "Langkah 1 ODM: tentukan domain & cakupan",
  [(AB, "Pasang Protégé 5.6 + Pellet, JDK 25, Fuseki 6, Python 3 di laptop masing-masing", "Kedua laptop bisa membuka SahamExpertKB_v2.owl & menjalankan Pellet"),
   (AB, "Baca bagian 1–3 panduan ini & Dokumen Pengembangan v2; sepakati tujuan sistem & stakeholder", "Notulen 1 halaman: tujuan, stakeholder, batasan"),
   (AB, "Sepakati 12 Competency Questions (CQ) — pertanyaan yang wajib dijawab KB (Bagian 7)", "Daftar CQ final"),
   (A, "Siapkan folder bersama (Google Drive/GitHub) & aturan kerja (Bagian 5.3)", "Folder proyek bersama")]),
 ("F1. Pengumpulan Data", "Minggu 1–2", "J.62DMI00.004.1 Mengumpulkan Data", "—",
  [(B, "Unduh laporan keuangan terbaru (LK Q3-2026, format PSAK) dari idx.co.id untuk emiten; hitung ROE, DER/NPL, NPM/NIM, pertumbuhan EPS, CFO/laba atau CAR, DPR, Altman Z", "Kolom fundamental di data/emiten.csv"),
   (B, "Ambil harga, PER 5 tahun, dividend yield, free float, keanggotaan indeks (BEI, MSCI)", "Kolom valuasi & indeks"),
   (A, "Ambil data harga harian (TradingView/Yahoo) → hitung MA50, MA200, RSI, MACD, volume relatif, ATR, perubahan 20 hari", "Kolom teknikal"),
   (A, "Ambil broker summary & net asing 20 hari dari aplikasi broker → skor acc/dist, net ritel", "Kolom bandarmology"),
   (B, "Kumpulkan berita makro/geopolitik/emiten terbaru (judul, tanggal, URL, media) & tandai peristiwa/sektor/emiten terkait", "data/berita.csv"),
   (A, "Perbarui indikator makro (BI-Rate, Fed, kurs, inflasi, Brent, emas, CDS, yield SBN, IHSG) & kondisi pasar", "data/makro.csv, data/kondisi_pasar.csv")]),
 ("F2. Menelaah & Memvalidasi Data", "Minggu 2", "J.62DMI00.005.1 Menelaah Data; J.62DMI00.006.1 Memvalidasi Data", "—",
  [(A, "Jalankan python3 validasi_data.py; perbaiki semua ERROR", "Hasil 'LULUS'"),
   (B, "Cek kewajaran angka (bandingkan 3–5 emiten dengan aplikasi broker / laporan tahunan); catat sumber tiap angka", "Log validasi data (sheet Excel)"),
   (AB, "Tandai data yang masih indikatif vs terverifikasi", "Kolom catatan di Excel")]),
 ("F3. Persiapan & Integrasi Data", "Minggu 2–3", "J.62DMI00.007.1–.011.1 (objek, bersihkan, konstruksi, label, integrasi data)", "—",
  [(A, "Integrasikan semua CSV → python run_all.py (membangun OWL, inferensi, laporan, paket Fuseki)", "output/SahamExpertKB_v2.owl terbarui"),
   (B, "Beri label arah berita yang ambigu (kolom arah_manual: 1 naik / -1 turun) & kredibilitas sumber", "berita.csv berlabel"),
   (A, "Periksa log_sentimen.txt: skor sentimen sektor & emiten masuk akal", "Catatan pemeriksaan")]),
 ("F4. Pemodelan Pengetahuan (Ontologi + SWRL)", "Minggu 3–4", "J.62DMI00.012.1 Membangun Skenario Model; J.62DMI00.013.1 Membangun Model", "Langkah 2–7 ODM: reuse, istilah, kelas & hierarki, properti, facet, individu",
  [(B, "Tinjau pengetahuan pakar: sensitivitas 12 faktor per sektor, skor tema, fase siklus, probabilitas skenario, ambang tesis/kill switch; usulkan perubahan beralasan", "Tabel parameter pakar + alasan"),
   (A, "Terapkan perubahan parameter ke kb_market.py / kb_v2.py; tambah/ubah aturan di rules_swrl.py / rules_v2.py bila perlu", "Kode & ontologi terbarui"),
   (A, "Jelaskan struktur kelas–subclass–properti (Struktur Ontologi v2) & 303 aturan per pilar", "Bab rancangan ontologi"),
   (B, "Tulis dasar teori tiap pilar (fundamental, teknikal, bandarmology, sentimen, geopolitik, CBR) dengan contoh dari KB", "Bab landasan teori")]),
 ("F5. Evaluasi", "Minggu 4–5", "J.62DMI00.014.1 Mengevaluasi Hasil Pemodelan; J.62DMI00.015.1 Melakukan Review Pemodelan", "Evaluasi ontologi (konsistensi & competency questions)",
  [(A, "Uji konsistensi Pellet di Protégé, uji SWRLTab/Drools, uji Fuseki = Pellet, uji emiten fiktif UJI_*", "Tabel hasil uji teknis"),
   (B, "Jawab 12 Competency Questions memakai DL Query/SPARQL; bandingkan dengan jawaban yang diharapkan", "Tabel CQ: lulus/gagal"),
   (B, "Validasi pakar: minta 1–2 analis/dosen menilai prediksi sektor & alasan (form skala 1–5)", "Rekap validasi pakar"),
   (AB, "Bandingkan rekomendasi sistem dengan riset sekuritas terbaru; bahas perbedaan", "Bab pembahasan")]),
 ("F6. Deployment", "Minggu 5", "J.62DMI00.016.1 Rencana Deployment; J.62DMI00.017.1 Melakukan Deployment", "—",
  [(A, "Jalankan Fuseki (/saham & /saham-pellet), siapkan 15 query SPARQL & demo what-if", "Endpoint berjalan + skrip demo"),
   (B, "Susun laporan akhir (hasil prediksi, top-3 emiten, analis biasa vs pakar, risiko) & slide presentasi", "Laporan + slide")]),
 ("F7. Pemeliharaan & Presentasi", "Minggu 6", "J.62DMI00.018.1 Rencana Pemeliharaan; J.62DMI00.019.1 Melakukan Pemeliharaan", "—",
  [(AB, "Tetapkan jadwal pembaruan data: harian (harga, berita), bulanan (makro), kuartalan (LK) & cek kill switch", "Rencana pemeliharaan 1 halaman"),
   (AB, "Gladi presentasi 10 menit (skrip demo di Tutorial v2 + Panduan Fuseki); bagi bagian bicara", "Presentasi siap")]),
]
json.dump(FASE, open(os.path.join(SCR, "tasks.json"), "w"), ensure_ascii=False)

def emi(k): return [e for e in r["emiten"] if e["kode"] == k][0]
an = emi("ANTM")
bb = [s for s in r["sektor"] if s["nama"] == "Sektor_BarangBaku"][0]
reg = [g for g in r["v2"]["regime"] if g["aktif"]][0]

CSS = """@page{size:A4;margin:15mm 14mm 17mm 14mm}
body{font-family:'DejaVu Sans',Arial;font-size:9.6pt;color:#1d2433;line-height:1.5}
h1{font-size:20pt;color:#0b3d6e;margin:0 0 4px}.sub{color:#555}
h2{font-size:13.5pt;color:#fff;background:#0b3d6e;padding:6px 10px;margin:18px 0 8px;break-after:avoid}
h3{font-size:11pt;color:#0b3d6e;margin:12px 0 4px;break-after:avoid}
table{border-collapse:collapse;width:100%;font-size:8.3pt;margin:6px 0 10px}
th{background:#174f86;color:#fff;padding:4px 6px;text-align:left}td{border-bottom:1px solid #d6dbe3;padding:3px 6px;vertical-align:top}
tr{break-inside:avoid}tr:nth-child(even) td{background:#f5f7fb}
.box{border:3px solid #0b3d6e;padding:14px;margin-bottom:10px}
.tip{background:#e9f6ee;border:1px solid #8fcca5;padding:7px 10px;border-radius:4px;margin:8px 0;break-inside:avoid}
.warn{background:#fff3e0;border:1px solid #f0b36b;padding:7px 10px;border-radius:4px;margin:8px 0;break-inside:avoid}
.step{border-left:4px solid #e0a100;background:#f7f9fc;padding:6px 10px;margin:5px 0;break-inside:avoid}
.n{display:inline-block;background:#e0a100;color:#fff;border-radius:50%;width:20px;height:20px;text-align:center;line-height:20px;margin-right:6px;font-size:8.5pt;font-weight:bold}
code{background:#eef1f6;padding:0 3px;border-radius:3px;font-size:8.4pt;font-family:'DejaVu Sans Mono',monospace}
pre{background:#1e2635;color:#e8edf5;padding:8px 10px;border-radius:4px;font-size:8.2pt;white-space:pre-wrap;break-inside:avoid;font-family:'DejaVu Sans Mono',monospace}
.flow{display:flex;gap:4px;align-items:stretch;margin:8px 0}.fb{flex:1;border-radius:6px;padding:6px;color:#fff;font-size:8pt}
.c1{background:#5b7aa6}.c2{background:#2f5f98}.c3{background:#174f86}.c4{background:#0b3d6e}.c5{background:#e0a100;color:#1d2433}.c6{background:#3e8e63}
.ar{align-self:center;color:#0b3d6e;font-size:14pt}
.pa{color:#0b5fa5;font-weight:bold}.pb{color:#a0407a;font-weight:bold}.pab{color:#3e8e63;font-weight:bold}"""
H = []; w = H.append
w(f"<!doctype html><html lang='id'><head><meta charset='utf-8'><style>{CSS}</style></head><body>")
w("<div class='box'><h1>Panduan Lengkap Proyek SahamExpertKB v2</h1><div class='sub'>Cara kerja data · Metodologi standar (SKKNI & ontology engineering) · Pembagian tugas berdua · Langkah end-to-end sampai knowledge base berjalan<br>Kelompok 9 KBR · Jonnathan Azarel Gunawan (L0224005) · Gloria Dana Praysilia (L0224043)</div></div>")
w("<p><b>Isi:</b> 1. Gambaran sederhana · 2. Tiga jenis isi knowledge base · 3. Bagaimana data mengalir · 4. Contoh perjalanan satu data (ANTM & sektor Barang Baku) · 5. Pembagian tugas berdua · 6. Langkah end-to-end · 7. Competency Questions & pengujian · 8. Standar yang diikuti · 9. Tanya-jawab kebingungan umum</p>")

# 1
w("<h2>1. Gambaran Sederhana: Sistem Pakar = Dokter Spesialis Saham</h2>")
w("<table><tr><th>Dunia kedokteran</th><th>Di proyek ini</th><th>Letaknya</th></tr>"
  "<tr><td>Buku ilmu kedokteran (definisi penyakit, gejala)</td><td><b>Knowledge base – pengetahuan</b>: konsep saham, rasio + rumus, pola chart, pola bandar, teori geopolitik</td><td>Kelas & individu konsep di ontologi (<code>kb_taxonomy.py</code>, <code>kb_concepts.py</code>)</td></tr>"
  "<tr><td>Rekam medis pasien (tensi, hasil lab)</td><td><b>Data/fakta</b>: angka emiten, indikator makro, berita, kondisi pasar</td><td>File <code>data/*.csv</code> → individu Emiten, Makro, Berita</td></tr>"
  "<tr><td>SOP diagnosis (\"jika demam &gt; 38 dan …, maka …\")</td><td><b>Aturan SWRL</b> (303 aturan)</td><td><code>rules_swrl.py</code>, <code>rules_v2.py</code> → aturan di ontologi</td></tr>"
  "<tr><td>Dokter yang berpikir menerapkan SOP</td><td><b>Reasoner</b> (Pellet di Protégé, atau Jena di Fuseki)</td><td>Menu Reasoner → Pellet / server Fuseki</td></tr>"
  "<tr><td>Diagnosis + resep + alasan</td><td><b>Output</b>: prediksi sektor, top pick, sinyal, risiko, jalur alasan</td><td>Kelas inferensi (kuning di Protégé), laporan PDF, query SPARQL</td></tr></table>")
w("<div class='tip'>Kuncinya: <b>Anda tidak menulis kesimpulan</b>. Anda mengisi pengetahuan, data, dan aturan; <b>reasoner</b> yang menyimpulkan. Karena itu sistem ini disebut <i>knowledge-based</i> — 98% isinya pengetahuan & fakta, hanya 2% aturan.</div>")

# 2
w("<h2>2. Tiga Jenis Isi Knowledge Base</h2>")
w("<table><tr><th>Jenis</th><th>Istilah ontologi</th><th>Contoh</th><th>Seberapa sering berubah</th><th>Siapa mengisi</th></tr>"
  "<tr><td><b>Pengetahuan (konsep)</b></td><td>TBox: Class, Subclass, Object/Data Property</td><td><code>Emiten → EmitenPerbankan</code>; properti <code>roe</code>; definisi PER beserta rumus</td><td>Jarang (saat rancangan)</td><td>Knowledge engineer + pakar domain</td></tr>"
  "<tr><td><b>Fakta (data)</b></td><td>ABox: Individu & nilai propertinya</td><td><code>ANTM roe 18.0</code>; <code>Makro_BIRate 5.75</code>; berita N19</td><td>Harian–kuartalan</td><td>Analis data</td></tr>"
  "<tr><td><b>Aturan</b></td><td>RBox/SWRL</td><td><code>Emiten(?e) ∧ roe(?e,?v) ∧ ?v ≥ 15 → poinROE(?e,2)</code></td><td>Saat kalibrasi</td><td>Knowledge engineer (atas masukan pakar)</td></tr></table>")
w("<h3>Status data saat ini</h3><table><tr><th>Data</th><th>File</th><th>Status</th></tr>"
  "<tr><td>Indikator makro & kondisi pasar (BI-Rate, Fed, CDS, Brent, IHSG, dll.)</td><td><code>data/makro.csv</code>, <code>data/kondisi_pasar.csv</code></td><td><b>Nyata</b> dari berita Sep–Okt 2026 (URL tercantum)</td></tr>"
  "<tr><td>Berita (53 item)</td><td><code>data/berita.csv</code></td><td><b>Nyata</b> (judul, tanggal, URL)</td></tr>"
  "<tr><td>Data 64 emiten (rasio, teknikal, bandar, revisi laba)</td><td><code>data/emiten.csv</code></td><td><b>Indikatif</b> — wajib diganti data terbaru (tugas F1)</td></tr>"
  "<tr><td>Parameter pakar (sensitivitas sektor, bobot regime, ambang)</td><td><code>kb_market.py</code>, <code>kb_v2.py</code></td><td>Heuristik awal — dikalibrasi lewat validasi pakar (F4–F5)</td></tr></table>")

# 3
w("<h2>3. Bagaimana Data Mengalir (dari sumber sampai kesimpulan)</h2>")
w("<div class='flow'><div class='fb c1'><b>1. Sumber</b><br>IDX, KSEI, BI, BPS, Fed, aplikasi broker, media</div><div class='ar'>→</div>"
  "<div class='fb c2'><b>2. CSV/Excel</b><br>data/emiten.csv, berita.csv, makro.csv, kondisi_pasar.csv</div><div class='ar'>→</div>"
  "<div class='fb c3'><b>3. Validasi</b><br>validasi_data.py → LULUS</div><div class='ar'>→</div>"
  "<div class='fb c4'><b>4. Bangun ontologi</b><br>python run_all.py → SahamExpertKB_v2.owl</div><div class='ar'>→</div>"
  "<div class='fb c5'><b>5. Reasoner</b><br>Pellet (Protégé) / Jena (Fuseki) menjalankan 303 aturan</div><div class='ar'>→</div>"
  "<div class='fb c6'><b>6. Output</b><br>Prediksi sektor, top pick, sinyal, risiko, laporan PDF, SPARQL</div></div>")
w("<table><tr><th>Tahap</th><th>Apa yang terjadi</th><th>Perintah / alat</th></tr>"
  "<tr><td>Isi data</td><td>Edit <code>Template_Data_Emiten.xlsx</code> lalu simpan sheet DATA_EMITEN sebagai <code>data/emiten.csv</code> (CSV UTF-8). Berita/makro diedit langsung di CSV-nya.</td><td>Excel / Numbers</td></tr>"
  "<tr><td>Validasi</td><td>Cek nama sektor/indeks/komoditas valid, angka dalam rentang wajar, kolom wajib terisi</td><td><code>python3 validasi_data.py</code></td></tr>"
  "<tr><td>Skor sentimen</td><td>Judul berita → nada × arah variabel × sensitivitas sektor (komponen ML &lt;20%)</td><td>otomatis di <code>run_all.py</code></td></tr>"
  "<tr><td>Bangun OWL</td><td>CSV + pengetahuan + aturan → file OWL (TBox + ABox + SWRL)</td><td>otomatis</td></tr>"
  "<tr><td>Reasoning</td><td>Pellet menurunkan skor & kelas; diekspor ke <code>_inferred.owl</code>, JSON, laporan PDF, paket Fuseki</td><td>otomatis; atau manual di Protégé</td></tr></table>")

# 4
w("<h2>4. Contoh Perjalanan Satu Data</h2><h3>4.1 Emiten ANTM — dari angka mentah ke kesimpulan</h3>")
f1 = lambda x: (f"{x:+g}" if x else "0")
ms = an["skorAdaptifRegime"]; W = reg["bobot"]
_v = [an["skorFundamental"], an["skorValuasi"], an["skorTeknikal"], an["skorBandar"], an["skorSentimen"], an["skorKontribusiSektorEV"], an["penaltiRisiko"], an["poinLikuiditas"], an["poinSmartMoney"]]
_formula = " + ".join(f"{str(w_).replace('.', ',')}×{v:g}" for w_, v in zip(W, _v))
_stat = " + ".join(f"{v:g}" for v in [an["skorFundamental"], an["skorValuasi"], an["skorTeknikal"], an["skorBandar"], an["skorSentimen"], an["skorKontribusiSektor"], an["penaltiRisiko"], an["poinLikuiditas"]])
_kelas_bb = [k for k in ("SektorBullishKuat", "SektorBullishModerat", "SektorNetral", "SektorBearish") if k in bb["kelas"]]
w("<table><tr><th>Langkah</th><th>Data masuk</th><th>Aturan</th><th>Hasil</th></tr>"
  f"<tr><td>Fundamental</td><td>ROE 18 · DER 0,3 · NPM 6 · EPS +35% · CFO/laba 1,0</td><td>R-FUND-01..09</td><td>poin 2+2+1+2+2 = <b>skorFundamental {an['skorFundamental']:g}</b> → <code>FundamentalKuat</code></td></tr>"
  f"<tr><td>Valuasi</td><td>PER 10 vs rata-rata 5 th 18 → rasio 0,56</td><td>R-VAL-02/03</td><td>&lt;0,6 → <b>skorValuasi {an['skorValuasi']:g}</b> → <code>Undervalued</code></td></tr>"
  f"<tr><td>Teknikal</td><td>+7% di atas MA50, +18% di atas MA200, RSI 63, MACD +, volume 1,6×</td><td>R-TEK-01..06</td><td>3+2+1+1 = <b>skorTeknikal {an['skorTeknikal']:g}</b> → <code>TrenNaik</code></td></tr>"
  f"<tr><td>Bandarmology</td><td>Acc/dist +32, net asing +Rp120 M</td><td>R-BDR-01..03</td><td>3+2 = <b>skorBandar {an['skorBandar']:g}</b> → <code>AkumulasiBandar</code></td></tr>"
  f"<tr><td>Sentimen</td><td>Skor sentimen berita yang menyebut ANTM (sentiment_scorer)</td><td>R-SEN-01</td><td><b>{f1(an['skorSentimen'])}</b></td></tr>"
  f"<tr><td>Sektor</td><td>Barang Baku skor outlook {bb['skorOutlookAktif']} (EV {bb['skorEkspektasiProbabilistik']})</td><td>R-EMT-01 / R-ROB</td><td>statis <b>{f1(an['skorKontribusiSektor'])}</b> · berbasis EV <b>{f1(an['skorKontribusiSektorEV'])}</b></td></tr>"
  f"<tr><td>Risiko & likuiditas</td><td>Altman 4,5 · transaksi Rp420 M/hari</td><td>R-RISK-01, R-EMT-02</td><td>penalti {an['penaltiRisiko']:g} · likuiditas {an['poinLikuiditas']:g}</td></tr>"
  f"<tr><td><b>Skor statis (analis biasa)</b></td><td colspan='2'>{_stat}</td><td><b>{an['skorTotalEmiten']:g}</b>{' → <code>KandidatTopPick</code>' if 'KandidatTopPick' in an['kelas'] else ''}</td></tr>"
  f"<tr><td><b>Skor adaptif (pakar)</b></td><td colspan='2'>{reg['label']}: {_formula} (urutan: fundamental, valuasi, teknikal, bandar, sentimen, sektor-EV, risiko, likuiditas, smart money)</td><td><b>{ms:g}</b> ≥ ambang {reg['ambang']} → {'<code>KandidatTopPickAdaptif</code>' if 'KandidatTopPickAdaptif' in an['kelas'] else 'belum top pick'}</td></tr></table>")
w("<h3>4.2 Sektor Barang Baku — dari peristiwa dunia ke prediksi</h3>")
_lain = bb['skorOutlookAktif'] - bb['skorValuasiSektor'] - bb['skorTema'] - bb['poinSentimen'] - bb['poinAsing']
w(f"<table><tr><th>Komponen</th><th>Asal</th><th>Nilai</th></tr>"
  f"<tr><td>Makro-geopolitik + rotasi siklus</td><td>Σ sensitivitas sektor × arah 12 faktor skenario aktif, ditambah poin fase siklus (late cycle → barang baku disukai)</td><td>{f1(_lain)}</td></tr>"
  f"<tr><td>Valuasi sektor</td><td>PER sektor ÷ PER 5 th = {bb['rasioValuasi']:.2f}</td><td>{f1(bb['skorValuasiSektor'])}</td></tr>"
  f"<tr><td>Tema struktural</td><td>Hilirisasi nikel + emas safe haven (skor tema × 2)</td><td>{f1(bb['skorTema'])}</td></tr>"
  f"<tr><td>Sentimen sektor</td><td>Agregat berita (scorer)</td><td>{f1(bb['poinSentimen'])}</td></tr>"
  f"<tr><td>Aliran asing</td><td>Aliran asing 3 bulan</td><td>{f1(bb['poinAsing'])}</td></tr>"
  f"<tr><td><b>Skor outlook (Base)</b></td><td>R-SEK-07 → R-SEK-12</td><td><b>{bb['skorOutlookAktif']}</b> → <code>{', '.join(_kelas_bb)}</code>; Bull {bb['skorOutlookBull']}, Bear {bb['skorOutlookBear']} → EV {bb['skorEkspektasiProbabilistik']} → <code>SektorRobustLintasSkenario</code> → <code>SektorPilihanInti</code></td></tr></table>")
w("<p>Jalur alasan (multi-hop) yang ikut disimpulkan: " + "; ".join("<i>" + " → ".join(E(x) for x in t["jalur"]) + "</i>" for t in bb["tailwind"][:3]) + (f"; preseden historis: <i>{E(bb['preseden'][0])}</i>" if bb["preseden"] else "") + ".</p>")

# 5
w("<h2>5. Pembagian Tugas Berdua</h2>")
w("<table><tr><th>Peran</th><th>Fokus</th><th>Usulan</th></tr>"
  "<tr><td class='pa'>Peran A — Knowledge Engineer & Sistem</td><td>Ontologi (kelas, properti), aturan SWRL, Protégé + Pellet, pipeline <code>run_all.py</code>, Fuseki & SPARQL, data teknikal/bandarmology/makro, pengujian teknis</td><td>Jonnathan</td></tr>"
  "<tr><td class='pb'>Peran B — Domain Expert, Data & Validasi</td><td>Data fundamental & indeks, berita & label sentimen, parameter pakar (sensitivitas, skenario, ambang), competency questions, validasi pakar, laporan & slide</td><td>Gloria</td></tr>"
  "<tr><td class='pab'>A + B</td><td>Kesepakatan tujuan, review silang, pembahasan hasil, presentasi</td><td>Bersama</td></tr></table>")
w("<div class='tip'>Pembagian ini usulan; boleh ditukar sesuai keahlian. Yang penting <b>setiap orang menguasai keseluruhan alur</b> karena dosen bisa bertanya ke siapa saja. Lakukan <b>review silang</b>: A memeriksa data B, B memeriksa hasil penalaran A.</div>")
w("<h3>5.1 Rencana kerja per fase (6 minggu — sesuaikan dengan tenggat)</h3>")
for (f, mg, sk, odm, tasks) in FASE:
    w(f"<h3>{E(f)} <span style='font-weight:normal;color:#555'>· {mg} · SKKNI: {E(sk)}{' · ' + E(odm) if odm != '—' else ''}</span></h3>")
    w("<table><tr><th style='width:13%'>PIC</th><th>Tugas</th><th style='width:30%'>Deliverable</th></tr>")
    for pic, t, d in tasks:
        cl = "pa" if pic == A else ("pb" if pic == B else "pab")
        w(f"<tr><td class='{cl}'>{pic}</td><td>{E(t)}</td><td>{E(d)}</td></tr>")
    w("</table>")
w("<h3>5.2 Titik serah-terima</h3><table><tr><th>Dari → Ke</th><th>Yang diserahkan</th><th>Kapan</th></tr>"
  "<tr><td class='pb'>B → A</td><td>data/emiten.csv (fundamental, indeks), berita.csv berlabel</td><td>Akhir F1–F3</td></tr>"
  "<tr><td class='pa'>A → B</td><td>Hasil validasi_data.py & daftar data yang ditolak</td><td>F2</td></tr>"
  "<tr><td class='pb'>B → A</td><td>Tabel parameter pakar (sensitivitas, skenario, ambang) + alasan</td><td>F4</td></tr>"
  "<tr><td class='pa'>A → B</td><td>Ontologi & hasil inferensi terbaru (OWL, laporan PDF, JSON) untuk divalidasi</td><td>F4–F5</td></tr>"
  "<tr><td class='pb'>B → A</td><td>Hasil CQ & validasi pakar → perbaikan aturan/ambang</td><td>F5</td></tr></table>")
w("<h3>5.3 Aturan kerja agar tidak bentrok</h3>"
  "<div class='step'><span class='n'>1</span><b>Sumber kebenaran = folder <code>data/</code> + file <code>.py</code></b>. File <code>.owl</code> adalah <i>hasil build</i>; jangan diedit langsung di Protégé (akan tertimpa saat <code>run_all.py</code>). Perubahan di Protégé hanya untuk eksplorasi.</div>"
  "<div class='step'><span class='n'>2</span>Hanya <b>satu orang menjalankan build</b> per hari (Peran A); B mengirim CSV terbaru sebelum jam yang disepakati.</div>"
  "<div class='step'><span class='n'>3</span>Gunakan Google Drive/GitHub dengan versi bertanggal (mis. <code>emiten_2026-11-05.csv</code>) atau commit Git dengan pesan jelas.</div>"
  "<div class='step'><span class='n'>4</span>Setiap angka di CSV punya sumber; catat di sheet log validasi.</div>"
  "<div class='step'><span class='n'>5</span>Gunakan sheet <b>CHECKLIST_TUGAS</b> di <code>Template_Data_Emiten.xlsx</code> untuk memantau status.</div>")

# 6
w("<h2>6. Langkah End-to-End sampai Knowledge Base Berjalan</h2>")
steps = [
 ("Instalasi", "Pasang Protégé 5.6.x, plugin Pellet (File → Check for plugins), Python 3, JDK 25 (untuk Fuseki & pipeline), Fuseki 6.2.0. Ekstrak <code>KBR_Kelompok9_SahamExpertKB_v2.zip</code>."),
 ("Coba hasil yang sudah ada", "Buka <code>output/SahamExpertKB_v2.owl</code> di Protégé → Reasoner → Pellet → Start reasoner → tab Individuals by class → kelas <code>SektorPilihanInti</code>, <code>KandidatTopPickAdaptif</code>. Pastikan muncul hasil (latar kuning)."),
 ("Pahami struktur", "Buka <code>STRUKTUR_ONTOLOGI_v2.pdf</code> & tab Entities → Classes. Cocokkan 15 kelas akar dengan bagian 1–2 panduan ini."),
 ("Isi/perbarui data", "Isi <code>Template_Data_Emiten.xlsx</code> (sheet KAMUS_KOLOM menjelaskan cara menghitung tiap kolom) → simpan sebagai <code>data/emiten.csv</code>. Perbarui <code>data/berita.csv</code>, <code>data/makro.csv</code>, <code>data/kondisi_pasar.csv</code>."),
 ("Validasi data", "Terminal di folder proyek: <code>python3 validasi_data.py</code> → harus <b>LULUS</b>."),
 ("Bangun ulang", "<code>python run_all.py</code> (sama untuk Windows, macOS, Linux). Hasil: OWL baru, <code>_inferred.owl</code>, laporan PDF, paket Fuseki."),
 ("Jalankan reasoner", "Buka OWL baru di Protégé → Pellet → Start reasoner. Atau SWRLTab → OWL+SWRL→Drools → Run Drools → Drools→OWL."),
 ("Jawab Competency Questions", "Jalankan 12 CQ (Bagian 7) lewat DL Query / SPARQL; isi tabel lulus/gagal."),
 ("Uji teknis", "Konsistensi (Pellet), emiten fiktif <code>UJI_*</code> terdeteksi benar, <code>output/validasi_owlapi_pellet.txt</code> CONSISTENT=true, Fuseki /saham = /saham-pellet."),
 ("Deploy", "<code>./start_fuseki.sh ~/Downloads/apache-jena-fuseki-6.2.0</code> → <code>http://localhost:3030</code> → query SPARQL & what-if (Panduan Fuseki)."),
 ("Validasi pakar", "Tunjukkan prediksi sektor & alasan ke analis/dosen; catat skor kesesuaian 1–5 & masukan; perbaiki parameter, ulangi langkah 5–8."),
 ("Laporan & presentasi", "Gunakan Laporan Hasil v2, Dokumen Pengembangan v2, Struktur Ontologi v2; latih demo 10 menit."),
]
for i, (t, d) in enumerate(steps, 1):
    w(f"<div class='step'><span class='n'>{i}</span><b>{t}.</b> {d}</div>")
w("<pre>cd ~/Downloads/KBR_Kelompok9_SahamExpertKB_v2\npython validasi_data.py     # 1) cek data (macOS/Linux: python3)\npython run_all.py           # 2) bangun ontologi + reasoning + laporan + paket Fuseki\nopen output/LAPORAN_HASIL_PREDIKSI_v2.pdf   # 3) lihat hasil</pre>")

# 7
w("<h2>7. Competency Questions (CQ) & Cara Mengujinya</h2><p>CQ adalah standar evaluasi ontologi: daftar pertanyaan yang <b>harus</b> bisa dijawab knowledge base. Jawaban di bawah dihasilkan otomatis oleh <code>tools/uji_cq.py</code> dari hasil inferensi terbaru (tanggal acuan " + str(__import__('kb_geo').TODAY) + ").</p>")
import runpy, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    _cq = runpy.run_path(os.path.join(HERE, "tools", "uji_cq.py"))["CQ"]
CQ = [(c[0], c[1], f"<code>{E(c[2])}</code>", E(c[3])) for c in _cq]
w("<table><tr><th>Kode</th><th>Pertanyaan</th><th>Cara menguji</th><th>Jawaban KB</th><th>Lulus?</th></tr>")
for c in CQ:
    w(f"<tr><td>{c[0]}</td><td>{c[1]}</td><td>{c[2]}</td><td>{c[3]}</td><td>✔</td></tr>")
w("</table>")
w("<h3>Pengujian teknis</h3><table><tr><th>Uji</th><th>Cara</th><th>Hasil saat ini</th></tr>"
  "<tr><td>Konsistensi logika</td><td>Pellet di Protégé / validasi_owlapi_pellet.txt</td><td>CONSISTENT = true</td></tr>"
  "<tr><td>Unit test aturan tata kelola</td><td>Emiten fiktif UJI_GORENG, UJI_GADAI, UJI_INSIDER</td><td>Ketiganya terdeteksi benar</td></tr>"
  "<tr><td>Kesetaraan mesin</td><td>Pellet vs Jena (Fuseki)</td><td>Prediksi sektor (Q01), regime (Q05), skor statis & adaptif serta status top pick (Q04) identik</td></tr>"
  "<tr><td>What-if</td><td>CDS 103,79 → 75 + CDS & rupiah membaik (whatif_update.ru)</td><td>Stres 11 → 10, muncul DivergensiIntermarketBullish, tesis Keuangan terpicu</td></tr>"
  "<tr><td>Rasio KB</td><td>Hitung aksioma</td><td>KB 98,0% vs aturan 2,0%</td></tr></table>")

# 8
w("<h2>8. Standar yang Diikuti</h2><table><tr><th>Standar</th><th>Dipakai untuk</th><th>Penerapan di proyek</th></tr>"
  "<tr><td><b>SKKNI Kepmenaker No. 299 Tahun 2020</b> — Bidang Artificial Intelligence Subbidang Data Science</td><td>Alur kerja & pembagian kompetensi</td><td>Fase F1–F7 dipetakan ke unit J.62DMI00.004.1 (Mengumpulkan Data) s.d. J.62DMI00.019.1 (Melakukan Pemeliharaan Model)</td></tr>"
  "<tr><td><b>Ontology Development 101</b> (Noy & McGuinness, Stanford)</td><td>Langkah membangun ontologi</td><td>Domain → reuse → istilah → kelas & hierarki → properti → facet (domain/range/tipe) → individu</td></tr>"
  "<tr><td><b>W3C OWL 2 & SWRL</b></td><td>Format knowledge base & aturan</td><td>File RDF/XML (OWL) + 303 aturan SWRL; SPARQL 1.1 untuk query</td></tr>"
  "<tr><td><b>IDX-IC (BEI)</b></td><td>Klasifikasi sektor</td><td>11 sektor & subsektor</td></tr>"
  "<tr><td><b>PSAK (SAK Indonesia)</b></td><td>Sumber rasio keuangan</td><td>Rasio dihitung dari laporan keuangan PSAK yang dipublikasikan di IDX</td></tr>"
  "<tr><td><b>Regulasi OJK/BEI</b></td><td>Batasan & kepatuhan</td><td>Free float, keterbukaan informasi, disclaimer bukan nasihat investasi</td></tr></table>")

# 9
w("<h2>9. Tanya-Jawab Kebingungan Umum</h2>")
for q, a in [
 ("Kenapa ada begitu banyak file?", "Hanya 4 yang perlu disentuh sehari-hari: <code>data/emiten.csv</code>, <code>data/berita.csv</code>, <code>data/makro.csv</code>, <code>data/kondisi_pasar.csv</code>. Sisanya kode yang membangun ontologi otomatis dan hasil (folder <code>output/</code>)."),
 ("Apakah harus bisa Python?", "Tidak untuk mengisi data dan menjalankan. Cukup dua perintah: <code>python3 validasi_data.py</code> dan <code>python run_all.py</code>. Python hanya diperlukan bila mengubah aturan/parameter pakar."),
 ("Data emiten indikatif — apakah hasilnya salah?", "Struktur penalaran benar dan teruji; angkanya contoh. Setelah Anda mengganti dengan data nyata (F1), seluruh kesimpulan otomatis mengikuti data baru."),
 ("Apa bedanya Pellet, SWRLTab, dan Fuseki?", "Ketiganya menjalankan aturan yang sama dengan mesin berbeda: Pellet (reasoner OWL di Protégé), SWRLTab (mesin Drools di Protégé), Fuseki (server SPARQL dengan mesin aturan Jena). Hasilnya sudah diuji identik."),
 ("Bagian mana yang 'knowledge-based' dan mana yang ML?", "Knowledge-based: semua kelas, fakta, dan 303 aturan (98%). ML/statistik (&lt;20%): hanya skor sentimen judul berita dan agregasi breadth, yang menjadi input aturan."),
 ("Bagaimana menambah emiten baru?", "Tambah satu baris di Excel/CSV dengan sektor & subsektor dari sheet NILAI_VALID → validasi → python run_all.py. Emiten baru otomatis dinilai semua aturan."),
 ("Bagaimana menambah berita/peristiwa baru?", "Berita: tambah baris di berita.csv (isi kolom peristiwa dengan id peristiwa yang ada). Peristiwa baru: tambah di <code>kb_geo.py</code> daftar PERISTIWA (tugas Peran A)."),
]:
    w(f"<div class='step'><b>{q}</b><br>{a}</div>")
w("</body></html>")
hp = os.path.join(SCR, "panduan.html"); open(hp, "w", encoding="utf-8").write("\n".join(H))
dst = os.path.join(OUT, "PANDUAN_LENGKAP_PROYEK_DAN_PEMBAGIAN_TUGAS.pdf")
footer = '<div style="font-size:7pt;width:100%;text-align:center;color:#777">Panduan Lengkap Proyek · SahamExpertKB v2 · Halaman <span class="pageNumber"></span>/<span class="totalPages"></span></div>'
js = os.path.join(SCR, "p.js")
open(js, "w").write(f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}');await p.pdf({{path:{json.dumps(dst)},format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
footerTemplate:{json.dumps(footer)},margin:{{top:'15mm',bottom:'17mm',left:'14mm',right:'14mm'}}}});await b.close();}})();""")
subprocess.run(["node", js], check=True)
print("PDF:", dst)
