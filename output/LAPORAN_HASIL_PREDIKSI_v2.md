# Laporan Hasil Inferensi v2 — Sistem Pakar Prediksi Sektor Saham BEI (1–3 Tahun)

Kelompok 9 KBR · Jonnathan Azarel Gunawan (L0224005) · Gloria Dana Praysilia (L0224043)  
Tanggal acuan: **12 November 2026** · Skenario aktif: **Base Case 2027-2028: Normalisasi Bertahap** · Regime terdeteksi: **Krisis Likuiditas / Kapitulasi** · Reasoner: Pellet (OWLAPI) — konsisten ✅

> **Disclaimer:** Keluaran penalaran sistem pakar untuk keperluan akademik/edukasi, bukan nasihat investasi. Data makro & berita bersumber dari pemberitaan s.d. {TGL} (anotasi `sumberReferensi`). **Rasio, teknikal, bandarmology, revisi konsensus per emiten adalah snapshot indikatif** dan ditandai `DataIndikatif`; sistem sendiri menandai rekomendasinya `PerluVerifikasiData`.

## 0. Ringkasan Eksekutif — Keputusan Pakar

1. **Regime pasar: Krisis Likuiditas / Kapitulasi** (skor stres 11/12). Bobot pilar otomatis bergeser: fundamental & valuasi ×1,5, smart money ×1,5, penalti neraca lemah ×1,5, teknikal & sentimen ×0,5; risiko per transaksi dipangkas ke **0.50%** modal.
2. **Strategi pasar:** syarat zona akumulasi generasional belum terpenuhi (drawdown IHSG -39.27% > −40%); dasar belum terkonfirmasi (CDS & rupiah masih memburuk) → **selektif, tunggu konfirmasi**; posisi tetap dibatasi aturan ukuran posisi regime.
3. **Sektor inti (core, robust lintas skenario):** **Barang Baku** (EV 10.75), **Kesehatan** (EV 7.50).
4. **Sektor satelit (asimetris-kontrarian):** **Infrastruktur** (Base 6 → Bull 20), **Keuangan** (Base 0 → Bull 19); pemicu tesis: yield SBN < 6.75%. **Keuangan** dipantau sebagai kontrarian (pemicu CDS < 85 bps, kini 103.79).
5. **Top pick adaptif-regime:** ANTM (35.0), TINS (33.0), AADI (29.0), LSIP (29.0), NCKL (26.5), JPFA (26.5), MIKA (26.0).
6. **Akumulasi bertahap (kualitas yang terpukul):** .
7. **Katalis ≤45 hari:** RDG Bank Indonesia 17-18 Nov 2026 (H-6); Efektif MSCI Review (1 Des 2026) (H-19); FOMC 9 Des 2026 (H-27); Window dressing akhir tahun (≈pertengahan Des) (H-33); RDG Bank Indonesia 15-16 Des 2026 (H-34) → kandidat dengan katalis biner dekat diberi strategi tranche.
8. **Kill switch:** semua tesis masih valid; Tesis: Emas & nikel menopang Barang Baku **rapuh**, Tesis: Kesehatan defensif **rapuh**, Tesis kontrarian: Infrastruktur digital **rapuh**. 5 indikator makro harian sudah kedaluwarsa → perlu pembaruan sebelum eksekusi.

## 1. Konteks Pasar (state vector `Pasar_ID_Okt2026`)

| Indikator | Nilai | Catatan / sumber |
|---|---|---|
| Drawdown IHSG vs akhir 2025 | -39.27% | IHSG 4.996,61 (19 Okt) vs 8.646 |
| Perubahan IHSG ±1 bulan | -11.54% | 30 Sep 6.095,86 → 19 Okt |
| Hari crash terbesar | -11.57% | 16 Okt 2026, setelah MSCI umumkan konsultasi standalone (15 Okt) |
| Net asing YTD | Rp-98.00 T | s.d. 16 Okt |
| CDS Indonesia 5Y | 103.79 bps | 21 Okt; naik dari 92,40 |
| Yield SBN 10Y / spread vs UST | 7.71% / 281 bps | 17 Sep (kedaluwarsa) |
| USD/IDR | 18,239 | awal Okt |
| Fed Funds (batas atas) | 4.00% | FOMC 16 Sep naik 25 bps; median akhir 2026 4,1% |
| Inflasi Indonesia | 3.23% | Sep 2026 |
| Brent | US$92.39 | 12 Okt; serangan Houthi |
| Emas | US$3,959.03 | 18 Sep; turun dari puncak |
| Breadth (% saham > MA200) | 18.75% | dihitung dari universe 64 emiten |

Katalis struktural terbesar: **konsultasi MSCI reklasifikasi ke Standalone** — masukan s.d. 30 Apr 2027, keputusan final paling lambat akhir Juni 2027; estimasi outflow pasif USD3–6 miliar.

## 2. Deteksi Regime & Bobot Adaptif (meta-knowledge)

| Komponen stres | Nilai | Poin |
|---|---|---|
| Drawdown IHSG | -39.27 | 2 |
| CDS 5Y | 103.79 | 1 |
| Net asing YTD | -98.00 | 2 |
| USD/IDR | 18,239.00 | 2 |
| Yield SBN 10Y | 7.71 | 2 |
| Breadth | 18.75 | 2 |
| **Skor stres** | | **11 / 12** |

| Regime | F | V | T | B | S | Sektor | Risiko | Likuid | SmartMoney | Risiko/transaksi | Tranche | Ambang top pick |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Krisis Likuiditas / Kapitulasi ◀ aktif** | 1.5 | 1.5 | 0.5 | 1.0 | 0.5 | 1.0 | 1.5 | 1.0 | 1.5 | 0.50% | 30/30/40 | 24.7 |
| Risk-Off Normal | 1.2 | 1.0 | 0.8 | 1.2 | 0.8 | 1.0 | 1.2 | 1.0 | 1.2 | 0.75% | 40/30/30 | 23.8 |
| Netral | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.00% | 50/30/20 | 22.8 |
| Risk-On / Euforia | 0.8 | 0.7 | 1.3 | 1.2 | 1.2 | 1.0 | 0.8 | 1.0 | 1.0 | 1.00% | 60/40/0 | 23.1 |

*Analis biasa memakai bobot tetap di semua kondisi; sistem pakar mengubah bobot sesuai regime (R-REG, R-ADP-02).*

## 3. Reaction Function Kebijakan (antisipatif)

| Antisipasi | Terpicu? | Node transmisi yang diaktifkan |
|---|---|---|
| BI Naikkan Suku Bunga Pre-emptif | ✅ | Suku Bunga BI Naik/Tinggi |
| Penyesuaian Harga BBM / Subsidi | — | Penyesuaian Harga BBM Bersubsidi (Antisipasi) |
| Outflow Asing dari SBN | — | Outflow Asing dari SBN |
| Stabilisasi Pasar oleh Otoritas & Institusi Domestik | ✅ | Dukungan Likuiditas Domestik (institusi lokal, buyback) |
| Kenaikan Premi Risiko Negara | ✅ | Premi Risiko Negara (CDS) Naik |

Node yang diaktifkan ikut merambat lewat rantai kausal (R-GEO-04) sehingga headwind/tailwind sektor sudah memperhitungkan reaksi otoritas **sebelum** diumumkan.

## 4. OUTPUT UTAMA — Prediksi Sektor 1–3 Tahun (probabilistik & robust)

Probabilitas skenario: Base 50% · Bull 25% · Bear 25%. EV = Σ p × skor outlook.

| # | Sektor | Base | Bull | Bear | **EV** | Prediksi (Base) | Peran portofolio | Penanda pakar |
|---|---|---|---|---|---|---|---|---|
| 1 | Barang Baku | 11 | 17 | 4 | **10.75** | BULLISH MODERAT | **INTI (core)** | RobustLintasSkenario, KeyakinanTinggi, PresedenHistoris, DiuntungkanGeopolitik, PerluPemantauanKetat |
| 2 | Infrastruktur | 6 | 20 | -1 | **7.75** | NETRAL | **SATELIT** | AsimetriPositif, PerluPemantauanKetat |
| 3 | Kesehatan | 8 | 8 | 6 | **7.50** | BULLISH MODERAT | **INTI (core)** | RobustLintasSkenario, DiuntungkanGeopolitik, PerluPemantauanKetat |
| 4 | Barang Konsumen Primer | 6 | 12 | 1 | **6.25** | NETRAL | kontrarian (pantau) | DiuntungkanGeopolitik |
| 5 | Perindustrian | 4 | 14 | -1 | **5.25** | NETRAL |  | AsimetriPositif |
| 6 | Energi | 6 | 2 | 4 | **4.50** | NETRAL |  | PresedenHistoris, DiuntungkanGeopolitik |
| 7 | Keuangan | 0 | 19 | -10 | **2.25** | BEARISH | **SATELIT** | AsimetriPositif, PresedenHistoris, KatalisDekat |
| 8 | Properti & Real Estat | -2 | 14 | -9 | **0.25** | BEARISH |  | KatalisDekat |
| 9 | Teknologi | -4 | 16 | -13 | **-1.25** | BEARISH |  |  |
| 10 | Transportasi & Logistik | -5 | 10 | -13 | **-3.25** | BEARISH |  | DiuntungkanGeopolitik |
| 11 | Barang Konsumen Non-Primer | -7 | 12 | -17 | **-4.75** | BEARISH |  |  |

### 4.1 Jalur penalaran multi-hop (sektor inti & satelit)

#### Sektor Barang Baku — INTI (core)

**Tailwind:**

- Tekanan Rupiah (rekor ~Rp18.239/USD, 12 Nov 2026) → Rupiah Melemah → Pendapatan Eksportir (USD) Naik dalam Rupiah *(provenans global/geopolitik)*
- Kebijakan Hilirisasi & Kuota RKAB Nikel → Harga Nikel Tertopang Kuota
- Harga Emas Tinggi (puncak ~US$4.390 Sep, ~US$3.959 pada 12 Nov 2026) → Permintaan Safe Haven Emas *(provenans global/geopolitik)*

**Tema struktural:** Hilirisasi Nikel & Mineral; Emas Safe Haven & Bank Sentral

**Preseden historis (CBR):** Supercycle Komoditas & Perang Rusia-Ukraina 2022

**Tesis & kill switch:** Tesis: Emas & nikel menopang Barang Baku — indikator Harga Emas Spot = 3,959.03; status: Rapuh, Valid.

#### Sektor Kesehatan — INTI (core)

**Tailwind:**

- Penutupan Selat Hormuz & Berakhirnya Gencatan (8 Jul 2026) → Premi Risiko Timur Tengah Naik → Risk-off Global *(provenans global/geopolitik)*

**Headwind:**

- Tekanan Rupiah (rekor ~Rp18.239/USD, 12 Nov 2026) → Rupiah Melemah → Biaya Bahan Baku Impor Naik

**Tema struktural:** Belanja Kesehatan & JKN

**Tesis & kill switch:** Tesis: Kesehatan defensif — indikator Kurs USD/IDR = 18,239.00; status: Rapuh, Valid.

#### Sektor Infrastruktur — SATELIT

**Tailwind:**

- Investor Domestik Membeli Blue Chip Terdiskon → Dukungan Likuiditas Domestik (institusi lokal, buyback)
- Gelombang Investasi Data Center & AI → Investasi Data Center & AI → Permintaan Konektivitas & Fiber Naik
- Reformasi Free Float 15% & Transparansi OJK/BEI → Reformasi Transparansi Pasar Modal → Kepercayaan Investor Asing Pulih (1-3 th)

**Peluang kontrarian:** Diskon Valuasi Ekstrem Big Caps; Dukungan Likuiditas Domestik (institusi lokal, buyback)

**Headwind:**

- MSCI Freeze FIF Indonesia (Feb-Nov 2026) → Outflow Dana Pasif (MSCI/S&P)
- Twin Deficit Q1 2026 & Kekhawatiran Fiskal → Tekanan Fiskal / Twin Deficit → Ruang Belanja Infrastruktur Terbatas

**Tema struktural:** Data Center & AI; Konsolidasi Telko (XLSmart)

**Tesis & kill switch:** Tesis kontrarian: Infrastruktur digital — indikator Yield SBN 10Y = 7.71; status: PerluDataBaru, Rapuh, Valid.

#### Sektor Keuangan — SATELIT

**Tailwind:**

- Investor Domestik Membeli Blue Chip Terdiskon → Dukungan Likuiditas Domestik (institusi lokal, buyback)
- S&P Pertahankan Rating Indonesia BBB Stabil → Stabilitas Rating Investment Grade
- BI Akan Turunkan GWM Bank → Likuiditas Bank Longgar (GWM turun)
- Reformasi Free Float 15% & Transparansi OJK/BEI → Reformasi Transparansi Pasar Modal → Kepercayaan Investor Asing Pulih (1-3 th)

**Peluang kontrarian:** Diskon Valuasi Ekstrem Big Caps; Dukungan Likuiditas Domestik (institusi lokal, buyback)

**Headwind:**

- MSCI Freeze FIF Indonesia (Feb-Nov 2026) → Outflow Dana Pasif (MSCI/S&P)
- Krisis Pasar Modal Indonesia 2026 (IHSG -42% YTD) → Dana Asing Keluar dari Emerging Market
- MSCI Konsultasi Reklasifikasi Indonesia ke Standalone (15 Okt 2026) → Premi Risiko Negara (CDS) Naik
- MSCI Konsultasi Reklasifikasi Indonesia ke Standalone (15 Okt 2026) → Premi Risiko Negara (CDS) Naik → Outflow Asing dari SBN
- RDG BI Okt 2026: BI Rate Tetap 5,75%, Deposit Facility Naik ke 5% → Suku Bunga BI Naik/Tinggi → Biaya Kredit Naik

**Tema struktural:** Inklusi & Pendalaman Keuangan; Reformasi Free Float & Transparansi; Danantara & Konsolidasi BUMN

**Preseden historis (CBR):** Kenaikan Fed & Perang Dagang 2018; Supercycle Komoditas & Perang Rusia-Ukraina 2022

**Tesis & kill switch:** Tesis kontrarian: Big banks pasca-kapitulasi — indikator CDS Indonesia 5Y = 103.79; status: PerluDataBaru, Valid.

## 5. Top-3 Emiten per Sektor Inti/Satelit — Analis Biasa vs Sistem Pakar

*Skor statis* = penjumlahan pilar berbobot sama (cara analis biasa). *Skor adaptif* = bobot regime krisis + smart money + kontribusi sektor berbasis EV.

**Sektor Barang Baku**

| Rank | Emiten | Skor statis | **Skor adaptif** | Konfluensi | RS vs IHSG | ERP | Pos. maks | Status pakar | Catatan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **ANTM** — Aneka Tambang | 27 | **35.0** | 5.0/6 | 8.5 pp | 2.3 pp | 7.1% | TOP PICK ADAPTIF | RisikoKonsentrasiTema, RisikoOutflowPasif |
| 2 | **TINS** — Timah | 27 | **33.0** | 6/6 | 6.5 pp | 4.8 pp | 6.2% | TOP PICK ADAPTIF | ZonaAbuAbu |
| 3 | **NCKL** — Trimegah Bangun Persada | 21 | **26.5** | 4/6 | 2.5 pp | 7.7 pp | 7.3% | TOP PICK ADAPTIF | CelahEkspektasiPositif, RisikoHSC, RisikoKonsentrasiTema |

**Sektor Kesehatan**

| Rank | Emiten | Skor statis | **Skor adaptif** | Konfluensi | RS vs IHSG | ERP | Pos. maks | Status pakar | Catatan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **MIKA** — Mitra Keluarga Karyasehat | 21 | **26.0** | 4/6 | 0.5 pp | -3.5 pp | 10.0% | TOP PICK ADAPTIF | MahalVsObligasi |
| 2 | **KLBF** — Kalbe Farma | 19 | **23.0** | 3/6 | -1.5 pp | -1.0 pp | 9.6% | watchlist | MahalVsObligasi, RisikoOutflowPasif |
| 3 | **SIDO** — Industri Jamu & Farmasi Sido Muncul | 20 | **23.0** | 4/6 | 0.5 pp | 0.6 pp | 10.4% | watchlist |  |

**Sektor Infrastruktur**

| Rank | Emiten | Skor statis | **Skor adaptif** | Konfluensi | RS vs IHSG | ERP | Pos. maks | Status pakar | Catatan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **ISAT** — Indosat Ooredoo Hutchison | 18 | **23.5** | 4/6 | -3.5 pp | 3.4 pp | 7.3% | - | ZonaAbuAbu, RisikoOutflowPasif |
| 2 | **TLKM** — Telkom Indonesia | 11 | **18.0** | 2/6 | -6.5 pp | 3.4 pp | 8.3% | - | ZonaAbuAbu, RisikoOutflowPasif |
| 3 | **TOWR** — Sarana Menara Nusantara | 12 | **17.0** | 2/6 | -5.5 pp | 7.7 pp | 7.6% | - | ZonaAbuAbu |

**Sektor Keuangan**

| Rank | Emiten | Skor statis | **Skor adaptif** | Konfluensi | RS vs IHSG | ERP | Pos. maks | Status pakar | Catatan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **BBCA** — Bank Central Asia | 13 | **23.5** | 2/6 | -9.5 pp | -0.0 pp | 8.3% | - | MahalVsObligasi, RisikoOutflowPasif |
| 2 | **BRIS** — Bank Syariah Indonesia | 15 | **22.0** | 2/6 | -4.5 pp | 0.6 pp | 6.9% | - | RisikoHSC |
| 3 | **BMRI** — Bank Mandiri | 12 | **20.5** | 2/6 | -11.5 pp | 9.0 pp | 7.1% | - | MurahKarenaLabaTurun, ERPSangatMenarik, RisikoOutflowPasif |

### 5.1 Di mana sistem pakar berbeda dari analis biasa

- **Hanya dipilih analis biasa (skor statis) — dibuang sistem pakar:**
  - **BRMS**: skor adaptif 22.5 < ambang 24.7; tanpa jejak smart money; ERP negatif (kalah dari SBN); kekuatannya dominan dari teknikal (bobot 0,5 di regime krisis)
- **Hanya dipilih sistem pakar:**
  - **AADI** (statis 25 → adaptif 29.0): fundamental 10/10; jejak smart money; ERP 17.3 pp; sektor EV 4.50
  - **JPFA** (statis 19 → adaptif 26.5): fundamental 8/10; jejak smart money; ERP 9.0 pp; sektor EV 6.25
  - **LSIP** (statis 22 → adaptif 29.0): fundamental 9/10; jejak smart money; sektor EV 6.25
- **Disepakati keduanya:** ANTM, MIKA, NCKL, TINS.

## 6. Rencana Akumulasi Bertahap (kapitulasi)

Regime Krisis Likuiditas / Kapitulasi: porsi tranche 30% / 30% / 40% dari alokasi; tangga harga T1 = harga, T2 = −2×ATR, T3 = −4×ATR.

| Emiten | Sektor | T1 | T2 | T3 | Pos. maks | Pemicu | Katalis biner dekat |
|---|---|---|---|---|---|---|---|

## 7. Konfluensi, Konflik, Refleksivitas & Ekspektasi Laba

- **Konfluensi tinggi (≥5/6 pilar):** AADI, AALI, ANTM, BRMS, DSNG, JPFA, LSIP, TINS
- **Tunggu konfirmasi (konflik sinyal):** AADI, BRMS
- **Fundamental kuat vs bandar distribusi:** -
- **Distribusi saat euforia:** -
- **Berita buruk priced-in:** JPFA, MEDC
- **Sell the news:** -
- **Mengungguli IHSG ≥5 pp:** AALI, ANTM, BRMS, DSNG, JPFA, LSIP, MDKA, MEDC, TINS
- **Kapitulasi emiten:** BBCA, BBRI, BMRI
- **Celah ekspektasi positif (revisi naik, harga tertinggal):** AMMN, CPIN, HEAL, NCKL
- **Murah karena laba turun (value-trap dini):** AADI, ACES, BBNI, BBRI, BMRI, BSDE, CTRA, DMAS, MAPI, MYOR, PTBA, SMRA, UNVR
- **ERP ≥ 8 pp (murah vs SBN):** AADI, ASII, AUTO, BBNI, BBTN, BMRI, BSDE, CTRA, DMAS, ERAA, INDF, INKP, ITMG, JPFA, JSMR, MEDC, PGAS, PTBA, SMDR, TMAS, UNTR
- **Mahal vs obligasi (ERP < 0):** AMMN, AMRT, BBCA, BRMS, BUKA, CPIN, DCII, EMTK, EXCL, HEAL, IMPC, INCO, KLBF, MDKA, MIKA, MTEL, MYOR, SILO, SMGR, UNVR
- **Risiko konsentrasi tema:** ANTM, NCKL

## 8. Kalender Katalis

| Katalis | Tanggal | H- | Tipe | ≤45 hari |
|---|---|---|---|---|
| FOMC 28 Okt 2026 | 2026-10-28 | -15 | Biner |  |
| Batas rilis laporan keuangan Q3-2026 (≈31 Okt) | 2026-10-31 | -12 | Terjadwal |  |
| Pemilu Sela AS 3 Nov 2026 | 2026-11-03 | -9 | Biner |  |
| MSCI Index Review Nov 2026 (umum 11 Nov) | 2026-11-11 | -1 | Biner |  |
| RDG Bank Indonesia 17-18 Nov 2026 | 2026-11-18 | 6 | Biner | ✅ |
| Efektif MSCI Review (1 Des 2026) | 2026-12-01 | 19 | Terjadwal | ✅ |
| FOMC 9 Des 2026 | 2026-12-09 | 27 | Biner | ✅ |
| Window dressing akhir tahun (≈pertengahan Des) | 2026-12-15 | 33 | Musiman | ✅ |
| RDG Bank Indonesia 15-16 Des 2026 | 2026-12-16 | 34 | Biner | ✅ |
| Evaluasi mayor LQ45 (≈akhir Jan 2027) | 2027-01-25 | 74 | Terjadwal |  |
| Ramadan-Lebaran 2027 (≈Feb-Mar) | 2027-02-08 | 88 | Musiman |  |
| MSCI Index Review Feb 2027 (umum 9 Feb) | 2027-02-09 | 89 | Biner |  |
| Musim RUPS & dividen (≈Mar-Jun 2027) | 2027-03-15 | 123 | Musiman |  |
| Batas akhir konsultasi MSCI (30 Apr 2027) | 2027-04-30 | 169 | Biner |  |
| Keputusan final MSCI standalone (≈akhir Jun 2027) | 2027-06-30 | 230 | Biner |  |

Strategi tranche sebelum katalis biner: -.

## 9. Tesis Investasi & Kill Switch

| Tesis | Indikator kunci | Nilai | Batas bawah | Batas atas | Pemicu kontrarian | Buffer | Status |
|---|---|---|---|---|---|---|---|
| Tesis: Emas & nikel menopang Barang Baku | Harga Emas Spot | 3,959.03 | 3,800.00 | - | - | 4.0% | Rapuh, Valid |
| Tesis: Premi geopolitik minyak | Harga Brent | 92.39 | 75.00 | - | - | 18.8% | Valid |
| Tesis: Kesehatan defensif | Kurs USD/IDR | 18,239.00 | - | 19,500.00 | - | 6.9% | Rapuh, Valid |
| Tesis kontrarian: Big banks pasca-kapitulasi | CDS Indonesia 5Y | 103.79 | - | 150.00 | 85.00 | 44.5% | PerluDataBaru, Valid |
| Tesis kontrarian: Infrastruktur digital | Yield SBN 10Y | 7.71 | - | 8.00 | 6.75 | 3.8% | PerluDataBaru, Rapuh, Valid |
| Tesis: Konsumen primer (MBG & CPO) | Inflasi Indonesia (yoy) | 3.23 | - | 5.00 | - | 54.8% | Valid |

## 10. Kesehatan Fundamental, Risiko Collapse & Tata Kelola

| Emiten | Kategori | Penalti | Sinyal |
|---|---|---|---|
| MDKA | ZonaDistress | -5 |  |
| SMRA | RisikoGoingConcern, ZonaDistress, RisikoManipulasiLaba, ValueTrap | -5 | SinyalHindari |
| GOTO | RisikoGoingConcern, ZonaDistress, RedFlagBerita | -5 | SinyalHindari |
| EXCL | RisikoGoingConcern, ZonaDistress | -5 | SinyalHindari |
| JSMR | RisikoGoingConcern, ZonaDistress | -5 | SinyalHindari |
| ASSA | RisikoGoingConcern, ZonaDistress | -5 | SinyalHindari |
| INKP | ZonaAbuAbu, ValueTrap | -1 |  |
| NCKL | RisikoHSC | 0 |  |
| ERAA | ValueTrap | 0 |  |
| BRIS | RisikoHSC | 0 |  |
| BBTN | ValueTrap | 0 |  |
| DCII | RisikoHSC | 0 |  |

## 11. Sinyal Quant Trade

| Emiten | Sinyal | Harga | SL (−2·ATR) | TP (+3·ATR) | Pos. maks | Konteks |
|---|---|---|---|---|---|---|
| ANTM | SinyalEntry, SinyalBuyOnWeakness | 2,900 | 2,697 | 3,204 | 7.1% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| TINS | SinyalEntry | 1,900 | 1,748 | 2,128 | 6.2% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| AADI | SinyalEntry, SinyalBuyOnWeakness | 5,400 | 5,054 | 5,918 | 7.8% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, TungguKonfirmasi |
| LSIP | SinyalEntry, SinyalBuyOnWeakness | 1,050 | 987 | 1,144 | 8.3% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| JPFA | SinyalEntry, SinyalBuyOnWeakness | 1,600 | 1,491 | 1,763 | 7.3% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| MIKA | SinyalBuyOnWeakness | 2,100 | 1,995 | 2,258 | 10.0% | AkumulasiInstitusiAsing, AkumulasiTersembunyi |
| CPIN | SinyalBuyOnWeakness | 4,100 | 3,870 | 4,444 | 8.9% | AkumulasiInstitusiAsing, AkumulasiTersembunyi |
| DSNG | SinyalEntry | 850 | 796 | 932 | 7.8% | FaseMarkUpWyckoff |
| UNTR | SinyalBuyOnWeakness | 20,000 | 18,920 | 21,620 | 9.3% | AkumulasiInstitusiAsing, AkumulasiTersembunyi |
| IMPC | SinyalEntry | 1,900 | 1,763 | 2,105 | 6.9% | FaseMarkUpWyckoff |
| BBCA | SinyalBuyOnWeakness | 6,200 | 5,828 | 6,758 | 8.3% | AkumulasiTersembunyi |
| BRMS | SinyalScalpingLong | 430 | - | - | 4.8% | FaseMarkUpWyckoff, LonjakanVolume, TungguKonfirmasi |
| AALI | SinyalEntry | 6,000 | 5,688 | 6,468 | 9.6% | FaseMarkUpWyckoff |
| MEDC | SinyalEntry | 1,150 | 1,063 | 1,281 | 6.6% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| MDKA | SinyalEntry, SinyalScalpingLong | 1,900 | 1,729 | 2,156 | 5.6% | AkumulasiInstitusiAsing, FaseMarkUpWyckoff, LonjakanVolume |

**Anti-FOMO:** ACES, BBRI, EMTK, GOTO, JSMR, MAPI, SMGR, SMRA, UNVR terdeteksi distribusi ke ritel.

## 12. Uji Aturan dengan Emiten Hipotetis (Validation & Verification)

| Emiten uji (fiktif) | Skenario uji | Kelas yang berhasil diinferensi |
|---|---|---|
| UJI_GORENG | free float 8%, volume 4,5×, ARA 3×/5 hari, top-3 broker 80%, RSI 88 | IndikasiSahamGorengan, RisikoPumpAndDump, RisikoHSC, SinyalHindari, TungguKonfirmasi |
| UJI_GADAI | 45% saham pengendali digadaikan, downtrend | RisikoForcedSellPengendali, SinyalHindari |
| UJI_INSIDER | direksi membeli, PER 6 vs rata-rata 12 | SinyalOrangDalam |

Emiten uji tidak masuk peringkat apa pun; fungsinya membuktikan aturan tata kelola bekerja karena data gadai/orang dalam emiten nyata belum diisi.

## 13. Kualitas Data

- **Indikator makro kedaluwarsa (umur > 5× frekuensi):** Makro_CDS5Y, Makro_NetAsingYTD, Makro_SpreadSBN_UST, Makro_UST10Y, Makro_YieldSBN10Y
- **Tesis perlu data baru:** Tesis kontrarian: Big banks pasca-kapitulasi, Tesis kontrarian: Infrastruktur digital
- **Rekomendasi yang wajib diverifikasi (PerluVerifikasiData):** AADI, ANTM, JPFA, LSIP, MIKA, NCKL, TINS

## 14. Rekomendasi per Persona

- **Mahasiswa Konservatif**: AADI, BBCA, BMRI, JPFA, UNTR
- **PekerjaMuda Moderat**: AADI, ANTM, JPFA, LSIP, MIKA, NCKL, SIDO, SILO, TINS
- **GenZ Agresif**: AADI, AALI, ANTM, DSNG, IMPC, JPFA, LSIP, MDKA, MEDC, TINS
- **TraderScalper**: BRMS, MDKA

## 15. Rasio Knowledge Base vs Reasoning

| Komponen | Aksioma | Porsi |
|---|---|---|
| Knowledge Base (TBox + ABox + anotasi + deklarasi) | 15,064 | **98.0%** |
| Reasoning (aturan SWRL) | 303 | 2.0% |
| **Total** | 15,367 | 100% |

Aksioma logis saja: KB 8,707 vs aturan 303 → **96.6% KB**.

**303 aturan SWRL per pilar:** Fundamental (30), Regime Pasar (24), Teknikal (16), Konfluensi (15), Integrasi (14), Bandarmology (13), Sentimen (13), Geopolitik (11), Fundamental-Risiko (10), Quant Trade (10), Tesis & Invalidasi (10), Fundamental-Valuasi (8), Tata Kelola (8), Prediksi Sektor (7), Robustness Skenario (7), Stakeholder (6), Struktur Pasar (6), Katalis (6), Fundamental-Sektor (5), Rotasi Sektor (5), Reaction Function (5), Refleksivitas (5), Adaptif Regime (5), Teknikal-Pola (4), Bandarmology-Wyckoff (4), Geopolitik→Emiten (4), Bandarmology-Sektor (4), Kualitas Data (4), Kapitulasi (4), Ekspektasi Laba (4), Valuasi Relatif Obligasi (4), Konflik Sinyal (4), Skenario (3), Makro-Geopolitik (3), Case-Based Reasoning (3), Likuiditas (3), Profil Investor (3), Bandarmology-Broker (2), Tema Struktural (2), Scalper Pattern (2), Intermarket (2), Konstruksi Portofolio (2), Manajemen Posisi (2), Peringatan (1).
