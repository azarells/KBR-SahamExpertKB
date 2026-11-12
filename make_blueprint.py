# -*- coding: utf-8 -*-
"""Dokumen Pengembangan v2: Sumber Data, Katalog Indikator, dan Pembeda Sistem Pakar vs Analis Biasa (PDF)."""
import json, os, re, sys, subprocess, collections, html, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "lib"))
import warnings; warnings.filterwarnings("ignore")
import kb_sources as SRC, kb_v2 as V2, kb_market as M, kb_geo as G
from rules_swrl import define_rules
RULES = define_rules(M.FAKTOR)
OUT = os.path.join(HERE, "output")
r = json.load(open(os.path.join(OUT, "hasil_inferensi.json"), encoding="utf-8"))
val = open(os.path.join(OUT, "validasi_owlapi_pellet.txt")).read()
num = lambda k: int(re.search(k + r"=(\d+)", val).group(1))
E = html.escape
REAL = [e for e in r["emiten"] if not e["uji"]]
EMI = {e["kode"]: e for e in r["emiten"]}
has = lambda e, c: c in e["kelas"]
lst = lambda c: ", ".join(sorted(e["kode"] for e in REAL if has(e, c))) or "–"
V = r["v2"]; P = V["pasar"]
regime = [g for g in V["regime"] if g["aktif"]][0]
F = lambda x, d=1: f"{float(x):,.{d}f}" if x is not None else "–"
sek = {s["nama"]: s for s in r["sektor"]}
inti = [s["label"].replace("Sektor ", "") for s in r["sektor"] if "SektorPilihanInti" in s["kelas"]]
sat = [s["label"].replace("Sektor ", "") for s in r["sektor"] if "SektorPilihanSatelit" in s["kelas"]]
static = {e["kode"] for e in REAL if has(e, "KandidatTopPick")}
adapt = {e["kode"] for e in REAL if has(e, "KandidatTopPickAdaptif")}
cnt = collections.Counter(p.split("-")[1] if "-" in c else c for c, p, _, _ in [(x[0], x[0], 0, 0) for x in RULES])
v2codes = {"DAT", "PAS", "STR", "REG", "ANT", "RS", "REF", "KAP", "REV", "ERP", "GOV", "ROB", "ADP", "KON", "POS", "KAT", "TES"}
n_v2 = sum(1 for x in RULES if x[0].split("-")[1] in v2codes or x[0] in ("R-PRF-08", "R-PRF-09"))

CSS = """
@page{size:A4;margin:15mm 14mm 17mm 14mm}
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:9.3pt;color:#1d2433;line-height:1.48}
h1{font-size:20pt;color:#0b3d6e;margin:0 0 4px} .sub{color:#555;margin-bottom:10px}
h2{font-size:13.5pt;color:#fff;background:#0b3d6e;padding:6px 10px;margin:18px 0 8px;break-after:avoid}
h3{font-size:11pt;color:#0b3d6e;margin:12px 0 4px;break-after:avoid}
table{border-collapse:collapse;width:100%;font-size:7.9pt;margin:6px 0 10px}
th{background:#174f86;color:#fff;padding:4px 5px;text-align:left} td{border-bottom:1px solid #d6dbe3;padding:3px 5px;vertical-align:top}
tr{break-inside:avoid} tr:nth-child(even) td{background:#f5f7fb}
.box{border:2px solid #0b3d6e;padding:10px 12px;margin:8px 0;break-inside:avoid}
.warn{background:#fff3e0;border:1px solid #f0b36b;padding:6px 10px;border-radius:4px;margin:8px 0;break-inside:avoid}
.tip{background:#e9f6ee;border:1px solid #8fcca5;padding:6px 10px;border-radius:4px;margin:8px 0;break-inside:avoid}
.kpi{display:inline-block;width:23%;margin:0 1% 6px 0;border:1px solid #c9d3e3;border-radius:6px;padding:6px 8px;vertical-align:top;background:#f7f9fc}
.kpi b{font-size:14pt;color:#0b3d6e;display:block}
.layer{border-radius:6px;padding:7px 10px;margin:5px 0;color:#fff;break-inside:avoid}
.l1{background:#5b7aa6}.l2{background:#2f5f98}.l3{background:#0b3d6e}.l4{background:#e0a100;color:#1d2433}.l5{background:#3e8e63}
.st-T{color:#1b7a3d;font-weight:bold}.st-S{color:#a86b00;font-weight:bold}.st-R{color:#777}
code{background:#eef1f6;padding:0 3px;border-radius:3px;font-size:8pt}
"""
H = []; w = H.append
w(f"<!doctype html><html lang='id'><head><meta charset='utf-8'><style>{CSS}</style></head><body>")
w("<div class='box'><h1>Dokumen Pengembangan v2 — SahamExpertKB</h1>")
w("<div class='sub'>Sumber Data · Katalog Indikator · Apa yang Membedakan Sistem Pakar dari Analis Saham Biasa<br>Kelompok 9 KBR · Jonnathan Azarel Gunawan (L0224005) · Gloria Dana Praysilia (L0224043) · data acuan " + str(G.TODAY) + "</div>")
w(f"<div class='kpi'><b>{num('CLASSES')}</b>kelas (v1: 226)</div><div class='kpi'><b>{num('INDIVIDUALS'):,}</b>individu (v1: 1.003)</div>"
  f"<div class='kpi'><b>{num('SWRL_RULES')}</b>aturan SWRL (v1: 182)</div><div class='kpi'><b>{(num('TOTAL_AXIOMS') - num('SWRL_RULES')) / num('TOTAL_AXIOMS'):.1%}</b>porsi knowledge base</div>")
w(f"<div class='kpi'><b>{len(SRC.SUMBER)}</b>sumber data terdaftar</div><div class='kpi'><b>{len(SRC.K)}</b>indikator dalam katalog</div>"
  f"<div class='kpi'><b>{n_v2}</b>aturan pakar baru v2</div><div class='kpi'><b>{num('TOTAL_AXIOMS'):,}</b>aksioma (v1: 10.701)</div></div>")

# ---------------- 1
w("<h2>1. Inti Perubahan v2 dalam Satu Halaman</h2>")
w("<p>v1 sudah menggabungkan fundamental, teknikal, bandarmology, sentimen, geopolitik, dan CBR. Namun v1 masih bekerja seperti <b>analis yang rajin</b>: menjumlahkan skor pilar dengan bobot tetap pada satu skenario. "
  "v2 menambahkan <b>lapisan meta-penalaran</b> — pengetahuan <i>tentang kapan</i> sebuah pengetahuan berlaku — yang menjadi ciri pakar sesungguhnya:</p><ol>"
  "<li><b>Konteks mengubah makna sinyal</b> (deteksi regime → bobot adaptif).</li>"
  "<li><b>Antisipasi, bukan reaksi</b> (reaction function otoritas, katalis terjadwal).</li>"
  "<li><b>Berpikir tingkat dua</b> (priced-in, sell the news, celah ekspektasi, forced selling).</li>"
  "<li><b>Keputusan di bawah ketidakpastian</b> (ekspektasi probabilistik 3 skenario, robustness, asimetri, core–satelit).</li>"
  "<li><b>Disiplin eksekusi</b> (akumulasi bertahap, ukuran posisi berbasis risiko, konsentrasi tema, kill switch).</li>"
  "<li><b>Risiko yang tidak terlihat di rasio</b> (tata kelola, free float/HSC, gadai saham, saham gorengan).</li>"
  "<li><b>Tahu batas pengetahuan sendiri</b> (kesegaran data, data indikatif → wajib verifikasi, unit test aturan).</li></ol>")
w("<h3>Arsitektur v2</h3>")
w("<div class='layer l1'><b>Lapisan 0 — Sumber Data</b> (35 sumber: IDX, KSEI, OJK, BI, BPS, Kemenkeu, ESDM, FRED, Fed, EIA, MSCI, GDELT, GPR Index, ACLED, terminal, aplikasi broker, media) → <code>SumberData</code>, <code>IndikatorKatalog</code></div>")
w("<div class='layer l2'><b>Lapisan 1 — Basic Knowledge</b> (konsep saham, rasio + rumus + ambang, teknikal, pola, mekanisme BEI, aksi korporasi, bias perilaku)</div>")
w("<div class='layer l3'><b>Lapisan 2 — Expert Knowledge v1</b> (bandarmology, sentimen aspect-based, transmisi geopolitik multi-hop, rotasi siklus, CBR, skenario)</div>")
w("<div class='layer l4'><b>Lapisan 3 — Meta-Penalaran Pakar v2</b> (regime &amp; bobot adaptif, reaction function, refleksivitas, kapitulasi, revisi laba, ERP, tata kelola, robustness, konfluensi/konflik, sizing, katalis, tesis &amp; kill switch, kualitas data)</div>")
w("<div class='layer l5'><b>Lapisan 4 — Keluaran untuk Stakeholder</b> (prediksi sektor core/satelit, top pick adaptif, rencana akumulasi 3 tranche, sinyal quant + SL/TP + ukuran posisi, kalender katalis, status kill switch, peringatan risiko, rekomendasi per persona)</div>")
w("<div class='tip'>Komponen non-simbolik tetap &lt;20%: scorer sentimen, detektor pola, dan agregasi breadth hanya menyuplai nilai input. Semua keputusan dibuat oleh aturan SWRL yang dapat ditelusuri.</div>")

# ---------------- 2  pembeda
w("<h2>2. Yang Membedakan Sistem Pakar dari Analis Saham Biasa</h2>")
w("<p>Setiap baris di bawah adalah modul yang <b>sudah diimplementasikan</b> sebagai aturan SWRL. Kolom terakhir menunjukkan apa yang benar-benar dihasilkan reasoner Pellet pada data acuan " + str(G.TODAY) + ".</p>")
w("<table><tr><th style='width:15%'>Kemampuan</th><th style='width:20%'>Analis saham biasa</th><th style='width:30%'>Sistem pakar v2</th><th style='width:9%'>Aturan</th><th>Bukti hasil inferensi</th></tr>")
ant = [a["label"] for a in V["antisipasi"] if a["terpicu"]]
rows = [
 ("Deteksi regime & bobot adaptif", "Bobot pilar sama di semua kondisi pasar; rasio dibaca dengan cara yang sama saat euforia maupun krisis.",
  "Skor stres 6 komponen (drawdown, CDS, net asing, kurs, yield SBN, breadth) → 4 regime. Bobot 9 pilar dan risiko per transaksi berubah otomatis.",
  "R-STR, R-REG, R-ADP", f"Regime <b>{E(regime['label'])}</b> (stres {P['skorStresPasar']}/12). Top pick statis vs adaptif berbeda: dibuang {', '.join(sorted(static - adapt))}; ditambah {', '.join(sorted(adapt - static))}."),
 ("Reaction function otoritas", "Menunggu BI/pemerintah mengumumkan kebijakan, lalu bereaksi.",
  "Ambang kondisi (kurs, inflasi, Brent, Fed, spread SBN-UST, drawdown, CDS) langsung mengaktifkan node transmisi kebijakan yang belum diumumkan.",
  "R-ANT", f"{len(ant)} antisipasi terpicu: " + "; ".join(E(x) for x in ant)),
 ("Geopolitik multi-hop berbasis berita", "Membaca berita lepas; dampak ke sektor ditebak.",
  "Berita kredibel ≤180 hari mengaktifkan peristiwa → rantai kausal → tailwind/headwind sektor → routing ke emiten lewat eksposur komoditas; provenans geopolitik ditelusuri.",
  "R-GEO", f"{len(r['peristiwaAktif'])} peristiwa aktif, {len(r['pergerakanAktif'])} node transmisi aktif; berita basi otomatis gugur."),
 ("Berpikir tingkat dua (refleksivitas)", "Berita bagus = beli, berita buruk = jual.",
  "Kekuatan relatif vs IHSG + jejak bandar: berita buruk yang tak lagi menekan harga = priced-in; berita bagus + kalah dari pasar + distribusi = sell the news.",
  "R-RS, R-REF", f"Mengungguli IHSG ≥5 pp: {lst('OutperformPasar')}."),
 ("Kapitulasi & akumulasi bertahap", "Memangkas target setelah crash (prosiklikal), atau all-in terlalu dini.",
  "Capitulation day + drawdown ≥40% + breadth washout + CDS tinggi → zona akumulasi generasional; bila CDS & rupiah belum membaik → beli 3 tranche bertangga ATR.",
  "R-PAS, R-KAP", f"Zona akumulasi generasional + dasar belum terkonfirmasi → tranche {'/'.join(str(x) for x in regime['tranche'])}. Kandidat: {lst('KandidatAkumulasiBertahap')}."),
 ("Konfirmasi intermarket", "Hanya melihat IHSG.", "CDS, rupiah, dan yield harus membaik lebih dulu sebelum dasar IHSG dianggap kredibel.", "R-PAS-05/06",
  "Dasar belum terkonfirmasi (CDS 92 → 99,7 bps; rupiah melemah)."),
 ("Arah ekspektasi laba", "PER statis dari laba historis.", "Revisi konsensus 3 bulan: revisi naik + murah + harga tertinggal = celah ekspektasi; murah + revisi turun = value trap dini.", "R-REV",
  f"Celah ekspektasi: {lst('CelahEkspektasiPositif')}. Value trap dini: {lst('MurahKarenaLabaTurun')}."),
 ("Valuasi relatif obligasi (ERP)", "Membandingkan PER dengan rata-rata historis saja.", "Earnings yield − yield SBN 10Y: saham yang kalah dari SBN tidak layak dibeli hanya karena 'turun banyak'.", "R-ERP",
  f"ERP ≥ 8 pp: {len([e for e in REAL if has(e, 'ERPSangatMenarik')])} emiten; ERP &lt; 0: {lst('MahalVsObligasi')}."),
 ("Bandarmology lanjutan", "Net buy/sell asing harian.", "Fase Wyckoff, akumulasi tersembunyi (bandar beli saat ritel panik), distribusi ke ritel, tipe broker akumulator, poin smart money (akumulasi × kekuatan relatif).", "R-BDR, R-ADP-01",
  f"Akumulasi tersembunyi: {lst('AkumulasiTersembunyi')}. Distribusi ke ritel: {lst('DistribusiKeRitel')}."),
 ("Tata kelola & manipulasi", "Tidak tercermin di rasio, sering terlewat.", "Free float &lt;15% (risiko HSC/dikeluarkan indeks), gadai saham pengendali, transaksi orang dalam, deteksi saham gorengan & pump-and-dump.", "R-GOV",
  f"Risiko HSC: {lst('RisikoHSC')}. Uji fiktif: gorengan, gadai, dan orang dalam terdeteksi benar."),
 ("Keputusan di bawah ketidakpastian", "Satu skenario (base case) dan satu angka target.", "Ekspektasi probabilistik 3 skenario, sektor robust (tahan semua skenario), asimetri upside/downside, konstruksi portofolio inti–satelit.", "R-ROB",
  f"Inti: {', '.join(inti)}. Satelit: {', '.join(sat)}."),
 ("Ingatan kasus terstruktur (CBR)", "Analogi sejarah anekdotal.", "Skor kemiripan berbobot vs 9 kasus krisis (1998–2025) → preseden sektor.", "R-CBR",
  "Analog: " + ", ".join(c["label"] for c in r["cbr"] if c["analog"]) + "."),
 ("Konfluensi & resolusi konflik", "Satu indikator favorit mendominasi.", "6 bendera pilar; konflik (fundamental vs bandar, momentum tanpa fundamental, distribusi saat euforia, murah karena laba turun) → tunggu konfirmasi.", "R-KON",
  f"Konfluensi tinggi: {lst('KonfluensiTinggi')}. Tunggu konfirmasi: {lst('TungguKonfirmasi')}."),
 ("Ukuran posisi & konsentrasi", "Rekomendasi 'beli' tanpa ukuran posisi.", "Ukuran = risiko per transaksi (regime) ÷ (2×ATR); deteksi dua top pick dengan eksposur komoditas sama.", "R-POS",
  f"Risiko/transaksi {F(regime['risiko'],2)}% (krisis). Konsentrasi tema: {lst('RisikoKonsentrasiTema')}."),
 ("Katalis & timing", "Kalender tidak sistematis.", "Katalis biner/musiman/terjadwal dengan hitung mundur; kandidat dengan katalis biner ≤45 hari wajib masuk bertahap.", "R-KAT",
  f"Strategi tranche sebelum katalis biner: {lst('StrategiTrancheKatalisBiner')}."),
 ("Tesis & kill switch", "Jarang menetapkan kapan analisisnya salah.", "Setiap tesis punya indikator kunci, ambang invalidasi, buffer, dan pemicu kontrarian; buffer &lt;10% = rapuh.", "R-TES",
  "Rapuh: " + (", ".join(t["label"] for t in V["tesis"] if "TesisRapuh" in t["kelas"]) or "–") + ". Belum terpicu: tesis kontrarian Keuangan (CDS &lt; 85) & Infrastruktur (SBN &lt; 6,75%)."),
 ("Kesadaran kualitas data", "Jarang menyatakan batas data.", "Umur data vs frekuensi pembaruan; rekomendasi berbasis data indikatif diberi label wajib verifikasi.", "R-DAT",
  f"{len(V['dataKedaluwarsa'])} indikator kedaluwarsa; {len([e for e in REAL if has(e, 'PerluVerifikasiData')])} rekomendasi ditandai PerluVerifikasiData."),
]
for a, b, c, d, e in rows:
    w(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td><code>{d}</code></td><td>{e}</td></tr>")
w("</table>")

# ---------------- 3 contoh jejak
w("<h2>3. Contoh Jejak Penalaran: Tiga Emiten, Tiga Kesimpulan Berbeda</h2>")
def trace(code, judul):
    e = EMI[code]
    s = sek[e["sektor"]]
    w(f"<h3>{judul}</h3><table><tr><th style='width:28%'>Langkah</th><th>Hasil</th></tr>")
    w(f"<tr><td>Analis biasa (skor statis)</td><td>{e['skorTotalEmiten']} → {'TOP PICK' if has(e, 'KandidatTopPick') else 'bukan top pick'}</td></tr>")
    w(f"<tr><td>Sektor ({E(s['label'])})</td><td>Base {s['skorOutlookBase']}, Bull {s['skorOutlookBull']}, Bear {s['skorOutlookBear']}, EV {F(s['skorEkspektasiProbabilistik'],2)} → kontribusi {e['skorKontribusiSektorEV']}</td></tr>")
    w(f"<tr><td>Pilar</td><td>Fundamental {e['skorFundamental']}/10 · valuasi {e['skorValuasi']}/3 · teknikal {e['skorTeknikal']}/7 · bandar {e['skorBandar']}/5 · sentimen {e['skorSentimen']} · smart money {e['poinSmartMoney']}/2 · penalti {e['penaltiRisiko']}</td></tr>")
    w(f"<tr><td>Konteks pakar</td><td>RS vs IHSG {F(e['kekuatanRelatifPersen'])} pp · ERP {F(e['equityRiskPremium'])} pp · revisi EPS {F(e['revisiEPS3BulanPersen'],0)}% · konfluensi {e['skorKonfluensi']}/6</td></tr>")
    k = [c for c in e["kelas"] if c not in ("InferensiEmiten", "KategoriInferensi")]
    w(f"<tr><td>Kelas inferensi</td><td>{', '.join(k)}</td></tr>")
    concl = []
    if has(e, "KandidatTopPickAdaptif"): concl.append("TOP PICK ADAPTIF")
    if has(e, "KandidatAkumulasiBertahap"): concl.append(f"AKUMULASI BERTAHAP (T1 {F(e['hargaTranche1'],0)} / T2 {F(e['hargaTranche2'],0)} / T3 {F(e['hargaTranche3'],0)})")
    if has(e, "TungguKonfirmasi"): concl.append("TUNGGU KONFIRMASI")
    w(f"<tr><td><b>Kesimpulan sistem pakar</b></td><td><b>{' · '.join(concl) or 'Tidak direkomendasikan'}</b> — skor adaptif {F(e['skorAdaptifRegime'])} (ambang {F(regime['ambang'])}), ukuran posisi maks {F(e['ukuranPosisiMaksPersen'])}% modal</td></tr></table>")
trace("BBCA", "BBCA — sektor bearish, tetapi kualitas yang terpukul: akumulasi bertahap")
trace("BRMS", "BRMS — top pick analis biasa, dibuang sistem pakar")
trace("ANTM", "ANTM — disepakati keduanya, keyakinan tinggi")

# ---------------- 4 sumber data
w("<h2>4. Sumber Data</h2>")
w("<p>Setiap sumber tercatat di ontologi sebagai individu <code>SumberData</code> dengan jenis akses, format, dan skor kredibilitas. Indikator dihubungkan lewat <code>diperolehDari</code>.</p>")
w("<table><tr><th>Sumber</th><th>Jenis</th><th>Akses</th><th>Format</th><th>Kred.</th><th>Data yang dipakai</th></tr>")
for (n, cls, l, akses, fmt, kred, url, d) in SRC.SUMBER:
    w(f"<tr><td><b>{E(l)}</b><br><span style='color:#777'>{E(url)}</span></td><td>{cls.replace('SumberData', '')}</td><td>{E(akses)}</td><td>{E(fmt)}</td><td>{kred:.2f}</td><td>{E(d)}</td></tr>")
w("</table>")
w("<div class='warn'>Akses: data resmi (IDX, KSEI, BI, BPS, FRED) cukup untuk versi akademik. Konsensus EPS, CDS real-time, dan kepemilikan institusi umumnya butuh terminal berbayar; dalam proyek ini nilainya indikatif dan diberi penanda <code>DataIndikatif</code>.</div>")

# ---------------- 5 katalog indikator
st_count = collections.Counter(x[7] for x in SRC.K)
sf_count = collections.Counter(x[3] for x in SRC.K)
w("<h2>5. Katalog Indikator yang Bisa Masuk</h2>")
w(f"<p>{len(SRC.K)} indikator: <span class='st-T'>{st_count['Terintegrasi v2']} terintegrasi v2</span> (sudah dipakai aturan), <span class='st-S'>{st_count['Siap Integrasi']} siap integrasi</span> (struktur siap, tinggal pipeline), "
  f"<span class='st-R'>{st_count['Roadmap']} roadmap</span>. Sifat waktu: {sf_count['Leading']} leading, {sf_count['Coincident']} coincident, {sf_count['Lagging']} lagging. "
  "Pakar memberi bobot lebih pada indikator <b>leading</b> (CDS, revisi konsensus, breadth, PMI, GPR) karena harga bergerak mendahului laporan keuangan.</p>")
srcname = {s[0]: s[2].split(" (")[0] for s in SRC.SUMBER}
by = collections.OrderedDict()
for x in SRC.K:
    by.setdefault(x[2], []).append(x)
w("<table><tr><th style='width:14%'>Pilar</th><th style='width:24%'>Indikator</th><th>Sifat</th><th>Frekuensi</th><th style='width:22%'>Sumber</th><th>Status</th><th>Dipakai untuk</th></tr>")
for pil, items in by.items():
    for j, (n, l, pilar, sifat, frek, fh, src, status, cat) in enumerate(items):
        cl = {"Terintegrasi v2": "st-T", "Siap Integrasi": "st-S", "Roadmap": "st-R"}[status]
        w(f"<tr><td>{'<b>' + E(pil) + '</b>' if j == 0 else ''}</td><td>{E(l)}</td><td>{sifat}</td><td>{E(frek)}</td><td>{E(', '.join(srcname[s] for s in src))}</td><td class='{cl}'>{status}</td><td>{E(cat)}</td></tr>")
w("</table>")

# ---------------- 6 pipeline
w("<h2>6. Rancangan Pipeline Data Otomatis (Roadmap)</h2>")
w("<table><tr><th>Tahap</th><th>Sumber → properti ontologi</th><th>Frekuensi</th><th>Metode</th></tr>")
for a, b, c, d in [
 ("1. Makro global", "FRED, Fed, EIA → <code>Makro_FedFundsRate</code>, <code>Makro_UST10Y</code>, <code>Makro_Brent</code>, <code>KondisiPasar</code>", "Harian", "API resmi (FRED/EIA) + parser rilis FOMC"),
 ("2. Makro domestik", "BI, BPS, Kemenkeu → BI-Rate, inflasi, yield SBN, defisit", "Harian–bulanan", "Unduh Excel/CSV terjadwal"),
 ("3. Pasar & aliran", "IDX ringkasan perdagangan & transaksi asing, KSEI kepemilikan → <code>netAsing20HariM</code>, breadth, kepemilikan asing", "Harian/bulanan", "Unduh berkas resmi + agregasi"),
 ("4. Fundamental", "IDX XBRL laporan keuangan → rasio emiten; konsensus (terminal) → <code>revisiEPS3BulanPersen</code>", "Kuartalan", "Parser XBRL + rumus rasio"),
 ("5. Tata kelola", "Keterbukaan informasi IDX (laporan kepemilikan, gadai, transaksi direksi) → <code>sahamDigadaikanPersen</code>, <code>transaksiOrangDalam</code>", "Harian", "Pemantauan pengumuman + ekstraksi teks"),
 ("6. Bandarmology", "Broker summary (aplikasi broker) → <code>skorAccDistBroker</code>, <code>konsentrasiBrokerTop3Persen</code>", "Harian", "Ekspor data langganan"),
 ("7. Geopolitik", "GDELT + GPR Index + media → <code>Berita</code>, aktivasi <code>PeristiwaGeopolitik</code> otomatis", "15 menit–harian", "Kueri GDELT + sentiment_scorer"),
 ("8. Indeks", "MSCI/FTSE/S&P pengumuman → <code>Katalis</code>, keanggotaan indeks", "Kuartalan", "Pemantauan halaman pengumuman"),
 ("9. Reasoning & monitoring", "Pellet/Drools → kelas inferensi; kill switch dicek setiap pembaruan indikator kunci", "Harian", "run_all.sh terjadwal + notifikasi saat TesisGugur/TesisRapuh"),
 ("10. Backtest", "Walk-forward 2013–2026 vs IHSG/LQ45 → kalibrasi ambang & bobot regime (komponen <20%)", "Kuartalan", "Validasi panel pakar (Stk_PanelPakar)")]:
    w(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>")
w("</table>")

# ---------------- 7 daftar aturan v2
w("<h2>7. Daftar Aturan SWRL Baru v2</h2>")
w("<table><tr><th style='width:11%'>Kode</th><th style='width:18%'>Modul</th><th>Penjelasan</th></tr>")
for code, pilar, desc, body in RULES:
    pre = code.split("-")[1]
    if pre in v2codes or code in ("R-PRF-08", "R-PRF-09"):
        w(f"<tr><td><code>{code}</code></td><td>{E(pilar)}</td><td>{E(desc)}</td></tr>")
w("</table>")

# ---------------- 8 batasan
w("<h2>8. Batasan & Etika</h2><ul>"
  "<li>Angka rasio, teknikal, bandarmology, dan revisi konsensus per emiten bersifat <b>indikatif</b>; data gadai saham & transaksi orang dalam emiten nyata belum diisi (bernilai 0) sehingga aturan tata kelola dibuktikan dengan emiten fiktif <code>UJI_*</code>.</li>"
  "<li>Ambang &amp; bobot regime adalah heuristik pakar awal; harus dikalibrasi lewat backtest walk-forward dan divalidasi panel pakar. Beberapa kandidat berada tepat di sekitar ambang (mis. skor 24,5 vs ambang 24,7), sehingga sensitivitas ambang wajib diuji.</li>"
  "<li>SWRL bersifat monoton (tanpa negation-as-failure dan tanpa agregasi); agregasi seperti breadth dihitung di luar reasoner dan dicatat sebagai data.</li>"
  "<li>Sistem diposisikan sebagai alat riset & edukasi di aplikasi sekuritas, bukan nasihat investasi personal (lihat <code>Stk_OJK_Kepatuhan</code>).</li></ul>")
w("</body></html>")

tmp = tempfile.mkdtemp(); hp = os.path.join(tmp, "b.html")
open(hp, "w", encoding="utf-8").write("\n".join(H))
dst = os.path.join(OUT, "DOKUMEN_PENGEMBANGAN_v2.pdf")
footer = '<div style="font-size:7pt;width:100%;text-align:center;color:#777">Dokumen Pengembangan v2 · SahamExpertKB · Kelompok 9 KBR · Halaman <span class="pageNumber"></span>/<span class="totalPages"></span></div>'
js = os.path.join(tmp, "p.js")
open(js, "w").write(f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}');await p.pdf({{path:{json.dumps(dst)},format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
footerTemplate:{json.dumps(footer)},margin:{{top:'15mm',bottom:'17mm',left:'14mm',right:'14mm'}}}});await b.close();}})();""")
subprocess.run(["node", js], check=True)
print("PDF:", dst)
