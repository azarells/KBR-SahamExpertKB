# -*- coding: utf-8 -*-
"""Diagram SVG untuk Buku Panduan SahamExpertKB (digambar dengan kode, tanpa pustaka luar)."""
from html import escape as E

INK, MUTED, LINE = "#1d2433", "#5d6672", "#9aa3ae"
BLUE, BLUE_S = "#2f5bd3", "#e8eefc"
GREEN, GREEN_S = "#1f8a5b", "#e3f4ec"
ORANGE, ORANGE_S = "#b26a00", "#fbf0dc"
RED, RED_S = "#c23b3b", "#fae5e5"
PURPLE, PURPLE_S = "#7a3ea8", "#f1e8f8"
GREY_S = "#f1f3f6"


def svg(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{E(label)}" '
            f'font-family="DejaVu Sans, Arial, sans-serif" xmlns="http://www.w3.org/2000/svg">'
            f'<defs>'
            f'<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{LINE}"/></marker>'
            f'<marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker>'
            f'<marker id="ahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{GREEN}"/></marker>'
            f'</defs>{body}</svg>')


def text(x, y, s, size=12, fill=INK, weight=400, anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" xml:space="preserve"{st}>{E(s)}</text>'


def box(x, y, w, h, title, lines=(), fill=BLUE_S, stroke=BLUE, tsize=13, lsize=11, rx=8, center=True, tcolor=INK):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
    n = len(lines)
    total = tsize + n * (lsize + 4)
    cy = y + (h - total) / 2 + tsize - 2 if center else y + tsize + 8
    cx = x + w / 2 if center else x + 10
    anc = "middle" if center else "start"
    out += text(cx, cy, title, tsize, tcolor, 700, anc)
    for i, l in enumerate(lines):
        out += text(cx, cy + (i + 1) * (lsize + 4) + 2, l, lsize, MUTED, 400, anc)
    return out


def arrow(x1, y1, x2, y2, label=None, color=LINE, dash=False, lx=None, ly=None, lsize=10.5, marker="ah", width=1.4):
    d = ' stroke-dasharray="5 4"' if dash else ""
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d} marker-end="url(#{marker})"/>'
    if label:
        out += text(lx if lx is not None else (x1 + x2) / 2 + 6, ly if ly is not None else (y1 + y2) / 2 - 5, label, lsize, MUTED)
    return out


def path(d, color=LINE, dash=False, marker="ah", width=1.4):
    ds = ' stroke-dasharray="5 4"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{ds} marker-end="url(#{marker})"/>'


def title(x, y, s):
    return text(x, y, s, 14.5, INK, 700)


# =================================================================== D1 sistem pakar klasik
def d_sistem_pakar():
    b = title(20, 26, "Sistem berbasis pengetahuan memisahkan pengetahuan dari mesin penalaran")
    b += box(20, 60, 170, 70, "Pakar saham", ["analis, buku, riset"], GREY_S, LINE)
    b += box(20, 170, 170, 70, "Knowledge engineer", ["Kelompok 9"], GREY_S, LINE)
    b += arrow(105, 130, 105, 170, "wawancara, literatur", lx=112)
    b += box(250, 60, 230, 180, "Knowledge base", ["", "Ontologi OWL", "kelas · properti · individu", "", "303 aturan SWRL", "JIKA … MAKA …"], BLUE_S, BLUE, 14)
    b += arrow(190, 205, 250, 180, "menyusun", lx=196, ly=228)
    b += box(540, 60, 200, 80, "Mesin inferensi", ["reasoner Pellet / Jena"], ORANGE_S, ORANGE)
    b += box(540, 165, 200, 75, "Antarmuka", ["Protégé · Fuseki · dashboard"], GREEN_S, GREEN)
    b += arrow(480, 100, 540, 100, "membaca", lx=486, ly=92)
    b += arrow(640, 140, 640, 165)
    b += box(540, 270, 200, 50, "Pengguna", ["investor, sekuritas, dosen"], GREY_S, LINE, 12, 10.5)
    b += arrow(640, 240, 640, 270)
    b += text(250, 275, "Ganti data atau tambah aturan → jawaban berubah,", 11, MUTED)
    b += text(250, 291, "tanpa menulis ulang program. Itulah bedanya dengan", 11, MUTED)
    b += text(250, 307, "program biasa yang logikanya tertanam di kode.", 11, MUTED)
    return svg(760, 335, b, "Arsitektur sistem berbasis pengetahuan")


# =================================================================== D2 ontologi mini
def d_ontologi_mini():
    b = title(20, 26, "Ontologi = kelas (kotak), individu (belah ketupat), dan hubungan (panah)")
    # kelas
    b += box(300, 50, 160, 40, "owl:Thing", [], GREY_S, LINE, 12)
    b += box(90, 130, 170, 44, "EntitasPasarModal", [], BLUE_S, BLUE, 12)
    b += box(510, 130, 170, 44, "KategoriInferensi", [], ORANGE_S, ORANGE, 12)
    b += path("M380 90 L380 110 L175 110 L175 130")
    b += path("M380 90 L380 110 L595 110 L595 130")
    b += box(30, 220, 120, 40, "Emiten", [], BLUE_S, BLUE, 12)
    b += box(190, 220, 120, 40, "Sektor", [], BLUE_S, BLUE, 12)
    b += path("M175 174 L175 196 L90 196 L90 220")
    b += path("M175 174 L175 196 L250 196 L250 220")
    b += box(470, 220, 250, 40, "KandidatTopPickAdaptif", [], ORANGE_S, ORANGE, 12)
    b += arrow(595, 174, 595, 220)
    b += text(186, 205, "subClassOf", 10, MUTED)
    b += text(602, 203, "subClassOf", 10, MUTED)
    # individu
    def diamond(cx, cy, label, c=PURPLE):
        return (f'<path d="M{cx} {cy-16} L{cx+16} {cy} L{cx} {cy+16} L{cx-16} {cy}z" fill="{PURPLE_S}" stroke="{c}" stroke-width="1.3"/>'
                + text(cx, cy + 34, label, 12, INK, 700, "middle"))
    b += diamond(90, 330, "ANTM")
    b += diamond(250, 330, "Sektor_BarangBaku")
    b += arrow(90, 314, 90, 262, None, PURPLE, dash=True)
    b += text(96, 292, "rdf:type", 10, PURPLE)
    b += arrow(250, 314, 250, 262, None, PURPLE, dash=True)
    b += text(256, 292, "rdf:type", 10, PURPLE)
    b += arrow(108, 330, 232, 330, None, BLUE, marker="ahb")
    b += text(170, 322, "termasukSektor", 10.5, BLUE, 600, "middle")
    b += f'<rect x="20" y="380" width="250" height="52" rx="6" fill="#fff" stroke="{LINE}" stroke-dasharray="3 3"/>'
    b += text(30, 400, "Data property ANTM:", 11, INK, 700)
    b += text(30, 420, "roe = 18 · der = 0,3 · hargaPenutupan = 2900", 10.5, MUTED)
    b += path("M106 330 C 330 400, 420 300, 470 245", ORANGE, dash=True, marker="ah")
    b += text(330, 360, "disimpulkan reasoner", 10.5, ORANGE, 600)
    b += text(330, 375, "(bukan diketik)", 10.5, ORANGE)
    b += text(470, 300, "Kotak biru = TBox (kosakata/skema)", 11, MUTED)
    b += text(470, 318, "Belah ketupat = ABox (fakta individu)", 11, MUTED)
    b += text(470, 336, "Panah putus-putus oranye = hasil penalaran", 11, MUTED)
    return svg(760, 445, b, "Contoh ontologi mini")


# =================================================================== D3 triple
def d_triple():
    b = title(20, 26, "Setiap fakta adalah satu triple: subjek → predikat → objek")
    rows = [("ex:ANTM", "ex:termasukSektor", "ex:Sektor_BarangBaku", "objek = individu lain (object property)"),
            ("ex:ANTM", "ex:roe", '"18.0"^^xsd:double', "objek = nilai/literal (data property)"),
            ("ex:ANTM", "rdf:type", "ex:Emiten", "objek = kelas (keanggotaan)"),
            ("ex:ANTM", "ex:skorTotalEmiten", "27", "triple ini DITAMBAHKAN reasoner")]
    y = 52
    for i, (s, p, o, note) in enumerate(rows):
        hl = i == 3
        b += box(20, y, 120, 34, s, [], PURPLE_S, PURPLE, 11.5)
        b += arrow(140, y + 17, 300, y + 17, None, ORANGE if hl else BLUE, marker="ahb" if not hl else "ah")
        b += text(220, y + 11, p, 10.5, ORANGE if hl else BLUE, 600, "middle")
        b += box(300, y, 190, 34, o, [], ORANGE_S if hl else GREY_S, ORANGE if hl else LINE, 11.5)
        b += text(505, y + 21, note, 10.5, ORANGE if hl else MUTED, 600 if hl else 400)
        y += 50
    b += text(20, y + 14, "Semua triple bersama-sama membentuk graf. Di file .owl (RDF/XML) atau .ttl (Turtle), isinya hanya daftar triple seperti ini.", 11, MUTED)
    return svg(760, y + 28, b, "Triple RDF")


# =================================================================== D4 reasoner
def d_reasoner():
    b = title(20, 26, "Reasoner membaca fakta + aturan, lalu menambahkan fakta baru")
    b += box(20, 55, 210, 130, "Masukan (asserted)", ["fakta dari CSV:", "roe 18, der 0,3, npm 6,", "pertumbuhan EPS 48, …", "", "kelas & hierarki (TBox)"], GREY_S, LINE, 13, 10.5)
    b += box(20, 200, 210, 60, "303 aturan SWRL", ["R-FUND-01: ROE ≥ 15 → poin 2", ""], BLUE_S, BLUE, 12.5, 10.5)
    b += box(290, 105, 170, 110, "Reasoner Pellet", ["1. cek konsistensi", "2. klasifikasi kelas", "3. jalankan aturan", "4. realisasi individu"], ORANGE_S, ORANGE, 13, 10.5)
    b += arrow(230, 120, 290, 140)
    b += arrow(230, 230, 290, 190)
    b += box(520, 55, 220, 205, "Keluaran (inferred)", ["poinROE 2, poinSolvabilitas 2", "skorFundamental 9", "skorTotalEmiten 27", "skorAdaptifRegime 35,0", "", "FundamentalKuat", "KandidatTopPickAdaptif", "", "→ tampil KUNING di Protégé"], GREEN_S, GREEN, 13, 10.5)
    b += arrow(460, 160, 520, 160, None, GREEN, marker="ahg")
    b += text(20, 290, "Putih di Protégé = asserted (diketik/diimpor). Kuning = inferred (hasil penalaran). Fakta inferred tidak disimpan di", 11, MUTED)
    b += text(20, 306, "SahamExpertKB_v2.owl, melainkan dihitung ulang setiap reasoner dijalankan; versi yang sudah dibekukan ada di *_inferred.owl.", 11, MUTED)
    return svg(760, 320, b, "Cara kerja reasoner")


# =================================================================== D5 anatomi SWRL
def d_swrl():
    b = title(20, 26, "Anatomi satu aturan SWRL (R-FUND-01a)")
    b += f'<rect x="20" y="48" width="720" height="54" rx="8" fill="#0f172a"/>'
    b += text(36, 72, "Emiten(?e) ^ roe(?e, ?v) ^ swrlb:greaterThanOrEqual(?v, 15.0)", 13.5, "#d6e2ff", 600)
    b += text(36, 92, "    -> poinROE(?e, 2)", 13.5, "#9ef0c4", 600)
    def num(cx, cy, n, c):
        return f'<circle cx="{cx}" cy="{cy}" r="9" fill="{c}"/>' + text(cx, cy + 4, str(n), 10.5, "#fff", 700, "middle")
    b += num(76, 114, 1, BLUE) + num(186, 114, 2, BLUE) + num(388, 114, 3, ORANGE) + num(222, 87, 4, GREEN)
    rows = [(1, "Emiten(?e)", "atom kelas: ?e harus anggota kelas Emiten", BLUE),
            (2, "roe(?e, ?v)", "atom properti: ambil nilai ROE milik ?e ke variabel ?v", BLUE),
            (3, "swrlb:greaterThanOrEqual(?v, 15.0)", "built-in: bandingkan angka, ?v ≥ 15", ORANGE),
            (4, "poinROE(?e, 2)", "kepala aturan: fakta baru yang ditambahkan bila 1–3 terpenuhi", GREEN)]
    for i, (n, nmx, ket, c) in enumerate(rows):
        y = 150 + i * 38
        b += num(30, y - 4, n, c) + text(48, y, nmx, 12, c, 700) + text(48, y + 15, ket, 10.5, MUTED)
    b += text(20, 320, "Dibaca: JIKA ?e adalah Emiten DAN ROE-nya ≥ 15, MAKA beri ?e poinROE = 2. Tanda ^ = DAN, -> = MAKA.", 11.5, INK)
    b += text(20, 340, "SWRL tidak punya ELSE. Maka dibuat tiga aturan berpasangan yang intervalnya tidak tumpang tindih:", 11.5, INK)
    b += text(36, 358, "R-FUND-01a: ROE ≥ 15 → 2", 11, MUTED) + text(270, 358, "R-FUND-01b: 8 ≤ ROE < 15 → 1", 11, MUTED) + text(520, 358, "R-FUND-01c: ROE < 8 → 0", 11, MUTED)
    return svg(760, 372, b, "Anatomi aturan SWRL")


# =================================================================== D6 ontologi eksternal
def d_eksternal():
    b = title(20, 26, "Ontologi eksternal: memakai kosakata yang sudah disepakati orang lain")
    layers = [("Fondasi W3C (selalu dipakai)", "RDF · RDFS · OWL · XSD · SWRL", GREY_S, LINE),
              ("Kosakata umum", "Dublin Core (metadata) · SKOS (pemetaan konsep) · schema.org · FOAF · OWL-Time", GREEN_S, GREEN),
              ("Ontologi domain keuangan", "FIBO (Financial Industry Business Ontology, EDM Council)", ORANGE_S, ORANGE),
              ("Ontologi milik proyek", "SahamExpertKB: 298 kelas, 1.392 individu, 303 aturan", BLUE_S, BLUE)]
    y = 48
    for i, (t, s, f, c) in enumerate(layers):
        w = 720 - i * 60
        x = 20 + i * 30
        b += box(x, y, w, 46, t, [s], f, c, 12.5, 10.5)
        y += 54
    b += text(20, y + 16, "Tiga cara memakai ontologi eksternal:", 12.5, INK, 700)
    cards = [("1. Rujuk IRI saja", ["tulis IRI-nya di anotasi", "skos:closeMatch fibo:Issuer", "ringan, tanpa unduh"], GREY_S, LINE),
             ("2. owl:imports", ["salin seluruh isi ontologi", "lain ke dalam ontologi kita", "lengkap, tapi berat"], BLUE_S, BLUE),
             ("3. Alignment logis", ["subClassOf / equivalentClass", "BankSentral ⊑ fibo:CentralBank", "ikut dinalar reasoner"], ORANGE_S, ORANGE)]
    for i, (t, ls, f, c) in enumerate(cards):
        b += box(20 + i * 245, y + 28, 230, 92, t, ls, f, c, 12.5, 10.5)
    return svg(760, y + 132, b, "Lapisan ontologi eksternal")


# =================================================================== D7 Ontology 101
def d_od101():
    steps = [("1", "Domain & lingkup", "competency questions"), ("2", "Pakai ulang", "W3C, FIBO, SKOS"),
             ("3", "Daftar istilah", "emiten, ROE, regime…"), ("4", "Kelas & hierarki", "298 kelas"),
             ("5", "Properti", "65 object + 220 data"), ("6", "Facet/batasan", "domain, range, tipe"),
             ("7", "Buat individu", "1.392 dari CSV"), ("+", "Aturan & uji", "303 SWRL, 103 soal")]
    b = title(20, 26, "Metodologi Ontology Development 101 (Noy & McGuinness) + aturan")
    for i, (n, t, s) in enumerate(steps):
        col, row = i % 4, i // 4
        x, y = 20 + col * 185, 50 + row * 100
        f, c = (ORANGE_S, ORANGE) if n == "+" else (BLUE_S, BLUE)
        b += box(x, y, 165, 70, f"{n}. {t}" if n != "+" else t, [s], f, c, 11.5, 10.5)
        if col < 3:
            b += arrow(x + 165, y + 35, x + 185, y + 35)
    b += path("M682 120 L682 135 L102 135 L102 150")
    b += path("M682 220 L682 238 L380 238 L380 142 L472 142 L472 121", dash=True)
    b += text(20, 256, "Iteratif: soal uji yang gagal membawa kembali ke langkah 3–7, misalnya temuan celah aturan R-PAS-05 di proyek ini.", 11, MUTED)
    return svg(760, 268, b, "Ontology Development 101")


# =================================================================== D8 arsitektur berlapis
def d_arsitektur():
    b = title(20, 26, "Arsitektur SahamExpertKB dari sumber data sampai pengguna")
    col = [("SUMBER", 20, GREY_S, LINE, ["IDX (lap. keuangan)", "BI, BPS, The Fed", "berita Kontan/CNBC", "broker summary"]),
           ("DATA", 165, GREY_S, LINE, ["emiten.csv", "makro.csv", "berita.csv", "kondisi_pasar.csv"]),
           ("PEMBANGUN", 310, BLUE_S, BLUE, ["validasi_data.py", "sentiment_scorer", "build_ontology.py", "(owlready2)"]),
           ("PENGETAHUAN", 455, BLUE_S, BLUE, ["SahamExpertKB", "_v2.owl", "TBox + ABox", "+ 303 aturan SWRL"]),
           ("PENALARAN", 600, ORANGE_S, ORANGE, ["Pellet", "OWLAPI validasi", "_inferred.owl", "hasil_inferensi.json"])]
    for t, x, f, c, ls in col:
        b += text(x + 65, 52, t, 10.5, MUTED, 700, "middle")
        b += f'<rect x="{x}" y="60" width="130" height="120" rx="8" fill="{f}" stroke="{c}" stroke-width="1.3"/>'
        for i, l in enumerate(ls):
            b += text(x + 65, 84 + i * 22, l, 10, INK, 400, "middle")
    for x in (150, 295, 440, 585):
        b += arrow(x, 120, x + 15, 120)
    # lapisan bawah
    b += text(20, 214, "PENYAJIAN", 10.5, MUTED, 700)
    outs = [("Protégé", ["DL Query · SWRLTab", "explanation · what-if"], 20, GREEN_S, GREEN),
            ("Apache Jena Fuseki", ["/saham (aturan Jena, live)", "/saham-pellet (hasil jadi)"], 200, GREEN_S, GREEN),
            ("Dashboard web", ["dashboard/server.py", "SPARQL lewat HTTP"], 400, GREEN_S, GREEN),
            ("Laporan & uji", ["PDF, DOCX, slide", "uji_kb.py 103 soal"], 580, GREEN_S, GREEN)]
    for t, ls, x, f, c in outs:
        b += box(x, 225, 160, 64, t, ls, f, c, 12, 10)
    b += path("M665 180 L665 200 L100 200 L100 225")
    b += path("M665 200 L280 200 L280 225", marker="ah")
    b += path("M665 200 L660 200 L660 225", marker="ah")
    b += arrow(360, 257, 400, 257, None, GREEN, marker="ahg")
    b += text(362, 250, "HTTP", 9.5, GREEN)
    b += box(400, 310, 160, 40, "Pengguna", ["investor · sekuritas · dosen"], GREY_S, LINE, 11.5, 10)
    b += arrow(480, 289, 480, 310)
    b += text(20, 335, "Seluruh rantai atas dijalankan oleh satu perintah:", 11, MUTED)
    b += text(20, 351, "python3 run_all.py (12 tahap).", 11, INK, 700)
    return svg(760, 362, b, "Arsitektur SahamExpertKB")


# =================================================================== D9 pipeline run_all
def d_pipeline():
    st = [("1", "Validasi data CSV", "validasi_data.py"), ("2", "Skor sentimen", "sentiment_scorer.py"),
          ("3", "Ontologi + Pellet", "build_ontology.py"), ("4", "Ekspor inferensi", "OWLAPI → _inferred.owl"),
          ("5", "Cek konsistensi", "OWLAPI + Pellet"), ("6", "Laporan prediksi", "make_report.py → PDF"),
          ("7", "Aturan Jena", "swrl2jena.py → .rules"), ("8", "Data Fuseki", "angka → xsd:double"),
          ("9", "Dok. pengembangan", "make_blueprint.py"), ("10", "Uji 12 CQ", "tools/uji_cq.py"),
          ("11", "Panduan proyek", "tools/make_panduan.py"), ("12", "Uji KB 103 soal", "tools/uji_kb.py --whatif")]
    b = title(20, 26, "python3 run_all.py menjalankan 12 tahap berurutan")
    for i, (n, t, s) in enumerate(st):
        col, row = i % 4, i // 4
        x, y = 20 + col * 185, 48 + row * 82
        core = n in ("1", "3", "4", "5", "12")
        b += box(x, y, 165, 60, f"{n}. {t}", [s], ORANGE_S if core else BLUE_S, ORANGE if core else BLUE, 11.5, 10)
        if col < 3:
            b += arrow(x + 165, y + 30, x + 185, y + 30)
    b += path("M682 108 L682 119 L102 119 L102 130")
    b += path("M682 190 L682 201 L102 201 L102 212")
    b += text(20, 300, "Oranye = tahap inti (wajib OK). Biru = tahap pendukung; tahap 6, 9, 11 membuat PDF dan butuh pandoc + Playwright.", 11, MUTED)
    return svg(760, 312, b, "Pipeline run_all")


# =================================================================== D10 alur penalaran emiten
def d_alur_emiten():
    b = title(20, 26, "Alur penalaran satu emiten (contoh ANTM)")
    pil = [("Fundamental", "ROE, DER, NPM, EPS, CFO", "9"), ("Valuasi", "PER vs rata-rata 5 th", "3"), ("Teknikal", "MA, RSI, MACD, volume", "7"),
           ("Bandarmology", "broker, net asing", "5"), ("Sentimen", "berita", "−1"), ("Sektor", "outlook sektor", "2"),
           ("Risiko", "Altman Z, tata kelola", "0"), ("Likuiditas", "nilai transaksi", "2")]
    for i, (n, s, v) in enumerate(pil):
        y = 48 + i * 37
        b += box(20, y, 190, 31, n, [], BLUE_S, BLUE, 11.5)
        b += text(220, y + 20, s, 10, MUTED)
        b += f'<circle cx="370" cy="{y + 15}" r="13" fill="#fff" stroke="{BLUE}"/>' + text(370, y + 20, v, 11.5, INK, 700, "middle")
        b += path(f"M383 {y + 15} C 410 {y + 15}, 410 190, 440 190")
    b += box(440, 160, 140, 60, "Skor statis", ["jumlah = 27"], GREY_S, LINE, 12.5, 10.5)
    b += box(440, 250, 140, 66, "Regime pasar", ["Krisis Likuiditas", "stres 11/12"], ORANGE_S, ORANGE, 12, 10.5)
    b += box(610, 160, 135, 60, "Skor adaptif", ["bobot regime = 35,0"], ORANGE_S, ORANGE, 12.5, 10.5)
    b += arrow(580, 190, 610, 190)
    b += path("M580 283 L677 283 L677 220", ORANGE, marker="ah")
    b += text(590, 300, "fundamental ×1,5", 10, ORANGE)
    b += text(590, 313, "teknikal ×0,5", 10, ORANGE)
    b += box(610, 50, 135, 70, "Top pick pakar", ["35,0 ≥ ambang 24,7", "R-ADP-03"], GREEN_S, GREEN, 12, 10)
    b += arrow(677, 160, 677, 120, None, GREEN, marker="ahg")
    b += box(440, 50, 140, 70, "Manajemen risiko", ["SL/TP dari ATR", "posisi maks 7,1%"], GREY_S, LINE, 11.5, 10)
    b += arrow(610, 85, 580, 85)
    return svg(760, 345, b, "Alur penalaran emiten")


# =================================================================== D11 alur penalaran sektor
def d_alur_sektor():
    b = title(20, 26, "Alur penalaran sektor: dari berita sampai sektor inti")
    st = [("Berita", ["71 judul", "+ skor sentimen"], GREY_S, LINE), ("Peristiwa aktif", ["31 peristiwa", "Fed, perang, minyak"], BLUE_S, BLUE),
          ("Gerakan pasar", ["memicuPergerakan", "→ menyebabkan"], BLUE_S, BLUE), ("Tailwind", ["& headwind sektor", "+ tema struktural"], BLUE_S, BLUE),
          ("Skor skenario", ["base · bull · bear", "→ ekspektasi"], ORANGE_S, ORANGE), ("Peran", ["inti · satelit", "kontrarian"], GREEN_S, GREEN)]
    for i, (t, ls, f, c) in enumerate(st):
        x = 20 + i * 123
        b += box(x, 50, 112, 72, t, ls, f, c, 11, 9.5)
        if i < 5:
            b += arrow(x + 112, 86, x + 123, 86)
    b += f'<rect x="20" y="145" width="720" height="98" rx="8" fill="#fff" stroke="{LINE}" stroke-dasharray="3 3"/>'
    b += text(34, 166, "Contoh rantai nyata yang disimpulkan KB:", 11.5, INK, 700)
    b += text(34, 186, "Ev_EskalasiTimurTengah_Okt2026 → PremiRisikoTimurTengah → SafeHavenEmas → menguntungkan Barang Baku", 10.5, MUTED)
    b += text(34, 204, "Ev_RupiahTertekan_2026 → RupiahMelemah → PendapatanEksportirNaik → menguntungkan Barang Baku", 10.5, MUTED)
    b += text(34, 222, "Barang Baku: base 11 · bull 17 · bear 4 → tidak pernah negatif → SektorPilihanInti", 10.5, GREEN, 600)
    b += text(34, 238, "Kill switch: emas < US$3.800 → Tesis_BarangBaku_EmasNikel gugur → sektor dipantau ketat", 10.5, RED, 600)
    return svg(760, 255, b, "Alur penalaran sektor")


# =================================================================== D12 Fuseki client-server
def d_fuseki():
    b = title(20, 26, "Fuseki = server yang menjawab pertanyaan SPARQL lewat HTTP")
    b += box(20, 60, 200, 64, "Browser / dashboard", ["fetch('/saham/query')"], GREEN_S, GREEN, 12, 10)
    b += box(20, 140, 200, 50, "Aplikasi sekuritas", ["Python, Java, PHP…"], GREEN_S, GREEN, 12, 10)
    b += box(20, 206, 200, 50, "Terminal (curl)", ["curl …/query"], GREEN_S, GREEN, 12, 10)
    b += f'<rect x="300" y="50" width="250" height="220" rx="10" fill="{ORANGE_S}" stroke="{ORANGE}" stroke-width="1.5"/>'
    b += text(425, 74, "Apache Jena Fuseki", 13.5, INK, 700, "middle")
    b += text(425, 92, "localhost:3030", 11, MUTED, 400, "middle")
    eps = [("/saham/query", "SELECT, ASK (membaca)"), ("/saham/update", "INSERT, DELETE (mengubah)"), ("/saham-pellet/query", "membaca hasil Pellet"), ("/$/ping", "cek server hidup")]
    for i, (e, s) in enumerate(eps):
        y = 108 + i * 38
        b += f'<rect x="316" y="{y}" width="218" height="32" rx="6" fill="#fff" stroke="{ORANGE}"/>'
        b += text(326, y + 14, e, 11, INK, 700) + text(326, y + 27, s, 9.5, MUTED)
    b += arrow(220, 92, 300, 120, "permintaan HTTP", lx=222, ly=82)
    b += arrow(220, 165, 300, 165)
    b += arrow(220, 231, 300, 205)
    b += arrow(300, 250, 220, 250, "JSON", color=GREEN, marker="ahg", lx=240, ly=266)
    b += box(610, 70, 135, 80, "Dataset", ["kumpulan triple", "di memori"], BLUE_S, BLUE, 12, 10)
    b += box(610, 170, 135, 80, "Reasoner", ["aturan Jena", "(305 aturan)"], BLUE_S, BLUE, 12, 10)
    b += arrow(550, 110, 610, 110)
    b += arrow(550, 210, 610, 210)
    b += text(20, 296, "Protégé = meja kerja untuk merancang dan mengecek ontologi (satu orang, satu laptop).", 11, MUTED)
    b += text(20, 312, "Fuseki = server untuk MELAYANI ontologi itu ke banyak program sekaligus, persis seperti MySQL melayani tabel.", 11, MUTED)
    return svg(760, 325, b, "Fuseki client-server")


# =================================================================== D13 dua dataset
def d_dua_dataset():
    b = title(20, 26, "Konfigurasi proyek: dua dataset dalam satu server Fuseki")
    b += box(20, 52, 340, 200, "", [], BLUE_S, BLUE)
    b += text(190, 76, "/saham — penalaran langsung", 13, INK, 700, "middle")
    b += box(40, 92, 140, 48, "saham_data.ttl", ["fakta + ontologi"], "#fff", BLUE, 11, 9.5)
    b += box(200, 92, 140, 48, "saham_rules.rules", ["305 aturan Jena"], "#fff", BLUE, 11, 9.5)
    b += box(100, 168, 180, 52, "InfModel", ["GenericRuleReasoner"], ORANGE_S, ORANGE, 11.5, 9.5)
    b += arrow(110, 140, 160, 168)
    b += arrow(270, 140, 220, 168)
    b += text(190, 240, "bisa query DAN update (what-if)", 10.5, BLUE, 600, "middle")
    b += box(400, 52, 340, 200, "", [], GREEN_S, GREEN)
    b += text(570, 76, "/saham-pellet — hasil jadi", 13, INK, 700, "middle")
    b += box(470, 100, 200, 48, "SahamExpertKB_v2_inferred.owl", ["hasil Pellet dari run_all"], "#fff", GREEN, 10.5, 9.5)
    b += box(480, 168, 180, 52, "MemoryModel", ["tanpa reasoner"], "#fff", GREEN, 11.5, 9.5)
    b += arrow(570, 148, 570, 168)
    b += text(570, 240, "hanya query (baca), selalu konsisten", 10.5, GREEN, 600, "middle")
    b += text(20, 280, "Keduanya diuji memberi jawaban yang sama: regime Krisis Likuiditas, stres 11/12, 7 top pick pakar yang identik.", 11, MUTED)
    return svg(760, 292, b, "Dua dataset Fuseki")


# =================================================================== D14 arsitektur dashboard
def d_dashboard():
    b = title(20, 26, "Dashboard live: tiga program yang saling bicara")
    b += box(20, 60, 190, 110, "Browser", ["localhost:8080", "", "index.html", "(HTML + JavaScript)"], GREEN_S, GREEN, 13, 10.5)
    b += box(285, 60, 190, 110, "dashboard/server.py", ["Python, port 8080", "", "menyajikan halaman", "+ meneruskan /fuseki/…"], BLUE_S, BLUE, 12.5, 10.5)
    b += box(550, 60, 190, 110, "Fuseki", ["port 3030", "", "/saham", "/saham-pellet"], ORANGE_S, ORANGE, 13, 10.5)
    b += arrow(210, 95, 285, 95, "SPARQL", lx=225, ly=88)
    b += arrow(285, 135, 210, 135, "JSON", color=GREEN, marker="ahg", lx=230, ly=152)
    b += arrow(475, 95, 550, 95, "diteruskan", lx=480, ly=88)
    b += arrow(550, 135, 475, 135, None, GREEN, marker="ahg")
    b += f'<rect x="20" y="195" width="720" height="78" rx="8" fill="#fff" stroke="{LINE}" stroke-dasharray="3 3"/>'
    b += text(34, 216, "Kenapa perlu server.py di tengah?", 11.5, INK, 700)
    b += text(34, 235, "Browser melarang halaman di port 8080 meminta data ke port 3030 (aturan keamanan CORS).", 10.5, MUTED)
    b += text(34, 252, "server.py membuat keduanya tampak satu alamat: halaman meminta /fuseki/saham/query ke server.py,", 10.5, MUTED)
    b += text(34, 268, "lalu server.py meneruskannya ke http://localhost:3030/saham/query dan mengembalikan jawabannya.", 10.5, MUTED)
    return svg(760, 285, b, "Arsitektur dashboard")


# =================================================================== D15 SPARQL pattern matching
def d_sparql():
    b = title(20, 26, "SPARQL mencari pola triple di dalam graf")
    b += f'<rect x="20" y="44" width="330" height="128" rx="8" fill="#0f172a"/>'
    q = ["SELECT ?kode ?skor WHERE {", "  ?e a ex:KandidatTopPickAdaptif ;", "     ex:kodeSaham ?kode ;", "     ex:skorAdaptifRegime ?skor .", "}", "ORDER BY DESC(?skor)"]
    for i, l in enumerate(q):
        b += text(32, 66 + i * 17, l, 11.5, "#d6e2ff", 500)
    b += arrow(350, 108, 400, 108)
    b += f'<rect x="400" y="44" width="340" height="128" rx="8" fill="#fff" stroke="{LINE}"/>'
    rows = [("?kode", "?skor"), ("ANTM", "35,0"), ("TINS", "33,0"), ("LSIP", "29,5"), ("AADI", "29,0"), ("…", "…")]
    for i, (a, c) in enumerate(rows):
        y = 66 + i * 19
        b += text(420, y, a, 11.5, INK, 700 if i == 0 else 400) + text(560, y, c, 11.5, INK, 700 if i == 0 else 400)
        if i == 0:
            b += f'<line x1="412" y1="{y + 6}" x2="728" y2="{y + 6}" stroke="{LINE}"/>'
    b += text(20, 196, "?e, ?kode, ?skor = variabel (diawali tanda tanya). Setiap baris hasil = satu cara mengisi variabel", 11, MUTED)
    b += text(20, 212, "sehingga ketiga pola cocok dengan triple di graf. Tanda ; = subjek sama dengan baris sebelumnya,", 11, MUTED)
    b += text(20, 228, "a = singkatan rdf:type, titik = akhir pola.", 11, MUTED)
    return svg(760, 240, b, "Cara kerja SPARQL")


ALL = {"sistem_pakar": d_sistem_pakar, "ontologi_mini": d_ontologi_mini, "triple": d_triple, "reasoner": d_reasoner,
       "swrl": d_swrl, "eksternal": d_eksternal, "od101": d_od101, "arsitektur": d_arsitektur, "pipeline": d_pipeline,
       "alur_emiten": d_alur_emiten, "alur_sektor": d_alur_sektor, "fuseki": d_fuseki, "dua_dataset": d_dua_dataset,
       "dashboard": d_dashboard, "sparql": d_sparql}
