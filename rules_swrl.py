# -*- coding: utf-8 -*-
"""
RBox: aturan SWRL sistem pakar. Setiap aturan diberi kode, pilar, dan penjelasan (rdfs:label & rdfs:comment)
agar tampil rapi di Protégé > Window > Tabs > SWRLTab.
Konvensi bin: interval setengah terbuka [bawah, atas) agar aturan saling lepas & menutup seluruh domain
(syarat penting karena SWRL monoton dan tidak mengenal negation-as-failure).
"""
from owlready2 import Imp, locstr

RULES = []

def R(code, pilar, desc, body):
    RULES.append((code, pilar, desc, body))

def bins(code, pilar, desc, prop, target, var, cuts, cls=None, extra=""):
    """cuts: list (lo, hi, poin, kelasOptional). lo/hi None = tak terbatas."""
    for j, (lo, hi, pts, kls) in enumerate(cuts):
        cond = [f"{prop}(?e, ?v)"]
        if lo is not None: cond.append(f"greaterThanOrEqual(?v, {lo})")
        if hi is not None: cond.append(f"lessThan(?v, {hi})")
        head = [f"{target}(?e, {pts})"] if target else []
        if kls: head.append(f"{kls}(?e)")
        rng = f"[{lo if lo is not None else '-inf'}, {hi if hi is not None else '+inf'})"
        R(f"{code}{chr(97 + j)}", pilar, f"{desc}: {prop} ∈ {rng} → {target or ''} {pts if target else ''} {kls or ''}".strip(),
          f"{var}(?e), " + ", ".join(cond) + (", " + extra if extra else "") + " -> " + ", ".join(head))

def define_rules(FAKTOR):
    RULES.clear()
    # ================================================================= FUNDAMENTAL
    bins("R-FUND-01", "Fundamental", "Poin ROE", "roe", "poinROE", "Emiten", [(15.0, None, 2, None), (8.0, 15.0, 1, None), (None, 8.0, 0, None)])
    bins("R-FUND-02", "Fundamental", "Poin solvabilitas non-bank (DER)", "der", "poinSolvabilitas", "EmitenNonKeuangan",
         [(None, 0.5, 2, None), (0.5, 1.5, 1, None), (1.5, None, 0, None)])
    bins("R-FUND-03", "Fundamental", "Poin solvabilitas bank (NPL)", "npl", "poinSolvabilitas", "EmitenPerbankan",
         [(None, 2.0, 2, None), (2.0, 3.5, 1, None), (3.5, None, 0, None)])
    bins("R-FUND-04", "Fundamental", "Poin margin non-bank (NPM)", "npm", "poinMargin", "EmitenNonKeuangan",
         [(15.0, None, 2, None), (5.0, 15.0, 1, None), (None, 5.0, 0, None)])
    bins("R-FUND-05", "Fundamental", "Poin margin bank (NIM)", "nim", "poinMargin", "EmitenPerbankan",
         [(5.0, None, 2, None), (3.5, 5.0, 1, None), (None, 3.5, 0, None)])
    bins("R-FUND-06", "Fundamental", "Poin pertumbuhan EPS", "pertumbuhanEPS", "poinPertumbuhan", "Emiten",
         [(15.0, None, 2, None), (0.0, 15.0, 1, None), (None, 0.0, 0, None)])
    bins("R-FUND-07", "Fundamental", "Poin kualitas laba (CFO/laba)", "cfoPerLabaBersih", "poinKualitas", "EmitenNonKeuangan",
         [(1.0, None, 2, None), (0.7, 1.0, 1, None), (None, 0.7, 0, None)])
    bins("R-FUND-08", "Fundamental", "Poin permodalan bank (CAR)", "car", "poinKualitas", "EmitenPerbankan",
         [(20.0, None, 2, None), (15.0, 20.0, 1, None), (None, 15.0, 0, None)])
    R("R-FUND-09", "Fundamental", "Skor fundamental = ROE + solvabilitas + margin + pertumbuhan + kualitas (0-10)",
      "Emiten(?e), poinROE(?e, ?a), poinSolvabilitas(?e, ?b), poinMargin(?e, ?c), poinPertumbuhan(?e, ?d), poinKualitas(?e, ?f), add(?s, ?a, ?b, ?c, ?d, ?f) -> skorFundamental(?e, ?s)")
    bins("R-FUND-10", "Fundamental", "Klasifikasi kesehatan fundamental", "skorFundamental", None, "Emiten",
         [(8, None, None, "FundamentalKuat"), (5, 8, None, "FundamentalSedang"), (None, 5, None, "FundamentalLemah")])
    R("R-FUND-11", "Fundamental", "Kualitas laba tinggi: CFO ≥ laba bersih pada emiten yang laba",
      "EmitenNonKeuangan(?e), cfoPerLabaBersih(?e, ?c), greaterThanOrEqual(?c, 1.0), per(?e, ?p), greaterThan(?p, 0.0) -> KualitasLabaTinggi(?e)")
    R("R-FUND-12", "Fundamental", "Dividen andalan: yield ≥ 6%, payout ≤ 90%, fundamental ≥ 5",
      "Emiten(?e), dividendYield(?e, ?y), greaterThanOrEqual(?y, 6.0), dpr(?e, ?d), lessThanOrEqual(?d, 90.0), skorFundamental(?e, ?s), greaterThanOrEqual(?s, 5) -> DividenAndalan(?e)")

    # ================================================================= VALUASI
    R("R-VAL-01", "Fundamental-Valuasi", "Emiten merugi (PER ≤ 0) → skor valuasi 0",
      "Emiten(?e), per(?e, ?p), lessThanOrEqual(?p, 0.0) -> EmitenMerugi(?e), skorValuasi(?e, 0)")
    R("R-VAL-02", "Fundamental-Valuasi", "Rasio PER terhadap rata-rata 5 tahun (PER band)",
      "Emiten(?e), per(?e, ?p), greaterThan(?p, 0.0), per5Tahun(?e, ?q), greaterThan(?q, 0.0), divide(?r, ?p, ?q) -> rasioPERvsHistoris(?e, ?r)")
    bins("R-VAL-03", "Fundamental-Valuasi", "Skor valuasi PER band", "rasioPERvsHistoris", "skorValuasi", "Emiten",
         [(None, 0.6, 3, "Undervalued"), (0.6, 0.85, 2, "Undervalued"), (0.85, 1.1, 1, "FairValued"), (1.1, None, 0, "Overvalued")])
    R("R-VAL-04", "Fundamental-Valuasi", "EPS estimasi = harga / PER",
      "Emiten(?e), hargaPenutupan(?e, ?h), per(?e, ?p), greaterThan(?p, 0.0), divide(?eps, ?h, ?p) -> epsEstimasi(?e, ?eps)")
    R("R-VAL-05", "Fundamental-Valuasi", "Nilai wajar = EPS × PER rata-rata 5 tahun; upside = (NW/harga - 1) × 100",
      "Emiten(?e), epsEstimasi(?e, ?eps), per5Tahun(?e, ?q), hargaPenutupan(?e, ?h), multiply(?nw, ?eps, ?q), divide(?r, ?nw, ?h), subtract(?u0, ?r, 1.0), multiply(?u, ?u0, 100.0) -> nilaiWajar(?e, ?nw), potensiUpsidePersen(?e, ?u)")

    # ================================================================= RISIKO / COLLAPSE
    bins("R-RISK-01", "Fundamental-Risiko", "Zona Altman Z non-bank & penalti risiko", "altmanZ", "penaltiRisiko", "EmitenNonKeuangan",
         [(None, 1.81, -5, "ZonaDistress"), (1.81, 2.99, -1, "ZonaAbuAbu"), (2.99, None, 0, "ZonaAman")])
    bins("R-RISK-02", "Fundamental-Risiko", "Permodalan bank & penalti risiko", "car", "penaltiRisiko", "EmitenPerbankan",
         [(None, 12.0, -5, "BankModalLemah"), (12.0, None, 0, None)])
    R("R-RISK-03", "Fundamental-Risiko", "Bank NPL > 5% → modal lemah (batas OJK)",
      "EmitenPerbankan(?e), npl(?e, ?n), greaterThan(?n, 5.0) -> BankModalLemah(?e)")
    R("R-RISK-04", "Fundamental-Risiko", "Going concern: distress + DER > 1,5",
      "ZonaDistress(?e), der(?e, ?d), greaterThan(?d, 1.5) -> RisikoGoingConcern(?e)")
    R("R-RISK-05", "Fundamental-Risiko", "Going concern: distress + arus kas lemah (CFO/laba < 0,7)",
      "ZonaDistress(?e), cfoPerLabaBersih(?e, ?c), lessThan(?c, 0.7) -> RisikoGoingConcern(?e)")
    R("R-RISK-06", "Fundamental-Risiko", "Going concern: merugi + distress",
      "ZonaDistress(?e), EmitenMerugi(?e) -> RisikoGoingConcern(?e)")
    R("R-RISK-07", "Fundamental-Risiko", "Beneish M > -1,78 → indikasi manipulasi laba",
      "Emiten(?e), beneishM(?e, ?m), greaterThan(?m, -1.78) -> RisikoManipulasiLaba(?e)")

    # ================================================================= TEKNIKAL
    R("R-TEK-01a", "Teknikal", "Tren naik penuh: harga > MA50, harga > MA200, MA50 > MA200 → 3 poin",
      "Emiten(?e), jarakMA200Persen(?e, ?a), greaterThanOrEqual(?a, 0.0), jarakMA50Persen(?e, ?b), greaterThanOrEqual(?b, 0.0), selisihMA50MA200Persen(?e, ?c), greaterThanOrEqual(?c, 0.0) -> poinTren(?e, 3), TrenNaik(?e)")
    R("R-TEK-01b", "Teknikal", "Pullback dalam uptrend: harga > MA200, harga < MA50 → 2 poin",
      "Emiten(?e), jarakMA200Persen(?e, ?a), greaterThanOrEqual(?a, 0.0), jarakMA50Persen(?e, ?b), lessThan(?b, 0.0) -> poinTren(?e, 2), PullbackDalamUptrend(?e)")
    R("R-TEK-01c", "Teknikal", "Pemulihan awal: harga > MA50 & MA200 tetapi MA50 < MA200 (menuju golden cross) → 2 poin",
      "Emiten(?e), jarakMA200Persen(?e, ?a), greaterThanOrEqual(?a, 0.0), jarakMA50Persen(?e, ?b), greaterThanOrEqual(?b, 0.0), selisihMA50MA200Persen(?e, ?c), lessThan(?c, 0.0) -> poinTren(?e, 2)")
    R("R-TEK-01d", "Teknikal", "Rebound di bawah MA200: harga > MA50, harga < MA200 → 1 poin",
      "Emiten(?e), jarakMA200Persen(?e, ?a), lessThan(?a, 0.0), jarakMA50Persen(?e, ?b), greaterThanOrEqual(?b, 0.0) -> poinTren(?e, 1)")
    R("R-TEK-01e", "Teknikal", "Downtrend: harga < MA50 & < MA200 → 0 poin",
      "Emiten(?e), jarakMA200Persen(?e, ?a), lessThan(?a, 0.0), jarakMA50Persen(?e, ?b), lessThan(?b, 0.0) -> poinTren(?e, 0), TrenTurun(?e)")
    bins("R-TEK-02", "Teknikal", "Poin RSI-14", "rsi14", "poinRSI", "Emiten",
         [(None, 30.0, 1, "Oversold"), (30.0, 40.0, 1, None), (40.0, 65.0, 2, None), (65.0, 75.0, 1, None), (75.0, None, 0, "Overbought")])
    R("R-TEK-03a", "Teknikal", "MACD histogram positif → 1", "Emiten(?e), histogramMACD(?e, ?m), greaterThan(?m, 0) -> poinMACD(?e, 1)")
    R("R-TEK-03b", "Teknikal", "MACD histogram ≤ 0 → 0", "Emiten(?e), histogramMACD(?e, ?m), lessThanOrEqual(?m, 0) -> poinMACD(?e, 0)")
    bins("R-TEK-04", "Teknikal", "Poin volume", "rasioVolume", "poinVolume", "Emiten", [(1.5, None, 1, None), (None, 1.5, 0, None)])
    R("R-TEK-05", "Teknikal", "Lonjakan volume ≥ 2× rata-rata", "Emiten(?e), rasioVolume(?e, ?v), greaterThanOrEqual(?v, 2.0) -> LonjakanVolume(?e)")
    R("R-TEK-06", "Teknikal", "Skor teknikal = tren + RSI + MACD + volume (0-7)",
      "Emiten(?e), poinTren(?e, ?a), poinRSI(?e, ?b), poinMACD(?e, ?c), poinVolume(?e, ?d), add(?s, ?a, ?b, ?c, ?d) -> skorTeknikal(?e, ?s)")
    R("R-TEK-07", "Teknikal-Pola", "Pola chart bullish terkonfirmasi akumulasi bandar",
      "terdeteksiPola(?e, ?p), PolaBullish(?p), AkumulasiBandar(?e) -> KonfirmasiPolaBullish(?e)")
    R("R-TEK-08", "Teknikal-Pola", "Candlestick bullish terkonfirmasi akumulasi bandar",
      "terdeteksiPola(?e, ?p), CandlestickBullish(?p), AkumulasiBandar(?e) -> KonfirmasiPolaBullish(?e)")
    R("R-TEK-09", "Teknikal-Pola", "Pola bearish terkonfirmasi distribusi (acc/dist ≤ -10)",
      "terdeteksiPola(?e, ?p), PolaBearish(?p), skorAccDistBroker(?e, ?a), lessThanOrEqual(?a, -10.0) -> KonfirmasiPolaBearish(?e)")
    R("R-TEK-10", "Teknikal-Pola", "Candlestick bearish + downtrend",
      "terdeteksiPola(?e, ?p), CandlestickBearish(?p), TrenTurun(?e) -> KonfirmasiPolaBearish(?e)")

    # ================================================================= BANDARMOLOGY
    bins("R-BDR-01", "Bandarmology", "Poin Acc/Dist broker", "skorAccDistBroker", "poinAccDist", "Emiten",
         [(30.0, None, 3, None), (10.0, 30.0, 2, None), (-10.0, 10.0, 1, None), (None, -10.0, 0, None)])
    bins("R-BDR-02", "Bandarmology", "Poin net foreign 20 hari", "netAsing20HariM", "poinAsing", "Emiten",
         [(50.0, None, 2, "AsingAkumulasi"), (0.0, 50.0, 1, None), (-50.0, 0.0, 0, None), (None, -50.0, 0, "AsingDistribusi")])
    R("R-BDR-03", "Bandarmology", "Skor bandarmology = acc/dist + asing (0-5)",
      "Emiten(?e), poinAccDist(?e, ?a), poinAsing(?e, ?b), add(?s, ?a, ?b) -> skorBandar(?e, ?s)")
    R("R-BDR-04", "Bandarmology", "Akumulasi bandar: Acc/Dist ≥ 20", "Emiten(?e), skorAccDistBroker(?e, ?a), greaterThanOrEqual(?a, 20.0) -> AkumulasiBandar(?e)")
    R("R-BDR-05", "Bandarmology", "Distribusi bandar: Acc/Dist ≤ -20", "Emiten(?e), skorAccDistBroker(?e, ?a), lessThanOrEqual(?a, -20.0) -> DistribusiBandar(?e)")
    R("R-BDR-06", "Bandarmology", "Smart money divergence: bandar akumulasi saat harga turun & ritel jual (Wyckoff akumulasi)",
      "Emiten(?e), skorAccDistBroker(?e, ?a), greaterThanOrEqual(?a, 20.0), netRitel20HariM(?e, ?r), lessThan(?r, 0.0), perubahanHarga20HariPersen(?e, ?c), lessThan(?c, 0.0) -> AkumulasiTersembunyi(?e)")
    R("R-BDR-07", "Bandarmology", "Distribusi ke ritel: bandar jual, broker ritel net buy",
      "Emiten(?e), skorAccDistBroker(?e, ?a), lessThanOrEqual(?a, -10.0), netRitel20HariM(?e, ?r), greaterThan(?r, 0.0) -> DistribusiKeRitel(?e)")
    R("R-BDR-08", "Bandarmology-Wyckoff", "Fase akumulasi: akumulasi di bawah MA200",
      "Emiten(?e), skorAccDistBroker(?e, ?a), greaterThanOrEqual(?a, 20.0), jarakMA200Persen(?e, ?m), lessThan(?m, 0.0) -> FaseAkumulasiWyckoff(?e)")
    R("R-BDR-09", "Bandarmology-Wyckoff", "Fase mark-up: akumulasi + di atas MA200 + MA50 > MA200",
      "Emiten(?e), skorAccDistBroker(?e, ?a), greaterThanOrEqual(?a, 10.0), jarakMA200Persen(?e, ?m), greaterThanOrEqual(?m, 0.0), selisihMA50MA200Persen(?e, ?s), greaterThanOrEqual(?s, 0.0) -> FaseMarkUpWyckoff(?e)")
    R("R-BDR-10", "Bandarmology-Wyckoff", "Fase distribusi: bandar jual saat RSI tinggi",
      "Emiten(?e), skorAccDistBroker(?e, ?a), lessThanOrEqual(?a, -10.0), rsi14(?e, ?r), greaterThanOrEqual(?r, 65.0) -> FaseDistribusiWyckoff(?e)")
    R("R-BDR-11", "Bandarmology-Wyckoff", "Fase mark-down: bandar jual + di bawah MA200",
      "Emiten(?e), skorAccDistBroker(?e, ?a), lessThanOrEqual(?a, -10.0), jarakMA200Persen(?e, ?m), lessThan(?m, 0.0) -> FaseMarkDownWyckoff(?e)")
    R("R-BDR-12", "Bandarmology-Broker", "Akumulator utama broker asing + akumulasi → akumulasi institusi asing",
      "brokerAkumulatorUtama(?e, ?b), BrokerAsing(?b), AkumulasiBandar(?e) -> AkumulasiInstitusiAsing(?e)")
    R("R-BDR-13", "Bandarmology-Broker", "Pembeli utama broker ritel → waspada (exit liquidity)",
      "brokerAkumulatorUtama(?e, ?b), BrokerRitel(?b) -> AkumulasiDidominasiRitel(?e)")

    # ================================================================= SENTIMEN
    bins("R-SEN-01", "Sentimen", "Poin sentimen emiten", "skorSentimenEmiten", "skorSentimen", "Emiten",
         [(0.3, None, 2, None), (0.1, 0.3, 1, None), (-0.1, 0.1, 0, None), (-0.3, -0.1, -1, None), (None, -0.3, -2, None)])
    R("R-SEN-02", "Sentimen", "Sentimen positif ≥ 0,2", "Emiten(?e), skorSentimenEmiten(?e, ?s), greaterThanOrEqual(?s, 0.2) -> SentimenPositif(?e)")
    R("R-SEN-03", "Sentimen", "Sentimen negatif ≤ -0,2", "Emiten(?e), skorSentimenEmiten(?e, ?s), lessThanOrEqual(?s, -0.2) -> SentimenNegatif(?e)")
    R("R-SEN-04", "Sentimen", "Red flag: berita kredibel (≥0,8) bernada sangat negatif (≤ -0,4) dalam 180 hari",
      "Berita(?n), tentangEmiten(?n, ?e), skorSentimenBerita(?n, ?s), lessThanOrEqual(?s, -0.4), kredibilitasSumber(?n, ?c), greaterThanOrEqual(?c, 0.8), umurHari(?n, ?d), lessThanOrEqual(?d, 180) -> RedFlagBerita(?e), memilikiRedFlag(?e, ?n)")
    bins("R-SEN-05", "Sentimen", "Poin sentimen sektor", "skorSentimenSektor", "poinSentimenSektor", "Sektor",
         [(0.3, None, 2, None), (0.1, 0.3, 1, None), (-0.1, 0.1, 0, None), (-0.3, -0.1, -1, None), (None, -0.3, -2, None)])

    # ================================================================= GEOPOLITIK & MAKRO (multi-hop)
    R("R-GEO-01", "Geopolitik", "Peristiwa aktif bila dikonfirmasi berita kredibel (≥ 0,7) berumur ≤ 180 hari",
      "Berita(?n), tentangPeristiwa(?n, ?ev), kredibilitasSumber(?n, ?c), greaterThanOrEqual(?c, 0.7), umurHari(?n, ?d), lessThanOrEqual(?d, 180) -> PeristiwaAktif(?ev)")
    R("R-GEO-02", "Geopolitik", "Kebijakan domestik yang masih berjalan selalu aktif",
      "KebijakanDomestik(?ev), statusKebijakanBerjalan(?ev, 1) -> PeristiwaAktif(?ev)")
    R("R-GEO-03", "Geopolitik", "Hop-1: peristiwa aktif memicu node transmisi",
      "PeristiwaAktif(?ev), memicuPergerakan(?ev, ?m) -> PergerakanAktif(?m)")
    R("R-GEO-04", "Geopolitik", "Hop-n: propagasi kausal antar node transmisi (multi-hop)",
      "PergerakanAktif(?m), menyebabkan(?m, ?n) -> PergerakanAktif(?n)")
    R("R-GEO-05", "Geopolitik", "Provenans geopolitik: node yang dipicu peristiwa global aktif",
      "PeristiwaAktif(?ev), PeristiwaGlobal(?ev), memicuPergerakan(?ev, ?m) -> PergerakanGeopolitik(?m)")
    R("R-GEO-06", "Geopolitik", "Provenans geopolitik diturunkan sepanjang rantai kausal aktif",
      "PergerakanGeopolitik(?m), PergerakanAktif(?m), menyebabkan(?m, ?n) -> PergerakanGeopolitik(?n)")
    R("R-GEO-07", "Geopolitik", "Tailwind sektor dari node aktif", "PergerakanAktif(?m), menguntungkanSektor(?m, ?s) -> memilikiTailwind(?s, ?m)")
    R("R-GEO-08", "Geopolitik", "Headwind sektor dari node aktif", "PergerakanAktif(?m), merugikanSektor(?m, ?s) -> memilikiHeadwind(?s, ?m)")
    R("R-GEO-09", "Geopolitik", "Peluang kontrarian (diskon teknikal/pasif)",
      "PergerakanAktif(?m), menciptakanPeluangKontrarian(?m, ?s) -> memilikiPeluangKontrarian(?s, ?m), SektorPeluangKontrarian(?s)")
    R("R-GEO-10", "Geopolitik", "Sektor diuntungkan geopolitik", "memilikiTailwind(?s, ?m), PergerakanGeopolitik(?m), PergerakanAktif(?m) -> SektorDiuntungkanGeopolitik(?s)")
    R("R-GEO-11", "Geopolitik", "Sektor dirugikan geopolitik", "memilikiHeadwind(?s, ?m), PergerakanGeopolitik(?m), PergerakanAktif(?m) -> SektorDirugikanGeopolitik(?s)")
    R("R-GEO-12", "Geopolitik→Emiten", "Routing ke emiten: komoditas pendapatan naik",
      "PergerakanAktif(?m), menaikkanHargaKomoditas(?m, ?k), eksposurKomoditasPendapatan(?e, ?k) -> diuntungkanOleh(?e, ?m), PenerimaManfaatKomoditas(?e)")
    R("R-GEO-13", "Geopolitik→Emiten", "Routing ke emiten: komoditas biaya naik",
      "PergerakanAktif(?m), menaikkanHargaKomoditas(?m, ?k), eksposurKomoditasBiaya(?e, ?k) -> ditekanOleh(?e, ?m), KorbanKenaikanKomoditas(?e)")
    R("R-GEO-14", "Geopolitik→Emiten", "Routing ke emiten: komoditas pendapatan turun",
      "PergerakanAktif(?m), menurunkanHargaKomoditas(?m, ?k), eksposurKomoditasPendapatan(?e, ?k) -> ditekanOleh(?e, ?m)")
    R("R-GEO-15", "Geopolitik→Emiten", "Keputusan penyedia indeks aktif → risiko outflow pasif konstituen",
      "KeputusanPenyediaIndeks(?ev), PeristiwaAktif(?ev), berdampakPadaIndeks(?ev, ?i), anggotaIndeks(?e, ?i) -> RisikoOutflowPasif(?e)")

    # ================================================================= PENILAIAN SEKTOR PER SKENARIO
    R("R-SKN-01", "Skenario", "Skenario aktif dipilih (statusAktif = 1)", "Skenario(?sc), statusAktif(?sc, 1) -> SkenarioAktif(?sc)")
    atoms, prods = [], []
    for i, f in enumerate(FAKTOR):
        atoms.append(f"sens{f}(?s, ?x{i}), arah{f}(?sc, ?y{i}), multiply(?p{i}, ?x{i}, ?y{i})")
        prods.append(f"?p{i}")
    # Dipecah 2 bagian karena SWRLTab/Drools hanya menerima maks. 11 argumen per built-in
    R("R-SEK-01a", "Makro-Geopolitik", "Skor makro-geo bagian A = Σ sensitivitas × arah (faktor 1-6: energi, USD, suku bunga, inflasi, emas, logam/China)",
      "PenilaianSektor(?a), menilaiSektor(?a, ?s), dibawahSkenario(?a, ?sc), " + ", ".join(atoms[:6]) + f", add(?t, {', '.join(prods[:6])}) -> skorMakroGeoA(?a, ?t)")
    R("R-SEK-01b", "Makro-Geopolitik", "Skor makro-geo bagian B = Σ sensitivitas × arah (faktor 7-12: risk-off, belanja pemerintah, daya beli, tarif, CPO, digital)",
      "PenilaianSektor(?a), menilaiSektor(?a, ?s), dibawahSkenario(?a, ?sc), " + ", ".join(atoms[6:]) + f", add(?t, {', '.join(prods[6:])}) -> skorMakroGeoB(?a, ?t)")
    R("R-SEK-01c", "Makro-Geopolitik", "Skor makro-geo = bagian A + bagian B (12 faktor)",
      "PenilaianSektor(?a), skorMakroGeoA(?a, ?x), skorMakroGeoB(?a, ?y), add(?t, ?x, ?y) -> skorMakroGeo(?a, ?t)")
    R("R-SEK-02", "Fundamental-Sektor", "Rasio valuasi sektor = PER / PER 5 th",
      "Sektor(?s), perSektor(?s, ?p), per5TahunSektor(?s, ?q), divide(?r, ?p, ?q) -> rasioValuasiSektor(?s, ?r)")
    bins("R-SEK-03", "Fundamental-Sektor", "Skor valuasi sektor", "rasioValuasiSektor", "skorValuasiSektor", "Sektor",
         [(None, 0.6, 3, "SektorMurahHistoris"), (0.6, 0.85, 2, "SektorMurahHistoris"), (0.85, 1.1, 1, None), (1.1, None, 0, None)])
    R("R-SEK-04", "Tema Struktural", "Skor tema tertimbang = tema × 2", "Sektor(?s), skorTemaStruktural(?s, ?t), multiply(?w, ?t, 2) -> skorTemaTertimbang(?s, ?w)")
    R("R-SEK-05", "Tema Struktural", "Sektor didukung tema (skor ≥ 2)", "Sektor(?s), skorTemaStruktural(?s, ?t), greaterThanOrEqual(?t, 2) -> SektorDidukungTema(?s)")
    bins("R-SEK-06", "Bandarmology-Sektor", "Poin aliran asing sektor 3 bulan", "aliranAsing3BulanT", "poinAliranAsing", "Sektor",
         [(1.0, None, 2, None), (0.0, 1.0, 1, None), (-5.0, 0.0, 0, None), (None, -5.0, -1, None)])
    for fase, prop in [("Fase_EarlyCycle", "skorFaseEarly"), ("Fase_MidCycle", "skorFaseMid"), ("Fase_LateCycle", "skorFaseLate"), ("Fase_ResesiStagflasi", "skorFaseResesi")]:
        R(f"R-ROT-{fase[5:]}", "Rotasi Sektor", f"Skor rotasi bila skenario berada di {fase}",
          f"PenilaianSektor(?a), dibawahSkenario(?a, ?sc), faseSiklus(?sc, {fase}), menilaiSektor(?a, ?s), {prop}(?s, ?v) -> skorRotasi(?a, ?v)")
    R("R-SEK-07", "Integrasi", "SKOR OUTLOOK = makro-geo + valuasi + tema×2 + sentimen + aliran asing + rotasi",
      "PenilaianSektor(?a), menilaiSektor(?a, ?s), skorMakroGeo(?a, ?m), skorRotasi(?a, ?r), skorValuasiSektor(?s, ?v), skorTemaTertimbang(?s, ?t), poinSentimenSektor(?s, ?n), poinAliranAsing(?s, ?f), add(?o, ?m, ?r, ?v, ?t, ?n, ?f) -> skorOutlook(?a, ?o)")
    for j, (lo, hi, k) in enumerate([(12, None, "PenilaianBullishKuat"), (7, 12, "PenilaianBullishModerat"), (2, 7, "PenilaianNetral"), (None, 2, "PenilaianBearish")]):
        cond = ["skorOutlook(?a, ?o)"] + ([f"greaterThanOrEqual(?o, {lo})"] if lo is not None else []) + ([f"lessThan(?o, {hi})"] if hi is not None else [])
        R(f"R-SEK-08{chr(97 + j)}", "Integrasi", f"Kelas penilaian {k}", "PenilaianSektor(?a), " + ", ".join(cond) + f" -> {k}(?a)")
    R("R-SEK-09", "Skenario", "Penilaian di skenario aktif", "PenilaianSektor(?a), dibawahSkenario(?a, ?sc), SkenarioAktif(?sc) -> PenilaianAktif(?a)")
    R("R-SEK-10", "Skenario", "Skor outlook sektor mengikuti skenario aktif", "PenilaianAktif(?a), menilaiSektor(?a, ?s), skorOutlook(?a, ?o) -> skorOutlookAktif(?s, ?o)")
    R("R-SEK-11", "Rotasi Sektor", "Sektor favorit fase siklus (rotasi ≥ 2 di skenario aktif)",
      "PenilaianAktif(?a), menilaiSektor(?a, ?s), skorRotasi(?a, ?r), greaterThanOrEqual(?r, 2) -> SektorFavoritSiklus(?s)")
    for j, (lo, hi, k) in enumerate([(12, None, "SektorBullishKuat"), (7, 12, "SektorBullishModerat"), (2, 7, "SektorNetral"), (None, 2, "SektorBearish")]):
        cond = ["skorOutlookAktif(?s, ?o)"] + ([f"greaterThanOrEqual(?o, {lo})"] if lo is not None else []) + ([f"lessThan(?o, {hi})"] if hi is not None else [])
        R(f"R-SEK-12{chr(97 + j)}", "Prediksi Sektor", f"PREDIKSI 1-3 TH: {k}", "Sektor(?s), " + ", ".join(cond) + f" -> {k}(?s)")
    R("R-SEK-13a", "Prediksi Sektor", "Bullish kuat ⊂ bullish", "SektorBullishKuat(?s) -> SektorBullish(?s)")
    R("R-SEK-13b", "Prediksi Sektor", "Bullish moderat ⊂ bullish", "SektorBullishModerat(?s) -> SektorBullish(?s)")
    R("R-SEK-14", "Prediksi Sektor", "Keyakinan tinggi: bullish + preseden historis + tema struktural (konfluensi)",
      "SektorBullish(?s), SektorPresedenHistoris(?s), SektorDidukungTema(?s) -> SektorKeyakinanTinggi(?s)")

    # ================================================================= CBR
    cb = [("cbrFed", 2), ("cbrMinyak", 2), ("cbrUSD", 2), ("cbrRiskOff", 1), ("cbrKomoditas", 1), ("cbrInflasi", 1)]
    at, ws = [], []
    for i, (f, w) in enumerate(cb):
        at.append(f"{f}(?sc, ?a{i}), {f}(?p, ?b{i}), subtract(?d{i}, ?a{i}, ?b{i}), abs(?g{i}, ?d{i}), multiply(?w{i}, ?g{i}, {w})")
        ws.append(f"?w{i}")
    R("R-CBR-01", "Case-Based Reasoning", "Skor kemiripan = 20 - Σ bobot × |fitur skenario - fitur kasus| (bobot Fed, minyak, USD = 2)",
      "SkenarioAktif(?sc), PeriodeHistoris(?p), " + ", ".join(at) + f", add(?dist, {', '.join(ws)}), subtract(?sim, 20, ?dist) -> skorKemiripan(?p, ?sim)")
    R("R-CBR-02", "Case-Based Reasoning", "Periode analog bila kemiripan ≥ 13",
      "SkenarioAktif(?sc), PeriodeHistoris(?p), skorKemiripan(?p, ?k), greaterThanOrEqual(?k, 13) -> PeriodeAnalog(?p), analogDengan(?sc, ?p)")
    R("R-CBR-03", "Case-Based Reasoning", "Sektor pemenang periode analog → preseden historis",
      "PeriodeAnalog(?p), unggulPadaPeriode(?p, ?s) -> SektorPresedenHistoris(?s), memilikiPreseden(?s, ?p)")

    # ================================================================= INTEGRASI EMITEN
    for j, (lo, hi, pts) in enumerate([(12, None, 4), (7, 12, 2), (2, 7, 0), (None, 2, -3)]):
        cond = ["skorOutlookAktif(?s, ?o)"] + ([f"greaterThanOrEqual(?o, {lo})"] if lo is not None else []) + ([f"lessThan(?o, {hi})"] if hi is not None else [])
        R(f"R-EMT-01{chr(97 + j)}", "Integrasi", f"Kontribusi outlook sektor ke emiten = {pts}",
          "Emiten(?e), termasukSektor(?e, ?s), " + ", ".join(cond) + f" -> skorKontribusiSektor(?e, {pts})")
    bins("R-EMT-02", "Likuiditas", "Poin likuiditas (nilai transaksi harian)", "likuiditasHarianM", "poinLikuiditas", "Emiten",
         [(100.0, None, 2, None), (20.0, 100.0, 1, None), (None, 20.0, 0, None)])
    R("R-EMT-03", "Integrasi", "SKOR TOTAL EMITEN = fundamental + valuasi + teknikal + bandar + sentimen + sektor + risiko + likuiditas",
      "Emiten(?e), skorFundamental(?e, ?a), skorValuasi(?e, ?b), skorTeknikal(?e, ?c), skorBandar(?e, ?d), skorSentimen(?e, ?f), skorKontribusiSektor(?e, ?g), penaltiRisiko(?e, ?h), poinLikuiditas(?e, ?i), add(?t, ?a, ?b, ?c, ?d, ?f, ?g, ?h, ?i) -> skorTotalEmiten(?e, ?t)")
    R("R-EMT-04", "Integrasi", "Kandidat top pick: skor total ≥ 21 di sektor bullish",
      "Emiten(?e), termasukSektor(?e, ?s), SektorBullish(?s), skorTotalEmiten(?e, ?t), greaterThanOrEqual(?t, 21) -> KandidatTopPick(?e), topPickSektor(?s, ?e)")
    R("R-EMT-05", "Integrasi", "Watchlist: skor total 16-20 di sektor bullish",
      "Emiten(?e), termasukSektor(?e, ?s), SektorBullish(?s), skorTotalEmiten(?e, ?t), greaterThanOrEqual(?t, 16), lessThan(?t, 21) -> KandidatWatchlist(?e), watchlistSektor(?s, ?e)")
    R("R-EMT-06", "Integrasi", "Keyakinan tinggi: top pick + akumulasi bandar + fundamental kuat",
      "KandidatTopPick(?e), AkumulasiBandar(?e), FundamentalKuat(?e) -> KeyakinanTinggi(?e)")
    R("R-EMT-07", "Peringatan", "Value trap: murah tetapi fundamental lemah & downtrend",
      "Emiten(?e), skorValuasi(?e, ?v), greaterThanOrEqual(?v, 2), FundamentalLemah(?e), jarakMA200Persen(?e, ?m), lessThan(?m, 0.0) -> ValueTrap(?e)")
    R("R-EMT-08", "Integrasi", "Defensif berkualitas: sektor defensif + fundamental kuat + zona aman + yield ≥ 4%",
      "Emiten(?e), termasukSektor(?e, ?s), SektorDefensif(?s), FundamentalKuat(?e), penaltiRisiko(?e, ?p), equal(?p, 0), dividendYield(?e, ?y), greaterThanOrEqual(?y, 4.0) -> DefensifBerkualitas(?e)")

    # ================================================================= SINYAL QUANT TRADE
    R("R-SIG-01", "Quant Trade", "ATR rupiah = harga × ATR% / 100",
      "Emiten(?e), hargaPenutupan(?e, ?h), atrPersen(?e, ?a), multiply(?x, ?h, ?a), divide(?r, ?x, 100.0) -> atrRupiah(?e, ?r)")
    R("R-SIG-02", "Quant Trade", "Sinyal entry: teknikal ≥ 5, bandar ≥ 3, RSI < 70",
      "Emiten(?e), skorTeknikal(?e, ?t), greaterThanOrEqual(?t, 5), skorBandar(?e, ?b), greaterThanOrEqual(?b, 3), rsi14(?e, ?r), lessThan(?r, 70.0) -> SinyalEntry(?e)")
    R("R-SIG-03", "Quant Trade", "Buy on weakness: fundamental kuat, pullback dalam uptrend, RSI < 50, acc/dist ≥ 10",
      "FundamentalKuat(?e), PullbackDalamUptrend(?e), rsi14(?e, ?r), lessThan(?r, 50.0), skorAccDistBroker(?e, ?a), greaterThanOrEqual(?a, 10.0) -> SinyalBuyOnWeakness(?e)")
    R("R-SIG-04", "Quant Trade", "Buy on weakness kontrarian: fundamental kuat + undervalued + akumulasi tersembunyi + tanpa penalti risiko",
      "FundamentalKuat(?e), Undervalued(?e), AkumulasiTersembunyi(?e), penaltiRisiko(?e, ?p), equal(?p, 0) -> SinyalBuyOnWeakness(?e)")
    R("R-SIG-05", "Quant Trade", "Stop loss & take profit untuk sinyal entry (SL = H - 2×ATR, TP = H + 3×ATR)",
      "SinyalEntry(?e), hargaPenutupan(?e, ?h), atrRupiah(?e, ?a), multiply(?a2, ?a, 2.0), multiply(?a3, ?a, 3.0), subtract(?sl, ?h, ?a2), add(?tp, ?h, ?a3) -> hargaStopLoss(?e, ?sl), hargaTakeProfit(?e, ?tp)")
    R("R-SIG-06", "Quant Trade", "Stop loss & take profit untuk buy on weakness",
      "SinyalBuyOnWeakness(?e), hargaPenutupan(?e, ?h), atrRupiah(?e, ?a), multiply(?a2, ?a, 2.0), multiply(?a3, ?a, 3.0), subtract(?sl, ?h, ?a2), add(?tp, ?h, ?a3) -> hargaStopLoss(?e, ?sl), hargaTakeProfit(?e, ?tp)")
    R("R-SIG-07", "Quant Trade", "Exit/take profit: overbought + distribusi",
      "Overbought(?e), skorAccDistBroker(?e, ?a), lessThanOrEqual(?a, -10.0) -> SinyalExit(?e)")
    R("R-SIG-08", "Quant Trade", "Exit: konfirmasi pola bearish + asing distribusi", "KonfirmasiPolaBearish(?e), AsingDistribusi(?e) -> SinyalExit(?e)")
    R("R-SIG-09", "Quant Trade", "Hindari: downtrend + asing jual + bandar distribusi",
      "TrenTurun(?e), netAsing20HariM(?e, ?f), lessThan(?f, -50.0), skorAccDistBroker(?e, ?a), lessThanOrEqual(?a, -10.0) -> SinyalHindari(?e)")
    R("R-SIG-10", "Quant Trade", "Hindari: risiko going concern", "RisikoGoingConcern(?e) -> SinyalHindari(?e)")
    R("R-SIG-11", "Scalper Pattern", "Scalping long: volume ≥ 2×, di atas VWAP, bid/offer ≥ 1,5, likuid, free float ≥ 15% (bukan saham gorengan)",
      "Emiten(?e), rasioVolume(?e, ?v), greaterThanOrEqual(?v, 2.0), jarakVWAPPersen(?e, ?w), greaterThan(?w, 0.0), rasioBidOffer(?e, ?b), greaterThanOrEqual(?b, 1.5), likuiditasHarianM(?e, ?l), greaterThanOrEqual(?l, 20.0), freeFloatPersen(?e, ?f), greaterThanOrEqual(?f, 15.0) -> SinyalScalpingLong(?e)")
    R("R-SIG-12", "Scalper Pattern", "Scalping hindari: volume tinggi di bawah VWAP & tekanan offer",
      "Emiten(?e), rasioVolume(?e, ?v), greaterThanOrEqual(?v, 1.5), jarakVWAPPersen(?e, ?w), lessThan(?w, 0.0), rasioBidOffer(?e, ?b), lessThan(?b, 0.8) -> SinyalScalpingHindari(?e)")

    # ================================================================= STAKEHOLDER / PROFIL
    R("R-PRF-01", "Profil Investor", "Cocok konservatif: fundamental kuat, tanpa penalti, yield ≥ 5%, likuid",
      "FundamentalKuat(?e), penaltiRisiko(?e, ?p), equal(?p, 0), dividendYield(?e, ?y), greaterThanOrEqual(?y, 5.0), likuiditasHarianM(?e, ?l), greaterThanOrEqual(?l, 50.0) -> CocokKonservatif(?e)")
    R("R-PRF-02", "Profil Investor", "Cocok moderat: skor total ≥ 20, fundamental ≥ 5, penalti ≥ -1",
      "Emiten(?e), skorTotalEmiten(?e, ?t), greaterThanOrEqual(?t, 20), skorFundamental(?e, ?f), greaterThanOrEqual(?f, 5), penaltiRisiko(?e, ?p), greaterThanOrEqual(?p, -1) -> CocokModerat(?e)")
    R("R-PRF-03", "Profil Investor", "Cocok agresif: teknikal ≥ 5 & bandar ≥ 3",
      "Emiten(?e), skorTeknikal(?e, ?t), greaterThanOrEqual(?t, 5), skorBandar(?e, ?b), greaterThanOrEqual(?b, 3) -> CocokAgresif(?e)")
    R("R-PRF-04", "Stakeholder", "Rekomendasi persona konservatif",
      "InvestorRitel(?i), memilikiProfilRisiko(?i, ProfilKonservatif), CocokKonservatif(?e) -> direkomendasikanUntuk(?e, ?i)")
    R("R-PRF-05", "Stakeholder", "Rekomendasi persona moderat (hanya sektor bullish)",
      "InvestorRitel(?i), memilikiProfilRisiko(?i, ProfilModerat), CocokModerat(?e), termasukSektor(?e, ?s), SektorBullish(?s) -> direkomendasikanUntuk(?e, ?i)")
    R("R-PRF-06", "Stakeholder", "Rekomendasi persona agresif horizon pendek (swing)",
      "InvestorRitel(?i), memilikiProfilRisiko(?i, ProfilAgresif), memilikiHorizon(?i, Horizon_Pendek), CocokAgresif(?e), SinyalEntry(?e) -> direkomendasikanUntuk(?e, ?i)")
    R("R-PRF-07", "Stakeholder", "Rekomendasi scalper intraday",
      "InvestorRitel(?i), memilikiHorizon(?i, Horizon_Intraday), SinyalScalpingLong(?e) -> direkomendasikanUntuk(?e, ?i)")

    from rules_v2 import add_v2
    add_v2(R, bins, None)
    return RULES

def build_rules(onto, FAKTOR, kodeAturan, pilarAnalisis):
    define_rules(FAKTOR)
    imps = []
    with onto:
        for code, pilar, desc, body in RULES:
            imp = Imp(name="Aturan_" + code.replace("-", "_"))
            imp.set_as_rule(body)
            imp.label = [code]
            imp.comment = [locstr(f"[{pilar}] {desc}", lang="id")]
            imp.kodeAturan = [code]
            imp.pilarAnalisis = [pilar]
            imps.append(imp)
    return imps
