# -*- coding: utf-8 -*-
"""
Individu pengetahuan dasar & pakar (konsep).
Format: (NamaIndividu, Kelas, Label, Definisi, {anotasi tambahan})
Anotasi tambahan yang dikenal: rumus, interpretasi, ambangBatas, contohPenerapan, heuristikPakar
"""

C = []
def add(name, cls, label, definisi, **kw):
    C.append((name, cls, label, definisi, kw))

# ---------------------------------------------------------------- INSTRUMEN
add("SahamBiasa", "InstrumenPasarModal", "Saham Biasa (Common Stock)", "Bukti kepemilikan perusahaan dengan hak suara RUPS dan hak atas dividen setelah kewajiban lain dipenuhi.")
add("SahamPreferen", "InstrumenPasarModal", "Saham Preferen", "Saham dengan hak prioritas dividen/likuidasi, umumnya tanpa hak suara.")
add("Waran", "InstrumenPasarModal", "Waran", "Hak membeli saham baru pada harga dan periode tertentu; biasanya pemanis IPO/right issue.", heuristikPakar="Waran deep out-of-the-money mendekati jatuh tempo bernilai ~0; jangan dikoleksi sebagai investasi.")
add("HMETD_Right", "InstrumenPasarModal", "HMETD / Right", "Hak Memesan Efek Terlebih Dahulu untuk pemegang saham lama saat right issue.")
add("ETF", "InstrumenPasarModal", "Exchange Traded Fund", "Reksa dana yang unit penyertaannya diperdagangkan di bursa, umumnya mengikuti indeks (mis. LQ45, IDX30).")
add("ReksaDanaSaham", "InstrumenPasarModal", "Reksa Dana Saham", "Wadah investasi kolektif minimal 80% di saham, dikelola Manajer Investasi.")
add("ObligasiKorporasi", "InstrumenPasarModal", "Obligasi Korporasi", "Surat utang perusahaan dengan kupon tetap/mengambang.")
add("SuratBerhargaNegara", "InstrumenPasarModal", "Surat Berharga Negara (SBN)", "Surat utang pemerintah; yield SBN 10Y adalah acuan risk-free domestik.", heuristikPakar="Yield SBN naik tajam = tekanan untuk saham valuasi tinggi & properti.")
add("SingleStockFutures", "InstrumenPasarModal", "Single Stock Futures", "Kontrak berjangka atas saham tunggal di BEI.")
add("IPO", "InstrumenPasarModal", "Initial Public Offering", "Penawaran umum perdana saham ke publik.", heuristikPakar="Hati-hati IPO dengan free float kecil dan lock-up pendek: rawan dibanting setelah ARA berturut-turut.")

# ---------------------------------------------------------------- MEKANISME
add("Lot", "MekanismePerdagangan", "Lot", "Satuan perdagangan saham di BEI; 1 lot = 100 lembar.")
add("FraksiHarga", "MekanismePerdagangan", "Fraksi Harga (Tick Size)", "Kelipatan perubahan harga: Rp1 (<Rp200), Rp2 (Rp200-<500), Rp5 (Rp500-<2.000), Rp10 (Rp2.000-<5.000), Rp25 (≥Rp5.000).")
add("AutoRejectionAtas", "MekanismePerdagangan", "Auto Rejection Atas (ARA)", "Batas kenaikan harga harian maksimum; order di atas batas ditolak sistem JATS.", heuristikPakar="ARA beruntun dengan volume tipis & broker tunggal = tanda saham digoreng.")
add("AutoRejectionBawah", "MekanismePerdagangan", "Auto Rejection Bawah (ARB)", "Batas penurunan harga harian maksimum.")
add("SettlementT2", "MekanismePerdagangan", "Penyelesaian T+2", "Penyelesaian transaksi (serah saham & dana) dua hari bursa setelah transaksi; dijamin KPEI.")
add("SesiPerdagangan", "MekanismePerdagangan", "Sesi Perdagangan", "Sesi I dan Sesi II perdagangan reguler hari bursa.")
add("PraPembukaan", "MekanismePerdagangan", "Pra-Pembukaan (Pre-opening)", "Periode pembentukan harga pembukaan melalui call auction.")
add("PraPenutupan", "MekanismePerdagangan", "Pra-Penutupan (Pre-closing)", "Periode pembentukan harga penutupan melalui call auction.", heuristikPakar="Lonjakan harga khusus di pre-closing berulang kali = indikasi 'window dressing'/marking the close.")
add("FullCallAuction", "MekanismePerdagangan", "Full Call Auction (FCA)", "Mekanisme lelang berkala untuk saham Papan Pemantauan Khusus; order book tidak transparan.")
add("PasarReguler", "MekanismePerdagangan", "Pasar Reguler", "Pasar dengan mekanisme tawar-menawar berkelanjutan dalam satuan lot.")
add("PasarNegosiasi", "MekanismePerdagangan", "Pasar Negosiasi", "Pasar transaksi berdasarkan negosiasi (crossing/block trade) di luar order book reguler.", heuristikPakar="Transaksi nego besar di bawah harga pasar oleh pihak pengendali = sinyal waspada (potensi distribusi).")
add("PasarTunai", "MekanismePerdagangan", "Pasar Tunai", "Pasar dengan penyelesaian T+0 untuk pemenuhan kewajiban.")
add("OrderBook", "MekanismePerdagangan", "Order Book (Bid-Offer)", "Daftar antrean beli (bid) dan jual (offer) per tingkat harga.")
add("JenisOrderLimit", "MekanismePerdagangan", "Limit Order", "Order dengan harga tertentu.")
add("JenisOrderMarket", "MekanismePerdagangan", "Market Order", "Order yang langsung dicocokkan dengan harga terbaik yang tersedia.")
add("KapitalisasiPasar", "MekanismePerdagangan", "Kapitalisasi Pasar", "Harga × jumlah saham beredar.", rumus="MarketCap = Harga × SahamBeredar")
add("FreeFloat", "MekanismePerdagangan", "Free Float", "Porsi saham yang dimiliki publik (<5%) dan dapat diperdagangkan bebas; dasar bobot indeks MSCI (Foreign Inclusion Factor).", ambangBatas="Rencana OJK/BEI 2026: minimum 15% (bertahap).")
add("SID_RDN", "MekanismePerdagangan", "SID & RDN", "Single Investor Identification (KSEI) dan Rekening Dana Nasabah untuk dana investor.")

# ---------------------------------------------------------------- AKSI KORPORASI
add("DividenTunai", "AksiKorporasiPositif", "Dividen Tunai", "Pembagian laba dalam bentuk uang; ada cum date, ex date, recording date, payment date.", heuristikPakar="Harga cenderung naik menjelang cum date dan terkoreksi setelah ex date (dividend trap jangka pendek).")
add("DividenSaham", "AksiKorporasiNetral", "Dividen Saham", "Pembagian laba dalam bentuk saham baru.")
add("StockSplit", "AksiKorporasiPositif", "Stock Split", "Pemecahan nilai nominal saham untuk meningkatkan likuiditas & keterjangkauan.")
add("ReverseStockSplit", "AksiKorporasiNegatif", "Reverse Stock Split", "Penggabungan saham; sering dilakukan emiten berharga sangat rendah.")
add("Buyback", "AksiKorporasiPositif", "Pembelian Kembali Saham (Buyback)", "Emiten membeli sahamnya sendiri; sinyal manajemen menilai harga undervalued.", heuristikPakar="Buyback saat krisis pasar (OJK mengizinkan tanpa RUPS dalam kondisi berfluktuasi signifikan) adalah sinyal kuat.")
add("RightIssue", "AksiKorporasiNegatif", "Right Issue (PMHMETD)", "Penambahan modal dengan HMETD; dilutif bila tidak di-exercise.", heuristikPakar="Right issue untuk ekspansi produktif = netral/positif; untuk bayar utang = negatif.")
add("PrivatePlacement", "AksiKorporasiNegatif", "Private Placement (PMTHMETD)", "Penambahan modal tanpa HMETD kepada investor tertentu; maks 10% dalam 2 tahun.")
add("TenderOffer", "AksiKorporasiNetral", "Tender Offer", "Penawaran membeli saham dari publik oleh pihak tertentu, sering dengan premium.")
add("Merger", "AksiKorporasiNetral", "Merger", "Penggabungan dua perusahaan atau lebih.")
add("Akuisisi", "AksiKorporasiNetral", "Akuisisi", "Pengambilalihan pengendalian perusahaan.")
add("GoPrivate", "AksiKorporasiNetral", "Go Private / Voluntary Delisting", "Emiten keluar dari bursa secara sukarela dengan tender offer.")
add("DelistingPaksa", "AksiKorporasiNegatif", "Forced Delisting", "Penghapusan pencatatan oleh bursa (mis. suspensi >24 bulan, going concern).")
add("RUPS", "AksiKorporasiNetral", "Rapat Umum Pemegang Saham", "Forum pengambilan keputusan tertinggi (RUPST/RUPSLB).")

# ---------------------------------------------------------------- PENGAWASAN
add("Suspensi", "StatusPengawasan", "Suspensi Perdagangan", "Penghentian sementara perdagangan saham oleh bursa.")
add("UnusualMarketActivity", "StatusPengawasan", "Unusual Market Activity (UMA)", "Pengumuman bursa atas pergerakan harga/volume tidak wajar.", heuristikPakar="UMA setelah reli tajam sering diikuti profit taking; UMA bukan larangan beli.")
add("NotasiKhusus", "StatusPengawasan", "Notasi Khusus", "Huruf penanda kondisi emiten (mis. E=ekuitas negatif, M=PKPU, X=papan pemantauan khusus).")
add("PapanPemantauanKhusus", "StatusPengawasan", "Papan Pemantauan Khusus", "Papan untuk saham bermasalah likuiditas/fundamental; diperdagangkan via FCA.")
add("CircuitBreakerTradingHalt", "StatusPengawasan", "Trading Halt Pasar", "Penghentian perdagangan pasar bila IHSG turun tajam dalam sehari.")
add("BatasHargaGocap", "StatusPengawasan", "Batas Harga Minimum Rp50", "Harga minimum di Papan Utama/Pengembangan; saham 'gocap' tertahan tak bisa turun lagi di pasar reguler.")

# ---------------------------------------------------------------- BIAYA PAJAK
add("FeeTransaksi", "BiayaDanPajak", "Fee Broker", "Biaya beli (~0,15%) dan jual (~0,25%, termasuk pajak) tergantung sekuritas.")
add("PPhFinalPenjualan", "BiayaDanPajak", "PPh Final Penjualan Saham 0,1%", "Pajak final 0,1% dari nilai bruto penjualan saham.")
add("PajakDividen", "BiayaDanPajak", "Pajak Dividen", "PPh dividen 10% final bagi WP orang pribadi dalam negeri; dapat dibebaskan bila diinvestasikan kembali sesuai ketentuan.")

# ---------------------------------------------------------------- GAYA INVESTASI
add("ValueInvesting", "GayaInvestasi", "Value Investing", "Membeli saham di bawah nilai intrinsik dengan margin of safety (Graham, Buffett).")
add("GrowthInvesting", "GayaInvestasi", "Growth Investing", "Fokus emiten dengan pertumbuhan laba tinggi berkelanjutan.")
add("DividendInvesting", "GayaInvestasi", "Dividend Investing", "Fokus pada arus kas dividen stabil.")
add("GARP", "GayaInvestasi", "Growth at Reasonable Price", "Pertumbuhan dengan valuasi wajar; gunakan PEG < 1.")
add("MomentumTrading", "GayaInvestasi", "Momentum Trading", "Mengikuti saham yang sedang tren kuat.")
add("ContrarianInvesting", "GayaInvestasi", "Contrarian Investing", "Membeli saat pasar panik, menjual saat euforia.", heuristikPakar="'Be fearful when others are greedy, greedy when others are fearful.' Krisis = peluang bagi emiten berneraca kuat.")
add("SwingTrading", "GayaInvestasi", "Swing Trading", "Memegang posisi beberapa hari-minggu memanfaatkan ayunan harga.")
add("DayTrading", "GayaInvestasi", "Day Trading", "Buka-tutup posisi dalam satu hari.")
add("Scalping", "GayaInvestasi", "Scalping", "Mengambil untung kecil berkali-kali dalam hitungan menit; butuh likuiditas tinggi & disiplin cut loss.")
add("PositionTrading", "GayaInvestasi", "Position Trading", "Memegang berbulan-bulan mengikuti tren besar.")
add("IndexInvesting", "GayaInvestasi", "Index/Passive Investing", "Membeli indeks (ETF) untuk mengikuti pasar.")
add("DollarCostAveraging", "GayaInvestasi", "Dollar Cost Averaging", "Investasi rutin dengan nominal tetap untuk meratakan harga beli; cocok untuk pemula.")

# ---------------------------------------------------------------- MANAJEMEN RISIKO
add("StopLoss", "ManajemenRisiko", "Stop Loss / Cut Loss", "Batas rugi yang ditetapkan sebelum entry.", rumus="SL = Entry - 2 × ATR (aturan sistem)")
add("TakeProfit", "ManajemenRisiko", "Take Profit", "Target keluar dengan untung.", rumus="TP = Entry + 3 × ATR (aturan sistem)")
add("RiskRewardRatio", "ManajemenRisiko", "Risk/Reward Ratio", "Perbandingan potensi rugi dan untung.", ambangBatas="Minimal 1:1,5")
add("PositionSizing", "ManajemenRisiko", "Position Sizing", "Ukuran posisi berdasar risiko per transaksi.", rumus="Jumlah lembar = (Modal × %Risiko) / (Entry - SL)", ambangBatas="Risiko 1-2% modal per transaksi")
add("Diversifikasi", "ManajemenRisiko", "Diversifikasi", "Menyebar modal ke beberapa emiten/sektor dengan korelasi rendah.")
add("TrailingStop", "ManajemenRisiko", "Trailing Stop", "Stop loss yang digeser mengikuti kenaikan harga.")
add("AveragingDown", "ManajemenRisiko", "Averaging Down", "Menambah posisi saat harga turun; hanya untuk emiten fundamental kuat.", heuristikPakar="Averaging down pada value trap = bencana; pastikan bukan ZonaDistress.")
add("AveragingUp", "ManajemenRisiko", "Averaging Up / Pyramiding", "Menambah posisi saat tren terkonfirmasi naik.")
add("MarginOfSafety", "ManajemenRisiko", "Margin of Safety", "Selisih nilai intrinsik dengan harga pasar.", ambangBatas="≥ 25-30% untuk value investor")

# ---------------------------------------------------------------- BIAS PERILAKU
for n, l, d in [
    ("FOMO", "Fear of Missing Out", "Membeli karena takut ketinggalan reli; sering di pucuk."),
    ("HerdingBias", "Herding", "Ikut-ikutan mayoritas/influencer tanpa analisis."),
    ("LossAversion", "Loss Aversion", "Rasa sakit rugi lebih besar dari senang untung; menahan saham rugi terlalu lama."),
    ("ConfirmationBias", "Confirmation Bias", "Hanya mencari informasi yang mendukung keyakinan."),
    ("Overconfidence", "Overconfidence", "Terlalu yakin pada analisis sendiri; overtrading."),
    ("AnchoringBias", "Anchoring", "Terpaku pada harga beli/harga tertinggi lama."),
    ("DispositionEffect", "Disposition Effect", "Cepat menjual saham untung, menahan saham rugi."),
    ("RecencyBias", "Recency Bias", "Menganggap tren terbaru akan berlanjut selamanya."),
    ("PanicSelling", "Panic Selling", "Menjual karena panik saat pasar jatuh tajam; sering dimanfaatkan bandar untuk akumulasi murah."),
]:
    add(n, "BiasPerilaku", l, d)

# ---------------------------------------------------------------- SIKLUS & PROFIL
add("BullMarket", "SiklusPasar", "Bull Market", "Pasar naik ≥20% dari titik terendah dengan higher high-higher low.")
add("BearMarket", "SiklusPasar", "Bear Market", "Pasar turun ≥20% dari puncak.", contohPenerapan="IHSG 2026: dari 8.646 (akhir 2025) ke 4.996,61 (19 Okt 2026), -42% YTD.")
add("SidewaysMarket", "SiklusPasar", "Sideways Market", "Pasar bergerak mendatar dalam rentang.")
add("Wyckoff_Akumulasi", "FaseWyckoff", "Wyckoff: Akumulasi", "Bandar mengumpulkan barang di area bawah setelah downtrend; volume naik di support, harga sideways.")
add("Wyckoff_MarkUp", "FaseWyckoff", "Wyckoff: Mark-Up", "Harga dinaikkan setelah barang terkumpul; breakout resistance.")
add("Wyckoff_Distribusi", "FaseWyckoff", "Wyckoff: Distribusi", "Bandar melepas barang ke ritel di area atas.")
add("Wyckoff_MarkDown", "FaseWyckoff", "Wyckoff: Mark-Down", "Harga turun setelah distribusi selesai.")
add("ProfilKonservatif", "ProfilRisiko", "Konservatif", "Mengutamakan keamanan modal & dividen; toleransi drawdown rendah.")
add("ProfilModerat", "ProfilRisiko", "Moderat", "Seimbang antara pertumbuhan dan keamanan.")
add("ProfilAgresif", "ProfilRisiko", "Agresif", "Toleransi volatilitas tinggi, mengejar return tinggi/trading.")
add("Horizon_Intraday", "HorizonInvestasi", "Intraday", "< 1 hari")
add("Horizon_Pendek", "HorizonInvestasi", "Jangka Pendek", "1 minggu - 3 bulan")
add("Horizon_Menengah", "HorizonInvestasi", "Jangka Menengah (1-3 Tahun)", "Horizon utama prediksi sektor sistem ini.")
add("Horizon_Panjang", "HorizonInvestasi", "Jangka Panjang", "> 3 tahun")

# ---------------------------------------------------------------- LAPORAN KEUANGAN
for n, l, d in [
    ("Neraca", "Laporan Posisi Keuangan (Neraca)", "Aset = Liabilitas + Ekuitas pada satu titik waktu."),
    ("LaporanLabaRugi", "Laporan Laba Rugi", "Pendapatan, beban, laba kotor, laba usaha, laba bersih dalam satu periode."),
    ("LaporanArusKas", "Laporan Arus Kas", "Arus kas operasi (CFO), investasi (CFI), pendanaan (CFF)."),
    ("LaporanPerubahanEkuitas", "Laporan Perubahan Ekuitas", "Perubahan modal, laba ditahan, dividen."),
    ("CALK", "Catatan atas Laporan Keuangan", "Rincian kebijakan akuntansi, kontinjensi, transaksi pihak berelasi."),
    ("OpiniAuditor", "Opini Auditor", "WTP, WDP, TMP, TW; paragraf 'going concern' adalah red flag."),
]:
    add(n, "LaporanKeuangan", l, d)

# ---------------------------------------------------------------- RASIO
R = [
 ("PER", "RasioValuasi", "Price to Earnings Ratio", "Harga / EPS", "Berapa tahun laba untuk 'balik modal'. Bandingkan dengan rata-rata historis & sektor.", "Murah bila < 0,85× rata-rata 5 th; mahal bila ≥ 1,1×"),
 ("PBV", "RasioValuasi", "Price to Book Value", "Harga / BVPS", "Harga relatif terhadap nilai buku; penting untuk bank & properti.", "PBV < 1 dengan ROE > 10% sering undervalued"),
 ("PSR", "RasioValuasi", "Price to Sales", "Market Cap / Penjualan", "Untuk emiten belum laba (teknologi).", "Bandingkan dengan peers"),
 ("EV_EBITDA", "RasioValuasi", "EV/EBITDA", "(Market Cap + Utang - Kas) / EBITDA", "Netral struktur modal; baik untuk komoditas & infrastruktur.", "< 5x murah untuk komoditas"),
 ("PEG", "RasioValuasi", "PEG Ratio", "PER / Pertumbuhan EPS (%)", "Menyesuaikan PER dengan pertumbuhan.", "< 1 menarik"),
 ("EarningsYield", "RasioValuasi", "Earnings Yield", "EPS / Harga = 1/PER", "Bandingkan dengan yield SBN 10Y (equity risk premium).", "EY - Yield SBN > 3% menarik"),
 ("ROE", "RasioProfitabilitas", "Return on Equity", "Laba Bersih / Ekuitas", "Efisiensi modal pemegang saham; gunakan DuPont.", "≥ 15% sangat baik; 8-15% cukup"),
 ("ROA", "RasioProfitabilitas", "Return on Assets", "Laba Bersih / Total Aset", "Efisiensi aset.", "Bank ≥ 1,5% baik"),
 ("ROIC", "RasioProfitabilitas", "Return on Invested Capital", "NOPAT / (Ekuitas + Utang berbunga)", "Kualitas penciptaan nilai; bandingkan dengan WACC.", "ROIC > WACC"),
 ("GPM", "RasioProfitabilitas", "Gross Profit Margin", "Laba Kotor / Pendapatan", "Daya tawar harga & efisiensi produksi.", "Tren stabil/naik"),
 ("OPM", "RasioProfitabilitas", "Operating Profit Margin", "Laba Usaha / Pendapatan", "Efisiensi operasional.", ""),
 ("NPM", "RasioProfitabilitas", "Net Profit Margin", "Laba Bersih / Pendapatan", "Porsi laba bersih dari pendapatan.", "≥ 15% tinggi; 5-15% sedang"),
 ("EBITDAMargin", "RasioProfitabilitas", "EBITDA Margin", "EBITDA / Pendapatan", "Profitabilitas kas sebelum D&A.", ""),
 ("DER", "RasioSolvabilitas", "Debt to Equity Ratio", "Total Liabilitas / Ekuitas", "Leverage; semakin tinggi semakin rentan saat bunga naik.", "≤ 0,5 konservatif; > 1,5 berisiko (non-bank)"),
 ("NetGearing", "RasioSolvabilitas", "Net Gearing", "(Utang berbunga - Kas) / Ekuitas", "Leverage bersih kas.", "Net cash = sangat aman"),
 ("InterestCoverage", "RasioSolvabilitas", "Interest Coverage Ratio", "EBIT / Beban Bunga", "Kemampuan bayar bunga.", "< 1,5x berbahaya"),
 ("DebtToEBITDA", "RasioSolvabilitas", "Net Debt / EBITDA", "Utang bersih / EBITDA", "Lama pelunasan utang dari EBITDA.", "> 4x berisiko"),
 ("CurrentRatio", "RasioLikuiditas", "Current Ratio", "Aset Lancar / Liabilitas Lancar", "Likuiditas jangka pendek.", "≥ 1,5 sehat"),
 ("QuickRatio", "RasioLikuiditas", "Quick Ratio", "(Aset Lancar - Persediaan) / Liabilitas Lancar", "Likuiditas tanpa persediaan.", "≥ 1"),
 ("CashRatio", "RasioLikuiditas", "Cash Ratio", "Kas / Liabilitas Lancar", "Likuiditas paling ketat.", ""),
 ("AssetTurnover", "RasioEfisiensi", "Asset Turnover", "Pendapatan / Total Aset", "Produktivitas aset.", ""),
 ("InventoryTurnover", "RasioEfisiensi", "Inventory Turnover", "HPP / Persediaan", "Kecepatan perputaran persediaan.", ""),
 ("DSO", "RasioEfisiensi", "Days Sales Outstanding", "Piutang / Penjualan × 365", "Lama penagihan piutang; naik tajam = red flag.", ""),
 ("CashConversionCycle", "RasioEfisiensi", "Cash Conversion Cycle", "DIO + DSO - DPO", "Siklus kas operasional.", ""),
 ("EPSGrowth", "RasioPertumbuhan", "Pertumbuhan EPS (YoY)", "(EPS_t / EPS_t-1) - 1", "Momentum laba.", "≥ 15% tinggi; < 0 menurun"),
 ("RevenueGrowth", "RasioPertumbuhan", "Pertumbuhan Pendapatan", "(Rev_t / Rev_t-1) - 1", "Momentum bisnis.", ""),
 ("EPS", "RasioPertumbuhan", "Earnings per Share", "Laba Bersih / Saham Beredar", "Laba per lembar saham.", ""),
 ("BVPS", "RasioValuasi", "Book Value per Share", "Ekuitas / Saham Beredar", "Nilai buku per lembar.", ""),
 ("DividendYield", "RasioDividen", "Dividend Yield", "DPS / Harga", "Imbal hasil tunai.", "≥ 6% tinggi (bandingkan yield SBN)"),
 ("DPR", "RasioDividen", "Dividend Payout Ratio", "DPS / EPS", "Porsi laba dibagikan.", "> 100% tidak berkelanjutan"),
 ("NPL", "RasioPerbankan", "Non Performing Loan", "Kredit bermasalah (kol 3-5) / Total kredit", "Kualitas aset bank.", "≤ 2% sangat baik; > 5% batas OJK"),
 ("CAR", "RasioPerbankan", "Capital Adequacy Ratio", "Modal / ATMR", "Kecukupan modal bank.", "≥ 20% kuat; < 12% lemah"),
 ("NIM", "RasioPerbankan", "Net Interest Margin", "Pendapatan bunga bersih / Aset produktif", "Spread bunga bank.", "≥ 5% tinggi"),
 ("LDR", "RasioPerbankan", "Loan to Deposit Ratio", "Kredit / DPK", "Intermediasi & likuiditas bank.", "78-92% ideal"),
 ("CASA", "RasioPerbankan", "CASA Ratio", "(Giro + Tabungan) / DPK", "Dana murah; tinggi = biaya dana rendah.", "≥ 70% sangat baik"),
 ("BOPO", "RasioPerbankan", "BOPO", "Beban Operasional / Pendapatan Operasional", "Efisiensi bank.", "< 70% efisien"),
 ("CostOfCredit", "RasioPerbankan", "Cost of Credit", "Biaya pencadangan / Rata-rata kredit", "Beban risiko kredit.", "Naik = tekanan laba"),
 ("FreeCashFlow", "RasioArusKas", "Free Cash Flow", "CFO - Capex", "Kas bebas untuk dividen, buyback, bayar utang.", "Positif konsisten"),
 ("CFOtoNetIncome", "RasioArusKas", "CFO / Laba Bersih", "Arus kas operasi / Laba bersih", "Kualitas laba (accrual check).", "≥ 1 berkualitas; < 0,7 waspada"),
 ("FCFYield", "RasioArusKas", "FCF Yield", "FCF / Market Cap", "Imbal hasil kas bebas.", "≥ 8% menarik"),
]
for n, cls, l, rumus, interp, amb in R:
    add(n, cls, l, interp, rumus=rumus, interpretasi=interp, ambangBatas=amb)

add("AltmanZScore", "ModelSkorRisiko", "Altman Z-Score", "Model prediksi kebangkrutan (Altman, 1968).", rumus="Z = 1,2X1 + 1,4X2 + 3,3X3 + 0,6X4 + 1,0X5 (X1=WC/TA, X2=RE/TA, X3=EBIT/TA, X4=MVE/TL, X5=Sales/TA)", ambangBatas="Z < 1,81 distress; 1,81-2,99 abu-abu; ≥ 2,99 aman")
add("PiotroskiFScore", "ModelSkorRisiko", "Piotroski F-Score", "Skor 0-9 kualitas fundamental (profitabilitas, leverage, efisiensi).", ambangBatas="≥ 7 kuat; ≤ 3 lemah")
add("BeneishMScore", "ModelSkorRisiko", "Beneish M-Score", "Model deteksi manipulasi laba (8 variabel).", ambangBatas="M > -1,78 indikasi manipulasi")
add("DCF", "MetodeValuasi", "Discounted Cash Flow", "Nilai kini arus kas bebas masa depan didiskon WACC.", rumus="V = Σ FCF_t/(1+WACC)^t + TV/(1+WACC)^n")
add("DDM", "MetodeValuasi", "Dividend Discount Model (Gordon)", "Nilai saham dari dividen yang tumbuh konstan.", rumus="P = D1 / (r - g)")
add("ValuasiRelatif", "MetodeValuasi", "Valuasi Relatif (PER Band)", "Nilai wajar = EPS × PER rata-rata historis/peers.", rumus="Fair Value = EPS × PER_5th (dipakai aturan R-VAL-05)")
add("NAV", "MetodeValuasi", "Net Asset Value / RNAV", "Untuk properti & holding: nilai aset bersih revaluasi.")
add("SOTP", "MetodeValuasi", "Sum of The Parts", "Untuk konglomerasi (ASII, holding).")
add("GrahamNumber", "MetodeValuasi", "Graham Number", "Batas harga wajar defensif.", rumus="√(22,5 × EPS × BVPS)")
for n, l, d in [
    ("StripRatio", "Strip Ratio (Batu Bara)", "Overburden / batu bara; makin rendah makin efisien."),
    ("CashCostPerTon", "Cash Cost per Ton", "Biaya tunai produksi per ton komoditas."),
    ("ARPU", "ARPU (Telko)", "Average Revenue per User."),
    ("MarketingSales", "Marketing Sales (Properti)", "Prapenjualan properti; indikator utama pendapatan 1-3 tahun ke depan."),
    ("SSSG", "Same Store Sales Growth (Ritel)", "Pertumbuhan penjualan toko lama."),
    ("TenancyRatio", "Tenancy Ratio (Menara)", "Rata-rata penyewa per menara."),
    ("AISC", "All-in Sustaining Cost (Emas)", "Biaya produksi emas per ons; margin = harga emas - AISC."),
]:
    add(n, "MetrikIndustriSpesifik", l, d)

# ---------------------------------------------------------------- TEKNIKAL
T = [
 ("SMA", "IndikatorTren", "Simple Moving Average", "Rata-rata harga n periode (MA20, MA50, MA200).", "Harga > MA200 = tren primer naik"),
 ("EMA", "IndikatorTren", "Exponential Moving Average", "MA berbobot data terbaru.", ""),
 ("MACD", "IndikatorTren", "MACD", "EMA12 - EMA26, signal EMA9; histogram > 0 momentum naik.", "Histogram > 0 bullish"),
 ("ADX", "IndikatorTren", "Average Directional Index", "Kekuatan tren.", "> 25 tren kuat"),
 ("Ichimoku", "IndikatorTren", "Ichimoku Kinko Hyo", "Sistem tren (Tenkan, Kijun, Kumo, Chikou).", "Harga di atas Kumo bullish"),
 ("ParabolicSAR", "IndikatorTren", "Parabolic SAR", "Titik trailing stop tren.", ""),
 ("RSI", "IndikatorMomentum", "Relative Strength Index (14)", "Osilator 0-100.", "≥ 70/75 overbought; < 30 oversold; 40-65 sehat"),
 ("Stochastic", "IndikatorMomentum", "Stochastic Oscillator", "Posisi close relatif range.", "> 80 overbought; < 20 oversold"),
 ("CCI", "IndikatorMomentum", "Commodity Channel Index", "Deviasi harga dari rata-rata.", ""),
 ("WilliamsR", "IndikatorMomentum", "Williams %R", "Osilator momentum.", ""),
 ("BollingerBands", "IndikatorVolatilitas", "Bollinger Bands", "MA20 ± 2 standar deviasi; squeeze mendahului ledakan harga.", ""),
 ("ATR", "IndikatorVolatilitas", "Average True Range", "Rata-rata rentang harga; dasar stop loss sistem.", "SL = Entry - 2×ATR"),
 ("KeltnerChannel", "IndikatorVolatilitas", "Keltner Channel", "EMA ± ATR.", ""),
 ("OBV", "IndikatorVolume", "On Balance Volume", "Akumulasi volume naik/turun; divergensi OBV vs harga = jejak bandar.", ""),
 ("VWAP", "IndikatorVolume", "Volume Weighted Average Price", "Harga rata-rata tertimbang volume intraday; acuan scalper & institusi.", "Di atas VWAP = pembeli dominan"),
 ("MFI", "IndikatorVolume", "Money Flow Index", "RSI berbobot volume.", ""),
 ("AccDistLine", "IndikatorVolume", "Accumulation/Distribution Line", "Aliran uang berdasar posisi close dalam range.", ""),
 ("VolumeProfile", "IndikatorVolume", "Volume Profile", "Distribusi volume per harga (POC, value area).", ""),
]
for n, cls, l, d, amb in T:
    add(n, cls, l, d, ambangBatas=amb)

for n, cls2, l, d in [
    ("HeadAndShoulders", ["PolaBearish", "PolaReversal"], "Head and Shoulders", "Tiga puncak dengan puncak tengah tertinggi; breakdown neckline = sinyal jual."),
    ("InverseHeadAndShoulders", ["PolaBullish", "PolaReversal"], "Inverse Head and Shoulders", "Tiga lembah, lembah tengah terdalam; breakout neckline = beli."),
    ("DoubleTop", ["PolaBearish", "PolaReversal"], "Double Top", "Dua puncak setara; breakdown support tengah."),
    ("DoubleBottom", ["PolaBullish", "PolaReversal"], "Double Bottom", "Dua lembah setara (pola 'W')."),
    ("TripleBottom", ["PolaBullish", "PolaReversal"], "Triple Bottom", "Tiga kali uji support kuat."),
    ("RoundingBottom", ["PolaBullish", "PolaReversal"], "Rounding Bottom", "Dasar membulat; akumulasi jangka panjang."),
    ("CupAndHandle", ["PolaBullish", "PolaKontinuasi"], "Cup and Handle", "Mangkuk + pegangan; breakout bibir mangkuk."),
    ("BullFlag", ["PolaBullish", "PolaKontinuasi"], "Bull Flag", "Konsolidasi singkat setelah tiang naik tajam."),
    ("BearFlag", ["PolaBearish", "PolaKontinuasi"], "Bear Flag", "Konsolidasi naik singkat setelah turun tajam."),
    ("AscendingTriangle", ["PolaBullish", "PolaKontinuasi"], "Ascending Triangle", "Resistance datar, support naik."),
    ("DescendingTriangle", ["PolaBearish", "PolaKontinuasi"], "Descending Triangle", "Support datar, resistance turun."),
    ("FallingWedge", ["PolaBullish", "PolaReversal"], "Falling Wedge", "Baji menyempit turun; breakout ke atas."),
    ("RisingWedge", ["PolaBearish", "PolaReversal"], "Rising Wedge", "Baji menyempit naik; breakdown ke bawah."),
    ("SymmetricalTriangle", ["PolaKontinuasi"], "Symmetrical Triangle", "Konsolidasi menyempit; arah tergantung breakout."),
    ("RectangleRange", ["PolaKontinuasi"], "Rectangle / Trading Range", "Harga bergerak di antara support-resistance datar."),
]:
    add(n, cls2, l, d)

for n, cls, l, d in [
    ("Hammer", "CandlestickBullish", "Hammer", "Badan kecil di atas, ekor bawah panjang di area support."),
    ("InvertedHammer", "CandlestickBullish", "Inverted Hammer", "Ekor atas panjang di dasar tren turun."),
    ("BullishEngulfing", "CandlestickBullish", "Bullish Engulfing", "Lilin hijau menelan lilin merah sebelumnya."),
    ("MorningStar", "CandlestickBullish", "Morning Star", "Pola 3 lilin pembalikan naik."),
    ("PiercingLine", "CandlestickBullish", "Piercing Line", "Lilin hijau menutup di atas setengah badan merah sebelumnya."),
    ("ThreeWhiteSoldiers", "CandlestickBullish", "Three White Soldiers", "Tiga lilin hijau berturut-turut."),
    ("BullishHarami", "CandlestickBullish", "Bullish Harami", "Lilin kecil di dalam badan lilin merah besar."),
    ("BullishMarubozu", "CandlestickBullish", "Bullish Marubozu", "Lilin hijau tanpa ekor; dominasi pembeli penuh."),
    ("ShootingStar", "CandlestickBearish", "Shooting Star", "Ekor atas panjang di puncak tren naik."),
    ("HangingMan", "CandlestickBearish", "Hanging Man", "Bentuk hammer di puncak tren."),
    ("BearishEngulfing", "CandlestickBearish", "Bearish Engulfing", "Lilin merah menelan lilin hijau."),
    ("EveningStar", "CandlestickBearish", "Evening Star", "Pola 3 lilin pembalikan turun."),
    ("DarkCloudCover", "CandlestickBearish", "Dark Cloud Cover", "Lilin merah menutup di bawah setengah badan hijau."),
    ("ThreeBlackCrows", "CandlestickBearish", "Three Black Crows", "Tiga lilin merah berturut-turut."),
    ("Doji", "CandlestickIndecision", "Doji", "Open ≈ close; keraguan pasar."),
    ("SpinningTop", "CandlestickIndecision", "Spinning Top", "Badan kecil, ekor atas-bawah."),
    ("DragonflyDoji", "CandlestickBullish", "Dragonfly Doji", "Doji dengan ekor bawah panjang di support."),
    ("GravestoneDoji", "CandlestickBearish", "Gravestone Doji", "Doji dengan ekor atas panjang di resistance."),
]:
    add(n, cls, l, d)

for n, l, d in [
    ("Support", "Support", "Area harga di mana permintaan cukup kuat menahan penurunan."),
    ("Resistance", "Resistance", "Area harga di mana penawaran menahan kenaikan."),
    ("Trendline", "Trendline", "Garis penghubung higher low (uptrend) / lower high (downtrend)."),
    ("Breakout", "Breakout", "Harga menembus resistance dengan volume besar."),
    ("Breakdown", "Breakdown", "Harga menembus support ke bawah."),
    ("FalseBreakout", "False Breakout / Bull Trap", "Breakout gagal yang menjebak pembeli."),
    ("Pullback", "Pullback", "Koreksi sementara dalam tren naik."),
    ("GoldenCross", "Golden Cross", "MA50 memotong MA200 dari bawah."),
    ("DeathCross", "Death Cross", "MA50 memotong MA200 dari atas."),
    ("BullishDivergence", "Bullish Divergence", "Harga lower low, RSI/OBV higher low."),
    ("BearishDivergence", "Bearish Divergence", "Harga higher high, RSI/OBV lower high."),
    ("GapUp", "Gap Up", "Harga buka di atas high sebelumnya."),
    ("BreakawayGap", "Breakaway Gap", "Gap di awal tren baru."),
    ("ExhaustionGap", "Exhaustion Gap", "Gap di akhir tren; tanda kelelahan."),
    ("HigherHighHigherLow", "Higher High - Higher Low", "Struktur tren naik."),
]:
    add(n, "KonsepTeknikal", l, d)
for n, l, d in [
    ("DowTheory", "Dow Theory", "Tren primer, sekunder, minor; indeks harus saling konfirmasi; volume konfirmasi tren."),
    ("ElliottWave", "Elliott Wave", "5 gelombang impuls + 3 gelombang koreksi (A-B-C)."),
    ("FibonacciRetracement", "Fibonacci Retracement", "Level koreksi 23,6%, 38,2%, 50%, 61,8%, 78,6%."),
    ("WyckoffMethod", "Metode Wyckoff", "Composite Man, hukum supply-demand, cause-effect, effort-result."),
    ("SectorRotationTheory", "Teori Rotasi Sektor", "Sektor unggul bergantian mengikuti fase siklus ekonomi (Early→Mid→Late→Resesi)."),
]:
    add(n, "TeoriTeknikal", l, d)

# ---------------------------------------------------------------- BANDARMOLOGY
for n, l, d, h in [
    ("BrokerSummary", "Broker Summary", "Rekap net buy/sell per broker pada satu saham dan periode.", "Top 3 buyer konsisten (broker asing/institusi) selama >10 hari = akumulasi."),
    ("NetForeignFlow", "Net Foreign Flow", "Selisih beli-jual investor asing.", "Asing net sell besar di big caps saat MSCI freeze = outflow pasif, bukan selalu fundamental."),
    ("TopBuyerSeller", "Top Buyer/Top Seller", "Broker dengan net buy/sell terbesar.", ""),
    ("AvgPriceBandar", "Average Price Bandar", "Harga rata-rata beli broker akumulator; menjadi 'support psikologis' bandar.", "Harga di bawah avg bandar = bandar 'nyangkut', biasanya akan dijaga/diangkat."),
    ("DoneDetail", "Done Detail / Trade Book", "Rincian transaksi yang terjadi per harga & broker.", ""),
    ("RunningTrade", "Running Trade", "Aliran transaksi real-time.", ""),
    ("BidOfferImbalance", "Bid-Offer Imbalance", "Ketimpangan antrean bid vs offer.", "Bid tebal yang ditarik sebelum dimakan = fake bid (spoofing)."),
    ("IcebergOrder", "Iceberg Order", "Order besar yang ditampilkan sebagian kecil.", "Offer kecil yang terus terisi ulang di satu harga = bandar distribusi diam-diam."),
    ("CrossingBlock", "Crossing / Block Trade", "Transaksi tutup sendiri antar-akun pada pasar nego.", ""),
    ("ForeignInclusionFactor", "Foreign Inclusion Factor (FIF)", "Faktor porsi saham yang dapat dibeli asing di indeks MSCI.", "Freeze FIF oleh MSCI membatasi bobot Indonesia di portofolio global."),
    ("AccDistBrokerScore", "Skor Akumulasi/Distribusi Broker", "Skor -100..100 dari konsentrasi net buy top-5 broker vs bottom-5 (fitur 'Bandar Detector').", "≥ 20 akumulasi; ≤ -20 distribusi"),
]:
    add(n, "KonsepBandarmology", l, d, heuristikPakar=h)

for n, cls, l, d in [
    ("PolaAkumulasi", "PolaBandarBullish", "Akumulasi", "Bandar mengumpulkan barang secara bertahap; harga ditahan sideways, volume di support naik."),
    ("PolaMarkUp", "PolaBandarBullish", "Mark-Up", "Harga diangkat cepat setelah barang cukup; offer dimakan agresif (haka)."),
    ("PolaShakeout", "PolaBandarBullish", "Shakeout", "Harga dibanting singkat menembus support untuk memancing cut loss ritel, lalu kembali naik."),
    ("PolaSpring", "PolaBandarBullish", "Spring (Wyckoff)", "False breakdown di dasar akumulasi."),
    ("PolaReAkumulasi", "PolaBandarBullish", "Re-Akumulasi", "Konsolidasi akumulasi lanjutan di tengah uptrend."),
    ("PolaDistribusi", "PolaBandarBearish", "Distribusi", "Bandar melepas barang ke ritel di atas; berita positif sering muncul bersamaan."),
    ("PolaUTAD", "PolaBandarBearish", "Upthrust After Distribution", "False breakout di puncak distribusi."),
    ("PolaMarkDown", "PolaBandarBearish", "Mark-Down", "Penurunan setelah distribusi selesai."),
    ("PolaPumpAndDump", ["PolaBandarBearish", "PolaManipulatif"], "Pump and Dump ('Goreng')", "Harga dipompa dengan rumor lalu dibuang ke ritel."),
    ("PolaWashTrade", "PolaManipulatif", "Wash Trade", "Transaksi semu untuk menciptakan kesan likuid; dilarang UU Pasar Modal."),
    ("PolaSpoofing", "PolaManipulatif", "Spoofing / Fake Bid", "Order palsu besar untuk memengaruhi persepsi lalu dibatalkan."),
    ("PolaPaintingTheTape", "PolaManipulatif", "Painting the Tape / Marking the Close", "Mengatur harga penutupan."),
    ("PolaHakaHaki", "PolaBandarBullish", "Haka (Hajar Kanan)", "Beli agresif langsung di offer; tanda urgensi pembeli besar."),
]:
    add(n, cls, l, d)

for n, l, d in [
    ("Scalp_OpeningRangeBreakout", "Opening Range Breakout", "Entry saat harga menembus high 15-30 menit pertama dengan volume."),
    ("Scalp_VWAPReclaim", "VWAP Reclaim", "Entry saat harga kembali di atas VWAP setelah sempat di bawah."),
    ("Scalp_MomentumIgnition", "Momentum Ignition", "Lonjakan volume & haka beruntun memicu momentum singkat."),
    ("Scalp_BidAskSqueeze", "Bid-Ask Squeeze", "Offer tipis + bid tebal; harga mudah naik 1-3 tick."),
    ("Scalp_FirstPullback", "First Pullback", "Entry pada koreksi pertama setelah breakout."),
    ("Scalp_GapAndGo", "Gap and Go", "Gap up dengan volume besar berlanjut naik."),
    ("Scalp_EndOfDayRun", "End of Day Run", "Kenaikan menjelang pre-closing (waspada marking the close)."),
]:
    add(n, "PolaScalper", l, d)

# ---------------------------------------------------------------- SENTIMEN
for n, l, d in [
    ("Sumber_BeritaFinansial", "Berita Finansial", "Media bisnis (Bisnis.com, Kontan, CNBC Indonesia, Bloomberg, Reuters)."),
    ("Sumber_RisetAnalis", "Riset Analis", "Rekomendasi & target harga sekuritas."),
    ("Sumber_MediaSosial", "Media Sosial", "Stockbit stream, X/Twitter, Telegram; bobot kredibilitas rendah, rawan pompom."),
    ("Sumber_KeterbukaanInformasi", "Keterbukaan Informasi IDX", "Pengumuman resmi emiten/bursa; kredibilitas tertinggi."),
    ("Sumber_RegulatorBankSentral", "Rilis Regulator & Bank Sentral", "OJK, BI, The Fed, BPS."),
    ("Sumber_Rumor", "Rumor", "Informasi tak terverifikasi; diabaikan bila kredibilitas < 0,7."),
]:
    add(n, "SumberSentimen", l, d)
add("Sentimen_Positif", "KategoriSentimen", "Positif", "Skor ≥ 0,2")
add("Sentimen_Netral", "KategoriSentimen", "Netral", "-0,2 < skor < 0,2")
add("Sentimen_Negatif", "KategoriSentimen", "Negatif", "Skor ≤ -0,2")
add("ML_SentimentScorer", "KomponenML", "Aspect-Based Sentiment Scorer", "Skor leksikon finansial Indonesia + arah variabel makro × sensitivitas sektor (sentiment_scorer.py). Output: skorSentimen berita, sektor, emiten.")
add("ML_PatternDetector", "KomponenML", "Detektor Pola Chart/Candle", "Modul pengenal pola dari data OHLCV; output terdeteksiPola (input ke SWRL).")
add("ML_BacktestWeightCalibrator", "KomponenML", "Kalibrator Bobot Backtest", "Penyesuaian bobot ambang melalui walk-forward backtest; tetap di bawah kendali aturan pakar.")

# ---------------------------------------------------------------- SIKLUS EKONOMI & TEMA
add("Fase_EarlyCycle", "FaseSiklusEkonomi", "Early Cycle (Pemulihan)", "Suku bunga turun, kredit pulih; unggul: keuangan, konsumer siklikal, properti, teknologi.")
add("Fase_MidCycle", "FaseSiklusEkonomi", "Mid Cycle (Ekspansi)", "Pertumbuhan stabil; unggul: teknologi, industri, barang baku.")
add("Fase_LateCycle", "FaseSiklusEkonomi", "Late Cycle (Overheating/Ketat)", "Inflasi & bunga tinggi; unggul: energi, barang baku, kesehatan, konsumer primer.")
add("Fase_ResesiStagflasi", "FaseSiklusEkonomi", "Resesi / Stagflasi", "Pertumbuhan turun, risk-off; unggul: konsumer primer, kesehatan, infrastruktur/utilitas, emas.")

TEMA = [
 ("Tema_HilirisasiMineral", "Hilirisasi Nikel & Mineral", "Larangan ekspor bijih & smelter; Indonesia produsen nikel terbesar dunia; rantai baterai EV.", 3),
 ("Tema_EmasSafeHaven", "Emas Safe Haven & Bank Sentral", "Pembelian emas bank sentral dan premi geopolitik mendorong harga emas rekor.", 3),
 ("Tema_KetahananEnergi", "Ketahanan Energi & Gas", "Premi risiko Timur Tengah; gas sebagai energi transisi; batu bara substitusi saat minyak mahal.", 1),
 ("Tema_TransisiEnergi", "Transisi Energi (Headwind Batu Bara)", "Komitmen net zero menekan valuasi batu bara jangka panjang.", -1),
 ("Tema_MakanBergiziGratis", "Program Makan Bergizi Gratis (MBG)", "Belanja pemerintah besar untuk pangan & protein (unggas, telur, susu).", 2),
 ("Tema_Biodiesel", "Mandatori Biodiesel B40/B50", "Menyerap CPO domestik; menopang harga CPO.", 2),
 ("Tema_DataCenterAI", "Data Center & AI", "Investasi hyperscaler & kebutuhan konektivitas, fiber, menara, listrik.", 2),
 ("Tema_KonsolidasiTelko", "Konsolidasi Telko (XLSmart)", "Persaingan rasional pasca-merger; ARPU membaik.", 1),
 ("Tema_InklusiKeuangan", "Inklusi & Pendalaman Keuangan", "Penetrasi kredit rendah, bank digital, ultra-mikro.", 2),
 ("Tema_PopulasiKesehatan", "Belanja Kesehatan & JKN", "Belanja kesehatan per kapita rendah, penuaan, JKN.", 2),
 ("Tema_TigaJutaRumah", "Program 3 Juta Rumah", "Dorongan perumahan rakyat & insentif PPN DTP.", 1),
 ("Tema_Danantara", "Danantara & Konsolidasi BUMN", "Superholding BUMN; potensi efisiensi namun ada risiko kebijakan dividen.", 0),
 ("Tema_ReformasiPasarModal", "Reformasi Free Float & Transparansi", "Min. free float 15%, keterbukaan pemegang >1%, HSC alert; kunci pemulihan kepercayaan asing 1-3 th.", 2),
 ("Tema_DigitalisasiKonsumen", "Digitalisasi Konsumen", "E-commerce, ride-hailing, fintech; profitabilitas masih jadi isu.", 1),
]
for n, l, d, s in TEMA:
    add(n, "TemaStruktural", l, d, skorTemaDefault=str(s))

# ---------------------------------------------------------------- HEURISTIK PAKAR (bahasa natural)
HEUR = [
 ("H01_Petrodolar", "Efek Petrodolar", "Minyak naik → surplus petrodolar & USD kuat → dana asing keluar EM → IHSG tertekan, namun energi & batu bara diuntungkan (substitusi energi)."),
 ("H02_FedHawkish", "Fed Hawkish → EM Tertekan", "Fed menaikkan/menahan bunga tinggi → yield UST naik → DXY menguat → rupiah melemah → asing jual big caps bank."),
 ("H03_RupiahLemah", "Rupiah Lemah", "Eksportir berbasis USD (batu bara, CPO, nikel, emas) untung; importir bahan baku (farmasi, pakan, gandum, elektronik) tertekan."),
 ("H04_SukuBungaBI", "BI Rate Naik", "Bunga naik → KPR & kredit kendaraan melemah → properti & otomotif tertekan; bank dengan CASA tinggi relatif tahan."),
 ("H05_Inflasi", "Inflasi Pangan", "Inflasi pangan → daya beli turun → konsumer non-primer tertekan; produsen pangan dengan pricing power bertahan."),
 ("H06_RiskOffEmas", "Risk-off → Emas", "Konflik & ketidakpastian → safe haven emas → penambang emas (ANTM, MDKA, BRMS, AMMN via tembaga-emas) diuntungkan."),
 ("H07_MSCIFreeze", "MSCI Freeze", "Freeze FIF/ancaman reklasifikasi → dana pasif keluar dari konstituen MSCI (big caps) → diskon valuasi ekstrem → peluang 1-3 th bila reformasi diterima."),
 ("H08_ContrarianKrisis", "Kontrarian Krisis", "Pasar -40% dengan sektor di bawah 0,7× PER historis: emiten neraca kuat & dividen tinggi historis memberi return terbaik 1-3 th (preseden 2008-09, 2020-21)."),
 ("H09_SmartMoney", "Smart Money Divergence", "Harga turun + ritel jual + broker asing/institusi akumulasi = fase akumulasi; jangan ikut panic selling."),
 ("H10_DistribusiBerita", "Distribusi saat Berita Bagus", "Berita sangat positif + RSI tinggi + broker ritel net buy besar = distribusi; ambil untung."),
 ("H11_ValueTrap", "Value Trap", "PER rendah tapi laba turun, utang tinggi, downtrend = murah karena memang buruk."),
 ("H12_KonfluensiPilar", "Konfluensi Multi-Pilar", "Keyakinan tinggi hanya bila ≥3 pilar (fundamental, teknikal, bandar, sentimen, makro-geopolitik) searah."),
 ("H13_PerangDagang", "Perang Dagang AS-China", "Tarif → permintaan China melemah → logam industri & batu bara tertekan; relokasi pabrik ke ASEAN positif kawasan industri."),
 ("H14_OPEC", "Keputusan OPEC+", "Pemangkasan produksi → minyak naik; penambahan kuota → minyak turun (negatif MEDC, positif maskapai/logistik)."),
 ("H15_BelanjaPemerintah", "Belanja Pemerintah", "Program MBG → permintaan protein & pangan → unggas (CPIN, JPFA) & produsen pangan; batas: ruang fiskal & twin deficit."),
]
for n, l, d in HEUR:
    add(n, "AturanPakar", l, d)

# ---------------------------------------------------------------- KELUARAN & SDG
add("Output_PrediksiSektor", "KeluaranSistem", "Prediksi Sektor 1-3 Tahun", "Peringkat sektor + jalur penjelasan (tailwind/headwind/tema/preseden).")
add("Output_TopPickEmiten", "KeluaranSistem", "Top Pick Emiten per Sektor", "Top-3 emiten di sektor bullish berdasarkan skor total multi-pilar.")
add("Output_KesehatanFundamental", "KeluaranSistem", "Kesehatan Fundamental & Risiko Collapse", "Zona Altman, going concern, manipulasi laba, bank modal lemah.")
add("Output_SinyalQuantTrade", "KeluaranSistem", "Sinyal Quant Trade", "Entry/exit, buy on weakness, scalping, harga SL/TP berbasis ATR.")
add("Output_SkenarioWhatIf", "KeluaranSistem", "Analisis Skenario What-If", "Perbandingan Base/Bull/Bear per sektor.")
add("Output_KecocokanProfil", "KeluaranSistem", "Kecocokan Profil Investor", "Rekomendasi sesuai profil risiko persona.")
add("Output_PenjelasanEdukatif", "KeluaranSistem", "Penjelasan Edukatif (Explainable)", "Jejak penalaran + definisi konsep dasar untuk pemula.")
add("Output_PeringatanRisiko", "KeluaranSistem", "Peringatan Risiko", "Value trap, distribusi ke ritel, red flag berita, outflow pasif.")
for n, l, d in [
    ("SDG1_NoPoverty", "SDG 1 - Tanpa Kemiskinan", "Kesejahteraan finansial jangka panjang."),
    ("SDG4_QualityEducation", "SDG 4 - Pendidikan Berkualitas", "Edukasi berbasis kasus & penalaran yang dapat dijelaskan."),
    ("SDG8_DecentWork", "SDG 8 - Pekerjaan Layak & Pertumbuhan Ekonomi", "Literasi & kualitas keputusan investasi."),
    ("SDG10_ReducedInequalities", "SDG 10 - Berkurangnya Kesenjangan", "Demokratisasi insight setara analis senior bagi ritel."),
]:
    add(n, "TujuanSDG", l, d)

# ---------------------------------------------------------------- INDIKATOR MAKRO (definisi & heuristik)
for n, cls, l, d, h in [
 ("Def_PDB", "IndikatorEkonomiRiil", "Pertumbuhan PDB", "Pertumbuhan output ekonomi riil (yoy).", "PDB melambat → konsumer non-primer & properti tertekan."),
 ("Def_NeracaPerdagangan", "IndikatorEkonomiRiil", "Neraca Perdagangan", "Ekspor - impor barang.", "Surplus mengecil → tekanan rupiah."),
 ("Def_TransaksiBerjalan", "IndikatorEkonomiRiil", "Neraca Transaksi Berjalan", "Current account: perdagangan barang-jasa, pendapatan primer & sekunder.", "Defisit membesar + defisit finansial = twin deficit → rupiah rentan."),
 ("Def_CadanganDevisa", "IndikatorEkonomiRiil", "Cadangan Devisa", "Aset valas BI untuk stabilisasi rupiah.", "Turun cepat = BI agresif intervensi."),
 ("Def_PMI", "IndikatorEkonomiRiil", "PMI Manufaktur", "Purchasing Managers' Index; > 50 ekspansi.", "PMI < 50 beruntun → industri & bahan baku melemah."),
 ("Def_IKK", "IndikatorEkonomiRiil", "Indeks Keyakinan Konsumen", "Survei BI; > 100 optimis.", "IKK turun → ritel & otomotif melemah."),
 ("Def_PenjualanMobil", "IndikatorEkonomiRiil", "Penjualan Mobil (Gaikindo)", "Indikator daya beli kelas menengah.", "Dasar proyeksi ASII & AUTO."),
 ("Def_YieldSBN10Y", "IndikatorMoneter", "Yield SBN 10 Tahun", "Imbal hasil obligasi pemerintah acuan.", "Yield naik → cost of equity naik → PER wajar turun."),
 ("Def_YieldUST10Y", "IndikatorMoneter", "Yield US Treasury 10Y", "Risk-free global.", "Yield UST tertinggi sejak 2002 (Okt 2026) menekan aset EM."),
 ("Def_DotPlot", "IndikatorMoneter", "FOMC Dot Plot", "Proyeksi suku bunga tiap anggota FOMC.", "Median dot naik = hawkish."),
 ("Def_QT_QE", "IndikatorMoneter", "Quantitative Tightening / Easing", "Pengurangan/penambahan neraca bank sentral.", "QT menyedot likuiditas global."),
 ("Def_CarryTrade", "IndikatorMoneter", "Carry Trade (Yen/USD)", "Meminjam mata uang berbunga rendah untuk aset berimbal tinggi.", "Unwinding carry trade = risk-off mendadak di EM."),
 ("Def_FedFundsFutures", "IndikatorMoneter", "Fed Funds Futures (CME FedWatch)", "Probabilitas pasar atas keputusan FOMC.", "Perubahan probabilitas > 20 pp = repricing cepat."),
 ("Def_NetForeignBEI", "IndikatorAliranDana", "Net Foreign Buy/Sell BEI", "Aliran dana asing harian di pasar reguler.", "Net sell berturut > 10 hari di big caps = tekanan IHSG."),
 ("Def_CPI_US", "IndikatorEkonomiRiil", "CPI/PCE Amerika Serikat", "Inflasi AS; PCE adalah acuan The Fed.", "Core PCE > 3% → Fed sulit memangkas."),
 ("Def_HargaMinyak", "IndikatorHargaKomoditas", "Harga Minyak (Brent/WTI)", "Acuan energi global.", "Brent > US$100 → inflasi impor & beban subsidi APBN."),
 ("Def_HBA", "IndikatorHargaKomoditas", "Harga Batubara Acuan (HBA)", "Acuan pemerintah untuk royalti & DMO.", ""),
 ("Def_HargaReferensiCPO", "IndikatorHargaKomoditas", "Harga Referensi CPO (Kemendag)", "Dasar bea keluar & pungutan ekspor CPO.", ""),
]:
    add(n, cls, l, d, heuristikPakar=h)

# ---------------------------------------------------------------- tambahan konsep dasar
add("TahapanIPO", "InstrumenPasarModal", "Tahapan IPO", "Pra-efektif → bookbuilding → efektif OJK → penawaran umum (e-IPO) → penjatahan → pencatatan di BEI.")
add("LockUp", "MekanismePerdagangan", "Lock-up Period", "Larangan menjual saham pra-IPO dalam periode tertentu.", heuristikPakar="Berakhirnya lock-up sering memicu tekanan jual.")
add("CumExDate", "AksiKorporasiPositif", "Cum Date & Ex Date", "Cum date: hari terakhir berhak dividen di pasar reguler; ex date: hari pertama tanpa hak.")
add("PapanUtama", "MekanismePerdagangan", "Papan Utama", "Papan untuk emiten besar dengan rekam jejak.")
add("PapanPengembangan", "MekanismePerdagangan", "Papan Pengembangan", "Papan untuk emiten yang belum memenuhi papan utama.")
add("PapanAkselerasi", "MekanismePerdagangan", "Papan Akselerasi", "Papan untuk emiten aset skala kecil/menengah.")
add("PapanEkonomiBaru", "MekanismePerdagangan", "Papan Ekonomi Baru", "Papan untuk perusahaan teknologi/inovasi dengan saham hak suara multipel.")
add("ShortSelling", "MekanismePerdagangan", "Short Selling", "Menjual efek yang belum dimiliki; di BEI terbatas pada efek & anggota bursa tertentu.")
add("MarginTrading", "MekanismePerdagangan", "Transaksi Margin", "Pembelian dengan pinjaman dana dari sekuritas; forced sell saat harga jatuh memperdalam koreksi.", heuristikPakar="Saat crash, forced sell margin menciptakan harga di bawah nilai wajar (peluang bagi kas tunai).")
add("Diversifikasi_Sektor", "ManajemenRisiko", "Batas Konsentrasi Sektor", "Batasi maksimal ~25-30% portofolio per sektor.")
add("MaxDrawdown", "ManajemenRisiko", "Maximum Drawdown", "Penurunan terbesar dari puncak ke lembah portofolio.")
add("SharpeRatio", "ManajemenRisiko", "Sharpe Ratio", "Return lebih per unit volatilitas.", rumus="(Rp - Rf) / σp")
add("Beta", "ManajemenRisiko", "Beta Saham", "Sensitivitas return saham terhadap IHSG.", ambangBatas="> 1 lebih volatil dari pasar")
add("WalkForwardBacktest", "KomponenML", "Backtest Walk-Forward", "Evaluasi rolling: kalibrasi di jendela t, uji di t+1, terhadap baseline IHSG/LQ45.")
