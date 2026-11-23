# -*- coding: utf-8 -*-
"""PANDUAN PRESENTASI SahamExpertKB: roadmap bergambar, arsitektur sampai dashboard,
naskah demo dashboard per panel, rencana cadangan, dan glosarium lengkap.
Pakai: python3 tools/make_panduan_presentasi.py   (butuh Node.js + Playwright)"""
import base64, io, json, os, subprocess, sys, tempfile
from html import escape as E
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tools", "buku"))
import diagram as D  # noqa: E402

IMG = os.path.join(HERE, "docs", "img2")
LOGO = os.path.join(HERE, "dashboard", "assets", "logo_kbr.png")
DST = os.path.join(HERE, "output", "PANDUAN_PRESENTASI_SahamExpertKB.pdf")
VAL = {}
for ln in open(os.path.join(HERE, "output", "validasi_owlapi_pellet.txt"), encoding="utf-8"):
    for kv in ln.split():
        if "=" in kv:
            k, v = kv.split("=", 1); VAL[k] = v
fmtn = lambda x: f"{int(x):,}".replace(",", ".")

def b64img(path, maxw=1700, q=84):
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def b64png(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()

H = []
w = H.append
FN = [0]
def fig(html, cap):
    FN[0] += 1; w(f'<figure>{html}<figcaption>Gambar {FN[0]}. {cap}</figcaption></figure>')
def shot(name, cap, width="100%"):
    p = os.path.join(IMG, name)
    if os.path.exists(p): fig(f'<img src="{b64img(p)}" style="width:{width}">', cap)
def table(head, rows, widths=None):
    cg = "".join(f'<col style="width:{x}">' for x in widths) if widths else ""
    w(f"<table><colgroup>{cg}</colgroup><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
      "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table>")
def note(s, k="info"):
    lbl = {"info": "Intinya", "say": "Ucapkan", "tip": "Tips", "warn": "Perhatian"}[k]
    w(f'<div class="note {k}"><b>{lbl}.</b> {s}</div>')

# =============================================================== SVG: ROADMAP
def roadmap():
    steps = [
        ("Masalah &amp; CQ", "investor ritel sulit menggabung", "banyak analisis; 12 competency", "questions"),
        ("Akuisisi pengetahuan", "heuristik analis + data IDX,", "BI, BPS, 71 berita", ""),
        ("Reuse ontologi", "W3C (RDF/OWL/SWRL) +", "FIBO, schema.org, SKOS", ""),
        ("Rancang TBox", "298 kelas, 65 object &amp;", "220 data property", ""),
        ("Isi ABox dari CSV", "owlready2 membangun", "1.392 individu otomatis", ""),
        ("Tulis aturan SWRL", "303 aturan berkode &amp;", "berpilar (interval, built-in)", ""),
        ("Reasoning Pellet", "konsisten · SROIQ(D) ·", "+7.943 aksioma inferensi", ""),
        ("Uji knowledge base", "103/103 soal lulus", "(12 CQ + what-if)", ""),
        ("Sajikan di Fuseki", "SPARQL lewat HTTP · 2 dataset", "· 305 aturan Jena", ""),
        ("Dashboard live", "visual, what-if, 100", "pertanyaan bervisual", ""),
    ]
    W, Hh = 1000, 560
    xs = [100, 285, 470, 655, 840]
    pos = [(x, 110) for x in xs] + [(x, 380) for x in reversed(xs)]
    s = [f'<svg viewBox="0 0 {W} {Hh}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, Arial">']
    s.append('<defs><linearGradient id="rg" x1="0" x2="1"><stop offset="0" stop-color="#e04a55"/><stop offset="1" stop-color="#7a0e17"/></linearGradient></defs>')
    # jalur berkelok
    d = f"M{pos[0][0]} {pos[0][1]} L{pos[4][0]} {pos[4][1]} C{pos[4][0]+150} {pos[4][1]} {pos[5][0]+150} {pos[5][1]} {pos[5][0]} {pos[5][1]} L{pos[9][0]} {pos[9][1]}"
    s.append(f'<path d="{d}" fill="none" stroke="#f6d3d6" stroke-width="26" stroke-linecap="round"/>')
    s.append(f'<path d="{d}" fill="none" stroke="url(#rg)" stroke-width="6" stroke-dasharray="2 12" stroke-linecap="round"/>')
    fase = [("FASE 1 · MERANCANG KNOWLEDGE BASE", 30), ("FASE 2 · MENALAR, MENGUJI, MENYAJIKAN", 300)]
    for t, y in fase:
        s.append(f'<text x="30" y="{y}" font-size="13" font-weight="700" fill="#a8131f" letter-spacing="2">{t}</text>')
    for i, ((x, y), (t, a, b, c)) in enumerate(zip(pos, steps)):
        col = "#7a0e17" if i in (6, 9) else "#a8131f"
        s.append(f'<circle cx="{x}" cy="{y}" r="27" fill="{col}" stroke="#fff" stroke-width="5"/>')
        s.append(f'<text x="{x}" y="{y+7}" text-anchor="middle" font-size="20" font-weight="800" fill="#fff">{i+1}</text>')
        ty = y + 52
        s.append(f'<text x="{x}" y="{ty}" text-anchor="middle" font-size="14.5" font-weight="800" fill="#1f1416">{t}</text>')
        for j, ln in enumerate([a, b, c]):
            if ln: s.append(f'<text x="{x}" y="{ty+18+j*15}" text-anchor="middle" font-size="11.5" fill="#5d4a4d">{ln}</text>')
    s.append('<text x="960" y="545" text-anchor="end" font-size="11" fill="#7c6b6e">Semua tahap 3–8 dijalankan ulang dengan satu perintah: python3 run_all.py</text>')
    s.append("</svg>")
    return "".join(s)

# =============================================================== SVG: ARSITEKTUR SAMPAI DASHBOARD
def arsitektur():
    W, Hh = 1000, 620
    s = [f'<svg viewBox="0 0 {W} {Hh}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, Arial">',
         '<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#a8131f"/></marker></defs>']
    def box(x, y, w_, h, t, lines, fill="#fff", stroke="#e9c9cd", tc="#7a0e17"):
        s.append(f'<rect x="{x}" y="{y}" width="{w_}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
        s.append(f'<text x="{x+w_/2}" y="{y+24}" text-anchor="middle" font-size="14" font-weight="800" fill="{tc}">{t}</text>')
        for i, l in enumerate(lines):
            s.append(f'<text x="{x+w_/2}" y="{y+44+i*16}" text-anchor="middle" font-size="11.5" fill="{"#fff" if fill.startswith("#7") or fill.startswith("#8") else "#4a3b3e"}">{l}</text>')
    def arrow(x1, y1, x2, y2, lbl=None, lx=None, ly=None):
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#a8131f" stroke-width="2" marker-end="url(#ar)"/>')
        if lbl: s.append(f'<text x="{lx}" y="{ly}" font-size="10.5" fill="#a8131f" font-weight="700">{lbl}</text>')
    lay = [("1 · SUMBER", 38), ("2 · DATA", 158), ("3 · KNOWLEDGE BASE", 278), ("4 · PENALARAN", 398), ("5 · PENYAJIAN", 518)]
    for t, y in lay:
        s.append(f'<rect x="10" y="{y-26}" width="980" height="112" rx="16" fill="{"#fff8f9" if lay.index((t, y)) % 2 == 0 else "#fdf0f2"}"/>')
        s.append(f'<text x="24" y="{y-8}" font-size="11" font-weight="800" fill="#a8131f" letter-spacing="1.5">{t}</text>')
    box(150, 22, 220, 70, "Data pasar &amp; laporan", ["IDX, situs emiten, BI, BPS, The Fed"])
    box(420, 22, 200, 70, "Berita keuangan", ["71 berita · Bisnis, Kontan, …"])
    box(670, 22, 260, 70, "Pengetahuan pakar", ["ambang rasio, heuristik, logika makro"])
    box(150, 142, 300, 70, "data/*.csv", ["emiten, makro, berita, kondisi pasar"])
    box(520, 142, 240, 70, "validasi_data.py + sentimen", ["cek kolom &amp; skor berita"])
    box(150, 262, 330, 74, "build_ontology.py (owlready2)", ["kb_*.py (TBox) + CSV (ABox) + rules (303 SWRL)"])
    box(560, 262, 190, 74, "SahamExpertKB_v2.owl", ["15.519 aksioma · SROIQ(D)"], fill="#7a0e17", stroke="#7a0e17", tc="#fff")
    box(790, 262, 170, 74, "Modul alignment", ["FIBO · schema.org · SKOS"])
    box(150, 382, 230, 74, "Pellet (OWLAPI)", ["konsistensi · klasifikasi · SWRL"])
    box(440, 382, 230, 74, "…_inferred.owl", ["+7.943 aksioma inferensi"], fill="#7a0e17", stroke="#7a0e17", tc="#fff")
    box(730, 382, 230, 74, "swrl2jena.py", ["303 SWRL → 305 aturan Jena"])
    box(40, 502, 190, 80, "Protégé", ["DL Query · SWRLTab", "explanation (?)"])
    box(270, 502, 300, 80, "Apache Jena Fuseki :3030", ["/saham-pellet (hasil Pellet)", "/saham (Jena live + update)"], fill="#7a0e17", stroke="#7a0e17", tc="#fff")
    box(610, 502, 150, 80, "server.py :8080", ["halaman + proxy", "/fuseki → :3030"])
    box(800, 502, 170, 80, "Dashboard (browser)", ["Chart.js · 100 pertanyaan", "what-if"])
    arrow(260, 92, 260, 140); arrow(520, 92, 400, 140); arrow(800, 92, 470, 262)
    arrow(300, 212, 300, 260); arrow(640, 212, 450, 260)
    arrow(480, 299, 558, 299); arrow(750, 299, 788, 299, "imports", 752, 292)
    arrow(600, 336, 300, 380); arrow(380, 419, 438, 419); arrow(700, 336, 830, 380)
    arrow(250, 456, 140, 500, "buka .owl", 130, 486); arrow(555, 456, 420, 500, "dimuat", 500, 486); arrow(845, 456, 520, 500, "aturan", 700, 486)
    arrow(570, 542, 608, 542); arrow(760, 542, 798, 542, "SPARQL/JSON", 742, 532)
    s.append("</svg>")
    return "".join(s)

# =============================================================== KONTEN
CSS = """@page{size:A4;margin:15mm 14mm 17mm 14mm}*{box-sizing:border-box}
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:9.8pt;color:#1f1416;line-height:1.5}
h1{font-size:22pt;color:#7a0e17;margin:0 0 6px;letter-spacing:-.3px}
h2{font-size:14pt;color:#7a0e17;margin:18px 0 6px;padding-bottom:3px;border-bottom:2px solid #f6d3d6;break-after:avoid}
h3{font-size:11pt;margin:12px 0 4px;color:#1f1416;break-after:avoid}
p{margin:4px 0 7px;text-align:justify}ul,ol{margin:4px 0 8px;padding-left:20px}li{margin:2px 0}
table{border-collapse:collapse;width:100%;margin:6px 0 12px;font-size:8.8pt}
th{background:#fdecee;color:#7a0e17;text-align:left;padding:5px 6px;border:1px solid #f0d5d8}
td{padding:4px 6px;border:1px solid #f0e2e4;vertical-align:top}tr{break-inside:avoid}
figure{margin:8px 0 12px;text-align:center;break-inside:avoid}figure img{border:1px solid #f0d5d8;border-radius:8px}
figcaption{font-size:8.4pt;color:#7c6b6e;margin-top:3px}
.note{border-left:4px solid #a8131f;background:#fdf2f3;padding:6px 10px;margin:7px 0 10px;border-radius:0 8px 8px 0;font-size:9.3pt;break-inside:avoid}
.note.say{border-color:#1d8a57;background:#eef8f3}.note.tip{border-color:#b86e00;background:#fff6e6}.note.warn{border-color:#c8202d;background:#fde6e8}
code{font-family:'DejaVu Sans Mono',monospace;font-size:8.4pt;background:#fdecee;color:#7a0e17;padding:0 3px;border-radius:3px}
pre{font-family:'DejaVu Sans Mono',monospace;font-size:8.2pt;background:#1c0b0e;color:#ffd9dd;padding:8px 10px;border-radius:7px;white-space:pre-wrap;break-inside:avoid}
.pb{break-after:page}
.cover{height:262mm;display:flex;flex-direction:column;justify-content:space-between;padding:16mm 6mm 0}
.cover img.logo{width:70mm}
.cover h1{font-size:32pt;line-height:1.08;margin-top:14mm}.cover .sub{font-size:13pt;color:#4a3b3e;max-width:160mm}
.cover .meta{border-top:3px solid #7a0e17;padding-top:8px;color:#5d4a4d;font-size:10pt}
.step{display:grid;grid-template-columns:62px 1fr;gap:10px;border:1px solid #f0d5d8;border-radius:10px;padding:8px 10px;margin:7px 0;break-inside:avoid}
.step .t{background:#7a0e17;color:#fff;border-radius:8px;text-align:center;font-weight:800;padding:6px 2px;font-size:9pt;line-height:1.25}
.step b.h{font-size:10.3pt;color:#7a0e17}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.chk{list-style:none;padding-left:0}.chk li:before{content:"☐  ";color:#a8131f;font-weight:800}
.gl td:first-child{font-weight:700;width:27%}"""

w(f"""<div class="cover"><div><img class="logo" src="{b64png(LOGO)}"><h1>Panduan Presentasi<br>SahamExpertKB</h1>
<p class="sub">Roadmap dari nol sampai dashboard, arsitektur sistem, naskah demo dashboard panel demi panel, rencana cadangan, dan glosarium semua istilah.</p></div>
<div>{roadmap()}</div>
<div class="meta">Kelompok 9 · Knowledge Based Reasoning · Jonnathan Azarel Gunawan (L0224005) &amp; Gloria Dana Praysilia (L0224043)<br>
{VAL.get('CLASSES')} kelas · {fmtn(VAL.get('INDIVIDUALS'))} individu · {VAL.get('SWRL_RULES')} aturan SWRL · {fmtn(VAL.get('TOTAL_AXIOMS'))} aksioma · data acuan 19 November 2026</div></div><div class="pb"></div>""")

# ---------------------------------------------------- 1. alur presentasi
w('<h1>1. Alur presentasi (±12 menit)</h1>')
w('<p>Urutan ini dirancang supaya dosen lebih dulu paham <b>masalah</b> dan <b>cara berpikir sistem</b>, baru melihat dashboard sebagai bukti. Bagian demo dashboard (langkah 5) adalah inti presentasi.</p>')
ALUR = [
    ("0:00–1:00", "Pembuka &amp; masalah", "Perkenalkan tim dan judul. Masalahnya: investor ritel kesulitan menggabungkan fundamental, teknikal, bandarmology, berita, dan makro, terutama saat pasar krisis seperti 2026 (IHSG turun ±40%, asing jual ±Rp97 T)."),
    ("1:00–2:30", "Kenapa sistem pakar", "Data krisis sedikit sehingga ML sulit dilatih dan sulit dijelaskan. Pengetahuan pakar justru berupa aturan JIKA–MAKA. Porsi KB 98%, ML hanya skor sentimen."),
    ("2:30–4:00", "Roadmap pembangunan", "Tunjukkan Gambar 1 (roadmap 10 langkah): masalah → akuisisi → reuse ontologi → TBox → ABox → SWRL → Pellet → uji → Fuseki → dashboard."),
    ("4:00–5:30", "Arsitektur", "Tunjukkan Gambar 2: CSV → owlready2 → OWL + 303 SWRL → Pellet → Fuseki (dua dataset) → server.py → dashboard. Sebut SROIQ(D) dan modul alignment FIBO."),
    ("5:30–10:30", "Demo dashboard", "Ikuti naskah Bab 3 panel demi panel, termasuk what-if Kapitulasi dan satu-dua pertanyaan dari 100 Pertanyaan."),
    ("10:30–11:30", "Bukti &amp; validasi", "103/103 uji lulus, konsisten menurut Pellet, Pellet = Jena (dua mesin, hasil identik). Opsional: Protégé, klik ANTM, tunjukkan baris kuning dan tombol ?."),
    ("11:30–12:00", "Penutup", "Keterbatasan (data manual, belum backtest) dan rencana (data otomatis, backtest, API sekuritas). Sistem ini alat bantu analisis, bukan nasihat investasi."),
]
for t, h, s in ALUR:
    w(f'<div class="step"><div class="t">{t}</div><div><b class="h">{h}</b><br>{s}</div></div>')
note("\"Kami membangun sistem pakar yang tidak hanya memberi skor saham, tetapi juga tahu kondisi pasar sedang apa, menyesuaikan cara menilai, menguji tiga skenario masa depan, dan tahu kapan tesisnya salah.\"", "say")

w('<div class="pb"></div><h1>2. Roadmap &amp; arsitektur</h1>')
w('<h2>2.1 Roadmap: langkah dari awal sampai akhir</h2>')
fig(roadmap(), "Roadmap pembangunan SahamExpertKB, 10 langkah dalam dua fase.")
table(["#", "Langkah", "Apa yang dikerjakan", "Hasil / bukti"], [
    ["1", "Masalah &amp; competency questions", "menetapkan domain, stakeholder, dan 12 pertanyaan yang wajib dijawab KB", "proposal, daftar CQ"],
    ["2", "Akuisisi pengetahuan &amp; data", "heuristik analis, ambang rasio, data IDX/BI/BPS, 71 berita", "<code>data/*.csv</code>, log sumber"],
    ["3", "Reuse ontologi eksternal", "fondasi W3C; pemetaan ke FIBO, schema.org, SKOS, Dublin Core", "<code>SahamExpertKB_alignment.ttl</code>"],
    ["4", "Rancang TBox", "kelas entitas, pengetahuan, kesimpulan; properti; domain-range; disjoint", "298 kelas, 285 properti"],
    ["5", "Isi ABox dari CSV", "owlready2 membangun individu dan nilai properti otomatis", "1.392 individu"],
    ["6", "Tulis aturan SWRL", "interval berpasangan, built-in aritmetika, aturan berantai, meta-penalaran", "303 aturan, 1.656 atom"],
    ["7", "Reasoning Pellet", "cek konsistensi, klasifikasi, eksekusi aturan, ekspor inferensi", "konsisten, SROIQ(D), +7.943 aksioma"],
    ["8", "Uji knowledge base", "12 CQ, 98 soal statis, 5 what-if", "103/103 lulus"],
    ["9", "Sajikan di Fuseki", "SWRL → aturan Jena; dataset /saham-pellet dan /saham", "endpoint SPARQL :3030"],
    ["10", "Dashboard live", "visual, logo emiten, what-if, 100 pertanyaan bervisual", "http://localhost:8080"],
], ["5%", "22%", "48%", "25%"])
w('<h2>2.2 Arsitektur sampai ke tahap dashboard</h2>')
fig(arsitektur(), "Arsitektur berlapis: dari sumber data sampai dashboard di browser.")
table(["Lapisan", "Komponen", "Fungsinya"], [
    ["Sumber", "IDX, BI, BPS, media, pengetahuan pakar", "asal fakta dan aturan"],
    ["Data", "<code>data/*.csv</code>, <code>validasi_data.py</code>, <code>sentiment_scorer.py</code>", "menyimpan fakta dalam bentuk yang mudah diperbarui berdua; skor sentimen berita"],
    ["Knowledge base", "<code>build_ontology.py</code>, <code>kb_*.py</code>, <code>rules_*.py</code> → <code>SahamExpertKB_v2.owl</code>", "merakit ontologi OWL + 303 aturan SWRL"],
    ["Penalaran", "Pellet (owlready2 &amp; OWLAPI), <code>swrl2jena.py</code>", "menarik kesimpulan; menerjemahkan aturan untuk Fuseki"],
    ["Penyajian", "Protégé, Apache Jena Fuseki, <code>dashboard/server.py</code>, dashboard", "melihat, melayani SPARQL, dan menampilkan hasil ke pengguna"],
], ["16%", "44%", "40%"])
w('<h2>2.3 Apa yang terjadi saat dashboard dibuka</h2>')
ol = ["Browser memuat <code>index.html</code>, <code>style.css</code>, <code>app.js</code>, Chart.js, dan daftar 100 query dari <code>server.py</code> (port 8080).",
      "Setiap panel mengirim query SPARQL ke <code>/fuseki/saham-pellet/query</code>. <code>server.py</code> meneruskannya ke Fuseki di port 3030 (proxy, agar tidak terkena CORS).",
      "Fuseki menjalankan query terhadap graf RDF lalu mengembalikan JSON standar SPARQL.",
      "<code>app.js</code> mengubah JSON menjadi kartu, grafik Chart.js, SVG, atau tabel, lengkap dengan logo emiten.",
      "Tombol <b>Jena live</b> mengganti dataset ke <code>/saham</code>, yang dinalar langsung oleh 305 aturan Jena. Tombol what-if mengirim SPARQL UPDATE ke <code>/saham/update</code>, aturan menalar ulang, dan dashboard membandingkan sebelum vs sesudah."]
w("<ol>" + "".join(f"<li>{x}</li>" for x in ol) + "</ol>")
fig(D.d_dashboard(), "Tiga program yang bekerja sama: browser, server.py, dan Fuseki.")

# ---------------------------------------------------- 3. naskah demo
w('<div class="pb"></div><h1>3. Cara mempresentasikan dashboard</h1>')
w('<p>Untuk setiap panel ada tiga hal: <b>apa yang diklik</b>, <b>apa yang diucapkan</b>, dan <b>angka kunci</b> yang perlu disebut. Gulir dari atas ke bawah mengikuti menu: Ringkasan → Sektor → Emiten → Bedah → Tesis &amp; Risiko → Geopolitik → What-if → 100 Pertanyaan.</p>')
PANEL = [
    ("p_header.png", "3.1 Ringkasan: regime pasar", "Tidak perlu klik. Tunjuk lampu hijau di kanan atas, lalu kartu merah regime.",
     "Setiap angka di halaman ini ditanyakan langsung ke knowledge base lewat SPARQL. Enam indikator stres memberi skor 11 dari 12, jadi sistem menyimpulkan pasar sedang Krisis Likuiditas. Akibatnya bobot fundamental, valuasi, risiko, dan smart money dinaikkan 1,5 kali, sedangkan teknikal dan sentimen diturunkan menjadi 0,5.",
     "Skor stres 11/12 · CDS 99,6 (premi risiko tinggi) · drawdown −39,3% (belum kapitulasi, batasnya −40%) · emas 3.746 (tesis gugur)."),
    ("p_skcards.png", "3.2 Sektor inti dan satelit", "Tunjuk empat kartu sektor.",
     "Setiap sektor dinilai di tiga skenario: base, bull, dan bear. Sektor inti adalah sektor yang tetap positif di semua skenario, yaitu Barang Baku dan Kesehatan. Sektor satelit adalah taruhan kecil dengan potensi naik jauh lebih besar dari risikonya, yaitu Infrastruktur dan Keuangan.",
     "Barang Baku: base 11, ekspektasi 10,75 · Kesehatan: 8 / 7,5 · Keuangan: −10 sampai 19."),
    ("p_sektor.png", "3.3 Rentang skor dan peta panas", "Tunjuk grafik rentang (kiri) dan peta panas (kanan).",
     "Garis menunjukkan rentang dari skenario terburuk sampai terbaik. Garis pendek di kanan nol berarti robust, seperti Kesehatan. Perhatikan Energi: di skenario bull skornya justru turun, karena harga minyak ikut turun ketika ketegangan geopolitik mereda. Ini bukti sistem menalar, bukan sekadar mengikuti pasar.",
     "Ekspektasi = 0,5 × base + 0,25 × bull + 0,25 × bear."),
    ("p_picks.png", "3.4 Top pick sistem pakar", "Tunjuk kartu berlogo; klik ANTM.",
     "Ini tujuh saham pilihan sistem pakar, diurutkan menurut skor adaptif. Setiap kartu menunjukkan skor statis, potensi naik ke nilai wajar, dan batas posisi maksimum dari manajemen risiko.",
     "ANTM 35 · TINS 33 · LSIP 29,5 · AADI 29 · JPFA 26,5 · NCKL 26,5 · MIKA 26."),
    ("p_pick.png", "3.5 Analis biasa vs sistem pakar", "Tunjuk grafik batang dan peta sebaran.",
     "Analis biasa menjumlah delapan pilar dengan bobot sama dan hanya memilih empat saham. Sistem pakar menyesuaikan bobot dengan regime dan menemukan tiga peluang tambahan: AADI, JPFA, dan LSIP. Di peta sebaran, garis putus-putus adalah ambang top pick saat krisis, 24,7.",
     "Analis biasa 4 saham · sistem pakar 7 saham · ambang krisis 24,7."),
    ("p_bedah.png", "3.6 Bedah satu emiten (ANTM)", "Setelah klik ANTM, halaman turun ke panel ini.",
     "Setiap rekomendasi bisa dibedah. ANTM kuat di fundamental (9) dan teknikal (7), sentimennya sedikit negatif. Level harga dihitung dari volatilitas: stop loss 2.697, take profit 3.204,5, nilai wajar 5.220. Di bawahnya ada 26 kelas yang disimpulkan reasoner, termasuk peringatan bahwa ANTM dan NCKL sama-sama bergantung pada nikel.",
     "Statis 27 → adaptif 35 · posisi maks 7,1% modal · upside 80%."),
    ("p_risiko.png", "3.7 Tesis dan kill switch", "Tunjuk tesis emas (merah, Gugur).",
     "Pakar yang baik tahu kapan dia salah. Setiap sektor pilihan punya indikator kunci dan batas gugur. Titik adalah nilai sekarang, garis merah adalah batasnya. Harga emas 3.745 sudah di bawah 3.800, jadi tesis emas gugur dan Barang Baku otomatis ditandai untuk dipantau ketat.",
     "Emas gugur · Brent valid (91,95 &gt; 75) · Kesehatan &amp; Infrastruktur rapuh (jarak &lt; 10%)."),
    ("p_geo.png", "3.8 Geopolitik, katalis, dan CBR", "Tunjuk empat kolom rantai, lalu grafik kemiripan.",
     "Berita tidak hanya diberi skor positif atau negatif. Sistem menelusuri rantai sebab-akibatnya sampai ke sektor. Di kanan ada kalender katalis dan perbandingan dengan sembilan krisis historis; yang paling mirip adalah 2022 dan 2018.",
     "17 jalur sebab-akibat · katalis terdekat: MSCI review 12 hari lagi · analog 2022 (17) dan 2018 (15)."),
    ("p_whatif.png", "3.9 Demo what-if (wajib)", "Klik Kapitulasi IHSG, tunggu ±2 detik, tunjuk baris bertanda ◀, lalu klik Reset.",
     "Ini bukti bahwa sistemnya benar-benar menalar. Saya ubah datanya: IHSG turun 45% dengan satu hari crash 10,5%. Perintah SPARQL UPDATE dikirim ke Fuseki, 305 aturan menalar ulang di server, dan sistem langsung menyimpulkan kapitulasi lalu memunculkan lima kandidat akumulasi bertahap.",
     "Kapitulasi: tidak → ya · kandidat: BBCA, BMRI, CPIN, MIKA, UNTR · update ±1 detik."),
    ("p_tanya.png", "3.10 100 Pertanyaan", "Klik 2–3 pertanyaan, misalnya no. 24, 2, dan 36. Klik tombol SPARQL untuk menunjukkan query-nya.",
     "Kami menyiapkan 100 pertanyaan penting. Setiap jawaban adalah query SPARQL yang dijalankan langsung ke Fuseki, lalu dashboard memilih bentuk visual yang paling cocok.",
     "No. 2 gauge stres · no. 24 peta skor statis vs adaptif · no. 36 kartu fundamental kuat · no. 67 broker akumulator."),
]
for img, judul, klik, ucap, angka in PANEL:
    w(f'<h2>{judul}</h2>')
    shot(img, judul.split(" ", 1)[1])
    table(["", ""], [["<b>Klik</b>", klik], ["<b>Ucapkan</b>", f"<i>\"{ucap}\"</i>"], ["<b>Angka kunci</b>", angka]], ["16%", "84%"])

w('<h2>3.11 Rekomendasi 10 pertanyaan untuk didemokan</h2>')
table(["No.", "Pertanyaan", "Visual", "Kenapa menarik"], [
    ["2", "Berapa skor stres pasar dari 12?", "gauge", "pembuka cepat, langsung terlihat"],
    ["4", "Bobot sembilan pilar di regime aktif", "radar", "menjelaskan meta-penalaran pakar"],
    ["13", "Skor sektor di tiga skenario", "batang berkelompok", "robustness lintas skenario"],
    ["24", "Hubungan skor statis dan adaptif", "peta sebaran", "inti perbedaan analis vs pakar"],
    ["36", "Emiten dengan fundamental kuat", "kartu emiten berlogo", "visual paling menarik"],
    ["39", "Bagaimana hubungan ROE dan DER?", "peta sebaran", "fundamental klasik"],
    ["61", "Emiten yang diakumulasi bandar", "kartu emiten", "bandarmology"],
    ["77", "Pergerakan makro yang menguntungkan sektor", "batang horizontal", "geopolitik → sektor"],
    ["84", "Emiten rawan collapse (going concern)", "kartu emiten", "manajemen risiko"],
    ["99", "Aturan SWRL per pilar", "batang horizontal", "menunjukkan isi 303 aturan"],
], ["8%", "42%", "20%", "30%"])

# ---------------------------------------------------- 4. persiapan & cadangan
w('<div class="pb"></div><h1>4. Persiapan dan rencana cadangan</h1>')
w('<h2>4.1 Checklist 15 menit sebelum presentasi</h2>')
w('<ul class="chk">' + "".join(f"<li>{x}</li>" for x in [
    "Laptop dicas penuh, mode jangan ganggu aktif, notifikasi dimatikan.",
    "Terminal: <code>cd ~/Downloads/KBR_Kelompok9_SahamExpertKB_v2</code> lalu <code>./dashboard/start_demo.sh ~/Downloads/apache-jena-fuseki-6.3.0</code>; tunggu tulisan <i>Fuseki siap</i>.",
    "Safari: buka <code>localhost:8080</code>, pastikan lampu hijau <i>Terhubung</i> dan logo Stock tampil. Tekan Cmd + Option + R bila tampilan lama.",
    "Coba sekali what-if Kapitulasi lalu Reset, supaya mesin aturan Jena sudah “panas”.",
    "Perbesar tampilan ke 90% (Cmd + −) bila layar proyektor kecil.",
    "Protégé terbuka di jendela lain: <code>output/SahamExpertKB_v2.owl</code>, reasoner Pellet sudah dijalankan, individu ANTM dipilih.",
    "PDF cadangan siap: buku panduan, laporan hasil prediksi, dan dokumen ini.",
]) + "</ul>")
w('<h2>4.2 Kalau ada masalah saat demo</h2>')
table(["Masalah", "Penyebab", "Yang dilakukan"], [
    ["Lampu merah / \"Fuseki tidak terhubung\"", "Terminal start_demo tertutup", "<code>lsof -ti :3030 -ti :8080 | xargs kill</code>, lalu jalankan ulang <code>start_demo.sh</code>; sambil menunggu, jelaskan arsitektur"],
    ["Tampilan lama (header hitam)", "cache Safari", "Cmd + Option + E lalu Cmd + R, atau buka jendela privat Cmd + Shift + N"],
    ["What-if lama sekali", "penalaran ulang 305 aturan", "tunggu 2–5 detik; jelaskan bahwa server sedang menalar ulang"],
    ["Hasil aneh setelah beberapa what-if", "data /saham masih berubah", "klik <b>Reset ke data asli</b>"],
    ["Logo emiten berupa inisial", "tidak ada internet", "tidak masalah; logo resmi bisa disimpan di <code>dashboard/logo/KODE.png</code>"],
    ["Laptop / proyektor bermasalah total", "-", "presentasikan dari PDF ini (semua screenshot ada di Bab 3)"],
], ["28%", "24%", "48%"])
w('<h2>4.3 Kalimat kunci yang sebaiknya diingat</h2>')
w("<ul>" + "".join(f"<li>{x}</li>" for x in [
    "<b>Ontologi</b> menyimpan pengetahuan; <b>SWRL</b> menyimpan cara pakar menalar; <b>Pellet</b> menarik kesimpulan; <b>Fuseki</b> menyajikannya; <b>dashboard</b> menampilkannya.",
    "Porsi knowledge base 98%; ML hanya skor sentimen berita dan tetap ditafsirkan aturan.",
    "Ekspresivitas SROIQ(D) dicek dengan pemeriksa OWLAPI yang sama dengan Protégé.",
    "Dua mesin berbeda (Pellet dan aturan Jena) memberi hasil identik: regime, skor stres, tujuh top pick.",
    "103 dari 103 soal uji lulus, termasuk 12 competency questions dan 5 what-if.",
    "Sistem ini alat bantu analisis, bukan nasihat investasi personal.",
]) + "</ul>")

# ---------------------------------------------------- 5. glosarium
w('<div class="pb"></div><h1>5. Daftar istilah dan artinya</h1>')
GL = [
("Ontologi &amp; web semantik", [
 ("Ontologi", "deskripsi formal tentang konsep dalam suatu bidang beserta hubungannya, yang bisa dinalar komputer"),
 ("Kelas (class)", "kategori benda, mis. Emiten, Sektor"),
 ("Subkelas", "kelas yang lebih khusus; anggotanya otomatis anggota kelas induk (EmitenPerbankan ⊑ Emiten)"),
 ("Individu (instance)", "anggota nyata suatu kelas, mis. ANTM, BBCA"),
 ("Object property", "hubungan antar-individu, mis. ANTM <i>termasukSektor</i> Barang Baku"),
 ("Data property", "nilai angka/teks milik individu, mis. ROE ANTM = 18"),
 ("Annotation property", "keterangan untuk manusia (label, rumus) yang tidak dinalar"),
 ("Aksioma", "satu pernyataan logis di ontologi"),
 ("TBox", "bagian skema: kelas, hierarki, properti, batasan"),
 ("ABox", "bagian fakta tentang individu"),
 ("RBox", "aksioma tentang properti (mis. transitif, invers)"),
 ("RDF", "model data berbentuk triple subjek–predikat–objek"),
 ("Triple", "satu fakta: subjek – predikat – objek"),
 ("IRI", "alamat unik global untuk setiap nama (mirip URL)"),
 ("Prefix / namespace", "singkatan IRI, mis. <code>ex:</code> untuk ontologi proyek"),
 ("Turtle (.ttl)", "format penulisan RDF yang ringkas; RDF/XML (.owl) adalah format lain untuk isi yang sama"),
 ("RDFS", "bahasa dasar untuk kelas, subkelas, domain, range"),
 ("OWL 2", "Web Ontology Language, bahasa ontologi standar W3C yang lebih kaya dari RDFS"),
 ("Domain / range", "kelas subjek / kelas atau tipe objek dari sebuah properti"),
 ("disjointWith", "dua kelas tidak boleh punya anggota yang sama"),
 ("Open World Assumption", "yang tidak tercatat dianggap tidak diketahui, bukan salah"),
 ("No unique name assumption", "OWL tidak otomatis menganggap dua nama berbeda sebagai dua benda berbeda"),
 ("SROIQ(D)", "tingkat ekspresivitas logika deskripsi yang setara OWL 2 DL: S transitif, R karakteristik peran, O nominal, I invers, Q kardinalitas berkualifikasi, (D) tipe data"),
 ("Ontologi eksternal", "ontologi buatan pihak lain yang dipakai ulang"),
 ("owl:imports", "memasukkan seluruh isi ontologi lain"),
 ("Modul alignment", "ontologi kecil yang memetakan konsep proyek ke ontologi eksternal"),
 ("FIBO", "Financial Industry Business Ontology, ontologi standar industri keuangan (EDM Council)"),
 ("schema.org", "kosakata umum web (Corporation, NewsArticle)"),
 ("SKOS", "kosakata W3C untuk memetakan konsep (closeMatch, exactMatch)"),
 ("Dublin Core", "kosakata metadata: judul, pembuat, tanggal, lisensi"),
 ("catalog-v001.xml", "file pemetaan IRI ke file lokal agar Protégé bisa mengimpor tanpa internet"),
]),
("Penalaran, aturan &amp; query", [
 ("Sistem pakar / KBS", "sistem yang menyimpan pengetahuan pakar secara eksplisit dan menalar darinya"),
 ("Knowledge base", "ontologi + fakta + aturan"),
 ("Reasoner", "program yang menarik kesimpulan dari ontologi dan aturan"),
 ("Pellet", "reasoner OWL-DL yang mendukung SWRL beserta built-in; reasoner utama proyek"),
 ("HermiT", "reasoner bawaan Protégé; tidak mendukung built-in SWRL"),
 ("Konsisten", "tidak ada kontradiksi logika"),
 ("Klasifikasi", "menyusun hierarki kelas yang tersirat"),
 ("Realisasi", "menentukan setiap individu masuk kelas mana saja"),
 ("Asserted", "fakta yang dimasukkan (latar putih di Protégé)"),
 ("Inferred", "fakta hasil penalaran (latar kuning di Protégé)"),
 ("Explanation", "tombol ? di Protégé yang menunjukkan alasan suatu kesimpulan"),
 ("SWRL", "Semantic Web Rule Language, aturan JIKA (body) – MAKA (head)"),
 ("Built-in (swrlb:)", "fungsi SWRL: greaterThan, lessThan, add, multiply, subtract"),
 ("Interval berpasangan", "pola aturan berbatas [bawah, atas) yang menutup semua nilai, pengganti ELSE"),
 ("Monoton", "aturan hanya menambah fakta, tidak pernah menghapus"),
 ("Aturan berantai", "kesimpulan satu aturan menjadi masukan aturan lain"),
 ("SQWRL", "perluasan SWRL untuk query (select, orderBy, limit)"),
 ("DL Query", "tab Protégé untuk bertanya dengan ekspresi kelas (Manchester syntax)"),
 ("SPARQL", "bahasa query untuk graf RDF (mirip SQL untuk tabel)"),
 ("SPARQL Update", "perintah INSERT/DELETE untuk mengubah data"),
 ("Competency question (CQ)", "pertanyaan yang wajib bisa dijawab knowledge base"),
 ("Ontology Development 101", "metodologi Noy &amp; McGuinness untuk membangun ontologi"),
 ("Case-based reasoning (CBR)", "membandingkan kondisi sekarang dengan kasus historis yang mirip"),
]),
("Tools &amp; teknologi", [
 ("Protégé", "editor dan alat pemeriksa ontologi dari Stanford"),
 ("SWRLTab / SQWRLTab", "plugin Protégé untuk menyunting aturan dan menjalankan SQWRL (engine Drools)"),
 ("owlready2", "pustaka Python untuk membangun ontologi dan menjalankan Pellet"),
 ("OWLAPI", "pustaka Java untuk ontologi OWL; dipakai untuk ekspor inferensi dan cek ekspresivitas"),
 ("Apache Jena", "kerangka kerja Java untuk web semantik"),
 ("Apache Jena Fuseki", "server SPARQL yang melayani graf RDF lewat HTTP (port 3030)"),
 ("Dataset (Fuseki)", "kumpulan graf yang dilayani dengan satu nama: /saham dan /saham-pellet"),
 ("Endpoint", "alamat HTTP untuk operasi tertentu, mis. /saham-pellet/query, /saham/update"),
 ("GenericRuleReasoner", "mesin aturan Jena yang menjalankan 305 aturan di dataset /saham"),
 ("InfModel", "graf Jena yang dilengkapi reasoner"),
 ("swrl2jena.py", "skrip proyek yang menerjemahkan SWRL ke aturan Jena"),
 ("run_all.py", "skrip yang menjalankan 12 tahap pipeline dengan satu perintah"),
 ("server.py", "server dashboard (port 8080) yang juga meneruskan permintaan ke Fuseki"),
 ("Proxy / CORS", "penerus permintaan; dipakai agar browser tidak diblokir aturan lintas alamat (CORS)"),
 ("Chart.js", "pustaka grafik JavaScript yang dipakai dashboard (disimpan lokal)"),
 ("JSON", "format data yang dikembalikan Fuseki ke dashboard"),
 ("Playwright", "alat otomasi browser untuk membuat PDF laporan"),
]),
("Pasar saham &amp; analisis", [
 ("BEI / IDX", "Bursa Efek Indonesia"), ("IHSG", "Indeks Harga Saham Gabungan"),
 ("Emiten", "perusahaan yang sahamnya tercatat di bursa"),
 ("Sektor IDX-IC", "klasifikasi 11 sektor industri BEI"),
 ("LQ45", "indeks 45 saham paling likuid dan berkapitalisasi besar"),
 ("ROE", "laba bersih ÷ ekuitas; mengukur profitabilitas"),
 ("DER", "utang ÷ ekuitas; mengukur beban utang"),
 ("PER", "harga ÷ laba per saham; mengukur mahal-murah"),
 ("PBV", "harga ÷ nilai buku per saham"),
 ("EPS", "laba per saham"), ("Dividend yield", "dividen ÷ harga saham"),
 ("Altman Z", "skor risiko kebangkrutan (aman, abu-abu, distress)"),
 ("Beneish M", "skor indikasi manipulasi laba"),
 ("NIM / NPL / CAR", "rasio bank: margin bunga bersih / kredit macet / kecukupan modal"),
 ("Nilai wajar", "perkiraan harga pantas dari metode valuasi"),
 ("Equity risk premium (ERP)", "selisih imbal hasil saham terhadap obligasi negara"),
 ("RSI", "indikator momentum 0–100; &lt; 30 jenuh jual, &gt; 70 jenuh beli"),
 ("MA200", "rata-rata harga 200 hari; acuan tren jangka panjang"),
 ("ATR", "rata-rata rentang harga harian; ukuran volatilitas"),
 ("Wyckoff", "teori fase pasar: akumulasi, mark-up, distribusi, mark-down"),
 ("Bandarmology", "analisis jejak transaksi pemain besar lewat data broker"),
 ("Akumulasi / distribusi", "pemain besar sedang membeli / menjual bertahap"),
 ("Net asing", "selisih beli dan jual investor asing"),
 ("Free float", "porsi saham yang beredar bebas di publik"),
 ("CDS 5Y", "credit default swap 5 tahun; ukuran premi risiko negara"),
 ("Yield SBN", "imbal hasil Surat Berharga Negara"),
 ("Breadth", "persentase saham di atas MA200; ukuran kesehatan pasar"),
 ("Drawdown", "penurunan dari titik tertinggi"),
 ("Kapitulasi", "fase jual panik besar-besaran yang sering menandai dasar pasar"),
 ("Katalis", "peristiwa terjadwal yang bisa menggerakkan harga (FOMC, MSCI review)"),
 ("MSCI / FTSE", "penyedia indeks global yang diikuti dana pasif"),
 ("Stop loss / take profit", "batas jual rugi / batas ambil untung"),
]),
("Istilah sistem SahamExpertKB", [
 ("Regime pasar", "kondisi pasar (Krisis Likuiditas, Risk-Off, Netral, Risk-On) yang menentukan bobot penilaian"),
 ("Skor stres pasar", "jumlah poin 0–2 dari enam indikator (0–12)"),
 ("Pilar", "aspek penilaian: fundamental, valuasi, teknikal, bandarmology, sentimen, sektor, risiko, likuiditas, smart money"),
 ("Skor statis", "jumlah delapan pilar dengan bobot sama (cara analis biasa)"),
 ("Skor adaptif", "jumlah sembilan pilar × bobot regime aktif (cara pakar)"),
 ("Ambang top pick", "skor adaptif minimum untuk menjadi top pick (24,7 saat krisis)"),
 ("Top pick adaptif", "emiten yang lolos ambang regime, sektornya berekspektasi positif, dan penaltinya kecil"),
 ("Watchlist", "emiten berskor 16–20 di sektor bullish; dipantau"),
 ("Skenario base/bull/bear", "tiga kemungkinan masa depan 2027–2028 dengan probabilitas 50/25/25%"),
 ("Skor outlook sektor", "makro-geo + valuasi + tema×2 + sentimen + aliran asing + rotasi"),
 ("Ekspektasi probabilistik", "rata-rata tertimbang skor sektor di tiga skenario"),
 ("Sektor inti", "bullish di skenario aktif dan robust di semua skenario"),
 ("Sektor satelit", "potensi naik ≥ 1,5× risikonya, plus ada peluang kontrarian"),
 ("Kontrarian", "peluang membeli saat harga tertekan oleh sentimen sementara"),
 ("Tesis investasi", "alasan memilih sektor, dengan satu indikator kunci"),
 ("Kill switch", "batas yang membuat tesis dinyatakan gugur"),
 ("Valid / rapuh / gugur / terpicu", "status tesis: aman / jarak ke batas &lt; 10% / melewati batas / pemicu kontrarian tercapai"),
 ("Akumulasi bertahap", "strategi membeli dalam beberapa tranche saat kapitulasi"),
 ("Tranche", "bagian pembelian bertahap (mis. 30/30/40%)"),
 ("Ukuran posisi maksimum", "batas porsi modal per saham dari risiko per transaksi ÷ (2 × ATR%)"),
 ("Persona investor", "profil pengguna: mahasiswa konservatif, pekerja muda moderat, Gen Z agresif, trader scalper"),
 ("What-if", "simulasi mengubah data lalu melihat kesimpulan baru setelah aturan menalar ulang"),
 ("Pellet vs Jena live", "dua sumber dashboard: hasil Pellet yang sudah jadi vs penalaran langsung aturan Jena"),
]),
]
for kat, items in GL:
    w(f"<h2>{kat}</h2>")
    w('<table class="gl"><tr><th>Istilah</th><th>Arti</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in items) + "</table>")

# =============================================================== RENDER
html = f"<!DOCTYPE html><html lang='id'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(H)}</body></html>"
tmp = tempfile.mkdtemp(); hp = os.path.join(tmp, "p.html"); open(hp, "w", encoding="utf-8").write(html)
footer = '<div style="font-size:7.5pt;width:100%;text-align:center;color:#999">Panduan Presentasi SahamExpertKB · Kelompok 9 · <span class="pageNumber"></span>/<span class="totalPages"></span></div>'
js = os.path.join(tmp, "p.js")
open(js, "w").write(f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}',{{waitUntil:'load'}});await p.pdf({{path:{json.dumps(DST)},format:'A4',printBackground:true,displayHeaderFooter:true,
headerTemplate:'<span></span>',footerTemplate:{json.dumps(footer)},margin:{{top:'15mm',bottom:'17mm',left:'14mm',right:'14mm'}}}});await b.close();}})();""")
subprocess.run(["node", js], check=True)
n = sum(len(x) for _, x in GL)
print("PDF:", DST, "istilah:", n)
