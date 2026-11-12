# -*- coding: utf-8 -*-
"""
Builder Ontologi: Sistem Pakar Prediksi Sektor Saham BEI (Kelompok 9 KBR)
Integrasi Fundamental + Teknikal + Bandarmology + Sentimen + Geopolitik/Makro + CBR, berbasis SWRL.

Jalankan:  PYTHONPATH=lib python3 build_ontology.py [--reason]
Keluaran:  output/SahamExpertKB_v2.owl         (asserted: TBox + ABox + SWRL)
           output/SahamExpertKB_v2_inferred.owl (dibuat run_all.sh via OWLAPI+Pellet)
           output/hasil_inferensi.json                                              [--reason]
"""
import sys, os, types, json, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import warnings; warnings.filterwarnings("ignore")
from owlready2 import *
import owlready2

from kb_taxonomy import TAXONOMY, DISJOINT
from kb_concepts import C as CONCEPTS
import kb_market as M
import kb_geo as G
import kb_v2 as V2
import kb_sources as SRC
from sentiment_scorer import score_all
from rules_swrl import build_rules

IRI = "http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#"
OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

world = World()
onto = world.get_ontology(IRI[:-1])

def L(x):
    return locstr(x, lang="id")

with onto:
    # ------------------------------------------------------------ ANOTASI
    class rumus(AnnotationProperty): pass
    class interpretasi(AnnotationProperty): pass
    class ambangBatas(AnnotationProperty): pass
    class contohPenerapan(AnnotationProperty): pass
    class heuristikPakar(AnnotationProperty): pass
    class sumberReferensi(AnnotationProperty): pass
    class kodeAturan(AnnotationProperty): pass
    class pilarAnalisis(AnnotationProperty): pass
    class lapisanPengetahuan(AnnotationProperty): pass
    class catatanData(AnnotationProperty): pass

    onto.metadata.comment = [L(
        "Knowledge Base Sistem Pakar Prediksi Sektor Saham Unggulan & Kesehatan Fundamental Emiten BEI (horizon 1-3 tahun). "
        "Integrasi analisis Fundamental, Teknikal, Bandarmology, Sentimen (aspect-based), Geopolitik-Makro multi-hop, "
        "Case-Based Reasoning historis, dan rotasi siklus sektor. Penalaran dengan SWRL (jalankan Pellet / SWRLTab-Drools). "
        "Kelompok 9: Jonnathan Azarel Gunawan (L0224005), Gloria Dana Praysilia (L0224043). Tanggal acuan data: " + str(G.TODAY) + ". v2: lapisan sumber data & katalog indikator, deteksi regime + bobot adaptif, reaction function kebijakan, refleksivitas (priced-in), kapitulasi & akumulasi bertahap, revisi laba, ERP, tata kelola/gorengan, robustness skenario, konfluensi/konflik, sizing, katalis, tesis & kill switch.")]
    onto.metadata.label = [L("SahamExpertKB - Ontologi Pakar Saham Indonesia")]
    onto.metadata.versionInfo = [f"2.1 ({G.TODAY})"]

    # ------------------------------------------------------------ KELAS
    CLS = {}
    for line in TAXONOMY.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, parent, label, comment = [x.strip() for x in line.split("|", 3)]
        par = Thing if parent == "Thing" else CLS[parent]
        c = types.new_class(name, (par,))
        c.label = [L(label)]
        c.comment = [L(comment)]
        CLS[name] = c
    for line in V2.TAXONOMY_V2.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, parent, label, comment = [x.strip() for x in line.split("|", 3)]
        par = Thing if parent == "Thing" else CLS[parent]
        c = types.new_class(name, (par,))
        c.label = [L(label)]; c.comment = [L(comment)]
        CLS[name] = c
    for group in DISJOINT + [["RegimeAktif", "KondisiPasar"], ["TesisValid", "TesisGugur"], ["KatalisBiner", "KatalisMusiman", "KatalisTerjadwal"]]:
        AllDisjoint([CLS[g] for g in group])
    # lapisan pengetahuan
    for n in ["PengetahuanDasarSaham", "AnalisisFundamental", "AnalisisTeknikal"]:
        CLS[n].lapisanPengetahuan = ["Basic Layer"]
    for n in ["Bandarmology", "AnalisisSentimen", "AnalisisGeopolitikMakro", "PenalaranPakar"]:
        CLS[n].lapisanPengetahuan = ["Expert Layer (inti 80% knowledge-based)"]
    CLS["KomponenML"].lapisanPengetahuan = ["Komponen ML pendukung (<20%)"]

    # ------------------------------------------------------------ OBJECT PROPERTIES
    OP = {}
    def op(name, dom, rng, label, comment="", functional=False, symmetric=False, transitive=False, inverse=None):
        bases = [ObjectProperty]
        if functional: bases.append(FunctionalProperty)
        if symmetric: bases.append(SymmetricProperty)
        if transitive: bases.append(TransitiveProperty)
        p = types.new_class(name, tuple(bases))
        if dom: p.domain = [CLS[dom]]
        if rng: p.range = [CLS[rng]]
        p.label = [L(label)]
        if comment: p.comment = [L(comment)]
        if inverse: p.inverse_property = OP[inverse]
        OP[name] = p
        return p

    op("termasukSektor", "Emiten", "Sektor", "termasuk sektor", "Emiten termasuk ke dalam sektor IDX-IC.", functional=True)
    op("termasukSubsektor", "Emiten", "Subsektor", "termasuk subsektor", functional=True)
    op("bagianDariSektor", "Subsektor", "Sektor", "bagian dari sektor", functional=True)
    op("anggotaIndeks", "Emiten", "IndeksSaham", "anggota indeks", "Emiten adalah konstituen indeks (indikatif, verifikasi ke penyedia indeks).")
    op("memilikiKonstituen", "IndeksSaham", "Emiten", "memiliki konstituen", inverse="anggotaIndeks")
    op("bagianDariGrup", "Emiten", "KonglomerasiGrup", "bagian dari grup")
    op("diterbitkanOleh", "IndeksSaham", "PenyediaIndeks", "diterbitkan oleh")
    op("memengaruhiIndeks", "IndeksSaham", "IndeksSaham", "memengaruhi indeks", "Korelasi/transmisi sentimen antar-indeks (mis. NASDAQ → IDXTECHNO).")
    op("memilikiIndeksSektoral", "Sektor", "IndeksSektoralBEI", "memiliki indeks sektoral")
    op("pesaingDari", "Emiten", "Emiten", "pesaing dari", symmetric=True)
    op("eksposurKomoditasPendapatan", "Emiten", "Komoditas", "eksposur komoditas (pendapatan)", "Pendapatan emiten naik bila harga komoditas ini naik.")
    op("eksposurKomoditasBiaya", "Emiten", "Komoditas", "eksposur komoditas (biaya)", "Biaya emiten naik bila harga komoditas ini naik.")
    op("terdeteksiPola", "Emiten", None, "terdeteksi pola", "Output detektor pola (komponen ML) - pola chart/candlestick/bandar.")
    op("brokerAkumulatorUtama", "Emiten", "Broker", "broker akumulator utama", "Top net buyer 20 hari (indikatif).")
    op("brokerDistributorUtama", "Emiten", "Broker", "broker distributor utama", "Top net seller 20 hari (indikatif).")
    op("tentangPeristiwa", "Berita", "PeristiwaGeopolitik", "tentang peristiwa")
    op("tentangSektor", "Berita", "Sektor", "tentang sektor")
    op("tentangEmiten", "Berita", "Emiten", "tentang emiten")
    op("dariSumber", "Berita", "SumberSentimen", "dari sumber")
    op("memicuPergerakan", "PeristiwaGeopolitik", "PergerakanMakro", "memicu pergerakan", "Peristiwa memicu node transmisi makro (hop pertama).")
    op("menyebabkan", "PergerakanMakro", "PergerakanMakro", "menyebabkan", "Relasi kausal antar node transmisi (multi-hop).")
    op("menguntungkanSektor", "PergerakanMakro", "Sektor", "menguntungkan sektor")
    op("merugikanSektor", "PergerakanMakro", "Sektor", "merugikan sektor")
    op("menciptakanPeluangKontrarian", "PergerakanMakro", "Sektor", "menciptakan peluang kontrarian")
    op("menaikkanHargaKomoditas", "PergerakanMakro", "Komoditas", "menaikkan harga komoditas")
    op("menurunkanHargaKomoditas", "PergerakanMakro", "Komoditas", "menurunkan harga komoditas")
    op("berdampakPadaIndeks", "PeristiwaGeopolitik", "IndeksSaham", "berdampak pada indeks")
    op("diputuskanOleh", "PeristiwaGeopolitik", "Institusi", "diputuskan oleh")
    op("dirilisOleh", "IndikatorMakro", "Institusi", "dirilis oleh")
    op("memilikiTailwind", "Sektor", "PergerakanMakro", "memiliki tailwind (alasan positif)", "INFERENSI: node makro aktif yang menguntungkan sektor.")
    op("memilikiHeadwind", "Sektor", "PergerakanMakro", "memiliki headwind (alasan negatif)", "INFERENSI: node makro aktif yang merugikan sektor.")
    op("memilikiPeluangKontrarian", "Sektor", "PergerakanMakro", "memiliki peluang kontrarian", "INFERENSI.")
    op("diuntungkanOleh", "Emiten", "PergerakanMakro", "diuntungkan oleh", "INFERENSI: routing geopolitik ke emiten via eksposur komoditas.")
    op("ditekanOleh", "Emiten", "PergerakanMakro", "ditekan oleh", "INFERENSI.")
    op("memilikiRedFlag", "Emiten", "Berita", "memiliki red flag", "INFERENSI.")
    op("didukungTema", "Sektor", "TemaStruktural", "didukung tema struktural")
    op("disukaiPadaFase", "Sektor", "FaseSiklusEkonomi", "disukai pada fase siklus")
    op("menilaiSektor", "PenilaianSektor", "Sektor", "menilai sektor", functional=True)
    op("dibawahSkenario", "PenilaianSektor", "Skenario", "di bawah skenario", functional=True)
    op("faseSiklus", "Skenario", "FaseSiklusEkonomi", "fase siklus", functional=True)
    op("analogDengan", "Skenario", "PeriodeHistoris", "analog dengan (CBR)", "INFERENSI: periode historis mirip skenario aktif.")
    op("unggulPadaPeriode", "PeriodeHistoris", "Sektor", "sektor unggul pada periode")
    op("terpurukPadaPeriode", "PeriodeHistoris", "Sektor", "sektor terpuruk pada periode")
    op("memilikiPreseden", "Sektor", "PeriodeHistoris", "memiliki preseden historis", "INFERENSI.")
    op("topPickSektor", "Sektor", "Emiten", "top pick sektor", "INFERENSI: kandidat top pick di sektor bullish.")
    op("watchlistSektor", "Sektor", "Emiten", "watchlist sektor", "INFERENSI.")
    op("memilikiProfilRisiko", "InvestorRitel", "ProfilRisiko", "memiliki profil risiko", functional=True)
    op("memilikiHorizon", "InvestorRitel", "HorizonInvestasi", "memiliki horizon", functional=True)
    op("direkomendasikanUntuk", "Emiten", "InvestorRitel", "direkomendasikan untuk", "INFERENSI: kecocokan emiten dengan persona.")
    op("mengonsumsiKeluaran", "Stakeholder", "KeluaranSistem", "mengonsumsi keluaran")
    op("mendukungSDG", "KeluaranSistem", "TujuanSDG", "mendukung SDG")
    op("mengawasi", "Institusi", None, "mengawasi")
    op("heuristikDigunakanOleh", "AturanPakar", "KeluaranSistem", "heuristik digunakan oleh")

    # ------------------------------------------------------------ DATA PROPERTIES
    DP = {}
    def dp(name, dom, rng, label, comment="", functional=False):
        bases = [DataProperty] + ([FunctionalProperty] if functional else [])
        p = types.new_class(name, tuple(bases))
        if dom: p.domain = [CLS[dom]]
        p.range = [rng]
        p.label = [L(label)]
        if comment: p.comment = [L(comment)]
        DP[name] = p
        return p
    # emiten - identitas & fundamental
    for n, rng, l in [("kodeSaham", str, "kode saham"), ("namaPerusahaan", str, "nama perusahaan")]:
        dp(n, "Emiten", rng, l)
    for n, l in [("hargaPenutupan", "harga penutupan (Rp, indikatif)"), ("kapitalisasiPasarT", "kapitalisasi pasar (Rp triliun)"),
                 ("likuiditasHarianM", "nilai transaksi harian rata-rata (Rp miliar)"), ("freeFloatPersen", "free float (%)"),
                 ("per", "PER (x)"), ("per5Tahun", "rata-rata PER 5 tahun (x)"), ("pbv", "PBV (x)"), ("roe", "ROE (%)"),
                 ("der", "DER (x)"), ("npm", "NPM (%)"), ("pertumbuhanEPS", "pertumbuhan EPS yoy (%)"),
                 ("cfoPerLabaBersih", "CFO / laba bersih (x)"), ("npl", "NPL gross (%)"), ("nim", "NIM (%)"), ("car", "CAR (%)"),
                 ("dividendYield", "dividend yield (%)"), ("dpr", "dividend payout ratio (%)"), ("altmanZ", "Altman Z-Score"),
                 ("beneishM", "Beneish M-Score"), ("jarakMA50Persen", "jarak harga ke MA50 (%)"), ("jarakMA200Persen", "jarak harga ke MA200 (%)"),
                 ("selisihMA50MA200Persen", "selisih MA50 vs MA200 (%)"), ("rsi14", "RSI 14"), ("rasioVolume", "volume / rata-rata 20 hari"),
                 ("atrPersen", "ATR 14 (% harga)"), ("skorAccDistBroker", "skor Acc/Dist broker (-100..100)"),
                 ("netAsing20HariM", "net foreign 20 hari (Rp miliar)"), ("netRitel20HariM", "net broker ritel 20 hari (Rp miliar)"),
                 ("perubahanHarga20HariPersen", "perubahan harga 20 hari (%)"), ("jarakVWAPPersen", "jarak ke VWAP intraday (%)"),
                 ("rasioBidOffer", "rasio volume bid/offer"), ("skorSentimenEmiten", "skor sentimen emiten (-1..1, output scorer)")]:
        dp(n, "Emiten", float, l)
    dp("histogramMACD", "Emiten", int, "arah histogram MACD (+1/-1)")
    dp("jumlahBeritaRelevan", "Emiten", int, "jumlah berita relevan")
    # emiten - hasil inferensi
    for n, l in [("poinROE", "poin ROE"), ("poinSolvabilitas", "poin solvabilitas (DER/NPL)"), ("poinMargin", "poin margin (NPM/NIM)"),
                 ("poinPertumbuhan", "poin pertumbuhan EPS"), ("poinKualitas", "poin kualitas (CFO/laba atau CAR)"),
                 ("skorFundamental", "skor fundamental (0-10)"), ("skorValuasi", "skor valuasi (0-3)"), ("poinTren", "poin tren"),
                 ("poinRSI", "poin RSI"), ("poinMACD", "poin MACD"), ("poinVolume", "poin volume"), ("skorTeknikal", "skor teknikal (0-7)"),
                 ("poinAccDist", "poin acc/dist"), ("poinAsing", "poin asing"), ("skorBandar", "skor bandarmology (0-5)"),
                 ("skorSentimen", "skor sentimen (-2..2)"), ("skorKontribusiSektor", "kontribusi outlook sektor (-3..4)"),
                 ("penaltiRisiko", "penalti risiko (-5..0)"), ("poinLikuiditas", "poin likuiditas (0-2)"), ("skorTotalEmiten", "SKOR TOTAL EMITEN")]:
        dp(n, "Emiten", int, l, "INFERENSI SWRL")
    for n, l in [("rasioPERvsHistoris", "rasio PER / PER 5 th"), ("epsEstimasi", "EPS estimasi (Rp)"), ("nilaiWajar", "nilai wajar PER-band (Rp)"),
                 ("potensiUpsidePersen", "potensi upside (%)"), ("atrRupiah", "ATR (Rp)"), ("hargaStopLoss", "harga stop loss (Rp)"),
                 ("hargaTakeProfit", "harga take profit (Rp)")]:
        dp(n, "Emiten", float, l, "INFERENSI SWRL")
    # sektor
    dp("kodeIndeksSektor", "Sektor", str, "kode indeks sektoral")
    for n, l in [("perSektor", "PER sektor (x)"), ("per5TahunSektor", "PER rata-rata 5 th sektor"), ("aliranAsing3BulanT", "net asing 3 bulan (Rp T)"),
                 ("skorSentimenSektor", "skor sentimen sektor (output scorer)")]:
        dp(n, "Sektor", float, l)
    for n, l in [("skorTemaStruktural", "skor tema struktural (-2..3, pakar)"), ("skorFaseEarly", "skor rotasi Early Cycle"),
                 ("skorFaseMid", "skor rotasi Mid Cycle"), ("skorFaseLate", "skor rotasi Late Cycle"), ("skorFaseResesi", "skor rotasi Resesi/Stagflasi")]:
        dp(n, "Sektor", int, l)
    for f in M.FAKTOR:
        dp("sens" + f, "Sektor", int, "sensitivitas sektor terhadap " + f, M.FAKTOR_DESC[f] + " ; nilai -2..2 (pakar)")
        dp("arah" + f, "Skenario", int, "arah faktor " + f + " pada skenario", M.FAKTOR_DESC[f] + " ; nilai -2..2")
    for n, l in [("skorValuasiSektor", "skor valuasi sektor"), ("skorTemaTertimbang", "skor tema × 2"), ("poinSentimenSektor", "poin sentimen sektor"),
                 ("poinAliranAsing", "poin aliran asing sektor"), ("skorOutlookAktif", "SKOR OUTLOOK SEKTOR (skenario aktif)")]:
        dp(n, "Sektor", int, l, "INFERENSI SWRL")
    dp("rasioValuasiSektor", "Sektor", float, "rasio PER sektor / PER 5 th", "INFERENSI SWRL")
    # penilaian
    for n, l in [("skorMakroGeoA", "skor makro-geo bagian A (faktor 1-6)"), ("skorMakroGeoB", "skor makro-geo bagian B (faktor 7-12)"), ("skorMakroGeo", "skor makro-geopolitik Σ(sensitivitas × arah)"), ("skorRotasi", "skor rotasi siklus"), ("skorOutlook", "skor outlook penilaian")]:
        dp(n, "PenilaianSektor", int, l, "INFERENSI SWRL")
    # skenario & CBR
    dp("statusAktif", "Skenario", int, "status aktif (1 = dipakai)")
    dp("probabilitasSkenario", "Skenario", float, "probabilitas subjektif pakar")
    for n in ["cbrFed", "cbrMinyak", "cbrUSD", "cbrRiskOff", "cbrKomoditas", "cbrInflasi"]:
        dp(n, None, int, "fitur CBR " + n[3:], "Fitur kasus (-2..2) untuk skenario & periode historis")
    dp("tahunPeriode", "PeriodeHistoris", int, "tahun periode")
    dp("skorKemiripan", "PeriodeHistoris", int, "skor kemiripan dengan skenario aktif (maks 20)", "INFERENSI SWRL")
    # berita
    dp("judulBerita", "Berita", str, "judul berita")
    dp("namaMedia", "Berita", str, "nama media")
    dp("urlSumber", None, str, "URL sumber")
    dp("tanggalTerbit", "Berita", datetime.date, "tanggal terbit")
    dp("umurHari", "Berita", int, "umur berita (hari, terhadap tanggal acuan data/tanggal_acuan.txt)")
    dp("kredibilitasSumber", "Berita", float, "kredibilitas sumber (0..1)")
    dp("skorSentimenBerita", "Berita", float, "skor nada berita (-1..1)")
    dp("arahVariabel", "Berita", int, "arah variabel makro terdeteksi (+1/0/-1)")
    # lain
    dp("kodeIndeks", "IndeksSaham", str, "kode indeks")
    dp("negaraAsal", "IndeksSaham", str, "negara/wilayah")
    dp("jumlahKonstituen", "IndeksSaham", int, "jumlah konstituen")
    dp("nilaiIndikator", "IndikatorMakro", float, "nilai indikator")
    dp("satuan", None, str, "satuan")
    dp("tanggalData", None, str, "tanggal data")
    dp("tanggalPeristiwa", "PeristiwaGeopolitik", str, "tanggal peristiwa")
    dp("statusKebijakanBerjalan", "PeristiwaGeopolitik", int, "kebijakan masih berjalan (1/0)")
    dp("skorKekuatanTema", "TemaStruktural", int, "kekuatan tema (-2..3)")
    dp("modalAwalJuta", "InvestorRitel", float, "modal awal (Rp juta)")
    dp("kebutuhanStakeholder", "Stakeholder", str, "kebutuhan stakeholder")
    dp("tahunBerdiriIndeks", "IndeksSaham", int, "tahun berdiri")

    # ------------------------------------------------------------ PROPERTIES v2
    op("menyediakanIndikator", "SumberData", "IndikatorKatalog", "menyediakan indikator")
    op("diperolehDari", "IndikatorKatalog", "SumberData", "diperoleh dari", inverse="menyediakanIndikator")
    op("regimeTerdeteksi", "KondisiPasar", "RegimePasar", "regime terdeteksi", "INFERENSI: regime dari skor stres pasar.")
    op("antisipasiMengaktifkan", "AntisipasiKebijakan", "PergerakanMakro", "antisipasi mengaktifkan")
    op("katalisSektor", "Katalis", "Sektor", "katalis untuk sektor")
    op("katalisIndeks", "Katalis", "IndeksSaham", "katalis untuk indeks")
    op("memilikiKatalisDekat", "Emiten", "Katalis", "memiliki katalis dekat", "INFERENSI.")
    op("sektorMemilikiKatalis", "Sektor", "Katalis", "sektor memiliki katalis dekat", "INFERENSI.")
    op("tesisUntukSektor", "TesisInvestasi", "Sektor", "tesis untuk sektor")
    op("indikatorKunciTesis", "TesisInvestasi", "IndikatorMakro", "indikator kunci tesis")
    op("topPickAdaptifSektor", "Sektor", "Emiten", "top pick adaptif sektor", "INFERENSI (regime-aware).")
    op("terkonsentrasiDengan", "Emiten", "Emiten", "terkonsentrasi dengan", "INFERENSI: berbagi eksposur komoditas.", symmetric=True)
    for n in ["drawdownIHSGPersen", "perubahanIHSG1BulanPersen", "penurunanHarianTerbesarPersen", "netAsingYTDT", "cds5YBps", "yieldSBN10Y",
              "spreadSBNUSTBps", "kursUSDIDR", "inflasiYoY", "biRatePersen", "ffrAtasPersen", "brentUSD", "emasUSD", "breadthPersenDiAtasMA200"]:
        dp(n, "KondisiPasar", float, n)
    for n in ["trenCDS1Bulan", "trenRupiah1Bulan", "trenYieldSBN1Bulan", "statusAktifKondisi"]:
        dp(n, "KondisiPasar", int, n)
    for n in ["poinStresDrawdown", "poinStresCDS", "poinStresAsing", "poinStresKurs", "poinStresYield", "poinStresBreadth", "skorStresPasar"]:
        dp(n, "KondisiPasar", int, n, "INFERENSI SWRL")
    for n in ["bobotFundamental", "bobotValuasi", "bobotTeknikal", "bobotBandar", "bobotSentimen", "bobotSektor", "bobotRisiko", "bobotLikuiditas",
              "bobotSmartMoney", "risikoPerTransaksiPersen", "ambangTopPickAdaptif"]:
        dp(n, "RegimePasar", float, n, "Meta-knowledge pakar: bobot pilar per regime")
    for n in ["porsiTranche1", "porsiTranche2", "porsiTranche3"]:
        dp(n, "RegimePasar", int, n + " (% modal alokasi)")
    dp("tanggalKatalis", "Katalis", str, "tanggal katalis")
    dp("hariMenujuKatalis", "Katalis", int, "hari menuju katalis (terhadap tanggal acuan)")
    for n in ["ambangInvalidasiBawah", "ambangInvalidasiAtas", "ambangPemicuBawah"]:
        dp(n, "TesisInvestasi", float, n)
    for n in ["bufferBawahPersen", "bufferAtasPersen"]:
        dp(n, "TesisInvestasi", float, n, "INFERENSI SWRL")
    dp("umurDataHari", None, int, "umur data (hari)")
    dp("frekuensiHari", None, int, "frekuensi pembaruan (hari)")
    for n in ["sifatWaktu", "frekuensiUpdate", "statusIntegrasi", "pilarIndikator", "jenisAkses", "formatData"]:
        dp(n, None, str, n)
    dp("skorKredibilitasSumber", "SumberData", float, "kredibilitas sumber (0-1)")
    for n in ["revisiEPS3BulanPersen", "sahamDigadaikanPersen", "konsentrasiBrokerTop3Persen"]:
        dp(n, "Emiten", float, n)
    for n in ["transaksiOrangDalam", "jumlahARA5Hari"]:
        dp(n, "Emiten", int, n)
    for n in ["kekuatanRelatifPersen", "equityRiskPremium", "skorAdaptifRegime", "ukuranPosisiMaksPersen", "hargaTranche1", "hargaTranche2", "hargaTranche3"]:
        dp(n, "Emiten", float, n, "INFERENSI SWRL")
    for n in ["poinSmartMoney", "flagFundamental", "flagValuasi", "flagTeknikal", "flagBandar", "flagSentimen", "flagMakroSektor", "skorKonfluensi", "skorKontribusiSektorEV"]:
        dp(n, "Emiten", int, n, "INFERENSI SWRL")
    dp("skorEkspektasiProbabilistik", "Sektor", float, "skor ekspektasi probabilistik (Σ p × outlook)", "INFERENSI SWRL")
    for n in ["skorOutlookBase", "skorOutlookBull", "skorOutlookBear", "upsideSkenario", "downsideSkenario"]:
        dp(n, "Sektor", int, n, "INFERENSI SWRL")

    # ------------------------------------------------------------ INDIVIDU: KONSEP DASAR
    IND = {}
    def ind(name, cls, label=None, comment=None):
        clss = cls if isinstance(cls, list) else [cls]
        i = CLS[clss[0]](name, namespace=onto)
        for extra in clss[1:]:
            i.is_a.append(CLS[extra])
        if label: i.label = [L(label)]
        if comment: i.comment = [L(comment)]
        IND[name] = i
        return i
    ANN = {"rumus": rumus, "interpretasi": interpretasi, "ambangBatas": ambangBatas, "contohPenerapan": contohPenerapan, "heuristikPakar": heuristikPakar}
    for (n, cls, l, d, kw) in CONCEPTS:
        i = ind(n, cls, l, d)
        for k, v in kw.items():
            if not v: continue
            if k == "skorTemaDefault":
                i.skorKekuatanTema = [int(v)]
            else:
                setattr(i, ANN[k].python_name, [L(v)])

    # ------------------------------------------------------------ INSTITUSI, PENYEDIA, INDEKS, BROKER, KOMODITAS
    for n, cls, l, d in M.INSTITUSI:
        ind(n, cls, l, d)
    IND["OJK"].mengawasi = [IND["BEI_Bursa"], IND["KSEI"], IND["KPEI"]]
    for n, l in M.PENYEDIA:
        ind(n, "PenyediaIndeks", l)
    for (n, cls, l, prov, neg, jml, ket) in M.INDEKS:
        i = ind(n, cls, l, ket or None)
        i.kodeIndeks = [n]; i.negaraAsal = [neg]; i.diterbitkanOleh = [IND[prov]]
        if jml: i.jumlahKonstituen = [jml]
    for a, b in M.PENGARUH_INDEKS:
        IND[a].memengaruhiIndeks.append(IND[b])
    for code, nama, cls in M.BROKER:
        i = ind("Broker_" + code, cls, f"{code} - {nama}", f"Kode broker {code}. Verifikasi kode di situs BEI.")
    for n, cls, l, sat in M.KOMODITAS:
        i = ind(n, cls, l); i.satuan = [sat]
    for (n, cls, l, val, sat, tgl, url, ket) in M.MAKRO:
        i = ind(n, cls, l, ket or None)
        i.nilaiIndikator = [float(val)]; i.satuan = [sat]; i.tanggalData = [tgl]
        if url: i.urlSumber = [url]; i.sumberReferensi = [url]
        tg = tgl if len(tgl) == 10 else (tgl + "-15" if len(tgl) == 7 else tgl + "-07-01")
        i.umurDataHari = [(G.TODAY - datetime.date.fromisoformat(tg)).days]
        i.frekuensiHari = [V2.FREKUENSI_MAKRO.get(n, 30)]
    IND["Makro_BIRate"].dirilisOleh = [IND["BankIndonesia"]]; IND["Makro_DepositFacility"].dirilisOleh = [IND["BankIndonesia"]]
    IND["Makro_FedFundsRate"].dirilisOleh = [IND["TheFed"]]; IND["Makro_InflasiID"].dirilisOleh = [IND["BPS"]]

    # ------------------------------------------------------------ SEKTOR & SUBSEKTOR
    news, sek_sent, emi_sent, emi_cnt = score_all()
    for (n, l, kode, pe, pe5, flow, tema, fase, sens) in M.SEKTOR:
        i = ind(n, ["Sektor", G.SEKTOR_KATEGORI[n]], "Sektor " + l, f"Sektor {l} (IDX-IC), indeks {kode}.")
        i.kodeIndeksSektor = [kode]; i.memilikiIndeksSektoral = [IND[kode]]
        i.perSektor = [float(pe)]; i.per5TahunSektor = [float(pe5)]; i.aliranAsing3BulanT = [float(flow)]
        i.skorTemaStruktural = [tema]
        i.skorFaseEarly, i.skorFaseMid, i.skorFaseLate, i.skorFaseResesi = [fase[0]], [fase[1]], [fase[2]], [fase[3]]
        for f, v in zip(M.FAKTOR, sens):
            setattr(i, "sens" + f, [v])
        i.skorSentimenSektor = [float(sek_sent[n])]
        i.didukungTema = [IND[t] for t in M.SEKTOR_TEMA[n]]
        fav = [("Fase_EarlyCycle", fase[0]), ("Fase_MidCycle", fase[1]), ("Fase_LateCycle", fase[2]), ("Fase_ResesiStagflasi", fase[3])]
        i.disukaiPadaFase = [IND[f] for f, v in fav if v >= 2]
        i.catatanData = ["PER sektor, aliran asing: indikatif (estimasi pakar). Skor sentimen: output sentiment_scorer.py"]
    for n, l, s in M.SUBSEKTOR:
        i = ind(n, "Subsektor", l); i.bagianDariSektor = IND[s]
    for g in M.GRUP:
        ind(g, "KonglomerasiGrup", g.replace("Grup_", "Grup ").replace("_", " "))

    # ------------------------------------------------------------ EMITEN
    foreign = ["KZ", "BK", "AK", "ZP", "RX", "YU", "KK"]; inst = ["CC", "NI", "DX", "LG", "AZ"]; retail = ["YP", "PD", "XL", "XC"]
    UJI = M.parse_emiten(V2.EMITEN_UJI_TABLE)
    ind("Grup_Uji", "KonglomerasiGrup", "Grup Uji (fiktif)")
    for k, r in enumerate(M.EMITEN + UJI):
        cls = ["EmitenPerbankan" if r["bank"] else "EmitenNonKeuangan"]
        if r["kode"].startswith("UJI_"): cls.append("EmitenUji")
        if r["bumn"]: cls.append("EmitenBUMN")
        if r["syariah"]: cls.append("EmitenSyariah")
        e = ind(r["kode"], cls, f"{r['kode']} - {r['nama']}")
        e.kodeSaham = [r["kode"]]; e.namaPerusahaan = [r["nama"]]
        e.termasukSektor = IND[r["sektor"]]; e.termasukSubsektor = IND[r["sub"]]
        e.bagianDariGrup = [IND[r["grup"]]]
        e.anggotaIndeks = [IND[x] for x in r["indeks"]]
        e.eksposurKomoditasPendapatan = [IND[x] for x in r["komU"]]
        e.eksposurKomoditasBiaya = [IND[x] for x in r["komB"]]
        e.terdeteksiPola = [IND[x] for x in r["pola"]]
        e.hargaPenutupan = [r["harga"]]; e.kapitalisasiPasarT = [r["mcap"]]; e.likuiditasHarianM = [r["likuid"]]; e.freeFloatPersen = [r["ff"]]
        e.per = [r["per"]]; e.per5Tahun = [r["per5"]]; e.pbv = [r["pbv"]]; e.roe = [r["roe"]]
        if r["bank"]:
            e.npl = [r["f2"]]; e.nim = [r["f3"]]; e.car = [r["f5"]]
        else:
            e.der = [r["f2"]]; e.npm = [r["f3"]]; e.cfoPerLabaBersih = [r["f5"]]; e.altmanZ = [r["altman"]]
        e.pertumbuhanEPS = [r["epsg"]]; e.dividendYield = [r["dy"]]; e.dpr = [r["dpr"]]; e.beneishM = [r["beneish"]]
        e.jarakMA50Persen = [r["ma50"]]; e.jarakMA200Persen = [r["ma200"]]; e.selisihMA50MA200Persen = [r["ma50v200"]]
        e.rsi14 = [r["rsi"]]; e.histogramMACD = [r["macd"]]; e.rasioVolume = [r["volr"]]; e.atrPersen = [r["atr"]]
        e.skorAccDistBroker = [r["acc"]]; e.netAsing20HariM = [r["for20"]]; e.netRitel20HariM = [r["ret20"]]
        e.perubahanHarga20HariPersen = [r["chg20"]]; e.jarakVWAPPersen = [r["vwap"]]; e.rasioBidOffer = [r["bo"]]
        e.skorSentimenEmiten = [float(emi_sent.get(r["kode"], 0.0))]; e.jumlahBeritaRelevan = [emi_cnt.get(r["kode"], 0)]
        if r["kode"] in V2.EKSTRA_UJI:
            rv, gd, od, kb, ara = V2.EKSTRA_UJI[r["kode"]]
        else:
            rv, gd, od, kb, ara = r.get("revisi", V2.REVISI.get(r["kode"], 0.0)), 0.0, 0, 35.0 + (k % 4) * 3, 0
        e.revisiEPS3BulanPersen = [float(rv)]; e.sahamDigadaikanPersen = [float(gd)]; e.transaksiOrangDalam = [int(od)]
        e.konsentrasiBrokerTop3Persen = [float(kb)]; e.jumlahARA5Hari = [int(ara)]
        # broker (indikatif, deterministik dari pola aliran)
        if r["acc"] >= 10:
            a = foreign[k % 7] if r["for20"] > 0 else inst[k % 5]
            d = retail[k % 4] if r["ret20"] < 0 else (foreign[(k + 3) % 7] if r["for20"] < 0 else inst[(k + 2) % 5])
        elif r["acc"] <= -10:
            a = retail[k % 4]; d = foreign[k % 7] if r["for20"] < 0 else inst[k % 5]
        else:
            a = inst[k % 5]; d = retail[(k + 1) % 4]
        e.brokerAkumulatorUtama = [IND["Broker_" + a]]; e.brokerDistributorUtama = [IND["Broker_" + d]]
        if r["kode"].startswith("UJI_"):
            e.catatanData = ["EMITEN FIKTIF untuk pengujian aturan (unit test) - bukan saham nyata."]
        else:
            e.is_a.append(CLS["DataIndikatif"])
            e.catatanData = ["SNAPSHOT INDIKATIF (demonstrasi penalaran) - perbarui dari laporan keuangan & data pasar terbaru sebelum digunakan. Data gadai/orang dalam = 0 (belum diisi dari keterbukaan informasi)."]
    by_sub = {}
    for r in M.EMITEN:
        by_sub.setdefault(r["sub"], []).append(r["kode"])
    for sub, codes in by_sub.items():
        for a in codes:
            for b in codes:
                if a < b:
                    IND[a].pesaingDari.append(IND[b])

    # ------------------------------------------------------------ PERGERAKAN, PERISTIWA
    for (n, l, geo, sebab, untung, rugi, kontra, kn, kt) in G.PERGERAKAN:
        ind(n, ["PergerakanGeopolitik"] if geo else ["PergerakanMakro"], l)
    for (n, l, geo, sebab, untung, rugi, kontra, kn, kt) in G.PERGERAKAN:
        i = IND[n]
        i.menyebabkan = [IND[x] for x in sebab]
        i.menguntungkanSektor = [IND[x] for x in untung]
        i.merugikanSektor = [IND[x] for x in rugi]
        i.menciptakanPeluangKontrarian = [IND[x] for x in kontra]
        i.menaikkanHargaKomoditas = [IND[x] for x in kn]
        i.menurunkanHargaKomoditas = [IND[x] for x in kt]
    for (n, clss, l, tgl, desc, memicu, oleh, berjalan, idx) in G.PERISTIWA:
        i = ind(n, clss, l, desc)
        i.tanggalPeristiwa = [tgl]
        i.memicuPergerakan = [IND[x] for x in memicu]
        if oleh: i.diputuskanOleh = [IND[oleh]]
        i.statusKebijakanBerjalan = [berjalan]
        i.berdampakPadaIndeks = [IND[x] for x in idx]

    # ------------------------------------------------------------ BERITA
    nmap = {n["id"]: n for n in news}
    for (nid, tgl, media, url, judul, kelas, kred, ev, sek, emi, var, ov) in G.BERITA:
        s = nmap[nid]
        i = ind("Berita_" + nid, kelas, judul)
        i.judulBerita = [judul]; i.namaMedia = [media]
        if url: i.urlSumber = [url]; i.sumberReferensi = [url]
        i.tanggalTerbit = [datetime.date.fromisoformat(tgl)]; i.umurHari = [s["umur"]]
        i.kredibilitasSumber = [float(kred)]; i.skorSentimenBerita = [float(s["tone"])]; i.arahVariabel = [int(s["arah"])]
        i.tentangPeristiwa = [IND[x] for x in ev]; i.tentangSektor = [IND[x] for x in sek]; i.tentangEmiten = [IND[x] for x in emi]
        i.dariSumber = [IND["Sumber_RisetAnalis" if kelas == "BeritaRisetAnalis" else ("Sumber_BeritaFinansial")]]
        if s["metode"] == "anotasi-analis":
            i.catatanData = ["Arah variabel dianotasi analis (human-in-the-loop) karena judul ambigu bagi leksikon."]

    # ------------------------------------------------------------ SKENARIO, PENILAIAN, CBR
    for (n, l, aktif, prob, fase, arah, cbr, desc) in G.SKENARIO:
        i = ind(n, "Skenario", l, desc)
        i.statusAktif = [aktif]; i.probabilitasSkenario = [prob]; i.faseSiklus = IND[fase]
        for f, v in zip(M.FAKTOR, arah):
            setattr(i, "arah" + f, [v])
        i.cbrFed, i.cbrMinyak, i.cbrUSD, i.cbrRiskOff, i.cbrKomoditas, i.cbrInflasi = [[x] for x in cbr]
        for s in M.SEKTOR:
            a = ind(f"Penilaian_{s[0].replace('Sektor_', '')}_{n.replace('Skenario_', '')}", "PenilaianSektor",
                    f"Penilaian {s[1]} - {l}")
            a.menilaiSektor = IND[s[0]]; a.dibawahSkenario = i
    for (n, l, th, cbr, win, lose, les) in G.PERIODE:
        i = ind(n, "PeriodeHistoris", l, les)
        i.tahunPeriode = [th]
        i.cbrFed, i.cbrMinyak, i.cbrUSD, i.cbrRiskOff, i.cbrKomoditas, i.cbrInflasi = [[x] for x in cbr]
        i.unggulPadaPeriode = [IND["Sektor_" + x] for x in win]
        i.terpurukPadaPeriode = [IND["Sektor_" + x] for x in lose]

    # ------------------------------------------------------------ STAKEHOLDER & KELUARAN
    for (n, cls, l, keb, kons, prof, hor, modal) in G.STAKEHOLDER:
        i = ind(n, cls, l)
        i.kebutuhanStakeholder = [keb]
        i.mengonsumsiKeluaran = [IND[x] for x in kons]
        if prof: i.memilikiProfilRisiko = IND[prof]
        if hor: i.memilikiHorizon = IND[hor]
        if modal: i.modalAwalJuta = [modal]
    for o, sdgs in G.KELUARAN_SDG.items():
        IND[o].mendukungSDG = [IND[x] for x in sdgs]
    for h in [c for c in CONCEPTS if c[1] == "AturanPakar"]:
        IND[h[0]].heuristikDigunakanOleh = [IND["Output_PrediksiSektor"], IND["Output_PenjelasanEdukatif"]]

    # ------------------------------------------------------------ INDIVIDU v2
    for (n, cls, l, akses, fmt, kred, url, d) in SRC.SUMBER:
        i = ind(n, cls, l, d)
        i.jenisAkses = [akses]; i.formatData = [fmt]; i.skorKredibilitasSumber = [float(kred)]
        if url: i.urlSumber = [url]
    for (n, l, pilar, sifat, frek, fh, src, status, cat) in SRC.K:
        i = ind(n, ["IndikatorKatalog", "Indikator" + sifat], l, f"Pilar: {pilar}. {cat}".strip())
        i.pilarIndikator = [pilar]; i.sifatWaktu = [sifat]; i.frekuensiUpdate = [frek]; i.frekuensiHari = [fh]; i.statusIntegrasi = [status]
        i.diperolehDari = [IND[x] for x in src]
    KP = V2.KONDISI
    real = [r for r in M.EMITEN]
    breadth = round(100.0 * sum(1 for r in real if r["ma200"] >= 0) / len(real), 2)
    i = ind(KP["nama"], "KondisiPasar", KP["label"], "State vector pasar untuk deteksi regime & reaction function. Breadth dihitung dari universe 64 emiten (agregasi di luar SWRL karena SWRL tidak dapat menghitung jumlah).")
    for key, val in KP.items():
        if key in ("nama", "label"): continue
        setattr(i, key, [int(val)] if key.startswith("tren") else [float(val)])
    i.breadthPersenDiAtasMA200 = [breadth]; i.statusAktifKondisi = [1]
    for (n, l, d, w, risk, tr) in V2.REGIME:
        i = ind(n, "RegimePasar", l, d)
        for prop, val in zip(["bobotFundamental", "bobotValuasi", "bobotTeknikal", "bobotBandar", "bobotSentimen", "bobotSektor", "bobotRisiko", "bobotLikuiditas", "bobotSmartMoney"], w):
            setattr(i, prop, [float(val)])
        mx = sum(a * b for a, b in zip(w, V2.MAKS_PILAR))
        i.ambangTopPickAdaptif = [round(0.65 * mx, 2)]; i.risikoPerTransaksiPersen = [float(risk)]
        i.porsiTranche1, i.porsiTranche2, i.porsiTranche3 = [tr[0]], [tr[1]], [tr[2]]
    for (n, l, d, mv) in V2.ANTISIPASI:
        i = ind(n, "AntisipasiKebijakan", l, d); i.antisipasiMengaktifkan = [IND[mv]]
    for (n, cls, l, tgl, sek, idx, d) in V2.KATALIS:
        i = ind(n, cls, l, d or None)
        i.tanggalKatalis = [tgl]; i.hariMenujuKatalis = [V2.hari_menuju(tgl)]
        i.katalisSektor = [IND[x] for x in sek]; i.katalisIndeks = [IND[x] for x in idx]
    for (n, l, sek, indk, lo, hi, trig, d) in V2.TESIS:
        i = ind(n, "TesisInvestasi", l, d)
        i.tesisUntukSektor = [IND[sek]]; i.indikatorKunciTesis = [IND[indk]]
        i.ambangInvalidasiBawah = [float(lo)]; i.ambangInvalidasiAtas = [float(hi)]
        if trig is not None: i.ambangPemicuBawah = [float(trig)]
    for n, l, d in V2.HEUR_V2:
        i = ind(n, "AturanPakar", l, d)
        i.heuristikDigunakanOleh = [IND["Output_PrediksiSektor"], IND["Output_SinyalQuantTrade"]]
    ind("Output_RegimeDanStrategiPasar", "KeluaranSistem", "Regime & Strategi Pasar", "Deteksi regime, kapitulasi, akumulasi bertahap, antisipasi kebijakan.")
    ind("Output_TesisDanKillSwitch", "KeluaranSistem", "Tesis & Kill Switch", "Pemantauan validitas tesis & ambang invalidasi.")
    ind("Output_KalenderKatalis", "KeluaranSistem", "Kalender Katalis", "Katalis biner/musiman ≤ 45 hari & strategi tranche.")
    IND["Stk_MitraSekuritas"].mengonsumsiKeluaran.extend([IND["Output_RegimeDanStrategiPasar"], IND["Output_TesisDanKillSwitch"], IND["Output_KalenderKatalis"]])
    IND["Stk_ManajerInvestasi"].mengonsumsiKeluaran.extend([IND["Output_RegimeDanStrategiPasar"], IND["Output_TesisDanKillSwitch"]])
    IND["Stk_TimEquityResearch"].mengonsumsiKeluaran.extend([IND["Output_KalenderKatalis"], IND["Output_TesisDanKillSwitch"]])

    # ------------------------------------------------------------ SWRL
    RULES = build_rules(onto, M.FAKTOR, kodeAturan, pilarAnalisis)

def count_stats():
    n_cls = len(list(onto.classes())); n_op = len(list(onto.object_properties())); n_dp = len(list(onto.data_properties()))
    n_ap = len(list(onto.annotation_properties())); n_ind = len(list(onto.individuals())); n_rules = len(list(onto.rules()))
    return dict(kelas=n_cls, objectProperty=n_op, dataProperty=n_dp, annotationProperty=n_ap, individu=n_ind, aturanSWRL=n_rules)

if __name__ == "__main__":
    asserted = os.path.join(OUT, "SahamExpertKB_v2.owl")
    onto.save(file=asserted, format="rdfxml")
    print("Disimpan:", asserted, count_stats())
    if "--reason" in sys.argv:
        import time; t = time.time()
        with onto:
            sync_reasoner_pellet(world, infer_property_values=True, infer_data_property_values=True, debug=0)
        print("Pellet selesai dalam %.1f detik" % (time.time() - t))
        # Catatan: file *_inferred.owl dibuat oleh tools/java/ExportInferred (OWLAPI + Pellet) agar identik dengan Protégé.
        from export_results import export
        export(onto, OUT)
