# -*- coding: utf-8 -*-
"""
TBox (taksonomi kelas) untuk Sistem Pakar Prediksi Sektor Saham BEI.
Format tiap baris:  NamaKelas | Induk | Label (id) | Definisi (rdfs:comment)
Induk "Thing" = owl:Thing.
"""

TAXONOMY = r"""
# ======================= LAPISAN AKAR =======================
EntitasPasarModal | Thing | Entitas Pasar Modal | Semua entitas nyata di pasar modal: emiten, sektor, indeks, broker, institusi, komoditas.
PengetahuanDasarSaham | Thing | Pengetahuan Dasar Saham (Basic Layer) | Lapisan ilmu dasar yang wajib dikuasai investor: konsep, mekanisme, aksi korporasi, gaya investasi, manajemen risiko.
AnalisisFundamental | Thing | Analisis Fundamental | Pilar analisis nilai intrinsik perusahaan berbasis laporan keuangan, rasio, dan valuasi.
AnalisisTeknikal | Thing | Analisis Teknikal | Pilar analisis pergerakan harga & volume (indikator, pola chart, candlestick).
Bandarmology | Thing | Bandarmology | Pilar analisis jejak pemodal besar (bandar/asing/institusi) via broker summary, foreign flow, dan order book.
AnalisisSentimen | Thing | Analisis Sentimen | Pilar interpretasi berita, riset, media sosial, dan aksi korporasi menjadi sinyal sentimen sektoral/emiten.
AnalisisGeopolitikMakro | Thing | Analisis Geopolitik & Makro | Pilar pakar: transmisi peristiwa geopolitik, kebijakan moneter, dan komoditas ke arah dana asing & sektor.
PenalaranPakar | Thing | Penalaran Pakar | Struktur penalaran: skenario, penilaian sektor, kasus historis (CBR), siklus ekonomi, tema struktural.
Stakeholder | Thing | Stakeholder | Pihak yang berkepentingan terhadap sistem pakar (mitra, pengguna, validator, regulator).
KeluaranSistem | Thing | Keluaran Sistem | Jenis output yang dihasilkan sistem pakar.
KategoriInferensi | Thing | Kategori Hasil Inferensi | Kelas-kelas yang keanggotaannya diturunkan oleh aturan SWRL (bukan diisi manual).
TujuanSDG | Thing | Tujuan Pembangunan Berkelanjutan (SDG) | Target SDGs yang didukung keluaran sistem.

# ======================= ENTITAS PASAR =======================
Emiten | EntitasPasarModal | Emiten | Perusahaan tercatat (listed company) di Bursa Efek Indonesia.
EmitenPerbankan | Emiten | Emiten Perbankan | Emiten bank; dinilai dengan rasio khusus perbankan (NPL, CAR, NIM, LDR).
EmitenNonKeuangan | Emiten | Emiten Non-Keuangan | Emiten selain bank; dinilai dengan DER, margin, Altman Z-Score.
EmitenBUMN | Emiten | Emiten BUMN | Emiten yang mayoritas sahamnya dimiliki negara (kini di bawah koordinasi Danantara).
EmitenSyariah | Emiten | Emiten Syariah | Emiten yang masuk Daftar Efek Syariah (DES) OJK.
Sektor | EntitasPasarModal | Sektor IDX-IC | Klasifikasi sektor menurut IDX Industrial Classification (IDX-IC), 11 sektor.
SektorDefensif | Sektor | Sektor Defensif | Sektor yang permintaannya stabil di segala siklus (konsumer primer, kesehatan, infrastruktur telko).
SektorSiklikal | Sektor | Sektor Siklikal | Sektor yang sangat bergantung siklus ekonomi & suku bunga.
SektorKomoditas | Sektor | Sektor Berbasis Komoditas | Sektor yang labanya ditentukan harga komoditas global.
Subsektor | EntitasPasarModal | Subsektor / Industri | Turunan sektor IDX-IC (mis. batu bara, bank, telekomunikasi).
KonglomerasiGrup | EntitasPasarModal | Grup Konglomerasi | Grup usaha pengendali beberapa emiten (afiliasi).
IndeksSaham | EntitasPasarModal | Indeks Saham | Ukuran statistik pergerakan harga sekumpulan saham.
IndeksDomestik | IndeksSaham | Indeks Domestik (BEI) | Indeks yang diterbitkan Bursa Efek Indonesia.
IndeksKomposit | IndeksDomestik | Indeks Komposit | Indeks seluruh saham tercatat (IHSG).
IndeksLikuiditas | IndeksDomestik | Indeks Likuiditas & Kapitalisasi | Indeks saham paling likuid & berkapitalisasi besar (LQ45, IDX30, IDX80, Kompas100).
IndeksSektoralBEI | IndeksDomestik | Indeks Sektoral BEI | Indeks 11 sektor IDX-IC.
IndeksTematik | IndeksDomestik | Indeks Tematik/Faktor | Indeks berbasis faktor (value, growth, quality, dividen, BUMN).
IndeksSyariah | IndeksDomestik | Indeks Syariah | Indeks saham syariah (JII, ISSI, JII70).
IndeksESG | IndeksDomestik | Indeks ESG | Indeks berbasis kinerja lingkungan, sosial, tata kelola.
IndeksGlobal | IndeksSaham | Indeks Global | Indeks bursa luar negeri dan indeks penyedia global.
IndeksAmerika | IndeksGlobal | Indeks Amerika Serikat | NASDAQ, S&P 500, Dow Jones, Russell 2000, dll.
IndeksEropa | IndeksGlobal | Indeks Eropa | FTSE 100, DAX, CAC 40, Euro Stoxx 50.
IndeksAsiaPasifik | IndeksGlobal | Indeks Asia-Pasifik | Nikkei, Hang Seng, Shanghai, KOSPI, STI, dll.
IndeksMSCI | IndeksGlobal | Indeks MSCI | Keluarga indeks MSCI Inc. yang menjadi acuan dana pasif global.
IndeksFTSERussell | IndeksGlobal | Indeks FTSE Russell | Keluarga indeks FTSE Russell (LSEG).
IndeksSPDowJones | IndeksGlobal | Indeks S&P Dow Jones | Keluarga indeks S&P Dow Jones Indices.
IndikatorRisikoGlobal | IndeksGlobal | Indikator Risiko Global | Indeks volatilitas & dolar (VIX, DXY).
PenyediaIndeks | EntitasPasarModal | Penyedia Indeks | Lembaga penerbit indeks (MSCI, FTSE Russell, S&P DJI, BEI, Nasdaq Inc).
Broker | EntitasPasarModal | Broker / Anggota Bursa | Perusahaan efek anggota bursa, diidentifikasi kode 2 huruf.
BrokerAsing | Broker | Broker Asing | Broker afiliasi asing; jejaknya mencerminkan dana institusi global.
BrokerLokal | Broker | Broker Lokal | Broker domestik.
BrokerRitel | BrokerLokal | Broker Ritel | Broker dengan basis nasabah ritel dominan; net buy masif dari broker ritel sering jadi tanda distribusi.
BrokerInstitusiLokal | BrokerLokal | Broker Institusi Lokal | Broker domestik yang melayani dana pensiun, asuransi, MI.
Institusi | EntitasPasarModal | Institusi / Otoritas | Regulator, bank sentral, SRO, lembaga statistik, organisasi internasional.
Regulator | Institusi | Regulator | Otoritas pengatur (OJK).
SelfRegulatoryOrganization | Institusi | SRO | BEI, KSEI, KPEI.
BankSentral | Institusi | Bank Sentral | Bank Indonesia, The Federal Reserve, ECB, BoJ, PBoC.
OrganisasiInternasional | Institusi | Organisasi Internasional | OPEC+, IMF, Bank Dunia, lembaga pemeringkat.
LembagaPemeringkat | OrganisasiInternasional | Lembaga Pemeringkat | S&P, Moody's, Fitch.
Komoditas | EntitasPasarModal | Komoditas | Barang komoditas global yang memengaruhi laba emiten.
KomoditasEnergi | Komoditas | Komoditas Energi | Minyak (WTI, Brent), gas/LNG, batu bara.
KomoditasLogam | Komoditas | Komoditas Logam Industri | Nikel, timah, tembaga, bauksit, aluminium.
LogamMulia | Komoditas | Logam Mulia | Emas dan perak (aset safe haven).
KomoditasAgrikultur | Komoditas | Komoditas Agrikultur | CPO, karet, gandum, jagung, kedelai.
PapanPencatatan | EntitasPasarModal | Papan Pencatatan | Papan Utama, Pengembangan, Akselerasi, Ekonomi Baru, Pemantauan Khusus.

# ======================= PENGETAHUAN DASAR =======================
InstrumenPasarModal | PengetahuanDasarSaham | Instrumen Pasar Modal | Jenis efek yang diperdagangkan.
MekanismePerdagangan | PengetahuanDasarSaham | Mekanisme Perdagangan | Aturan main transaksi di BEI.
AksiKorporasi | PengetahuanDasarSaham | Aksi Korporasi | Tindakan emiten yang memengaruhi jumlah saham, harga, atau hak pemegang saham.
AksiKorporasiPositif | AksiKorporasi | Aksi Korporasi Umumnya Positif | Aksi yang umumnya dipersepsi positif (dividen, buyback, stock split).
AksiKorporasiNegatif | AksiKorporasi | Aksi Korporasi Berpotensi Negatif | Aksi yang berpotensi dilutif/negatif (right issue utk bayar utang, private placement diskon, reverse split).
AksiKorporasiNetral | AksiKorporasi | Aksi Korporasi Netral/Kontekstual | Dampaknya bergantung konteks (merger, akuisisi, tender offer).
StatusPengawasan | PengetahuanDasarSaham | Status Pengawasan Bursa | Mekanisme pengawasan: suspensi, UMA, notasi khusus, FCA.
BiayaDanPajak | PengetahuanDasarSaham | Biaya & Pajak Transaksi | Komponen biaya dan pajak investasi saham.
GayaInvestasi | PengetahuanDasarSaham | Gaya Investasi / Trading | Strategi dan horizon investasi.
ManajemenRisiko | PengetahuanDasarSaham | Manajemen Risiko | Teknik mengendalikan kerugian dan ukuran posisi.
BiasPerilaku | PengetahuanDasarSaham | Bias Perilaku (Behavioral Finance) | Kesalahan psikologis investor yang dieksploitasi bandar.
SiklusPasar | PengetahuanDasarSaham | Siklus/Fase Pasar | Fase pasar (bull, bear, sideways) dan fase Wyckoff.
FaseWyckoff | SiklusPasar | Fase Wyckoff | Akumulasi, Mark-up, Distribusi, Mark-down (Richard Wyckoff).
ProfilRisiko | PengetahuanDasarSaham | Profil Risiko Investor | Konservatif, Moderat, Agresif.
HorizonInvestasi | PengetahuanDasarSaham | Horizon Investasi | Jangka waktu investasi (intraday s.d. >3 tahun).

# ======================= FUNDAMENTAL =======================
LaporanKeuangan | AnalisisFundamental | Laporan Keuangan | Neraca, laba rugi, arus kas, perubahan ekuitas, CALK.
RasioKeuangan | AnalisisFundamental | Rasio Keuangan | Rasio untuk menilai kinerja dan kesehatan emiten.
RasioValuasi | RasioKeuangan | Rasio Valuasi | Mengukur mahal/murahnya harga saham relatif terhadap fundamental.
RasioProfitabilitas | RasioKeuangan | Rasio Profitabilitas | Mengukur kemampuan menghasilkan laba.
RasioSolvabilitas | RasioKeuangan | Rasio Solvabilitas/Leverage | Mengukur struktur utang dan kemampuan bayar jangka panjang.
RasioLikuiditas | RasioKeuangan | Rasio Likuiditas | Mengukur kemampuan bayar kewajiban jangka pendek.
RasioEfisiensi | RasioKeuangan | Rasio Aktivitas/Efisiensi | Mengukur efisiensi pemakaian aset.
RasioPertumbuhan | RasioKeuangan | Rasio Pertumbuhan | Pertumbuhan pendapatan, laba, EPS.
RasioDividen | RasioKeuangan | Rasio Dividen | Kebijakan & imbal hasil dividen.
RasioPerbankan | RasioKeuangan | Rasio Khusus Perbankan | NPL, CAR, NIM, LDR, CASA, BOPO, CoC.
RasioArusKas | RasioKeuangan | Rasio Arus Kas & Kualitas Laba | FCF, CFO/Laba bersih.
ModelSkorRisiko | AnalisisFundamental | Model Skor Risiko | Model prediksi kebangkrutan/manipulasi (Altman Z, Piotroski F, Beneish M).
MetodeValuasi | AnalisisFundamental | Metode Valuasi | DCF, DDM, relatif, NAV, SOTP, Graham.
MetrikIndustriSpesifik | AnalisisFundamental | Metrik Industri Spesifik | Metrik khusus sektor (strip ratio, ARPU, marketing sales, SSSG).

# ======================= TEKNIKAL =======================
IndikatorTeknikal | AnalisisTeknikal | Indikator Teknikal | Alat bantu matematis atas harga/volume.
IndikatorTren | IndikatorTeknikal | Indikator Tren | MA, EMA, MACD, ADX, Ichimoku, Parabolic SAR.
IndikatorMomentum | IndikatorTeknikal | Indikator Momentum (Osilator) | RSI, Stochastic, CCI, Williams %R.
IndikatorVolatilitas | IndikatorTeknikal | Indikator Volatilitas | Bollinger Bands, ATR, Keltner Channel.
IndikatorVolume | IndikatorTeknikal | Indikator Volume | OBV, VWAP, MFI, Accumulation/Distribution, Volume Profile.
PolaChart | AnalisisTeknikal | Pola Chart | Formasi harga berulang pada grafik.
PolaBullish | PolaChart | Pola Chart Bullish | Pola yang mengindikasikan potensi kenaikan.
PolaBearish | PolaChart | Pola Chart Bearish | Pola yang mengindikasikan potensi penurunan.
PolaReversal | PolaChart | Pola Pembalikan (Reversal) | Pola pembalikan tren.
PolaKontinuasi | PolaChart | Pola Kelanjutan (Continuation) | Pola kelanjutan tren.
PolaCandlestick | AnalisisTeknikal | Pola Candlestick | Pola lilin Jepang 1-3 batang.
CandlestickBullish | PolaCandlestick | Candlestick Bullish | Sinyal pembalikan/kelanjutan naik.
CandlestickBearish | PolaCandlestick | Candlestick Bearish | Sinyal pembalikan/kelanjutan turun.
CandlestickIndecision | PolaCandlestick | Candlestick Ragu (Indecision) | Keseimbangan pembeli-penjual.
KonsepTeknikal | AnalisisTeknikal | Konsep Teknikal | Support, resistance, trendline, breakout, gap, divergence, dll.
TeoriTeknikal | AnalisisTeknikal | Teori Teknikal | Dow Theory, Elliott Wave, Fibonacci, Wyckoff.

# ======================= BANDARMOLOGY =======================
KonsepBandarmology | Bandarmology | Konsep Bandarmology | Alat baca jejak bandar: broker summary, foreign flow, done detail, order book.
PolaBandar | Bandarmology | Pola Bandar | Pola perilaku pemodal besar.
PolaBandarBullish | PolaBandar | Pola Bandar Bullish | Akumulasi, spring, shakeout, mark-up.
PolaBandarBearish | PolaBandar | Pola Bandar Bearish | Distribusi, UTAD, mark-down, pump & dump.
PolaManipulatif | PolaBandar | Pola Manipulatif (Dilarang) | Praktik yang melanggar UU Pasar Modal (wash trade, spoofing, cornering).
PolaScalper | Bandarmology | Pola Scalper/Intraday | Pola entry-exit intraday yang dipakai scalper berpengalaman.

# ======================= SENTIMEN =======================
SumberSentimen | AnalisisSentimen | Sumber Sentimen | Asal informasi sentimen.
KategoriSentimen | AnalisisSentimen | Kategori Sentimen | Positif, Netral, Negatif.
Berita | AnalisisSentimen | Berita / Item Informasi | Item berita finansial yang di-skor sentimennya (input komponen ML <20%).
BeritaMakroGeopolitik | Berita | Berita Makro & Geopolitik | Berita kebijakan moneter, perang, komoditas, indeks global.
BeritaEmiten | Berita | Berita Emiten | Berita spesifik perusahaan/aksi korporasi.
BeritaRisetAnalis | Berita | Laporan/Rekomendasi Analis | Rekomendasi & target harga sekuritas.
KomponenML | AnalisisSentimen | Komponen ML Pendukung | Modul non-simbolik (<20%): scoring sentimen teks, deteksi pola chart, kalibrasi bobot backtest.

# ======================= GEOPOLITIK & MAKRO =======================
IndikatorMakro | AnalisisGeopolitikMakro | Indikator Makro & Global | Variabel makro terukur (suku bunga, kurs, inflasi, harga komoditas).
IndikatorMoneter | IndikatorMakro | Indikator Moneter | Fed Funds Rate, BI Rate, yield obligasi.
IndikatorNilaiTukar | IndikatorMakro | Indikator Nilai Tukar | USD/IDR, DXY.
IndikatorEkonomiRiil | IndikatorMakro | Indikator Ekonomi Riil | PDB, inflasi, neraca dagang, cadangan devisa, PMI.
IndikatorHargaKomoditas | IndikatorMakro | Indikator Harga Komoditas | Harga minyak, emas, batu bara, CPO, nikel.
IndikatorAliranDana | IndikatorMakro | Indikator Aliran Dana | Net buy/sell asing, level indeks.
PeristiwaGeopolitik | AnalisisGeopolitikMakro | Peristiwa Geopolitik & Kebijakan | Peristiwa yang memicu transmisi makro.
KonflikPerang | PeristiwaGeopolitik | Konflik / Perang | Konflik bersenjata antarnegara.
KebijakanMoneter | PeristiwaGeopolitik | Keputusan Kebijakan Moneter | Keputusan The Fed (FOMC), BI (RDG), bank sentral lain.
KebijakanDagangTarif | PeristiwaGeopolitik | Kebijakan Dagang & Tarif | Tarif, sanksi, perang dagang.
KeputusanOPEC | PeristiwaGeopolitik | Keputusan OPEC+ | Keputusan kuota produksi minyak.
KrisisEkonomi | PeristiwaGeopolitik | Krisis Ekonomi/Keuangan | Krisis inflasi, krisis pasar modal, krisis nilai tukar.
KebijakanDomestik | PeristiwaGeopolitik | Kebijakan Domestik Indonesia | Program pemerintah, regulasi OJK/BEI, fiskal.
KeputusanPenyediaIndeks | PeristiwaGeopolitik | Keputusan Penyedia Indeks | Keputusan MSCI/FTSE/S&P DJI (rebalancing, freeze, reklasifikasi).
PemiluPolitik | PeristiwaGeopolitik | Pemilu & Politik | Pemilu negara besar.
GencatanDeeskalasi | PeristiwaGeopolitik | Gencatan Senjata / De-eskalasi | Peristiwa yang menurunkan premi risiko.
PeristiwaGlobal | PeristiwaGeopolitik | Peristiwa Global (Lintas Negara) | Peristiwa yang berasal dari luar negeri/antarnegara: perang, The Fed, OPEC+, tarif, penyedia indeks global.
PeristiwaAktif | KategoriInferensi | Peristiwa Aktif | (Inferensi) peristiwa yang dikonfirmasi berita kredibel & masih relevan (≤180 hari).
PergerakanMakro | AnalisisGeopolitikMakro | Pergerakan Makro (Node Transmisi) | Node rantai kausal multi-hop: perubahan arah variabel makro.
PergerakanGeopolitik | PergerakanMakro | Pergerakan Berbasis Geopolitik | Pergerakan yang berakar dari konflik/kebijakan antarnegara.
PergerakanAktif | KategoriInferensi | Pergerakan Makro Aktif | (Inferensi) node transmisi yang sedang berlangsung.

# ======================= PENALARAN PAKAR =======================
Skenario | PenalaranPakar | Skenario Makro 1-3 Tahun | Asumsi arah faktor makro (Base/Bull/Bear) untuk horizon 1-3 tahun.
SkenarioAktif | KategoriInferensi | Skenario Aktif | (Inferensi) skenario yang dipilih pengguna (statusAktif=1).
PenilaianSektor | PenalaranPakar | Penilaian Sektor per Skenario | Objek reifikasi: skor sektor X di bawah skenario Y.
PeriodeHistoris | PenalaranPakar | Periode Historis (Kasus CBR) | Kasus historis untuk case-based reasoning.
PeriodeAnalog | KategoriInferensi | Periode Analog | (Inferensi) periode historis yang mirip dengan skenario aktif (skor kemiripan ≥ ambang).
FaseSiklusEkonomi | PenalaranPakar | Fase Siklus Ekonomi | Early, Mid, Late cycle, Resesi/Stagflasi (teori rotasi sektor).
TemaStruktural | PenalaranPakar | Tema Struktural Jangka Panjang | Megatren 1-3 tahun (hilirisasi, AI/data center, MBG, dll).
AturanPakar | PenalaranPakar | Heuristik Pakar | Heuristik/kaidah ahli saham dalam bahasa natural (dasar penyusunan SWRL).

# ======================= STAKEHOLDER =======================
StakeholderUtama | Stakeholder | Stakeholder Utama | Perusahaan sekuritas/broker mitra implementasi (embedded engine).
StakeholderKandidat | Stakeholder | Stakeholder Kandidat | Tim riset ekuitas, manajer investasi, edukator.
EndUser | Stakeholder | End User | Investor ritel awam & pemula.
InvestorRitel | EndUser | Investor Ritel (Persona) | Persona pengguna akhir dengan profil risiko & horizon.
Validator | Stakeholder | Validator | Panel pakar/analis senior yang memvalidasi aturan dan hasil backtest.
RegulatorStakeholder | Stakeholder | Regulator (Konteks Kepatuhan) | OJK & BEI sebagai pihak yang aturannya harus dipatuhi.

# ======================= KATEGORI INFERENSI: EMITEN =======================
InferensiEmiten | KategoriInferensi | Inferensi Level Emiten | Kategori hasil penalaran atas emiten.
FundamentalKuat | InferensiEmiten | Fundamental Kuat | Skor fundamental ≥ 8 dari 10.
FundamentalSedang | InferensiEmiten | Fundamental Sedang | Skor fundamental 5-7.
FundamentalLemah | InferensiEmiten | Fundamental Lemah | Skor fundamental ≤ 4.
EmitenMerugi | InferensiEmiten | Emiten Merugi | PER ≤ 0 (laba bersih negatif).
Undervalued | InferensiEmiten | Undervalued (Diskon Dalam) | PER < 0,85 × rata-rata PER 5 tahun.
FairValued | InferensiEmiten | Wajar | PER 0,85-1,1 × rata-rata 5 tahun.
Overvalued | InferensiEmiten | Overvalued | PER ≥ 1,1 × rata-rata 5 tahun.
ZonaDistress | InferensiEmiten | Zona Distress (Altman Z < 1,81) | Risiko kebangkrutan tinggi dalam 1-2 tahun.
ZonaAbuAbu | InferensiEmiten | Zona Abu-abu (1,81 ≤ Z < 2,99) | Perlu pemantauan.
ZonaAman | InferensiEmiten | Zona Aman (Z ≥ 2,99) | Risiko kebangkrutan rendah.
BankModalLemah | InferensiEmiten | Bank Modal Lemah | CAR < 12% atau NPL > 5%.
RisikoGoingConcern | InferensiEmiten | Risiko Going Concern / Rawan Collapse | Kombinasi distress + leverage tinggi + arus kas lemah.
RisikoManipulasiLaba | InferensiEmiten | Risiko Manipulasi Laba | Beneish M-Score > -1,78.
KualitasLabaTinggi | InferensiEmiten | Kualitas Laba Tinggi | CFO/Laba bersih ≥ 1 (laba didukung kas).
DividenAndalan | InferensiEmiten | Dividen Andalan | Dividend yield ≥ 6% dan payout ≤ 90% dengan fundamental kuat/sedang.
TrenNaik | InferensiEmiten | Tren Naik (Uptrend) | Harga > MA50 > MA200.
TrenTurun | InferensiEmiten | Tren Turun (Downtrend) | Harga < MA50 dan < MA200.
PullbackDalamUptrend | InferensiEmiten | Pullback dalam Uptrend | Harga di atas MA200 tetapi di bawah MA50.
Overbought | InferensiEmiten | Overbought | RSI ≥ 75.
Oversold | InferensiEmiten | Oversold | RSI < 30.
LonjakanVolume | InferensiEmiten | Lonjakan Volume | Volume ≥ 2 × rata-rata 20 hari.
AkumulasiBandar | InferensiEmiten | Akumulasi Bandar | Skor Acc/Dist broker ≥ 20.
DistribusiBandar | InferensiEmiten | Distribusi Bandar | Skor Acc/Dist broker ≤ -20.
AsingAkumulasi | InferensiEmiten | Asing Akumulasi | Net foreign buy 20 hari > Rp50 miliar.
AsingDistribusi | InferensiEmiten | Asing Distribusi | Net foreign sell 20 hari < -Rp50 miliar.
AkumulasiTersembunyi | InferensiEmiten | Akumulasi Tersembunyi (Smart Money Divergence) | Bandar akumulasi saat harga turun & ritel menjual - ciri khas fase akumulasi Wyckoff.
DistribusiKeRitel | InferensiEmiten | Distribusi ke Ritel | Bandar distribusi sementara broker ritel net buy besar.
FaseAkumulasiWyckoff | InferensiEmiten | Fase Akumulasi (Wyckoff) | Akumulasi di bawah MA200.
FaseMarkUpWyckoff | InferensiEmiten | Fase Mark-Up (Wyckoff) | Akumulasi + uptrend.
FaseDistribusiWyckoff | InferensiEmiten | Fase Distribusi (Wyckoff) | Distribusi saat RSI tinggi.
FaseMarkDownWyckoff | InferensiEmiten | Fase Mark-Down (Wyckoff) | Distribusi + downtrend.
KonfirmasiPolaBullish | InferensiEmiten | Konfirmasi Pola Bullish | Pola chart/candle bullish terkonfirmasi akumulasi bandar.
KonfirmasiPolaBearish | InferensiEmiten | Konfirmasi Pola Bearish | Pola chart/candle bearish terkonfirmasi distribusi.
SentimenPositif | InferensiEmiten | Sentimen Positif | Skor sentimen emiten ≥ 0,2.
SentimenNegatif | InferensiEmiten | Sentimen Negatif | Skor sentimen emiten ≤ -0,2.
RisikoOutflowPasif | InferensiEmiten | Risiko Outflow Dana Pasif | Konstituen MSCI saat freeze/ancaman reklasifikasi aktif.
PenerimaManfaatKomoditas | InferensiEmiten | Penerima Manfaat Komoditas | Emiten dengan eksposur komoditas yang harganya sedang naik.
KorbanKenaikanKomoditas | InferensiEmiten | Tertekan Kenaikan Biaya Komoditas | Emiten yang biaya inputnya naik.
ValueTrap | InferensiEmiten | Value Trap | Murah tetapi fundamental lemah & downtrend - jebakan bagi pemula.
DefensifBerkualitas | InferensiEmiten | Defensif Berkualitas | Fundamental kuat + zona aman + dividen, di sektor defensif.
KandidatTopPick | InferensiEmiten | Kandidat Top Pick | Skor total ≥ 22 di sektor bullish.
KandidatWatchlist | InferensiEmiten | Watchlist | Skor total 17-21 di sektor bullish.
SinyalEntry | InferensiEmiten | Sinyal Entry (Buy) | Teknikal + bandar mendukung, belum overbought.
SinyalBuyOnWeakness | InferensiEmiten | Sinyal Buy on Weakness | Fundamental kuat, koreksi sehat, bandar akumulasi.
SinyalExit | InferensiEmiten | Sinyal Exit / Take Profit | Overbought + distribusi, atau breakdown + asing jual.
SinyalHindari | InferensiEmiten | Sinyal Hindari | Downtrend + asing & bandar distribusi.
SinyalScalpingLong | InferensiEmiten | Sinyal Scalping Long | Lonjakan volume, di atas VWAP, bid tebal.
SinyalScalpingHindari | InferensiEmiten | Scalping: Hindari | Volume tinggi di bawah VWAP dengan tekanan offer.
CocokKonservatif | InferensiEmiten | Cocok untuk Investor Konservatif | Dividen, fundamental kuat, zona aman, likuid.
CocokModerat | InferensiEmiten | Cocok untuk Investor Moderat | Skor total ≥ 20 & fundamental ≥ sedang.
CocokAgresif | InferensiEmiten | Cocok untuk Investor Agresif | Momentum teknikal & bandar kuat.
RedFlagBerita | InferensiEmiten | Red Flag Berita | Berita negatif kredibel terkait emiten (dikeluarkan indeks, regulasi, gagal bayar).
AkumulasiInstitusiAsing | InferensiEmiten | Akumulasi Institusi Asing | Akumulator utama adalah broker asing dan skor Acc/Dist ≥ 20.
AkumulasiDidominasiRitel | InferensiEmiten | Akumulasi Didominasi Ritel (Waspada) | Pembeli utama broker ritel - rawan menjadi 'exit liquidity' bandar.
KeyakinanTinggi | InferensiEmiten | Keyakinan Tinggi (Confluence) | Top pick + akumulasi bandar + fundamental kuat (konfluensi multi-pilar).

# ======================= KATEGORI INFERENSI: SEKTOR =======================
InferensiSektor | KategoriInferensi | Inferensi Level Sektor | Kategori hasil penalaran atas sektor.
SektorBullishKuat | InferensiSektor | Sektor Bullish Kuat 1-3 Th | Skor outlook ≥ 14 (skenario aktif).
SektorBullishModerat | InferensiSektor | Sektor Bullish Moderat 1-3 Th | Skor outlook 8-13.
SektorNetral | InferensiSektor | Sektor Netral | Skor outlook 2-7.
SektorBearish | InferensiSektor | Sektor Bearish | Skor outlook < 2.
SektorBullish | InferensiSektor | Sektor Bullish (gabungan) | Gabungan bullish kuat & moderat.
SektorDiuntungkanGeopolitik | InferensiSektor | Sektor Diuntungkan Geopolitik | Ada tailwind dari pergerakan berbasis geopolitik.
SektorDirugikanGeopolitik | InferensiSektor | Sektor Dirugikan Geopolitik | Ada headwind dari pergerakan berbasis geopolitik.
SektorPresedenHistoris | InferensiSektor | Sektor dengan Preseden Historis | Unggul pada periode historis analog (CBR).
SektorMurahHistoris | InferensiSektor | Sektor Murah Historis | PER sektor < 0,85 × rata-rata 5 tahun.
SektorDidukungTema | InferensiSektor | Sektor Didukung Tema Struktural | Skor tema ≥ 2.
SektorFavoritSiklus | InferensiSektor | Sektor Favorit Fase Siklus | Skor rotasi fase siklus ≥ 2.
SektorPeluangKontrarian | InferensiSektor | Sektor Peluang Kontrarian | Diskon valuasi akibat outflow teknikal/pasif (bukan fundamental) - peluang 1-3 tahun.
SektorKeyakinanTinggi | InferensiSektor | Sektor Keyakinan Tinggi | Bullish + preseden historis + tema (konfluensi).
PenilaianBullishKuat | KategoriInferensi | Penilaian: Bullish Kuat | Penilaian sektor-skenario dengan skor ≥ 14.
PenilaianBullishModerat | KategoriInferensi | Penilaian: Bullish Moderat | Skor 8-13.
PenilaianNetral | KategoriInferensi | Penilaian: Netral | Skor 2-7.
PenilaianBearish | KategoriInferensi | Penilaian: Bearish | Skor < 2.
PenilaianAktif | KategoriInferensi | Penilaian di Skenario Aktif | Penilaian yang berada di skenario aktif.
"""

# Disjointness (pasangan kelas yang saling lepas)
DISJOINT = [
    ["EmitenPerbankan", "EmitenNonKeuangan"],
    ["FundamentalKuat", "FundamentalSedang", "FundamentalLemah"],
    ["Undervalued", "FairValued", "Overvalued"],
    ["ZonaDistress", "ZonaAbuAbu", "ZonaAman"],
    ["SektorBullishKuat", "SektorBullishModerat", "SektorNetral", "SektorBearish"],
    ["PenilaianBullishKuat", "PenilaianBullishModerat", "PenilaianNetral", "PenilaianBearish"],
    ["BrokerAsing", "BrokerLokal"],
    ["PolaBullish", "PolaBearish"],
    ["CandlestickBullish", "CandlestickBearish", "CandlestickIndecision"],
    ["PolaBandarBullish", "PolaBandarBearish"],
]
