# -*- coding: utf-8 -*-
"""BUKU PANDUAN LENGKAP SahamExpertKB — dari nol (ontologi, RDF, OWL, reasoner, SWRL, SPARQL,
ontologi eksternal) sampai arsitektur proyek, Fuseki, dan dashboard live. Keluaran: PDF bergambar.

Pakai:  python3 tools/make_buku_panduan.py
Butuh:  Node.js + Playwright (sama seperti PDF lain di proyek ini; lihat README).
"""
import base64, json, os, re, subprocess, sys, tempfile
from html import escape as E

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tools", "buku"))
import diagram as D  # noqa: E402

OUT = os.path.join(HERE, "output")
IMG = os.path.join(HERE, "docs", "img")
DST = os.path.join(OUT, "BUKU_PANDUAN_LENGKAP_SahamExpertKB.pdf")

# ------------------------------------------------------------------ angka dari hasil build terakhir
VAL = {}
for ln in open(os.path.join(OUT, "validasi_owlapi_pellet.txt"), encoding="utf-8"):
    for kv in ln.split():
        if "=" in kv:
            k, v = kv.split("=", 1); VAL[k] = v
R = json.load(open(os.path.join(OUT, "hasil_inferensi.json"), encoding="utf-8"))
TGL = open(os.path.join(HERE, "data", "tanggal_acuan.txt"), encoding="utf-8").read().strip()
NK, NI, NOP, NDP, NAT, NR = VAL.get("CLASSES"), VAL.get("INDIVIDUALS"), VAL.get("OBJECT_PROPERTIES"), VAL.get("DATA_PROPERTIES"), VAL.get("TOTAL_AXIOMS"), VAL.get("SWRL_RULES")
fmtn = lambda x: f"{int(x):,}".replace(",", ".")
PICK = sorted(e["kode"] for e in R["emiten"] if "KandidatTopPickAdaptif" in e["kelas"])

# ------------------------------------------------------------------ helper HTML
H = []
TOC = []
def w(s): H.append(s)
def bab(no, judul, sub=""):
    TOC.append((1, no, judul)); w(f'<section class="bab"><div class="babno">BAGIAN {no}</div><h1 id="b{no}">{E(judul)}</h1>' + (f'<p class="babsub">{sub}</p>' if sub else "") + "</section>")
def h2(no, judul):
    TOC.append((2, no, judul)); w(f'<h2 id="s{no.replace(".", "_")}">{no} {E(judul)}</h2>')
def h3(judul): w(f"<h3>{E(judul)}</h3>")
def p(s): w(f"<p>{s}</p>")
def ul(items): w("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
def ol(items): w("<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>")
def code(s, judul=None): w((f'<div class="codettl">{E(judul)}</div>' if judul else "") + f"<pre>{E(s.strip())}</pre>")
def note(s, jenis="info"):
    lbl = {"info": "Intinya", "tip": "Tips", "warn": "Perhatian", "dosen": "Kalau dosen bertanya"}[jenis]
    w(f'<div class="note {jenis}"><b>{lbl}.</b> {s}</div>')
def table(head, rows, widths=None):
    cg = "".join(f'<col style="width:{x}">' for x in widths) if widths else ""
    w(f"<table><colgroup>{cg}</colgroup><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
      "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table>")
FIGN = [0]
def fig(svg_html, cap):
    FIGN[0] += 1; w(f'<figure>{svg_html}<figcaption>Gambar {FIGN[0]}. {cap}</figcaption></figure>')
def img(name, cap, width="100%"):
    path = os.path.join(IMG, name)
    if not os.path.exists(path):
        return
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    FIGN[0] += 1
    w(f'<figure><img src="data:image/png;base64,{b64}" style="width:{width}"><figcaption>Gambar {FIGN[0]}. {cap}</figcaption></figure>')
def pb(): w('<div class="pb"></div>')
def kode(s): return f"<code>{E(s)}</code>"

CSS = """
@page{size:A4;margin:16mm 15mm 18mm 15mm}
*{box-sizing:border-box}
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:10pt;color:#1d2433;line-height:1.55}
h1{font-size:21pt;color:#0b3d6e;margin:0 0 6px;line-height:1.2}
h2{font-size:13.5pt;color:#0b3d6e;margin:20px 0 6px;border-bottom:1.5px solid #d5deeb;padding-bottom:3px;break-after:avoid}
h3{font-size:11pt;color:#1d2433;margin:14px 0 4px;break-after:avoid}
p{margin:5px 0 7px;text-align:justify}
ul,ol{margin:4px 0 8px 0;padding-left:20px}li{margin:2px 0}
code{font-family:'DejaVu Sans Mono',Menlo,monospace;font-size:8.6pt;background:#f1f3f6;padding:0 3px;border-radius:3px}
pre{font-family:'DejaVu Sans Mono',Menlo,monospace;font-size:8.2pt;background:#0f172a;color:#dbe5ff;padding:9px 11px;border-radius:7px;white-space:pre-wrap;line-height:1.45;margin:4px 0 10px;break-inside:avoid}
.codettl{font-size:8.5pt;color:#5d6672;margin-top:8px;font-weight:700}
table{border-collapse:collapse;width:100%;margin:6px 0 12px;font-size:8.9pt;break-inside:auto}
th{background:#eef3fb;text-align:left;padding:5px 6px;border:1px solid #d5deeb;color:#0b3d6e}
td{padding:4px 6px;border:1px solid #e1e5ea;vertical-align:top}
tr{break-inside:avoid}
figure{margin:10px 0 14px;break-inside:avoid;text-align:center}
figure img{border:1px solid #d5deeb;border-radius:6px}
figcaption{font-size:8.6pt;color:#5d6672;margin-top:4px;text-align:center}
.note{border-left:4px solid #2f5bd3;background:#f2f6fd;padding:7px 10px;margin:8px 0 10px;border-radius:0 6px 6px 0;font-size:9.4pt;break-inside:avoid}
.note.tip{border-color:#1f8a5b;background:#eef8f3}.note.warn{border-color:#b26a00;background:#fdf6ea}.note.dosen{border-color:#7a3ea8;background:#f6f0fb}
.bab{break-before:page;padding-top:30mm;margin-bottom:10px}
.babno{font-size:10pt;letter-spacing:.2em;color:#2f5bd3;font-weight:700}
.babsub{color:#5d6672;font-size:11pt;text-align:left;max-width:150mm}
.pb{break-after:page}
.cover{height:255mm;display:flex;flex-direction:column;justify-content:space-between;padding:20mm 4mm 0}
.cover h1{font-size:30pt}
.cover .tag{font-size:13pt;color:#3a4556;max-width:150mm;line-height:1.5}
.cover .meta{font-size:10pt;color:#5d6672;border-top:2px solid #0b3d6e;padding-top:8px}
.toc div{display:flex;justify-content:space-between;border-bottom:1px dotted #c9d2de;padding:2px 0;font-size:9.6pt}
.toc .l1{font-weight:700;margin-top:8px;color:#0b3d6e}
.toc .l2{padding-left:14px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.step{border:1px solid #d5deeb;border-radius:7px;padding:7px 10px;margin:6px 0;break-inside:avoid}
.qa{margin:0 0 8px;break-inside:avoid}.q{font-weight:700;color:#0b3d6e}.qn{display:inline-block;min-width:32px;color:#2f5bd3}
.a{padding-left:32px;text-align:justify}
.step b.n{display:inline-block;background:#2f5bd3;color:#fff;border-radius:50%;width:19px;height:19px;text-align:center;font-size:9pt;line-height:19px;margin-right:6px}
"""

# =================================================================== SAMPUL
w(f"""<div class="cover"><div>
<div class="babno">BUKU PANDUAN LENGKAP &amp; MODUL PRESENTASI</div>
<h1>SahamExpertKB<br>dari Nol sampai Dashboard Live</h1>
<p class="tag">Memahami ontologi, RDF, OWL, reasoner, SWRL, SPARQL, dan ontologi eksternal, lalu merancang arsitektur
sistem pakar saham Indonesia, menjalankannya di Protégé dan Apache Jena Fuseki, hingga menampilkannya sebagai dashboard web yang
menalar secara langsung.</p></div>
<div>{D.d_arsitektur()}</div>
<div class="meta">Kelompok 9 · Knowledge Based Reasoning · Jonnathan (Peran A) &amp; Gloria (Peran B)<br>
Data acuan {TGL} · Ontologi {NK} kelas · {fmtn(NI)} individu · {NR} aturan SWRL · {fmtn(NAT)} aksioma</div></div>""")
w('<div class="pb"></div><h1 style="font-size:17pt">Daftar isi</h1><div class="toc">@@TOC@@</div>')

# =================================================================== CARA MEMBACA
w('<div class="pb"></div><h1 style="font-size:17pt">Cara memakai buku ini</h1>')
p("Buku ini ditulis untuk pembaca yang <b>belum pernah belajar ontologi</b>. Setiap istilah dijelaskan dari awal, lalu langsung "
  "ditunjukkan contohnya di proyek SahamExpertKB. Urutannya mengikuti cara seorang knowledge engineer bekerja: pahami konsep, "
  "rancang arsitektur, bangun, sajikan, lalu uji.")
table(["Bagian", "Isi", "Baca bila…"], [
    ["I. Konsep dasar", "Sistem pakar, ontologi, RDF/triple, OWL, reasoner, SWRL, SPARQL, ontologi eksternal", "kamu belum paham istilah-istilahnya (mulai di sini)"],
    ["II. Arsitektur", "Gambaran besar SahamExpertKB, struktur ontologi, alur penalaran, peta file, roadmap", "kamu perlu menjelaskan rancangan ke dosen"],
    ["III. Membangun dari awal", "Sembilan langkah merancang KB, termasuk latihan membuat ontologi mini di Protégé", "kamu ingin bisa membuat ulang atau menambah fitur"],
    ["IV. Apache Jena Fuseki", "Apa, kenapa, instalasi di Mac, konfigurasi, query, update", "kamu bingung soal Fuseki (praktikum asdos)"],
    ["V. Dashboard live", "Arsitektur, cara menjalankan, penjelasan setiap visualisasi, skenario demo", "kamu akan presentasi"],
    ["VI. Uji &amp; lampiran", "Pengujian 103 soal, troubleshooting, glosarium, referensi", "ada error atau lupa istilah"],
    ["VII. 100 pertanyaan dosen", "Tanya-jawab per topik: konsep, ontologi, eksternal, SWRL, logika pakar, data, pipeline, Fuseki, dashboard, uji", "persiapan sesi tanya jawab"],
], ["22%", "48%", "30%"])
note("Untuk demo cepat cukup tiga perintah: <code>python3 run_all.py</code> (membangun KB), "
     "<code>./dashboard/start_demo.sh ~/Downloads/apache-jena-fuseki-6.3.0</code> (menyalakan Fuseki + dashboard), lalu buka "
     "<code>http://localhost:8080</code>.", "tip")

# =================================================================== RINGKASAN PRESENTASI
w('<div class="pb"></div><h1 style="font-size:17pt">Ringkasan satu halaman untuk presentasi</h1>')
note("<b>Pembuka 30 detik.</b> \"SahamExpertKB adalah sistem pakar berbasis ontologi OWL dan " + str(NR) + " aturan SWRL yang memprediksi sektor saham "
     "BEI yang berpeluang naik 1–3 tahun dan memilih emiten terbaiknya. Bedanya dengan analis biasa: sistem ini mendeteksi kondisi pasar "
     "lalu menyesuaikan cara menilainya, menguji prediksinya di tiga skenario, dan tahu kapan tesisnya gugur. Semua kesimpulan bisa "
     "dijelaskan, dan sistemnya bisa ditanyai aplikasi lain lewat Apache Jena Fuseki.\"", "tip")
table(["Angka kunci", "Nilai"], [
 ["Ukuran KB", f"{NK} kelas · {NOP} object property · {NDP} data property · {fmtn(NI)} individu · {fmtn(NAT)} aksioma"],
 ["Aturan", f"{NR} SWRL (dinalar Pellet) = 305 aturan Jena di Fuseki"],
 ["Porsi KB", "98% aksioma adalah pengetahuan; komponen statistik (sentimen) &lt; 20%"],
 ["Data", f"64 emiten · 11 sektor · 71 berita · data acuan {TGL}"],
 ["Regime saat ini", "Krisis Likuiditas (skor stres 11/12)"],
 ["Sektor inti / satelit", "Barang Baku, Kesehatan / Infrastruktur, Keuangan"],
 ["Top pick sistem pakar", ", ".join(PICK) + " (analis biasa hanya 4: ANTM, MIKA, NCKL, TINS)"],
 ["Pengujian", "103/103 soal lulus · konsisten (OWLAPI + Pellet) · Pellet = Jena"],
], ["28%", "72%"])
table(["Urutan bicara", "Isi", "Bab"], [
 ["1. Masalah", "investor ritel kesulitan menggabungkan banyak analisis, terlebih saat krisis", "1.1"],
 ["2. Konsep", "ontologi, SWRL, reasoner, ontologi eksternal (FIBO)", "1.2–1.8"],
 ["3. Arsitektur", "CSV → owlready2 → Pellet → Protégé / Fuseki / dashboard", "2.1–2.2"],
 ["4. Penalaran", "regime → bobot adaptif → skenario → inti/satelit → top pick → kill switch", "2.4, 5.3"],
 ["5. Demo", "dashboard: regime, sektor, analis vs pakar, bedah ANTM, tesis, what-if kapitulasi", "5.6"],
 ["6. Bukti", "103 soal, dua mesin identik, alignment FIBO konsisten", "6.1"],
 ["7. Penutup", "keterbatasan dan roadmap", "2.6"],
], ["20%", "64%", "16%"])

# =================================================================== BAGIAN I
bab("I", "Konsep dasar", "Semua istilah yang perlu kamu kuasai sebelum menyentuh Protégé atau Fuseki, dijelaskan dari nol dengan contoh dari proyek.")

h2("1.1", "Data, pengetahuan, dan sistem berbasis pengetahuan")
p("<b>Data</b> adalah angka mentah: <i>ROE ANTM = 18%</i>. <b>Informasi</b> adalah data yang diberi konteks: <i>ROE ANTM 18%, "
  "di atas rata-rata industri</i>. <b>Pengetahuan</b> adalah aturan yang dipakai pakar untuk mengambil keputusan dari informasi: "
  "<i>JIKA ROE ≥ 15% DAN utang rendah DAN laba tumbuh, MAKA fundamental perusahaan kuat</i>.")
p("<b>Sistem berbasis pengetahuan</b> (knowledge-based system, KBS), yang juga disebut <b>sistem pakar</b>, menyimpan pengetahuan "
  "semacam itu secara eksplisit lalu memakainya untuk menalar. Ciri utamanya: pengetahuan dipisahkan dari mesin yang menalar.")
fig(D.d_sistem_pakar(), "Komponen sistem berbasis pengetahuan dan padanannya di SahamExpertKB.")
table(["", "Program biasa", "Machine learning", "Sistem berbasis pengetahuan"], [
    ["Logika disimpan di", "kode program (if-else)", "bobot model hasil latihan", "knowledge base (ontologi + aturan)"],
    ["Bisa menjelaskan alasan?", "sulit", "sulit (kotak hitam)", "ya: rantai aturan bisa ditelusuri"],
    ["Butuh data latih?", "tidak", "banyak", "tidak; butuh pengetahuan pakar"],
    ["Mengubah perilaku", "ubah kode", "latih ulang", "ubah fakta atau aturan"],
], ["22%", "24%", "24%", "30%"])
note("Dosen meminta porsi knowledge base minimal 80%. Di proyek ini {0} dari {1} aksioma adalah pengetahuan, hanya {2} berupa aturan, "
     "sehingga porsi KB = {3}%. ML hanya dipakai sebagai pendukung (&lt; 20%) untuk skor sentimen judul berita.".format(
         fmtn(int(NAT) - int(NR)), fmtn(NAT), NR, f"{100 * (int(NAT) - int(NR)) / int(NAT):.1f}".replace(".", ",")), "dosen")

h2("1.2", "Apa itu ontologi")
p("Dalam ilmu komputer, <b>ontologi</b> adalah deskripsi formal tentang konsep-konsep dalam suatu bidang dan hubungan di antaranya, "
  "ditulis sedemikian rupa sehingga komputer bisa menalarnya. Bayangkan gabungan tiga hal: <b>kamus</b> (istilah apa saja yang ada), "
  "<b>peta hubungan</b> (bagaimana istilah saling terkait), dan <b>aturan</b> (apa yang pasti benar).")
p("Ontologi punya lima komponen. Hafalkan kelimanya karena istilah ini muncul terus di Protégé:")
table(["Komponen", "Artinya", "Contoh di SahamExpertKB", "Di Protégé"], [
    ["<b>Kelas</b> (class)", "kategori atau jenis benda", "Emiten, Sektor, Berita, RegimePasar", "tab Entities › Classes (ikon lingkaran kuning)"],
    ["<b>Subkelas</b>", "kelas yang lebih khusus; anggotanya otomatis anggota induknya", "EmitenPerbankan ⊑ Emiten", "hierarki pohon di Classes"],
    ["<b>Individu</b> (instance)", "benda nyata anggota suatu kelas", "ANTM, BBCA, Sektor_BarangBaku", "Individuals (ikon belah ketupat ungu)"],
    ["<b>Object property</b>", "hubungan antar-individu", "ANTM termasukSektor Sektor_BarangBaku", "Object properties"],
    ["<b>Data property</b>", "nilai/angka milik individu", "ANTM roe 18; ANTM der 0,3", "Data properties"],
    ["<b>Annotation property</b>", "keterangan untuk manusia, tidak dinalar", "rdfs:label, rumus, ambangBatas", "panel Annotations"],
], ["18%", "27%", "29%", "26%"])
fig(D.d_ontologi_mini(), "Contoh ontologi mini yang diambil dari SahamExpertKB.")
h3("TBox dan ABox")
p("Ontologi biasanya dibagi dua. <b>TBox</b> (terminological box) adalah kosakata atau skemanya: kelas, hierarki, properti, beserta "
  "batasannya. <b>ABox</b> (assertional box) adalah fakta tentang individu: ANTM adalah Emiten, ROE ANTM 18. Analogi basis data: "
  "TBox mirip struktur tabel, ABox mirip baris-baris datanya. Bedanya, ontologi bisa <i>menyimpulkan</i> fakta baru dari keduanya.")
img("protege_kelas.png", "Hierarki kelas SahamExpertKB di Protégé (tab Entities › Classes). Kelas teratas di bawah owl:Thing adalah cabang-cabang pengetahuan proyek.", "92%")

h2("1.3", "RDF: semua fakta adalah triple")
p("Ontologi OWL disimpan dalam format <b>RDF</b> (Resource Description Framework). Di RDF, setiap fakta ditulis sebagai satu "
  "<b>triple</b>: <b>subjek – predikat – objek</b>, mirip kalimat sederhana <i>ANTM – termasuk sektor – Barang Baku</i>.")
fig(D.d_triple(), "Empat triple tentang ANTM. Triple terakhir tidak ada di data, tetapi ditambahkan reasoner.")
h3("IRI, namespace, dan prefix")
p("Agar tidak tertukar dengan ANTM milik ontologi lain, setiap nama punya alamat unik global yang disebut <b>IRI</b> "
  "(mirip URL). Nama lengkap ANTM di proyek ini adalah:")
code("http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#ANTM")
p("Menulis IRI panjang berulang-ulang melelahkan, jadi dipakai <b>prefix</b> (singkatan). Prefix <code>ex:</code> berarti "
  "<code>http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#</code>, sehingga cukup ditulis <code>ex:ANTM</code>. Prefix lain yang "
  "akan sering kamu lihat:")
table(["Prefix", "Kepanjangan", "Isinya"], [
    ["<code>rdf:</code>", "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "dasar RDF, mis. <code>rdf:type</code> (adalah anggota kelas)"],
    ["<code>rdfs:</code>", "http://www.w3.org/2000/01/rdf-schema#", "<code>rdfs:subClassOf</code>, <code>rdfs:label</code>, <code>rdfs:comment</code>"],
    ["<code>owl:</code>", "http://www.w3.org/2002/07/owl#", "<code>owl:Class</code>, <code>owl:Thing</code>, <code>owl:imports</code>"],
    ["<code>xsd:</code>", "http://www.w3.org/2001/XMLSchema#", "tipe data: <code>xsd:integer</code>, <code>xsd:double</code>, <code>xsd:string</code>"],
    ["<code>swrlb:</code>", "http://www.w3.org/2003/11/swrlb#", "built-in aturan: <code>greaterThan</code>, <code>add</code>, <code>multiply</code>"],
], ["12%", "48%", "40%"])
h3("Satu fakta, dua cara menulis")
p("File <code>SahamExpertKB_v2.owl</code> memakai format <b>RDF/XML</b>; file Fuseki <code>saham_data.ttl</code> memakai "
  "<b>Turtle</b>. Isinya sama, hanya cara menulisnya berbeda. Turtle jauh lebih mudah dibaca manusia:")
code("""@prefix ex:  <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:ANTM  a                  ex:Emiten ;            # a = rdf:type
         ex:termasukSektor  ex:Sektor_BarangBaku ;
         ex:roe             "18.0"^^xsd:double ;
         ex:der             "0.3"^^xsd:double .""", "Turtle (.ttl)")
code("""<owl:NamedIndividual rdf:about="#ANTM">
  <rdf:type rdf:resource="#Emiten"/>
  <termasukSektor rdf:resource="#Sektor_BarangBaku"/>
  <roe rdf:datatype="http://www.w3.org/2001/XMLSchema#double">18.0</roe>
</owl:NamedIndividual>""", "RDF/XML (.owl)")

h2("1.4", "RDFS dan OWL: memberi makna pada triple")
p("RDF hanya mengatur bentuk triple. Agar komputer tahu <i>arti</i> sebuah kelas atau properti, dipakai dua bahasa di atasnya: "
  "<b>RDFS</b> (sederhana: kelas, subkelas, domain, range) dan <b>OWL</b> (Web Ontology Language, lebih kaya). Aksioma OWL yang "
  "dipakai di proyek ini:")
table(["Aksioma", "Arti", "Contoh"], [
    ["subClassOf", "setiap anggota A juga anggota B", "EmitenPerbankan subClassOf Emiten"],
    ["domain / range", "properti ini menghubungkan kelas apa ke apa", "termasukSektor: domain Emiten, range Sektor"],
    ["disjointWith", "tidak boleh ada individu di dua kelas ini sekaligus", "PolaBullish vs PolaBearish; EmitenPerbankan vs EmitenNonKeuangan"],
    ["equivalentClass", "dua kelas punya anggota yang persis sama", "tidak dipakai di proyek ini; hierarki cukup dengan subClassOf"],
    ["owl:imports", "masukkan seluruh isi ontologi lain", "modul alignment mengimpor SahamExpertKB (Bab 1.8)"],
], ["20%", "42%", "38%"])
h3("Dua asumsi yang sering menjebak")
p("<b>Open World Assumption (OWA).</b> Di basis data biasa, kalau suatu fakta tidak ada, dianggap salah. Di OWL, fakta yang tidak "
  "ada berarti <i>tidak diketahui</i>. Kalau ANTM tidak tercatat sebagai anggota LQ45, reasoner tidak menyimpulkan ANTM <i>bukan</i> "
  "anggota LQ45. Inilah sebabnya aturan SWRL proyek ini dibuat berpasangan dengan interval lengkap (Bab 1.6), bukan bergantung pada "
  "\"kalau tidak, maka…\".")
p("<b>No Unique Name Assumption.</b> OWL tidak otomatis menganggap dua nama berbeda sebagai dua benda berbeda. Bila perlu, "
  "kesamaan atau perbedaan dinyatakan eksplisit dengan <code>owl:sameAs</code> atau <code>owl:differentFrom</code>.")
h3("Tingkat ekspresivitas: SROIQ(D)")
p("Setiap huruf pada nama logika deskripsi menandai jenis aksioma yang dipakai. OWL 2 DL setara dengan SROIQ(D). Pemeriksa "
  "ekspresivitas OWLAPI (yang juga dipakai Protégé di <i>Active ontology › Ontology metrics</i>) melaporkan SahamExpertKB pada tingkat "
  "<b>SROIQ(D)</b>:")
table(["Huruf", "Arti", "Aksioma di SahamExpertKB"], [
 ["S", "ALC + peran transitif", "<code>memengaruhiIndeks</code> transitif (NASDAQ → MSCI EM → IHSG)"],
 ["R", "karakteristik dan inklusi peran kompleks", "<code>menyebabkan</code> asimetris dan irefleksif; <code>menguntungkanSektor</code> disjoint dengan <code>merugikanSektor</code>"],
 ["O", "nominal (individu dalam aksioma kelas)", "tiga skenario dan empat regime dinyatakan berbeda (<code>owl:AllDifferent</code>); restriksi <code>IndeksSektoralBEI ⊑ diterbitkanOleh value Penyedia_BEI</code> di modul alignment"],
 ["I", "peran invers", "<code>anggotaIndeks</code> ⇄ <code>memilikiKonstituen</code>"],
 ["Q", "kardinalitas berkualifikasi", "<code>Emiten ⊑ =1 termasukSektor.Sektor</code>; <code>PenilaianSektor ⊑ =1 dibawahSkenario.Skenario</code>; <code>TesisInvestasi ⊑ =1 indikatorKunciTesis.IndikatorMakro</code>"],
 ["(D)", "tipe data", "220 data property ber-range XSD (decimal, integer, string, …)"],
], ["9%", "31%", "60%"])
note("Restriksi nominal eksplisit sengaja ditaruh di modul alignment. Saat diuji di ontologi inti, satu restriksi hasValue membuat Pellet "
     "melambat dari ±6 detik menjadi ±2,5 menit karena berinteraksi dengan 303 aturan SWRL dan 1.392 individu. Ini contoh keputusan "
     "modularisasi dalam ontology engineering.", "dosen")

h2("1.5", "Reasoner: mesin yang menyimpulkan")
p("<b>Reasoner</b> adalah program yang membaca ontologi lalu mengerjakan empat hal: memeriksa <b>konsistensi</b> (tidak ada "
  "kontradiksi), <b>mengklasifikasi</b> hierarki kelas, <b>menjalankan aturan</b>, dan <b>merealisasi</b> individu (menentukan setiap "
  "individu masuk kelas mana saja). Hasilnya berupa fakta baru yang tidak pernah diketik siapa pun.")
fig(D.d_reasoner(), "Masukan dan keluaran reasoner untuk ANTM.")
table(["Reasoner", "Dipakai di", "Mendukung SWRL + built-in?", "Catatan"], [
    ["<b>Pellet</b>", "Protégé dan run_all.py (via owlready2)", "ya", "reasoner utama proyek"],
    ["HermiT", "Protégé (bawaan)", "tidak untuk built-in", "jangan dipakai: skor tidak terbentuk"],
    ["Jena GenericRuleReasoner", "Fuseki dataset /saham", "lewat konversi SWRL → aturan Jena", "menalar langsung di server"],
    ["Drools", "SWRLTab/SQWRLTab di Protégé", "ya", "dipakai untuk query SQWRL"],
], ["22%", "30%", "23%", "25%"])
img("protege_antm.png", "Hasil Pellet di Protégé untuk ANTM. Baris berlatar putih adalah fakta dari data; baris kuning adalah kesimpulan reasoner, misalnya KandidatTopPickAdaptif dan FundamentalKuat.", "100%")

h2("1.6", "SWRL: aturan JIKA–MAKA")
p("OWL saja tidak bisa berhitung (\"skor = fundamental + valuasi + …\") atau membandingkan angka dengan ambang. Untuk itu dipakai "
  "<b>SWRL</b> (Semantic Web Rule Language), yaitu aturan berbentuk <b>JIKA (body) MAKA (head)</b>. Dosen menyarankan SWRL karena "
  "keputusan analis saham memang berupa aturan seperti ini.")
fig(D.d_swrl(), "Anatomi aturan R-FUND-01a.")
h3("Pola penting di proyek ini")
ul(["<b>Interval berpasangan.</b> SWRL tidak punya ELSE dan bersifat monoton (hanya menambah fakta, tidak pernah menghapus). "
    "Maka setiap skor dipecah menjadi beberapa aturan dengan interval [bawah, atas) yang tidak tumpang tindih dan menutup seluruh "
    "kemungkinan nilai. Soal uji A05 membuktikan setiap emiten mendapat tepat satu nilai per pilar.",
    "<b>Aritmetika dengan built-in.</b> <code>swrlb:add</code> menjumlahkan delapan pilar menjadi skor total; "
    "<code>swrlb:multiply</code> mengalikan dengan bobot regime menjadi skor adaptif.",
    "<b>Berantai.</b> Kesimpulan satu aturan menjadi masukan aturan lain: poin → skor pilar → skor total → skor adaptif → top pick.",
    "<b>Berkode dan berpilar.</b> Setiap aturan punya kode (R-FUND-01a, R-PAS-03, …) dan pilar analisis, sehingga bisa ditelusuri di "
    "SWRLTab dan dihitung per pilar."])
p("<b>SQWRL</b> adalah perluasan SWRL untuk <i>bertanya</i>, bukan menyimpulkan. Bagian kepalanya berisi <code>sqwrl:select</code>, "
  "<code>sqwrl:orderBy</code>, dan <code>sqwrl:limit</code>, mirip SQL. Contoh 32 query ada di <code>output/SQWRL_queries.txt</code>.")
code("termasukSektor(?e, Sektor_BarangBaku) ^ skorAdaptifRegime(?e, ?t)\n  -> sqwrl:select(?e, ?t) ^ sqwrl:orderByDescending(?t) ^ sqwrl:limit(3)", "SQWRL: top-3 Barang Baku")

h2("1.7", "SPARQL: bahasa untuk bertanya ke graf")
p("<b>SPARQL</b> bagi RDF adalah apa SQL bagi tabel. Bedanya, SPARQL tidak memilih kolom dari tabel, melainkan mencari <b>pola "
  "triple</b> di dalam graf. Inilah bahasa yang dipakai Fuseki dan dashboard.")
fig(D.d_sparql(), "Query SPARQL mencari emiten yang menjadi top pick pakar beserta skornya.")
table(["Bagian", "Fungsi", "Contoh"], [
    ["<code>PREFIX</code>", "singkatan namespace", "<code>PREFIX ex: &lt;…SahamExpertKB.owl#&gt;</code>"],
    ["<code>SELECT ?a ?b</code>", "variabel yang ditampilkan", "<code>SELECT ?kode ?skor</code>"],
    ["<code>WHERE { … }</code>", "pola triple yang harus cocok", "<code>?e ex:kodeSaham ?kode .</code>"],
    ["<code>FILTER(…)</code>", "syarat tambahan", "<code>FILTER(?skor &gt;= 25)</code>"],
    ["<code>OPTIONAL { … }</code>", "pola boleh tidak ada (seperti LEFT JOIN)", "<code>OPTIONAL { ?e ex:der ?der }</code>"],
    ["<code>ORDER BY / LIMIT</code>", "urutkan, batasi jumlah", "<code>ORDER BY DESC(?skor) LIMIT 3</code>"],
    ["<code>GROUP BY, COUNT</code>", "agregasi", "<code>SELECT ?pilar (COUNT(?r) AS ?n)</code>"],
    ["<code>ASK</code>", "jawab ya/tidak", "<code>ASK { ?k a ex:KapitulasiPasar }</code>"],
    ["<code>INSERT / DELETE</code>", "mengubah data (SPARQL Update)", "dipakai fitur what-if dashboard"],
], ["22%", "36%", "42%"])
code("""PREFIX ex: <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?sektor ?skor WHERE {
  ?s a ex:SektorBullish ;              # sektor yang disimpulkan naik
     rdfs:label ?sektor ;
     ex:skorOutlookAktif ?skor .
} ORDER BY DESC(?skor)""", "Contoh lengkap: sektor yang diprediksi naik (hasil: Barang Baku 11, Kesehatan 8)")
note("SWRL membuat fakta baru (menalar), sedangkan SPARQL membaca fakta (bertanya). DL Query di Protégé juga bertanya, tetapi memakai "
     "bahasa kelas OWL (Manchester syntax), misalnya <code>Emiten and (anggotaIndeks value LQ45)</code>.", "info")

h2("1.8", "Ontologi eksternal: memakai ulang kosakata orang lain")
p("<b>Ontologi eksternal</b> adalah ontologi buatan pihak lain yang kita pakai ulang alih-alih membuat istilah sendiri. Tujuannya "
  "<b>interoperabilitas</b>: kalau dua sistem sama-sama memakai IRI yang sama untuk \"bank sentral\", data keduanya bisa digabung dan "
  "ditanyai bersama tanpa penerjemahan manual. Langkah ke-2 metodologi Ontology Development 101 berbunyi \"pertimbangkan memakai "
  "ulang ontologi yang sudah ada\".")
fig(D.d_eksternal(), "Lapisan ontologi yang dipakai dan tiga cara memakai ontologi eksternal.")
table(["Ontologi eksternal", "Pemilik", "Gunanya", "Dipakai di proyek?"], [
    ["RDF, RDFS, OWL, XSD", "W3C", "fondasi semua ontologi", "ya (wajib)"],
    ["SWRL, SWRLB", "W3C (member submission)", "aturan dan built-in", "ya (303 aturan)"],
    ["Dublin Core (<code>dcterms:</code>)", "DCMI", "metadata: judul, pembuat, tanggal, lisensi, sumber", "ya, di modul alignment"],
    ["SKOS (<code>skos:</code>)", "W3C", "pemetaan antar-konsep: exactMatch, closeMatch, broader", "ya, di modul alignment"],
    ["schema.org", "Google, Microsoft, dkk.", "kosakata umum web: Corporation, NewsArticle", "ya (Emiten, Berita)"],
    ["FIBO", "EDM Council", "ontologi industri keuangan: Issuer, EquityIndex, CentralBank", "ya (7 pemetaan)"],
    ["FOAF, OWL-Time, GeoNames", "komunitas / W3C", "orang, waktu, lokasi", "tidak (belum perlu)"],
], ["25%", "20%", "35%", "20%"])
h3("Contoh nyata di proyek: modul alignment")
p("Proyek ini punya file <code>output/SahamExpertKB_alignment.ttl</code>, yaitu ontologi kecil terpisah yang <b>mengimpor</b> "
  "SahamExpertKB lalu memetakan konsepnya ke FIBO dan schema.org. Semua IRI FIBO di dalamnya diverifikasi dari repositori resmi "
  "github.com/edmcouncil/fibo. FIBO lengkap terdiri dari ratusan file ontologi; kalau diimpor seluruhnya, ontologi proyek menjadi "
  "sangat berat. Karena itu FIBO cukup dirujuk IRI-nya (cara 1 dan 3), bukan diimpor (cara 2).")
code("""<http://kbr.kelompok9.id/ontologi/SahamExpertKB-alignment.owl>
    a owl:Ontology ;
    owl:imports <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl> ;     # cara 2: imports
    dcterms:creator "Kelompok 9 — Knowledge Based Reasoning" .              # Dublin Core

ex:BankSentral rdfs:subClassOf fibo-fbc-fct-fse:CentralBank .              # cara 3: dinalar Pellet
ex:BEI_Bursa   rdf:type        fibo-fbc-fct-mkt:Exchange .
ex:Emiten      skos:closeMatch fibo-fbc-fi-fi:Issuer , schema:Corporation . # cara 1: anotasi
ex:IndeksSaham skos:closeMatch fibo-ind-mkt-bas:EquityIndex .""", "Potongan SahamExpertKB_alignment.ttl")
p("Hasil uji dengan OWLAPI + Pellet: ontologi gabungan tetap <b>konsisten</b>, dan reasoner menyimpulkan BankIndonesia, TheFed, ECB, "
  "PBoC, dan BankOfJapan sebagai <code>fibo:CentralBank</code>, serta BEI_Bursa sebagai <code>fibo:Exchange</code>. Tidak ada satu "
  "pun yang diketik langsung; semuanya hasil penalaran dari satu aksioma <code>subClassOf</code>.")
h3("Mencoba di Protégé")
ol(["<i>File › Open</i> › <code>output/SahamExpertKB_alignment.ttl</code>. Protégé membaca <code>catalog-v001.xml</code> di folder yang sama, "
    "sehingga ontologi utama ikut termuat dari file lokal tanpa internet.",
    "Tab <i>Active ontology</i> › bagian <i>Ontology imports</i>: terlihat <i>Direct imports</i> berisi SahamExpertKB. Inilah wujud "
    "<code>owl:imports</code>.",
    "Jalankan Pellet, lalu DL Query: <code>fibo-fbc-fct-fse:CentralBank</code> (atau klik kelas <i>central bank (FIBO)</i> di hierarki). "
    "Hasilnya lima bank sentral.",
    "Untuk mengimpor ontologi dari internet: <i>Ontology imports › Direct imports ›</i> <b>+</b> › <i>Import an ontology contained in a "
    "document located on the web</i> › tempel IRI-nya."])
note("Ontologi eksternal = ontologi milik pihak lain yang dipakai ulang. Proyek ini memakai fondasi W3C (RDF, RDFS, OWL, XSD, SWRL) "
     "dan modul alignment ke FIBO, schema.org, SKOS, dan Dublin Core. FIBO tidak diimpor penuh karena terlalu besar; cukup dirujuk "
     "IRI-nya, dan satu aksioma subClassOf sudah membuat Pellet menyimpulkan Bank Indonesia sebagai CentralBank versi FIBO.", "dosen")

h2("1.9", "Metodologi: Ontology Development 101")
p("Proyek ini mengikuti panduan klasik Noy &amp; McGuinness (Stanford), ditambah tahap aturan dan pengujian. Urutan inilah yang "
  "dipakai di Bagian III untuk membangun dari awal.")
fig(D.d_od101(), "Tujuh langkah Ontology Development 101 ditambah tahap aturan dan uji.")

# =================================================================== BAGIAN II
bab("II", "Arsitektur SahamExpertKB", "Bagaimana semua komponen tersusun, dari CSV sampai rekomendasi saham, dan mengapa dirancang begitu.")
h2("2.1", "Gambaran besar")
p("SahamExpertKB adalah sistem pakar yang memprediksi sektor saham BEI yang berpeluang naik dalam 1–3 tahun, lalu memilih emiten "
  "teratas per sektor. Pengetahuannya mencakup fundamental, teknikal, bandarmology, sentimen berita, geopolitik dan makro, serta "
  "meta-penalaran pakar (regime pasar, tesis dan kill switch, skenario).")
fig(D.d_arsitektur(), "Arsitektur berlapis SahamExpertKB.")
table(["Keputusan desain", "Alasan"], [
    ["Data di CSV, ontologi dibangun oleh Python (owlready2)", "1.392 individu terlalu banyak untuk diketik manual di Protégé; CSV mudah diperbarui berdua"],
    ["Pellet sebagai reasoner utama", "mendukung SWRL beserta built-in aritmetika dan perbandingan"],
    ["Aturan berkode dan berpilar", "bisa ditelusuri (explanation) dan dihitung porsinya"],
    ["Dua mesin (Pellet + Jena)", "Pellet untuk validasi formal; Jena di Fuseki untuk melayani aplikasi dan what-if secara langsung"],
    ["Uji otomatis 103 soal", "setiap perubahan data langsung ketahuan dampaknya"],
], ["38%", "62%"])
h2("2.2", "Pipeline pembangunan")
fig(D.d_pipeline(), "Dua belas tahap yang dijalankan run_all.py.")
h2("2.3", "Struktur ontologi")
table(["Metrik", "Jumlah"], [["Kelas", NK], ["Object property", NOP], ["Data property", NDP], ["Individu", fmtn(NI)],
                             ["Aturan SWRL", NR], ["Total aksioma", fmtn(NAT)]], ["60%", "40%"])
table(["Cabang kelas teratas", "Isinya"], [
    ["KategoriInferensi (131 subkelas)", "semua kelas hasil penalaran: FundamentalKuat, SektorBullish, KandidatTopPickAdaptif, TesisGugur, …"],
    ["EntitasPasarModal (46)", "Emiten, Sektor, Subsektor, IndeksSaham (66 indeks: LQ45, MSCI, NASDAQ, …), Broker, Institusi"],
    ["AnalisisGeopolitikMakro (19)", "PeristiwaGeopolitik, PergerakanMakro, IndikatorMakro, Komoditas"],
    ["AnalisisTeknikal (16)", "IndikatorTeknikal (RSI, MACD, …), PolaChart, PolaCandlestick, TeoriTeknikal"],
    ["PengetahuanDasarSaham (15)", "mekanisme BEI, aksi korporasi, instrumen, bias perilaku, biaya &amp; pajak"],
    ["AnalisisFundamental (14)", "RasioKeuangan (40 rasio + rumus), MetodeValuasi, ModelSkorRisiko"],
    ["PenalaranPakar (14)", "RegimePasar, Skenario, TesisInvestasi, Katalis, PeriodeHistoris (case-based reasoning)"],
    ["AnalisisSentimen, Bandarmology", "Berita, KomponenML; KonsepBandarmology, PolaBandar"],
    ["Stakeholder, SumberData, dll.", "pemangku kepentingan dan persona investor; sumber data dan indikator"],
], ["35%", "65%"])
table(["Object property penting", "Domain → Range", "Contoh"], [
    ["termasukSektor", "Emiten → Sektor", "ANTM → Sektor_BarangBaku"],
    ["anggotaIndeks", "Emiten → IndeksSaham", "ANTM → LQ45, MSCI_Indonesia"],
    ["memicuPergerakan", "PeristiwaGeopolitik → PergerakanMakro", "Ev_FedHike_Sep2026 → Mv_YieldUSNaik"],
    ["menyebabkan", "PergerakanMakro → PergerakanMakro", "PremiRisikoTimurTengah → HargaMinyakNaik"],
    ["menguntungkanSektor", "PergerakanMakro → Sektor", "SafeHavenEmas → Sektor_BarangBaku"],
    ["regimeTerdeteksi", "KondisiPasar → RegimePasar", "Pasar_ID_Okt2026 → Regime_KrisisLikuiditas"],
    ["indikatorKunciTesis", "TesisInvestasi → IndikatorMakro", "Tesis_BarangBaku_EmasNikel → Makro_Emas"],
    ["direkomendasikanUntuk", "Emiten → InvestorRitel", "ANTM → Persona_GenZ_Agresif"],
], ["28%", "37%", "35%"])
h2("2.4", "Alur penalaran")
fig(D.d_alur_emiten(), "Dari data mentah ke rekomendasi untuk satu emiten.")
fig(D.d_alur_sektor(), "Dari berita ke prediksi sektor.")
p(f"Hasil per {TGL}: sektor inti <b>Barang Baku</b> dan <b>Kesehatan</b>; top pick sistem pakar <b>{', '.join(PICK)}</b>; regime "
  "<b>Krisis Likuiditas</b> (stres 11/12).")
h2("2.5", "Peta file proyek")
table(["File / folder", "Fungsi", "Disentuh siapa"], [
    ["<code>data/*.csv</code>", "semua data: emiten, makro, berita, kondisi pasar", "A + B (rutin)"],
    ["<code>kb_*.py</code>", "pengetahuan statis: taksonomi, konsep, geopolitik, pasar, v2", "A (bila menambah konsep)"],
    ["<code>rules_swrl.py</code>, <code>rules_v2.py</code>", "303 aturan SWRL", "A (bila menambah aturan)"],
    ["<code>build_ontology.py</code>", "merakit ontologi + menjalankan Pellet", "tidak perlu diubah"],
    ["<code>run_all.py</code>", "menjalankan 12 tahap", "dijalankan setiap data berubah"],
    ["<code>tools/uji_kb.py</code>", "uji 103 soal", "dijalankan otomatis"],
    ["<code>tools/swrl2jena.py</code>", "konversi SWRL → aturan Jena untuk Fuseki", "otomatis (tahap 7)"],
    ["<code>output/SahamExpertKB_v2.owl</code>", "ontologi untuk Protégé", "dibuka di Protégé"],
    ["<code>output/fuseki/</code>", "data, aturan, konfigurasi, skrip Fuseki", "Bagian IV"],
    ["<code>output/SahamExpertKB_alignment.ttl</code>", "modul ontologi eksternal", "Bab 1.8"],
    ["<code>dashboard/</code>", "dashboard live + server + skrip demo", "Bagian V"],
], ["38%", "42%", "20%"])

# =================================================================== BAGIAN III
h2("2.6", "Roadmap: dari proposal sampai dashboard, dan langkah berikutnya")
p("Proyek dikerjakan bertahap. Setiap fase menghasilkan artefak yang bisa diuji, dan fase berikutnya dibangun di atasnya.")
table(["Fase", "Kegiatan", "Hasil"], [
 ["1. Lingkup", "menentukan domain, stakeholder, dan 12 competency questions; menyusun proposal", "proposal + daftar CQ"],
 ["2. Akuisisi pengetahuan", "mengumpulkan heuristik pakar (rasio, teknikal, bandarmology, makro) dan data (IDX, BI, berita)", "CSV + log sumber"],
 ["3. Ontologi v1", "taksonomi pengetahuan saham, entitas pasar, konsep dasar", "kelas, properti, individu"],
 ["4. Aturan + reasoner", "aturan SWRL per pilar dengan pola interval berpasangan; Pellet", "skor emiten, prediksi sektor"],
 ["5. Ontologi v2 (meta-penalaran)", "regime pasar, skenario dan robustness, tesis + kill switch, CBR historis, geopolitik → emiten, persona", "303 aturan, skor adaptif"],
 ["6. Pengujian", "uji 12 CQ, 103 soal otomatis, what-if, perbaikan celah aturan (R-PAS-05)", "HASIL_UJI_KB.md (103/103)"],
 ["7. Penyajian", "Fuseki dua mesin (Pellet + Jena), modul alignment ontologi eksternal, dashboard live", "sistem siap demo"],
], ["22%", "52%", "26%"])
table(["Rencana berikutnya", "Manfaat"], [
 ["Pengambilan data otomatis (IDX, BI, berita)", "KB selalu mutakhir tanpa mengisi CSV manual"],
 ["Backtest historis berkala", "mengukur akurasi prediksi sektor dan top pick terhadap harga nyata"],
 ["Fuseki dengan TDB2 + autentikasi", "penyimpanan permanen dan aman untuk mitra sekuritas"],
 ["API rekomendasi per persona", "aplikasi sekuritas bisa memanggil langsung"],
 ["Explanation di dashboard", "menampilkan rantai aturan di balik setiap kesimpulan, seperti tombol ? di Protégé"],
 ["Perluasan emiten dan pemetaan FIBO", "cakupan pasar lebih luas, interoperabilitas lebih dalam"],
], ["45%", "55%"])

bab("III", "Membangun dari awal", "Sembilan langkah merancang knowledge base seperti SahamExpertKB, plus latihan membuat ontologi mini dengan tangan di Protégé.")
LANGKAH = [
    ("Tentukan domain, tujuan, dan competency questions",
     "Tulis pertanyaan yang <b>wajib</b> bisa dijawab KB. Pertanyaan ini menjadi batas lingkup sekaligus alat uji. Contoh proyek: "
     "\"Sektor apa yang naik 1–3 tahun?\", \"Emiten mana yang rawan collapse?\", \"Apa dampak The Fed?\" (12 CQ di proposal, "
     "diperluas menjadi 103 soal uji)."),
    ("Kumpulkan sumber pengetahuan",
     "Pengetahuan pakar (buku analisis saham, ambang rasio, heuristik analis) dan data (laporan keuangan IDX, BI, berita). Catat "
     "sumber setiap angka; proyek ini menyimpannya di <code>data/log_sumber_emiten.csv</code> dan kolom URL di CSV."),
    ("Pakai ulang ontologi yang ada",
     "Gunakan fondasi W3C, lalu cari ontologi domain (FIBO untuk keuangan). Putuskan: diimpor, dirujuk IRI-nya, atau dipetakan "
     "(Bab 1.8)."),
    ("Daftar istilah, lalu susun kelas dan hierarki",
     "Tulis semua kata benda penting (emiten, sektor, rasio, berita, regime…), kelompokkan menjadi kelas, lalu susun dari umum ke "
     "khusus. Pisahkan kelas <i>entitas</i> (Emiten) dari kelas <i>kesimpulan</i> (FundamentalKuat) supaya rapi."),
    ("Definisikan properti",
     "Object property untuk hubungan (termasukSektor), data property untuk angka (roe, der). Beri domain dan range."),
    ("Isi individu (data)",
     "Untuk data besar, isi lewat skrip dari CSV (owlready2), bukan mengetik di Protégé. Satu baris CSV = satu individu beserta "
     "properti-propertinya."),
    ("Tulis aturan SWRL",
     "Terjemahkan heuristik pakar menjadi aturan. Gunakan pola interval berpasangan agar setiap individu pasti mendapat satu nilai. "
     "Beri kode dan pilar pada setiap aturan."),
    ("Jalankan reasoner dan uji",
     "Pellet: cek konsistensi, lihat hasil inferensi. Jalankan uji competency questions; kalau gagal, kembali ke langkah 4–7."),
    ("Sajikan",
     "Pasang di Fuseki agar bisa ditanyai aplikasi lewat SPARQL, lalu buat antarmuka (dashboard)."),
]
for i, (t, s) in enumerate(LANGKAH, 1):
    w(f'<div class="step"><b class="n">{i}</b><b>{t}</b><br>{s}</div>')
h2("3.1", "Latihan: ontologi mini di Protégé (±30 menit)")
p("Latihan ini membuat versi kecil SahamExpertKB dengan tangan, supaya kamu paham apa yang dikerjakan skrip Python secara otomatis. "
  "Kerjakan di file baru (<i>File › New</i>).")
STEPS = [
    ("Beri nama ontologi", "Tab <i>Active ontology</i> › <i>Ontology IRI</i>: <code>http://contoh.id/saham-mini</code>."),
    ("Buat kelas", "Tab <i>Entities › Classes</i> › pilih <code>owl:Thing</code> › ikon <i>Add subclass</i>. Buat <code>Emiten</code>, <code>Sektor</code>, dan <code>FundamentalKuat</code>."),
    ("Buat object property", "<i>Object properties</i> › <b>+</b> › <code>termasukSektor</code>; isi <i>Domains</i> = Emiten, <i>Ranges</i> = Sektor."),
    ("Buat data property", "<i>Data properties</i> › <b>+</b> › <code>roe</code> (range <code>xsd:decimal</code>) dan <code>der</code> (range <code>xsd:decimal</code>)."),
    ("Buat individu", "<i>Individuals</i> › <b>+</b> › <code>ANTM</code>; <i>Types</i> = Emiten; <i>Object property assertions</i>: termasukSektor BarangBaku (buat individu <code>BarangBaku</code> bertipe Sektor); <i>Data property assertions</i>: roe 18.0, der 0.3. Buat juga <code>BUMI</code> dengan roe 4.0, der 2.5."),
    ("Tulis aturan", "<i>Window › Tabs › SWRLTab</i> › <i>New</i>, tempel aturan di bawah, beri nama <code>R1</code>."),
    ("Jalankan reasoner", "<i>Reasoner › Pellet › Start reasoner</i>. Klik ANTM: muncul <code>FundamentalKuat</code> berlatar kuning. BUMI tidak."),
    ("Bertanya", "Tab <i>DL Query</i>: ketik <code>FundamentalKuat</code>, centang <i>Instances</i>, klik <i>Execute</i> → ANTM."),
]
for i, (t, s) in enumerate(STEPS, 1):
    w(f'<div class="step"><b class="n">{i}</b><b>{t}.</b> {s}</div>')
code("Emiten(?e) ^ roe(?e, ?r) ^ der(?e, ?d) ^ swrlb:greaterThanOrEqual(?r, 15.0) ^ swrlb:lessThan(?d, 0.5)\n  -> FundamentalKuat(?e)", "Aturan R1 untuk latihan")
note("Inilah yang dilakukan <code>build_ontology.py</code>, hanya dalam skala 298 kelas, 1.392 individu, dan 303 aturan. Bila dosen "
     "meminta bukti kamu bisa membuat ontologi tanpa skrip, latihan ini yang kamu tunjukkan.", "dosen")
h2("3.2", "Menambah sesuatu ke SahamExpertKB")
table(["Ingin menambah", "Ubah", "Lalu"], [
    ["emiten baru", "satu baris di <code>data/emiten.csv</code> (kolom lihat <code>data/kamus_kolom.json</code>)", "<code>python3 validasi_data.py</code> → <code>python3 run_all.py</code>"],
    ["berita baru", "satu baris di <code>data/berita.csv</code> (isi kolom peristiwa dengan ID yang ada)", "<code>python3 run_all.py</code>"],
    ["angka makro baru", "<code>data/makro.csv</code> dan <code>data/kondisi_pasar.csv</code>; perbarui <code>data/tanggal_acuan.txt</code>", "<code>python3 run_all.py</code>"],
    ["aturan baru", "tambahkan <code>R(\"KODE\", \"Pilar\", \"keterangan\", \"aturan SWRL\")</code> di <code>rules_v2.py</code>", "build, lalu tambah soal uji di <code>tools/uji_kb.py</code>"],
    ["konsep baru", "kelas/individu di <code>kb_concepts.py</code> atau <code>kb_v2.py</code>", "build + uji"],
], ["20%", "50%", "30%"])

# =================================================================== BAGIAN IV
bab("IV", "Apache Jena Fuseki", "Apa itu Fuseki, kenapa proyek ini membutuhkannya, dan cara memasang, menjalankan, serta menanyainya, langkah demi langkah di Mac.")
h2("4.1", "Apa itu Fuseki?")
p("<b>Apache Jena Fuseki</b> adalah <b>server SPARQL</b>: program yang menyimpan graf RDF (disebut <i>dataset</i>) dan menjawab "
  "query SPARQL yang dikirim lewat HTTP, persis seperti server web menjawab permintaan halaman. Fuseki adalah bagian dari Apache "
  "Jena, kerangka kerja Java untuk web semantik.")
fig(D.d_fuseki(), "Peran Fuseki: menerima query dari banyak program dan menjawab dalam format JSON.")
table(["", "Protégé", "Fuseki"], [
    ["Analogi", "Microsoft Word / meja kerja", "server basis data (seperti MySQL)"],
    ["Fungsi utama", "merancang, mengedit, mengecek ontologi", "melayani ontologi ke program lain"],
    ["Pengguna", "satu orang di satu laptop", "banyak program sekaligus lewat jaringan"],
    ["Cara bertanya", "DL Query, SQWRL (klik di aplikasi)", "SPARQL lewat HTTP (dari kode apa pun)"],
    ["Reasoner", "Pellet, HermiT, Drools", "aturan Jena (GenericRuleReasoner), RDFS, OWL-mini"],
], ["20%", "40%", "40%"])
h3("Kenapa proyek ini butuh Fuseki")
ul(["<b>Stakeholder utama</b> proyek adalah mitra sekuritas yang ingin menanamkan sistem pakar di aplikasinya. Aplikasi tidak bisa "
    "\"membuka Protégé\"; ia butuh alamat yang bisa ditanya, misalnya <code>http://server:3030/saham/query</code>.",
    "<b>Bahasa apa pun</b> bisa bertanya: Python, Java, JavaScript (dashboard), PHP, bahkan <code>curl</code> di terminal.",
    "<b>What-if langsung</b>: dengan SPARQL Update, data bisa diubah dan aturan menalar ulang di server dalam hitungan detik.",
    "<b>Validasi silang</b>: Fuseki memakai mesin aturan Jena, berbeda dari Pellet. Hasil yang sama dari dua mesin berbeda adalah "
    "bukti aturannya benar, bukan kebetulan perilaku satu reasoner."])
h3("Istilah Fuseki")
table(["Istilah", "Artinya", "Di proyek"], [
    ["Dataset", "kumpulan graf RDF yang dilayani dengan satu nama", "<code>/saham</code> dan <code>/saham-pellet</code>"],
    ["Endpoint", "alamat untuk operasi tertentu", "<code>/saham/query</code> (baca), <code>/saham/update</code> (ubah)"],
    ["Port", "\"pintu\" jaringan tempat server mendengar", "3030 (bawaan Fuseki)"],
    ["Konfigurasi assembler", "file Turtle yang menjelaskan dataset dan reasoner", "<code>output/fuseki/config_saham.ttl</code>"],
    ["InfModel", "graf yang dilengkapi reasoner", "dataset /saham"],
    ["TDB2", "penyimpanan permanen di disk", "tidak dipakai; proyek memakai memori agar selalu segar dari file"],
], ["24%", "42%", "34%"])

h2("4.2", "Memasang Fuseki di Mac")
STEPS = [
    ("Pastikan Java 21 atau lebih baru", "Jena 6 membutuhkan Java 21+. Cek dengan <code>java -version</code>; di laptopmu sudah ada Temurin 25.0.5."),
    ("Unduh", "Buka <code>https://jena.apache.org/download/</code> › bagian <i>Apache Jena Fuseki</i> › unduh <code>apache-jena-fuseki-6.3.0.zip</code> (versi terbaru saat buku ini ditulis)."),
    ("Ekstrak ke Downloads", "Klik dua kali file zip-nya. Hasilnya folder <code>~/Downloads/apache-jena-fuseki-6.3.0</code> yang berisi <code>fuseki-server</code>."),
    ("Izinkan dijalankan", "macOS memblokir program hasil unduhan. Jalankan sekali di Terminal:"),
]
for i, (t, s) in enumerate(STEPS, 1):
    w(f'<div class="step"><b class="n">{i}</b><b>{t}.</b> {s}</div>')
code("""cd ~/Downloads/apache-jena-fuseki-6.3.0
chmod +x fuseki-server                         # izin eksekusi
/usr/bin/xattr -dr com.apple.quarantine .                      # lepas karantina Gatekeeper""")
note("Kalau versi yang kamu unduh berbeda (misalnya 6.4.0), cukup sesuaikan nama folder di semua perintah buku ini.", "tip")

h2("4.3", "Konfigurasi proyek, dijelaskan baris per baris")
p("Proyek sudah menyediakan konfigurasi siap pakai. <code>start_fuseki.sh</code> membuat <code>config_saham.ttl</code> dari "
  "templatnya dengan mengganti <code>__DIR__</code> menjadi lokasi folder di laptopmu.")
fig(D.d_dua_dataset(), "Dua dataset yang dilayani Fuseki dalam proyek ini.")
code("""[] rdf:type fuseki:Server .                              # deklarasi: ini konfigurasi server

:svcSaham rdf:type fuseki:Service ;                      # LAYANAN pertama
    fuseki:name "saham" ;                                # → http://localhost:3030/saham
    fuseki:endpoint [ fuseki:operation fuseki:query ;  fuseki:name "query" ] ;    # /saham/query
    fuseki:endpoint [ fuseki:operation fuseki:update ; fuseki:name "update" ] ;   # /saham/update
    fuseki:dataset :dsSaham .

:dsSaham rdf:type ja:RDFDataset ; ja:defaultGraph :infSaham .

:infSaham rdf:type ja:InfModel ;                         # graf + REASONER
    ja:reasoner [
        ja:reasonerURL <http://jena.hpl.hp.com/2003/GenericRuleReasoner> ;
        ja:rulesFrom <file://…/saham_rules.rules> ] ;   # 305 aturan hasil konversi SWRL
    ja:baseModel :baseSaham .

:baseSaham rdf:type ja:MemoryModel ;                     # data dimuat ke memori
    ja:content [ ja:externalContent <file://…/saham_data.ttl> ] .

:svcPellet … fuseki:name "saham-pellet" …                # LAYANAN kedua: hasil Pellet, hanya baca
    ja:content [ ja:externalContent <file://…/SahamExpertKB_v2_inferred.owl> ] .""", "config_saham.template.ttl (diringkas)")
h3("Dari mana aturan Jena berasal?")
p("Fuseki tidak bisa membaca SWRL secara langsung. Tahap 7 <code>run_all.py</code> menjalankan <code>tools/swrl2jena.py</code> yang "
  "menerjemahkan ke-303 aturan SWRL menjadi sintaks aturan Jena, lalu menambahkan 2 aturan RDFS supaya hierarki kelas ikut "
  "diturunkan (total 305). Tahap 8 mengubah angka desimal menjadi <code>xsd:double</code> karena mesin aturan Jena membandingkan "
  "angka lebih andal dalam tipe itu.")
code("""# SWRL (Protégé / Pellet)
Emiten(?e) ^ roe(?e, ?v) ^ swrlb:greaterThanOrEqual(?v, 15.0) -> poinROE(?e, 2)

# Aturan Jena (Fuseki) hasil swrl2jena.py
[R_FUND_01a: (?e rdf:type ex:Emiten) (?e ex:roe ?v) ge(?v, '15.0'^^xsd:double) -> (?e ex:poinROE 2)]""", "Aturan yang sama dalam dua bahasa")

h2("4.4", "Menjalankan Fuseki")
code("""cd ~/Downloads/KBR_Kelompok9_SahamExpertKB_v2
python3 run_all.py                                          # pastikan file Fuseki terbaru
bash output/fuseki/start_fuseki.sh ~/Downloads/apache-jena-fuseki-6.3.0""")
p("Terminal akan menampilkan versi Java, lokasi config, lalu log Fuseki. Server siap ketika muncul baris berisi <b>Started</b> dan "
  "<b>port 3030</b>. Biarkan jendela Terminal ini terbuka; menutupnya berarti mematikan server. Tekan <b>Ctrl+C</b> untuk berhenti.")
note("Saat dataset /saham dimuat, mesin aturan Jena langsung menalar ke-305 aturan atas sekitar 27.000 triple. Proses ini memakan "
     "beberapa detik; pada pengujian penalaran awal selesai dalam ±1,5 detik.", "info")
h3("Mengecek server dari Terminal kedua")
code("""curl http://localhost:3030/$/ping                          # jawaban: tanggal/waktu = server hidup
curl http://localhost:3030/$/datasets                      # daftar dataset (JSON)""")

h2("4.5", "Bertanya lewat antarmuka web Fuseki")
STEPS = [
    ("Buka", "<code>http://localhost:3030</code> di browser. Halaman <i>Datasets</i> menampilkan <code>/saham</code> dan <code>/saham-pellet</code>."),
    ("Pilih dataset", "Klik tombol <b>query</b> di baris <code>/saham-pellet</code>. Muncul editor SPARQL dengan contoh query."),
    ("Tempel query", "Hapus contoh, tempel query dari <code>output/uji_kb/queries_uji.rq</code> (salin mulai baris PREFIX sampai sebelum <code>###</code> berikutnya) atau dari contoh di bawah."),
    ("Jalankan", "Klik tombol ▶. Hasil tampil sebagai tabel; bisa diganti ke tampilan JSON atau diunduh CSV."),
    ("Info dataset", "Tab <i>info</i> menunjukkan jumlah triple dan statistik permintaan."),
]
for i, (t, s) in enumerate(STEPS, 1):
    w(f'<div class="step"><b class="n">{i}</b><b>{t}.</b> {s}</div>')
code("""PREFIX ex: <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>
SELECT ?kode ?statis ?adaptif WHERE {
  ?e a ex:KandidatTopPickAdaptif ;
     ex:kodeSaham ?kode ;
     ex:skorTotalEmiten ?statis ;
     ex:skorAdaptifRegime ?adaptif .
} ORDER BY DESC(?adaptif)""", "Query pertama: top pick sistem pakar")
p(f"Hasil yang benar: tujuh baris, {', '.join(PICK)} (urut menurut skor adaptif, ANTM teratas dengan 35,0).")

h2("4.6", "Bertanya dari Terminal dan dari program")
p("Inilah kekuatan Fuseki: program apa pun cukup mengirim HTTP POST. Jawaban dalam format JSON standar SPARQL.")
code("""curl -s http://localhost:3030/saham-pellet/query \\
  -H 'Accept: application/sparql-results+json' \\
  --data-urlencode 'query=PREFIX ex: <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>
SELECT ?stres WHERE { ex:Pasar_ID_Okt2026 ex:skorStresPasar ?stres }'""", "Terminal (curl)")
code("""{ "head": { "vars": [ "stres" ] },
  "results": { "bindings": [
      { "stres": { "type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#int", "value": "11" } } ] } }""", "Jawaban JSON")
code("""import json, urllib.parse, urllib.request
q = '''PREFIX ex: <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>
SELECT ?kode WHERE { ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode }'''
data = urllib.parse.urlencode({"query": q}).encode()
req = urllib.request.Request("http://localhost:3030/saham-pellet/query", data,
                             {"Accept": "application/sparql-results+json"})
hasil = json.load(urllib.request.urlopen(req))
print([b["kode"]["value"] for b in hasil["results"]["bindings"]])""", "Python (tanpa pustaka tambahan)")

h2("4.7", "Mengubah data: SPARQL Update dan what-if")
p("Endpoint <code>/saham/update</code> menerima perintah <code>DELETE</code>/<code>INSERT</code>. Karena dataset /saham dilengkapi "
  "reasoner, setiap perubahan membuat ke-305 aturan menghitung ulang kesimpulan secara otomatis.")
code("""PREFIX ex:  <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
DELETE WHERE { ex:Pasar_ID_Okt2026 ex:cds5YBps ?lama } ;
INSERT DATA  { ex:Pasar_ID_Okt2026 ex:cds5YBps "75.0"^^xsd:double }""", "Contoh: CDS Indonesia turun ke 75 bps")
ol(["Di UI Fuseki pilih dataset <code>/saham</code> › <b>query</b>, lalu ganti endpoint (kolom <i>SPARQL endpoint</i>) menjadi "
    "<code>/saham/update</code>. Atau pakai file siap pakai <code>output/fuseki/whatif_update.ru</code>.",
    "Jalankan. Jawaban: <i>Update succeeded</i>.",
    "Kembali ke endpoint <code>/saham/query</code>, tanyakan skor stres: hasilnya turun dari 11 menjadi 10, dan "
    "<code>Tesis_Keuangan_Kontrarian</code> menjadi <code>TesisTerpicu</code>.",
    "Untuk mengembalikan data asli, matikan lalu nyalakan lagi Fuseki (data dimuat ulang dari file), atau tekan <b>Reset</b> di dashboard."])
note("Perubahan lewat SPARQL Update hanya ada di memori server dan hilang saat Fuseki dimatikan. File <code>saham_data.ttl</code> "
     "tidak pernah berubah. Ini disengaja, supaya eksperimen what-if tidak merusak data proyek.", "warn")
note("Pellet adalah reasoner OWL yang dipakai untuk validasi formal di Protégé dan pipeline. Fuseki memakai mesin aturan Jena yang "
     "menjalankan aturan yang sama hasil konversi otomatis. Keduanya diuji memberi hasil identik (regime, skor stres, 7 top pick), "
     "dan Fuseki memungkinkan aplikasi lain bertanya lewat HTTP serta melakukan what-if secara langsung.", "dosen")

# =================================================================== BAGIAN V
bab("V", "Dashboard web live", "Tampilan yang menanyai knowledge base secara langsung lewat Fuseki, cocok untuk presentasi dan untuk memperlihatkan bentuk produk ke stakeholder.")
h2("5.1", "Arsitektur")
fig(D.d_dashboard(), "Tiga program yang bekerja sama saat dashboard dibuka.")
p("Tidak ada angka yang ditulis tetap di halaman. Setiap panel mengirim query SPARQL ke Fuseki saat dibuka; tombol <i>lihat SPARQL</i> "
  "di setiap panel menampilkan query-nya, sehingga dashboard sekaligus menjadi alat belajar SPARQL.")
h2("5.2", "Menjalankan")
h3("Cara cepat: satu perintah")
code("""cd ~/Downloads/KBR_Kelompok9_SahamExpertKB_v2
./dashboard/start_demo.sh ~/Downloads/apache-jena-fuseki-6.3.0""")
p("Skrip menyalakan Fuseki di latar belakang (log di <code>output/fuseki/fuseki.log</code>), menunggu sampai server siap, lalu "
  "menyalakan dashboard dan membuka browser ke <code>http://localhost:8080</code>. Tekan <b>Ctrl+C</b> untuk mematikan keduanya.")
h3("Cara manual: dua jendela Terminal")
code("""# Terminal 1 — server knowledge base
bash output/fuseki/start_fuseki.sh ~/Downloads/apache-jena-fuseki-6.3.0

# Terminal 2 — dashboard (setelah Terminal 1 menampilkan "Started")
python3 dashboard/server.py""")
note("Indikator di kanan atas dashboard harus hijau dengan tulisan <i>Terhubung · /saham-pellet · … triple</i>. Kalau merah, Fuseki "
     "belum menyala atau masih memuat; tunggu beberapa detik lalu muat ulang halaman.", "tip")
h2("5.3", "Membaca setiap visualisasi")
p("Setiap panel di bawah dijelaskan dengan pola yang sama: <b>apa yang ditampilkan</b>, <b>cara membacanya</b>, <b>dari mana angkanya</b> "
  "(aturan SWRL yang menghasilkan), <b>contoh dari data saat ini</b>, dan <b>kalimat untuk presentasi</b>. Kalimat presentasi bisa "
  "langsung kamu ucapkan saat menunjuk panel tersebut.")
def vis(rows):
    table(["", ""], [[f"<b>{a}</b>", b] for a, b in rows], ["22%", "78%"])

h3("A. Header: status koneksi dan sumber penalaran")
img("dash_atas.png", "Bagian atas dashboard: status koneksi, pilihan sumber penalaran, kartu regime dan indikator pasar.")
vis([
 ("Ditampilkan", "Lampu status, nama dataset yang sedang ditanyai, jumlah triple di dataset itu, dan dua tombol sumber: <i>Pellet (hasil jadi)</i> dan <i>Jena (penalaran langsung)</i>."),
 ("Cara membaca", "Hijau berarti Fuseki menjawab. Jumlah triple dihitung dengan <code>SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }</code>. Dataset Pellet (±37.500 triple) lebih besar dari data mentah (±27.200 triple) karena sudah berisi hasil inferensi."),
 ("Dari mana", "Tombol Pellet menanyai <code>/saham-pellet</code> (inferensi Pellet yang sudah jadi). Tombol Jena menanyai <code>/saham</code>, yang menalar sendiri dengan 305 aturan hasil terjemahan SWRL."),
 ("Kalimat presentasi", "\"Setiap angka di halaman ini diambil langsung dari knowledge base lewat SPARQL ke Fuseki. Kalau saya pindah ke mesin Jena, angkanya tetap sama. Artinya dua reasoner berbeda menghasilkan kesimpulan yang sama dari aturan yang sama.\""),
])
h3("B. Kartu regime pasar")
vis([
 ("Ditampilkan", "Regime yang terdeteksi (saat ini <b>Krisis Likuiditas / Kapitulasi</b>) dan skor stres <b>11/12</b>."),
 ("Cara membaca", "Makin tinggi skor stres, makin defensif bobot analisis. ≥ 8 Krisis Likuiditas, 5–7 Risk-Off, 3–4 Netral, &lt; 3 Risk-On (aturan R-REG-01..04)."),
 ("Dari mana", "R-STR-01..06 memberi 0–2 poin untuk enam indikator, R-STR-07 menjumlahkannya dengan <code>swrlb:add</code>."),
 ("Kalimat presentasi", "\"Sistem tidak menilai saham dengan cara yang sama di semua kondisi. Enam indikator stres memberi skor 11 dari 12, jadi regime-nya krisis. Karena itu bobot fundamental, valuasi, dan smart money dinaikkan menjadi 1,5, sedangkan teknikal dan sentimen diturunkan menjadi 0,5.\""),
])
table(["Indikator", "Nilai sekarang", "2 poin", "1 poin", "0 poin", "Poin"], [
 ["Drawdown IHSG", "−39,3%", "≤ −30%", "−30 s.d. −15%", "&gt; −15%", "2"],
 ["CDS Indonesia 5Y", "99,6 bps", "≥ 120", "80–120", "&lt; 80", "1"],
 ["Net asing YTD", "−97,62 T", "≤ −50 T", "−50 s.d. −10 T", "&gt; −10 T", "2"],
 ["Kurs USD/IDR", "18.232", "≥ 17.500", "16.500–17.500", "&lt; 16.500", "2"],
 ["Yield SBN 10Y", "7,668%", "≥ 7,5%", "6,75–7,5%", "&lt; 6,75%", "2"],
 ["Breadth (% saham &gt; MA200)", "18,75%", "&lt; 25%", "25–50%", "≥ 50%", "2"],
 ["<b>Skor stres</b>", "", "", "", "", "<b>11</b>"],
], ["26%", "16%", "14%", "17%", "15%", "12%"])
table(["Bobot pilar", "Fund.", "Val.", "Tekn.", "Bandar", "Sent.", "Sektor", "Risiko", "Likuid.", "Smart money", "Ambang top pick"], [
 ["<b>Krisis Likuiditas</b> (aktif)", "1,5", "1,5", "0,5", "1,0", "0,5", "1,0", "1,5", "1,0", "1,5", "24,7"],
 ["Risk-Off", "1,2", "1,0", "0,8", "1,2", "0,8", "1,0", "1,2", "1,0", "1,2", "23,79"],
 ["Netral", "1,0", "1,0", "1,0", "1,0", "1,0", "1,0", "1,0", "1,0", "1,0", "22,75"],
 ["Risk-On", "0,8", "0,7", "1,3", "1,2", "1,2", "1,0", "0,8", "1,0", "1,0", "23,14"],
])
h3("C. Kartu indikator pasar")
vis([
 ("Ditampilkan", "BI-Rate 6% (inflasi 3,23%), CDS 99,6 bps, drawdown IHSG −39,3%, USD/IDR 18.232 (net asing −97,62 T), emas US$3.746/oz, Brent US$91,95/barel."),
 ("Cara membaca", "Ini fakta masukan (ABox) dari <code>data/kondisi_pasar.csv</code> dan <code>data/makro.csv</code>, bukan hasil penalaran. Setiap kartu terhubung ke aturan tertentu."),
 ("Dipakai aturan", "CDS ≥ 90 → <code>PremiRisikoNegaraTinggi</code> (R-PAS-01). Emas menjadi indikator kill switch tesis Barang Baku, Brent untuk tesis Energi, kurs untuk tesis Kesehatan, inflasi untuk tesis Konsumen Primer, dan yield untuk tesis Infrastruktur."),
 ("Kalimat presentasi", "\"Ini data mentahnya. Yang menarik bukan angkanya, tetapi bagaimana angka ini menggerakkan aturan, misalnya emas 3.746 yang membuat satu tesis kami gugur.\""),
])
h3("D. Skor sektor per skenario (grafik rentang)")
img("dash_sektor.png", "Prediksi sektor per skenario.", "70%")
vis([
 ("Ditampilkan", "Untuk 11 sektor: garis rentang skor dari skenario terburuk sampai terbaik, <b>titik</b> = skor di skenario aktif (Base), <b>belah ketupat</b> = ekspektasi probabilistik, label status di kanan (Bullish Moderat, Netral, Bearish) dan peran (Inti, Satelit, Kontrarian). Nama tebal = sektor inti."),
 ("Cara membaca", "Makin ke kanan makin baik. <b>Garis pendek di kanan nol</b> berarti sektor itu bagus di skenario apa pun (robust). <b>Garis panjang melewati nol</b> berarti hasilnya sangat bergantung skenario (taruhan). Belah ketupat di kanan titik berarti skenario lain secara rata-rata lebih menguntungkan daripada skenario aktif."),
 ("Rumus skor", "R-SEK-07: <b>skor outlook = makro-geo + valuasi sektor + tema × 2 + sentimen + aliran asing + rotasi siklus</b>. Makro-geo sendiri = Σ sensitivitas sektor × arah 12 faktor (minyak, USD, suku bunga, inflasi, emas, logam, risk-off, belanja pemerintah, daya beli, tarif, …), dihitung terpisah untuk ketiga skenario."),
 ("Status", "≥ 12 Bullish Kuat, 7–11 Bullish Moderat, 2–6 Netral, &lt; 2 Bearish (R-SEK-12a..d)."),
 ("Ekspektasi", "R-ROB-01: 0,5 × Base + 0,25 × Bull + 0,25 × Bear. Contoh Barang Baku: 0,5×11 + 0,25×17 + 0,25×4 = 10,75."),
 ("Peran", "<b>Inti</b> (R-ROB-04): bullish di skenario aktif dan robust (Base ≥ 7, Bull ≥ 7, Bear ≥ 2). <b>Satelit</b> (R-ROB-05): asimetri positif (upside ≥ 1,5 × downside dan ekspektasi ≥ 2) plus peluang kontrarian. <b>Kontrarian</b> (R-GEO-09): ada pergerakan makro aktif yang menciptakan diskon harga di sektor itu."),
 ("Kalimat presentasi", "\"Kami tidak hanya memprediksi satu masa depan. Setiap sektor dinilai di tiga skenario. Barang Baku dan Kesehatan menjadi sektor inti karena tetap positif bahkan di skenario terburuk. Keuangan bearish sekarang, tetapi upside-nya 19 poin dibanding downside 10, jadi kami menjadikannya satelit, yaitu taruhan kecil dengan potensi besar.\""),
])
SKT = [("Barang Baku", 4, 11, 17, "10,75", "Bullish Moderat · <b>Inti</b>"), ("Kesehatan", 6, 8, 8, "7,5", "Bullish Moderat · <b>Inti</b>"),
       ("Infrastruktur", -1, 6, 20, "7,75", "Netral · Satelit · Kontrarian"), ("Konsumen Primer", 1, 6, 12, "6,25", "Netral · Kontrarian"),
       ("Perindustrian", -1, 4, 14, "5,25", "Netral (asimetri positif)"), ("Energi", 4, 6, 2, "4,5", "Netral"),
       ("Keuangan", -10, 0, 19, "2,25", "Bearish · Satelit · Kontrarian"), ("Properti", -9, -2, 14, "0,25", "Bearish"),
       ("Teknologi", -13, -4, 16, "−1,25", "Bearish"), ("Transportasi", -12, -4, 11, "−2,25", "Bearish"), ("Konsumen Non-Primer", -16, -6, 13, "−3,75", "Bearish")]
table(["Sektor", "Bear", "Base (aktif)", "Bull", "Ekspektasi", "Status · peran"], [[a, str(b), str(c), str(d), e, f] for a, b, c, d, e, f in SKT],
      ["24%", "10%", "14%", "10%", "13%", "29%"])
note("Energi adalah contoh bagus untuk menunjukkan bahwa sistem benar-benar menalar: di skenario Bull, ketegangan geopolitik mereda dan harga "
     "minyak turun, sehingga skor Energi justru lebih rendah (2) daripada di Base (6). Sektor tidak selalu naik bersama pasar.", "dosen")
h3("E. Top-3 emiten per sektor pilihan")
vis([
 ("Ditampilkan", "Untuk sektor inti dan satelit, tiga sampai empat emiten teratas menurut skor adaptif regime. Bintang ★ = top pick sistem pakar."),
 ("Cara membaca", "Emiten tanpa bintang tetap yang terbaik di sektornya, tetapi belum lolos syarat top pick. Contoh: BBCA (23,5) teratas di Keuangan, tetapi di bawah ambang krisis 24,7."),
 ("Dari mana", "R-ADP-02 (skor adaptif) dan R-ADP-03 (top pick adaptif: skor ≥ ambang regime, ekspektasi sektor ≥ 2, penalti risiko ≥ −1)."),
 ("Kalimat presentasi", "\"Di sektor inti, Barang Baku punya tiga top pick (ANTM, TINS, NCKL) dan Kesehatan satu (MIKA). Di sektor satelit belum ada yang lolos ambang. Saat krisis, sistem sengaja selektif.\""),
])
h3("F. Analis biasa vs sistem pakar")
img("dash_pick.png", "Perbandingan skor statis dan skor adaptif.", "72%")
vis([
 ("Ditampilkan", "Tabel emiten dengan skor statis, skor adaptif, apakah dipilih analis biasa, apakah dipilih sistem pakar, dan ukuran posisi maksimum (% modal)."),
 ("Analis biasa", "Skor statis = jumlah 8 pilar dengan bobot sama (R-EMT-03). Top pick statis: skor ≥ 21 <i>dan</i> sektornya bullish di skenario aktif (R-EMT-04). Hasilnya 4 emiten: ANTM, MIKA, NCKL, TINS."),
 ("Sistem pakar", "Skor adaptif = Σ bobot regime × 9 pilar (R-ADP-02), dengan kontribusi sektor memakai nilai ekspektasi lintas skenario dan tambahan pilar smart money. Hasilnya 7 emiten: AADI, ANTM, JPFA, LSIP, MIKA, NCKL, TINS. Tiga tambahan berasal dari sektor yang netral di Base tetapi berekspektasi positif."),
 ("Contoh ANTM", "Statis: 9 + 3 + 7 + 5 + (−1) + 2 + 0 + 2 = <b>27</b>. Adaptif: 1,5×9 + 1,5×3 + 0,5×7 + 1×5 + 0,5×(−1) + 1×4 + 1,5×0 + 1×2 + 1,5×2 = <b>35</b>."),
 ("Posisi maks", "R-POS-01: risiko per transaksi regime ÷ (2 × ATR%) × 100. ANTM: 0,5% ÷ (2 × 3,5%) × 100 = 7,14% modal."),
 ("Kalimat presentasi", "\"Analis biasa memberi bobot sama ke semua pilar. Sistem pakar menyesuaikan bobot dengan regime. Hasilnya, sistem menemukan tiga peluang tambahan yang dilewatkan analis biasa: AADI, JPFA, dan LSIP.\""),
])
h3("G. Bedah satu emiten")
img("dash_emiten.png", "Bedah emiten ANTM.", "60%")
vis([
 ("Ditampilkan", "Batang kontribusi delapan pilar, lencana skor statis dan adaptif, tabel harga (harga, stop loss, take profit, nilai wajar, upside, posisi maks), serta semua kelas yang disimpulkan reasoner."),
 ("Cara membaca", "Batang biru = kontribusi positif, merah = negatif. Lencana hijau = kelas positif (FundamentalKuat, AkumulasiBandar, Undervalued), merah = peringatan (RisikoKonsentrasiTema, RisikoOutflowPasif), abu-abu = keterangan."),
 ("Rumus harga", "Stop loss = harga − 2 × ATR, take profit = harga + 3 × ATR (risk–reward 1 : 1,5). ANTM: 2.900 − 203 = 2.697; 2.900 + 304,5 = 3.204,5. Nilai wajar 5.220 dari metode valuasi, upside 80%."),
 ("Kalimat presentasi", "\"Setiap rekomendasi bisa dibedah. ANTM kuat di fundamental dan teknikal, sentimennya sedikit negatif, dan reasoner menyimpulkan 28 kelas, termasuk peringatan bahwa ANTM dan NCKL sama-sama bergantung pada nikel.\""),
])
h3("H. Tesis investasi dan kill switch")
img("dash_tesis.png", "Status tesis investasi.", "68%")
vis([
 ("Ditampilkan", "Setiap tesis: indikator kunci, nilai saat ini, batas gugur, dan status (Valid, Rapuh, Gugur, Terpicu)."),
 ("Aturan", "R-TES-01/02: indikator melewati batas → <b>Gugur</b>. R-TES-03: di dalam rentang → <b>Valid</b>. R-TES-06/07: jarak ke batas &lt; 10% → <b>Rapuh</b>. R-TES-08: tesis kontrarian, indikator melewati ambang pemicu → <b>Terpicu</b>. R-TES-09/10: sektor dengan tesis gugur atau rapuh dipantau ketat."),
 ("Kalimat presentasi", "\"Pakar yang baik tahu kapan dia salah. Setiap tesis punya kill switch. Tesis emas sudah gugur karena emas 3.745 di bawah batas 3.800, jadi sistem otomatis menandai Barang Baku untuk dipantau ketat walaupun sektornya masih inti.\""),
])
table(["Tesis", "Indikator", "Nilai", "Batas", "Status"], [
 ["Emas & nikel menopang Barang Baku", "Emas", "3.745,56", "gugur bila &lt; 3.800", "<b>Gugur</b>, rapuh"],
 ["Premi geopolitik minyak (Energi)", "Brent", "91,95", "gugur bila &lt; 75", "Valid (jarak 18%)"],
 ["Kesehatan defensif", "USD/IDR", "18.232", "gugur bila &gt; 19.500", "Valid, rapuh (jarak 7%)"],
 ["Big banks pasca-kapitulasi (kontrarian)", "CDS 5Y", "99,6", "gugur &gt; 150; terpicu &lt; 85", "Valid, belum terpicu"],
 ["Infrastruktur digital (kontrarian)", "Yield SBN 10Y", "7,668", "gugur &gt; 8; terpicu &lt; 6,75", "Valid, rapuh"],
 ["Konsumen primer (MBG & CPO)", "Inflasi", "3,23", "gugur bila &gt; 5", "Valid"],
], ["34%", "15%", "12%", "21%", "18%"])
h3("I. Rantai sebab-akibat geopolitik")
vis([
 ("Ditampilkan", "Jalur dari peristiwa aktif → pergerakan pasar → pergerakan lanjutan → sektor yang diuntungkan atau dirugikan."),
 ("Dari mana", "Object property <code>memicuPergerakan</code>, <code>menyebabkan</code>, dan <code>menguntungkanSektor</code>/<code>merugikanSektor</code>, serta aturan R-GEO. Saat ini ada 31 peristiwa aktif dan 44 pergerakan aktif."),
 ("Contoh", "Penutupan Selat Hormuz → premi risiko Timur Tengah naik → harga minyak naik → substitusi ke batu bara → <b>Energi diuntungkan</b> (dan AADI ikut diuntungkan)."),
 ("Kalimat presentasi", "\"Berita tidak hanya diberi skor positif atau negatif. Sistem menelusuri rantai sebab-akibatnya sampai ke sektor dan emiten.\""),
])
h3("J. Simulasi what-if dan konsol")
p("Dijelaskan di Bab 5.4 dan 5.5. Inti kalimat presentasinya: <i>\"Ini bukti bahwa sistemnya benar-benar menalar, bukan menampilkan "
  "hasil yang sudah dihitung. Saya ubah datanya, aturan menalar ulang di server, lalu kesimpulannya berubah sesuai logika pakar.\"</i>")
h2("5.4", "Simulasi what-if")
p("Tombol simulasi mengirim SPARQL Update ke <code>/saham</code>, menunggu aturan menalar ulang, lalu menampilkan tabel "
  "<b>sebelum vs sesudah</b>. Dataset Pellet tidak pernah diubah, sehingga <b>Reset</b> selalu bisa mengembalikan nilai asli.")
img("dash_whatif.png", "Hasil simulasi \"CDS membaik ke 75 bps\": perintah SPARQL Update yang dikirim (atas) dan keluaran KB yang berubah (bawah, ditandai ◀).", "78%")
table(["Tombol", "Yang diubah", "Hasil yang diharapkan"], [
    ["Skenario bull aktif", "statusAktif skenario", "8 sektor menjadi bullish kuat"],
    ["Skenario bear aktif", "statusAktif skenario", "tidak ada sektor bullish; Barang Baku, Energi, Kesehatan bertahan netral"],
    ["CDS membaik ke 75 bps", "CDS dan tren CDS/rupiah", "skor stres 11 → 10; Tesis_Keuangan_Kontrarian terpicu"],
    ["Emas naik ke US$4.000", "harga emas", "tesis Barang Baku kembali valid"],
    ["Brent jatuh ke US$70", "harga Brent", "tesis Energi gugur (batas US$75)"],
    ["Kapitulasi IHSG", "drawdown −45%, crash −10,5%", "kapitulasi aktif; 5 kandidat akumulasi bertahap muncul (BBCA, BMRI, CPIN, MIKA, UNTR)"],
], ["26%", "28%", "46%"])
h2("5.5", "Konsol SPARQL")
img("dash_konsol.png", "Konsol SPARQL di dashboard: pilih contoh, ubah, jalankan. Sama dengan menu query di UI Fuseki.", "88%")
h2("5.6", "Skenario demo 7 menit di depan dosen")
DEMO = [
    ("0:00", "Buka dashboard. Jelaskan indikator hijau: setiap angka diambil langsung dari KB lewat SPARQL ke Fuseki."),
    ("0:45", "Kartu regime: pasar Krisis Likuiditas (stres 11/12); karena itu bobot fundamental dinaikkan ×1,5."),
    ("1:30", "Prediksi sektor: Barang Baku dan Kesehatan adalah sektor inti karena tidak pernah bearish di skenario mana pun."),
    ("2:30", "Analis biasa vs pakar: pakar menambah LSIP, AADI, JPFA. Klik ANTM untuk menunjukkan delapan pilar dan kelas inferensinya."),
    ("3:30", "Tesis: emas di bawah US$3.800 sehingga tesis emas gugur (kill switch nyata dari data 19 November)."),
    ("4:15", "What-if: klik \"Kapitulasi IHSG\" → muncul 5 kandidat akumulasi beserta tabel sebelum/sesudah. Klik Reset."),
    ("5:15", "Klik \"lihat SPARQL\" di satu panel: tunjukkan query-nya, lalu jalankan contoh di konsol."),
    ("6:00", "Pindah ke Protégé: klik ANTM, tunjukkan baris kuning, lalu tombol ? (explanation)."),
]
table(["Menit", "Yang ditunjukkan"], [[a, b] for a, b in DEMO], ["12%", "88%"])
h2("5.7", "Menambah panel sendiri")
p("Semua query dashboard ada di objek <code>Q</code> dalam <code>dashboard/index.html</code>. Untuk menambah panel: tulis query "
  "SPARQL-nya (uji dulu di konsol), tambahkan ke objek <code>Q</code>, buat fungsi <code>loadXxx()</code> yang memanggil "
  "<code>sparql(Q.xxx)</code> dan mengisi elemen HTML, lalu daftarkan fungsi itu di <code>refreshAll()</code>.")

# =================================================================== BAGIAN VI
bab("VI", "Pengujian dan lampiran", "Bukti bahwa KB menjawab semua pertanyaan, penanganan error, glosarium, dan referensi.")
h2("6.1", "Pengujian")
p("<code>python3 tools/uji_kb.py --whatif</code> menjalankan <b>103 soal</b> (98 statis + 5 what-if) dan menulis jawabannya ke "
  "<code>output/HASIL_UJI_KB.md</code>. Soal mencakup 17 modul: struktur KB, kebenaran aturan, pengetahuan dasar, fundamental, "
  "teknikal, bandarmology, sentimen, geopolitik, indeks, prediksi sektor, rekomendasi emiten, meta-penalaran, stakeholder, kualitas "
  "data, dan what-if. Panduan pengujian rinci beserta 20 tanya-jawab dosen tersedia sebagai dokumen terpisah.")
table(["Jenis uji", "Cara", "Hasil"], [
    ["Konsistensi", "OWLAPI + Pellet", "konsisten"],
    ["Kebenaran aturan", "satu nilai per pilar (A05), penjumlahan skor (A06), emiten uji fiktif (A07)", "67/67 emiten benar"],
    ["Competency questions", "SPARQL ke ontologi hasil inferensi", "12/12 CQ + 86 soal lain"],
    ["What-if", "ubah data → Pellet ulang", "5/5 sesuai logika pakar"],
    ["Dua mesin", "Fuseki (Jena) vs Pellet", "regime, stres, 7 top pick identik"],
    ["Ontologi eksternal", "alignment + Pellet", "konsisten; 5 bank sentral → fibo:CentralBank"],
], ["24%", "48%", "28%"])
h2("6.2", "Troubleshooting")
table(["Gejala", "Penyebab", "Solusi"], [
    ["<code>fuseki-server tidak ditemukan / tidak executable</code>", "folder salah atau izin belum diberikan", "cek path folder; jalankan <code>chmod +x</code> dan <code>/usr/bin/xattr -dr com.apple.quarantine</code> (Bab 4.2)"],
    ["<code>UnsupportedClassVersionError</code>", "Java terlalu lama", "pakai JDK 21+; <code>start_fuseki.sh</code> otomatis memilih JDK 25 bila ada"],
    ["<code>Address already in use</code> / port 3030 terpakai", "Fuseki lama masih jalan", "<code>lsof -i :3030</code> lalu <code>kill &lt;PID&gt;</code>"],
    ["Dashboard: indikator merah / error 502", "Fuseki belum menyala atau masih memuat", "nyalakan Fuseki dulu; tunggu \"Started\"; muat ulang halaman"],
    ["Port 8080 terpakai", "program lain memakai 8080", "<code>python3 dashboard/server.py --port 8090</code>"],
    ["Query error <code>Unresolved prefixed name</code>", "PREFIX lupa ditulis", "tambahkan baris <code>PREFIX ex: &lt;…&gt;</code> di atas query"],
    ["What-if tidak mengubah apa pun", "tipe data salah, atau mengirim ke /saham-pellet", "pakai <code>xsd:double</code> untuk desimal, kirim ke <code>/saham/update</code>"],
    ["Protégé: tidak ada baris kuning", "reasoner belum jalan atau memakai HermiT", "<i>Reasoner › Pellet › Start reasoner</i>"],
    ["Protégé: alignment gagal impor", "catalog-v001.xml tidak satu folder", "buka file alignment dari folder <code>output/</code>"],
    ["Tahap 6/9/11 run_all GAGAL (playwright)", "modul Node tidak terlihat", "<code>export NODE_PATH=\"$PWD/node_modules\"</code> sebelum <code>run_all.py</code>"],
], ["30%", "30%", "40%"])
h2("6.3", "Glosarium")
GLOS = [("ABox", "bagian ontologi berisi fakta tentang individu"), ("Aksioma", "satu pernyataan logis di ontologi"),
        ("Annotation property", "keterangan untuk manusia, tidak dinalar (label, rumus)"), ("Asserted", "fakta yang dimasukkan langsung (putih di Protégé)"),
        ("Built-in (swrlb)", "fungsi bawaan SWRL: perbandingan dan aritmetika"), ("Competency question", "pertanyaan yang wajib bisa dijawab KB"),
        ("Data property", "properti bernilai angka/teks"), ("Dataset (Fuseki)", "kumpulan graf yang dilayani dengan satu nama"),
        ("DL Query", "tab Protégé untuk bertanya dengan ekspresi kelas OWL"), ("Endpoint", "alamat HTTP untuk query atau update"),
        ("FIBO", "Financial Industry Business Ontology, ontologi standar industri keuangan"), ("Individu", "anggota nyata suatu kelas"),
        ("Inferred", "fakta hasil penalaran (kuning di Protégé)"), ("IRI", "alamat unik global untuk setiap nama"),
        ("Kill switch", "ambang yang membuat tesis investasi gugur"), ("Konsisten", "tidak mengandung kontradiksi logika"),
        ("Object property", "properti yang menghubungkan dua individu"), ("Ontologi", "deskripsi formal konsep dan hubungannya"),
        ("OWA", "Open World Assumption: yang tidak diketahui bukan berarti salah"), ("OWL", "Web Ontology Language"),
        ("owl:imports", "memasukkan isi ontologi lain"), ("Prefix", "singkatan namespace, mis. ex:"),
        ("RDF", "model data berupa triple"), ("Reasoner", "program yang menarik kesimpulan dari ontologi"),
        ("Regime", "kondisi pasar (Krisis, Risk-off, Netral, Risk-on) yang mengubah bobot analisis"), ("SKOS", "kosakata W3C untuk memetakan konsep"),
        ("SPARQL", "bahasa query untuk RDF"), ("SPARQL Update", "perintah INSERT/DELETE untuk mengubah data"),
        ("SQWRL", "perluasan SWRL untuk query"), ("SWRL", "bahasa aturan JIKA–MAKA untuk OWL"),
        ("TBox", "bagian ontologi berisi kosakata dan skema"), ("Triple", "fakta subjek–predikat–objek"),
        ("Turtle", "format penulisan RDF yang ringkas (.ttl)")]
table(["Istilah", "Arti"], [[f"<b>{a}</b>", b] for a, b in GLOS], ["28%", "72%"])
h2("6.4", "Referensi")
ul(["Noy, N. F. &amp; McGuinness, D. L. (2001). <i>Ontology Development 101: A Guide to Creating Your First Ontology</i>. Stanford KSL.",
    "W3C. <i>OWL 2 Web Ontology Language Primer</i>; <i>RDF 1.1 Primer</i>; <i>SPARQL 1.1 Query Language</i>; <i>SPARQL 1.1 Update</i>.",
    "W3C Member Submission (2004). <i>SWRL: A Semantic Web Rule Language Combining OWL and RuleML</i>.",
    "Apache Jena. <i>Fuseki documentation</i> dan <i>Download</i>: https://jena.apache.org/documentation/fuseki2/ · https://jena.apache.org/download/",
    "EDM Council. <i>Financial Industry Business Ontology (FIBO)</i>: https://github.com/edmcouncil/fibo",
    "Stanford Center for Biomedical Informatics Research. <i>Protégé 5 User Guide</i>.",
    "Sirin, E. et al. (2007). Pellet: A practical OWL-DL reasoner. <i>Journal of Web Semantics</i>, 5(2).",
    "Kepmenaker No. 299 Tahun 2020 tentang SKKNI Bidang Data Science (alur unit kompetensi proyek)."])

# =================================================================== BAGIAN VII
import qa as QAM  # noqa: E402
bab("VII", "100 pertanyaan dosen dan jawabannya", "Dikelompokkan per topik. Jawaban sengaja ringkas (2–4 kalimat) agar mudah diucapkan; angka mengacu pada data 19 November 2026.")
n = 0
for kat, items in QAM.QA:
    TOC.append((2, "", kat)); w(f'<h2>{E(kat)}</h2>')
    for q, a in items:
        n += 1
        w(f'<div class="qa"><div class="q"><span class="qn">{n}</span>{E(q)}</div><div class="a">{E(a)}</div></div>')

# =================================================================== TOC + RENDER
toc = "".join(f'<div class="l{lv}"><span>{("Bagian " + no + ". ") if lv == 1 else (no + "  ")}{E(t)}</span></div>' for lv, no, t in TOC)
html = f"<!DOCTYPE html><html lang='id'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(H).replace('@@TOC@@', toc)}</body></html>"
tmp = tempfile.mkdtemp()
hp = os.path.join(tmp, "buku.html"); open(hp, "w", encoding="utf-8").write(html)
footer = '<div style="font-size:7.5pt;width:100%;text-align:center;color:#888">Buku Panduan Lengkap SahamExpertKB · Kelompok 9 · <span class="pageNumber"></span>/<span class="totalPages"></span></div>'
js = os.path.join(tmp, "p.js")
open(js, "w").write(f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}',{{waitUntil:'load'}});await p.pdf({{path:{json.dumps(DST)},format:'A4',printBackground:true,displayHeaderFooter:true,
headerTemplate:'<span></span>',footerTemplate:{json.dumps(footer)},margin:{{top:'16mm',bottom:'18mm',left:'15mm',right:'15mm'}}}});await b.close();}})();""")
subprocess.run(["node", js], check=True)
print("PDF:", DST)
