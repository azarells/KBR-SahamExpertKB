# -*- coding: utf-8 -*-
"""UJI KNOWLEDGE BASE LENGKAP — SahamExpertKB v2
=================================================
Menanyai ontologi hasil inferensi Pellet (output/SahamExpertKB_v2_inferred.owl) dengan SPARQL
(Apache Jena yang sudah ada di lib/, tanpa instalasi tambahan), lalu mencocokkan jawabannya dengan
kriteria lulus. Jawaban TIDAK ditulis tangan: semuanya dibaca dari KB.

Pakai (setelah python run_all.py):
    python3 tools/uji_kb.py            # uji statis (±80 soal, ±5 detik)
    python3 tools/uji_kb.py --whatif   # + uji what-if dinamis (ubah data -> Pellet ulang, ±40 detik)

Keluaran:
    output/HASIL_UJI_KB.md              tabel hasil + jawaban lengkap tiap soal
    output/uji_kb/queries_uji.rq        semua query SPARQL (bisa ditempel di Fuseki)
    output/uji_kb/hasil_uji_kb.json     hasil terstruktur
Kode keluar 0 bila semua lulus.
"""
import glob, json, os, re, subprocess, sys, shutil

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "output")
INF = os.path.join(OUT, "SahamExpertKB_v2_inferred.owl")
PFX = ("PREFIX ex: <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>\n"
       "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
       "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n")

T = []  # daftar soal


def soal(id, modul, tanya, protege, sparql, cek=None, jawab=None, cq=None):
    T.append(dict(id=id, modul=modul, tanya=tanya, protege=protege, sparql=sparql.strip(),
                  cek=cek or (lambda r: len(r) > 0), jawab=jawab, cq=cq))


# ------------------------------------------------------------------ util jawaban
def kol(r, k): return [x[k] for x in r]
def daftar(k, sep=", "): return lambda r: f"({len(r)}) " + sep.join(dict.fromkeys(kol(r, k)))
def nm(s): return re.sub(r"^(Sektor_|Ev_|Mv_|Tesis_|Persona_|Stk_|Regime_|Skenario_|Kasus_|Antisipasi_|K_|Kom_|Sub_|Broker_|Tema_)", "", s)
def f(x):
    try:
        v = float(x); return f"{v:g}" if abs(v) >= 0.01 or v == 0 else f"{v:.3f}"
    except Exception: return x
def baris(fmt):
    return lambda r: "; ".join(fmt(x) for x in r)
def ada(*nilai, k=None):
    """kriteria: semua nilai muncul di kolom k"""
    return lambda r: all(v in [x[k] for x in r] for v in nilai)
def minimal(n): return lambda r: len(r) >= n


# ================================================================== A. STRUKTUR & KUALITAS KB
soal("A01", "Struktur KB", "Apakah knowledge base konsisten (tidak ada kontradiksi logika)?",
     "Reasoner › Pellet › Start reasoner. Jika tidak muncul dialog *Inconsistent ontology* dan kelas `owl:Nothing` kosong, KB konsisten.",
     "#FILE validasi_owlapi_pellet.txt CONSISTENT",
     cek=lambda r: r and r[0]["nilai"] == "true", jawab=lambda r: "CONSISTENT = " + r[0]["nilai"] + " (OWLAPI + Pellet)")
soal("A02", "Struktur KB", "Berapa ukuran ontologi (kelas, properti, individu, aturan SWRL)?",
     "Active Ontology › tab *Ontology metrics*.",
     "#FILE validasi_owlapi_pellet.txt METRIK",
     cek=lambda r: int(r[0]["SWRL_RULES"]) >= 300,
     jawab=lambda r: ", ".join(f"{k}={v}" for k, v in r[0].items()))
soal("A03", "Struktur KB", "Apakah porsi knowledge base ≥ 80% dibanding porsi reasoning (aturan)?",
     "Ontology metrics: (Axiom count − SWRL rules) ÷ Axiom count.",
     "#FILE validasi_owlapi_pellet.txt RASIO",
     cek=lambda r: float(r[0]["persen"]) >= 80,
     jawab=lambda r: f"KB = {r[0]['persen']}% dari {r[0]['total']} aksioma; aturan SWRL = {r[0]['aturan']} aksioma")
soal("A04", "Struktur KB", "Berapa aturan SWRL per pilar analisis (semua aturan berkode & berpilar)?",
     "Window › Tabs › SWRLTab: kolom *Name* = kode aturan, kolom *Comment* = penjelasan.",
     """SELECT ?pilar (COUNT(?r) AS ?jumlah) WHERE { ?r ex:kodeAturan ?k ; ex:pilarAnalisis ?pilar } GROUP BY ?pilar ORDER BY DESC(?jumlah)""",
     cek=lambda r: sum(int(x["jumlah"]) for x in r) == 303,
     jawab=lambda r: f"total {sum(int(x['jumlah']) for x in r)} aturan · " + ", ".join(f"{x['pilar']} {x['jumlah']}" for x in r))
soal("A05", "Uji kebenaran aturan", "Apakah setiap emiten mendapat TEPAT SATU nilai per pilar skor (interval aturan saling lepas & menutup domain)?",
     "Pilih beberapa emiten di *Individuals*, lihat *Property assertions* (kuning): skorFundamental, skorValuasi, skorTeknikal, skorBandar masing-masing hanya satu nilai.",
     """SELECT ?kode (COUNT(DISTINCT ?f) AS ?nF) (COUNT(DISTINCT ?v) AS ?nV) (COUNT(DISTINCT ?t) AS ?nT) (COUNT(DISTINCT ?b) AS ?nB) (COUNT(DISTINCT ?x) AS ?nTotal)
WHERE { ?e a ex:Emiten ; ex:kodeSaham ?kode .
 OPTIONAL { ?e ex:skorFundamental ?f } OPTIONAL { ?e ex:skorValuasi ?v } OPTIONAL { ?e ex:skorTeknikal ?t }
 OPTIONAL { ?e ex:skorBandar ?b } OPTIONAL { ?e ex:skorTotalEmiten ?x } } GROUP BY ?kode""",
     cek=lambda r: len(r) >= 64 and all(all(x[k] == "1" for k in ("nF", "nV", "nT", "nB", "nTotal")) for x in r),
     jawab=lambda r: f"{sum(all(x[k]=='1' for k in ('nF','nV','nT','nB','nTotal')) for x in r)}/{len(r)} emiten punya tepat 1 nilai di tiap pilar")
soal("A06", "Uji kebenaran aturan", "Apakah skor total = jumlah 8 komponen (aritmetika swrlb:add benar) untuk semua emiten?",
     "Contoh ANTM di *Property assertions*: fundamental + valuasi + teknikal + bandar + sentimen + kontribusiSektor + penaltiRisiko + likuiditas = skorTotalEmiten.",
     """SELECT ?kode ?f ?v ?t ?b ?s ?k ?p ?l ?total WHERE { ?e a ex:Emiten ; ex:kodeSaham ?kode ; ex:skorFundamental ?f ; ex:skorValuasi ?v ;
 ex:skorTeknikal ?t ; ex:skorBandar ?b ; ex:skorSentimen ?s ; ex:skorKontribusiSektor ?k ; ex:penaltiRisiko ?p ; ex:poinLikuiditas ?l ; ex:skorTotalEmiten ?total } ORDER BY ?kode""",
     cek=lambda r: len(r) >= 64 and all(abs(sum(float(x[c]) for c in "fvtbskpl") - float(x["total"])) < 1e-6 for x in r),
     jawab=lambda r: f"{sum(abs(sum(float(x[c]) for c in 'fvtbskpl') - float(x['total'])) < 1e-6 for x in r)}/{len(r)} emiten cocok. Contoh "
                     + "; ".join(f"{x['kode']}: {x['f']}+{x['v']}+{x['t']}+{x['b']}+({x['s']})+({x['k']})+({x['p']})+{x['l']} = {x['total']}" for x in r if x["kode"] in ("ANTM", "BRMS")))
soal("A07", "Uji kebenaran aturan", "Apakah aturan bekerja pada emiten UJI fiktif (unit test aturan tata kelola/gorengan/collapse)?",
     "DL Query: `EmitenUji` → klik tiap individu, lihat kelas inferensi (kuning) di *Types*.",
     """SELECT ?e ?kelas WHERE { ?e a ex:EmitenUji ; a ?k . ?k rdfs:subClassOf* ex:KategoriInferensi .
 FILTER(?k NOT IN (ex:KategoriInferensi, ex:InferensiEmiten, ex:PenandaKualitasData)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?e ?kelas""",
     cek=lambda r: any(x["kelas"] == "IndikasiSahamGorengan" for x in r) and any(x["kelas"] == "RisikoGoingConcern" for x in r),
     jawab=lambda r: " · ".join(f"{e}: " + ", ".join(x["kelas"] for x in r if x["e"] == e) for e in dict.fromkeys(kol(r, "e"))))

# ================================================================== B. PENGETAHUAN DASAR SAHAM
soal("B01", "Pengetahuan dasar", "Apa itu PER, bagaimana rumusnya, dan kapan dianggap murah?",
     "Individuals › `PER` → panel *Annotations*: `rumus`, `interpretasi`, `ambangBatas`.",
     """SELECT ?label ?rumus ?interpretasi ?ambang WHERE { ex:PER rdfs:label ?label ; ex:rumus ?rumus ; ex:interpretasi ?interpretasi ; ex:ambangBatas ?ambang }""",
     jawab=lambda r: f"{r[0]['label']}: rumus {r[0]['rumus']}. {r[0]['interpretasi']} Ambang: {r[0]['ambang']}", cq="CQ12")
soal("B02", "Pengetahuan dasar", "Rasio keuangan apa saja yang ada di KB beserta rumusnya?",
     "DL Query: `RasioKeuangan` (centang *Instances*); klik individu untuk melihat anotasi `rumus`.",
     """SELECT ?r ?kelompok ?rumus WHERE { ?r a ex:RasioKeuangan ; a ?k . ?k rdfs:subClassOf ex:RasioKeuangan . OPTIONAL { ?r ex:rumus ?rumus }
 BIND(STRAFTER(STR(?k),"#") AS ?kelompok) } ORDER BY ?kelompok ?r""",
     cek=minimal(35), jawab=lambda r: f"({len(set(kol(r,'r')))} rasio) " + "; ".join(f"{x['r']} [{x['kelompok']}] = {x['rumus'] or '-'}" for x in r))
soal("B03", "Pengetahuan dasar", "Rasio khusus perbankan apa saja dan apa ambang sehatnya?",
     "DL Query: `RasioPerbankan`.",
     """SELECT ?r ?rumus ?ambang WHERE { ?r a ex:RasioPerbankan . OPTIONAL { ?r ex:rumus ?rumus } OPTIONAL { ?r ex:ambangBatas ?ambang } } ORDER BY ?r""",
     cek=ada("NIM", "NPL", "CAR", "LDR", k="r"), jawab=baris(lambda x: f"{x['r']} ({x['rumus'] or '-'}; ambang: {x['ambang'] or '-'})"))
soal("B04", "Pengetahuan dasar", "Bagaimana mekanisme perdagangan di BEI (ARB/ARA, lot, T+2, sesi, papan)?",
     "DL Query: `MekanismePerdagangan`; klik individu → `rdfs:comment`.",
     """SELECT ?m ?label ?penjelasan WHERE { ?m a ex:MekanismePerdagangan ; rdfs:label ?label . OPTIONAL { ?m rdfs:comment ?penjelasan } } ORDER BY ?m""",
     cek=ada("AutoRejectionBawah", "Lot", "SettlementT2", k="m"), jawab=baris(lambda x: f"{x['label']}: {x['penjelasan'] or '-'}"))
soal("B05", "Pengetahuan dasar", "Aksi korporasi mana yang berdampak positif, netral, dan negatif?",
     "DL Query: `AksiKorporasiPositif`, `AksiKorporasiNegatif`, `AksiKorporasiNetral`.",
     """SELECT ?dampak ?a WHERE { ?a a ?k . FILTER(?k IN (ex:AksiKorporasiPositif, ex:AksiKorporasiNegatif, ex:AksiKorporasiNetral)) BIND(STRAFTER(STR(?k),"AksiKorporasi") AS ?dampak) } ORDER BY ?dampak ?a""",
     cek=minimal(10), jawab=lambda r: " · ".join(f"{d}: " + ", ".join(x["a"] for x in r if x["dampak"] == d) for d in dict.fromkeys(kol(r, "dampak"))))
soal("B06", "Pengetahuan dasar", "Indikator teknikal apa saja dan bagaimana membaca RSI & MACD?",
     "DL Query: `IndikatorTeknikal`; individu `RSI`, `MACD` → anotasi.",
     """SELECT ?i ?rumus ?arti WHERE { ?i a ex:IndikatorTeknikal . OPTIONAL { ?i ex:rumus ?rumus } OPTIONAL { ?i rdfs:comment ?arti } } ORDER BY ?i""",
     cek=ada("RSI", "MACD", "SMA", k="i"),
     jawab=lambda r: f"({len(r)}) " + ", ".join(kol(r, "i")) + " · " + "; ".join(f"{x['i']}: {x['rumus'] or ''} {x['arti'] or ''}".strip() for x in r if x["i"] in ("RSI", "MACD")))
soal("B07", "Pengetahuan dasar", "Pola chart mana yang bullish, bearish, reversal, dan kontinuasi?",
     "DL Query: `PolaBullish`, `PolaBearish`, `PolaReversal`, `PolaKontinuasi`.",
     """SELECT ?jenis ?p WHERE { ?p a ?k . FILTER(?k IN (ex:PolaBullish, ex:PolaBearish, ex:PolaReversal, ex:PolaKontinuasi)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?p""",
     cek=minimal(15), jawab=lambda r: " · ".join(f"{d}: " + ", ".join(x["p"] for x in r if x["jenis"] == d) for d in dict.fromkeys(kol(r, "jenis"))))
soal("B08", "Pengetahuan dasar", "Pola candlestick apa saja yang dikenali?",
     "DL Query: `PolaCandlestick` (subkelas CandlestickBullish/Bearish/Indecision).",
     """SELECT ?jenis ?c WHERE { ?c a ?k . FILTER(?k IN (ex:CandlestickBullish, ex:CandlestickBearish, ex:CandlestickIndecision)) BIND(STRAFTER(STR(?k),"Candlestick") AS ?jenis) } ORDER BY ?jenis ?c""",
     cek=minimal(15), jawab=lambda r: " · ".join(f"{d}: " + ", ".join(x["c"] for x in r if x["jenis"] == d) for d in dict.fromkeys(kol(r, "jenis"))))
soal("B09", "Pengetahuan dasar", "Teori teknikal apa saja (Dow, Elliott, Wyckoff, Fibonacci, rotasi sektor)?",
     "DL Query: `TeoriTeknikal`.",
     """SELECT ?t ?arti WHERE { ?t a ex:TeoriTeknikal . OPTIONAL { ?t rdfs:comment ?arti } } ORDER BY ?t""",
     cek=ada("WyckoffMethod", "DowTheory", k="t"), jawab=baris(lambda x: f"{x['t']}: {x['arti'] or '-'}"))
soal("B10", "Pengetahuan dasar", "Bias perilaku investor apa yang dimodelkan?",
     "DL Query: `BiasPerilaku`.",
     """SELECT ?b ?arti WHERE { ?b a ex:BiasPerilaku . OPTIONAL { ?b rdfs:comment ?arti } } ORDER BY ?b""",
     cek=ada("FOMO", "PanicSelling", "LossAversion", k="b"), jawab=baris(lambda x: f"{x['b']}: {x['arti'] or '-'}"))
soal("B11", "Pengetahuan dasar", "Instrumen pasar modal dan gaya investasi apa saja yang dikenal KB?",
     "DL Query: `InstrumenPasarModal` dan `GayaInvestasi`.",
     """SELECT ?jenis ?i WHERE { ?i a ?k . FILTER(?k IN (ex:InstrumenPasarModal, ex:GayaInvestasi)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?i""",
     cek=minimal(20), jawab=lambda r: " · ".join(f"{d}: " + ", ".join(x["i"] for x in r if x["jenis"] == d) for d in dict.fromkeys(kol(r, "jenis"))))
soal("B12", "Pengetahuan dasar", "Konsep manajemen risiko apa saja (stop loss, position sizing, dll.)?",
     "DL Query: `ManajemenRisiko`.",
     """SELECT ?m ?rumus ?arti WHERE { ?m a ex:ManajemenRisiko . OPTIONAL { ?m ex:rumus ?rumus } OPTIONAL { ?m rdfs:comment ?arti } } ORDER BY ?m""",
     cek=ada("StopLoss", "PositionSizing", k="m"), jawab=baris(lambda x: f"{x['m']}" + (f" ({x['rumus']})" if x['rumus'] else "")))
soal("B13", "Pengetahuan dasar", "Biaya & pajak transaksi saham di Indonesia?",
     "DL Query: `BiayaDanPajak`.",
     """SELECT ?b ?arti WHERE { ?b a ex:BiayaDanPajak . OPTIONAL { ?b rdfs:comment ?arti } } ORDER BY ?b""",
     jawab=baris(lambda x: f"{x['b']}: {x['arti'] or '-'}"))
soal("B14", "Pengetahuan dasar", "Status pengawasan BEI apa saja (suspensi, UMA, notasi khusus, papan pemantauan)?",
     "DL Query: `StatusPengawasan`.",
     """SELECT ?s ?arti WHERE { ?s a ex:StatusPengawasan . OPTIONAL { ?s rdfs:comment ?arti } } ORDER BY ?s""",
     cek=ada("Suspensi", "UnusualMarketActivity", k="s"), jawab=baris(lambda x: f"{x['s']}: {x['arti'] or '-'}"))
soal("B15", "Pengetahuan dasar", "Heuristik pakar apa yang dipakai (aturan praktis ahli)?",
     "Cari anotasi `heuristikPakar` (Window › Tabs › *Annotation*/*Search*: heuristikPakar).",
     """SELECT ?h ?isi WHERE { ?h ex:heuristikPakar ?isi } ORDER BY ?h""",
     cek=minimal(30), jawab=lambda r: f"({len(r)}) " + "; ".join(f"{x['h']}: {x['isi'][:90]}" for x in r[:8]) + " …")

# ================================================================== C. FUNDAMENTAL
soal("C01", "Fundamental", "Emiten mana yang fundamentalnya kuat, sedang, dan lemah?",
     "DL Query: `FundamentalKuat` / `FundamentalSedang` / `FundamentalLemah`.",
     """SELECT ?kelas ?kode WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:FundamentalKuat, ex:FundamentalSedang, ex:FundamentalLemah)) FILTER NOT EXISTS { ?e a ex:EmitenUji }
 BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas ?kode""",
     cek=lambda r: "FundamentalKuat" in kol(r, "kelas"),
     jawab=lambda r: " · ".join(f"{d} ({kol(r,'kelas').count(d)}): " + ", ".join(x["kode"] for x in r if x["kelas"] == d) for d in dict.fromkeys(kol(r, "kelas"))))
soal("C02", "Fundamental", "Emiten mana yang undervalued, fair, overvalued (PER vs rata-rata 5 tahun)?",
     "DL Query: `Undervalued`, `FairValued`, `Overvalued`. SQWRL: `Emiten(?e) ^ rasioPERvsHistoris(?e, ?r) -> sqwrl:select(?e, ?r) ^ sqwrl:orderBy(?r)`",
     """SELECT ?kelas ?kode ?rasio WHERE { ?e ex:kodeSaham ?kode ; ex:rasioPERvsHistoris ?rasio ; a ?k . FILTER(?k IN (ex:Undervalued, ex:FairValued, ex:Overvalued)) FILTER NOT EXISTS { ?e a ex:EmitenUji }
 BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas ?rasio""",
     jawab=lambda r: " · ".join(f"{d} ({kol(r,'kelas').count(d)}): " + ", ".join(f"{x['kode']}({float(x['rasio']):.2f}×)" for x in r if x["kelas"] == d) for d in dict.fromkeys(kol(r, "kelas"))))
soal("C03", "Fundamental", "Emiten mana yang terlihat murah tapi sebenarnya jebakan (value trap)?",
     "DL Query: `ValueTrap`. Bandingkan dengan `MurahKarenaLabaTurun` (revisi laba turun + undervalued).",
     """SELECT ?jenis ?kode WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:ValueTrap, ex:MurahKarenaLabaTurun)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?kode""",
     jawab=lambda r: " · ".join(f"{d}: " + ", ".join(x["kode"] for x in r if x["jenis"] == d) for d in dict.fromkeys(kol(r, "jenis"))))
soal("C04", "Fundamental", "Emiten mana yang rawan collapse / going concern, dan apa buktinya?",
     "DL Query: `RisikoGoingConcern`. SQWRL Q11: `RisikoGoingConcern(?e) ^ altmanZ(?e, ?z) ^ der(?e, ?d) -> sqwrl:select(?e, ?z, ?d) ^ sqwrl:orderBy(?z)`",
     """SELECT ?kode ?altmanZ ?der WHERE { ?e a ex:RisikoGoingConcern ; ex:kodeSaham ?kode ; ex:altmanZ ?altmanZ . OPTIONAL { ?e ex:der ?der } FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY ?altmanZ""",
     jawab=baris(lambda x: f"{x['kode']} (Altman Z {f(x['altmanZ'])}, DER {f(x['der'])})"), cq="CQ6")
soal("C05", "Fundamental", "Zona Altman Z: siapa aman, abu-abu, distress?",
     "DL Query: `ZonaAman`, `ZonaAbuAbu`, `ZonaDistress`.",
     """SELECT ?zona (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:ZonaAman, ex:ZonaAbuAbu, ex:ZonaDistress)) FILTER NOT EXISTS { ?e a ex:EmitenUji }
 BIND(STRAFTER(STR(?k),"#") AS ?zona) } GROUP BY ?zona""",
     cek=minimal(3), jawab=baris(lambda x: f"{x['zona']} ({x['n']}): {x['emiten']}"))
soal("C06", "Fundamental", "Emiten mana yang berisiko manipulasi laba (Beneish M-Score) atau kualitas labanya tinggi?",
     "DL Query: `RisikoManipulasiLaba`, `KualitasLabaTinggi`.",
     """SELECT ?kelas (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:RisikoManipulasiLaba, ex:KualitasLabaTinggi)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']} ({x['n']}): {x['emiten']}"))
soal("C07", "Fundamental", "Berapa nilai wajar dan potensi upside emiten top pick?",
     "Individu `ANTM` → *Property assertions*: `nilaiWajar`, `potensiUpsidePersen`, `hargaPenutupan`.",
     """SELECT ?kode ?harga ?nilaiWajar ?upside WHERE { ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode ; ex:hargaPenutupan ?harga ; ex:nilaiWajar ?nilaiWajar ; ex:potensiUpsidePersen ?upside } ORDER BY DESC(?upside)""",
     jawab=baris(lambda x: f"{x['kode']}: harga {f(x['harga'])} → wajar {f(x['nilaiWajar'])} (upside {f(x['upside'])}%)"))
soal("C08", "Fundamental", "Emiten mana yang menjadi andalan dividen?",
     "DL Query: `DividenAndalan`.",
     """SELECT ?kode ?dy ?dpr WHERE { ?e a ex:DividenAndalan ; ex:kodeSaham ?kode ; ex:dividendYield ?dy . OPTIONAL { ?e ex:dpr ?dpr } } ORDER BY DESC(?dy)""",
     jawab=baris(lambda x: f"{x['kode']} (DY {f(x['dy'])}%)"))
soal("C09", "Fundamental", "Bank mana yang permodalannya lemah atau NPL-nya tinggi?",
     "DL Query: `EmitenPerbankan`, lalu `BankModalLemah`. Hasil kosong berarti semua bank lolos ambang (CAR ≥ batas).",
     """SELECT ?kode ?npl ?car ?nim ?lemah WHERE { ?e a ex:EmitenPerbankan ; ex:kodeSaham ?kode . OPTIONAL { ?e ex:npl ?npl } OPTIONAL { ?e ex:car ?car } OPTIONAL { ?e ex:nim ?nim }
 BIND(EXISTS { ?e a ex:BankModalLemah } AS ?lemah) } ORDER BY ?kode""",
     jawab=baris(lambda x: f"{x['kode']} (NPL {f(x['npl'])}%, CAR {f(x['car'])}%, NIM {f(x['nim'])}%, modal lemah: {'ya' if x['lemah']=='true' else 'tidak'})"))

# ================================================================== D. TEKNIKAL
soal("D01", "Teknikal", "Emiten mana yang sedang tren naik dan tren turun?",
     "DL Query: `TrenNaik` / `TrenTurun`.",
     """SELECT ?kelas (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:TrenNaik, ex:TrenTurun)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']} ({x['n']}): {x['emiten']}"))
soal("D02", "Teknikal", "Sinyal entry mana yang aktif, lengkap dengan stop loss & take profit (berbasis ATR)?",
     "SQWRL Q12: `SinyalEntry(?e) ^ hargaPenutupan(?e, ?h) ^ hargaStopLoss(?e, ?sl) ^ hargaTakeProfit(?e, ?tp) -> sqwrl:select(?e, ?h, ?sl, ?tp)`",
     """SELECT ?kode ?harga ?stopLoss ?takeProfit WHERE { ?e a ex:SinyalEntry ; ex:kodeSaham ?kode ; ex:hargaPenutupan ?harga ; ex:hargaStopLoss ?stopLoss ; ex:hargaTakeProfit ?takeProfit FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY ?kode""",
     cek=lambda r: len(r) > 0 and all(float(x["stopLoss"]) < float(x["harga"]) < float(x["takeProfit"]) for x in r),
     jawab=baris(lambda x: f"{x['kode']} {f(x['harga'])} (SL {f(x['stopLoss'])}, TP {f(x['takeProfit'])})"))
soal("D03", "Teknikal", "Sinyal buy-on-weakness, exit, dan hindari?",
     "DL Query: `SinyalBuyOnWeakness`, `SinyalExit`, `SinyalHindari`.",
     """SELECT ?sinyal (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:SinyalBuyOnWeakness, ex:SinyalExit, ex:SinyalHindari)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?sinyal) } GROUP BY ?sinyal""",
     jawab=baris(lambda x: f"{x['sinyal']}: {x['emiten']}"))
soal("D04", "Teknikal", "Pola chart apa yang terdeteksi dan mana yang terkonfirmasi indikator?",
     "SQWRL: `KonfirmasiPolaBullish(?e) ^ terdeteksiPola(?e, ?p) -> sqwrl:select(?e, ?p)`",
     """SELECT ?status ?kode ?pola WHERE { ?e ex:kodeSaham ?kode ; ex:terdeteksiPola ?pola ; a ?k . FILTER(?k IN (ex:KonfirmasiPolaBullish, ex:KonfirmasiPolaBearish)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"KonfirmasiPola") AS ?status) } ORDER BY ?status ?kode""",
     jawab=lambda r: " · ".join(f"{d}: " + ", ".join(f"{x['kode']}-{x['pola']}" for x in r if x["status"] == d) for d in dict.fromkeys(kol(r, "status"))))
soal("D05", "Teknikal", "Overbought/oversold (RSI) dan lonjakan volume?",
     "DL Query: `Overbought`, `Oversold`, `LonjakanVolume`.",
     """SELECT ?kelas ?kode ?rsi ?rasioVolume WHERE { ?e ex:kodeSaham ?kode ; ex:rsi14 ?rsi ; ex:rasioVolume ?rasioVolume ; a ?k . FILTER(?k IN (ex:Overbought, ex:Oversold, ex:LonjakanVolume)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['kode']} (RSI {f(x['rsi'])}, vol {f(x['rasioVolume'])}×)"))
soal("D06", "Teknikal", "Emiten mana yang outperform / underperform IHSG (kekuatan relatif)?",
     "DL Query: `OutperformPasar`. SQWRL Q29 untuk angka kekuatanRelatifPersen.",
     """SELECT ?kelas ?kode ?kr WHERE { ?e ex:kodeSaham ?kode ; ex:kekuatanRelatifPersen ?kr ; a ?k . FILTER(?k IN (ex:OutperformPasar, ex:UnderperformPasar)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas DESC(?kr)""",
     jawab=lambda r: " · ".join(f"{d} ({kol(r,'kelas').count(d)}): " + ", ".join(f"{x['kode']}({float(x['kr']):+.1f}%)" for x in r if x["kelas"] == d) for d in ("OutperformPasar", "UnderperformPasar") if d in kol(r, "kelas")))
soal("D07", "Teknikal", "Sinyal scalping (trader jangka sangat pendek)?",
     "DL Query: `SinyalScalpingLong`, `SinyalScalpingHindari`.",
     """SELECT ?sinyal ?kode WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:SinyalScalpingLong, ex:SinyalScalpingHindari)) BIND(STRAFTER(STR(?k),"#") AS ?sinyal) } ORDER BY ?sinyal""",
     jawab=baris(lambda x: f"{x['sinyal']}: {x['kode']}"))

# ================================================================== E. BANDARMOLOGY
soal("E01", "Bandarmology", "Emiten mana yang sedang diakumulasi bandar, dan broker siapa akumulatornya?",
     "DL Query: `AkumulasiBandar`. Individu emiten → `brokerAkumulatorUtama`.",
     """SELECT ?kode ?broker ?skorAccDist WHERE { ?e a ex:AkumulasiBandar ; ex:kodeSaham ?kode . OPTIONAL { ?e ex:brokerAkumulatorUtama ?broker } OPTIONAL { ?e ex:skorAccDistBroker ?skorAccDist } FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY DESC(?skorAccDist)""",
     jawab=baris(lambda x: f"{x['kode']} ({nm(x['broker'] or '-')}, acc/dist {f(x['skorAccDist'])})"))
soal("E02", "Bandarmology", "Di mana smart money diam-diam akumulasi saat harga masih turun (divergensi)?",
     "DL Query: `AkumulasiTersembunyi` (SQWRL Q13).",
     """SELECT ?kode ?chg20 ?netAsing WHERE { ?e a ex:AkumulasiTersembunyi ; ex:kodeSaham ?kode ; ex:perubahanHarga20HariPersen ?chg20 ; ex:netAsing20HariM ?netAsing FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY ?kode""",
     jawab=baris(lambda x: f"{x['kode']} (harga 20h {f(x['chg20'])}%, net asing {f(x['netAsing'])} M)"))
soal("E03", "Bandarmology", "Emiten mana yang sedang didistribusikan bandar ke ritel?",
     "DL Query: `DistribusiKeRitel`, `DistribusiBandar`.",
     """SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:DistribusiKeRitel, ex:DistribusiBandar)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['emiten']}"))
soal("E04", "Bandarmology", "Asing sedang akumulasi atau distribusi di emiten mana?",
     "DL Query: `AsingAkumulasi` / `AsingDistribusi`.",
     """SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:AsingAkumulasi, ex:AsingDistribusi)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['emiten']}"))
soal("E05", "Bandarmology", "Fase Wyckoff tiap emiten (akumulasi, mark-up, distribusi, mark-down)?",
     "DL Query: `FaseAkumulasiWyckoff`, `FaseMarkUpWyckoff`, `FaseDistribusiWyckoff`, `FaseMarkDownWyckoff`.",
     """SELECT ?fase (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:FaseAkumulasiWyckoff, ex:FaseMarkUpWyckoff, ex:FaseDistribusiWyckoff, ex:FaseMarkDownWyckoff)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?fase) } GROUP BY ?fase""",
     jawab=baris(lambda x: f"{x['fase']} ({x['n']}): {x['emiten']}"))
soal("E06", "Bandarmology", "Konsep & alat bandarmology apa yang ada di KB?",
     "DL Query: `KonsepBandarmology`, `PolaBandar`.",
     """SELECT ?jenis ?k2 WHERE { ?k2 a ?k . FILTER(?k IN (ex:KonsepBandarmology, ex:PolaBandarBullish, ex:PolaBandarBearish, ex:PolaManipulatif)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?k2""",
     cek=minimal(15), jawab=lambda r: " · ".join(f"{d}: " + ", ".join(x["k2"] for x in r if x["jenis"] == d) for d in dict.fromkeys(kol(r, "jenis"))))
soal("E07", "Bandarmology", "Broker apa saja dan bagaimana klasifikasinya (asing/lokal/ritel/institusi)?",
     "DL Query: `Broker` dan subkelasnya.",
     """SELECT ?jenis (GROUP_CONCAT(?bn; separator=", ") AS ?broker) WHERE { ?b a ?k . BIND(STRAFTER(STR(?b),"Broker_") AS ?bn) FILTER(?k IN (ex:BrokerAsing, ex:BrokerLokal, ex:BrokerRitel, ex:BrokerInstitusiLokal)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } GROUP BY ?jenis""",
     jawab=baris(lambda x: f"{x['jenis']}: {x['broker']}"))
soal("E08", "Bandarmology", "Apakah ada indikasi saham gorengan / pump and dump / jual paksa pengendali?",
     "DL Query: `IndikasiSahamGorengan`, `RisikoPumpAndDump`, `RisikoForcedSellPengendali`, `RisikoHSC`.",
     """SELECT ?kelas ?e WHERE { ?e a ?k . FILTER(?k IN (ex:IndikasiSahamGorengan, ex:RisikoPumpAndDump, ex:RisikoForcedSellPengendali, ex:RisikoHSC, ex:SinyalOrangDalam)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas""",
     jawab=lambda r: " · ".join(f"{d}: " + ", ".join(x["e"] for x in r if x["kelas"] == d) for d in dict.fromkeys(kol(r, "kelas"))))

# ================================================================== F. SENTIMEN
soal("F01", "Sentimen", "Berapa berita yang dianalisis dan dari kategori apa?",
     "DL Query: `Berita` (lalu `BeritaMakroGeopolitik`, `BeritaEmiten`, `BeritaRisetAnalis`).",
     """SELECT ?kategori (COUNT(?b) AS ?n) WHERE { ?b a ?k . FILTER(?k IN (ex:BeritaMakroGeopolitik, ex:BeritaEmiten, ex:BeritaRisetAnalis)) BIND(STRAFTER(STR(?k),"#") AS ?kategori) } GROUP BY ?kategori""",
     jawab=lambda r: f"total {sum(int(x['n']) for x in r)} berita · " + ", ".join(f"{x['kategori']} {x['n']}" for x in r))
soal("F02", "Sentimen", "Bagaimana skor sentimen tiap sektor dari berita?",
     "Individu `Sektor_*` → `skorSentimenSektor`, `poinSentimenSektor`.",
     """SELECT ?sektor ?skor ?poin WHERE { ?s a ex:Sektor ; ex:skorSentimenSektor ?skor . OPTIONAL { ?s ex:poinSentimenSektor ?poin } BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } ORDER BY DESC(?skor)""",
     cek=minimal(11), jawab=baris(lambda x: f"{x['sektor']} {float(x['skor']):+.3f} (poin {x['poin'] or 0})"))
soal("F03", "Sentimen", "Emiten mana yang sentimennya positif / negatif?",
     "DL Query: `SentimenPositif`, `SentimenNegatif`.",
     """SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:SentimenPositif, ex:SentimenNegatif)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['emiten']}"))
soal("F04", "Sentimen", "Berita mana yang menjadi red flag untuk emiten?",
     "SQWRL Q16: `memilikiRedFlag(?e, ?n) ^ judulBerita(?n, ?j) -> sqwrl:select(?e, ?j)`",
     """SELECT ?kode ?judul WHERE { ?e ex:memilikiRedFlag ?n ; ex:kodeSaham ?kode . ?n ex:judulBerita ?judul } ORDER BY ?kode""",
     jawab=baris(lambda x: f"{x['kode']}: \"{x['judul'][:80]}\""))
soal("F05", "Sentimen", "Emiten mana yang tahan berita buruk (harga tidak turun saat berita negatif)?",
     "DL Query: `SinyalKetahananBeritaBuruk`.",
     """SELECT ?kode WHERE { ?e a ex:SinyalKetahananBeritaBuruk ; ex:kodeSaham ?kode }""",
     cek=lambda r: True, jawab=lambda r: daftar("kode")(r) if r else "Tidak ada emiten yang memenuhi syarat saat ini (jawaban sah: kelas kosong).")
soal("F06", "Sentimen", "Komponen machine learning apa yang dipakai dan perannya (pendukung < 20%)?",
     "DL Query: `KomponenML`.",
     """SELECT ?m ?arti WHERE { ?m a ex:KomponenML . OPTIONAL { ?m rdfs:comment ?arti } } ORDER BY ?m""",
     jawab=baris(lambda x: f"{x['m']}: {(x['arti'] or '-')[:100]}"))

# ================================================================== G. GEOPOLITIK & MAKRO
soal("G01", "Geopolitik & makro", "Peristiwa geopolitik/makro apa saja yang sedang aktif?",
     "DL Query: `PeristiwaAktif`.",
     """SELECT ?jenis ?ev WHERE { ?ev a ex:PeristiwaAktif ; a ?k . ?k rdfs:subClassOf ex:PeristiwaGeopolitik . BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?ev""",
     cek=minimal(20), jawab=lambda r: f"({len(set(kol(r,'ev')))} peristiwa) " + " · ".join(f"{d}: " + ", ".join(nm(x["ev"]) for x in r if x["jenis"] == d) for d in dict.fromkeys(kol(r, "jenis"))), cq="CQ9")
soal("G02", "Geopolitik & makro", "Apa dampak kebijakan The Fed (FOMC hawkish / kenaikan FFR) ke pasar Indonesia?",
     "Individu `Ev_FedHike_Sep2026` → `memicuPergerakan`; lalu ikuti `menyebabkan` dan `menguntungkanSektor`/`merugikanSektor`.",
     """SELECT ?ev ?gerak ?lanjutan ?untung ?rugi WHERE { ?ev ex:memicuPergerakan ?gerak . FILTER(?ev IN (ex:Ev_FedHike_Sep2026, ex:Ev_FOMC_Hawkish_2026))
 OPTIONAL { ?gerak ex:menyebabkan ?lanjutan } OPTIONAL { ?gerak ex:menguntungkanSektor ?untung } OPTIONAL { ?gerak ex:merugikanSektor ?rugi } } ORDER BY ?ev ?gerak""",
     jawab=lambda r: "; ".join(dict.fromkeys(f"{nm(x['ev'])} → {nm(x['gerak'])}" + (f" → {nm(x['lanjutan'])}" if x['lanjutan'] else "")
                                             + (f" [+{nm(x['untung'])}]" if x['untung'] else "") + (f" [−{nm(x['rugi'])}]" if x['rugi'] else "") for x in r)))
soal("G03", "Geopolitik & makro", "Bagaimana perang/ketegangan Timur Tengah (Hormuz) memengaruhi minyak dan sektor saham?",
     "Individu `Ev_PenutupanHormuz_2026` dan `Ev_EskalasiTimurTengah_Okt2026` → `memicuPergerakan` → `menaikkanHargaKomoditas`, `menguntungkanSektor`.",
     """SELECT ?ev ?gerak ?komoditas ?untung ?rugi WHERE { ?ev ex:memicuPergerakan ?gerak . FILTER(?ev IN (ex:Ev_PenutupanHormuz_2026, ex:Ev_EskalasiTimurTengah_Okt2026, ex:Ev_GencatanRusiaUkraina_Okt2026))
 OPTIONAL { ?gerak ex:menaikkanHargaKomoditas ?komoditas } OPTIONAL { ?gerak ex:menguntungkanSektor ?untung } OPTIONAL { ?gerak ex:merugikanSektor ?rugi } } ORDER BY ?ev""",
     jawab=lambda r: "; ".join(dict.fromkeys(f"{nm(x['ev'])} → {nm(x['gerak'])}" + (f" (↑{nm(x['komoditas'])})" if x['komoditas'] else "")
                                             + (f" [+{nm(x['untung'])}]" if x['untung'] else "") + (f" [−{nm(x['rugi'])}]" if x['rugi'] else "") for x in r)))
soal("G04", "Geopolitik & makro", "Apa dampak inflasi dan krisis (rupiah, twin deficit, crash IHSG)?",
     "Individu `Ev_InflasiNaik_Sep2026`, `Ev_RupiahTertekan_2026`, `Ev_TwinDeficit_2026`, `Ev_CrashIHSG_16Okt2026` → `memicuPergerakan`.",
     """SELECT ?ev ?gerak ?untung ?rugi WHERE { ?ev ex:memicuPergerakan ?gerak . FILTER(?ev IN (ex:Ev_InflasiNaik_Sep2026, ex:Ev_RupiahTertekan_2026, ex:Ev_TwinDeficit_2026, ex:Ev_CrashIHSG_16Okt2026))
 OPTIONAL { ?gerak ex:menguntungkanSektor ?untung } OPTIONAL { ?gerak ex:merugikanSektor ?rugi } } ORDER BY ?ev""",
     jawab=lambda r: "; ".join(dict.fromkeys(f"{nm(x['ev'])} → {nm(x['gerak'])}" + (f" [+{nm(x['untung'])}]" if x['untung'] else "") + (f" [−{nm(x['rugi'])}]" if x['rugi'] else "") for x in r)))
soal("G05", "Geopolitik & makro", "Tunjukkan rantai sebab-akibat multi-hop: peristiwa → gerakan 1 → gerakan 2 → sektor diuntungkan.",
     "SQWRL Q07: `PeristiwaAktif(?ev) ^ memicuPergerakan(?ev, ?m1) ^ menyebabkan(?m1, ?m2) ^ menguntungkanSektor(?m2, ?s) -> sqwrl:select(?ev, ?m1, ?m2, ?s)`",
     """SELECT ?ev ?hop1 ?hop2 ?sektor WHERE { ?ev a ex:PeristiwaAktif ; ex:memicuPergerakan ?hop1 . ?hop1 ex:menyebabkan ?hop2 . ?hop2 ex:menguntungkanSektor ?sektor } ORDER BY ?sektor""",
     jawab=lambda r: f"({len(r)} jalur) " + "; ".join(f"{nm(x['ev'])} → {nm(x['hop1'])} → {nm(x['hop2'])} → {nm(x['sektor'])}" for x in r[:12]) + (" …" if len(r) > 12 else ""))
soal("G06", "Geopolitik & makro", "Sektor mana yang diuntungkan dan dirugikan geopolitik saat ini?",
     "DL Query: `SektorDiuntungkanGeopolitik`, `SektorDirugikanGeopolitik`.",
     """SELECT ?kelas (GROUP_CONCAT(?sek; separator=", ") AS ?sektor) WHERE { ?s a ?k . FILTER(?k IN (ex:SektorDiuntungkanGeopolitik, ex:SektorDirugikanGeopolitik)) BIND(STRAFTER(STR(?s),"Sektor_") AS ?sek) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['sektor']}"))
soal("G07", "Geopolitik & makro", "Berapa nilai indikator makro terkini (BI-Rate, Fed, kurs, Brent, emas, CDS, inflasi, SBN)?",
     "Individu `Pasar_ID_Okt2026` → *Property assertions*.",
     """SELECT ?biRate ?ffr ?kurs ?brent ?emas ?cds ?inflasi ?sbn10y ?drawdownIHSG WHERE { ?k a ex:KondisiPasarAktif ; ex:biRatePersen ?biRate ; ex:ffrAtasPersen ?ffr ; ex:kursUSDIDR ?kurs ; ex:brentUSD ?brent ;
 ex:emasUSD ?emas ; ex:cds5YBps ?cds ; ex:inflasiYoY ?inflasi ; ex:yieldSBN10Y ?sbn10y ; ex:drawdownIHSGPersen ?drawdownIHSG }""",
     jawab=lambda r: ", ".join(f"{k} {f(v)}" for k, v in r[0].items()))
soal("G08", "Geopolitik & makro", "Emiten mana yang diuntungkan / ditekan pergerakan komoditas & makro?",
     "SQWRL Q08: `diuntungkanOleh(?e, ?m) -> sqwrl:select(?e, ?m) ^ sqwrl:orderBy(?e)`",
     """SELECT ?arah ?kode ?gerak WHERE { { ?e ex:diuntungkanOleh ?gerak BIND("diuntungkan" AS ?arah) } UNION { ?e ex:ditekanOleh ?gerak BIND("ditekan" AS ?arah) } ?e ex:kodeSaham ?kode FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY ?arah ?kode""",
     jawab=lambda r: " · ".join(f"{d}: " + ", ".join(f"{x['kode']}({nm(x['gerak'])})" for x in r if x["arah"] == d) for d in dict.fromkeys(kol(r, "arah"))))
soal("G09", "Geopolitik & makro", "Indikator makro apa saja yang dipantau dan nilainya?",
     "DL Query: `IndikatorMakro`.",
     """SELECT ?i ?nilai ?satuan WHERE { ?i a ex:IndikatorMakro ; ex:nilaiIndikator ?nilai . OPTIONAL { ?i ex:satuan ?satuan } } ORDER BY ?i""",
     cek=minimal(15), jawab=baris(lambda x: f"{nm(x['i']).replace('Makro_','')} {f(x['nilai'])} {x['satuan'] or ''}".strip()))

# ================================================================== H. INDEKS
soal("H01", "Indeks", "Indeks apa saja yang tercakup (MSCI, LQ45, NASDAQ, FTSE, dll.)?",
     "DL Query: `IndeksSaham` dan subkelasnya (`IndeksMSCI`, `IndeksAmerika`, `IndeksDomestik`, ...).",
     """SELECT ?kategori (COUNT(?i) AS ?n) (GROUP_CONCAT(?id; separator=", ") AS ?indeks) WHERE { ?i a ?k . ?k rdfs:subClassOf+ ex:IndeksSaham .
 FILTER NOT EXISTS { ?k2 rdfs:subClassOf ?k . ?i a ?k2 . FILTER(?k2 != ?k) } BIND(STRAFTER(STR(?i),"#") AS ?id) BIND(STRAFTER(STR(?k),"#") AS ?kategori) } GROUP BY ?kategori ORDER BY ?kategori""",
     cek=lambda r: all(any(z in x["indeks"] for x in r) for z in ("LQ45", "MSCI_Indonesia", "NASDAQ")),
     jawab=baris(lambda x: f"{x['kategori']} ({x['n']}): {x['indeks']}"))
soal("H02", "Indeks", "Emiten mana saja anggota LQ45?",
     "DL Query: `Emiten and (anggotaIndeks value LQ45)`.",
     """SELECT ?kode WHERE { ?e ex:anggotaIndeks ex:LQ45 ; ex:kodeSaham ?kode } ORDER BY ?kode""",
     cek=minimal(20), jawab=daftar("kode"))
soal("H03", "Indeks", "Emiten mana anggota MSCI Indonesia dan mana yang berisiko outflow dana pasif (MSCI freeze/standalone)?",
     "DL Query: `Emiten and (anggotaIndeks value MSCI_Indonesia)` lalu `RisikoOutflowPasif` (SQWRL Q15).",
     """SELECT ?kode ?mcap ?outflow WHERE { ?e ex:anggotaIndeks ex:MSCI_Indonesia ; ex:kodeSaham ?kode ; ex:kapitalisasiPasarT ?mcap . BIND(EXISTS { ?e a ex:RisikoOutflowPasif } AS ?outflow) } ORDER BY DESC(?mcap)""",
     jawab=lambda r: f"({len(r)}) " + ", ".join(x["kode"] + ("⚠" if x["outflow"] == "true" else "") for x in r) + "  (⚠ = RisikoOutflowPasif)")
soal("H04", "Indeks", "Indeks syariah dan emiten syariah?",
     "DL Query: `IndeksSyariah`, `EmitenSyariah`.",
     """SELECT ?jenis (COUNT(?x) AS ?n) WHERE { { ?x a ex:IndeksSyariah BIND("IndeksSyariah" AS ?jenis) } UNION { ?x a ex:EmitenSyariah BIND("EmitenSyariah" AS ?jenis) } } GROUP BY ?jenis""",
     jawab=baris(lambda x: f"{x['jenis']}: {x['n']}"))
soal("H05", "Indeks", "Keputusan penyedia indeks apa yang memengaruhi pasar (MSCI review, freeze, FTSE, S&P)?",
     "DL Query: `KeputusanPenyediaIndeks`.",
     """SELECT ?ev ?label WHERE { ?ev a ex:KeputusanPenyediaIndeks ; rdfs:label ?label } ORDER BY ?ev""",
     jawab=baris(lambda x: x["label"]))

# ================================================================== I. PREDIKSI SEKTOR (keluaran utama)
soal("I01", "Prediksi sektor", "Sektor apa yang diprediksi naik dalam 1–3 tahun ke depan?",
     "DL Query: `SektorBullish` (dan `SektorBullishKuat`, `SektorBullishModerat`). SQWRL Q01/Q02.",
     """SELECT ?sektor ?prediksi ?skorAktif WHERE { ?s a ex:Sektor ; ex:skorOutlookAktif ?skorAktif ; a ?k . FILTER(?k IN (ex:SektorBullishKuat, ex:SektorBullishModerat, ex:SektorNetral, ex:SektorBearish))
 BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) BIND(STRAFTER(STR(?k),"Sektor") AS ?prediksi) } ORDER BY DESC(?skorAktif)""",
     cek=lambda r: any(x["prediksi"].startswith("Bullish") for x in r),
     jawab=lambda r: "NAIK: " + ", ".join(f"{x['sektor']} ({x['prediksi']}, skor {x['skorAktif']})" for x in r if x["prediksi"].startswith("Bullish"))
                     + " · lainnya: " + ", ".join(f"{x['sektor']} {x['prediksi']} ({x['skorAktif']})" for x in r if not x["prediksi"].startswith("Bullish")), cq="CQ1")
soal("I02", "Prediksi sektor", "Berapa skor sektor di tiap skenario (base, bull, bear) dan ekspektasi probabilistiknya?",
     "SQWRL Q23 / Q09. Atau individu `Penilaian_<Sektor>_<Skenario>` → `skorOutlook`.",
     """SELECT ?sektor ?base ?bull ?bear ?ekspektasi WHERE { ?s a ex:Sektor ; ex:skorOutlookBase ?base ; ex:skorOutlookBull ?bull ; ex:skorOutlookBear ?bear ; ex:skorEkspektasiProbabilistik ?ekspektasi
 BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } ORDER BY DESC(?ekspektasi)""",
     cek=minimal(11), jawab=baris(lambda x: f"{x['sektor']} B{x['base']}/U{x['bull']}/D{x['bear']} → E={f(x['ekspektasi'])}"))
soal("I03", "Prediksi sektor", "Sektor mana yang tahan di semua skenario (inti), satelit, dan peluang kontrarian?",
     "DL Query: `SektorPilihanInti`, `SektorPilihanSatelit`, `SektorPeluangKontrarian`, `SektorRobustLintasSkenario`.",
     """SELECT ?peran (GROUP_CONCAT(?sek; separator=", ") AS ?sektor) WHERE { ?s a ?k . FILTER(?k IN (ex:SektorPilihanInti, ex:SektorPilihanSatelit, ex:SektorPeluangKontrarian, ex:SektorRobustLintasSkenario, ex:SektorAsimetriPositif))
 BIND(STRAFTER(STR(?s),"Sektor_") AS ?sek) BIND(STRAFTER(STR(?k),"#") AS ?peran) } GROUP BY ?peran""",
     cek=lambda r: "SektorPilihanInti" in kol(r, "peran"), jawab=baris(lambda x: f"{x['peran']}: {x['sektor']}"), cq="CQ2")
soal("I04", "Prediksi sektor", "MENGAPA sektor terpilih diprediksi naik (jejak penjelasan tailwind/headwind/preseden)?",
     "Individu `Sektor_BarangBaku` → `memilikiTailwind`, `memilikiHeadwind`, `memilikiPreseden`. Klik **?** di sebelah aksioma kuning untuk *explanation* aturan.",
     """SELECT ?sektor ?jenis ?faktor WHERE { ?s a ex:SektorBullish . { ?s ex:memilikiTailwind ?faktor BIND("tailwind" AS ?jenis) } UNION { ?s ex:memilikiHeadwind ?faktor BIND("headwind" AS ?jenis) }
 UNION { ?s ex:memilikiPreseden ?faktor BIND("preseden" AS ?jenis) } UNION { ?s ex:didukungTema ?faktor BIND("tema" AS ?jenis) } BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } ORDER BY ?sektor ?jenis""",
     jawab=lambda r: " · ".join(f"{s}: " + "; ".join(f"{j} " + ", ".join(nm(x["faktor"]) for x in r if x["sektor"] == s and x["jenis"] == j)
                                                     for j in dict.fromkeys(x["jenis"] for x in r if x["sektor"] == s)) for s in dict.fromkeys(kol(r, "sektor"))), cq="CQ4")
soal("I05", "Prediksi sektor", "Periode sejarah mana yang paling mirip dengan kondisi sekarang (case-based reasoning)?",
     "SQWRL Q10: `PeriodeHistoris(?p) ^ skorKemiripan(?p, ?k) -> sqwrl:select(?p, ?k) ^ sqwrl:orderByDescending(?k)`; DL Query `PeriodeAnalog`.",
     """SELECT ?periode ?kemiripan ?analog WHERE { ?p a ex:PeriodeHistoris ; ex:skorKemiripan ?kemiripan . BIND(EXISTS { ?p a ex:PeriodeAnalog } AS ?analog) BIND(STRAFTER(STR(?p),"Kasus_") AS ?periode) } ORDER BY DESC(?kemiripan)""",
     cek=lambda r: any(x["analog"] == "true" for x in r), jawab=baris(lambda x: f"{x['periode']} {x['kemiripan']}/20" + (" ✔analog (≥13)" if x["analog"] == "true" else "")))
soal("I06", "Prediksi sektor", "Tema struktural jangka panjang apa yang mendukung sektor?",
     "DL Query: `TemaStruktural`; `SektorDidukungTema`.",
     """SELECT ?tema ?kekuatan ?sektor WHERE { ?t a ex:TemaStruktural . OPTIONAL { ?t ex:skorKekuatanTema ?kekuatan } OPTIONAL { ?s ex:didukungTema ?t BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } BIND(STRAFTER(STR(?t),"#") AS ?tema) } ORDER BY DESC(?kekuatan)""",
     jawab=lambda r: "; ".join(f"{t} ({next(x['kekuatan'] for x in r if x['tema']==t) or '-'}) → " + (", ".join(x["sektor"] for x in r if x["tema"] == t and x["sektor"]) or "-") for t in dict.fromkeys(kol(r, "tema"))))
soal("I07", "Prediksi sektor", "Fase siklus ekonomi apa yang berlaku dan sektor mana yang favorit di fase itu (rotasi sektor)?",
     "Individu `Skenario_Base_2027_2028` → `faseSiklus`; DL Query `SektorFavoritSiklus`.",
     """SELECT ?skenario ?fase ?favorit WHERE { ?sc a ex:SkenarioAktif ; ex:faseSiklus ?fase . OPTIONAL { ?s a ex:SektorFavoritSiklus BIND(STRAFTER(STR(?s),"Sektor_") AS ?favorit) } BIND(STRAFTER(STR(?sc),"Skenario_") AS ?skenario) }""",
     jawab=lambda r: f"skenario aktif {r[0]['skenario']}, fase {r[0]['fase']} → sektor favorit: " + ", ".join(x["favorit"] for x in r if x["favorit"]))
soal("I08", "Prediksi sektor", "Sektor mana yang murah secara historis, defensif, siklikal?",
     "DL Query: `SektorMurahHistoris`, `SektorDefensif`, `SektorSiklikal`.",
     """SELECT ?kelas (GROUP_CONCAT(?sek; separator=", ") AS ?sektor) WHERE { ?s a ?k . FILTER(?k IN (ex:SektorMurahHistoris, ex:SektorDefensif, ex:SektorSiklikal, ex:SektorKomoditas)) BIND(STRAFTER(STR(?s),"Sektor_") AS ?sek) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['sektor']}"))

# ================================================================== J. EMITEN
soal("J01", "Rekomendasi emiten", "Top-3 emiten per sektor pilihan (inti & satelit)?",
     "SQWRL Q03 (ganti nama sektor): `termasukSektor(?e, Sektor_BarangBaku) ^ skorAdaptifRegime(?e, ?t) -> sqwrl:select(?e, ?t) ^ sqwrl:orderByDescending(?t) ^ sqwrl:limit(3)`",
     """SELECT ?sektor ?kode ?skorAdaptif WHERE { ?s ex:kodeIndeksSektor ?kd . { ?s a ex:SektorPilihanInti } UNION { ?s a ex:SektorPilihanSatelit }
 ?e ex:termasukSektor ?s ; ex:kodeSaham ?kode ; ex:skorAdaptifRegime ?skorAdaptif . FILTER NOT EXISTS { ?e a ex:EmitenUji }
 { SELECT ?e (COUNT(?o) AS ?lebih) WHERE { ?e ex:termasukSektor ?s2 ; ex:skorAdaptifRegime ?sk . OPTIONAL { ?o ex:termasukSektor ?s2 ; ex:skorAdaptifRegime ?so . FILTER(?so > ?sk) FILTER NOT EXISTS { ?o a ex:EmitenUji } } } GROUP BY ?e }
 FILTER(?lebih < 3) BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } ORDER BY ?sektor DESC(?skorAdaptif)""",
     cek=minimal(6), jawab=lambda r: " · ".join(f"{s}: " + ", ".join(f"{x['kode']} ({f(x['skorAdaptif'])})" for x in r if x["sektor"] == s) for s in dict.fromkeys(kol(r, "sektor"))), cq="CQ3")
soal("J02", "Rekomendasi emiten", "Apa beda pilihan analis biasa (skor statis) dan sistem pakar (skor adaptif regime)?",
     "DL Query: `KandidatTopPick` vs `KandidatTopPickAdaptif`. SQWRL Q21.",
     """SELECT ?kode ?skorStatis ?skorAdaptif ?analisBiasa ?pakar WHERE { ?e ex:kodeSaham ?kode ; ex:skorTotalEmiten ?skorStatis ; ex:skorAdaptifRegime ?skorAdaptif .
 BIND(EXISTS { ?e a ex:KandidatTopPick } AS ?analisBiasa) BIND(EXISTS { ?e a ex:KandidatTopPickAdaptif } AS ?pakar) FILTER(?analisBiasa || ?pakar) } ORDER BY DESC(?skorAdaptif)""",
     jawab=lambda r: "Analis biasa: " + ", ".join(x["kode"] for x in r if x["analisBiasa"] == "true") + " · Pakar: " + ", ".join(x["kode"] for x in r if x["pakar"] == "true")
                     + " · Dibuang pakar: " + (", ".join(x["kode"] for x in r if x["analisBiasa"] == "true" and x["pakar"] == "false") or "-")
                     + " · Ditambah pakar: " + (", ".join(x["kode"] for x in r if x["analisBiasa"] == "false" and x["pakar"] == "true") or "-"), cq="CQ8")
soal("J03", "Rekomendasi emiten", "Mengapa BRMS tidak masuk top pick pakar padahal grafiknya paling kuat (outperform tertinggi)?",
     "Individu `BRMS` → bandingkan `skorTotalEmiten` vs `skorAdaptifRegime`, `pertumbuhanEPS`, kelas `RevisiLabaTurun`/`MomentumTanpaFundamental`.",
     """SELECT ?skorStatis ?skorAdaptif ?epsGrowth ?kelas WHERE { ex:BRMS ex:skorTotalEmiten ?skorStatis ; ex:skorAdaptifRegime ?skorAdaptif ; ex:pertumbuhanEPS ?epsGrowth ; a ?k .
 FILTER(?k IN (ex:MomentumTanpaFundamental, ex:RevisiLabaTurun, ex:FundamentalLemah, ex:FundamentalSedang, ex:Overvalued, ex:KonfluensiRendah, ex:TungguKonfirmasi, ex:KandidatTopPick)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) }""",
     jawab=lambda r: f"skor statis {r[0]['skorStatis']} vs adaptif {f(r[0]['skorAdaptif'])}; EPS growth {f(r[0]['epsGrowth'])}%; kelas: " + ", ".join(kol(r, "kelas")))
soal("J04", "Rekomendasi emiten", "Rincian skor multi-pilar emiten top pick (fundamental, valuasi, teknikal, bandar, sentimen, sektor, risiko, likuiditas)?",
     "SQWRL Q05 (ganti ANTM).",
     """SELECT ?kode ?fund ?val ?tek ?band ?sent ?sek ?risiko ?likuid ?total ?adaptif WHERE { ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode ; ex:skorFundamental ?fund ; ex:skorValuasi ?val ; ex:skorTeknikal ?tek ;
 ex:skorBandar ?band ; ex:skorSentimen ?sent ; ex:skorKontribusiSektor ?sek ; ex:penaltiRisiko ?risiko ; ex:poinLikuiditas ?likuid ; ex:skorTotalEmiten ?total ; ex:skorAdaptifRegime ?adaptif } ORDER BY DESC(?adaptif)""",
     jawab=baris(lambda x: f"{x['kode']}: F{x['fund']} V{x['val']} T{x['tek']} B{x['band']} S{x['sent']} Sek{x['sek']} R{x['risiko']} L{x['likuid']} = {x['total']} (adaptif {f(x['adaptif'])})"))
soal("J05", "Rekomendasi emiten", "Emiten dengan keyakinan tinggi dan watchlist?",
     "DL Query: `KeyakinanTinggi`, `KandidatWatchlist`.",
     """SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:KeyakinanTinggi, ex:KandidatWatchlist)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['emiten']}"))
soal("J06", "Rekomendasi emiten", "Berapa ukuran posisi maksimal per emiten top pick (manajemen risiko)?",
     "SQWRL Q20: `KandidatTopPickAdaptif(?e) ^ skorAdaptifRegime(?e, ?s) ^ ukuranPosisiMaksPersen(?e, ?p) -> sqwrl:select(?e, ?s, ?p)`",
     """SELECT ?kode ?posisiMaks ?atr WHERE { ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode ; ex:ukuranPosisiMaksPersen ?posisiMaks ; ex:atrPersen ?atr } ORDER BY DESC(?posisiMaks)""",
     jawab=baris(lambda x: f"{x['kode']} maks {float(x['posisiMaks']):.1f}% portofolio (ATR {f(x['atr'])}%)"))
soal("J07", "Rekomendasi emiten", "Apakah ada risiko konsentrasi (dua top pick dengan tema/komoditas sama)?",
     "DL Query: `RisikoKonsentrasiTema`; individu → `terkonsentrasiDengan`.",
     """SELECT ?a ?b WHERE { ?x ex:terkonsentrasiDengan ?y ; ex:kodeSaham ?a . ?y ex:kodeSaham ?b . FILTER(STR(?a) < STR(?b)) }""",
     jawab=baris(lambda x: f"{x['a']} ↔ {x['b']}"))

# ================================================================== K. META-PENALARAN v2 (pembeda pakar)
soal("K01", "Meta-penalaran", "Regime pasar apa yang sedang terjadi dan berapa skor stresnya?",
     "DL Query: `RegimeAktif`. SQWRL Q18.",
     """SELECT ?regime ?label ?stres ?cds ?drawdown ?breadth WHERE { ?k a ex:KondisiPasarAktif ; ex:regimeTerdeteksi ?r ; ex:skorStresPasar ?stres ; ex:cds5YBps ?cds ; ex:drawdownIHSGPersen ?drawdown ; ex:breadthPersenDiAtasMA200 ?breadth .
 ?r rdfs:label ?label BIND(STRAFTER(STR(?r),"Regime_") AS ?regime) }""",
     jawab=lambda r: f"{r[0]['label']} (stres {r[0]['stres']}/12; CDS {f(r[0]['cds'])} bps, drawdown IHSG {f(r[0]['drawdown'])}%, breadth {f(r[0]['breadth'])}%)", cq="CQ5")
soal("K02", "Meta-penalaran", "Bagaimana bobot pilar berubah menurut regime (adaptif)?",
     "SQWRL Q19; atau individu `Regime_*` → bobot*.",
     """SELECT ?regime ?aktif ?fund ?tek ?bandar ?smart ?risikoTrx ?ambang WHERE { ?r a ex:RegimePasar ; ex:bobotFundamental ?fund ; ex:bobotTeknikal ?tek ; ex:bobotBandar ?bandar ; ex:bobotSmartMoney ?smart ;
 ex:risikoPerTransaksiPersen ?risikoTrx ; ex:ambangTopPickAdaptif ?ambang . BIND(EXISTS { ?r a ex:RegimeAktif } AS ?aktif) BIND(STRAFTER(STR(?r),"Regime_") AS ?regime) } ORDER BY DESC(?aktif)""",
     cek=minimal(4), jawab=baris(lambda x: f"{x['regime']}{' (AKTIF)' if x['aktif']=='true' else ''}: F×{f(x['fund'])} T×{f(x['tek'])} B×{f(x['bandar'])} SM×{f(x['smart'])}, risiko/trx {f(x['risikoTrx'])}%, ambang {f(x['ambang'])}"))
soal("K03", "Meta-penalaran", "Reaksi kebijakan apa yang diantisipasi (reaction function BI/pemerintah)?",
     "DL Query: `AntisipasiTerpicu`. SQWRL Q25.",
     """SELECT ?antisipasi ?label ?mengaktifkan WHERE { ?a a ex:AntisipasiTerpicu ; rdfs:label ?label . OPTIONAL { ?a ex:antisipasiMengaktifkan ?mengaktifkan } BIND(STRAFTER(STR(?a),"Antisipasi_") AS ?antisipasi) }""",
     jawab=lambda r: "; ".join(f"{a} ({next(x['label'] for x in r if x['antisipasi']==a)}) → " + ", ".join(nm(x["mengaktifkan"] or "-") for x in r if x["antisipasi"] == a) for a in dict.fromkeys(kol(r, "antisipasi"))))
soal("K04", "Meta-penalaran", "Tesis investasi mana yang valid, rapuh, atau gugur (kill switch)?",
     "DL Query: `TesisValid`, `TesisRapuh`, `TesisGugur`, `TesisPerluDataBaru`. SQWRL Q26.",
     """SELECT ?tesis ?status WHERE { ?t a ex:TesisInvestasi ; a ?k . FILTER(?k IN (ex:TesisValid, ex:TesisRapuh, ex:TesisGugur, ex:TesisTerpicu, ex:TesisPerluDataBaru)) BIND(STRAFTER(STR(?t),"Tesis_") AS ?tesis) BIND(STRAFTER(STR(?k),"Tesis") AS ?status) } ORDER BY ?tesis""",
     jawab=lambda r: "; ".join(f"{t}: " + "/".join(x["status"] for x in r if x["tesis"] == t) for t in dict.fromkeys(kol(r, "tesis"))), cq="CQ10")
soal("K05", "Meta-penalaran", "Indikator kunci & ambang kill switch tiap tesis?",
     "Individu `Tesis_*` → `indikatorKunciTesis`, `ambangInvalidasiBawah/Atas`, `ambangPemicuBawah`.",
     """SELECT ?tesis ?indikator ?nilai ?invalidBawah ?invalidAtas WHERE { ?t a ex:TesisInvestasi ; ex:indikatorKunciTesis ?i . ?i ex:nilaiIndikator ?nilai .
 OPTIONAL { ?t ex:ambangInvalidasiBawah ?invalidBawah } OPTIONAL { ?t ex:ambangInvalidasiAtas ?invalidAtas } BIND(STRAFTER(STR(?t),"Tesis_") AS ?tesis) BIND(STRAFTER(STR(?i),"#") AS ?indikator) } ORDER BY ?tesis""",
     jawab=baris(lambda x: f"{x['tesis']}: {x['indikator'].replace('Makro_','')} = {f(x['nilai'])} → gugur bila " + " atau ".join(
         ([f"< {f(x['invalidBawah'])}"] if x['invalidBawah'] and float(x['invalidBawah']) > 0 else []) + ([f"> {f(x['invalidAtas'])}"] if x['invalidAtas'] and float(x['invalidAtas']) < 1e8 else []))))
soal("K06", "Meta-penalaran", "Katalis apa yang dekat (≤ 45 hari) dan emiten/sektor mana yang terdampak?",
     "DL Query: `KatalisDekat`. SQWRL Q27.",
     """SELECT ?katalis ?label ?hari ?emiten WHERE { ?k a ex:KatalisDekat ; rdfs:label ?label ; ex:hariMenujuKatalis ?hari . OPTIONAL { ?e ex:memilikiKatalisDekat ?k ; ex:kodeSaham ?emiten } BIND(STRAFTER(STR(?k),"K_") AS ?katalis) } ORDER BY ?hari""",
     jawab=lambda r: "; ".join(f"{next(x['label'] for x in r if x['katalis']==k)} ({next(x['hari'] for x in r if x['katalis']==k)} hari) → " + (", ".join(x["emiten"] for x in r if x["katalis"] == k and x["emiten"]) or "-") for k in dict.fromkeys(kol(r, "katalis"))))
soal("K07", "Meta-penalaran", "Emiten mana yang ERP-nya menarik vs obligasi negara (SBN), dan mana yang mahal vs obligasi?",
     "DL Query: `ERPSangatMenarik`, `ERPMenarik`, `MahalVsObligasi`. SQWRL Q29.",
     """SELECT ?kelas (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:ERPSangatMenarik, ex:ERPMenarik, ex:MahalVsObligasi)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']} ({x['n']}): {x['emiten']}"))
soal("K08", "Meta-penalaran", "Kapan & di harga berapa masuk bertahap (akumulasi 3 tranche)?",
     "DL Query: `KandidatAkumulasiBertahap`; cek `StrategiAkumulasiBertahap`, `KapitulasiPasar`. SQWRL Q22.",
     """SELECT ?kode ?t1 ?t2 ?t3 ?drawdown ?kapitulasi WHERE { ?k a ex:KondisiPasarAktif ; ex:drawdownIHSGPersen ?drawdown . BIND(EXISTS { ?k a ex:KapitulasiPasar } AS ?kapitulasi)
 OPTIONAL { ?e a ex:KandidatAkumulasiBertahap ; ex:kodeSaham ?kode ; ex:hargaTranche1 ?t1 ; ex:hargaTranche2 ?t2 ; ex:hargaTranche3 ?t3 } }""",
     jawab=lambda r: ("; ".join(f"{x['kode']}: T1 {f(x['t1'])}, T2 {f(x['t2'])}, T3 {f(x['t3'])}" for x in r if x["kode"])
                      or f"Belum ada: syarat kapitulasi pasar (drawdown IHSG ≤ −40% DAN hari crash ≤ −10% dalam sebulan) belum terpenuhi; drawdown saat ini {f(r[0]['drawdown'])}% (KapitulasiPasar = {r[0]['kapitulasi']}). Lihat uji what-if W04."), cq="CQ7")
soal("K09", "Meta-penalaran", "Apakah sinyal antar-pilar sejalan (konfluensi) atau bertentangan (perlu tunggu konfirmasi)?",
     "DL Query: `KonfluensiTinggi`, `TungguKonfirmasi`, `KonflikFundamentalVsBandar`. SQWRL Q28.",
     """SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:KonfluensiTinggi, ex:TungguKonfirmasi, ex:KonflikFundamentalVsBandar, ex:MomentumTanpaFundamental)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['emiten']}"))
soal("K10", "Meta-penalaran", "Revisi konsensus laba: siapa yang direvisi naik / turun dan apa artinya?",
     "DL Query: `RevisiLabaNaik`, `RevisiLabaTurun`, `CelahEkspektasiPositif`, `MurahKarenaLabaTurun`.",
     """SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:RevisiLabaNaik, ex:RevisiLabaTurun, ex:CelahEkspektasiPositif)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     jawab=baris(lambda x: f"{x['kelas']}: {x['emiten']}"))
soal("K11", "Meta-penalaran", "Apakah ada emiten yang kapitulasi (jual panik) atau berita baik yang sudah 'priced-in' (sell the news)?",
     "DL Query: `KapitulasiEmiten`, `SellTheNews`, `BreadthWashout`.",
     """SELECT ?kelas ?x WHERE { ?x a ?k . FILTER(?k IN (ex:KapitulasiEmiten, ex:SellTheNews, ex:BreadthWashout, ex:DasarBelumTerkonfirmasi)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas""",
     jawab=lambda r: " · ".join(f"{d}: " + ", ".join(nm(x["x"]) for x in r if x["kelas"] == d) for d in dict.fromkeys(kol(r, "kelas"))))

# ================================================================== L. STAKEHOLDER & PERSONA
soal("L01", "Stakeholder", "Siapa stakeholder sistem ini dan apa kebutuhannya?",
     "DL Query: `Stakeholder` (subkelas StakeholderUtama, StakeholderKandidat, Validator, RegulatorStakeholder, EndUser).",
     """SELECT ?peran ?s ?kebutuhan WHERE { ?s a ?k . FILTER(?k IN (ex:StakeholderUtama, ex:StakeholderKandidat, ex:Validator, ex:RegulatorStakeholder, ex:EndUser)) OPTIONAL { ?s ex:kebutuhanStakeholder ?kebutuhan }
 BIND(STRAFTER(STR(?k),"#") AS ?peran) } ORDER BY ?peran""",
     cek=minimal(10), jawab=baris(lambda x: f"{x['peran']}: {nm(x['s'])}" + (f" — {x['kebutuhan'][:70]}" if x['kebutuhan'] else "")))
soal("L02", "Stakeholder", "Saham apa yang direkomendasikan untuk tiap persona investor?",
     "SQWRL Q14: `direkomendasikanUntuk(?e, ?i) -> sqwrl:select(?i, ?e) ^ sqwrl:orderBy(?i)`",
     """SELECT ?persona (GROUP_CONCAT(?kode; separator=", ") AS ?saham) WHERE { ?e ex:direkomendasikanUntuk ?p ; ex:kodeSaham ?kode . FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?p),"Persona_") AS ?persona) } GROUP BY ?persona""",
     cek=minimal(3), jawab=baris(lambda x: f"{x['persona']}: {x['saham']}"), cq="CQ11")
soal("L03", "Stakeholder", "Profil risiko, horizon, dan modal tiap persona?",
     "Individu `Persona_*` → `memilikiProfilRisiko`, `memilikiHorizon`, `modalAwalJuta`.",
     """SELECT ?persona ?profil ?horizon ?modal WHERE { ?p a ex:EndUser . OPTIONAL { ?p ex:memilikiProfilRisiko ?profil } OPTIONAL { ?p ex:memilikiHorizon ?horizon } OPTIONAL { ?p ex:modalAwalJuta ?modal } BIND(STRAFTER(STR(?p),"Persona_") AS ?persona) }""",
     jawab=baris(lambda x: f"{x['persona']}: {x['profil'] or '-'}, {x['horizon'] or '-'}, modal Rp{f(x['modal'])} jt"))

# ================================================================== M. SUMBER & KUALITAS DATA
soal("M01", "Kualitas data", "Data apa yang sudah kedaluwarsa dan perlu diperbarui?",
     "DL Query: `DataKedaluwarsa`. SQWRL Q31.",
     """SELECT ?item ?umurHari WHERE { ?i a ex:DataKedaluwarsa . OPTIONAL { ?i ex:umurDataHari ?umurHari } BIND(STRAFTER(STR(?i),"#") AS ?item) } ORDER BY DESC(?umurHari)""",
     cek=lambda r: True, jawab=lambda r: "; ".join(f"{x['item']} ({x['umurHari'] or '?'} hari)" for x in r) or "tidak ada")
soal("M02", "Kualitas data", "Emiten mana yang datanya masih perlu diverifikasi (data indikatif)?",
     "DL Query: `PerluVerifikasiData`, `DataIndikatif`.",
     """SELECT ?kelas (COUNT(?e) AS ?n) WHERE { ?e a ?k . FILTER(?k IN (ex:PerluVerifikasiData, ex:DataIndikatif)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas""",
     cek=lambda r: True, jawab=baris(lambda x: f"{x['kelas']}: {x['n']} emiten"))
soal("M03", "Kualitas data", "Dari mana sumber data KB dan indikator mana yang bersifat leading?",
     "DL Query: `SumberData`, `IndikatorLeading`. SQWRL Q32.",
     """SELECT ?jenis (COUNT(?s) AS ?n) WHERE { ?s a ?k . FILTER(?k IN (ex:SumberDataResmi, ex:SumberDataPasar, ex:SumberDataBerita, ex:SumberDataAlternatif, ex:IndikatorLeading, ex:IndikatorCoincident, ex:IndikatorLagging)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } GROUP BY ?jenis""",
     jawab=baris(lambda x: f"{x['jenis']}: {x['n']}"))


# ================================================================== EKSEKUSI
def baca_validasi():
    p = os.path.join(OUT, "validasi_owlapi_pellet.txt"); d = {}
    for ln in open(p, encoding="utf-8"):
        for kv in ln.split():
            if "=" in kv and not kv.startswith("["):
                k, v = kv.split("=", 1); d[k] = v
    return d


def jalankan_sparql():
    jars = sorted(glob.glob(os.path.join(HERE, "lib", "owlready2", "pellet", "*.jar")))
    cp = os.pathsep.join(jars + [os.path.join(HERE, "tools", "java")])
    java = shutil.which("java") or sys.exit("Java tidak ditemukan.")
    if not os.path.exists(os.path.join(HERE, "tools", "java", "Sparql.class")):
        subprocess.run([shutil.which("javac") or "javac", "-nowarn", "-cp", cp, "-d", os.path.join(HERE, "tools", "java"),
                        os.path.join(HERE, "tools", "java", "Sparql.java")], check=True)
    os.makedirs(os.path.join(OUT, "uji_kb"), exist_ok=True)
    qf = os.path.join(OUT, "uji_kb", "queries_uji.rq")
    with open(qf, "w", encoding="utf-8") as fh:
        fh.write("# Semua query uji SahamExpertKB (tools/uji_kb.py). Di Fuseki: tempel bagian setelah baris '### ID'.\n")
        for t in T:
            if not t["sparql"].startswith("#FILE"):
                fh.write(f"### {t['id']}\n# {t['tanya']}\n{PFX}{t['sparql']}\n\n")
    r = subprocess.run([java, "-Xmx2g", "-cp", cp, "Sparql", INF, qf], capture_output=True, text=True, encoding="utf-8")
    hasil, cur, head = {}, None, None
    for ln in r.stdout.splitlines():
        if ln.startswith("### "): cur = ln[4:].strip(); hasil[cur] = []; head = None; continue
        if cur is None: continue
        cols = ln.split("\t")
        if head is None: head = cols; continue
        if cols[0] == "!ERROR": hasil[cur] = "ERROR: " + "\t".join(cols[1:]); continue
        hasil[cur].append(dict(zip(head, cols + [""] * (len(head) - len(cols)))))
    return hasil


# ------------------------------------------------------------------ uji what-if dinamis (Pellet ulang)
WHATIF = [
    ("W01", "What-if skenario", "Jika skenario BULL (pemulihan) yang aktif, sektor apa yang naik?",
     "Individu `Skenario_Base_2027_2028`: ubah `statusAktif` 1 → 0; `Skenario_Bull_Pemulihan`: 0 → 1. Jalankan ulang Pellet (Reasoner › Synchronize).",
     {"Skenario_Base_2027_2028": ("statusAktif", 0), "Skenario_Bull_Pemulihan": ("statusAktif", 1)}, "sektor"),
    ("W02", "What-if skenario", "Jika skenario BEAR (stagflasi) yang aktif, sektor apa yang bertahan?",
     "`Skenario_Base_2027_2028.statusAktif` = 0, `Skenario_Bear_Stagflasi.statusAktif` = 1, lalu Synchronize reasoner.",
     {"Skenario_Base_2027_2028": ("statusAktif", 0), "Skenario_Bear_Stagflasi": ("statusAktif", 1)}, "sektor"),
    ("W03", "What-if data emiten", "Jika ANTM tiba-tiba punya Altman Z = 1,2 dan DER = 3,5, apakah sistem langsung menandainya berisiko & mencoretnya?",
     "Individu `ANTM`: ubah `altmanZ` 4.5 → 1.2 dan `der` 0.3 → 3.5 (hapus nilai lama, tambah baru). Synchronize. Cek tipe ANTM.",
     {"ANTM": [("altmanZ", 1.2), ("der", 3.5)]}, "antm"),
    ("W04", "What-if pasar", "Jika IHSG kapitulasi (drawdown −45% dan ada hari crash −10,5% dalam sebulan), apakah strategi akumulasi bertahap aktif dan berapa harga tranche-nya?",
     "Individu `Pasar_ID_Okt2026`: ubah `drawdownIHSGPersen` → −45 dan `penurunanHarianTerbesarPersen` → −10.5 (syarat R-PAS-03: keduanya harus terpenuhi). Synchronize. DL Query `KapitulasiPasar`, `KandidatAkumulasiBertahap`.",
     {"Pasar_ID_Okt2026": [("drawdownIHSGPersen", -45.0), ("penurunanHarianTerbesarPersen", -10.5)]}, "tranche"),
    ("W05", "What-if pasar", "Jika premi risiko negara membaik (CDS turun ke 75 bps, CDS & rupiah membaik), apa yang berubah?",
     "Individu `Pasar_ID_Okt2026`: `cds5YBps` = 75, `trenCDS1Bulan` = −1, `trenRupiah1Bulan` = −1; individu `Makro_CDS5Y` `nilaiIndikator` = 75. Synchronize.",
     {"Pasar_ID_Okt2026": [("cds5YBps", 75.0), ("trenCDS1Bulan", -1), ("trenRupiah1Bulan", -1)], "Makro_CDS5Y": ("nilaiIndikator", 75.0)}, "cds"),
]


def uji_whatif():
    code = r'''
import sys, json
sys.path.insert(0, sys.argv[1] + "/lib")
from owlready2 import *
w = World(); o = w.get_ontology(sys.argv[1] + "/output/SahamExpertKB_v2.owl").load()
ns = o.get_namespace("http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#")
ubah, mode = json.loads(sys.argv[2]), sys.argv[3]
for ind, perub in ubah.items():
    for prop, nilai in (perub if isinstance(perub[0], list) else [perub]):
        setattr(ns[ind], prop, [nilai])
with o: sync_reasoner_pellet(w, infer_property_values=True, infer_data_property_values=True, debug=0)
inst = lambda c: sorted(i.name for i in ns[c].instances())
out = {}
if mode == "sektor":
    for c in ["SektorBullishKuat", "SektorBullishModerat", "SektorNetral", "SektorBearish", "SektorPilihanInti"]: out[c] = inst(c)
    out["skor"] = {s.name.replace("Sektor_", ""): (s.skorOutlookAktif or [None])[0] for s in ns.Sektor.instances()}
elif mode == "antm":
    out["kelasANTM"] = sorted(c.name for c in ns.ANTM.is_a if c.name in ("RisikoGoingConcern", "ZonaDistress", "ZonaAman", "ZonaAbuAbu", "KandidatTopPick", "KandidatTopPickAdaptif", "FundamentalKuat", "FundamentalSedang", "FundamentalLemah"))
    out["skorTotal"] = (ns.ANTM.skorTotalEmiten or [None])[0]; out["penaltiRisiko"] = (ns.ANTM.penaltiRisiko or [None])[0]
    out["topPickAdaptif"] = inst("KandidatTopPickAdaptif")
elif mode == "tranche":
    out["KapitulasiPasar"] = inst("KapitulasiPasar"); out["StrategiAkumulasiBertahap"] = inst("StrategiAkumulasiBertahap")
    out["tranche"] = {e.name: [(e.hargaTranche1 or [None])[0], (e.hargaTranche2 or [None])[0], (e.hargaTranche3 or [None])[0]] for e in ns.KandidatAkumulasiBertahap.instances()}
elif mode == "cds":
    k = ns.Pasar_ID_Okt2026
    out["skorStres"] = (k.skorStresPasar or [None])[0]; out["regime"] = [r.name for r in k.regimeTerdeteksi] if hasattr(k.regimeTerdeteksi, "__iter__") else [k.regimeTerdeteksi.name]
    out["DivergensiIntermarketBullish"] = inst("DivergensiIntermarketBullish"); out["TesisTerpicu"] = inst("TesisTerpicu"); out["PremiRisikoNegaraTinggi"] = inst("PremiRisikoNegaraTinggi")
print("@@" + json.dumps(out, default=str))
'''
    tmp = os.path.join(OUT, "uji_kb", "_whatif_runner.py"); open(tmp, "w", encoding="utf-8").write(code)
    env = dict(os.environ, PYTHONPATH=os.path.join(HERE, "lib"), PYTHONIOENCODING="utf-8")
    hasil = []
    for (id, modul, tanya, protege, ubah, mode) in WHATIF:
        r = subprocess.run([sys.executable, "-W", "ignore", tmp, HERE, json.dumps(ubah), mode], capture_output=True, text=True, env=env, encoding="utf-8")
        m = [ln for ln in r.stdout.splitlines() if ln.startswith("@@")]
        d = json.loads(m[0][2:]) if m else {"error": r.stderr[-400:]}
        if mode == "sektor":
            ok = "error" not in d and len(d["SektorBullishKuat"] + d["SektorBullishModerat"] + d["SektorNetral"] + d["SektorBearish"]) == 11
            jaw = ("Bullish kuat: " + (", ".join(nm(x) for x in d["SektorBullishKuat"]) or "-") + " · Bullish moderat: " + (", ".join(nm(x) for x in d["SektorBullishModerat"]) or "-")
                   + " · Netral: " + (", ".join(nm(x) for x in d["SektorNetral"]) or "-") + " · Bearish: " + (", ".join(nm(x) for x in d["SektorBearish"]) or "-")) if ok else str(d)
        elif mode == "antm":
            ok = "error" not in d and "RisikoGoingConcern" in d["kelasANTM"] and "ANTM" not in d["topPickAdaptif"]
            jaw = f"Kelas ANTM: {', '.join(d.get('kelasANTM', []))}; penalti risiko {d.get('penaltiRisiko')}, skor total {d.get('skorTotal')}; ANTM {'TIDAK lagi' if ok else 'masih'} top pick pakar" if "error" not in d else str(d)
        elif mode == "tranche":
            ok = "error" not in d and bool(d["KapitulasiPasar"]) and bool(d["tranche"])
            jaw = (f"KapitulasiPasar: {', '.join(d['KapitulasiPasar']) or '-'}; StrategiAkumulasiBertahap: {', '.join(d['StrategiAkumulasiBertahap']) or '-'}; "
                   + "; ".join(f"{k}: T1 {v[0]}, T2 {v[1]}, T3 {v[2]}" for k, v in sorted(d["tranche"].items()))) if "error" not in d else str(d)
        else:
            ok = "error" not in d and d["skorStres"] is not None and int(d["skorStres"]) < 11
            jaw = (f"skor stres {d['skorStres']} (sebelumnya 11), regime {', '.join(d['regime'])}; DivergensiIntermarketBullish: {', '.join(d['DivergensiIntermarketBullish']) or '-'}; "
                   f"TesisTerpicu: {', '.join(d['TesisTerpicu']) or '-'}; PremiRisikoNegaraTinggi: {', '.join(d['PremiRisikoNegaraTinggi']) or 'hilang'}") if "error" not in d else str(d)
        hasil.append(dict(id=id, modul=modul, tanya=tanya, protege=protege, sparql="(what-if: ubah data → Pellet ulang)", lulus=ok, jawaban=jaw, cq=None))
        print(f"  {id} {'LULUS' if ok else 'GAGAL'}", flush=True)
    os.remove(tmp)
    return hasil


def main():
    val = baca_validasi()
    sp = jalankan_sparql()
    total, rules = int(val.get("TOTAL_AXIOMS", 0)), int(val.get("SWRL_RULES", 0))
    file_rows = {
        "CONSISTENT": [{"nilai": val.get("CONSISTENT", "?")}],
        "METRIK": [{k: val.get(k, "?") for k in ("CLASSES", "OBJECT_PROPERTIES", "DATA_PROPERTIES", "INDIVIDUALS", "SWRL_RULES", "TOTAL_AXIOMS")}],
        "RASIO": [{"persen": f"{100 * (total - rules) / total:.1f}" if total else "0", "total": str(total), "aturan": str(rules)}],
    }
    hasil = []
    for t in T:
        rows = file_rows[t["sparql"].split()[-1]] if t["sparql"].startswith("#FILE") else sp.get(t["id"], "ERROR: tidak dijalankan")
        if isinstance(rows, str): ok, jaw = False, rows
        else:
            try: ok = bool(t["cek"](rows))
            except Exception as e: ok = False
            try: jaw = t["jawab"](rows) if t["jawab"] else daftar(list(rows[0].keys())[0])(rows)
            except Exception as e: jaw = f"(format jawaban gagal: {e}) {rows[:3]}"
        hasil.append(dict(id=t["id"], modul=t["modul"], tanya=t["tanya"], protege=t["protege"], sparql=t["sparql"], lulus=ok, jawaban=jaw, cq=t["cq"]))
    print(f"Uji statis: {sum(h['lulus'] for h in hasil)}/{len(hasil)} lulus")
    for h in hasil:
        if not h["lulus"]: print("  GAGAL", h["id"], h["jawaban"][:200])
    if "--whatif" in sys.argv:
        print("Uji what-if (Pellet dijalankan ulang per skenario):")
        hasil += uji_whatif()

    lulus = sum(h["lulus"] for h in hasil)
    tgl = open(os.path.join(HERE, "data", "tanggal_acuan.txt"), encoding="utf-8").read().strip()
    L = ["# Hasil Uji Knowledge Base — SahamExpertKB v2", "",
         f"Tanggal acuan data: **{tgl}** · Sumber: `output/SahamExpertKB_v2_inferred.owl` (hasil Pellet) · Dijalankan dengan `python3 tools/uji_kb.py{' --whatif' if '--whatif' in sys.argv else ''}`", "",
         f"## Ringkasan: **{lulus}/{len(hasil)} soal lulus**", "", "| Modul | Lulus |", "|---|---|"]
    for m in dict.fromkeys(h["modul"] for h in hasil):
        hs = [h for h in hasil if h["modul"] == m]; L.append(f"| {m} | {sum(h['lulus'] for h in hs)}/{len(hs)} |")
    L += ["", "Pemetaan 12 competency questions (CQ) proposal → soal uji: " + ", ".join(f"{h['cq']} = {h['id']}" for h in sorted([h for h in hasil if h["cq"]], key=lambda h: int(h["cq"][2:]))), ""]
    for m in dict.fromkeys(h["modul"] for h in hasil):
        L += [f"## {m}", ""]
        for h in [h for h in hasil if h["modul"] == m]:
            L += [f"### {h['id']} — {h['tanya']}" + (f"  *({h['cq']})*" if h["cq"] else ""), "",
                  f"- **Status:** {'✔ LULUS' if h['lulus'] else '✘ GAGAL'}",
                  f"- **Cara uji di Protégé:** {h['protege']}",
                  f"- **Jawaban KB:** {h['jawaban']}", ""]
            if not h["sparql"].startswith(("#FILE", "(what-if")):
                L += ["<details><summary>SPARQL</summary>", "", "```sparql", h["sparql"], "```", "</details>", ""]
    open(os.path.join(OUT, "HASIL_UJI_KB.md"), "w", encoding="utf-8").write("\n".join(L))
    json.dump(hasil, open(os.path.join(OUT, "uji_kb", "hasil_uji_kb.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"TOTAL: {lulus}/{len(hasil)} lulus -> output/HASIL_UJI_KB.md")
    sys.exit(0 if lulus == len(hasil) else 1)


if __name__ == "__main__":
    main()
