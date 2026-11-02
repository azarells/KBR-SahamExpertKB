# Laporan Hasil Inferensi v2 — Sistem Pakar Prediksi Sektor Saham BEI (1–3 Tahun)

Kelompok 9 KBR · Jonnathan Azarel Gunawan (L0224005) · Gloria Dana Praysilia (L0224043)  
Tanggal acuan: **26 Oktober 2026** · Skenario aktif: **Base Case 2027-2028: Normalisasi Bertahap** · Regime terdeteksi: **Krisis Likuiditas / Kapitulasi** · Reasoner: Pellet (OWLAPI) — konsisten ✅

> **Disclaimer:** Keluaran penalaran sistem pakar untuk keperluan akademik/edukasi, bukan nasihat investasi. Data makro & berita bersumber dari pemberitaan s.d. Okt 2026 (anotasi `sumberReferensi`). **Rasio, teknikal, bandarmology, revisi konsensus per emiten adalah snapshot indikatif** dan ditandai `DataIndikatif`; sistem sendiri menandai rekomendasinya `PerluVerifikasiData`.

## 0. Ringkasan Eksekutif — Keputusan Pakar

1. **Regime pasar: Krisis Likuiditas / Kapitulasi** (skor stres 10/12). Bobot pilar otomatis bergeser: fundamental & valuasi ×1,5, smart money ×1,5, penalti neraca lemah ×1,5, teknikal & sentimen ×0,5; risiko per transaksi dipangkas ke **0.50%** modal.
2. **Strategi pasar:** Zona Akumulasi Generasional — tetapi dasar belum terkonfirmasi (CDS & rupiah masih memburuk) → **akumulasi bertahap 30/30/40**, bukan all-in.
3. **Sektor inti (core, robust lintas skenario):** **Barang Baku** (EV 9.75), **Kesehatan** (EV 8.50).
4. **Sektor satelit (asimetris-kontrarian):** **Infrastruktur** (Base 6 → Bull 20); pemicu tesis: yield SBN < 6.75%. **Keuangan** dipantau sebagai kontrarian (pemicu CDS < 85 bps, kini 99.73).
5. **Top pick adaptif-regime:** ANTM (33.5), LSIP (29.0), TINS (28.0), AADI (27.5), JPFA (27.5), MIKA (27.5), CPIN (26.0), HEAL (26.0), DSNG (25.5), UNTR (25.0).
6. **Akumulasi bertahap (kualitas yang terpukul):** MIKA, CPIN, HEAL, UNTR, BBCA, BMRI.
7. **Katalis ≤45 hari:** FOMC 28 Okt 2026 (H-2); Batas rilis laporan keuangan Q3-2026 (≈31 Okt) (H-5); Pemilu Sela AS 3 Nov 2026 (H-8); MSCI Index Review Nov 2026 (umum 11 Nov) (H-16); Efektif MSCI Review (1 Des 2026) (H-36); FOMC 9 Des 2026 (H-44) → kandidat dengan katalis biner dekat diberi strategi tranche.
8. **Kill switch:** semua tesis masih valid; Tesis: Kesehatan defensif **rapuh**. 9 indikator makro harian sudah kedaluwarsa → perlu pembaruan sebelum eksekusi.

## 1. Konteks Pasar (state vector `Pasar_ID_Okt2026`)

| Indikator | Nilai | Catatan / sumber |
|---|---|---|
| Drawdown IHSG vs akhir 2025 | -42.21% | IHSG 4.996,61 (19 Okt) vs 8.646 |
| Perubahan IHSG ±1 bulan | -18.03% | 30 Sep 6.095,86 → 19 Okt |
| Hari crash terbesar | -11.57% | 16 Okt 2026, setelah MSCI umumkan konsultasi standalone (15 Okt) |
| Net asing YTD | Rp-88.19 T | s.d. 16 Okt |
| CDS Indonesia 5Y | 99.73 bps | 21 Okt; naik dari 92,40 |
| Yield SBN 10Y / spread vs UST | 7.14% / 216 bps | 17 Sep (kedaluwarsa) |
| USD/IDR | 17,938 | awal Okt |
| Fed Funds (batas atas) | 4.00% | FOMC 16 Sep naik 25 bps; median akhir 2026 4,1% |
| Inflasi Indonesia | 3.28% | Sep 2026 |
| Brent | US$106.65 | 12 Okt; serangan Houthi |
| Emas | US$4,390.11 | 18 Sep; turun dari puncak |
| Breadth (% saham > MA200) | 18.75% | dihitung dari universe 64 emiten |

Katalis struktural terbesar: **konsultasi MSCI reklasifikasi ke Standalone** — masukan s.d. 30 Apr 2027, keputusan final paling lambat akhir Juni 2027; estimasi outflow pasif USD3–6 miliar.

## 2. Deteksi Regime & Bobot Adaptif (meta-knowledge)

| Komponen stres | Nilai | Poin |
|---|---|---|
| Drawdown IHSG | -42.21 | 2 |
| CDS 5Y | 99.73 | 1 |
| Net asing YTD | -88.19 | 2 |
| USD/IDR | 17,938.00 | 2 |
| Yield SBN 10Y | 7.14 | 1 |
| Breadth | 18.75 | 2 |
| **Skor stres** | | **10 / 12** |

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
| Penyesuaian Harga BBM / Subsidi | ✅ | Penyesuaian Harga BBM Bersubsidi (Antisipasi) |
| Outflow Asing dari SBN | ✅ | Outflow Asing dari SBN |
| Stabilisasi Pasar oleh Otoritas & Institusi Domestik | ✅ | Dukungan Likuiditas Domestik (institusi lokal, buyback) |
| Kenaikan Premi Risiko Negara | ✅ | Premi Risiko Negara (CDS) Naik |

Node yang diaktifkan ikut merambat lewat rantai kausal (R-GEO-04) sehingga headwind/tailwind sektor sudah memperhitungkan reaksi otoritas **sebelum** diumumkan.

## 4. OUTPUT UTAMA — Prediksi Sektor 1–3 Tahun (probabilistik & robust)

Probabilitas skenario: Base 50% · Bull 25% · Bear 25%. EV = Σ p × skor outlook.

| # | Sektor | Base | Bull | Bear | **EV** | Prediksi (Base) | Peran portofolio | Penanda pakar |
|---|---|---|---|---|---|---|---|---|
| 1 | Barang Baku | 10 | 16 | 3 | **9.75** | BULLISH MODERAT | **INTI (core)** | RobustLintasSkenario, KeyakinanTinggi, PresedenHistoris, DiuntungkanGeopolitik |
| 2 | Kesehatan | 9 | 9 | 7 | **8.50** | BULLISH MODERAT | **INTI (core)** | RobustLintasSkenario, DiuntungkanGeopolitik, PerluPemantauanKetat |
| 3 | Infrastruktur | 6 | 20 | -1 | **7.75** | NETRAL | **SATELIT** | AsimetriPositif |
| 4 | Barang Konsumen Primer | 6 | 12 | 1 | **6.25** | NETRAL | kontrarian (pantau) | DiuntungkanGeopolitik |
| 5 | Perindustrian | 4 | 14 | -1 | **5.25** | NETRAL |  | AsimetriPositif |
| 6 | Energi | 6 | 2 | 4 | **4.50** | NETRAL |  | PresedenHistoris, DiuntungkanGeopolitik, KatalisDekat |
| 7 | Keuangan | -1 | 18 | -11 | **1.25** | BEARISH | kontrarian (pantau) | PresedenHistoris, KatalisDekat |
| 8 | Properti & Real Estat | -2 | 14 | -9 | **0.25** | BEARISH |  | KatalisDekat |
| 9 | Teknologi | -5 | 15 | -14 | **-2.25** | BEARISH |  | KatalisDekat |
| 10 | Transportasi & Logistik | -5 | 10 | -13 | **-3.25** | BEARISH |  | DiuntungkanGeopolitik |
| 11 | Barang Konsumen Non-Primer | -7 | 12 | -17 | **-4.75** | BEARISH |  |  |

### 4.1 Jalur penalaran multi-hop (sektor inti & satelit)

#### Sektor Barang Baku — INTI (core)

**Tailwind:**

- Tekanan Rupiah (~Rp17.900/USD) → Rupiah Melemah → Pendapatan Eksportir (USD) Naik dalam Rupiah *(provenans global/geopolitik)*
- Kebijakan Hilirisasi & Kuota RKAB Nikel → Harga Nikel Tertopang Kuota
- Harga Emas Tinggi (~US$4.390, Sep 2026) → Permintaan Safe Haven Emas *(provenans global/geopolitik)*

**Tema struktural:** Hilirisasi Nikel & Mineral; Emas Safe Haven & Bank Sentral

**Preseden historis (CBR):** Supercycle Komoditas & Perang Rusia-Ukraina 2022

**Tesis & kill switch:** Tesis: Emas & nikel menopang Barang Baku — indikator Harga Emas Spot = 4,390.11; status: PerluDataBaru, Valid.

#### Sektor Kesehatan — INTI (core)

**Tailwind:**

- Penutupan Selat Hormuz & Berakhirnya Gencatan (8 Jul 2026) → Premi Risiko Timur Tengah Naik → Risk-off Global *(provenans global/geopolitik)*

**Headwind:**

- Tekanan Rupiah (~Rp17.900/USD) → Rupiah Melemah → Biaya Bahan Baku Impor Naik

**Tema struktural:** Belanja Kesehatan & JKN

**Tesis & kill switch:** Tesis: Kesehatan defensif — indikator Kurs USD/IDR = 17,938.00; status: PerluDataBaru, Rapuh, Valid.

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

**Tesis & kill switch:** Tesis kontrarian: Infrastruktur digital — indikator Yield SBN 10Y = 7.14; status: PerluDataBaru, Valid.

## 5. Top-3 Emiten per Sektor Inti/Satelit — Analis Biasa vs Sistem Pakar

*Skor statis* = penjumlahan pilar berbobot sama (cara analis biasa). *Skor adaptif* = bobot regime krisis + smart money + kontribusi sektor berbasis EV.

**Sektor Barang Baku**

| Rank | Emiten | Skor statis | **Skor adaptif** | Konfluensi | RS vs IHSG | ERP | Pos. maks | Status pakar | Catatan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **ANTM** — Aneka Tambang | 28 | **33.5** | 5/6 | 15.0 pp | 2.9 pp | 7.1% | TOP PICK ADAPTIF | RisikoKonsentrasiTema, StrategiTrancheKatalisBiner, RisikoOutflowPasif |
| 2 | **TINS** — Timah | 25 | **28.0** | 6/6 | 13.0 pp | 5.4 pp | 6.2% | TOP PICK ADAPTIF | ZonaAbuAbu |
| 3 | **NCKL** — Trimegah Bangun Persada | 21 | **24.5** | 4/6 | 9.0 pp | 8.2 pp | 7.3% | - | CelahEkspektasiPositif, RisikoHSC, ERPSangatMenarik |

**Sektor Kesehatan**

| Rank | Emiten | Skor statis | **Skor adaptif** | Konfluensi | RS vs IHSG | ERP | Pos. maks | Status pakar | Catatan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **MIKA** — Mitra Keluarga Karyasehat | 21 | **27.5** | 4/6 | 7.0 pp | -3.0 pp | 10.0% | TOP PICK ADAPTIF · AKUMULASI BERTAHAP | MahalVsObligasi |
| 2 | **HEAL** — Medikaloka Hermina | 20 | **26.0** | 4/6 | 9.0 pp | -3.1 pp | 8.6% | TOP PICK ADAPTIF · AKUMULASI BERTAHAP | CelahEkspektasiPositif, MahalVsObligasi |
| 3 | **KLBF** — Kalbe Farma | 19 | **24.5** | 3/6 | 5.0 pp | -0.5 pp | 9.6% | watchlist | MahalVsObligasi, RisikoOutflowPasif |

**Sektor Infrastruktur**

| Rank | Emiten | Skor statis | **Skor adaptif** | Konfluensi | RS vs IHSG | ERP | Pos. maks | Status pakar | Catatan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **ISAT** — Indosat Ooredoo Hutchison | 16 | **21.5** | 3/6 | 3.0 pp | 4.0 pp | 7.3% | - | ZonaAbuAbu, RisikoOutflowPasif |
| 2 | **TLKM** — Telkom Indonesia | 11 | **19.0** | 3/6 | 0.0 pp | 4.0 pp | 8.3% | - | ZonaAbuAbu, RisikoOutflowPasif |
| 3 | **TOWR** — Sarana Menara Nusantara | 11 | **16.5** | 2/6 | 1.0 pp | 8.2 pp | 7.6% | - | ERPSangatMenarik, ZonaAbuAbu |

### 5.1 Di mana sistem pakar berbeda dari analis biasa

- **Hanya dipilih analis biasa (skor statis) — dibuang sistem pakar:**
  - **BRMS**: skor adaptif 24.5 < ambang 24.7; tanpa jejak smart money; ERP negatif (kalah dari SBN); kekuatannya dominan dari teknikal (bobot 0,5 di regime krisis)
  - **NCKL**: skor adaptif 24.5 < ambang 24.7; tanpa jejak smart money; risiko HSC/free float < 15%
  - **SIDO**: skor adaptif 24.5 < ambang 24.7; tanpa jejak smart money
- **Hanya dipilih sistem pakar:**
  - **AADI** (statis 23 → adaptif 27.5): fundamental 8/10; jejak smart money; ERP 17.9 pp; sektor EV 4.50
  - **CPIN** (statis 18 → adaptif 26.0): fundamental 8/10; jejak smart money; kualitas terpukul (akumulasi bertahap); sektor EV 6.25
  - **DSNG** (statis 21 → adaptif 25.5): fundamental 9/10; ERP 8.2 pp; sektor EV 6.25
  - **HEAL** (statis 20 → adaptif 26.0): fundamental 8/10; jejak smart money; kualitas terpukul (akumulasi bertahap); sektor EV 8.50
  - **JPFA** (statis 21 → adaptif 27.5): fundamental 8/10; jejak smart money; ERP 9.5 pp; sektor EV 6.25
  - **LSIP** (statis 22 → adaptif 29.0): fundamental 9/10; jejak smart money; ERP 8.2 pp; sektor EV 6.25
  - **UNTR** (statis 19 → adaptif 25.0): fundamental 8/10; jejak smart money; ERP 15.1 pp; kualitas terpukul (akumulasi bertahap); sektor EV 5.25
- **Disepakati keduanya:** ANTM, MIKA, TINS.

## 6. Rencana Akumulasi Bertahap (kapitulasi)

Regime Krisis Likuiditas / Kapitulasi: porsi tranche 30% / 30% / 40% dari alokasi; tangga harga T1 = harga, T2 = −2×ATR, T3 = −4×ATR.

| Emiten | Sektor | T1 | T2 | T3 | Pos. maks | Pemicu | Katalis biner dekat |
|---|---|---|---|---|---|---|---|
| **MIKA** | Kesehatan | 2,100 | 1,995 | 1,890 | 10.0% | AkumulasiBandar, AkumulasiTersembunyi | - |
| **CPIN** | KonsumenPrimer | 4,100 | 3,870 | 3,641 | 8.9% | AkumulasiBandar, AkumulasiTersembunyi, CelahEkspektasiPositif | - |
| **HEAL** | Kesehatan | 1,250 | 1,178 | 1,105 | 8.6% | AkumulasiBandar, AkumulasiTersembunyi, CelahEkspektasiPositif | - |
| **UNTR** | Perindustrian | 20,000 | 18,920 | 17,840 | 9.3% | AkumulasiBandar, AkumulasiTersembunyi | MSCI Index Review Nov 2026 (umum 11 Nov) |
| **BBCA** | Keuangan | 6,200 | 5,828 | 5,456 | 8.3% | KapitulasiEmiten, AkumulasiBandar, AkumulasiTersembunyi | FOMC 28 Okt 2026; FOMC 9 Des 2026; MSCI Index Review Nov 2026 (umum 11 Nov) |
| **BMRI** | Keuangan | 3,600 | 3,348 | 3,096 | 7.1% | KapitulasiEmiten | FOMC 28 Okt 2026; FOMC 9 Des 2026; MSCI Index Review Nov 2026 (umum 11 Nov) |

## 7. Konfluensi, Konflik, Refleksivitas & Ekspektasi Laba

- **Konfluensi tinggi (≥5/6 pilar):** AADI, AALI, ANTM, BRMS, DSNG, JPFA, LSIP, TINS
- **Tunggu konfirmasi (konflik sinyal):** AADI
- **Fundamental kuat vs bandar distribusi:** -
- **Distribusi saat euforia:** -
- **Berita buruk priced-in:** -
- **Sell the news:** -
- **Mengungguli IHSG ≥5 pp:** AADI, AALI, ANTM, AUTO, BRMS, CPIN, DCII, DMAS, DSNG, HEAL, IMPC, INCO, INDF, ITMG, JPFA, KLBF, LSIP, MDKA, MEDC, MIKA, MTDL, NCKL, PTBA, SIDO, SILO, SMDR, TINS, TMAS, UNTR
- **Kapitulasi emiten:** BBCA, BBRI, BMRI
- **Celah ekspektasi positif (revisi naik, harga tertinggal):** AMMN, CPIN, HEAL, NCKL
- **Murah karena laba turun (value-trap dini):** AADI, ACES, BBNI, BBRI, BMRI, BSDE, CTRA, DMAS, MAPI, MYOR, PTBA, SMRA, UNVR
- **ERP ≥ 8 pp (murah vs SBN):** AADI, ASII, AUTO, BBNI, BBTN, BMRI, BSDE, CTRA, DMAS, DSNG, ERAA, INDF, INKP, ITMG, JPFA, JSMR, LSIP, MEDC, NCKL, PGAS, PTBA, SMDR, SMRA, TMAS, TOWR, UNTR
- **Mahal vs obligasi (ERP < 0):** AMMN, AMRT, BRMS, BUKA, CPIN, DCII, EMTK, EXCL, HEAL, IMPC, INCO, KLBF, MDKA, MIKA, MTEL, MYOR, SILO, SMGR
- **Risiko konsentrasi tema:** AADI, ANTM, DSNG, LSIP, UNTR

## 8. Kalender Katalis

| Katalis | Tanggal | H- | Tipe | ≤45 hari |
|---|---|---|---|---|
| FOMC 28 Okt 2026 | 2026-10-28 | 2 | Biner | ✅ |
| Batas rilis laporan keuangan Q3-2026 (≈31 Okt) | 2026-10-31 | 5 | Terjadwal | ✅ |
| Pemilu Sela AS 3 Nov 2026 | 2026-11-03 | 8 | Biner | ✅ |
| MSCI Index Review Nov 2026 (umum 11 Nov) | 2026-11-11 | 16 | Biner | ✅ |
| Efektif MSCI Review (1 Des 2026) | 2026-12-01 | 36 | Terjadwal | ✅ |
| FOMC 9 Des 2026 | 2026-12-09 | 44 | Biner | ✅ |
| Window dressing akhir tahun (≈pertengahan Des) | 2026-12-15 | 50 | Musiman |  |
| Evaluasi mayor LQ45 (≈akhir Jan 2027) | 2027-01-25 | 91 | Terjadwal |  |
| Ramadan-Lebaran 2027 (≈Feb-Mar) | 2027-02-08 | 105 | Musiman |  |
| MSCI Index Review Feb 2027 (umum 9 Feb) | 2027-02-09 | 106 | Biner |  |
| Musim RUPS & dividen (≈Mar-Jun 2027) | 2027-03-15 | 140 | Musiman |  |
| Batas akhir konsultasi MSCI (30 Apr 2027) | 2027-04-30 | 186 | Biner |  |
| Keputusan final MSCI standalone (≈akhir Jun 2027) | 2027-06-30 | 247 | Biner |  |

Strategi tranche sebelum katalis biner: AADI, ANTM, BBCA, BMRI, UNTR.

## 9. Tesis Investasi & Kill Switch

| Tesis | Indikator kunci | Nilai | Batas bawah | Batas atas | Pemicu kontrarian | Buffer | Status |
|---|---|---|---|---|---|---|---|
| Tesis: Emas & nikel menopang Barang Baku | Harga Emas Spot | 4,390.11 | 3,800.00 | - | - | 13.4% | PerluDataBaru, Valid |
| Tesis: Premi geopolitik minyak | Harga Brent | 106.65 | 75.00 | - | - | 29.7% | PerluDataBaru, Valid |
| Tesis: Kesehatan defensif | Kurs USD/IDR | 17,938.00 | - | 19,500.00 | - | 8.7% | PerluDataBaru, Rapuh, Valid |
| Tesis kontrarian: Big banks pasca-kapitulasi | CDS Indonesia 5Y | 99.73 | - | 150.00 | 85.00 | 50.4% | Valid |
| Tesis kontrarian: Infrastruktur digital | Yield SBN 10Y | 7.14 | - | 8.00 | 6.75 | 12.0% | PerluDataBaru, Valid |
| Tesis: Konsumen primer (MBG & CPO) | Inflasi Indonesia (yoy) | 3.28 | - | 5.00 | - | 52.4% | Valid |

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
| LSIP | SinyalEntry, SinyalBuyOnWeakness | 1,050 | 987 | 1,144 | 8.3% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| TINS | SinyalEntry | 1,900 | 1,748 | 2,128 | 6.2% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| AADI | SinyalEntry, SinyalBuyOnWeakness | 5,400 | 5,054 | 5,918 | 7.8% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, TungguKonfirmasi |
| JPFA | SinyalEntry, SinyalBuyOnWeakness | 1,600 | 1,491 | 1,763 | 7.3% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| MIKA | SinyalBuyOnWeakness | 2,100 | 1,995 | 2,258 | 10.0% | AkumulasiInstitusiAsing, AkumulasiTersembunyi |
| CPIN | SinyalBuyOnWeakness | 4,100 | 3,870 | 4,444 | 8.9% | AkumulasiInstitusiAsing, AkumulasiTersembunyi |
| HEAL | SinyalBuyOnWeakness | 1,250 | 1,178 | 1,359 | 8.6% | AkumulasiInstitusiAsing, AkumulasiTersembunyi |
| DSNG | SinyalEntry | 850 | 796 | 932 | 7.8% | FaseMarkUpWyckoff |
| UNTR | SinyalBuyOnWeakness | 20,000 | 18,920 | 21,620 | 9.3% | AkumulasiInstitusiAsing, AkumulasiTersembunyi |
| BRMS | SinyalScalpingLong | 430 | - | - | 4.8% | FaseMarkUpWyckoff, LonjakanVolume |
| IMPC | SinyalEntry | 1,900 | 1,763 | 2,105 | 6.9% | FaseMarkUpWyckoff |
| AALI | SinyalEntry | 6,000 | 5,688 | 6,468 | 9.6% | FaseMarkUpWyckoff |
| MEDC | SinyalEntry | 1,150 | 1,063 | 1,281 | 6.6% | AkumulasiInstitusiAsing, AkumulasiTersembunyi, FaseMarkUpWyckoff |
| BBCA | SinyalBuyOnWeakness | 6,200 | 5,828 | 6,758 | 8.3% | AkumulasiTersembunyi |
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

- **Indikator makro kedaluwarsa (umur > 5× frekuensi):** Makro_Brent, Makro_Emas, Makro_IHSG, Makro_NetAsingYTD, Makro_SpreadSBN_UST, Makro_USDIDR, Makro_UST10Y, Makro_WTI, Makro_YieldSBN10Y
- **Tesis perlu data baru:** Tesis: Emas & nikel menopang Barang Baku, Tesis: Premi geopolitik minyak, Tesis: Kesehatan defensif, Tesis kontrarian: Infrastruktur digital
- **Rekomendasi yang wajib diverifikasi (PerluVerifikasiData):** AADI, ANTM, BBCA, BMRI, CPIN, DSNG, HEAL, JPFA, LSIP, MIKA, TINS, UNTR

## 14. Rekomendasi per Persona

- **Mahasiswa Konservatif**: AADI, BBCA, BMRI, JPFA, UNTR
- **PekerjaMuda Moderat**: AADI, ANTM, BRMS, DSNG, HEAL, JPFA, LSIP, MIKA, NCKL, SIDO, SILO, TINS
- **GenZ Agresif**: AADI, AALI, ANTM, DSNG, IMPC, JPFA, LSIP, MDKA, MEDC, TINS
- **TraderScalper**: BRMS, MDKA

## 15. Rasio Knowledge Base vs Reasoning

| Komponen | Aksioma | Porsi |
|---|---|---|
| Knowledge Base (TBox + ABox + anotasi + deklarasi) | 14,886 | **98.0%** |
| Reasoning (aturan SWRL) | 303 | 2.0% |
| **Total** | 15,189 | 100% |

Aksioma logis saja: KB 8,571 vs aturan 303 → **96.6% KB**.

**303 aturan SWRL per pilar:** Fundamental (30), Regime Pasar (24), Teknikal (16), Konfluensi (15), Integrasi (14), Bandarmology (13), Sentimen (13), Geopolitik (11), Fundamental-Risiko (10), Quant Trade (10), Tesis & Invalidasi (10), Fundamental-Valuasi (8), Tata Kelola (8), Prediksi Sektor (7), Robustness Skenario (7), Stakeholder (6), Struktur Pasar (6), Katalis (6), Fundamental-Sektor (5), Rotasi Sektor (5), Reaction Function (5), Refleksivitas (5), Adaptif Regime (5), Teknikal-Pola (4), Bandarmology-Wyckoff (4), Geopolitik→Emiten (4), Bandarmology-Sektor (4), Kualitas Data (4), Kapitulasi (4), Ekspektasi Laba (4), Valuasi Relatif Obligasi (4), Konflik Sinyal (4), Skenario (3), Makro-Geopolitik (3), Case-Based Reasoning (3), Likuiditas (3), Profil Investor (3), Bandarmology-Broker (2), Tema Struktural (2), Scalper Pattern (2), Intermarket (2), Konstruksi Portofolio (2), Manajemen Posisi (2), Peringatan (1).
