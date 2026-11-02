# -*- coding: utf-8 -*-
"""
RBox v2 — MODUL PAKAR LANJUTAN (yang membedakan sistem pakar dari analis biasa).
Dipanggil dari rules_swrl.define_rules().
"""

def add_v2(R, bins, REGIME_NAMES):
    # ================================================================ KUALITAS DATA
    R("R-DAT-01", "Kualitas Data", "Data kedaluwarsa bila umur > 5 × frekuensi pembaruan",
      "IndikatorMakro(?i), umurDataHari(?i, ?u), frekuensiHari(?i, ?f), multiply(?b, ?f, 5), greaterThan(?u, ?b) -> DataKedaluwarsa(?i)")
    R("R-DAT-02", "Kualitas Data", "Top pick adaptif berbasis data indikatif wajib diverifikasi",
      "DataIndikatif(?e), KandidatTopPickAdaptif(?e) -> PerluVerifikasiData(?e)")
    R("R-DAT-03", "Kualitas Data", "Kandidat akumulasi bertahap berbasis data indikatif wajib diverifikasi",
      "DataIndikatif(?e), KandidatAkumulasiBertahap(?e) -> PerluVerifikasiData(?e)")
    R("R-DAT-04", "Kualitas Data", "Tesis dengan indikator kunci kedaluwarsa perlu data baru",
      "TesisInvestasi(?t), indikatorKunciTesis(?t, ?i), DataKedaluwarsa(?i) -> TesisPerluDataBaru(?t)")

    # ================================================================ KONDISI PASAR & REGIME
    R("R-PAS-00", "Regime Pasar", "Kondisi pasar aktif (statusAktifKondisi = 1)",
      "KondisiPasar(?k), statusAktifKondisi(?k, 1) -> KondisiPasarAktif(?k)")
    V = "KondisiPasarAktif"
    bins("R-STR-01", "Regime Pasar", "Poin stres drawdown IHSG", "drawdownIHSGPersen", "poinStresDrawdown", V,
         [(None, -30.0, 2, None), (-30.0, -15.0, 1, None), (-15.0, None, 0, None)])
    bins("R-STR-02", "Regime Pasar", "Poin stres CDS 5Y", "cds5YBps", "poinStresCDS", V,
         [(120.0, None, 2, None), (80.0, 120.0, 1, None), (None, 80.0, 0, None)])
    bins("R-STR-03", "Regime Pasar", "Poin stres net asing YTD", "netAsingYTDT", "poinStresAsing", V,
         [(None, -50.0, 2, None), (-50.0, -10.0, 1, None), (-10.0, None, 0, None)])
    bins("R-STR-04", "Regime Pasar", "Poin stres kurs USD/IDR", "kursUSDIDR", "poinStresKurs", V,
         [(17500.0, None, 2, None), (16500.0, 17500.0, 1, None), (None, 16500.0, 0, None)])
    bins("R-STR-05", "Regime Pasar", "Poin stres yield SBN 10Y", "yieldSBN10Y", "poinStresYield", V,
         [(7.5, None, 2, None), (6.75, 7.5, 1, None), (None, 6.75, 0, None)])
    bins("R-STR-06", "Regime Pasar", "Poin stres breadth (% saham > MA200)", "breadthPersenDiAtasMA200", "poinStresBreadth", V,
         [(None, 25.0, 2, None), (25.0, 50.0, 1, None), (50.0, None, 0, None)])
    R("R-STR-07", "Regime Pasar", "Skor stres pasar = Σ 6 poin stres (0-12)",
      "KondisiPasarAktif(?k), poinStresDrawdown(?k, ?a), poinStresCDS(?k, ?b), poinStresAsing(?k, ?c), poinStresKurs(?k, ?d), poinStresYield(?k, ?f), poinStresBreadth(?k, ?g), add(?s, ?a, ?b, ?c, ?d, ?f, ?g) -> skorStresPasar(?k, ?s)")
    for j, (lo, hi, reg) in enumerate([(8, None, "Regime_KrisisLikuiditas"), (5, 8, "Regime_RiskOff"), (3, 5, "Regime_Netral"), (None, 3, "Regime_RiskOn")]):
        cond = ["skorStresPasar(?k, ?s)"] + ([f"greaterThanOrEqual(?s, {lo})"] if lo is not None else []) + ([f"lessThan(?s, {hi})"] if hi is not None else [])
        R(f"R-REG-0{j + 1}", "Regime Pasar", f"Deteksi regime: {reg}",
          "KondisiPasarAktif(?k), " + ", ".join(cond) + f" -> regimeTerdeteksi(?k, {reg}), RegimeAktif({reg})")
    R("R-PAS-01", "Struktur Pasar", "Premi risiko negara tinggi: CDS ≥ 90 bps",
      "KondisiPasarAktif(?k), cds5YBps(?k, ?c), greaterThanOrEqual(?c, 90.0) -> PremiRisikoNegaraTinggi(?k)")
    R("R-PAS-02", "Struktur Pasar", "Breadth washout: < 25% saham di atas MA200",
      "KondisiPasarAktif(?k), breadthPersenDiAtasMA200(?k, ?b), lessThan(?b, 25.0) -> BreadthWashout(?k)")
    R("R-PAS-03", "Struktur Pasar", "Kapitulasi pasar: drawdown ≤ -40% & hari crash ≤ -10%",
      "KondisiPasarAktif(?k), drawdownIHSGPersen(?k, ?d), lessThanOrEqual(?d, -40.0), penurunanHarianTerbesarPersen(?k, ?x), lessThanOrEqual(?x, -10.0) -> KapitulasiPasar(?k)")
    R("R-PAS-04", "Struktur Pasar", "Zona akumulasi generasional: kapitulasi + washout + premi risiko tinggi",
      "KapitulasiPasar(?k), BreadthWashout(?k), PremiRisikoNegaraTinggi(?k) -> ZonaAkumulasiGenerasional(?k)")
    R("R-PAS-05", "Intermarket", "Dasar belum terkonfirmasi: CDS & rupiah masih memburuk",
      "KondisiPasarAktif(?k), trenCDS1Bulan(?k, ?c), greaterThanOrEqual(?c, 1), trenRupiah1Bulan(?k, ?r), greaterThanOrEqual(?r, 1) -> DasarBelumTerkonfirmasi(?k)")
    R("R-PAS-06", "Intermarket", "Divergensi intermarket bullish: CDS & rupiah membaik saat IHSG masih turun",
      "KondisiPasarAktif(?k), trenCDS1Bulan(?k, ?c), lessThanOrEqual(?c, -1), trenRupiah1Bulan(?k, ?r), lessThanOrEqual(?r, -1), perubahanIHSG1BulanPersen(?k, ?m), lessThan(?m, 0.0) -> DivergensiIntermarketBullish(?k)")
    R("R-PAS-07", "Struktur Pasar", "Zona akumulasi tetapi dasar belum terkonfirmasi → akumulasi bertahap",
      "ZonaAkumulasiGenerasional(?k), DasarBelumTerkonfirmasi(?k) -> StrategiAkumulasiBertahap(?k)")
    R("R-PAS-08", "Struktur Pasar", "Kapitulasi + divergensi intermarket → akumulasi bertahap",
      "KapitulasiPasar(?k), DivergensiIntermarketBullish(?k) -> StrategiAkumulasiBertahap(?k)")

    # ================================================================ REACTION FUNCTION (antisipatif)
    R("R-ANT-01", "Reaction Function", "Rupiah ≥ 17.500 & inflasi ≥ 3% → antisipasi BI naik pre-emptif",
      "KondisiPasarAktif(?k), kursUSDIDR(?k, ?u), greaterThanOrEqual(?u, 17500.0), inflasiYoY(?k, ?i), greaterThanOrEqual(?i, 3.0) -> AntisipasiTerpicu(Antisipasi_BIHikePreemptif), PergerakanAktif(Mv_SukuBungaBINaik)")
    R("R-ANT-02", "Reaction Function", "Brent ≥ US$100 → antisipasi penyesuaian BBM/subsidi",
      "KondisiPasarAktif(?k), brentUSD(?k, ?b), greaterThanOrEqual(?b, 100.0) -> AntisipasiTerpicu(Antisipasi_PenyesuaianBBM), PergerakanAktif(Mv_KenaikanHargaBBM)")
    R("R-ANT-03", "Reaction Function", "Fed ≥ 4% & spread SBN-UST ≤ 225 bps → antisipasi outflow SBN",
      "KondisiPasarAktif(?k), ffrAtasPersen(?k, ?f), greaterThanOrEqual(?f, 4.0), spreadSBNUSTBps(?k, ?s), lessThanOrEqual(?s, 225.0) -> AntisipasiTerpicu(Antisipasi_OutflowSBN), PergerakanAktif(Mv_OutflowSBN)")
    R("R-ANT-04", "Reaction Function", "Drawdown ≤ -35% → antisipasi stabilisasi pasar (buyer of last resort)",
      "KondisiPasarAktif(?k), drawdownIHSGPersen(?k, ?d), lessThanOrEqual(?d, -35.0) -> AntisipasiTerpicu(Antisipasi_StabilisasiPasar), PergerakanAktif(Mv_DukunganLikuiditasDomestik)")
    R("R-ANT-05", "Reaction Function", "CDS ≥ 90 bps → antisipasi kenaikan premi risiko negara",
      "KondisiPasarAktif(?k), cds5YBps(?k, ?c), greaterThanOrEqual(?c, 90.0) -> AntisipasiTerpicu(Antisipasi_PremiRisikoNegara), PergerakanAktif(Mv_PremiRisikoNegaraNaik)")

    # ================================================================ REFLEKSIVITAS & KEKUATAN RELATIF
    R("R-RS-01", "Refleksivitas", "Kekuatan relatif = perubahan 20 hari − perubahan IHSG 1 bulan",
      "Emiten(?e), perubahanHarga20HariPersen(?e, ?c), KondisiPasarAktif(?k), perubahanIHSG1BulanPersen(?k, ?m), subtract(?rs, ?c, ?m) -> kekuatanRelatifPersen(?e, ?rs)")
    R("R-RS-02", "Refleksivitas", "Mengungguli pasar ≥ +5 pp", "Emiten(?e), kekuatanRelatifPersen(?e, ?r), greaterThanOrEqual(?r, 5.0) -> OutperformPasar(?e)")
    R("R-RS-03", "Refleksivitas", "Kalah dari pasar ≤ -5 pp", "Emiten(?e), kekuatanRelatifPersen(?e, ?r), lessThanOrEqual(?r, -5.0) -> UnderperformPasar(?e)")
    R("R-REF-01", "Refleksivitas", "Berita buruk priced-in: sentimen negatif, mengungguli pasar, bandar akumulasi",
      "SentimenNegatif(?e), kekuatanRelatifPersen(?e, ?r), greaterThanOrEqual(?r, 5.0), skorAccDistBroker(?e, ?a), greaterThanOrEqual(?a, 10.0) -> SinyalKetahananBeritaBuruk(?e)")
    R("R-REF-02", "Refleksivitas", "Sell the news: sentimen positif, kalah dari pasar, bandar distribusi",
      "SentimenPositif(?e), kekuatanRelatifPersen(?e, ?r), lessThan(?r, 0.0), skorAccDistBroker(?e, ?a), lessThanOrEqual(?a, -10.0) -> SellTheNews(?e)")

    # ================================================================ KAPITULASI & AKUMULASI BERTAHAP
    R("R-KAP-01", "Kapitulasi", "Kapitulasi emiten: volume ≥ 1,8×, RSI < 35, turun ≥ 15% sebulan",
      "Emiten(?e), rasioVolume(?e, ?v), greaterThanOrEqual(?v, 1.8), rsi14(?e, ?r), lessThan(?r, 35.0), perubahanHarga20HariPersen(?e, ?c), lessThanOrEqual(?c, -15.0) -> KapitulasiEmiten(?e)")
    R("R-KAP-02", "Kapitulasi", "Akumulasi bertahap: strategi pasar bertahap + kualitas + murah + tanpa penalti + kapitulasi emiten",
      "StrategiAkumulasiBertahap(?k), FundamentalKuat(?e), Undervalued(?e), penaltiRisiko(?e, ?p), equal(?p, 0), KapitulasiEmiten(?e) -> KandidatAkumulasiBertahap(?e)")
    R("R-KAP-03", "Kapitulasi", "Akumulasi bertahap: strategi pasar bertahap + kualitas + murah + tanpa penalti + akumulasi bandar di bawah MA200 (beaten-down quality)",
      "StrategiAkumulasiBertahap(?k), FundamentalKuat(?e), Undervalued(?e), penaltiRisiko(?e, ?p), equal(?p, 0), AkumulasiBandar(?e), jarakMA200Persen(?e, ?m), lessThan(?m, 0.0) -> KandidatAkumulasiBertahap(?e)")
    R("R-KAP-04", "Kapitulasi", "Tangga harga tranche: T1 = harga, T2 = harga − 2×ATR, T3 = harga − 4×ATR",
      "KandidatAkumulasiBertahap(?e), hargaPenutupan(?e, ?h), atrRupiah(?e, ?a), multiply(?a2, ?a, 2.0), multiply(?a4, ?a, 4.0), subtract(?t2, ?h, ?a2), subtract(?t3, ?h, ?a4) -> hargaTranche1(?e, ?h), hargaTranche2(?e, ?t2), hargaTranche3(?e, ?t3)")

    # ================================================================ REVISI LABA & ERP
    R("R-REV-01", "Ekspektasi Laba", "Revisi konsensus naik ≥ 5%", "Emiten(?e), revisiEPS3BulanPersen(?e, ?r), greaterThanOrEqual(?r, 5.0) -> RevisiLabaNaik(?e)")
    R("R-REV-02", "Ekspektasi Laba", "Revisi konsensus turun ≥ 5%", "Emiten(?e), revisiEPS3BulanPersen(?e, ?r), lessThanOrEqual(?r, -5.0) -> RevisiLabaTurun(?e)")
    R("R-REV-03", "Ekspektasi Laba", "Celah ekspektasi positif: revisi naik + undervalued + teknikal belum bereaksi (≤ 4)",
      "RevisiLabaNaik(?e), Undervalued(?e), skorTeknikal(?e, ?t), lessThanOrEqual(?t, 4) -> CelahEkspektasiPositif(?e)")
    R("R-REV-04", "Ekspektasi Laba", "Murah karena laba turun (peringatan dini value trap)", "RevisiLabaTurun(?e), Undervalued(?e) -> MurahKarenaLabaTurun(?e)")
    R("R-ERP-01", "Valuasi Relatif Obligasi", "ERP = 100/PER − yield SBN 10Y",
      "Emiten(?e), per(?e, ?p), greaterThan(?p, 0.0), KondisiPasarAktif(?k), yieldSBN10Y(?k, ?y), divide(?ey, 100.0, ?p), subtract(?erp, ?ey, ?y) -> equityRiskPremium(?e, ?erp)")
    R("R-ERP-02", "Valuasi Relatif Obligasi", "ERP ≥ 8 pp sangat menarik", "Emiten(?e), equityRiskPremium(?e, ?x), greaterThanOrEqual(?x, 8.0) -> ERPSangatMenarik(?e)")
    R("R-ERP-03", "Valuasi Relatif Obligasi", "4 ≤ ERP < 8 pp menarik", "Emiten(?e), equityRiskPremium(?e, ?x), greaterThanOrEqual(?x, 4.0), lessThan(?x, 8.0) -> ERPMenarik(?e)")
    R("R-ERP-04", "Valuasi Relatif Obligasi", "ERP < 0: SBN lebih menarik", "Emiten(?e), equityRiskPremium(?e, ?x), lessThan(?x, 0.0) -> MahalVsObligasi(?e)")

    # ================================================================ TATA KELOLA & MANIPULASI
    R("R-GOV-01", "Tata Kelola", "Free float < 15% → risiko HSC/dikeluarkan indeks", "Emiten(?e), freeFloatPersen(?e, ?f), lessThan(?f, 15.0) -> RisikoHSC(?e)")
    R("R-GOV-02", "Tata Kelola", "Saham pengendali digadaikan ≥ 30% saat downtrend → risiko forced sell",
      "Emiten(?e), sahamDigadaikanPersen(?e, ?g), greaterThanOrEqual(?g, 30.0), TrenTurun(?e) -> RisikoForcedSellPengendali(?e)")
    R("R-GOV-03", "Tata Kelola", "Orang dalam membeli saat undervalued", "Emiten(?e), transaksiOrangDalam(?e, ?t), greaterThanOrEqual(?t, 1), Undervalued(?e) -> SinyalOrangDalam(?e)")
    R("R-GOV-04", "Tata Kelola", "Indikasi saham gorengan: free float < 20%, volume ≥ 3×, ARA ≥ 2 kali/5 hari, top-3 broker ≥ 60%",
      "Emiten(?e), freeFloatPersen(?e, ?f), lessThan(?f, 20.0), rasioVolume(?e, ?v), greaterThanOrEqual(?v, 3.0), jumlahARA5Hari(?e, ?n), greaterThanOrEqual(?n, 2), konsentrasiBrokerTop3Persen(?e, ?c), greaterThanOrEqual(?c, 60.0) -> IndikasiSahamGorengan(?e)")
    R("R-GOV-05", "Tata Kelola", "Risiko pump & dump: gorengan + overvalued + RSI ≥ 80",
      "IndikasiSahamGorengan(?e), Overvalued(?e), rsi14(?e, ?r), greaterThanOrEqual(?r, 80.0) -> RisikoPumpAndDump(?e)")
    R("R-GOV-06", "Tata Kelola", "Rencana BEI keluarkan HSC aktif → emiten free float rendah tertekan",
      "RisikoHSC(?e), PeristiwaAktif(Ev_RencanaBEI_KeluarkanHSC) -> ditekanOleh(?e, Mv_PenghapusanHSC)")
    R("R-GOV-07", "Tata Kelola", "Pump & dump → hindari", "RisikoPumpAndDump(?e) -> SinyalHindari(?e)")
    R("R-GOV-08", "Tata Kelola", "Forced sell pengendali → hindari", "RisikoForcedSellPengendali(?e) -> SinyalHindari(?e)")

    # ================================================================ SKENARIO: EKSPEKTASI PROBABILISTIK & ROBUSTNESS
    R("R-ROB-01", "Robustness Skenario", "Skor ekspektasi probabilistik = Σ p(skenario) × skor outlook; upside = Bull − Base; downside = Base − Bear",
      "Sektor(?s), PenilaianSektor(?a1), menilaiSektor(?a1, ?s), dibawahSkenario(?a1, Skenario_Base_2027_2028), skorOutlook(?a1, ?o1), "
      "PenilaianSektor(?a2), menilaiSektor(?a2, ?s), dibawahSkenario(?a2, Skenario_Bull_Pemulihan), skorOutlook(?a2, ?o2), "
      "PenilaianSektor(?a3), menilaiSektor(?a3, ?s), dibawahSkenario(?a3, Skenario_Bear_Stagflasi), skorOutlook(?a3, ?o3), "
      "probabilitasSkenario(Skenario_Base_2027_2028, ?p1), probabilitasSkenario(Skenario_Bull_Pemulihan, ?p2), probabilitasSkenario(Skenario_Bear_Stagflasi, ?p3), "
      "multiply(?x1, ?p1, ?o1), multiply(?x2, ?p2, ?o2), multiply(?x3, ?p3, ?o3), add(?ev, ?x1, ?x2, ?x3), subtract(?up, ?o2, ?o1), subtract(?dn, ?o1, ?o3) "
      "-> skorEkspektasiProbabilistik(?s, ?ev), skorOutlookBase(?s, ?o1), skorOutlookBull(?s, ?o2), skorOutlookBear(?s, ?o3), upsideSkenario(?s, ?up), downsideSkenario(?s, ?dn)")
    R("R-ROB-02", "Robustness Skenario", "Robust: Base ≥ 7, Bull ≥ 7, Bear ≥ 2",
      "Sektor(?s), skorOutlookBase(?s, ?a), greaterThanOrEqual(?a, 7), skorOutlookBull(?s, ?b), greaterThanOrEqual(?b, 7), skorOutlookBear(?s, ?c), greaterThanOrEqual(?c, 2) -> SektorRobustLintasSkenario(?s)")
    R("R-ROB-03", "Robustness Skenario", "Asimetri positif: upside ≥ 1,5 × downside & ekspektasi ≥ 2",
      "Sektor(?s), upsideSkenario(?s, ?u), downsideSkenario(?s, ?d), greaterThanOrEqual(?d, 0), multiply(?d15, ?d, 1.5), greaterThanOrEqual(?u, ?d15), skorEkspektasiProbabilistik(?s, ?e), greaterThanOrEqual(?e, 2.0) -> SektorAsimetriPositif(?s)")
    R("R-ROB-04", "Konstruksi Portofolio", "Sektor inti (core): bullish di skenario aktif & robust lintas skenario",
      "SektorBullish(?s), SektorRobustLintasSkenario(?s) -> SektorPilihanInti(?s)")
    R("R-ROB-05", "Konstruksi Portofolio", "Sektor satelit: asimetri positif + peluang kontrarian",
      "SektorAsimetriPositif(?s), SektorPeluangKontrarian(?s) -> SektorPilihanSatelit(?s)")
    for j, (lo, hi, pts) in enumerate([(10.0, None, 4), (6.0, 10.0, 2), (2.0, 6.0, 0), (None, 2.0, -3)]):
        cond = ["skorEkspektasiProbabilistik(?s, ?v)"] + ([f"greaterThanOrEqual(?v, {lo})"] if lo is not None else []) + ([f"lessThan(?v, {hi})"] if hi is not None else [])
        R(f"R-ROB-06{chr(97 + j)}", "Robustness Skenario", f"Kontribusi sektor berbasis ekspektasi probabilistik = {pts}",
          "Emiten(?e), termasukSektor(?e, ?s), " + ", ".join(cond) + f" -> skorKontribusiSektorEV(?e, {pts})")

    # ================================================================ SMART MONEY & SKOR ADAPTIF REGIME
    R("R-ADP-01a", "Adaptif Regime", "Poin smart money 2: akumulasi ≥ 20 & mengungguli pasar ≥ 5",
      "Emiten(?e), skorAccDistBroker(?e, ?a), greaterThanOrEqual(?a, 20.0), kekuatanRelatifPersen(?e, ?r), greaterThanOrEqual(?r, 5.0) -> poinSmartMoney(?e, 2)")
    R("R-ADP-01b", "Adaptif Regime", "Poin smart money 1: akumulasi ≥ 20 tetapi belum mengungguli pasar",
      "Emiten(?e), skorAccDistBroker(?e, ?a), greaterThanOrEqual(?a, 20.0), kekuatanRelatifPersen(?e, ?r), lessThan(?r, 5.0) -> poinSmartMoney(?e, 1)")
    R("R-ADP-01c", "Adaptif Regime", "Poin smart money 0: akumulasi < 20",
      "Emiten(?e), skorAccDistBroker(?e, ?a), lessThan(?a, 20.0) -> poinSmartMoney(?e, 0)")
    R("R-ADP-02", "Adaptif Regime", "SKOR ADAPTIF = Σ bobot(regime aktif) × pilar (9 pilar)",
      "Emiten(?e), RegimeAktif(?r), "
      "bobotFundamental(?r, ?w1), bobotValuasi(?r, ?w2), bobotTeknikal(?r, ?w3), bobotBandar(?r, ?w4), bobotSentimen(?r, ?w5), bobotSektor(?r, ?w6), bobotRisiko(?r, ?w7), bobotLikuiditas(?r, ?w8), bobotSmartMoney(?r, ?w9), "
      "skorFundamental(?e, ?v1), skorValuasi(?e, ?v2), skorTeknikal(?e, ?v3), skorBandar(?e, ?v4), skorSentimen(?e, ?v5), skorKontribusiSektorEV(?e, ?v6), penaltiRisiko(?e, ?v7), poinLikuiditas(?e, ?v8), poinSmartMoney(?e, ?v9), "
      "multiply(?m1, ?w1, ?v1), multiply(?m2, ?w2, ?v2), multiply(?m3, ?w3, ?v3), multiply(?m4, ?w4, ?v4), multiply(?m5, ?w5, ?v5), multiply(?m6, ?w6, ?v6), multiply(?m7, ?w7, ?v7), multiply(?m8, ?w8, ?v8), multiply(?m9, ?w9, ?v9), "
      "add(?s, ?m1, ?m2, ?m3, ?m4, ?m5, ?m6, ?m7, ?m8, ?m9) -> skorAdaptifRegime(?e, ?s)")
    R("R-ADP-03", "Adaptif Regime", "Top pick adaptif: skor adaptif ≥ ambang regime, sektor ekspektasi ≥ 2, penalti ≥ -1",
      "Emiten(?e), RegimeAktif(?r), ambangTopPickAdaptif(?r, ?t), skorAdaptifRegime(?e, ?s), greaterThanOrEqual(?s, ?t), skorKontribusiSektorEV(?e, ?c), greaterThanOrEqual(?c, 0), penaltiRisiko(?e, ?p), greaterThanOrEqual(?p, -1), termasukSektor(?e, ?sk) -> KandidatTopPickAdaptif(?e), topPickAdaptifSektor(?sk, ?e)")

    # ================================================================ KONFLUENSI & KONFLIK
    for code, prop, flag, thr in [("R-KON-01", "skorFundamental", "flagFundamental", 7), ("R-KON-02", "skorValuasi", "flagValuasi", 2),
                                  ("R-KON-03", "skorTeknikal", "flagTeknikal", 5), ("R-KON-04", "skorBandar", "flagBandar", 3),
                                  ("R-KON-05", "skorSentimen", "flagSentimen", 1), ("R-KON-06", "skorKontribusiSektorEV", "flagMakroSektor", 2)]:
        bins(code, "Konfluensi", f"Bendera pilar {prop} ≥ {thr}", prop, flag, "Emiten", [(thr, None, 1, None), (None, thr, 0, None)])
    R("R-KON-07", "Konfluensi", "Skor konfluensi = jumlah pilar bullish (0-6)",
      "Emiten(?e), flagFundamental(?e, ?a), flagValuasi(?e, ?b), flagTeknikal(?e, ?c), flagBandar(?e, ?d), flagSentimen(?e, ?f), flagMakroSektor(?e, ?g), add(?s, ?a, ?b, ?c, ?d, ?f, ?g) -> skorKonfluensi(?e, ?s)")
    R("R-KON-08", "Konfluensi", "Konfluensi tinggi ≥ 5", "Emiten(?e), skorKonfluensi(?e, ?s), greaterThanOrEqual(?s, 5) -> KonfluensiTinggi(?e)")
    R("R-KON-09", "Konfluensi", "Konfluensi rendah ≤ 2", "Emiten(?e), skorKonfluensi(?e, ?s), lessThanOrEqual(?s, 2) -> KonfluensiRendah(?e)")
    R("R-KON-10", "Konflik Sinyal", "Fundamental kuat tetapi bandar distribusi", "FundamentalKuat(?e), DistribusiBandar(?e) -> KonflikFundamentalVsBandar(?e), TungguKonfirmasi(?e)")
    R("R-KON-11", "Konflik Sinyal", "Tren naik tanpa fundamental", "TrenNaik(?e), FundamentalLemah(?e) -> MomentumTanpaFundamental(?e), TungguKonfirmasi(?e)")
    R("R-KON-12", "Konflik Sinyal", "Sentimen positif tetapi bandar distribusi", "SentimenPositif(?e), DistribusiBandar(?e) -> DistribusiSaatEuforia(?e), TungguKonfirmasi(?e)")
    R("R-KON-13", "Konflik Sinyal", "Murah karena laba turun → tunggu", "MurahKarenaLabaTurun(?e), KandidatTopPickAdaptif(?e) -> TungguKonfirmasi(?e)")

    # ================================================================ UKURAN POSISI & KONSENTRASI
    R("R-POS-01", "Manajemen Posisi", "Ukuran posisi maks (% modal) = risiko per transaksi (regime) / (2 × ATR%) × 100",
      "Emiten(?e), RegimeAktif(?r), risikoPerTransaksiPersen(?r, ?x), atrPersen(?e, ?a), multiply(?d, ?a, 2.0), divide(?q, ?x, ?d), multiply(?u, ?q, 100.0) -> ukuranPosisiMaksPersen(?e, ?u)")
    R("R-POS-02", "Manajemen Posisi", "Konsentrasi tema: dua top pick adaptif berbagi komoditas pendapatan",
      "KandidatTopPickAdaptif(?a), KandidatTopPickAdaptif(?b), eksposurKomoditasPendapatan(?a, ?k), eksposurKomoditasPendapatan(?b, ?k), kodeSaham(?a, ?x), kodeSaham(?b, ?y), notEqual(?x, ?y) -> terkonsentrasiDengan(?a, ?b), RisikoKonsentrasiTema(?a)")

    # ================================================================ KATALIS
    R("R-KAT-01", "Katalis", "Katalis dekat: 0-45 hari ke depan",
      "Katalis(?k), hariMenujuKatalis(?k, ?d), greaterThanOrEqual(?d, 0), lessThanOrEqual(?d, 45) -> KatalisDekat(?k)")
    R("R-KAT-02", "Katalis", "Sektor dengan katalis dekat", "KatalisDekat(?k), katalisSektor(?k, ?s) -> sektorMemilikiKatalis(?s, ?k), SektorKatalisDekat(?s)")
    R("R-KAT-03", "Katalis", "Routing katalis sektor ke emiten", "KatalisDekat(?k), katalisSektor(?k, ?s), termasukSektor(?e, ?s) -> memilikiKatalisDekat(?e, ?k)")
    R("R-KAT-04", "Katalis", "Routing katalis indeks ke konstituen", "KatalisDekat(?k), katalisIndeks(?k, ?i), anggotaIndeks(?e, ?i) -> memilikiKatalisDekat(?e, ?k)")
    R("R-KAT-05", "Katalis", "Top pick adaptif + katalis biner dekat → masuk bertahap",
      "memilikiKatalisDekat(?e, ?k), KatalisBiner(?k), KandidatTopPickAdaptif(?e) -> StrategiTrancheKatalisBiner(?e)")
    R("R-KAT-06", "Katalis", "Kandidat akumulasi + katalis biner dekat → masuk bertahap",
      "memilikiKatalisDekat(?e, ?k), KatalisBiner(?k), KandidatAkumulasiBertahap(?e) -> StrategiTrancheKatalisBiner(?e)")

    # ================================================================ TESIS & KILL SWITCH
    base = "TesisInvestasi(?t), indikatorKunciTesis(?t, ?i), nilaiIndikator(?i, ?v), "
    R("R-TES-01", "Tesis & Invalidasi", "Tesis gugur: indikator di bawah ambang invalidasi bawah",
      base + "ambangInvalidasiBawah(?t, ?b), lessThan(?v, ?b) -> TesisGugur(?t)")
    R("R-TES-02", "Tesis & Invalidasi", "Tesis gugur: indikator di atas ambang invalidasi atas",
      base + "ambangInvalidasiAtas(?t, ?a), greaterThan(?v, ?a) -> TesisGugur(?t)")
    R("R-TES-03", "Tesis & Invalidasi", "Tesis valid: indikator di dalam rentang",
      base + "ambangInvalidasiBawah(?t, ?b), greaterThanOrEqual(?v, ?b), ambangInvalidasiAtas(?t, ?a), lessThanOrEqual(?v, ?a) -> TesisValid(?t)")
    R("R-TES-04", "Tesis & Invalidasi", "Buffer ke batas bawah (%)",
      base + "ambangInvalidasiBawah(?t, ?b), greaterThan(?b, 0.0), subtract(?d, ?v, ?b), divide(?q, ?d, ?v), multiply(?p, ?q, 100.0) -> bufferBawahPersen(?t, ?p)")
    R("R-TES-05", "Tesis & Invalidasi", "Buffer ke batas atas (%)",
      base + "ambangInvalidasiAtas(?t, ?a), lessThan(?a, 100000000.0), subtract(?d, ?a, ?v), divide(?q, ?d, ?v), multiply(?p, ?q, 100.0) -> bufferAtasPersen(?t, ?p)")
    R("R-TES-06", "Tesis & Invalidasi", "Tesis rapuh: buffer bawah < 10%", "TesisInvestasi(?t), bufferBawahPersen(?t, ?p), lessThan(?p, 10.0) -> TesisRapuh(?t)")
    R("R-TES-07", "Tesis & Invalidasi", "Tesis rapuh: buffer atas < 10%", "TesisInvestasi(?t), bufferAtasPersen(?t, ?p), lessThan(?p, 10.0) -> TesisRapuh(?t)")
    R("R-TES-08", "Tesis & Invalidasi", "Tesis kontrarian terpicu: indikator di bawah ambang pemicu",
      base + "ambangPemicuBawah(?t, ?x), lessThan(?v, ?x) -> TesisTerpicu(?t)")
    R("R-TES-09", "Tesis & Invalidasi", "Tesis gugur → sektor dipantau ketat", "TesisGugur(?t), tesisUntukSektor(?t, ?s) -> SektorPerluPemantauanKetat(?s)")
    R("R-TES-10", "Tesis & Invalidasi", "Tesis rapuh → sektor dipantau ketat", "TesisRapuh(?t), tesisUntukSektor(?t, ?s) -> SektorPerluPemantauanKetat(?s)")

    # ================================================================ PERSONA v2
    R("R-PRF-08", "Stakeholder", "Persona moderat: top pick adaptif tanpa konflik",
      "InvestorRitel(?i), memilikiProfilRisiko(?i, ProfilModerat), KandidatTopPickAdaptif(?e), KonfluensiTinggi(?e) -> direkomendasikanUntuk(?e, ?i)")
    R("R-PRF-09", "Stakeholder", "Persona konservatif: akumulasi bertahap pada emiten berdividen",
      "InvestorRitel(?i), memilikiProfilRisiko(?i, ProfilKonservatif), KandidatAkumulasiBertahap(?e), DividenAndalan(?e) -> direkomendasikanUntuk(?e, ?i)")
