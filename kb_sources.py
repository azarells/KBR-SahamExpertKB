# -*- coding: utf-8 -*-
"""
v2 — LAPISAN SUMBER DATA & KATALOG INDIKATOR
Setiap indikator dicatat: pilar, sifat waktu (Leading/Coincident/Lagging), frekuensi, sumber, status integrasi.
Status: "Terintegrasi v2" = sudah dipakai aturan SWRL; "Siap Integrasi" = struktur ada, tinggal pipeline data;
"Roadmap" = rencana pengembangan.
"""

# nama, kelas, label, jenisAkses, format, kredibilitas, url, deskripsi
SUMBER = [
 ("Src_IDX", "SumberDataResmi", "Bursa Efek Indonesia (idx.co.id)", "Gratis", "Web/PDF/XBRL", 0.98, "https://www.idx.co.id",
  "Laporan keuangan (XBRL), ringkasan perdagangan & transaksi asing harian, keterbukaan informasi (aksi korporasi, laporan kepemilikan ≥5% & direksi/komisaris), konstituen indeks, UMA/suspensi, papan pemantauan khusus."),
 ("Src_KSEI", "SumberDataResmi", "KSEI", "Gratis", "Web/PDF", 0.97, "https://www.ksei.co.id",
  "Statistik kepemilikan efek per tipe investor (lokal/asing, individu/institusi), jumlah SID, pemegang >1% (reformasi 2026)."),
 ("Src_OJK", "SumberDataResmi", "Otoritas Jasa Keuangan", "Gratis", "Web/PDF/Excel", 0.97, "https://www.ojk.go.id",
  "Statistik pasar modal & perbankan (NPL, CAR, LDR industri), regulasi free float, POJK."),
 ("Src_BI", "SumberDataResmi", "Bank Indonesia (SEKI, JISDOR)", "Gratis", "Web/Excel", 0.98, "https://www.bi.go.id",
  "BI-Rate, JISDOR, cadangan devisa, neraca pembayaran, kredit perbankan, survei konsumen (IKK), survei harga properti."),
 ("Src_BPS", "SumberDataResmi", "Badan Pusat Statistik", "Gratis", "Web/API", 0.98, "https://www.bps.go.id",
  "Inflasi, PDB, neraca perdagangan, NTP, penjualan eceran."),
 ("Src_Kemenkeu", "SumberDataResmi", "Kemenkeu / DJPPR", "Gratis", "Web/PDF", 0.96, "https://www.djppr.kemenkeu.go.id",
  "APBN KiTa (defisit, subsidi energi), lelang & kepemilikan asing SBN."),
 ("Src_ESDM", "SumberDataResmi", "Kementerian ESDM", "Gratis", "Web", 0.95, "https://www.esdm.go.id",
  "HBA batu bara, ICP minyak, RKAB nikel/batu bara, kebijakan DMO."),
 ("Src_Kemendag", "SumberDataResmi", "Kementerian Perdagangan", "Gratis", "Web", 0.95, "https://www.kemendag.go.id",
  "Harga referensi CPO, bea keluar, HPE."),
 ("Src_FRED", "SumberDataPasar", "FRED - Federal Reserve Bank of St. Louis", "Gratis (API)", "API/CSV", 0.98, "https://fred.stlouisfed.org",
  "Fed funds, yield UST, PCE, dolar broad index, M2, financial conditions index."),
 ("Src_FederalReserve", "SumberDataResmi", "Federal Reserve (FOMC)", "Gratis", "Web/PDF", 0.99, "https://www.federalreserve.gov",
  "Pernyataan FOMC, Summary of Economic Projections (dot plot), risalah."),
 ("Src_CMEFedWatch", "SumberDataPasar", "CME FedWatch", "Gratis", "Web", 0.9, "https://www.cmegroup.com",
  "Probabilitas keputusan FOMC tersirat dari futures."),
 ("Src_EIA", "SumberDataResmi", "U.S. EIA (STEO)", "Gratis (API)", "API/Excel", 0.95, "https://www.eia.gov",
  "Harga & proyeksi minyak, inventori."),
 ("Src_OPEC", "SumberDataResmi", "OPEC Monthly Oil Market Report", "Gratis", "PDF", 0.9, "https://www.opec.org",
  "Suplai-permintaan minyak, keputusan kuota OPEC+."),
 ("Src_LME", "SumberDataPasar", "London Metal Exchange", "Sebagian berbayar", "Web/API", 0.95, "https://www.lme.com",
  "Harga & stok nikel, timah, tembaga, aluminium."),
 ("Src_WGC", "SumberDataPasar", "World Gold Council", "Gratis", "Web/Excel", 0.93, "https://www.gold.org",
  "Permintaan emas bank sentral, aliran ETF emas."),
 ("Src_MPOB_GAPKI", "SumberDataResmi", "MPOB / GAPKI", "Gratis", "Web/PDF", 0.9, "https://mpob.gov.my",
  "Stok, produksi, ekspor sawit."),
 ("Src_GDELT", "SumberDataAlternatif", "GDELT Project", "Gratis", "BigQuery/CSV", 0.8, "https://www.gdeltproject.org",
  "Basis data peristiwa & nada berita global (mesin-bacaan) — sumber utama pemantauan geopolitik otomatis."),
 ("Src_GPRIndex", "SumberDataAlternatif", "Geopolitical Risk Index (Caldara-Iacoviello)", "Gratis", "Excel", 0.9, "https://www.matteoiacoviello.com/gpr.htm",
  "Indeks risiko geopolitik berbasis frekuensi berita (harian/bulanan, termasuk per negara)."),
 ("Src_EPU", "SumberDataAlternatif", "Economic Policy Uncertainty Index", "Gratis", "Excel", 0.88, "https://www.policyuncertainty.com",
  "Indeks ketidakpastian kebijakan berbasis berita."),
 ("Src_ACLED", "SumberDataAlternatif", "ACLED", "Gratis (riset, registrasi)", "API/CSV", 0.88, "https://acleddata.com",
  "Data konflik bersenjata & protes per lokasi."),
 ("Src_Cboe", "SumberDataPasar", "Cboe (VIX)", "Gratis", "Web/CSV", 0.97, "https://www.cboe.com",
  "VIX & indeks volatilitas."),
 ("Src_MSCI", "SumberDataPasar", "MSCI (Index Review & Market Classification)", "Gratis (pengumuman)", "Web/PDF", 0.97, "https://www.msci.com",
  "Hasil index review, konsultasi klasifikasi pasar, jadwal review."),
 ("Src_FTSE_SPDJI", "SumberDataPasar", "FTSE Russell & S&P DJI", "Gratis (pengumuman)", "Web/PDF", 0.95, "https://www.lseg.com/ftse-russell",
  "Klasifikasi negara & review indeks."),
 ("Src_Terminal", "SumberDataPasar", "Bloomberg / LSEG Workspace / S&P Capital IQ", "Berbayar", "API/Terminal", 0.97, "https://www.bloomberg.com/professional",
  "Konsensus EPS & revisi, CDS, kepemilikan institusi, data real-time."),
 ("Src_BrokerApp", "SumberDataPasar", "Stockbit / RTI Business / IPOT", "Gratis-terbatas / langganan", "Aplikasi/Web", 0.85, "https://stockbit.com",
  "Broker summary harian, bandar detector, foreign flow per saham, stream sosial."),
 ("Src_OHLCV", "SumberDataPasar", "TradingView / Yahoo Finance / Investing.com", "Gratis", "Web/API", 0.88, "https://finance.yahoo.com",
  "Harga OHLCV saham, indeks global, komoditas, kurs."),
 ("Src_WGB", "SumberDataPasar", "WorldGovernmentBonds / Investing (CDS & yield)", "Gratis", "Web", 0.82, "https://www.worldgovernmentbonds.com",
  "CDS 5Y negara & kurva yield (sumber sekunder)."),
 ("Src_MediaBisnis", "SumberDataBerita", "Media bisnis nasional (Bisnis, Kontan, CNBC Indonesia, Katadata, Investortrust)", "Gratis/berlangganan", "Web/RSS", 0.85, "https://www.bisnis.com",
  "Berita pasar, makro, emiten (input sentiment scorer)."),
 ("Src_MediaGlobal", "SumberDataBerita", "Media global (Reuters, Bloomberg, FT)", "Berlangganan", "Web/API", 0.93, "https://www.reuters.com",
  "Berita geopolitik & pasar global."),
 ("Src_RisetSekuritas", "SumberDataBerita", "Riset sekuritas (Mandiri, BRI Danareksa, Mirae, dll.)", "Nasabah/publik", "PDF", 0.85, "https://www.brids.co.id",
  "Target harga, rekomendasi, estimasi laba."),
 ("Src_GoogleTrends", "SumberDataAlternatif", "Google Trends", "Gratis", "Web/CSV", 0.75, "https://trends.google.com",
  "Minat pencarian ritel (proksi FOMO/kepanikan)."),
 ("Src_MediaSosial", "SumberDataBerita", "X / Stockbit Stream / Telegram", "Gratis", "Web/API", 0.5, "https://x.com",
  "Sentimen ritel; kredibilitas rendah, rawan pompom (bobot kecil)."),
 ("Src_IMF_WB", "SumberDataResmi", "IMF WEO / World Bank", "Gratis", "Excel/API", 0.95, "https://www.imf.org",
  "Proyeksi pertumbuhan & inflasi global."),
 ("Src_AIS", "SumberDataAlternatif", "Pelacakan kapal AIS & tarif tanker", "Berbayar", "API", 0.85, "https://www.marinetraffic.com",
  "Arus tanker di Selat Hormuz/Laut Merah (data alternatif geopolitik)."),
 ("Src_Satelit", "SumberDataAlternatif", "Data satelit & mobilitas", "Berbayar", "API", 0.75, "",
  "Aktivitas tambang/pabrik, lampu malam, mobilitas (roadmap)."),
]

# nama, label, pilar, sifat (L/C/G), frekuensi, frekuensiHari, sumber[], status, aturan terkait / catatan
K = []
def k(n, l, pilar, sifat, frek, fh, src, status, cat=""):
    K.append((n, l, pilar, {"L": "Leading", "C": "Coincident", "G": "Lagging"}[sifat], frek, fh, src, status, cat))

T, S, R = "Terintegrasi v2", "Siap Integrasi", "Roadmap"
# ---------------- Makro global & moneter
k("Ind_FedFundsRate", "Fed Funds Rate", "Makro Global", "C", "8x/tahun", 45, ["Src_FederalReserve", "Src_FRED"], T, "R-ANT-03, skenario")
k("Ind_DotPlot", "FOMC Dot Plot (median)", "Makro Global", "L", "Kuartalan", 90, ["Src_FederalReserve"], S, "Arah bunga 1-2 th")
k("Ind_FedWatchProb", "Probabilitas FedWatch", "Makro Global", "L", "Harian", 1, ["Src_CMEFedWatch"], S, "Katalis biner FOMC")
k("Ind_PCE_US", "Core PCE AS", "Makro Global", "G", "Bulanan", 30, ["Src_FRED"], T, "Fed reaction function")
k("Ind_UST10Y", "Yield US Treasury 10Y", "Makro Global", "C", "Harian", 1, ["Src_FRED"], T, "Spread SBN-UST")
k("Ind_DXY", "Indeks Dolar (DXY)", "Makro Global", "C", "Harian", 1, ["Src_OHLCV", "Src_FRED"], S, "")
k("Ind_VIX", "VIX", "Risiko Global", "C", "Harian", 1, ["Src_Cboe"], S, "Input skor stres pasar (roadmap bobot)")
k("Ind_MOVE", "MOVE Index (volatilitas obligasi)", "Risiko Global", "C", "Harian", 1, ["Src_Terminal"], R, "")
k("Ind_FCI", "Financial Conditions Index (NFCI)", "Risiko Global", "L", "Mingguan", 7, ["Src_FRED"], R, "")
k("Ind_ISM_PMI_US", "ISM Manufaktur AS", "Makro Global", "L", "Bulanan", 30, ["Src_OHLCV"], R, "")
k("Ind_ChinaPMI", "PMI China (Caixin/NBS)", "Makro Global", "L", "Bulanan", 30, ["Src_OHLCV"], S, "Permintaan logam & batu bara")
k("Ind_ChinaCredit", "China Credit Impulse", "Makro Global", "L", "Bulanan", 30, ["Src_Terminal"], R, "Leading 6-9 bulan untuk komoditas")
k("Ind_GlobalGDP", "Proyeksi PDB Global (IMF)", "Makro Global", "G", "Semesteran", 180, ["Src_IMF_WB"], S, "")
k("Ind_CopperGold", "Rasio Tembaga/Emas", "Intermarket", "L", "Harian", 1, ["Src_LME", "Src_OHLCV"], R, "Proksi ekspektasi pertumbuhan global")
# ---------------- Makro domestik
k("Ind_BIRate", "BI-Rate", "Makro Domestik", "C", "Bulanan", 30, ["Src_BI"], T, "R-ANT-01")
k("Ind_DepositFacility", "BI Deposit Facility", "Makro Domestik", "C", "Bulanan", 30, ["Src_BI"], T, "")
k("Ind_GWM", "Giro Wajib Minimum", "Makro Domestik", "L", "Ad hoc", 90, ["Src_BI"], T, "Likuiditas bank")
k("Ind_JISDOR", "Kurs USD/IDR (JISDOR)", "Makro Domestik", "C", "Harian", 1, ["Src_BI"], T, "Skor stres, R-ANT-01")
k("Ind_NDF", "Rupiah NDF 1M", "Intermarket", "L", "Harian", 1, ["Src_Terminal"], R, "Ekspektasi rupiah offshore")
k("Ind_Inflasi", "Inflasi IHK (yoy)", "Makro Domestik", "G", "Bulanan", 30, ["Src_BPS"], T, "R-ANT-01")
k("Ind_InflasiInti", "Inflasi Inti", "Makro Domestik", "G", "Bulanan", 30, ["Src_BPS"], S, "")
k("Ind_PDB_ID", "PDB Indonesia", "Makro Domestik", "G", "Kuartalan", 90, ["Src_BPS"], S, "")
k("Ind_TransaksiBerjalan", "Neraca Transaksi Berjalan", "Makro Domestik", "G", "Kuartalan", 90, ["Src_BI"], T, "Twin deficit")
k("Ind_NeracaDagang", "Neraca Perdagangan", "Makro Domestik", "C", "Bulanan", 30, ["Src_BPS"], S, "")
k("Ind_CadanganDevisa", "Cadangan Devisa", "Makro Domestik", "C", "Bulanan", 30, ["Src_BI"], S, "Kapasitas intervensi BI")
k("Ind_PMI_ID", "PMI Manufaktur Indonesia", "Makro Domestik", "L", "Bulanan", 30, ["Src_OHLCV"], S, "")
k("Ind_IKK", "Indeks Keyakinan Konsumen", "Makro Domestik", "L", "Bulanan", 30, ["Src_BI"], S, "Konsumen non-primer")
k("Ind_PenjualanEceran", "Survei Penjualan Eceran", "Makro Domestik", "C", "Bulanan", 30, ["Src_BI"], S, "")
k("Ind_PenjualanMobil", "Penjualan Mobil & Motor", "Makro Domestik", "C", "Bulanan", 30, ["Src_OHLCV"], S, "ASII, AUTO")
k("Ind_PertumbuhanKredit", "Pertumbuhan Kredit Perbankan", "Makro Domestik", "C", "Bulanan", 30, ["Src_BI", "Src_OJK"], S, "Sektor keuangan")
k("Ind_DefisitAPBN", "Defisit APBN & Subsidi Energi", "Makro Domestik", "C", "Bulanan", 30, ["Src_Kemenkeu"], T, "R-ANT-02 (subsidi)")
k("Ind_YieldSBN10Y", "Yield SBN 10Y", "Makro Domestik", "C", "Harian", 1, ["Src_Kemenkeu", "Src_WGB"], T, "ERP, skor stres, tesis infrastruktur")
k("Ind_SpreadSBN_UST", "Spread SBN-UST 10Y", "Intermarket", "L", "Harian", 1, ["Src_Kemenkeu", "Src_FRED"], T, "R-ANT-03")
k("Ind_KepemilikanAsingSBN", "Kepemilikan Asing SBN", "Aliran Dana", "C", "Harian", 1, ["Src_Kemenkeu"], S, "")
k("Ind_CDS5Y", "CDS Indonesia 5Y", "Intermarket", "L", "Harian", 1, ["Src_Terminal", "Src_WGB"], T, "Skor stres, R-ANT-05, tesis keuangan")
k("Ind_RatingNegara", "Rating & Outlook Negara (S&P/Moody's/Fitch)", "Makro Domestik", "L", "Ad hoc", 180, ["Src_MediaGlobal"], T, "")
# ---------------- Komoditas
for n, l, src, st in [("Ind_Brent", "Harga Brent", ["Src_EIA", "Src_OHLCV"], T), ("Ind_WTI", "Harga WTI", ["Src_EIA"], T),
                      ("Ind_ICP", "Indonesian Crude Price", ["Src_ESDM"], S), ("Ind_HBA", "Harga Batubara Acuan", ["Src_ESDM"], S),
                      ("Ind_Newcastle", "Batu Bara Newcastle", ["Src_OHLCV"], S), ("Ind_Emas", "Harga Emas Spot", ["Src_OHLCV", "Src_WGC"], T),
                      ("Ind_PembelianEmasBankSentral", "Pembelian Emas Bank Sentral", ["Src_WGC"], S), ("Ind_Nikel", "Nikel LME", ["Src_LME"], S),
                      ("Ind_NPIPremium", "Premi NPI/Matte Nikel", ["Src_Terminal"], R), ("Ind_Timah", "Timah LME", ["Src_LME"], S),
                      ("Ind_Tembaga", "Tembaga LME", ["Src_LME"], S), ("Ind_CPO", "Harga CPO / HR CPO", ["Src_Kemendag", "Src_MPOB_GAPKI"], T),
                      ("Ind_StokSawitMalaysia", "Stok Sawit Malaysia", ["Src_MPOB_GAPKI"], S), ("Ind_KurvaFuturesMinyak", "Struktur Kurva Futures Minyak (backwardation/contango)", ["Src_Terminal"], R),
                      ("Ind_TarifTanker", "Tarif Tanker & Arus Hormuz (AIS)", ["Src_AIS"], R), ("Ind_RKAB", "Kuota RKAB Nikel/Batu Bara", ["Src_ESDM"], T)]:
    k(n, l, "Komoditas", "C", "Harian" if st != R else "Harian", 1, src, st, "")
# ---------------- Geopolitik
k("Ind_GPR", "Geopolitical Risk Index (global & Indonesia)", "Geopolitik", "L", "Harian", 1, ["Src_GPRIndex"], S, "Input arah faktor RiskOff")
k("Ind_EPU", "Economic Policy Uncertainty", "Geopolitik", "L", "Bulanan", 30, ["Src_EPU"], R, "")
k("Ind_GDELTTone", "Nada & volume peristiwa GDELT (Iran, Hormuz, China-AS)", "Geopolitik", "L", "15 menit", 1, ["Src_GDELT"], S, "Aktivasi peristiwa otomatis (pengganti input manual)")
k("Ind_ACLED", "Insiden konflik ACLED", "Geopolitik", "C", "Mingguan", 7, ["Src_ACLED"], R, "")
k("Ind_KalenderPemilu", "Kalender Pemilu Negara Besar", "Geopolitik", "L", "Tahunan", 365, ["Src_MediaGlobal"], T, "Katalis biner")
k("Ind_KeputusanOPEC", "Keputusan Kuota OPEC+", "Geopolitik", "L", "Bulanan", 30, ["Src_OPEC"], T, "")
k("Ind_TarifDagang", "Daftar tarif & sanksi dagang", "Geopolitik", "L", "Ad hoc", 30, ["Src_MediaGlobal"], T, "")
# ---------------- Pasar & aliran dana
k("Ind_IHSG", "IHSG & drawdown dari puncak", "Struktur Pasar", "C", "Harian", 1, ["Src_IDX"], T, "Skor stres, kapitulasi")
k("Ind_PenurunanHarian", "Penurunan harian terbesar (capitulation day)", "Struktur Pasar", "C", "Harian", 1, ["Src_IDX"], T, "R-PAS-03")
k("Ind_Breadth", "Breadth: % saham di atas MA200", "Struktur Pasar", "L", "Harian", 1, ["Src_IDX", "Src_OHLCV"], T, "Washout (dihitung dari universe)")
k("Ind_AdvanceDecline", "Advance/Decline Line", "Struktur Pasar", "L", "Harian", 1, ["Src_IDX"], S, "")
k("Ind_NewLows", "Jumlah 52-week new low", "Struktur Pasar", "L", "Harian", 1, ["Src_IDX"], S, "")
k("Ind_PERPasarBand", "PER IHSG vs rata-rata ±SD", "Struktur Pasar", "L", "Harian", 1, ["Src_Terminal"], S, "Zona akumulasi generasional")
k("Ind_ERP", "Equity Risk Premium (earnings yield − yield SBN)", "Valuasi", "L", "Harian", 1, ["Src_IDX", "Src_Kemenkeu"], T, "R-ERP-*")
k("Ind_NetAsingHarian", "Net Foreign Buy/Sell BEI", "Aliran Dana", "C", "Harian", 1, ["Src_IDX", "Src_BrokerApp"], T, "")
k("Ind_NetAsingYTD", "Akumulasi Net Asing YTD", "Aliran Dana", "C", "Harian", 1, ["Src_IDX"], T, "Skor stres")
k("Ind_KepemilikanAsingSaham", "Kepemilikan Asing Saham (KSEI)", "Aliran Dana", "L", "Bulanan", 30, ["Src_KSEI"], S, "Posisi asing ekstrem rendah = kontrarian")
k("Ind_AliranETF_EIDO", "Aliran & premi/diskon ETF EIDO", "Aliran Dana", "L", "Harian", 1, ["Src_OHLCV"], R, "")
k("Ind_SubscriptionRDS", "Subscription/redemption reksa dana saham", "Aliran Dana", "C", "Bulanan", 30, ["Src_OJK"], S, "")
k("Ind_SaldoMargin", "Saldo pembiayaan margin", "Aliran Dana", "C", "Bulanan", 30, ["Src_OJK"], R, "Forced sell risk")
k("Ind_JumlahSID", "Jumlah investor (SID) & aktivitas ritel", "Sentimen", "C", "Bulanan", 30, ["Src_KSEI"], S, "")
k("Ind_JadwalMSCI", "Jadwal review MSCI & konsultasi klasifikasi", "Struktur Pasar", "L", "Kuartalan", 90, ["Src_MSCI"], T, "Katalis biner")
k("Ind_FIF_NOS", "FIF & NOS MSCI per emiten", "Aliran Dana", "L", "Kuartalan", 90, ["Src_MSCI"], S, "")
# ---------------- Fundamental emiten
for n, l, sifat, st in [("Ind_ROE", "ROE", "G", T), ("Ind_DER", "DER", "G", T), ("Ind_NPM", "NPM", "G", T), ("Ind_EPSGrowth", "Pertumbuhan EPS", "G", T),
                        ("Ind_CFOtoNI", "CFO/Laba Bersih (accrual)", "G", T), ("Ind_ROIC_WACC", "ROIC vs WACC", "G", S), ("Ind_FCFYield", "FCF Yield", "G", S),
                        ("Ind_InterestCoverage", "Interest Coverage", "G", S), ("Ind_ProfilJatuhTempo", "Profil jatuh tempo utang", "L", R),
                        ("Ind_PorsiUtangUSD", "Porsi utang USD (risiko kurs)", "L", R), ("Ind_AltmanZ", "Altman Z-Score", "L", T), ("Ind_PiotroskiF", "Piotroski F-Score", "L", S),
                        ("Ind_BeneishM", "Beneish M-Score", "L", T), ("Ind_PER_Band", "PER vs rata-rata 5 th", "C", T), ("Ind_PBV_ROE", "PBV vs ROE", "C", S),
                        ("Ind_EV_EBITDA", "EV/EBITDA", "C", S), ("Ind_DividenYield", "Dividend yield & DPR", "G", T),
                        ("Ind_NPL_CAR_NIM", "NPL, CAR, NIM (bank)", "G", T), ("Ind_CASA_CoC", "CASA & Cost of Credit (bank)", "L", S),
                        ("Ind_RevisiKonsensus", "Revisi konsensus EPS 3 bulan", "L", T), ("Ind_EarningsSurprise", "Earnings surprise vs konsensus", "C", S),
                        ("Ind_OpiniAuditor", "Opini auditor & paragraf going concern", "G", S)]:
    k(n, l, "Fundamental", sifat, "Kuartalan", 90, ["Src_IDX", "Src_Terminal"], st, "")
for n, l in [("Ind_StripRatio", "Strip ratio & cash cost (batu bara)"), ("Ind_AISC", "AISC (emas)"), ("Ind_MarketingSales", "Marketing sales (properti)"),
             ("Ind_ARPU", "ARPU (telko)"), ("Ind_SSSG", "SSSG (ritel)"), ("Ind_TenancyRatio", "Tenancy ratio (menara)"), ("Ind_FFBYield", "Yield TBS & umur tanaman (sawit)")]:
    k(n, l, "Fundamental Sektoral", "L", "Kuartalan", 90, ["Src_IDX", "Src_RisetSekuritas"], S, "")
# ---------------- Tata kelola & kepemilikan
for n, l, st, cat in [("Ind_FreeFloat", "Free float (min. 15%)", T, "R-GOV-01 HSC"), ("Ind_PemegangSahamPengendali", "Kepemilikan pengendali & >1%", S, ""),
                      ("Ind_SahamDigadaikan", "Saham pengendali yang digadaikan", T, "R-GOV-02"), ("Ind_TransaksiOrangDalam", "Transaksi direksi/komisaris/pengendali", T, "R-GOV-03"),
                      ("Ind_TransaksiAfiliasi", "Transaksi pihak berelasi material", R, ""), ("Ind_HSCAlert", "High Shareholding Concentration alert", T, "R-GOV-01"),
                      ("Ind_UMA_Suspensi", "Riwayat UMA & suspensi", S, "Deteksi gorengan")]:
    k(n, l, "Tata Kelola", "L", "Ad hoc", 30, ["Src_IDX", "Src_KSEI"], st, cat)
# ---------------- Teknikal & bandarmology
for n, l, st in [("Ind_MA", "MA50/MA200 & golden/death cross", T), ("Ind_RSI", "RSI-14", T), ("Ind_MACD", "MACD", T), ("Ind_Volume", "Volume relatif", T),
                 ("Ind_ATR", "ATR (stop & sizing)", T), ("Ind_RelativeStrength", "Kekuatan relatif vs IHSG", T), ("Ind_PolaChart", "Pola chart & candlestick (detektor)", T),
                 ("Ind_VWAP", "VWAP intraday", T), ("Ind_OrderBook", "Order book bid/offer", T)]:
    k(n, l, "Teknikal", "C", "Harian", 1, ["Src_OHLCV", "Src_BrokerApp"], st, "")
for n, l, st in [("Ind_BrokerSummary", "Broker summary (top buyer/seller)", T), ("Ind_AccDist", "Skor akumulasi/distribusi broker", T),
                 ("Ind_KonsentrasiBroker", "Konsentrasi top-3 broker (HHI)", T), ("Ind_AvgPriceBandar", "Harga rata-rata bandar", S),
                 ("Ind_NetRitel", "Net broker ritel", T), ("Ind_Crossing", "Frekuensi crossing/nego", S), ("Ind_ARA_Streak", "Jumlah ARA beruntun", T)]:
    k(n, l, "Bandarmology", "L", "Harian", 1, ["Src_BrokerApp", "Src_IDX"], st, "")
# ---------------- Sentimen
for n, l, src, st in [("Ind_SentimenBerita", "Skor sentimen berita aspect-based", ["Src_MediaBisnis", "Src_MediaGlobal"], T),
                      ("Ind_RekomendasiAnalis", "Rekomendasi & target harga analis", ["Src_RisetSekuritas"], T),
                      ("Ind_SentimenSosial", "Sentimen media sosial ritel", ["Src_MediaSosial"], S),
                      ("Ind_GoogleTrends", "Minat pencarian saham (Google Trends)", ["Src_GoogleTrends"], R),
                      ("Ind_FearGreedLokal", "Fear & Greed lokal (komposit)", ["Src_IDX", "Src_KSEI"], R)]:
    k(n, l, "Sentimen", "L", "Harian", 1, src, st, "")
