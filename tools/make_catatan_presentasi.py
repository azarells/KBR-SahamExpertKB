# -*- coding: utf-8 -*-
"""CATATAN PEGANGAN PRESENTASI: keputusan desain ontologi beserta alasannya, keputusan pakar
yang tampil di dashboard, kelemahan, dan lembar angka kunci.
Pakai: python3 tools/make_catatan_presentasi.py   (butuh Node.js + Playwright)"""
import base64, json, os, subprocess, tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(HERE, "dashboard", "assets", "logo_kbr.png")
DST = os.path.join(HERE, "output", "CATATAN_PRESENTASI_SahamExpertKB.pdf")
H = []; w = H.append

def table(head, rows, widths=None, cls=""):
    cg = "".join(f'<col style="width:{x}">' for x in widths) if widths else ""
    w(f'<table class="{cls}"><colgroup>{cg}</colgroup><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
      "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table>")
def card(judul, keputusan, alasan, bukti=None, ucap=None):
    w(f'<div class="card"><div class="ch">{judul}</div><div class="row"><span class="k">Keputusan</span><span>{keputusan}</span></div>'
      f'<div class="row"><span class="k">Alasan</span><span>{alasan}</span></div>' +
      (f'<div class="row"><span class="k">Bukti / contoh</span><span>{bukti}</span></div>' if bukti else "") +
      (f'<div class="say">“{ucap}”</div>' if ucap else "") + "</div>")
def note(s, k="info"):
    lbl = {"info": "Ingat", "warn": "Jujur saja", "tip": "Tips"}[k]
    w(f'<div class="note {k}"><b>{lbl}.</b> {s}</div>')

CSS = """@page{size:A4;margin:14mm 13mm 16mm 13mm}*{box-sizing:border-box}
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:9.4pt;color:#1f1416;line-height:1.45}
h1{font-size:19pt;color:#7a0e17;margin:0 0 4px;letter-spacing:-.3px}
h2{font-size:12.5pt;color:#7a0e17;margin:14px 0 6px;padding-bottom:3px;border-bottom:2px solid #f6d3d6;break-after:avoid}
p{margin:3px 0 6px;text-align:justify}ul{margin:3px 0 6px;padding-left:18px}li{margin:1px 0}
table{border-collapse:collapse;width:100%;margin:5px 0 10px;font-size:8.5pt}
th{background:#fdecee;color:#7a0e17;text-align:left;padding:4px 6px;border:1px solid #f0d5d8}
td{padding:4px 6px;border:1px solid #f0e2e4;vertical-align:top}tr{break-inside:avoid}
code{font-family:'DejaVu Sans Mono',monospace;font-size:8pt;background:#fdecee;color:#7a0e17;padding:0 3px;border-radius:3px}
.card{border:1px solid #f0d5d8;border-left:5px solid #a8131f;border-radius:8px;padding:7px 10px;margin:7px 0;break-inside:avoid;background:#fff}
.card .ch{font-weight:800;color:#7a0e17;font-size:10.2pt;margin-bottom:3px}
.card .row{display:grid;grid-template-columns:92px 1fr;gap:8px;margin:2px 0}
.card .k{font-size:8pt;font-weight:800;color:#a8131f;text-transform:uppercase;letter-spacing:.04em;padding-top:1px}
.card .say{margin-top:5px;background:#eef8f3;border-radius:6px;padding:5px 8px;font-style:italic;font-size:8.9pt;color:#135c3a}
.note{border-left:4px solid #a8131f;background:#fdf2f3;padding:5px 9px;margin:6px 0 9px;border-radius:0 7px 7px 0;font-size:8.9pt;break-inside:avoid}
.note.warn{border-color:#b86e00;background:#fff6e6}.note.tip{border-color:#1d8a57;background:#eef8f3}
.pb{break-after:page}
.top{display:flex;align-items:center;gap:14px;border-bottom:3px solid #7a0e17;padding-bottom:8px;margin-bottom:10px}
.top img{height:46px}.top .t{font-size:9pt;color:#5d4a4d}
.big{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin:8px 0}
.big div{background:linear-gradient(150deg,#fff,#fdecee);border:1px solid #f6d3d6;border-radius:10px;padding:7px 9px}
.big b{display:block;font-size:15pt;color:#7a0e17;line-height:1.1}.big span{font-size:7.8pt;color:#5d4a4d;font-weight:700}
.tree{font-family:'DejaVu Sans Mono',monospace;font-size:7.9pt;background:#fff8f9;border:1px solid #f0d5d8;border-radius:8px;padding:8px 10px;white-space:pre;line-height:1.38;break-inside:avoid}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:10px}"""

logo = "data:image/png;base64," + base64.b64encode(open(LOGO, "rb").read()).decode()
w(f'<div class="top"><img src="{logo}"><div><h1>Catatan Pegangan Presentasi</h1><div class="t">SahamExpertKB · Kelompok 9 · Jonnathan Azarel Gunawan &amp; Gloria Dana Praysilia · baca 15 menit sebelum tampil</div></div></div>')

# =============================================================== 0. PETA CEPAT
w('<h2>0. Peta cepat (hafalkan halaman ini)</h2>')
w('<p><b>Satu kalimat:</b> SahamExpertKB adalah sistem pakar berbasis ontologi OWL dan 303 aturan SWRL yang memprediksi sektor saham BEI yang berpeluang naik dalam 1–3 tahun dan memilih emiten terbaik, dengan cara menilai yang menyesuaikan kondisi pasar.</p>')
w('<div class="big">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in [
    ("298", "kelas"), ("285", "properti (65 objek + 220 data)"), ("1.392", "individu"), ("303", "aturan SWRL"),
    ("15.519", "aksioma"), ("+7.943", "aksioma hasil inferensi"), ("SROIQ(D)", "ekspresivitas (OWLAPI)"), ("103/103", "soal uji lulus"),
    ("98%", "porsi knowledge base"), ("11/12", "skor stres → Krisis"), ("2 + 2", "sektor inti + satelit"), ("7 vs 4", "top pick pakar vs analis biasa")]) + "</div>")
table(["Lapisan", "Isi", "Satu kata kunci"], [
    ["Data", "CSV: 64 emiten, 11 sektor, 71 berita, 23 indikator makro (per 19 Nov 2026)", "fakta"],
    ["Ontologi (TBox)", "kelas, hierarki, properti, batasan", "kosakata"],
    ["Fakta (ABox)", "1.392 individu dibangun otomatis oleh owlready2 dari CSV", "data"],
    ["Aturan", "303 SWRL berkode dan berpilar", "cara pakar berpikir"],
    ["Reasoner", "Pellet: konsistensi, klasifikasi, eksekusi aturan", "kesimpulan"],
    ["Server", "Apache Jena Fuseki: /saham-pellet dan /saham (305 aturan Jena)", "SPARQL lewat HTTP"],
    ["Dashboard", "visual, what-if, 100 pertanyaan bervisual", "bukti untuk pengguna"],
], ["17%", "63%", "20%"])

# =============================================================== 1. KEPUTUSAN DESAIN ONTOLOGI
w('<h2>1. Keputusan perancangan ontologi beserta alasannya</h2>')
card("1.1 Mulai dari competency questions, bukan dari kelas",
     "Lingkup ditentukan oleh 12 pertanyaan yang wajib bisa dijawab, misalnya sektor apa yang naik 1–3 tahun, emiten mana yang rawan collapse, apa beda pilihan analis biasa dan pakar.",
     "Ontology Development 101 (Noy &amp; McGuinness) menyarankan CQ sebagai batas lingkup dan alat uji. Semua kelas dan aturan harus berguna untuk menjawab salah satu CQ.",
     "12/12 CQ terjawab; diperluas menjadi 103 soal uji.",
     "Kami tidak mulai dari daftar kelas, tapi dari pertanyaan yang harus bisa dijawab sistem.")
card("1.2 Tiga cabang besar: entitas, pengetahuan, kesimpulan",
     "Kelas teratas dibagi menjadi (a) <b>entitas</b> dunia nyata: <code>EntitasPasarModal</code>; (b) <b>pengetahuan</b> analisis: <code>AnalisisFundamental</code>, <code>AnalisisTeknikal</code>, <code>Bandarmology</code>, <code>AnalisisSentimen</code>, <code>AnalisisGeopolitikMakro</code>, <code>PenalaranPakar</code>, <code>PengetahuanDasarSaham</code>; (c) <b>kesimpulan</b>: <code>KategoriInferensi</code> (131 subkelas).",
     "Memisahkan fakta (yang diketik) dari kesimpulan (yang diisi reasoner) membuat ontologi rapi, mudah dijelaskan, dan mudah diuji. Kelas kesimpulan boleh berubah saat data berubah; kelas entitas tidak.",
     "ANTM tercatat sebagai <code>Emiten</code> (fakta); Pellet menambahkan <code>FundamentalKuat</code>, <code>KandidatTopPickAdaptif</code> (kesimpulan, kuning di Protégé).",
     "Kami memisahkan apa yang kami ketahui dari apa yang disimpulkan sistem.")
w('<div class="tree">owl:Thing\n'
  '├── EntitasPasarModal ── Emiten · Sektor · Subsektor · IndeksSaham · Broker · Komoditas · Institusi · KonglomerasiGrup · PenyediaIndeks\n'
  '├── AnalisisFundamental ── RasioKeuangan (9 jenis) · MetodeValuasi · ModelSkorRisiko · LaporanKeuangan\n'
  '├── AnalisisTeknikal ── IndikatorTeknikal · PolaChart · PolaCandlestick · TeoriTeknikal · KonsepTeknikal\n'
  '├── Bandarmology ── KonsepBandarmology · PolaBandar · PolaScalper\n'
  '├── AnalisisSentimen ── Berita (3 jenis) · SumberSentimen · KomponenML\n'
  '├── AnalisisGeopolitikMakro ── PeristiwaGeopolitik (10 jenis) · PergerakanMakro · IndikatorMakro (5 jenis)\n'
  '├── PenalaranPakar ── RegimePasar · Skenario · PenilaianSektor · TesisInvestasi · Katalis · PeriodeHistoris · TemaStruktural …\n'
  '├── PengetahuanDasarSaham ── MekanismePerdagangan · AksiKorporasi · BiasPerilaku · ManajemenRisiko · ProfilRisiko …\n'
  '├── Stakeholder · SumberData · IndikatorKatalog · KeluaranSistem · TujuanSDG · PenandaKualitasData\n'
  '└── KategoriInferensi ── InferensiEmiten · InferensiSektor · InferensiPasar · RegimeAktif · TesisGugur/Valid/Rapuh …</div>')

w('<h2 style="break-before:page">1.3 Alasan pemilihan subkelas penting</h2>')
table(["Kelas induk → subkelas", "Alasan pemisahan", "Dipakai untuk"], [
    ["<b>Emiten</b> → EmitenPerbankan, EmitenNonKeuangan <i>(disjoint)</i>", "bank dinilai dengan rasio berbeda: NIM, NPL, CAR. Altman Z tidak berlaku untuk bank. Disjoint karena satu emiten tidak mungkin keduanya", "aturan risiko: Altman Z hanya untuk non-keuangan (R-RISK-01), CAR &lt; 12 untuk bank (R-RISK-02)"],
    ["<b>Emiten</b> → EmitenBUMN, EmitenSyariah <i>(tidak disjoint)</i>", "label tambahan yang bisa tumpang tindih: satu bank bisa BUMN sekaligus syariah", "filter persona dan pertanyaan dashboard"],
    ["<b>IndeksSaham</b> → IndeksDomestik, IndeksGlobal (+ MSCI, FTSE, Amerika, Asia, Eropa)", "dana pasif global (MSCI/FTSE) dan indeks luar negeri memengaruhi BEI lewat jalur berbeda dengan indeks domestik", "risiko outflow pasif, transmisi sentimen (memengaruhiIndeks transitif)"],
    ["<b>RasioKeuangan</b> → 9 jenis (profitabilitas, solvabilitas, likuiditas, valuasi, pertumbuhan, arus kas, dividen, efisiensi, perbankan)", "mengikuti pengelompokan buku analisis fundamental; satu pilar skor memakai satu atau dua jenis rasio", "40 individu rasio lengkap dengan rumus dan ambang batas"],
    ["<b>PolaChart</b> → PolaReversal / PolaKontinuasi dan PolaBullish / PolaBearish <i>(disjoint)</i>", "dua sumbu berbeda: apakah tren berbalik, dan ke arah mana. Bullish dan bearish tidak mungkin bersamaan", "konfirmasi pola bullish + akumulasi bandar (R-TEK-07)"],
    ["<b>Broker</b> → BrokerAsing, BrokerLokal <i>(disjoint)</i>", "bandarmology membedakan aliran dana asing dan lokal/ritel", "akumulasi institusi asing vs distribusi ke ritel"],
    ["<b>Berita</b> → BeritaEmiten, BeritaMakroGeopolitik, BeritaRisetAnalis", "dampaknya berbeda: berita makro memengaruhi sektor lewat sensitivitas; berita emiten langsung ke emitennya", "skor sentimen sektor vs emiten, red flag berita"],
    ["<b>PeristiwaGeopolitik</b> → 10 jenis (KebijakanMoneter, KonflikPerang, KeputusanOPEC, KeputusanPenyediaIndeks, …)", "setiap jenis memicu jalur transmisi makro yang berbeda", "rantai peristiwa → pergerakan → sektor"],
    ["<b>PenalaranPakar</b> → RegimePasar, Skenario, TesisInvestasi, Katalis, PeriodeHistoris, PenilaianSektor", "ini <i>meta-pengetahuan</i>: cara pakar menyesuaikan analisis, bukan data pasar", "bobot adaptif, robustness, kill switch, CBR"],
    ["<b>KategoriInferensi</b> → InferensiEmiten, InferensiSektor, InferensiPasar, TesisValid/TesisGugur <i>(disjoint)</i>", "semua kelas hasil penalaran dikumpulkan di satu cabang; disjoint menjaga konsistensi (tesis tidak boleh valid sekaligus gugur)", "baris kuning di Protégé; dashboard membaca kelas-kelas ini"],
], ["31%", "39%", "30%"])

card("1.4 PenilaianSektor sebagai individu tersendiri (pola relasi n-ari)",
     "Skor sektor per skenario disimpan sebagai individu <code>Penilaian_&lt;Sektor&gt;_&lt;Skenario&gt;</code> (33 individu = 11 sektor × 3 skenario), dihubungkan lewat <code>menilaiSektor</code> dan <code>dibawahSkenario</code>.",
     "Properti OWL hanya menghubungkan dua hal, padahal di sini ada tiga: sektor, skenario, dan skor. Pola standarnya adalah membuat individu perantara (reifikasi / n-ary relation pattern).",
     "<code>Penilaian_BarangBaku_Base_2027_2028</code>: skor outlook 11, makro 0, rotasi 2. Q-axiom: setiap penilaian tepat satu sektor dan satu skenario.",
     "OWL hanya punya relasi dua arah, jadi untuk sektor × skenario × skor kami membuat individu penilaian.")
card("1.5 Object property vs data property",
     "Hubungan antar-benda memakai object property (65, mis. <code>termasukSektor</code>, <code>anggotaIndeks</code>, <code>menyebabkan</code>). Angka memakai data property (220, mis. <code>roe</code>, <code>der</code>, <code>cds5YBps</code>) dengan tipe XSD. Keterangan untuk manusia (rumus, label) memakai annotation property.",
     "Object property bisa dinalar sebagai graf (rantai sebab-akibat, invers, transitif); data property bisa dibandingkan dengan ambang di aturan SWRL; anotasi tidak membebani reasoner.",
     "<code>termasukSektor</code> functional (satu sektor), <code>anggotaIndeks</code> ⇄ <code>memilikiKonstituen</code> (invers), <code>memengaruhiIndeks</code> transitif, <code>menyebabkan</code> asimetris dan irefleksif.")
card("1.6 Data di CSV, ontologi dibangun otomatis (owlready2)",
     "Fakta disimpan di <code>data/*.csv</code>; <code>build_ontology.py</code> membangun 1.392 individu dan menjalankan Pellet. Hasilnya tetap file OWL standar untuk Protégé.",
     "Mengetik ribuan nilai di Protégé lambat dan rawan salah; CSV mudah diedit berdua dan diperbarui berkala; pembangunan otomatis membuat hasil selalu konsisten dan bisa diulang dengan satu perintah.",
     "<code>python3 run_all.py</code> → 12 tahap, sekitar satu menit.")
card("1.7 Penamaan IRI yang bisa dibaca",
     "Emiten memakai kode saham (<code>ex:ANTM</code>); entitas lain memakai awalan jenis: <code>Sektor_</code>, <code>Ev_</code> (peristiwa), <code>Mv_</code> (pergerakan makro), <code>Tesis_</code>, <code>Regime_</code>, <code>Skenario_</code>, <code>Persona_</code>.",
     "Mudah dibaca di query SPARQL dan Protégé, sekaligus mencegah nama bertabrakan.")
card("1.8 Aturan SWRL berkode, berpilar, dan berinterval",
     "Setiap aturan punya kode (R-FUND-01a, R-PAS-03, …) dan pilar. Skor bertingkat memakai interval berpasangan [bawah, atas). Aturan disusun berantai: poin → skor pilar → skor total → skor adaptif → top pick.",
     "SWRL monoton dan tidak punya ELSE (sifat bahasanya), jadi interval harus tidak tumpang tindih dan menutup semua nilai. Kode dan pilar membuat aturan bisa ditelusuri dan dihitung porsinya.",
     "Uji A05: setiap emiten mendapat tepat satu nilai per pilar; uji W04 menemukan celah R-PAS-05 lalu diperbaiki.")
card("1.9 Pellet sebagai reasoner",
     "Pellet dipakai di pipeline (owlready2 &amp; OWLAPI) dan di Protégé.",
     "Pellet mendukung SWRL beserta built-in perbandingan dan aritmetika. HermiT, reasoner bawaan Protégé, tidak mendukung built-in itu, sehingga skor tidak akan terbentuk.")
card("1.10 Menaikkan ekspresivitas ke SROIQ(D) dengan modularisasi",
     "Ditambahkan aksioma S (transitif), R (asimetris, irefleksif, disjoint property), O (AllDifferent; hasValue di modul alignment), Q (kardinalitas berkualifikasi). I dan (D) sudah ada.",
     "Form mewajibkan SROIQ(D). Restriksi nominal di ontologi inti membuat Pellet sekitar 25× lebih lambat karena berinteraksi dengan 303 aturan dan 1.392 individu, jadi diletakkan di modul yang mengimpor ontologi inti.",
     "OWLAPI DLExpressivityChecker: inti dan gabungan = SROIQ(D); konsisten; 103/103 tetap lulus.")
card("1.11 Memakai ulang ontologi eksternal",
     "Fondasi W3C (RDF, RDFS, OWL, XSD, SWRL) dipakai langsung; modul <code>SahamExpertKB_alignment.ttl</code> memetakan ke FIBO, schema.org, SKOS, Dublin Core. FIBO dirujuk IRI-nya, tidak diimpor penuh.",
     "Interoperabilitas dengan sistem keuangan lain (langkah ke-2 OD101: reuse). FIBO terdiri dari ratusan file sehingga impor penuh membuat ontologi berat.",
     "Satu aksioma <code>BankSentral ⊑ fibo:CentralBank</code> → Pellet menyimpulkan BI, The Fed, ECB, PBoC, BoJ sebagai CentralBank versi FIBO.")
card("1.12 Fuseki dengan dua dataset",
     "<code>/saham-pellet</code> berisi hasil Pellet (hanya baca); <code>/saham</code> berisi data mentah + 305 aturan Jena (hasil terjemahan otomatis 303 SWRL + 2 RDFS) dan menerima SPARQL UPDATE.",
     "Aplikasi lain butuh endpoint HTTP, bukan Protégé. Dataset kedua memungkinkan what-if langsung, sekaligus validasi silang: dua mesin berbeda memberi hasil identik.",
     "Regime, skor stres 11, dan tujuh top pick sama di Pellet dan Jena.")

# =============================================================== 2. KEPUTUSAN PAKAR DI DASHBOARD
w('<div class="pb"></div><h1>2. Keputusan pakar yang tampil di dashboard</h1>')
w('<p>Setiap angka dan label di dashboard adalah hasil satu atau beberapa aturan. Tabel ini menunjukkan <b>keputusan apa</b>, <b>aturan dan ambangnya</b>, dan <b>alasan pakarnya</b>. Jenis penalarannya: <b>S</b> = scoring (jumlah poin), <b>W</b> = scoring berbobot, <b>L</b> = logika DAN/ATAU, <b>A</b> = ambang tunggal, <b>P</b> = probabilistik, <b>C</b> = rantai sebab-akibat / kasus.</p>')
table(["Panel", "Keputusan pakar", "Aturan &amp; ambang / rumus", "Jenis", "Alasan pakar"], [
    ["Ringkasan", "Berapa tingkat stres pasar", "R-STR-01..07: 6 indikator × 0–2 poin. Drawdown ≤ −30% (2), CDS ≥ 120 (2) / 80–120 (1), net asing ≤ −50 T (2), kurs ≥ 17.500 (2), yield ≥ 7,5% (2), breadth &lt; 25% (2)", "S", "satu indikator bisa menyesatkan; gabungan enam lebih stabil"],
    ["Ringkasan", "Regime pasar", "R-REG-01..04: stres ≥ 8 Krisis Likuiditas · 5–7 Risk-Off · 3–4 Netral · &lt; 3 Risk-On", "A", "cara menilai saham harus berbeda saat krisis dan saat normal"],
    ["Ringkasan", "Bobot sembilan pilar", "krisis: fundamental, valuasi, risiko, smart money ×1,5; teknikal, sentimen ×0,5; lainnya ×1", "W", "saat krisis hampir semua saham di bawah MA200, jadi sinyal teknikal dan sentimen menyesatkan; neraca dan dana besar lebih penting"],
    ["Ringkasan", "Premi risiko negara tinggi", "R-PAS-01: CDS ≥ 90", "A", "investor global menilai risiko Indonesia naik"],
    ["Ringkasan", "Kapitulasi pasar", "R-PAS-03: drawdown ≤ −40% <b>dan</b> crash harian ≤ −10%", "L", "jual panik besar sering menandai dasar pasar"],
    ["Sektor", "Skor outlook sektor", "R-SEK-07: makro-geo (12 faktor: sensitivitas × arah) + valuasi + tema × 2 + sentimen + aliran asing + rotasi", "S", "sektor dipengaruhi makro, valuasi, tema jangka panjang, dan aliran dana sekaligus"],
    ["Sektor", "Status sektor", "R-SEK-12: ≥ 12 Bullish Kuat · 7–11 Bullish Moderat · 2–6 Netral · &lt; 2 Bearish", "A", "kategori lebih mudah dipakai investor daripada angka mentah"],
    ["Sektor", "Ekspektasi lintas skenario", "R-ROB-01: 0,5 × base + 0,25 × bull + 0,25 × bear", "P", "masa depan tidak pasti; pakar menimbang beberapa skenario"],
    ["Sektor", "Sektor inti", "R-ROB-04: bullish <b>dan</b> robust (base ≥ 7, bull ≥ 7, bear ≥ 2)", "L", "fondasi portofolio harus aman di skenario terburuk"],
    ["Sektor", "Sektor satelit", "R-ROB-05: upside ≥ 1,5 × downside, ekspektasi ≥ 2, <b>dan</b> ada peluang kontrarian", "L", "taruhan kecil yang asimetris: rugi terbatas, potensi besar"],
    ["Emiten", "Skor statis (analis biasa)", "R-EMT-03: jumlah 8 pilar, bobot sama", "S", "pembanding: cara analis yang tidak memperhatikan regime"],
    ["Emiten", "Skor adaptif (pakar)", "R-ADP-02: Σ bobot regime × 9 pilar (termasuk smart money)", "W", "bobot mengikuti kondisi pasar"],
    ["Emiten", "Top pick analis biasa", "R-EMT-04: skor statis ≥ 21 di sektor bullish", "L", "hanya 4 saham"],
    ["Emiten", "Top pick sistem pakar", "R-ADP-03: skor adaptif ≥ ambang regime (24,7 saat krisis), sektor berekspektasi positif, penalti risiko ≥ −1", "L", "ambang dinaikkan saat krisis agar lebih selektif; 7 saham"],
    ["Emiten", "Watchlist", "R-EMT-05: skor statis 16–20 di sektor bullish", "A", "layak dipantau, belum layak dibeli"],
    ["Bedah", "Stop loss / take profit", "harga − 2 × ATR / harga + 3 × ATR", "A", "batas mengikuti volatilitas saham; risk–reward 1 : 1,5"],
    ["Bedah", "Ukuran posisi maksimum", "R-POS-01: risiko per transaksi regime (0,5% saat krisis) ÷ (2 × ATR%) × 100", "A", "saham yang lebih bergejolak mendapat porsi lebih kecil"],
    ["Bedah", "Fundamental kuat / risiko", "poin ROE, DER, margin, pertumbuhan, arus kas; Altman Z &lt; 1,81 distress (−5), 1,81–2,99 abu-abu (−1)", "S", "kualitas dan kesehatan keuangan dulu, baru harga"],
    ["Tesis", "Status tesis (kill switch)", "R-TES-01..08: gugur bila melewati batas; rapuh bila jarak &lt; 10%; terpicu bila melewati ambang kontrarian", "A", "pakar harus tahu kapan dia salah dan kapan harus waspada"],
    ["Tesis", "Sektor dipantau ketat", "R-TES-09/10: tesis gugur atau rapuh → sektor dipantau", "L", "Barang Baku tetap inti, tetapi diawasi karena tesis emas gugur"],
    ["Risiko", "Going concern", "zona distress Altman <b>dan</b> (DER &gt; 1,5 atau CFO/laba &lt; 0,7 atau merugi)", "L", "tanda awal perusahaan bermasalah"],
    ["Risiko", "Value trap", "R-EMT-07: murah, tetapi fundamental lemah dan tren turun", "L", "murah belum tentu menarik"],
    ["Risiko", "Outflow pasif", "keputusan MSCI/FTSE aktif yang berdampak pada indeks tempat emiten menjadi anggota", "C", "dana pasif menjual otomatis"],
    ["Geopolitik", "Sektor diuntungkan / dirugikan", "peristiwa aktif → memicuPergerakan → menyebabkan → menguntungkanSektor", "C", "dampak berita ditelusuri sampai ke sektor dan emiten"],
    ["Geopolitik", "Periode analog (CBR)", "kemiripan = 20 − Σ bobot × |selisih fitur|; analog bila ≥ 13 (saat ini 2022 = 17, 2018 = 15)", "C", "pakar belajar dari krisis sebelumnya"],
    ["Sentimen", "Bobot berita", "kredibilitas sumber × exp(−umur/90); &gt; 180 hari diabaikan; red flag bila kredibilitas ≥ 0,8 dan nada ≤ −0,4", "W", "berita lama dan sumber lemah kurang berpengaruh"],
    ["What-if", "Akumulasi bertahap", "kapitulasi + washout + premi risiko tinggi → strategi bertahap; emiten berkualitas, murah, tanpa penalti → kandidat; tranche 30/30/40%", "L", "membeli saat panik, tetapi bertahap karena dasar belum pasti"],
    ["Persona", "Rekomendasi per investor", "R-PRF-01..09: konservatif (fundamental kuat, yield ≥ 5%), moderat (skor ≥ 20, sektor bullish), agresif (teknikal ≥ 5, bandar ≥ 3)", "L", "saham yang sama tidak cocok untuk semua orang"],
    ["Semua", "Data perlu diverifikasi", "R-DAT-01..04: data indikatif atau kedaluwarsa → ditandai", "L", "sistem jujur soal kualitas datanya"],
], ["9%", "17%", "40%", "6%", "28%"], cls="ex")
note("Polanya: <b>scoring</b> dipakai untuk menggabungkan banyak sinyal menjadi satu ukuran; <b>aturan logika</b> memakai ukuran itu untuk mengambil keputusan; <b>meta-penalaran</b> (regime, skenario, kill switch) mengatur kapan dan seberapa kuat keputusan itu berlaku.")

# =============================================================== 3. KELEMAHAN & JAWABAN
w('<h2>3. Kelemahan yang perlu diakui (dan jawabannya)</h2>')
table(["Kelemahan", "Jawaban singkat"], [
    ["Ambang batas tetap (CDS 120, kurs 17.500, …)", "berasal dari pengetahuan pakar dan kondisi 2026; mengubahnya cukup satu baris aturan, lalu run_all.py"],
    ["Bobot enam indikator stres sama (maks 2 poin)", "pilihan sederhana dan transparan; kalibrasi bobot masuk rencana backtest"],
    ["Data diperbarui manual (CSV)", "pipeline sudah otomatis dari CSV; tinggal menyambungkan sumber data otomatis"],
    ["Belum ada backtest historis", "validasi saat ini terhadap logika pakar dan data aktual 19 Nov 2026 (mis. tesis emas gugur sesuai harga)"],
    ["Sentimen memakai leksikon sederhana", "sengaja kecil (&lt; 20%) dan tetap ditafsirkan aturan SWRL"],
    ["Nominal eksplisit di modul, bukan di inti", "keputusan modularisasi demi performa reasoner; KB gabungan tetap SROIQ(D) dan konsisten"],
], ["38%", "62%"])
note("Sistem ini alat bantu analisis dan edukasi, bukan nasihat investasi personal. Sampaikan ini di penutup.", "warn")

# =============================================================== 4. JAWABAN CEPAT
w('<h2>4. Jawaban cepat untuk pertanyaan yang paling mungkin</h2>')
table(["Pertanyaan", "Jawaban 1–2 kalimat"], [
    ["Kenapa sistem pakar, bukan ML?", "data krisis sedikit dan ML sulit dijelaskan; aturan pakar bisa ditulis eksplisit dan setiap kesimpulan bisa ditelusuri"],
    ["Apa itu ontologi?", "model formal pengetahuan dunia saham yang bisa dinalar komputer: kelas, hubungan, angka, individu, dan aturan"],
    ["Kenapa kelas kesimpulan dipisah?", "supaya jelas mana fakta dan mana hasil penalaran; kelas kesimpulan berubah saat data berubah"],
    ["Kenapa Perbankan dipisah dari NonKeuangan?", "bank dinilai dengan NIM, NPL, CAR; Altman Z hanya berlaku untuk non-keuangan"],
    ["Kenapa ada PenilaianSektor?", "OWL hanya relasi dua arah; sektor × skenario × skor butuh individu perantara (pola n-ari)"],
    ["Apa itu aksioma?", "satu pernyataan logis di ontologi; ada 15.519, dan Pellet menyimpulkan 7.943 lagi"],
    ["Kenapa SWRL tidak pakai ELSE?", "sifat bahasa SWRL (monoton, open world); diganti interval berpasangan, dibuktikan uji A05"],
    ["Apa bedanya skor statis dan adaptif?", "statis = 8 pilar bobot sama; adaptif = 9 pilar × bobot regime; ANTM 27 → 35"],
    ["Kenapa butuh Fuseki?", "agar aplikasi lain bisa bertanya lewat HTTP dan what-if bisa berjalan langsung"],
    ["Bagaimana tahu aturannya benar?", "103/103 uji lulus, konsisten menurut Pellet, dan dua mesin berbeda (Pellet dan Jena) memberi hasil identik"],
], ["34%", "66%"])

html = f"<!DOCTYPE html><html lang='id'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(H)}</body></html>"
tmp = tempfile.mkdtemp(); hp = os.path.join(tmp, "c.html"); open(hp, "w", encoding="utf-8").write(html)
footer = '<div style="font-size:7.5pt;width:100%;text-align:center;color:#999">Catatan Presentasi SahamExpertKB · Kelompok 9 · <span class="pageNumber"></span>/<span class="totalPages"></span></div>'
js = os.path.join(tmp, "c.js")
open(js, "w").write(f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}',{{waitUntil:'load'}});await p.pdf({{path:{json.dumps(DST)},format:'A4',printBackground:true,displayHeaderFooter:true,
headerTemplate:'<span></span>',footerTemplate:{json.dumps(footer)},margin:{{top:'14mm',bottom:'16mm',left:'13mm',right:'13mm'}}}});await b.close();}})();""")
subprocess.run(["node", js], check=True)
print("PDF:", DST)
