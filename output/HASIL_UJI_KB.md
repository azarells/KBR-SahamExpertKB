# Hasil Uji Knowledge Base — SahamExpertKB v2

Tanggal acuan data: **2026-11-19** · Sumber: `output/SahamExpertKB_v2_inferred.owl` (hasil Pellet) · Dijalankan dengan `python3 tools/uji_kb.py --whatif`

## Ringkasan: **103/103 soal lulus**

| Modul | Lulus |
|---|---|
| Struktur KB | 4/4 |
| Uji kebenaran aturan | 3/3 |
| Pengetahuan dasar | 15/15 |
| Fundamental | 9/9 |
| Teknikal | 7/7 |
| Bandarmology | 8/8 |
| Sentimen | 6/6 |
| Geopolitik & makro | 9/9 |
| Indeks | 5/5 |
| Prediksi sektor | 8/8 |
| Rekomendasi emiten | 7/7 |
| Meta-penalaran | 11/11 |
| Stakeholder | 3/3 |
| Kualitas data | 3/3 |
| What-if skenario | 2/2 |
| What-if data emiten | 1/1 |
| What-if pasar | 2/2 |

Pemetaan 12 competency questions (CQ) proposal → soal uji: CQ1 = I01, CQ2 = I03, CQ3 = J01, CQ4 = I04, CQ5 = K01, CQ6 = C04, CQ7 = K08, CQ8 = J02, CQ9 = G01, CQ10 = K04, CQ11 = L02, CQ12 = B01

## Struktur KB

### A01 — Apakah knowledge base konsisten (tidak ada kontradiksi logika)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Reasoner › Pellet › Start reasoner. Jika tidak muncul dialog *Inconsistent ontology* dan kelas `owl:Nothing` kosong, KB konsisten.
- **Jawaban KB:** CONSISTENT = true (OWLAPI + Pellet)

### A02 — Berapa ukuran ontologi (kelas, properti, individu, aturan SWRL)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Active Ontology › tab *Ontology metrics*.
- **Jawaban KB:** CLASSES=298, OBJECT_PROPERTIES=65, DATA_PROPERTIES=220, INDIVIDUALS=1392, SWRL_RULES=303, TOTAL_AXIOMS=15519

### A03 — Apakah porsi knowledge base ≥ 80% dibanding porsi reasoning (aturan)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Ontology metrics: (Axiom count − SWRL rules) ÷ Axiom count.
- **Jawaban KB:** KB = 98.0% dari 15519 aksioma; aturan SWRL = 303 aksioma

### A04 — Berapa aturan SWRL per pilar analisis (semua aturan berkode & berpilar)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Window › Tabs › SWRLTab: kolom *Name* = kode aturan, kolom *Comment* = penjelasan.
- **Jawaban KB:** total 303 aturan · Fundamental 30, Regime Pasar 24, Teknikal 16, Konfluensi 15, Integrasi 14, Bandarmology 13, Sentimen 13, Geopolitik 11, Fundamental-Risiko 10, Quant Trade 10, Tesis & Invalidasi 10, Fundamental-Valuasi 8, Tata Kelola 8, Prediksi Sektor 7, Robustness Skenario 7, Katalis 6, Stakeholder 6, Struktur Pasar 6, Adaptif Regime 5, Fundamental-Sektor 5, Reaction Function 5, Refleksivitas 5, Rotasi Sektor 5, Bandarmology-Sektor 4, Bandarmology-Wyckoff 4, Ekspektasi Laba 4, Geopolitik→Emiten 4, Kapitulasi 4, Konflik Sinyal 4, Kualitas Data 4, Teknikal-Pola 4, Valuasi Relatif Obligasi 4, Case-Based Reasoning 3, Likuiditas 3, Makro-Geopolitik 3, Profil Investor 3, Skenario 3, Bandarmology-Broker 2, Intermarket 2, Konstruksi Portofolio 2, Manajemen Posisi 2, Scalper Pattern 2, Tema Struktural 2, Peringatan 1

<details><summary>SPARQL</summary>

```sparql
SELECT ?pilar (COUNT(?r) AS ?jumlah) WHERE { ?r ex:kodeAturan ?k ; ex:pilarAnalisis ?pilar } GROUP BY ?pilar ORDER BY DESC(?jumlah)
```
</details>

## Uji kebenaran aturan

### A05 — Apakah setiap emiten mendapat TEPAT SATU nilai per pilar skor (interval aturan saling lepas & menutup domain)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Pilih beberapa emiten di *Individuals*, lihat *Property assertions* (kuning): skorFundamental, skorValuasi, skorTeknikal, skorBandar masing-masing hanya satu nilai.
- **Jawaban KB:** 67/67 emiten punya tepat 1 nilai di tiap pilar

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode (COUNT(DISTINCT ?f) AS ?nF) (COUNT(DISTINCT ?v) AS ?nV) (COUNT(DISTINCT ?t) AS ?nT) (COUNT(DISTINCT ?b) AS ?nB) (COUNT(DISTINCT ?x) AS ?nTotal)
WHERE { ?e a ex:Emiten ; ex:kodeSaham ?kode .
 OPTIONAL { ?e ex:skorFundamental ?f } OPTIONAL { ?e ex:skorValuasi ?v } OPTIONAL { ?e ex:skorTeknikal ?t }
 OPTIONAL { ?e ex:skorBandar ?b } OPTIONAL { ?e ex:skorTotalEmiten ?x } } GROUP BY ?kode
```
</details>

### A06 — Apakah skor total = jumlah 8 komponen (aritmetika swrlb:add benar) untuk semua emiten?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Contoh ANTM di *Property assertions*: fundamental + valuasi + teknikal + bandar + sentimen + kontribusiSektor + penaltiRisiko + likuiditas = skorTotalEmiten.
- **Jawaban KB:** 67/67 emiten cocok. Contoh ANTM: 9+3+7+5+(-1)+(2)+(0)+2 = 27; BRMS: 4+2+6+4+(0)+(2)+(0)+2 = 20

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?f ?v ?t ?b ?s ?k ?p ?l ?total WHERE { ?e a ex:Emiten ; ex:kodeSaham ?kode ; ex:skorFundamental ?f ; ex:skorValuasi ?v ;
 ex:skorTeknikal ?t ; ex:skorBandar ?b ; ex:skorSentimen ?s ; ex:skorKontribusiSektor ?k ; ex:penaltiRisiko ?p ; ex:poinLikuiditas ?l ; ex:skorTotalEmiten ?total } ORDER BY ?kode
```
</details>

### A07 — Apakah aturan bekerja pada emiten UJI fiktif (unit test aturan tata kelola/gorengan/collapse)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `EmitenUji` → klik tiap individu, lihat kelas inferensi (kuning) di *Types*.
- **Jawaban KB:** UJI_GADAI: AkumulasiDidominasiRitel, DistribusiKeRitel, ERPSangatMenarik, FaseMarkDownWyckoff, FundamentalLemah, KonfluensiRendah, RisikoForcedSellPengendali, SinyalHindari, SinyalScalpingHindari, TrenTurun, UnderperformPasar, Undervalued, ValueTrap, ZonaAbuAbu · UJI_GORENG: AkumulasiDidominasiRitel, DistribusiBandar, DistribusiKeRitel, FaseDistribusiWyckoff, FundamentalLemah, IndikasiSahamGorengan, KonfluensiRendah, LonjakanVolume, MahalVsObligasi, MomentumTanpaFundamental, OutperformPasar, Overbought, Overvalued, RisikoGoingConcern, RisikoHSC, RisikoManipulasiLaba, RisikoPumpAndDump, SinyalExit, SinyalHindari, TrenNaik, TungguKonfirmasi, ZonaDistress · UJI_INSIDER: ERPSangatMenarik, FundamentalKuat, KualitasLabaTinggi, SinyalOrangDalam, TrenTurun, Undervalued, ZonaAman

<details><summary>SPARQL</summary>

```sparql
SELECT ?e ?kelas WHERE { ?e a ex:EmitenUji ; a ?k . ?k rdfs:subClassOf* ex:KategoriInferensi .
 FILTER(?k NOT IN (ex:KategoriInferensi, ex:InferensiEmiten, ex:PenandaKualitasData)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?e ?kelas
```
</details>

## Pengetahuan dasar

### B01 — Apa itu PER, bagaimana rumusnya, dan kapan dianggap murah?  *(CQ12)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individuals › `PER` → panel *Annotations*: `rumus`, `interpretasi`, `ambangBatas`.
- **Jawaban KB:** Price to Earnings Ratio: rumus Harga / EPS. Berapa tahun laba untuk 'balik modal'. Bandingkan dengan rata-rata historis & sektor. Ambang: Murah bila < 0,85× rata-rata 5 th; mahal bila ≥ 1,1×

<details><summary>SPARQL</summary>

```sparql
SELECT ?label ?rumus ?interpretasi ?ambang WHERE { ex:PER rdfs:label ?label ; ex:rumus ?rumus ; ex:interpretasi ?interpretasi ; ex:ambangBatas ?ambang }
```
</details>

### B02 — Rasio keuangan apa saja yang ada di KB beserta rumusnya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `RasioKeuangan` (centang *Instances*); klik individu untuk melihat anotasi `rumus`.
- **Jawaban KB:** (40 rasio) CFOtoNetIncome [RasioArusKas] = Arus kas operasi / Laba bersih; FCFYield [RasioArusKas] = FCF / Market Cap; FreeCashFlow [RasioArusKas] = CFO - Capex; DPR [RasioDividen] = DPS / EPS; DividendYield [RasioDividen] = DPS / Harga; AssetTurnover [RasioEfisiensi] = Pendapatan / Total Aset; CashConversionCycle [RasioEfisiensi] = DIO + DSO - DPO; DSO [RasioEfisiensi] = Piutang / Penjualan × 365; InventoryTurnover [RasioEfisiensi] = HPP / Persediaan; CashRatio [RasioLikuiditas] = Kas / Liabilitas Lancar; CurrentRatio [RasioLikuiditas] = Aset Lancar / Liabilitas Lancar; QuickRatio [RasioLikuiditas] = (Aset Lancar - Persediaan) / Liabilitas Lancar; BOPO [RasioPerbankan] = Beban Operasional / Pendapatan Operasional; CAR [RasioPerbankan] = Modal / ATMR; CASA [RasioPerbankan] = (Giro + Tabungan) / DPK; CostOfCredit [RasioPerbankan] = Biaya pencadangan / Rata-rata kredit; LDR [RasioPerbankan] = Kredit / DPK; NIM [RasioPerbankan] = Pendapatan bunga bersih / Aset produktif; NPL [RasioPerbankan] = Kredit bermasalah (kol 3-5) / Total kredit; EPS [RasioPertumbuhan] = Laba Bersih / Saham Beredar; EPSGrowth [RasioPertumbuhan] = (EPS_t / EPS_t-1) - 1; RevenueGrowth [RasioPertumbuhan] = (Rev_t / Rev_t-1) - 1; EBITDAMargin [RasioProfitabilitas] = EBITDA / Pendapatan; GPM [RasioProfitabilitas] = Laba Kotor / Pendapatan; NPM [RasioProfitabilitas] = Laba Bersih / Pendapatan; OPM [RasioProfitabilitas] = Laba Usaha / Pendapatan; ROA [RasioProfitabilitas] = Laba Bersih / Total Aset; ROE [RasioProfitabilitas] = Laba Bersih / Ekuitas; ROIC [RasioProfitabilitas] = NOPAT / (Ekuitas + Utang berbunga); DER [RasioSolvabilitas] = Total Liabilitas / Ekuitas; DebtToEBITDA [RasioSolvabilitas] = Utang bersih / EBITDA; InterestCoverage [RasioSolvabilitas] = EBIT / Beban Bunga; NetGearing [RasioSolvabilitas] = (Utang berbunga - Kas) / Ekuitas; BVPS [RasioValuasi] = Ekuitas / Saham Beredar; EV_EBITDA [RasioValuasi] = (Market Cap + Utang - Kas) / EBITDA; EarningsYield [RasioValuasi] = EPS / Harga = 1/PER; PBV [RasioValuasi] = Harga / BVPS; PEG [RasioValuasi] = PER / Pertumbuhan EPS (%); PER [RasioValuasi] = Harga / EPS; PSR [RasioValuasi] = Market Cap / Penjualan

<details><summary>SPARQL</summary>

```sparql
SELECT ?r ?kelompok ?rumus WHERE { ?r a ex:RasioKeuangan ; a ?k . ?k rdfs:subClassOf ex:RasioKeuangan . OPTIONAL { ?r ex:rumus ?rumus }
 BIND(STRAFTER(STR(?k),"#") AS ?kelompok) } ORDER BY ?kelompok ?r
```
</details>

### B03 — Rasio khusus perbankan apa saja dan apa ambang sehatnya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `RasioPerbankan`.
- **Jawaban KB:** BOPO (Beban Operasional / Pendapatan Operasional; ambang: < 70% efisien); CAR (Modal / ATMR; ambang: ≥ 20% kuat; < 12% lemah); CASA ((Giro + Tabungan) / DPK; ambang: ≥ 70% sangat baik); CostOfCredit (Biaya pencadangan / Rata-rata kredit; ambang: Naik = tekanan laba); LDR (Kredit / DPK; ambang: 78-92% ideal); NIM (Pendapatan bunga bersih / Aset produktif; ambang: ≥ 5% tinggi); NPL (Kredit bermasalah (kol 3-5) / Total kredit; ambang: ≤ 2% sangat baik; > 5% batas OJK)

<details><summary>SPARQL</summary>

```sparql
SELECT ?r ?rumus ?ambang WHERE { ?r a ex:RasioPerbankan . OPTIONAL { ?r ex:rumus ?rumus } OPTIONAL { ?r ex:ambangBatas ?ambang } } ORDER BY ?r
```
</details>

### B04 — Bagaimana mekanisme perdagangan di BEI (ARB/ARA, lot, T+2, sesi, papan)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `MekanismePerdagangan`; klik individu → `rdfs:comment`.
- **Jawaban KB:** Auto Rejection Atas (ARA): Batas kenaikan harga harian maksimum; order di atas batas ditolak sistem JATS.; Auto Rejection Bawah (ARB): Batas penurunan harga harian maksimum.; Fraksi Harga (Tick Size): Kelipatan perubahan harga: Rp1 (<Rp200), Rp2 (Rp200-<500), Rp5 (Rp500-<2.000), Rp10 (Rp2.000-<5.000), Rp25 (≥Rp5.000).; Free Float: Porsi saham yang dimiliki publik (<5%) dan dapat diperdagangkan bebas; dasar bobot indeks MSCI (Foreign Inclusion Factor).; Full Call Auction (FCA): Mekanisme lelang berkala untuk saham Papan Pemantauan Khusus; order book tidak transparan.; Limit Order: Order dengan harga tertentu.; Market Order: Order yang langsung dicocokkan dengan harga terbaik yang tersedia.; Kapitalisasi Pasar: Harga × jumlah saham beredar.; Lock-up Period: Larangan menjual saham pra-IPO dalam periode tertentu.; Lot: Satuan perdagangan saham di BEI; 1 lot = 100 lembar.; Transaksi Margin: Pembelian dengan pinjaman dana dari sekuritas; forced sell saat harga jatuh memperdalam koreksi.; Order Book (Bid-Offer): Daftar antrean beli (bid) dan jual (offer) per tingkat harga.; Papan Akselerasi: Papan untuk emiten aset skala kecil/menengah.; Papan Ekonomi Baru: Papan untuk perusahaan teknologi/inovasi dengan saham hak suara multipel.; Papan Pengembangan: Papan untuk emiten yang belum memenuhi papan utama.; Papan Utama: Papan untuk emiten besar dengan rekam jejak.; Pasar Negosiasi: Pasar transaksi berdasarkan negosiasi (crossing/block trade) di luar order book reguler.; Pasar Reguler: Pasar dengan mekanisme tawar-menawar berkelanjutan dalam satuan lot.; Pasar Tunai: Pasar dengan penyelesaian T+0 untuk pemenuhan kewajiban.; Pra-Pembukaan (Pre-opening): Periode pembentukan harga pembukaan melalui call auction.; Pra-Penutupan (Pre-closing): Periode pembentukan harga penutupan melalui call auction.; SID & RDN: Single Investor Identification (KSEI) dan Rekening Dana Nasabah untuk dana investor.; Sesi Perdagangan: Sesi I dan Sesi II perdagangan reguler hari bursa.; Penyelesaian T+2: Penyelesaian transaksi (serah saham & dana) dua hari bursa setelah transaksi; dijamin KPEI.; Short Selling: Menjual efek yang belum dimiliki; di BEI terbatas pada efek & anggota bursa tertentu.

<details><summary>SPARQL</summary>

```sparql
SELECT ?m ?label ?penjelasan WHERE { ?m a ex:MekanismePerdagangan ; rdfs:label ?label . OPTIONAL { ?m rdfs:comment ?penjelasan } } ORDER BY ?m
```
</details>

### B05 — Aksi korporasi mana yang berdampak positif, netral, dan negatif?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `AksiKorporasiPositif`, `AksiKorporasiNegatif`, `AksiKorporasiNetral`.
- **Jawaban KB:** Negatif: DelistingPaksa, PrivatePlacement, ReverseStockSplit, RightIssue · Netral: Akuisisi, DividenSaham, GoPrivate, Merger, RUPS, TenderOffer · Positif: Buyback, CumExDate, DividenTunai, StockSplit

<details><summary>SPARQL</summary>

```sparql
SELECT ?dampak ?a WHERE { ?a a ?k . FILTER(?k IN (ex:AksiKorporasiPositif, ex:AksiKorporasiNegatif, ex:AksiKorporasiNetral)) BIND(STRAFTER(STR(?k),"AksiKorporasi") AS ?dampak) } ORDER BY ?dampak ?a
```
</details>

### B06 — Indikator teknikal apa saja dan bagaimana membaca RSI & MACD?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `IndikatorTeknikal`; individu `RSI`, `MACD` → anotasi.
- **Jawaban KB:** (18) ADX, ATR, AccDistLine, BollingerBands, CCI, EMA, Ichimoku, KeltnerChannel, MACD, MFI, OBV, ParabolicSAR, RSI, SMA, Stochastic, VWAP, VolumeProfile, WilliamsR · MACD:  EMA12 - EMA26, signal EMA9; histogram > 0 momentum naik.; RSI:  Osilator 0-100.

<details><summary>SPARQL</summary>

```sparql
SELECT ?i ?rumus ?arti WHERE { ?i a ex:IndikatorTeknikal . OPTIONAL { ?i ex:rumus ?rumus } OPTIONAL { ?i rdfs:comment ?arti } } ORDER BY ?i
```
</details>

### B07 — Pola chart mana yang bullish, bearish, reversal, dan kontinuasi?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `PolaBullish`, `PolaBearish`, `PolaReversal`, `PolaKontinuasi`.
- **Jawaban KB:** PolaBearish: BearFlag, DescendingTriangle, DoubleTop, HeadAndShoulders, RisingWedge · PolaBullish: AscendingTriangle, BullFlag, CupAndHandle, DoubleBottom, FallingWedge, InverseHeadAndShoulders, RoundingBottom, TripleBottom · PolaKontinuasi: AscendingTriangle, BearFlag, BullFlag, CupAndHandle, DescendingTriangle, RectangleRange, SymmetricalTriangle · PolaReversal: DoubleBottom, DoubleTop, FallingWedge, HeadAndShoulders, InverseHeadAndShoulders, RisingWedge, RoundingBottom, TripleBottom

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis ?p WHERE { ?p a ?k . FILTER(?k IN (ex:PolaBullish, ex:PolaBearish, ex:PolaReversal, ex:PolaKontinuasi)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?p
```
</details>

### B08 — Pola candlestick apa saja yang dikenali?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `PolaCandlestick` (subkelas CandlestickBullish/Bearish/Indecision).
- **Jawaban KB:** Bearish: BearishEngulfing, DarkCloudCover, EveningStar, GravestoneDoji, HangingMan, ShootingStar, ThreeBlackCrows · Bullish: BullishEngulfing, BullishHarami, BullishMarubozu, DragonflyDoji, Hammer, InvertedHammer, MorningStar, PiercingLine, ThreeWhiteSoldiers · Indecision: Doji, SpinningTop

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis ?c WHERE { ?c a ?k . FILTER(?k IN (ex:CandlestickBullish, ex:CandlestickBearish, ex:CandlestickIndecision)) BIND(STRAFTER(STR(?k),"Candlestick") AS ?jenis) } ORDER BY ?jenis ?c
```
</details>

### B09 — Teori teknikal apa saja (Dow, Elliott, Wyckoff, Fibonacci, rotasi sektor)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `TeoriTeknikal`.
- **Jawaban KB:** DowTheory: Tren primer, sekunder, minor; indeks harus saling konfirmasi; volume konfirmasi tren.; ElliottWave: 5 gelombang impuls + 3 gelombang koreksi (A-B-C).; FibonacciRetracement: Level koreksi 23,6%, 38,2%, 50%, 61,8%, 78,6%.; SectorRotationTheory: Sektor unggul bergantian mengikuti fase siklus ekonomi (Early→Mid→Late→Resesi).; WyckoffMethod: Composite Man, hukum supply-demand, cause-effect, effort-result.

<details><summary>SPARQL</summary>

```sparql
SELECT ?t ?arti WHERE { ?t a ex:TeoriTeknikal . OPTIONAL { ?t rdfs:comment ?arti } } ORDER BY ?t
```
</details>

### B10 — Bias perilaku investor apa yang dimodelkan?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `BiasPerilaku`.
- **Jawaban KB:** AnchoringBias: Terpaku pada harga beli/harga tertinggi lama.; ConfirmationBias: Hanya mencari informasi yang mendukung keyakinan.; DispositionEffect: Cepat menjual saham untung, menahan saham rugi.; FOMO: Membeli karena takut ketinggalan reli; sering di pucuk.; HerdingBias: Ikut-ikutan mayoritas/influencer tanpa analisis.; LossAversion: Rasa sakit rugi lebih besar dari senang untung; menahan saham rugi terlalu lama.; Overconfidence: Terlalu yakin pada analisis sendiri; overtrading.; PanicSelling: Menjual karena panik saat pasar jatuh tajam; sering dimanfaatkan bandar untuk akumulasi murah.; RecencyBias: Menganggap tren terbaru akan berlanjut selamanya.

<details><summary>SPARQL</summary>

```sparql
SELECT ?b ?arti WHERE { ?b a ex:BiasPerilaku . OPTIONAL { ?b rdfs:comment ?arti } } ORDER BY ?b
```
</details>

### B11 — Instrumen pasar modal dan gaya investasi apa saja yang dikenal KB?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `InstrumenPasarModal` dan `GayaInvestasi`.
- **Jawaban KB:** GayaInvestasi: ContrarianInvesting, DayTrading, DividendInvesting, DollarCostAveraging, GARP, GrowthInvesting, IndexInvesting, MomentumTrading, PositionTrading, Scalping, SwingTrading, ValueInvesting · InstrumenPasarModal: ETF, HMETD_Right, IPO, ObligasiKorporasi, ReksaDanaSaham, SahamBiasa, SahamPreferen, SingleStockFutures, SuratBerhargaNegara, TahapanIPO, Waran

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis ?i WHERE { ?i a ?k . FILTER(?k IN (ex:InstrumenPasarModal, ex:GayaInvestasi)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?i
```
</details>

### B12 — Konsep manajemen risiko apa saja (stop loss, position sizing, dll.)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `ManajemenRisiko`.
- **Jawaban KB:** AveragingDown; AveragingUp; Beta; Diversifikasi; Diversifikasi_Sektor; MarginOfSafety; MaxDrawdown; PositionSizing (Jumlah lembar = (Modal × %Risiko) / (Entry - SL)); RiskRewardRatio; SharpeRatio ((Rp - Rf) / σp); StopLoss (SL = Entry - 2 × ATR (aturan sistem)); TakeProfit (TP = Entry + 3 × ATR (aturan sistem)); TrailingStop

<details><summary>SPARQL</summary>

```sparql
SELECT ?m ?rumus ?arti WHERE { ?m a ex:ManajemenRisiko . OPTIONAL { ?m ex:rumus ?rumus } OPTIONAL { ?m rdfs:comment ?arti } } ORDER BY ?m
```
</details>

### B13 — Biaya & pajak transaksi saham di Indonesia?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `BiayaDanPajak`.
- **Jawaban KB:** FeeTransaksi: Biaya beli (~0,15%) dan jual (~0,25%, termasuk pajak) tergantung sekuritas.; PPhFinalPenjualan: Pajak final 0,1% dari nilai bruto penjualan saham.; PajakDividen: PPh dividen 10% final bagi WP orang pribadi dalam negeri; dapat dibebaskan bila diinvestasikan kembali sesuai ketentuan.

<details><summary>SPARQL</summary>

```sparql
SELECT ?b ?arti WHERE { ?b a ex:BiayaDanPajak . OPTIONAL { ?b rdfs:comment ?arti } } ORDER BY ?b
```
</details>

### B14 — Status pengawasan BEI apa saja (suspensi, UMA, notasi khusus, papan pemantauan)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `StatusPengawasan`.
- **Jawaban KB:** BatasHargaGocap: Harga minimum di Papan Utama/Pengembangan; saham 'gocap' tertahan tak bisa turun lagi di pasar reguler.; CircuitBreakerTradingHalt: Penghentian perdagangan pasar bila IHSG turun tajam dalam sehari.; NotasiKhusus: Huruf penanda kondisi emiten (mis. E=ekuitas negatif, M=PKPU, X=papan pemantauan khusus).; PapanPemantauanKhusus: Papan untuk saham bermasalah likuiditas/fundamental; diperdagangkan via FCA.; Suspensi: Penghentian sementara perdagangan saham oleh bursa.; UnusualMarketActivity: Pengumuman bursa atas pergerakan harga/volume tidak wajar.

<details><summary>SPARQL</summary>

```sparql
SELECT ?s ?arti WHERE { ?s a ex:StatusPengawasan . OPTIONAL { ?s rdfs:comment ?arti } } ORDER BY ?s
```
</details>

### B15 — Heuristik pakar apa yang dipakai (aturan praktis ahli)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Cari anotasi `heuristikPakar` (Window › Tabs › *Annotation*/*Search*: heuristikPakar).
- **Jawaban KB:** (37) AccDistBrokerScore: ≥ 20 akumulasi; ≤ -20 distribusi; AutoRejectionAtas: ARA beruntun dengan volume tipis & broker tunggal = tanda saham digoreng.; AveragingDown: Averaging down pada value trap = bencana; pastikan bukan ZonaDistress.; AvgPriceBandar: Harga di bawah avg bandar = bandar 'nyangkut', biasanya akan dijaga/diangkat.; BidOfferImbalance: Bid tebal yang ditarik sebelum dimakan = fake bid (spoofing).; BrokerSummary: Top 3 buyer konsisten (broker asing/institusi) selama >10 hari = akumulasi.; Buyback: Buyback saat krisis pasar (OJK mengizinkan tanpa RUPS dalam kondisi berfluktuasi signifika; ContrarianInvesting: 'Be fearful when others are greedy, greedy when others are fearful.' Krisis = peluang bagi …

<details><summary>SPARQL</summary>

```sparql
SELECT ?h ?isi WHERE { ?h ex:heuristikPakar ?isi } ORDER BY ?h
```
</details>

## Fundamental

### C01 — Emiten mana yang fundamentalnya kuat, sedang, dan lemah?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `FundamentalKuat` / `FundamentalSedang` / `FundamentalLemah`.
- **Jawaban KB:** FundamentalKuat (23): AADI, AMMN, ANTM, BBCA, BMRI, BRIS, CPIN, DCII, DMAS, DSNG, IMPC, JPFA, LSIP, MAPA, MIKA, NCKL, PWON, SIDO, SILO, SMDR, TINS, TMAS, UNTR · FundamentalLemah (9): BBTN, BRMS, BUKA, ERAA, EXCL, GOTO, INKP, SMGR, SMRA · FundamentalSedang (32): AALI, ACES, AKRA, AMRT, ASII, ASSA, AUTO, BBNI, BBRI, BIRD, BSDE, CTRA, EMTK, HEAL, ICBP, INCO, INDF, ISAT, ITMG, JSMR, KLBF, MAPI, MDKA, MEDC, MTDL, MTEL, MYOR, PGAS, PTBA, TLKM, TOWR, UNVR

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas ?kode WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:FundamentalKuat, ex:FundamentalSedang, ex:FundamentalLemah)) FILTER NOT EXISTS { ?e a ex:EmitenUji }
 BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas ?kode
```
</details>

### C02 — Emiten mana yang undervalued, fair, overvalued (PER vs rata-rata 5 tahun)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `Undervalued`, `FairValued`, `Overvalued`. SQWRL: `Emiten(?e) ^ rasioPERvsHistoris(?e, ?r) -> sqwrl:select(?e, ?r) ^ sqwrl:orderBy(?r)`
- **Jawaban KB:** FairValued (4): TMAS(0.92×), ITMG(0.92×), BUKA(1.00×), IMPC(1.00×) · Overvalued (5): EXCL(1.12×), MDKA(1.14×), DCII(1.25×), EMTK(1.25×), SMGR(1.25×) · Undervalued (54): ACES(0.36×), SMRA(0.43×), UNVR(0.44×), JSMR(0.50×), MAPI(0.50×), TINS(0.53×), BBRI(0.54×), BBCA(0.54×), TOWR(0.54×), BMRI(0.55×), ANTM(0.56×), BSDE(0.56×), ISAT(0.56×), AMRT(0.57×), BBNI(0.58×), BBTN(0.58×), BIRD(0.58×), PWON(0.58×), MAPA(0.59×), BRIS(0.60×), CTRA(0.60×), KLBF(0.60×), MYOR(0.60×), SIDO(0.60×), TLKM(0.60×), CPIN(0.61×), ASII(0.61×), HEAL(0.62×), SILO(0.63×), MIKA(0.63×), MTEL(0.64×), PGAS(0.64×), NCKL(0.65×), AKRA(0.65×), AALI(0.67×), AMMN(0.67×), ASSA(0.67×), BRMS(0.67×), JPFA(0.67×), MTDL(0.67×), ICBP(0.69×), UNTR(0.69×), ERAA(0.71×), INDF(0.71×), AADI(0.73×), DMAS(0.75×), PTBA(0.77×), AUTO(0.79×), INCO(0.80×), DSNG(0.81×), LSIP(0.81×), INKP(0.83×), MEDC(0.83×), SMDR(0.83×)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas ?kode ?rasio WHERE { ?e ex:kodeSaham ?kode ; ex:rasioPERvsHistoris ?rasio ; a ?k . FILTER(?k IN (ex:Undervalued, ex:FairValued, ex:Overvalued)) FILTER NOT EXISTS { ?e a ex:EmitenUji }
 BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas ?rasio
```
</details>

### C03 — Emiten mana yang terlihat murah tapi sebenarnya jebakan (value trap)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `ValueTrap`. Bandingkan dengan `MurahKarenaLabaTurun` (revisi laba turun + undervalued).
- **Jawaban KB:** MurahKarenaLabaTurun: AADI, ACES, BBNI, BBRI, BMRI, BSDE, CTRA, DMAS, JPFA, MAPI, MYOR, PTBA, SMRA, UNVR · ValueTrap: BBTN, ERAA, INKP, SMRA

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis ?kode WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:ValueTrap, ex:MurahKarenaLabaTurun)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?kode
```
</details>

### C04 — Emiten mana yang rawan collapse / going concern, dan apa buktinya?  *(CQ6)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `RisikoGoingConcern`. SQWRL Q11: `RisikoGoingConcern(?e) ^ altmanZ(?e, ?z) ^ der(?e, ?d) -> sqwrl:select(?e, ?z, ?d) ^ sqwrl:orderBy(?z)`
- **Jawaban KB:** JSMR (Altman Z 0.9, DER 2.3); EXCL (Altman Z 1, DER 2.5); SMRA (Altman Z 1.4, DER 1); GOTO (Altman Z 1.6, DER 0.05); ASSA (Altman Z 1.6, DER 1.6)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?altmanZ ?der WHERE { ?e a ex:RisikoGoingConcern ; ex:kodeSaham ?kode ; ex:altmanZ ?altmanZ . OPTIONAL { ?e ex:der ?der } FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY ?altmanZ
```
</details>

### C05 — Zona Altman Z: siapa aman, abu-abu, distress?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `ZonaAman`, `ZonaAbuAbu`, `ZonaDistress`.
- **Jawaban KB:** ZonaAman (35): AKRA, DSNG, BUKA, CPIN, ITMG, ANTM, SIDO, NCKL, ERAA, DCII, INCO, TMAS, MIKA, HEAL, UNVR, PTBA, LSIP, MTDL, JPFA, KLBF, MAPA, SILO, AMRT, UNTR, BRMS, AADI, SMDR, MYOR, BIRD, IMPC, DMAS, ACES, MAPI, AUTO, AALI; ZonaDistress (6): EXCL, SMRA, JSMR, MDKA, ASSA, GOTO; ZonaAbuAbu (17): MEDC, ISAT, BSDE, TOWR, MTEL, EMTK, ASII, PWON, AMMN, CTRA, TLKM, SMGR, PGAS, INDF, ICBP, INKP, TINS

<details><summary>SPARQL</summary>

```sparql
SELECT ?zona (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:ZonaAman, ex:ZonaAbuAbu, ex:ZonaDistress)) FILTER NOT EXISTS { ?e a ex:EmitenUji }
 BIND(STRAFTER(STR(?k),"#") AS ?zona) } GROUP BY ?zona
```
</details>

### C06 — Emiten mana yang berisiko manipulasi laba (Beneish M-Score) atau kualitas labanya tinggi?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `RisikoManipulasiLaba`, `KualitasLabaTinggi`.
- **Jawaban KB:** KualitasLabaTinggi (47): DSNG, MEDC, ISAT, TOWR, CPIN, ITMG, EXCL, MTEL, ANTM, SIDO, NCKL, DCII, INCO, ASII, PWON, TMAS, MIKA, HEAL, UNVR, PTBA, LSIP, JSMR, MDKA, JPFA, KLBF, AMMN, MAPA, SILO, AMRT, TLKM, SMGR, UNTR, AADI, ASSA, PGAS, INDF, ICBP, SMDR, INKP, BIRD, IMPC, DMAS, ACES, MAPI, TINS, AUTO, AALI; RisikoManipulasiLaba (1): SMRA

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:RisikoManipulasiLaba, ex:KualitasLabaTinggi)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### C07 — Berapa nilai wajar dan potensi upside emiten top pick?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `ANTM` → *Property assertions*: `nilaiWajar`, `potensiUpsidePersen`, `hargaPenutupan`.
- **Jawaban KB:** TINS: harga 1900 → wajar 3562.5 (upside 87.5%); ANTM: harga 2900 → wajar 5220 (upside 80%); MIKA: harga 2100 → wajar 3325 (upside 58.3333%); NCKL: harga 780 → wajar 1200 (upside 53.8462%); JPFA: harga 1600 → wajar 2400 (upside 50%); AADI: harga 5400 → wajar 7425 (upside 37.5%); LSIP: harga 1050 → wajar 1292.31 (upside 23.0769%)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?harga ?nilaiWajar ?upside WHERE { ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode ; ex:hargaPenutupan ?harga ; ex:nilaiWajar ?nilaiWajar ; ex:potensiUpsidePersen ?upside } ORDER BY DESC(?upside)
```
</details>

### C08 — Emiten mana yang menjadi andalan dividen?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `DividenAndalan`.
- **Jawaban KB:** ITMG (DY 14%); AADI (DY 13%); PTBA (DY 12%); UNTR (DY 11%); BBRI (DY 11%); BBNI (DY 10.5%); ASII (DY 10%); BMRI (DY 10%); AUTO (DY 9%); PGAS (DY 9%); TLKM (DY 8%); TMAS (DY 7%); JPFA (DY 6%); BIRD (DY 6%); LSIP (DY 6%); ACES (DY 6%); ISAT (DY 6%); AKRA (DY 6%)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?dy ?dpr WHERE { ?e a ex:DividenAndalan ; ex:kodeSaham ?kode ; ex:dividendYield ?dy . OPTIONAL { ?e ex:dpr ?dpr } } ORDER BY DESC(?dy)
```
</details>

### C09 — Bank mana yang permodalannya lemah atau NPL-nya tinggi?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `EmitenPerbankan`, lalu `BankModalLemah`. Hasil kosong berarti semua bank lolos ambang (CAR ≥ batas).
- **Jawaban KB:** BBCA (NPL 1.9%, CAR 29%, NIM 5.3%, modal lemah: tidak); BBNI (NPL 2%, CAR 21%, NIM 4%, modal lemah: tidak); BBRI (NPL 3%, CAR 25%, NIM 7.4%, modal lemah: tidak); BBTN (NPL 3.4%, CAR 17%, NIM 3.3%, modal lemah: tidak); BMRI (NPL 0.98%, CAR 18.4%, NIM 4.9%, modal lemah: tidak); BRIS (NPL 1.9%, CAR 19%, NIM 5.6%, modal lemah: tidak)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?npl ?car ?nim ?lemah WHERE { ?e a ex:EmitenPerbankan ; ex:kodeSaham ?kode . OPTIONAL { ?e ex:npl ?npl } OPTIONAL { ?e ex:car ?car } OPTIONAL { ?e ex:nim ?nim }
 BIND(EXISTS { ?e a ex:BankModalLemah } AS ?lemah) } ORDER BY ?kode
```
</details>

## Teknikal

### D01 — Emiten mana yang sedang tren naik dan tren turun?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `TrenNaik` / `TrenTurun`.
- **Jawaban KB:** TrenTurun (36): AKRA, ISAT, BUKA, BSDE, TOWR, EXCL, MTEL, EMTK, ERAA, SMRA, ASII, PWON, UNVR, JSMR, AMMN, CTRA, MAPA, AMRT, TLKM, SMGR, BRIS, BBTN, BBCA, ASSA, PGAS, BMRI, ICBP, INKP, MYOR, BBNI, BIRD, BBRI, ACES, GOTO, MAPI, AUTO; TrenNaik (11): DSNG, MEDC, ANTM, DCII, LSIP, MDKA, JPFA, BRMS, IMPC, TINS, AALI

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:TrenNaik, ex:TrenTurun)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### D02 — Sinyal entry mana yang aktif, lengkap dengan stop loss & take profit (berbasis ATR)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q12: `SinyalEntry(?e) ^ hargaPenutupan(?e, ?h) ^ hargaStopLoss(?e, ?sl) ^ hargaTakeProfit(?e, ?tp) -> sqwrl:select(?e, ?h, ?sl, ?tp)`
- **Jawaban KB:** AADI 5400 (SL 5054.4, TP 5918.4); AALI 6000 (SL 5688, TP 6468); ANTM 2900 (SL 2697, TP 3204.5); DSNG 850 (SL 795.6, TP 931.6); IMPC 1900 (SL 1763.2, TP 2105.2); JPFA 1600 (SL 1491.2, TP 1763.2); LSIP 1050 (SL 987, TP 1144.5); MDKA 1900 (SL 1729, TP 2156.5); MEDC 1150 (SL 1062.6, TP 1281.1); TINS 1900 (SL 1748, TP 2128)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?harga ?stopLoss ?takeProfit WHERE { ?e a ex:SinyalEntry ; ex:kodeSaham ?kode ; ex:hargaPenutupan ?harga ; ex:hargaStopLoss ?stopLoss ; ex:hargaTakeProfit ?takeProfit FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY ?kode
```
</details>

### D03 — Sinyal buy-on-weakness, exit, dan hindari?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SinyalBuyOnWeakness`, `SinyalExit`, `SinyalHindari`.
- **Jawaban KB:** SinyalHindari: EXCL, SMRA, JSMR, ASSA, BBRI, GOTO; SinyalBuyOnWeakness: CPIN, ANTM, MIKA, LSIP, JPFA, UNTR, AADI, BBCA

<details><summary>SPARQL</summary>

```sparql
SELECT ?sinyal (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:SinyalBuyOnWeakness, ex:SinyalExit, ex:SinyalHindari)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?sinyal) } GROUP BY ?sinyal
```
</details>

### D04 — Pola chart apa yang terdeteksi dan mana yang terkonfirmasi indikator?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL: `KonfirmasiPolaBullish(?e) ^ terdeteksiPola(?e, ?p) -> sqwrl:select(?e, ?p)`
- **Jawaban KB:** Bearish: ACES-HeadAndShoulders, EMTK-BearFlag, GOTO-DescendingTriangle, JSMR-HeadAndShoulders, MAPI-DescendingTriangle, SMGR-BearishEngulfing, SMGR-HeadAndShoulders, SMRA-HeadAndShoulders, SMRA-ThreeBlackCrows, UNVR-HeadAndShoulders · Bullish: AADI-BullishEngulfing, AADI-DoubleBottom, AMMN-FallingWedge, AMMN-MorningStar, ANTM-BullFlag, ANTM-CupAndHandle, BBCA-BullishHarami, BBCA-Hammer, CPIN-BullishEngulfing, CPIN-InverseHeadAndShoulders, HEAL-InverseHeadAndShoulders, ISAT-FallingWedge, JPFA-AscendingTriangle, KLBF-DoubleBottom, LSIP-BullFlag, MDKA-AscendingTriangle, MEDC-BullFlag, MEDC-BullishMarubozu, MIKA-FallingWedge, TINS-AscendingTriangle, TLKM-BullishHarami, TLKM-DoubleBottom, UNTR-InverseHeadAndShoulders

<details><summary>SPARQL</summary>

```sparql
SELECT ?status ?kode ?pola WHERE { ?e ex:kodeSaham ?kode ; ex:terdeteksiPola ?pola ; a ?k . FILTER(?k IN (ex:KonfirmasiPolaBullish, ex:KonfirmasiPolaBearish)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"KonfirmasiPola") AS ?status) } ORDER BY ?status ?kode
```
</details>

### D05 — Overbought/oversold (RSI) dan lonjakan volume?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `Overbought`, `Oversold`, `LonjakanVolume`.
- **Jawaban KB:** LonjakanVolume: BRMS (RSI 72, vol 2.6×); LonjakanVolume: MDKA (RSI 68, vol 2.1×)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas ?kode ?rsi ?rasioVolume WHERE { ?e ex:kodeSaham ?kode ; ex:rsi14 ?rsi ; ex:rasioVolume ?rasioVolume ; a ?k . FILTER(?k IN (ex:Overbought, ex:Oversold, ex:LonjakanVolume)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas
```
</details>

### D06 — Emiten mana yang outperform / underperform IHSG (kekuatan relatif)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `OutperformPasar`. SQWRL Q29 untuk angka kekuatanRelatifPersen.
- **Jawaban KB:** OutperformPasar (9): BRMS(+15.5%), MDKA(+13.5%), MEDC(+10.5%), ANTM(+8.5%), LSIP(+6.5%), TINS(+6.5%), AALI(+5.5%), DSNG(+5.5%), JPFA(+5.5%) · UnderperformPasar (21): AMRT(-5.5%), ASSA(-5.5%), EMTK(-5.5%), MYOR(-5.5%), PWON(-5.5%), TOWR(-5.5%), AKRA(-6.5%), CTRA(-6.5%), TLKM(-6.5%), BBTN(-7.5%), BSDE(-7.5%), JSMR(-7.5%), MAPI(-7.5%), UNVR(-8.5%), ACES(-9.5%), BBCA(-9.5%), BBNI(-9.5%), BBRI(-10.5%), SMGR(-10.5%), BMRI(-11.5%), SMRA(-12.5%)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas ?kode ?kr WHERE { ?e ex:kodeSaham ?kode ; ex:kekuatanRelatifPersen ?kr ; a ?k . FILTER(?k IN (ex:OutperformPasar, ex:UnderperformPasar)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas DESC(?kr)
```
</details>

### D07 — Sinyal scalping (trader jangka sangat pendek)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SinyalScalpingLong`, `SinyalScalpingHindari`.
- **Jawaban KB:** SinyalScalpingHindari: UJI_GADAI; SinyalScalpingLong: BRMS; SinyalScalpingLong: MDKA

<details><summary>SPARQL</summary>

```sparql
SELECT ?sinyal ?kode WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:SinyalScalpingLong, ex:SinyalScalpingHindari)) BIND(STRAFTER(STR(?k),"#") AS ?sinyal) } ORDER BY ?sinyal
```
</details>

## Bandarmology

### E01 — Emiten mana yang sedang diakumulasi bandar, dan broker siapa akumulatornya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `AkumulasiBandar`. Individu emiten → `brokerAkumulatorUtama`.
- **Jawaban KB:** ANTM (KK, acc/dist 32); MDKA (KZ, acc/dist 30); MEDC (ZP, acc/dist 28); CPIN (KZ, acc/dist 26); TLKM (AZ, acc/dist 25); JPFA (BK, acc/dist 25); AADI (KZ, acc/dist 24); HEAL (BK, acc/dist 23); UNTR (AK, acc/dist 22); AMMN (CC, acc/dist 22); BBCA (LG, acc/dist 22); KLBF (LG, acc/dist 22); LSIP (RX, acc/dist 21); ISAT (CC, acc/dist 20); MIKA (KZ, acc/dist 20); ICBP (LG, acc/dist 20); TINS (YU, acc/dist 20)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?broker ?skorAccDist WHERE { ?e a ex:AkumulasiBandar ; ex:kodeSaham ?kode . OPTIONAL { ?e ex:brokerAkumulatorUtama ?broker } OPTIONAL { ?e ex:skorAccDistBroker ?skorAccDist } FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY DESC(?skorAccDist)
```
</details>

### E02 — Di mana smart money diam-diam akumulasi saat harga masih turun (divergensi)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `AkumulasiTersembunyi` (SQWRL Q13).
- **Jawaban KB:** AADI (harga 20h -7%, net asing 65 M); ANTM (harga 20h -3%, net asing 120 M); BBCA (harga 20h -21%, net asing -2500 M); CPIN (harga 20h -9%, net asing 30 M); HEAL (harga 20h -9%, net asing 8 M); JPFA (harga 20h -6%, net asing 25 M); LSIP (harga 20h -5%, net asing 12 M); MEDC (harga 20h -1%, net asing 85 M); MIKA (harga 20h -11%, net asing 10 M); TINS (harga 20h -5%, net asing 25 M); TLKM (harga 20h -18%, net asing -700 M); UNTR (harga 20h -10%, net asing 45 M)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?chg20 ?netAsing WHERE { ?e a ex:AkumulasiTersembunyi ; ex:kodeSaham ?kode ; ex:perubahanHarga20HariPersen ?chg20 ; ex:netAsing20HariM ?netAsing FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY ?kode
```
</details>

### E03 — Emiten mana yang sedang didistribusikan bandar ke ritel?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `DistribusiKeRitel`, `DistribusiBandar`.
- **Jawaban KB:** DistribusiKeRitel: EMTK, SMRA, UNVR, JSMR, SMGR, BBRI, ACES, GOTO, MAPI; DistribusiBandar: SMRA, SMGR, GOTO

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:DistribusiKeRitel, ex:DistribusiBandar)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### E04 — Asing sedang akumulasi atau distribusi di emiten mana?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `AsingAkumulasi` / `AsingDistribusi`.
- **Jawaban KB:** AsingDistribusi: ASII, AMMN, AMRT, TLKM, BBCA, BMRI, BBNI, BBRI; AsingAkumulasi: MEDC, ANTM, MDKA, BRMS, AADI

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:AsingAkumulasi, ex:AsingDistribusi)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### E05 — Fase Wyckoff tiap emiten (akumulasi, mark-up, distribusi, mark-down)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `FaseAkumulasiWyckoff`, `FaseMarkUpWyckoff`, `FaseDistribusiWyckoff`, `FaseMarkDownWyckoff`.
- **Jawaban KB:** FaseMarkUpWyckoff (10): DSNG, MEDC, ANTM, LSIP, MDKA, JPFA, BRMS, IMPC, TINS, AALI; FaseAkumulasiWyckoff (10): ISAT, CPIN, MIKA, HEAL, KLBF, AMMN, TLKM, UNTR, BBCA, ICBP; FaseMarkDownWyckoff (9): EMTK, SMRA, UNVR, JSMR, SMGR, BBRI, ACES, GOTO, MAPI

<details><summary>SPARQL</summary>

```sparql
SELECT ?fase (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:FaseAkumulasiWyckoff, ex:FaseMarkUpWyckoff, ex:FaseDistribusiWyckoff, ex:FaseMarkDownWyckoff)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?fase) } GROUP BY ?fase
```
</details>

### E06 — Konsep & alat bandarmology apa yang ada di KB?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KonsepBandarmology`, `PolaBandar`.
- **Jawaban KB:** KonsepBandarmology: AccDistBrokerScore, AvgPriceBandar, BidOfferImbalance, BrokerSummary, CrossingBlock, DoneDetail, ForeignInclusionFactor, IcebergOrder, NetForeignFlow, RunningTrade, TopBuyerSeller · PolaBandarBearish: PolaDistribusi, PolaMarkDown, PolaPumpAndDump, PolaUTAD · PolaBandarBullish: PolaAkumulasi, PolaHakaHaki, PolaMarkUp, PolaReAkumulasi, PolaShakeout, PolaSpring · PolaManipulatif: PolaPaintingTheTape, PolaPumpAndDump, PolaSpoofing, PolaWashTrade

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis ?k2 WHERE { ?k2 a ?k . FILTER(?k IN (ex:KonsepBandarmology, ex:PolaBandarBullish, ex:PolaBandarBearish, ex:PolaManipulatif)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?k2
```
</details>

### E07 — Broker apa saja dan bagaimana klasifikasinya (asing/lokal/ritel/institusi)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `Broker` dan subkelasnya.
- **Jawaban KB:** BrokerLokal: CC, DX, YP, XL, XC, LG, AZ, NI, PD; BrokerInstitusiLokal: AZ, DX, LG, NI, CC; BrokerAsing: RX, KZ, BK, AK, ZP, KK, YU; BrokerRitel: YP, XC, XL, PD

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis (GROUP_CONCAT(?bn; separator=", ") AS ?broker) WHERE { ?b a ?k . BIND(STRAFTER(STR(?b),"Broker_") AS ?bn) FILTER(?k IN (ex:BrokerAsing, ex:BrokerLokal, ex:BrokerRitel, ex:BrokerInstitusiLokal)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } GROUP BY ?jenis
```
</details>

### E08 — Apakah ada indikasi saham gorengan / pump and dump / jual paksa pengendali?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `IndikasiSahamGorengan`, `RisikoPumpAndDump`, `RisikoForcedSellPengendali`, `RisikoHSC`.
- **Jawaban KB:** IndikasiSahamGorengan: UJI_GORENG · RisikoForcedSellPengendali: UJI_GADAI · RisikoHSC: BRIS, DCII, NCKL, UJI_GORENG · RisikoPumpAndDump: UJI_GORENG · SinyalOrangDalam: UJI_INSIDER

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas ?e WHERE { ?e a ?k . FILTER(?k IN (ex:IndikasiSahamGorengan, ex:RisikoPumpAndDump, ex:RisikoForcedSellPengendali, ex:RisikoHSC, ex:SinyalOrangDalam)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas
```
</details>

## Sentimen

### F01 — Berapa berita yang dianalisis dan dari kategori apa?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `Berita` (lalu `BeritaMakroGeopolitik`, `BeritaEmiten`, `BeritaRisetAnalis`).
- **Jawaban KB:** total 71 berita · BeritaEmiten 8, BeritaMakroGeopolitik 54, BeritaRisetAnalis 9

<details><summary>SPARQL</summary>

```sparql
SELECT ?kategori (COUNT(?b) AS ?n) WHERE { ?b a ?k . FILTER(?k IN (ex:BeritaMakroGeopolitik, ex:BeritaEmiten, ex:BeritaRisetAnalis)) BIND(STRAFTER(STR(?k),"#") AS ?kategori) } GROUP BY ?kategori
```
</details>

### F02 — Bagaimana skor sentimen tiap sektor dari berita?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Sektor_*` → `skorSentimenSektor`, `poinSentimenSektor`.
- **Jawaban KB:** Energi -0.005 (poin 0); KonsumenPrimer -0.051 (poin 0); TransportasiLogistik -0.075 (poin 0); Perindustrian -0.085 (poin 0); Kesehatan -0.087 (poin 0); BarangBaku -0.094 (poin 0); KonsumenNonPrimer -0.100 (poin 0); Keuangan -0.124 (poin -1); Infrastruktur -0.185 (poin -1); PropertiRealEstat -0.222 (poin -1); Teknologi -0.243 (poin -1)

<details><summary>SPARQL</summary>

```sparql
SELECT ?sektor ?skor ?poin WHERE { ?s a ex:Sektor ; ex:skorSentimenSektor ?skor . OPTIONAL { ?s ex:poinSentimenSektor ?poin } BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } ORDER BY DESC(?skor)
```
</details>

### F03 — Emiten mana yang sentimennya positif / negatif?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SentimenPositif`, `SentimenNegatif`.
- **Jawaban KB:** SentimenNegatif: AKRA, MEDC, ITMG, INCO, ASII, JPFA, AMMN, BBCA, BMRI, BBRI, GOTO; SentimenPositif: ISAT, EXCL, LSIP, AADI, BBNI, TINS

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:SentimenPositif, ex:SentimenNegatif)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### F04 — Berita mana yang menjadi red flag untuk emiten?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q16: `memilikiRedFlag(?e, ?n) ^ judulBerita(?n, ?j) -> sqwrl:select(?e, ?j)`
- **Jawaban KB:** AKRA: "Minyak Brent Turun ke US$ 92,39 per Barel Kamis (12/11), Pasar Cermati Pasokan G"; AMMN: "Asing Net Sell Rp 20,7 Miliar Saat IHSG Turun Rabu (11/11), Cek Saham yang Dijua"; AMMN: "IHSG Ditutup Melemah 1,07% ke Level 5.247,8"; AMMN: "Semester I Kelam, IHSG Ambles 34,73% Disertai Kejatuhan Saham Big Caps dan Net S"; ANTM: "Asing Net Sell Rp 20,7 Miliar Saat IHSG Turun Rabu (11/11), Cek Saham yang Dijua"; ANTM: "Harga Emas Dunia Bangkit dari Level Terendah 14 Bulan, Cermati Suku Bunga The Fe"; ASII: "IHSG Ditutup Melemah 1,07% ke Level 5.247,8"; BBCA: "Aksi Jual Asing Tekan Saham Big Banks, Simak Rekomendasinya"; BBCA: "IHSG Ambruk, Asing Net Sell Jumbo di Saham Big Banks BBCA-BMRI"; BBCA: "Semester I Kelam, IHSG Ambles 34,73% Disertai Kejatuhan Saham Big Caps dan Net S"; BBRI: "Aksi Jual Asing Tekan Saham Big Banks, Simak Rekomendasinya"; BBRI: "IHSG Ditutup Melemah 1,07% ke Level 5.247,8"; BBRI: "Semester I Kelam, IHSG Ambles 34,73% Disertai Kejatuhan Saham Big Caps dan Net S"; BMRI: "Aksi Jual Asing Tekan Saham Big Banks, Simak Rekomendasinya"; BMRI: "IHSG Ambruk, Asing Net Sell Jumbo di Saham Big Banks BBCA-BMRI"; BMRI: "IHSG Ditutup Melemah 1,07% ke Level 5.247,8"; BMRI: "Semester I Kelam, IHSG Ambles 34,73% Disertai Kejatuhan Saham Big Caps dan Net S"; BRMS: "Harga Emas Dunia Bangkit dari Level Terendah 14 Bulan, Cermati Suku Bunga The Fe"; GOTO: "MSCI Depak GOTO, Manajemen Perseroan Tegaskan Hal Ini"; GOTO: "Tertahan di Level Rp50, MSCI Bakal Bekukan Saham GOTO"; INCO: "Asing Net Sell Rp 20,7 Miliar Saat IHSG Turun Rabu (11/11), Cek Saham yang Dijua"; ITMG: "Asing Net Sell Rp 20,7 Miliar Saat IHSG Turun Rabu (11/11), Cek Saham yang Dijua"; JPFA: "Asing Net Sell Rp 20,7 Miliar Saat IHSG Turun Rabu (11/11), Cek Saham yang Dijua"; JPFA: "Segmen DOC dan Livebird Topang Kinerja Japfa (JPFA) di Tengah Tekanan Beban Bung"; MDKA: "Harga Emas Dunia Bangkit dari Level Terendah 14 Bulan, Cermati Suku Bunga The Fe"; MEDC: "Minyak Brent Turun ke US$ 92,39 per Barel Kamis (12/11), Pasar Cermati Pasokan G"; TLKM: "Semester I Kelam, IHSG Ambles 34,73% Disertai Kejatuhan Saham Big Caps dan Net S"

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?judul WHERE { ?e ex:memilikiRedFlag ?n ; ex:kodeSaham ?kode . ?n ex:judulBerita ?judul } ORDER BY ?kode
```
</details>

### F05 — Emiten mana yang tahan berita buruk (harga tidak turun saat berita negatif)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SinyalKetahananBeritaBuruk`.
- **Jawaban KB:** (2) MEDC, JPFA

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode WHERE { ?e a ex:SinyalKetahananBeritaBuruk ; ex:kodeSaham ?kode }
```
</details>

### F06 — Komponen machine learning apa yang dipakai dan perannya (pendukung < 20%)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KomponenML`.
- **Jawaban KB:** ML_BacktestWeightCalibrator: Penyesuaian bobot ambang melalui walk-forward backtest; tetap di bawah kendali aturan pakar.; ML_PatternDetector: Modul pengenal pola dari data OHLCV; output terdeteksiPola (input ke SWRL).; ML_SentimentScorer: Skor leksikon finansial Indonesia + arah variabel makro × sensitivitas sektor (sentiment_scorer.py).; WalkForwardBacktest: Evaluasi rolling: kalibrasi di jendela t, uji di t+1, terhadap baseline IHSG/LQ45.

<details><summary>SPARQL</summary>

```sparql
SELECT ?m ?arti WHERE { ?m a ex:KomponenML . OPTIONAL { ?m rdfs:comment ?arti } } ORDER BY ?m
```
</details>

## Geopolitik & makro

### G01 — Peristiwa geopolitik/makro apa saja yang sedang aktif?  *(CQ9)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `PeristiwaAktif`.
- **Jawaban KB:** (31 peristiwa) GencatanDeeskalasi: GencatanRusiaUkraina_Okt2026 · KebijakanDomestik: HargaCPONaik_Okt2026, HilirisasiNikel, InvestasiDataCenter, MandatoriBiodiesel, PembelianDomestikBlueChip, PerpresOjol_2026, ProgramMBG, ReformasiFreeFloat_OJK, RencanaBEI_KeluarkanHSC, SnP_AfirmasiBBB, TekananFiskalSubsidi · KebijakanMoneter: BI_RDG_Okt2026, BI_TurunkanGWM, EkspektasiKenaikanBIRate, FOMC_Hawkish_2026, FedHike_Sep2026 · KeputusanOPEC: OPEC_PertahankanProduksi · KeputusanPenyediaIndeks: GOTO_DidepakMSCI, MSCI_Freeze_2026, MSCI_KonsultasiStandalone_Okt2026, MSCI_ReviewAgustus2026, SPDJI_FrontierFlag · KonflikPerang: EskalasiTimurTengah_Okt2026, PenutupanHormuz_2026 · KrisisEkonomi: CrashIHSG_16Okt2026, EmasRekor_2026, InflasiNaik_Sep2026, KrisisPasarModal_2026, RupiahTertekan_2026, TwinDeficit_2026 · PeristiwaGlobal: EmasRekor_2026, EskalasiTimurTengah_Okt2026, FOMC_Hawkish_2026, FedHike_Sep2026, GOTO_DidepakMSCI, GencatanRusiaUkraina_Okt2026, MSCI_Freeze_2026, MSCI_KonsultasiStandalone_Okt2026, MSCI_ReviewAgustus2026, OPEC_PertahankanProduksi, PenutupanHormuz_2026, SPDJI_FrontierFlag

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis ?ev WHERE { ?ev a ex:PeristiwaAktif ; a ?k . ?k rdfs:subClassOf ex:PeristiwaGeopolitik . BIND(STRAFTER(STR(?k),"#") AS ?jenis) } ORDER BY ?jenis ?ev
```
</details>

### G02 — Apa dampak kebijakan The Fed (FOMC hawkish / kenaikan FFR) ke pasar Indonesia?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Ev_FedHike_Sep2026` → `memicuPergerakan`; lalu ikuti `menyebabkan` dan `menguntungkanSektor`/`merugikanSektor`.
- **Jawaban KB:** FOMC_Hawkish_2026 → YieldUSNaik → DolarMenguat [−PropertiRealEstat]; FOMC_Hawkish_2026 → YieldUSNaik → DolarMenguat [−Teknologi]; FedHike_Sep2026 → YieldUSNaik → DolarMenguat [−PropertiRealEstat]; FedHike_Sep2026 → YieldUSNaik → DolarMenguat [−Teknologi]

<details><summary>SPARQL</summary>

```sparql
SELECT ?ev ?gerak ?lanjutan ?untung ?rugi WHERE { ?ev ex:memicuPergerakan ?gerak . FILTER(?ev IN (ex:Ev_FedHike_Sep2026, ex:Ev_FOMC_Hawkish_2026))
 OPTIONAL { ?gerak ex:menyebabkan ?lanjutan } OPTIONAL { ?gerak ex:menguntungkanSektor ?untung } OPTIONAL { ?gerak ex:merugikanSektor ?rugi } } ORDER BY ?ev ?gerak
```
</details>

### G03 — Bagaimana perang/ketegangan Timur Tengah (Hormuz) memengaruhi minyak dan sektor saham?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Ev_PenutupanHormuz_2026` dan `Ev_EskalasiTimurTengah_Okt2026` → `memicuPergerakan` → `menaikkanHargaKomoditas`, `menguntungkanSektor`.
- **Jawaban KB:** EskalasiTimurTengah_Okt2026 → GangguanPelayaran; EskalasiTimurTengah_Okt2026 → PremiRisikoTimurTengah; GencatanRusiaUkraina_Okt2026 → PasokanDieselMembaik [+TransportasiLogistik] [−Energi]; PenutupanHormuz_2026 → GangguanPelayaran; PenutupanHormuz_2026 → PremiRisikoTimurTengah

<details><summary>SPARQL</summary>

```sparql
SELECT ?ev ?gerak ?komoditas ?untung ?rugi WHERE { ?ev ex:memicuPergerakan ?gerak . FILTER(?ev IN (ex:Ev_PenutupanHormuz_2026, ex:Ev_EskalasiTimurTengah_Okt2026, ex:Ev_GencatanRusiaUkraina_Okt2026))
 OPTIONAL { ?gerak ex:menaikkanHargaKomoditas ?komoditas } OPTIONAL { ?gerak ex:menguntungkanSektor ?untung } OPTIONAL { ?gerak ex:merugikanSektor ?rugi } } ORDER BY ?ev
```
</details>

### G04 — Apa dampak inflasi dan krisis (rupiah, twin deficit, crash IHSG)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Ev_InflasiNaik_Sep2026`, `Ev_RupiahTertekan_2026`, `Ev_TwinDeficit_2026`, `Ev_CrashIHSG_16Okt2026` → `memicuPergerakan`.
- **Jawaban KB:** CrashIHSG_16Okt2026 → AliranAsingKeluarEM [−Keuangan]; CrashIHSG_16Okt2026 → DiskonValuasiBigCaps; InflasiNaik_Sep2026 → InflasiNaik; RupiahTertekan_2026 → RupiahMelemah; TwinDeficit_2026 → TekananFiskal

<details><summary>SPARQL</summary>

```sparql
SELECT ?ev ?gerak ?untung ?rugi WHERE { ?ev ex:memicuPergerakan ?gerak . FILTER(?ev IN (ex:Ev_InflasiNaik_Sep2026, ex:Ev_RupiahTertekan_2026, ex:Ev_TwinDeficit_2026, ex:Ev_CrashIHSG_16Okt2026))
 OPTIONAL { ?gerak ex:menguntungkanSektor ?untung } OPTIONAL { ?gerak ex:merugikanSektor ?rugi } } ORDER BY ?ev
```
</details>

### G05 — Tunjukkan rantai sebab-akibat multi-hop: peristiwa → gerakan 1 → gerakan 2 → sektor diuntungkan.

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q07: `PeristiwaAktif(?ev) ^ memicuPergerakan(?ev, ?m1) ^ menyebabkan(?m1, ?m2) ^ menguntungkanSektor(?m2, ?s) -> sqwrl:select(?ev, ?m1, ?m2, ?s)`
- **Jawaban KB:** (17 jalur) EskalasiTimurTengah_Okt2026 → PremiRisikoTimurTengah → SafeHavenEmas → BarangBaku; PenutupanHormuz_2026 → PremiRisikoTimurTengah → SafeHavenEmas → BarangBaku; RupiahTertekan_2026 → RupiahMelemah → PendapatanEksportirNaik → BarangBaku; EskalasiTimurTengah_Okt2026 → PremiRisikoTimurTengah → HargaMinyakNaik → Energi; PenutupanHormuz_2026 → PremiRisikoTimurTengah → HargaMinyakNaik → Energi; RupiahTertekan_2026 → RupiahMelemah → PendapatanEksportirNaik → Energi; InvestasiDataCenter → InvestasiDataCenter → PermintaanKonektivitas → Infrastruktur; ReformasiFreeFloat_OJK → ReformasiTransparansi → KepercayaanAsingPulih → Infrastruktur; EskalasiTimurTengah_Okt2026 → PremiRisikoTimurTengah → RiskOffGlobal → Kesehatan; PenutupanHormuz_2026 → PremiRisikoTimurTengah → RiskOffGlobal → Kesehatan; ReformasiFreeFloat_OJK → ReformasiTransparansi → KepercayaanAsingPulih → Keuangan; MandatoriBiodiesel → PermintaanBiodiesel → HargaCPONaik → KonsumenPrimer …

<details><summary>SPARQL</summary>

```sparql
SELECT ?ev ?hop1 ?hop2 ?sektor WHERE { ?ev a ex:PeristiwaAktif ; ex:memicuPergerakan ?hop1 . ?hop1 ex:menyebabkan ?hop2 . ?hop2 ex:menguntungkanSektor ?sektor } ORDER BY ?sektor
```
</details>

### G06 — Sektor mana yang diuntungkan dan dirugikan geopolitik saat ini?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SektorDiuntungkanGeopolitik`, `SektorDirugikanGeopolitik`.
- **Jawaban KB:** SektorDirugikanGeopolitik: Infrastruktur, Keuangan, PropertiRealEstat, Energi, KonsumenPrimer, Perindustrian, KonsumenNonPrimer, Kesehatan, Teknologi, TransportasiLogistik; SektorDiuntungkanGeopolitik: BarangBaku, Kesehatan, KonsumenPrimer, TransportasiLogistik, Energi

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (GROUP_CONCAT(?sek; separator=", ") AS ?sektor) WHERE { ?s a ?k . FILTER(?k IN (ex:SektorDiuntungkanGeopolitik, ex:SektorDirugikanGeopolitik)) BIND(STRAFTER(STR(?s),"Sektor_") AS ?sek) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### G07 — Berapa nilai indikator makro terkini (BI-Rate, Fed, kurs, Brent, emas, CDS, inflasi, SBN)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Pasar_ID_Okt2026` → *Property assertions*.
- **Jawaban KB:** biRate 6, ffr 4, kurs 18232, brent 91.95, emas 3745.56, cds 99.6, inflasi 3.23, sbn10y 7.668, drawdownIHSG -39.3

<details><summary>SPARQL</summary>

```sparql
SELECT ?biRate ?ffr ?kurs ?brent ?emas ?cds ?inflasi ?sbn10y ?drawdownIHSG WHERE { ?k a ex:KondisiPasarAktif ; ex:biRatePersen ?biRate ; ex:ffrAtasPersen ?ffr ; ex:kursUSDIDR ?kurs ; ex:brentUSD ?brent ;
 ex:emasUSD ?emas ; ex:cds5YBps ?cds ; ex:inflasiYoY ?inflasi ; ex:yieldSBN10Y ?sbn10y ; ex:drawdownIHSGPersen ?drawdownIHSG }
```
</details>

### G08 — Emiten mana yang diuntungkan / ditekan pergerakan komoditas & makro?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q08: `diuntungkanOleh(?e, ?m) -> sqwrl:select(?e, ?m) ^ sqwrl:orderBy(?e)`
- **Jawaban KB:** ditekan: ASSA(HargaMinyakNaik), BIRD(HargaMinyakNaik), BRIS(PenghapusanHSC), CPIN(BiayaImporNaik), DCII(PenghapusanHSC), ICBP(BiayaImporNaik), INDF(BiayaImporNaik), INKP(SubstitusiBatuBara), JPFA(BiayaImporNaik), KLBF(BiayaImporNaik), MEDC(HargaMinyakTurun), NCKL(PenghapusanHSC), SMGR(SubstitusiBatuBara), UNVR(HargaCPONaik) · diuntungkan: AADI(SubstitusiBatuBara), AALI(HargaCPONaik), AMMN(SafeHavenEmas), ANTM(HargaNikelTertopang), ANTM(SafeHavenEmas), ASII(HargaCPONaik), ASII(SafeHavenEmas), ASII(SubstitusiBatuBara), BRMS(SafeHavenEmas), DSNG(HargaCPONaik), ICBP(HargaCPONaik), INCO(HargaNikelTertopang), INDF(HargaCPONaik), ITMG(SubstitusiBatuBara), LSIP(HargaCPONaik), MDKA(HargaNikelTertopang), MDKA(SafeHavenEmas), MEDC(HargaMinyakNaik), NCKL(HargaNikelTertopang), PTBA(SubstitusiBatuBara), UNTR(HargaNikelTertopang), UNTR(SafeHavenEmas), UNTR(SubstitusiBatuBara)

<details><summary>SPARQL</summary>

```sparql
SELECT ?arah ?kode ?gerak WHERE { { ?e ex:diuntungkanOleh ?gerak BIND("diuntungkan" AS ?arah) } UNION { ?e ex:ditekanOleh ?gerak BIND("ditekan" AS ?arah) } ?e ex:kodeSaham ?kode FILTER NOT EXISTS { ?e a ex:EmitenUji } } ORDER BY ?arah ?kode
```
</details>

### G09 — Indikator makro apa saja yang dipantau dan nilainya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `IndikatorMakro`.
- **Jawaban KB:** BIRate 6 %; Brent 91.95 US$/barel; CDS5Y 99.6 bps; CorePCE_US 3 %; DepositFacility 5.25 %; Emas 3745.56 US$/troy ons; EstimasiOutflowPasif 4.5 US$ miliar (titik tengah 3-6); FedFundsRate 4 %; IHSG 5247.88 poin; IHSG_16Okt 5185.11 poin; IHSG_30Sep 6095.86 poin; IHSG_Akhir2025 8646 poin; InflasiID 3.23 %; NetAsingYTD -97.62 Rp triliun; NetSellAsingH1 -73.6 Rp triliun; ProyeksiBrentEIA 105 US$/barel; ProyeksiBrentGS 90 US$/barel; RatingSP 0 BBB/A-2 stabil; SpreadSBN_UST 281 bps; USDIDR 18232 Rp; UST10Y 4.894 %; WTI 86.01 US$/barel; YieldSBN10Y 7.668 %

<details><summary>SPARQL</summary>

```sparql
SELECT ?i ?nilai ?satuan WHERE { ?i a ex:IndikatorMakro ; ex:nilaiIndikator ?nilai . OPTIONAL { ?i ex:satuan ?satuan } } ORDER BY ?i
```
</details>

## Indeks

### H01 — Indeks apa saja yang tercakup (MSCI, LQ45, NASDAQ, FTSE, dll.)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `IndeksSaham` dan subkelasnya (`IndeksMSCI`, `IndeksAmerika`, `IndeksDomestik`, ...).
- **Jawaban KB:** IndeksAmerika (6): NASDAQ_Composite, Russell2000, DowJones, PHLX_Semiconductor, SP500, NASDAQ100; IndeksAsiaPasifik (13): ShanghaiComposite, Sensex, HangSeng, TOPIX, PSEi, KOSPI, STI, Nikkei225, ASX200, FBMKLCI, CSI300, Nifty50, SET; IndeksESG (2): IDXESGL, SRIKEHATI; IndeksEropa (4): FTSE100, CAC40, EuroStoxx50, DAX40; IndeksFTSERussell (3): FTSE_Indonesia, FTSE_ASEAN40, FTSE_AllWorld; IndeksKomposit (1): IHSG; IndeksLikuiditas (4): IDX30, LQ45, Kompas100, IDX80; IndeksMSCI (10): MSCI_FrontierMarkets, MSCI_EM_Asia, MSCI_ASEAN, MSCI_EmergingMarkets, MSCI_AC_AsiaExJapan, MSCI_Indonesia, MSCI_ACWI, MSCI_Indonesia_IMI, MSCI_World, MSCI_Indonesia_SmallCap; IndeksSPDowJones (1): SP_Indonesia_BMI; IndeksSektoralBEI (11): IDXNONCYC, IDXINFRA, IDXENERGY, IDXCYCLIC, IDXFINANCE, IDXINDUST, IDXPROPERT, IDXTRANS, IDXBASIC, IDXHEALTH, IDXTECHNO; IndeksSyariah (3): ISSI, JII, JII70; IndeksTematik (6): IDXQ30, IDXV30, IDXBUMN20, IDXG30, IDXHIDIV20, IDXLQ45LCL; IndikatorRisikoGlobal (2): VIX, DXY

<details><summary>SPARQL</summary>

```sparql
SELECT ?kategori (COUNT(?i) AS ?n) (GROUP_CONCAT(?id; separator=", ") AS ?indeks) WHERE { ?i a ?k . ?k rdfs:subClassOf+ ex:IndeksSaham .
 FILTER NOT EXISTS { ?k2 rdfs:subClassOf ?k . ?i a ?k2 . FILTER(?k2 != ?k) } BIND(STRAFTER(STR(?i),"#") AS ?id) BIND(STRAFTER(STR(?k),"#") AS ?kategori) } GROUP BY ?kategori ORDER BY ?kategori
```
</details>

### H02 — Emiten mana saja anggota LQ45?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `Emiten and (anggotaIndeks value LQ45)`.
- **Jawaban KB:** (45) AADI, ACES, AKRA, AMMN, AMRT, ANTM, ASII, BBCA, BBNI, BBRI, BBTN, BMRI, BRIS, BRMS, BSDE, CPIN, CTRA, EXCL, HEAL, ICBP, INCO, INDF, INKP, ISAT, ITMG, JPFA, JSMR, KLBF, MAPI, MDKA, MEDC, MIKA, MTEL, MYOR, NCKL, PGAS, PTBA, PWON, SIDO, SMGR, TINS, TLKM, TOWR, UNTR, UNVR

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode WHERE { ?e ex:anggotaIndeks ex:LQ45 ; ex:kodeSaham ?kode } ORDER BY ?kode
```
</details>

### H03 — Emiten mana anggota MSCI Indonesia dan mana yang berisiko outflow dana pasif (MSCI freeze/standalone)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `Emiten and (anggotaIndeks value MSCI_Indonesia)` lalu `RisikoOutflowPasif` (SQWRL Q15).
- **Jawaban KB:** (16) BBCA⚠, BBRI⚠, AMMN⚠, BMRI⚠, TLKM⚠, ASII⚠, BBNI⚠, ICBP⚠, AMRT⚠, UNTR⚠, ANTM⚠, INDF⚠, KLBF⚠, ISAT⚠, MDKA⚠, AADI⚠  (⚠ = RisikoOutflowPasif)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?mcap ?outflow WHERE { ?e ex:anggotaIndeks ex:MSCI_Indonesia ; ex:kodeSaham ?kode ; ex:kapitalisasiPasarT ?mcap . BIND(EXISTS { ?e a ex:RisikoOutflowPasif } AS ?outflow) } ORDER BY DESC(?mcap)
```
</details>

### H04 — Indeks syariah dan emiten syariah?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `IndeksSyariah`, `EmitenSyariah`.
- **Jawaban KB:** EmitenSyariah: 58; IndeksSyariah: 3

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis (COUNT(?x) AS ?n) WHERE { { ?x a ex:IndeksSyariah BIND("IndeksSyariah" AS ?jenis) } UNION { ?x a ex:EmitenSyariah BIND("EmitenSyariah" AS ?jenis) } } GROUP BY ?jenis
```
</details>

### H05 — Keputusan penyedia indeks apa yang memengaruhi pasar (MSCI review, freeze, FTSE, S&P)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KeputusanPenyediaIndeks`.
- **Jawaban KB:** GOTO Dikeluarkan/Dibekukan MSCI (Mei 2026); MSCI Freeze FIF Indonesia (Feb-Nov 2026); MSCI Konsultasi Reklasifikasi Indonesia ke Standalone (15 Okt 2026); MSCI Review Agustus 2026 (GOTO & CPIN keluar Standard); S&P DJI Tandai Potensi Reklasifikasi ke Frontier (Jul 2026)

<details><summary>SPARQL</summary>

```sparql
SELECT ?ev ?label WHERE { ?ev a ex:KeputusanPenyediaIndeks ; rdfs:label ?label } ORDER BY ?ev
```
</details>

## Prediksi sektor

### I01 — Sektor apa yang diprediksi naik dalam 1–3 tahun ke depan?  *(CQ1)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SektorBullish` (dan `SektorBullishKuat`, `SektorBullishModerat`). SQWRL Q01/Q02.
- **Jawaban KB:** NAIK: BarangBaku (BullishModerat, skor 11), Kesehatan (BullishModerat, skor 8) · lainnya: Energi Netral (6), Infrastruktur Netral (6), KonsumenPrimer Netral (6), Perindustrian Netral (4), Keuangan Bearish (0), PropertiRealEstat Bearish (-2), Teknologi Bearish (-4), TransportasiLogistik Bearish (-4), KonsumenNonPrimer Bearish (-6)

<details><summary>SPARQL</summary>

```sparql
SELECT ?sektor ?prediksi ?skorAktif WHERE { ?s a ex:Sektor ; ex:skorOutlookAktif ?skorAktif ; a ?k . FILTER(?k IN (ex:SektorBullishKuat, ex:SektorBullishModerat, ex:SektorNetral, ex:SektorBearish))
 BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) BIND(STRAFTER(STR(?k),"Sektor") AS ?prediksi) } ORDER BY DESC(?skorAktif)
```
</details>

### I02 — Berapa skor sektor di tiap skenario (base, bull, bear) dan ekspektasi probabilistiknya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q23 / Q09. Atau individu `Penilaian_<Sektor>_<Skenario>` → `skorOutlook`.
- **Jawaban KB:** BarangBaku B11/U17/D4 → E=10.75; Infrastruktur B6/U20/D-1 → E=7.75; Kesehatan B8/U8/D6 → E=7.5; KonsumenPrimer B6/U12/D1 → E=6.25; Perindustrian B4/U14/D-1 → E=5.25; Energi B6/U2/D4 → E=4.5; Keuangan B0/U19/D-10 → E=2.25; PropertiRealEstat B-2/U14/D-9 → E=0.25; Teknologi B-4/U16/D-13 → E=-1.25; TransportasiLogistik B-4/U11/D-12 → E=-2.25; KonsumenNonPrimer B-6/U13/D-16 → E=-3.75

<details><summary>SPARQL</summary>

```sparql
SELECT ?sektor ?base ?bull ?bear ?ekspektasi WHERE { ?s a ex:Sektor ; ex:skorOutlookBase ?base ; ex:skorOutlookBull ?bull ; ex:skorOutlookBear ?bear ; ex:skorEkspektasiProbabilistik ?ekspektasi
 BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } ORDER BY DESC(?ekspektasi)
```
</details>

### I03 — Sektor mana yang tahan di semua skenario (inti), satelit, dan peluang kontrarian?  *(CQ2)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SektorPilihanInti`, `SektorPilihanSatelit`, `SektorPeluangKontrarian`, `SektorRobustLintasSkenario`.
- **Jawaban KB:** SektorAsimetriPositif: Keuangan, Perindustrian, Infrastruktur; SektorRobustLintasSkenario: BarangBaku, Kesehatan; SektorPilihanInti: Kesehatan, BarangBaku; SektorPeluangKontrarian: Infrastruktur, KonsumenPrimer, Keuangan; SektorPilihanSatelit: Infrastruktur, Keuangan

<details><summary>SPARQL</summary>

```sparql
SELECT ?peran (GROUP_CONCAT(?sek; separator=", ") AS ?sektor) WHERE { ?s a ?k . FILTER(?k IN (ex:SektorPilihanInti, ex:SektorPilihanSatelit, ex:SektorPeluangKontrarian, ex:SektorRobustLintasSkenario, ex:SektorAsimetriPositif))
 BIND(STRAFTER(STR(?s),"Sektor_") AS ?sek) BIND(STRAFTER(STR(?k),"#") AS ?peran) } GROUP BY ?peran
```
</details>

### I04 — MENGAPA sektor terpilih diprediksi naik (jejak penjelasan tailwind/headwind/preseden)?  *(CQ4)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Sektor_BarangBaku` → `memilikiTailwind`, `memilikiHeadwind`, `memilikiPreseden`. Klik **?** di sebelah aksioma kuning untuk *explanation* aturan.
- **Jawaban KB:** BarangBaku: preseden Supercycle_2022; tailwind HargaNikelTertopang, PendapatanEksportirNaik, SafeHavenEmas; tema EmasSafeHaven, HilirisasiMineral · Kesehatan: headwind BiayaImporNaik; tailwind RiskOffGlobal; tema PopulasiKesehatan

<details><summary>SPARQL</summary>

```sparql
SELECT ?sektor ?jenis ?faktor WHERE { ?s a ex:SektorBullish . { ?s ex:memilikiTailwind ?faktor BIND("tailwind" AS ?jenis) } UNION { ?s ex:memilikiHeadwind ?faktor BIND("headwind" AS ?jenis) }
 UNION { ?s ex:memilikiPreseden ?faktor BIND("preseden" AS ?jenis) } UNION { ?s ex:didukungTema ?faktor BIND("tema" AS ?jenis) } BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } ORDER BY ?sektor ?jenis
```
</details>

### I05 — Periode sejarah mana yang paling mirip dengan kondisi sekarang (case-based reasoning)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q10: `PeriodeHistoris(?p) ^ skorKemiripan(?p, ?k) -> sqwrl:select(?p, ?k) ^ sqwrl:orderByDescending(?k)`; DL Query `PeriodeAnalog`.
- **Jawaban KB:** Supercycle_2022 17/20 ✔analog (≥13); FedHike_PerangDagang_2018 15/20 ✔analog (≥13); TaperTantrum_2013 10/20; SVB_PuncakBunga_2023 9/20; Krisis1998 8/20; DevaluasiYuan_2015 5/20; TarifAS_2025 2/20; GFC_2008 0/20; COVID_2020 -2/20

<details><summary>SPARQL</summary>

```sparql
SELECT ?periode ?kemiripan ?analog WHERE { ?p a ex:PeriodeHistoris ; ex:skorKemiripan ?kemiripan . BIND(EXISTS { ?p a ex:PeriodeAnalog } AS ?analog) BIND(STRAFTER(STR(?p),"Kasus_") AS ?periode) } ORDER BY DESC(?kemiripan)
```
</details>

### I06 — Tema struktural jangka panjang apa yang mendukung sektor?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `TemaStruktural`; `SektorDidukungTema`.
- **Jawaban KB:** Tema_EmasSafeHaven (3) → BarangBaku; Tema_HilirisasiMineral (3) → BarangBaku, Perindustrian; Tema_DataCenterAI (2) → Infrastruktur, Teknologi; Tema_PopulasiKesehatan (2) → Kesehatan; Tema_InklusiKeuangan (2) → Keuangan; Tema_ReformasiPasarModal (2) → Keuangan; Tema_Biodiesel (2) → KonsumenPrimer; Tema_MakanBergiziGratis (2) → KonsumenPrimer; Tema_KetahananEnergi (1) → Energi; Tema_KonsolidasiTelko (1) → Infrastruktur; Tema_DigitalisasiKonsumen (1) → KonsumenNonPrimer, Teknologi; Tema_TigaJutaRumah (1) → PropertiRealEstat; Tema_Danantara (0) → Keuangan; Tema_TransisiEnergi (-1) → Energi

<details><summary>SPARQL</summary>

```sparql
SELECT ?tema ?kekuatan ?sektor WHERE { ?t a ex:TemaStruktural . OPTIONAL { ?t ex:skorKekuatanTema ?kekuatan } OPTIONAL { ?s ex:didukungTema ?t BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } BIND(STRAFTER(STR(?t),"#") AS ?tema) } ORDER BY DESC(?kekuatan)
```
</details>

### I07 — Fase siklus ekonomi apa yang berlaku dan sektor mana yang favorit di fase itu (rotasi sektor)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Skenario_Base_2027_2028` → `faseSiklus`; DL Query `SektorFavoritSiklus`.
- **Jawaban KB:** skenario aktif Base_2027_2028, fase Fase_LateCycle → sektor favorit: Energi, BarangBaku

<details><summary>SPARQL</summary>

```sparql
SELECT ?skenario ?fase ?favorit WHERE { ?sc a ex:SkenarioAktif ; ex:faseSiklus ?fase . OPTIONAL { ?s a ex:SektorFavoritSiklus BIND(STRAFTER(STR(?s),"Sektor_") AS ?favorit) } BIND(STRAFTER(STR(?sc),"Skenario_") AS ?skenario) }
```
</details>

### I08 — Sektor mana yang murah secara historis, defensif, siklikal?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SektorMurahHistoris`, `SektorDefensif`, `SektorSiklikal`.
- **Jawaban KB:** SektorKomoditas: Energi, BarangBaku; SektorSiklikal: Keuangan, Teknologi, PropertiRealEstat, TransportasiLogistik, KonsumenNonPrimer, Perindustrian; SektorDefensif: Kesehatan, Infrastruktur, KonsumenPrimer; SektorMurahHistoris: Energi, KonsumenPrimer, Infrastruktur, Perindustrian, KonsumenNonPrimer, Keuangan, PropertiRealEstat, Kesehatan, TransportasiLogistik, BarangBaku

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (GROUP_CONCAT(?sek; separator=", ") AS ?sektor) WHERE { ?s a ?k . FILTER(?k IN (ex:SektorMurahHistoris, ex:SektorDefensif, ex:SektorSiklikal, ex:SektorKomoditas)) BIND(STRAFTER(STR(?s),"Sektor_") AS ?sek) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

## Rekomendasi emiten

### J01 — Top-3 emiten per sektor pilihan (inti & satelit)?  *(CQ3)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q03 (ganti nama sektor): `termasukSektor(?e, Sektor_BarangBaku) ^ skorAdaptifRegime(?e, ?t) -> sqwrl:select(?e, ?t) ^ sqwrl:orderByDescending(?t) ^ sqwrl:limit(3)`
- **Jawaban KB:** BarangBaku: ANTM (35), TINS (33), NCKL (26.5) · Infrastruktur: ISAT (23.5), TLKM (18), MTEL (17), TOWR (17) · Kesehatan: MIKA (26), KLBF (23), SIDO (23), SILO (23) · Keuangan: BBCA (23.5), BRIS (22), BMRI (20.5)

<details><summary>SPARQL</summary>

```sparql
SELECT ?sektor ?kode ?skorAdaptif WHERE { ?s ex:kodeIndeksSektor ?kd . { ?s a ex:SektorPilihanInti } UNION { ?s a ex:SektorPilihanSatelit }
 ?e ex:termasukSektor ?s ; ex:kodeSaham ?kode ; ex:skorAdaptifRegime ?skorAdaptif . FILTER NOT EXISTS { ?e a ex:EmitenUji }
 { SELECT ?e (COUNT(?o) AS ?lebih) WHERE { ?e ex:termasukSektor ?s2 ; ex:skorAdaptifRegime ?sk . OPTIONAL { ?o ex:termasukSektor ?s2 ; ex:skorAdaptifRegime ?so . FILTER(?so > ?sk) FILTER NOT EXISTS { ?o a ex:EmitenUji } } } GROUP BY ?e }
 FILTER(?lebih < 3) BIND(STRAFTER(STR(?s),"Sektor_") AS ?sektor) } ORDER BY ?sektor DESC(?skorAdaptif)
```
</details>

### J02 — Apa beda pilihan analis biasa (skor statis) dan sistem pakar (skor adaptif regime)?  *(CQ8)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KandidatTopPick` vs `KandidatTopPickAdaptif`. SQWRL Q21.
- **Jawaban KB:** Analis biasa: ANTM, TINS, NCKL, MIKA · Pakar: ANTM, TINS, LSIP, AADI, JPFA, NCKL, MIKA · Dibuang pakar: - · Ditambah pakar: LSIP, AADI, JPFA

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?skorStatis ?skorAdaptif ?analisBiasa ?pakar WHERE { ?e ex:kodeSaham ?kode ; ex:skorTotalEmiten ?skorStatis ; ex:skorAdaptifRegime ?skorAdaptif .
 BIND(EXISTS { ?e a ex:KandidatTopPick } AS ?analisBiasa) BIND(EXISTS { ?e a ex:KandidatTopPickAdaptif } AS ?pakar) FILTER(?analisBiasa || ?pakar) } ORDER BY DESC(?skorAdaptif)
```
</details>

### J03 — Mengapa BRMS tidak masuk top pick pakar padahal grafiknya paling kuat (outperform tertinggi)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `BRMS` → bandingkan `skorTotalEmiten` vs `skorAdaptifRegime`, `pertumbuhanEPS`, kelas `RevisiLabaTurun`/`MomentumTanpaFundamental`.
- **Jawaban KB:** skor statis 20 vs adaptif 22; EPS growth -36.9%; kelas: MomentumTanpaFundamental, TungguKonfirmasi, FundamentalLemah

<details><summary>SPARQL</summary>

```sparql
SELECT ?skorStatis ?skorAdaptif ?epsGrowth ?kelas WHERE { ex:BRMS ex:skorTotalEmiten ?skorStatis ; ex:skorAdaptifRegime ?skorAdaptif ; ex:pertumbuhanEPS ?epsGrowth ; a ?k .
 FILTER(?k IN (ex:MomentumTanpaFundamental, ex:RevisiLabaTurun, ex:FundamentalLemah, ex:FundamentalSedang, ex:Overvalued, ex:KonfluensiRendah, ex:TungguKonfirmasi, ex:KandidatTopPick)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) }
```
</details>

### J04 — Rincian skor multi-pilar emiten top pick (fundamental, valuasi, teknikal, bandar, sentimen, sektor, risiko, likuiditas)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q05 (ganti ANTM).
- **Jawaban KB:** ANTM: F9 V3 T7 B5 S-1 Sek2 R0 L2 = 27 (adaptif 35); TINS: F9 V3 T7 B3 S2 Sek2 R-1 L2 = 27 (adaptif 33); LSIP: F9 V2 T7 B3 S1 Sek0 R0 L1 = 23 (adaptif 29.5); AADI: F10 V2 T5 B4 S2 Sek0 R0 L2 = 25 (adaptif 29); JPFA: F8 V2 T7 B3 S-2 Sek0 R0 L1 = 19 (adaptif 26.5); NCKL: F9 V2 T4 B3 S0 Sek2 R0 L1 = 21 (adaptif 26.5); MIKA: F9 V2 T4 B3 S0 Sek2 R0 L1 = 21 (adaptif 26)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?fund ?val ?tek ?band ?sent ?sek ?risiko ?likuid ?total ?adaptif WHERE { ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode ; ex:skorFundamental ?fund ; ex:skorValuasi ?val ; ex:skorTeknikal ?tek ;
 ex:skorBandar ?band ; ex:skorSentimen ?sent ; ex:skorKontribusiSektor ?sek ; ex:penaltiRisiko ?risiko ; ex:poinLikuiditas ?likuid ; ex:skorTotalEmiten ?total ; ex:skorAdaptifRegime ?adaptif } ORDER BY DESC(?adaptif)
```
</details>

### J05 — Emiten dengan keyakinan tinggi dan watchlist?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KeyakinanTinggi`, `KandidatWatchlist`.
- **Jawaban KB:** KeyakinanTinggi: ANTM, MIKA, TINS; KandidatWatchlist: SIDO, HEAL, KLBF, AMMN, SILO, BRMS

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:KeyakinanTinggi, ex:KandidatWatchlist)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### J06 — Berapa ukuran posisi maksimal per emiten top pick (manajemen risiko)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q20: `KandidatTopPickAdaptif(?e) ^ skorAdaptifRegime(?e, ?s) ^ ukuranPosisiMaksPersen(?e, ?p) -> sqwrl:select(?e, ?s, ?p)`
- **Jawaban KB:** MIKA maks 10.0% portofolio (ATR 2.5%); LSIP maks 8.3% portofolio (ATR 3%); AADI maks 7.8% portofolio (ATR 3.2%); JPFA maks 7.4% portofolio (ATR 3.4%); NCKL maks 7.4% portofolio (ATR 3.4%); ANTM maks 7.1% portofolio (ATR 3.5%); TINS maks 6.2% portofolio (ATR 4%)

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?posisiMaks ?atr WHERE { ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode ; ex:ukuranPosisiMaksPersen ?posisiMaks ; ex:atrPersen ?atr } ORDER BY DESC(?posisiMaks)
```
</details>

### J07 — Apakah ada risiko konsentrasi (dua top pick dengan tema/komoditas sama)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `RisikoKonsentrasiTema`; individu → `terkonsentrasiDengan`.
- **Jawaban KB:** ANTM ↔ NCKL

<details><summary>SPARQL</summary>

```sparql
SELECT ?a ?b WHERE { ?x ex:terkonsentrasiDengan ?y ; ex:kodeSaham ?a . ?y ex:kodeSaham ?b . FILTER(STR(?a) < STR(?b)) }
```
</details>

## Meta-penalaran

### K01 — Regime pasar apa yang sedang terjadi dan berapa skor stresnya?  *(CQ5)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `RegimeAktif`. SQWRL Q18.
- **Jawaban KB:** Krisis Likuiditas / Kapitulasi (stres 11/12; CDS 99.6 bps, drawdown IHSG -39.3%, breadth 18.75%)

<details><summary>SPARQL</summary>

```sparql
SELECT ?regime ?label ?stres ?cds ?drawdown ?breadth WHERE { ?k a ex:KondisiPasarAktif ; ex:regimeTerdeteksi ?r ; ex:skorStresPasar ?stres ; ex:cds5YBps ?cds ; ex:drawdownIHSGPersen ?drawdown ; ex:breadthPersenDiAtasMA200 ?breadth .
 ?r rdfs:label ?label BIND(STRAFTER(STR(?r),"Regime_") AS ?regime) }
```
</details>

### K02 — Bagaimana bobot pilar berubah menurut regime (adaptif)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q19; atau individu `Regime_*` → bobot*.
- **Jawaban KB:** KrisisLikuiditas (AKTIF): F×1.5 T×0.5 B×1 SM×1.5, risiko/trx 0.5%, ambang 24.7; Netral: F×1 T×1 B×1 SM×1, risiko/trx 1%, ambang 22.75; RiskOn: F×0.8 T×1.3 B×1.2 SM×1, risiko/trx 1%, ambang 23.14; RiskOff: F×1.2 T×0.8 B×1.2 SM×1.2, risiko/trx 0.75%, ambang 23.79

<details><summary>SPARQL</summary>

```sparql
SELECT ?regime ?aktif ?fund ?tek ?bandar ?smart ?risikoTrx ?ambang WHERE { ?r a ex:RegimePasar ; ex:bobotFundamental ?fund ; ex:bobotTeknikal ?tek ; ex:bobotBandar ?bandar ; ex:bobotSmartMoney ?smart ;
 ex:risikoPerTransaksiPersen ?risikoTrx ; ex:ambangTopPickAdaptif ?ambang . BIND(EXISTS { ?r a ex:RegimeAktif } AS ?aktif) BIND(STRAFTER(STR(?r),"Regime_") AS ?regime) } ORDER BY DESC(?aktif)
```
</details>

### K03 — Reaksi kebijakan apa yang diantisipasi (reaction function BI/pemerintah)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `AntisipasiTerpicu`. SQWRL Q25.
- **Jawaban KB:** StabilisasiPasar (Stabilisasi Pasar oleh Otoritas & Institusi Domestik) → DukunganLikuiditasDomestik; PremiRisikoNegara (Kenaikan Premi Risiko Negara) → PremiRisikoNegaraNaik; BIHikePreemptif (BI Naikkan Suku Bunga Pre-emptif) → SukuBungaBINaik

<details><summary>SPARQL</summary>

```sparql
SELECT ?antisipasi ?label ?mengaktifkan WHERE { ?a a ex:AntisipasiTerpicu ; rdfs:label ?label . OPTIONAL { ?a ex:antisipasiMengaktifkan ?mengaktifkan } BIND(STRAFTER(STR(?a),"Antisipasi_") AS ?antisipasi) }
```
</details>

### K04 — Tesis investasi mana yang valid, rapuh, atau gugur (kill switch)?  *(CQ10)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `TesisValid`, `TesisRapuh`, `TesisGugur`, `TesisPerluDataBaru`. SQWRL Q26.
- **Jawaban KB:** BarangBaku_EmasNikel: Gugur/Rapuh; Energi_PremiGeopolitik: Valid; Infrastruktur_DataCenter: PerluDataBaru/Rapuh/Valid; Kesehatan_Defensif: Rapuh/Valid; Keuangan_Kontrarian: Valid; KonsumenPrimer_MBG: Valid

<details><summary>SPARQL</summary>

```sparql
SELECT ?tesis ?status WHERE { ?t a ex:TesisInvestasi ; a ?k . FILTER(?k IN (ex:TesisValid, ex:TesisRapuh, ex:TesisGugur, ex:TesisTerpicu, ex:TesisPerluDataBaru)) BIND(STRAFTER(STR(?t),"Tesis_") AS ?tesis) BIND(STRAFTER(STR(?k),"Tesis") AS ?status) } ORDER BY ?tesis
```
</details>

### K05 — Indikator kunci & ambang kill switch tiap tesis?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Tesis_*` → `indikatorKunciTesis`, `ambangInvalidasiBawah/Atas`, `ambangPemicuBawah`.
- **Jawaban KB:** BarangBaku_EmasNikel: Emas = 3745.56 → gugur bila < 3800; Energi_PremiGeopolitik: Brent = 91.95 → gugur bila < 75; Infrastruktur_DataCenter: YieldSBN10Y = 7.668 → gugur bila > 8; Kesehatan_Defensif: USDIDR = 18232 → gugur bila > 19500; Keuangan_Kontrarian: CDS5Y = 99.6 → gugur bila > 150; KonsumenPrimer_MBG: InflasiID = 3.23 → gugur bila > 5

<details><summary>SPARQL</summary>

```sparql
SELECT ?tesis ?indikator ?nilai ?invalidBawah ?invalidAtas WHERE { ?t a ex:TesisInvestasi ; ex:indikatorKunciTesis ?i . ?i ex:nilaiIndikator ?nilai .
 OPTIONAL { ?t ex:ambangInvalidasiBawah ?invalidBawah } OPTIONAL { ?t ex:ambangInvalidasiAtas ?invalidAtas } BIND(STRAFTER(STR(?t),"Tesis_") AS ?tesis) BIND(STRAFTER(STR(?i),"#") AS ?indikator) } ORDER BY ?tesis
```
</details>

### K06 — Katalis apa yang dekat (≤ 45 hari) dan emiten/sektor mana yang terdampak?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KatalisDekat`. SQWRL Q27.
- **Jawaban KB:** Efektif MSCI Review (1 Des 2026) (12 hari) → AADI, AMMN, AMRT, ANTM, ASII, BBCA, BBNI, BBRI, BMRI, ICBP, INDF, ISAT, KLBF, MDKA, TLKM, UNTR; FOMC 9 Des 2026 (20 hari) → BBCA, BBNI, BBRI, BBTN, BMRI, BRIS, BSDE, CTRA, DMAS, PWON, SMRA; Window dressing akhir tahun (≈pertengahan Des) (26 hari) → AADI, ACES, AKRA, AMMN, AMRT, ANTM, ASII, BBCA, BBNI, BBRI, BBTN, BMRI, BRIS, BRMS, BSDE, CPIN, CTRA, EXCL, HEAL, ICBP, INCO, INDF, INKP, ISAT, ITMG, JPFA, JSMR, KLBF, MAPI, MDKA, MEDC, MIKA, MTEL, MYOR, NCKL, PGAS, PTBA, PWON, SIDO, SMGR, TINS, TLKM, TOWR, UNTR, UNVR; RDG Bank Indonesia 15-16 Des 2026 (27 hari) → BBCA, BBNI, BBRI, BBTN, BMRI, BRIS, BSDE, CTRA, DMAS, PWON, SMRA

<details><summary>SPARQL</summary>

```sparql
SELECT ?katalis ?label ?hari ?emiten WHERE { ?k a ex:KatalisDekat ; rdfs:label ?label ; ex:hariMenujuKatalis ?hari . OPTIONAL { ?e ex:memilikiKatalisDekat ?k ; ex:kodeSaham ?emiten } BIND(STRAFTER(STR(?k),"K_") AS ?katalis) } ORDER BY ?hari
```
</details>

### K07 — Emiten mana yang ERP-nya menarik vs obligasi negara (SBN), dan mana yang mahal vs obligasi?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `ERPSangatMenarik`, `ERPMenarik`, `MahalVsObligasi`. SQWRL Q29.
- **Jawaban KB:** ERPMenarik (15): AKRA, DSNG, TOWR, NCKL, SMRA, PWON, LSIP, MTDL, ASSA, BIRD, BBRI, ACES, MAPI, TINS, AALI; ERPSangatMenarik (21): MEDC, BSDE, ITMG, ERAA, ASII, TMAS, PTBA, JSMR, JPFA, CTRA, UNTR, BBTN, AADI, PGAS, BMRI, INDF, SMDR, INKP, BBNI, DMAS, AUTO; MahalVsObligasi (19): BUKA, CPIN, EXCL, MTEL, EMTK, DCII, INCO, MIKA, HEAL, UNVR, MDKA, KLBF, AMMN, SILO, AMRT, SMGR, BRMS, MYOR, IMPC

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (COUNT(?e) AS ?n) (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:ERPSangatMenarik, ex:ERPMenarik, ex:MahalVsObligasi)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### K08 — Kapan & di harga berapa masuk bertahap (akumulasi 3 tranche)?  *(CQ7)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KandidatAkumulasiBertahap`; cek `StrategiAkumulasiBertahap`, `KapitulasiPasar`. SQWRL Q22.
- **Jawaban KB:** Belum ada: syarat kapitulasi pasar (drawdown IHSG ≤ −40% DAN hari crash ≤ −10% dalam sebulan) belum terpenuhi; drawdown saat ini -39.3% (KapitulasiPasar = false). Lihat uji what-if W04.

<details><summary>SPARQL</summary>

```sparql
SELECT ?kode ?t1 ?t2 ?t3 ?drawdown ?kapitulasi WHERE { ?k a ex:KondisiPasarAktif ; ex:drawdownIHSGPersen ?drawdown . BIND(EXISTS { ?k a ex:KapitulasiPasar } AS ?kapitulasi)
 OPTIONAL { ?e a ex:KandidatAkumulasiBertahap ; ex:kodeSaham ?kode ; ex:hargaTranche1 ?t1 ; ex:hargaTranche2 ?t2 ; ex:hargaTranche3 ?t3 } }
```
</details>

### K09 — Apakah sinyal antar-pilar sejalan (konfluensi) atau bertentangan (perlu tunggu konfirmasi)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KonfluensiTinggi`, `TungguKonfirmasi`, `KonflikFundamentalVsBandar`. SQWRL Q28.
- **Jawaban KB:** KonfluensiTinggi: DSNG, ANTM, LSIP, JPFA, AADI, TINS, AALI; MomentumTanpaFundamental: BRMS; TungguKonfirmasi: JPFA, BRMS, AADI

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:KonfluensiTinggi, ex:TungguKonfirmasi, ex:KonflikFundamentalVsBandar, ex:MomentumTanpaFundamental)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### K10 — Revisi konsensus laba: siapa yang direvisi naik / turun dan apa artinya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `RevisiLabaNaik`, `RevisiLabaTurun`, `CelahEkspektasiPositif`, `MurahKarenaLabaTurun`.
- **Jawaban KB:** RevisiLabaNaik: DSNG, CPIN, ANTM, NCKL, DCII, HEAL, LSIP, MDKA, AMMN, BRMS, IMPC, TINS, AALI; RevisiLabaTurun: BUKA, BSDE, ITMG, EXCL, SMRA, UNVR, PTBA, JPFA, CTRA, SMGR, AADI, BMRI, MYOR, BBNI, DMAS, BBRI, ACES, MAPI; CelahEkspektasiPositif: CPIN, NCKL, HEAL, AMMN

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (GROUP_CONCAT(?kode; separator=", ") AS ?emiten) WHERE { ?e ex:kodeSaham ?kode ; a ?k . FILTER(?k IN (ex:RevisiLabaNaik, ex:RevisiLabaTurun, ex:CelahEkspektasiPositif)) FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### K11 — Apakah ada emiten yang kapitulasi (jual panik) atau berita baik yang sudah 'priced-in' (sell the news)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `KapitulasiEmiten`, `SellTheNews`, `BreadthWashout`.
- **Jawaban KB:** BreadthWashout: Pasar_ID_Okt2026 · DasarBelumTerkonfirmasi: Pasar_ID_Okt2026 · KapitulasiEmiten: BBCA, BBRI, BMRI

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas ?x WHERE { ?x a ?k . FILTER(?k IN (ex:KapitulasiEmiten, ex:SellTheNews, ex:BreadthWashout, ex:DasarBelumTerkonfirmasi)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } ORDER BY ?kelas
```
</details>

## Stakeholder

### L01 — Siapa stakeholder sistem ini dan apa kebutuhannya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `Stakeholder` (subkelas StakeholderUtama, StakeholderKandidat, Validator, RegulatorStakeholder, EndUser).
- **Jawaban KB:** EndUser: TraderScalper — Entry-exit intraday berbasis VWAP & order book.; EndUser: PekerjaMuda_Moderat — Menabung rutin (DCA) di saham sektor unggulan.; EndUser: GenZ_Agresif — Mencari momentum, rawan FOMO; butuh peringatan distribusi.; EndUser: Mahasiswa_Konservatif — Modal kecil, ingin dividen & keamanan, horizon 1-3 tahun.; RegulatorStakeholder: BEI_Kepatuhan — Kepatuhan penggunaan data pasar & aturan perdagangan.; RegulatorStakeholder: OJK_Kepatuhan — Sistem diposisikan sebagai alat riset & edukasi, bukan nasihat investa; StakeholderKandidat: AnalisJunior — Alat bantu penalaran terstruktur & pembelajaran heuristik pakar.; StakeholderKandidat: EdukatorKomunitas — Materi belajar berbasis kasus nyata & penalaran pakar.; StakeholderKandidat: TimEquityResearch — Outlook sektoral yang konsisten & dapat ditelusuri jejak alasannya.; StakeholderKandidat: ManajerInvestasi — Sinyal rotasi sektor untuk alokasi portofolio & manajemen risiko outfl; StakeholderUtama: MitraSekuritas — Fitur riset sektoral prediktif yang embedded di aplikasi trading; meni; Validator: PanelPakar — Memvalidasi bobot, ambang aturan, dan hasil backtest walk-forward.

<details><summary>SPARQL</summary>

```sparql
SELECT ?peran ?s ?kebutuhan WHERE { ?s a ?k . FILTER(?k IN (ex:StakeholderUtama, ex:StakeholderKandidat, ex:Validator, ex:RegulatorStakeholder, ex:EndUser)) OPTIONAL { ?s ex:kebutuhanStakeholder ?kebutuhan }
 BIND(STRAFTER(STR(?k),"#") AS ?peran) } ORDER BY ?peran
```
</details>

### L02 — Saham apa yang direkomendasikan untuk tiap persona investor?  *(CQ11)*

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** SQWRL Q14: `direkomendasikanUntuk(?e, ?i) -> sqwrl:select(?i, ?e) ^ sqwrl:orderBy(?i)`
- **Jawaban KB:** PekerjaMuda_Moderat: SILO, AADI, JPFA, ANTM, MIKA, LSIP, SIDO, NCKL, TINS; GenZ_Agresif: TINS, JPFA, ANTM, MEDC, LSIP, MDKA, AADI, AALI, IMPC, DSNG; TraderScalper: MDKA, BRMS; Mahasiswa_Konservatif: AADI, UNTR, JPFA, BMRI, BBCA

<details><summary>SPARQL</summary>

```sparql
SELECT ?persona (GROUP_CONCAT(?kode; separator=", ") AS ?saham) WHERE { ?e ex:direkomendasikanUntuk ?p ; ex:kodeSaham ?kode . FILTER NOT EXISTS { ?e a ex:EmitenUji } BIND(STRAFTER(STR(?p),"Persona_") AS ?persona) } GROUP BY ?persona
```
</details>

### L03 — Profil risiko, horizon, dan modal tiap persona?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Persona_*` → `memilikiProfilRisiko`, `memilikiHorizon`, `modalAwalJuta`.
- **Jawaban KB:** TraderScalper: ProfilAgresif, Horizon_Intraday, modal Rp50 jt; PekerjaMuda_Moderat: ProfilModerat, Horizon_Menengah, modal Rp25 jt; Mahasiswa_Konservatif: ProfilKonservatif, Horizon_Menengah, modal Rp5 jt; GenZ_Agresif: ProfilAgresif, Horizon_Pendek, modal Rp10 jt

<details><summary>SPARQL</summary>

```sparql
SELECT ?persona ?profil ?horizon ?modal WHERE { ?p a ex:EndUser . OPTIONAL { ?p ex:memilikiProfilRisiko ?profil } OPTIONAL { ?p ex:memilikiHorizon ?horizon } OPTIONAL { ?p ex:modalAwalJuta ?modal } BIND(STRAFTER(STR(?p),"Persona_") AS ?persona) }
```
</details>

## Kualitas data

### M01 — Data apa yang sudah kedaluwarsa dan perlu diperbarui?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `DataKedaluwarsa`. SQWRL Q31.
- **Jawaban KB:** Makro_SpreadSBN_UST (17 hari); Makro_UST10Y (17 hari); Makro_YieldSBN10Y (8 hari); Makro_NetAsingYTD (6 hari)

<details><summary>SPARQL</summary>

```sparql
SELECT ?item ?umurHari WHERE { ?i a ex:DataKedaluwarsa . OPTIONAL { ?i ex:umurDataHari ?umurHari } BIND(STRAFTER(STR(?i),"#") AS ?item) } ORDER BY DESC(?umurHari)
```
</details>

### M02 — Emiten mana yang datanya masih perlu diverifikasi (data indikatif)?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `PerluVerifikasiData`, `DataIndikatif`.
- **Jawaban KB:** DataIndikatif: 64 emiten; PerluVerifikasiData: 7 emiten

<details><summary>SPARQL</summary>

```sparql
SELECT ?kelas (COUNT(?e) AS ?n) WHERE { ?e a ?k . FILTER(?k IN (ex:PerluVerifikasiData, ex:DataIndikatif)) BIND(STRAFTER(STR(?k),"#") AS ?kelas) } GROUP BY ?kelas
```
</details>

### M03 — Dari mana sumber data KB dan indikator mana yang bersifat leading?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** DL Query: `SumberData`, `IndikatorLeading`. SQWRL Q32.
- **Jawaban KB:** SumberDataPasar: 11; SumberDataAlternatif: 7; IndikatorCoincident: 53; SumberDataResmi: 13; IndikatorLagging: 17; IndikatorLeading: 62; SumberDataBerita: 4

<details><summary>SPARQL</summary>

```sparql
SELECT ?jenis (COUNT(?s) AS ?n) WHERE { ?s a ?k . FILTER(?k IN (ex:SumberDataResmi, ex:SumberDataPasar, ex:SumberDataBerita, ex:SumberDataAlternatif, ex:IndikatorLeading, ex:IndikatorCoincident, ex:IndikatorLagging)) BIND(STRAFTER(STR(?k),"#") AS ?jenis) } GROUP BY ?jenis
```
</details>

## What-if skenario

### W01 — Jika skenario BULL (pemulihan) yang aktif, sektor apa yang naik?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Skenario_Base_2027_2028`: ubah `statusAktif` 1 → 0; `Skenario_Bull_Pemulihan`: 0 → 1. Jalankan ulang Pellet (Reasoner › Synchronize).
- **Jawaban KB:** Bullish kuat: BarangBaku, Infrastruktur, Keuangan, KonsumenNonPrimer, KonsumenPrimer, Perindustrian, PropertiRealEstat, Teknologi · Bullish moderat: Kesehatan, TransportasiLogistik · Netral: Energi · Bearish: -

### W02 — Jika skenario BEAR (stagflasi) yang aktif, sektor apa yang bertahan?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** `Skenario_Base_2027_2028.statusAktif` = 0, `Skenario_Bear_Stagflasi.statusAktif` = 1, lalu Synchronize reasoner.
- **Jawaban KB:** Bullish kuat: - · Bullish moderat: - · Netral: BarangBaku, Energi, Kesehatan · Bearish: Infrastruktur, Keuangan, KonsumenNonPrimer, KonsumenPrimer, Perindustrian, PropertiRealEstat, Teknologi, TransportasiLogistik

## What-if data emiten

### W03 — Jika ANTM tiba-tiba punya Altman Z = 1,2 dan DER = 3,5, apakah sistem langsung menandainya berisiko & mencoretnya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `ANTM`: ubah `altmanZ` 4.5 → 1.2 dan `der` 0.3 → 3.5 (hapus nilai lama, tambah baru). Synchronize. Cek tipe ANTM.
- **Jawaban KB:** Kelas ANTM: FundamentalSedang, RisikoGoingConcern, ZonaDistress; penalti risiko -5, skor total 20; ANTM TIDAK lagi top pick pakar

## What-if pasar

### W04 — Jika IHSG kapitulasi (drawdown −45% dan ada hari crash −10,5% dalam sebulan), apakah strategi akumulasi bertahap aktif dan berapa harga tranche-nya?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Pasar_ID_Okt2026`: ubah `drawdownIHSGPersen` → −45 dan `penurunanHarianTerbesarPersen` → −10.5 (syarat R-PAS-03: keduanya harus terpenuhi). Synchronize. DL Query `KapitulasiPasar`, `KandidatAkumulasiBertahap`.
- **Jawaban KB:** KapitulasiPasar: Pasar_ID_Okt2026; StrategiAkumulasiBertahap: Pasar_ID_Okt2026; BBCA: T1 6200.0, T2 5828, T3 5456; BMRI: T1 3600.0, T2 3348, T3 3096; CPIN: T1 4100.0, T2 3870.4, T3 3640.8; MIKA: T1 2100.0, T2 1995, T3 1890; UNTR: T1 20000.0, T2 18920, T3 17840

### W05 — Jika premi risiko negara membaik (CDS turun ke 75 bps, CDS & rupiah membaik), apa yang berubah?

- **Status:** ✔ LULUS
- **Cara uji di Protégé:** Individu `Pasar_ID_Okt2026`: `cds5YBps` = 75, `trenCDS1Bulan` = −1, `trenRupiah1Bulan` = −1; individu `Makro_CDS5Y` `nilaiIndikator` = 75. Synchronize.
- **Jawaban KB:** skor stres 10.0 (sebelumnya 11), regime Regime_KrisisLikuiditas; DivergensiIntermarketBullish: Pasar_ID_Okt2026; TesisTerpicu: Tesis_Keuangan_Kontrarian; PremiRisikoNegaraTinggi: hilang
