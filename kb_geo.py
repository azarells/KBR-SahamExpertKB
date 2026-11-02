# -*- coding: utf-8 -*-
"""
ABox geopolitik, makro, berita (sentimen), skenario, kasus historis (CBR), stakeholder.
Tanggal acuan sistem: 2026-10-26 (v2).
"""
import datetime
TODAY = datetime.date(2026, 10, 26)
# Tanggal acuan bisa diubah tanpa menyentuh kode: tulis YYYY-MM-DD di data/tanggal_acuan.txt
try:
    import os as _o
    _p = _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "data", "tanggal_acuan.txt")
    if _o.path.exists(_p):
        TODAY = datetime.date.fromisoformat(open(_p, encoding="utf-8-sig").read().strip()[:10])
except Exception:
    pass

# ------------------------------------------------------------------ PERISTIWA
# nama, kelas(list), label, tanggal, deskripsi, memicu[], diputuskanOleh, statusBerjalan(0/1), berdampakPadaIndeks[]
PERISTIWA = [
 ("Ev_PerangIran_AS_Israel_2026", ["KonflikPerang", "PeristiwaGlobal"], "Perang Iran vs AS-Israel (mulai 28 Feb 2026)", "2026-02-28",
  "Serangan gabungan AS-Israel ke Iran; Selat Hormuz terganggu; Brent sempat US$114,74; Nikkei -7%, KOSPI -8%.", ["Mv_PremiRisikoTimurTengah"], None, 0, []),
 ("Ev_PenutupanHormuz_2026", ["KonflikPerang", "PeristiwaGlobal"], "Penutupan Selat Hormuz & Berakhirnya Gencatan (8 Jul 2026)", "2026-07-08",
  "Trump menyatakan gencatan senjata interim dengan Iran berakhir; Iran menutup Selat Hormuz; Brent +7,6%.", ["Mv_PremiRisikoTimurTengah", "Mv_GangguanPelayaran"], None, 0, []),
 ("Ev_GencatanSenjata_AS_Iran_Apr2026", ["GencatanDeeskalasi", "PeristiwaGlobal"], "Gencatan Senjata AS-Iran (Apr 2026)", "2026-04-15",
  "Harga minyak & gas anjlok setelah kesepakatan gencatan senjata (kemudian dibatalkan Juli 2026).", ["Mv_DeeskalasiTimurTengah"], None, 0, []),
 ("Ev_EskalasiTimurTengah_Okt2026", ["KonflikPerang", "PeristiwaGlobal"], "Serangan Houthi ke Riyadh & Tanker di Hormuz (Okt 2026)", "2026-10-10",
  "Serangan Houthi ke bandara Riyadh; 5 kilang Saudi ditutup sementara; tanker diserang dekat Sohar; Brent US$106,65.", ["Mv_PremiRisikoTimurTengah", "Mv_GangguanPelayaran"], None, 0, []),
 ("Ev_GencatanRusiaUkraina_Okt2026", ["GencatanDeeskalasi", "PeristiwaGlobal"], "Gencatan Senjata Rusia-Ukraina (infrastruktur energi, Okt 2026)", "2026-10-12",
  "Trump umumkan gencatan senjata mencakup infrastruktur energi; Rusia pasok >300 ribu ton diesel. Ukraina menuduh pelanggaran.", ["Mv_PasokanDieselMembaik"], None, 0, []),
 ("Ev_FOMC_Hawkish_2026", ["KebijakanMoneter", "PeristiwaGlobal"], "FOMC Hawkish: Peluang Kenaikan Bunga (Risalah Sep 2026)", "2026-10-08",
  "Core PCE 3,0%, headline 3,4%; 16/18 pejabat proyeksikan ≥1 kenaikan lagi; yield UST tertinggi sejak 2002; FFR 3,75% bisa ke 4,25%.", ["Mv_YieldUSNaik"], "TheFed", 0, []),
 ("Ev_BI_RDG_Okt2026", ["KebijakanMoneter"], "RDG BI Okt 2026: BI Rate Tetap 5,75%, Deposit Facility Naik ke 5%", "2026-10-21",
  "BI menahan BI Rate, menaikkan DF untuk stabilisasi rupiah.", ["Mv_SukuBungaBINaik"], "BankIndonesia", 0, []),
 ("Ev_EkspektasiKenaikanBIRate", ["KebijakanMoneter"], "Konsensus: BI Rate Naik ke 6%", "2026-10-21",
  "Mayoritas ekonom proyeksikan kenaikan BI Rate karena rupiah & arus modal asing.", ["Mv_SukuBungaBINaik"], "BankIndonesia", 0, []),
 ("Ev_BI_TurunkanGWM", ["KebijakanMoneter"], "BI Akan Turunkan GWM Bank", "2026-10-21",
  "Pelonggaran likuiditas perbankan meringankan biaya dana.", ["Mv_LikuiditasBankLonggar"], "BankIndonesia", 0, []),
 ("Ev_RupiahTertekan_2026", ["KrisisEkonomi"], "Tekanan Rupiah (~Rp17.900/USD)", "2026-10-21",
  "Rupiah melemah di tengah ketidakpastian global & outflow.", ["Mv_RupiahMelemah"], None, 0, []),
 ("Ev_InflasiNaik_Sep2026", ["KrisisEkonomi"], "Inflasi Naik ke 3,28% (Sep 2026)", "2026-10-01",
  "Didorong harga pangan & emas.", ["Mv_InflasiNaik"], "BPS", 0, []),
 ("Ev_KrisisPasarModal_2026", ["KrisisEkonomi"], "Krisis Pasar Modal Indonesia 2026 (IHSG -42% YTD)", "2026-10-19",
  "IHSG 4.996,61 (terendah sejak Okt 2020); net sell asing H1 Rp73,6 T; big caps anjlok.", ["Mv_AliranAsingKeluarEM", "Mv_DiskonValuasiBigCaps"], None, 0, []),
 ("Ev_TwinDeficit_2026", ["KrisisEkonomi"], "Twin Deficit Q1 2026 & Kekhawatiran Fiskal", "2026-07-01",
  "Neraca transaksi berjalan & finansial melemah; kekhawatiran kondisi fiskal.", ["Mv_TekananFiskal"], None, 0, []),
 ("Ev_TekananFiskalSubsidi", ["KebijakanDomestik"], "Subsidi Energi Membengkak (Rp376,8 T)", "2026-10-10",
  "Lonjakan harga minyak menekan APBN.", ["Mv_TekananFiskal"], "Kemenkeu", 0, []),
 ("Ev_MSCI_Freeze_2026", ["KeputusanPenyediaIndeks", "PeristiwaGlobal"], "MSCI Freeze FIF Indonesia (Feb-Nov 2026)", "2026-04-20",
  "MSCI tidak menaikkan FIF, memblokir penambahan & migrasi naik; freeze dipertahankan hingga review Nov 2026.", ["Mv_AliranPasifKeluar"], None, 0, ["MSCI_Indonesia", "MSCI_EmergingMarkets"]),
 ("Ev_SPDJI_FrontierFlag", ["KeputusanPenyediaIndeks", "PeristiwaGlobal"], "S&P DJI Tandai Potensi Reklasifikasi ke Frontier (Jul 2026)", "2026-07-08",
  "Risiko kehilangan status emerging market.", ["Mv_AliranPasifKeluar"], None, 0, ["SP_Indonesia_BMI"]),
 ("Ev_ReformasiFreeFloat_OJK", ["KebijakanDomestik"], "Reformasi Free Float 15% & Transparansi OJK/BEI", "2026-04-16",
  "Min. free float 15% (roadmap), keterbukaan pemegang >1%, 39 klasifikasi investor, HSC alert.", ["Mv_ReformasiTransparansi"], "OJK", 1, []),
 ("Ev_SnP_AfirmasiBBB", ["KebijakanDomestik"], "S&P Pertahankan Rating Indonesia BBB Stabil", "2026-07-15",
  "Investment grade dipertahankan; mengurangi risiko pasar obligasi.", ["Mv_StabilitasRating"], "SnP_Ratings", 0, []),
 ("Ev_HargaCPONaik_Okt2026", ["KebijakanDomestik"], "HR CPO Oktober 2026 Naik 3,44%", "2026-09-30",
  "Kemendag menaikkan harga referensi CPO.", ["Mv_HargaCPONaik"], "Kemendag", 0, []),
 ("Ev_EmasRekor_2026", ["KrisisEkonomi", "PeristiwaGlobal"], "Harga Emas Tinggi (~US$4.390, Sep 2026)", "2026-09-18",
  "Safe haven & pembelian bank sentral; terkoreksi dari puncak karena kenaikan Fed.", ["Mv_SafeHavenEmas"], None, 0, []),
 ("Ev_GOTO_DidepakMSCI", ["KeputusanPenyediaIndeks", "PeristiwaGlobal"], "GOTO Dikeluarkan/Dibekukan MSCI (Mei 2026)", "2026-05-28",
  "GOTO tertahan di Rp50 (gocap); MSCI membekukan/mengeluarkan dari indeks.", [], None, 0, []),
 ("Ev_PerpresOjol_2026", ["KebijakanDomestik"], "Perpres Ojek Online 2026", "2026-08-31",
  "Regulasi ride-hailing yang menekan prospek GOTO.", ["Mv_RegulasiPlatformKetat"], None, 0, []),
 ("Ev_ProgramMBG", ["KebijakanDomestik"], "Program Makan Bergizi Gratis (berjalan)", "2025-01-06",
  "Program belanja pangan nasional sejak Jan 2025.", ["Mv_BelanjaProgramPemerintah"], None, 1, []),
 ("Ev_MandatoriBiodiesel", ["KebijakanDomestik"], "Mandatori Biodiesel B40 (menuju B50)", "2025-01-01",
  "Penyerapan CPO untuk biodiesel.", ["Mv_PermintaanBiodiesel"], None, 1, []),
 ("Ev_InvestasiDataCenter", ["KebijakanDomestik"], "Gelombang Investasi Data Center & AI", "2025-06-01",
  "Hyperscaler & operator lokal membangun kapasitas data center.", ["Mv_InvestasiDataCenter"], None, 1, []),
 ("Ev_HilirisasiNikel", ["KebijakanDomestik"], "Kebijakan Hilirisasi & Kuota RKAB Nikel", "2024-01-01",
  "Larangan ekspor bijih, pembatasan kuota RKAB menopang harga nikel.", ["Mv_HargaNikelTertopang"], None, 1, []),
 ("Ev_TarifAS_LiberationDay_2025", ["KebijakanDagangTarif", "PeristiwaGlobal"], "Tarif Resiprokal AS 'Liberation Day' (Apr 2025)", "2025-04-02",
  "Tarif impor AS ke banyak negara; risk-off global April 2025.", ["Mv_PerangDagang"], None, 0, []),
 ("Ev_OPEC_PertahankanProduksi", ["KeputusanOPEC", "PeristiwaGlobal"], "OPEC+ Pertahankan Produksi", "2025-11-01",
  "OPEC+ menahan kenaikan produksi.", ["Mv_PasokanMinyakStabil"], "OPEC_Plus", 0, []),
 ("Ev_MSCI_KonsultasiStandalone_Okt2026", ["KeputusanPenyediaIndeks", "PeristiwaGlobal"], "MSCI Konsultasi Reklasifikasi Indonesia ke Standalone (15 Okt 2026)", "2026-10-15",
  "Konsultasi publik hingga 30 Apr 2027; keputusan final paling lambat akhir Jun 2027. Estimasi outflow pasif USD3-6 miliar.", ["Mv_AliranPasifKeluar", "Mv_PremiRisikoNegaraNaik"], None, 0, ["MSCI_Indonesia", "MSCI_EmergingMarkets"]),
 ("Ev_CrashIHSG_16Okt2026", ["KrisisEkonomi"], "Crash IHSG 16 Okt 2026 (-11,57% sehari)", "2026-10-16",
  "Capitulation day; net sell asing Rp3,34 T; IHSG 5.185 lalu 4.996 (19 Okt).", ["Mv_AliranAsingKeluarEM", "Mv_DiskonValuasiBigCaps"], None, 0, []),
 ("Ev_FedHike_Sep2026", ["KebijakanMoneter", "PeristiwaGlobal"], "FOMC Naikkan Bunga ke 3,75-4,00% (16 Sep 2026)", "2026-09-16",
  "Kenaikan pertama sejak 2023 (12-0); median dot akhir 2026 4,1%.", ["Mv_YieldUSNaik"], "TheFed", 0, []),
 ("Ev_PembelianDomestikBlueChip", ["KebijakanDomestik"], "Investor Domestik Membeli Blue Chip Terdiskon", "2026-10-19",
  "Aliran beli domestik menahan kejatuhan big caps.", ["Mv_DukunganLikuiditasDomestik"], None, 0, []),
 ("Ev_RencanaBEI_KeluarkanHSC", ["KebijakanDomestik"], "Rencana BEI Keluarkan Saham HSC dari Perhitungan IHSG", "2026-10-19",
  "Saham dengan konsentrasi kepemilikan tinggi berisiko dikeluarkan dari indeks (volatilitas jangka pendek).", ["Mv_PenghapusanHSC"], "BEI_Bursa", 0, []),
 ("Ev_MSCI_ReviewAgustus2026", ["KeputusanPenyediaIndeks", "PeristiwaGlobal"], "MSCI Review Agustus 2026 (GOTO & CPIN keluar Standard)", "2026-08-12",
  "GOTO keluar MSCI Standard/IMI; CPIN pindah ke Small Cap.", [], None, 0, []),
 ("Ev_MoodysOutlookNegatif_Feb2026", ["KebijakanDomestik"], "Moody's Turunkan Outlook Utang RI ke Negatif (Feb 2026)", "2026-02-06",
  "Outlook negatif; CDS naik.", ["Mv_PremiRisikoNegaraNaik"], "Moodys", 0, []),
 ("Ev_PemiluSelaAS_2026", ["PemiluPolitik", "PeristiwaGlobal"], "Pemilu Sela AS (3 Nov 2026)", "2026-11-03",
  "Potensi volatilitas kebijakan fiskal & tarif AS.", [], None, 0, []),
]

# ------------------------------------------------------------------ PERGERAKAN (node transmisi)
# nama, label, geopolitik(0/1), menyebabkan[], menguntungkan[], merugikan[], peluangKontrarian[], komoditasNaik[], komoditasTurun[]
S = lambda *a: ["Sektor_" + x for x in a]
PERGERAKAN = [
 ("Mv_PremiRisikoTimurTengah", "Premi Risiko Timur Tengah Naik", 1, ["Mv_HargaMinyakNaik", "Mv_SafeHavenEmas", "Mv_RiskOffGlobal"], [], [], [], [], []),
 ("Mv_DeeskalasiTimurTengah", "De-eskalasi Timur Tengah", 1, ["Mv_HargaMinyakTurun"], [], [], [], [], []),
 ("Mv_HargaMinyakNaik", "Harga Minyak Naik", 0, ["Mv_PetrodolarDolarKuat", "Mv_InflasiNaik", "Mv_SubstitusiBatuBara", "Mv_PermintaanBiodiesel", "Mv_SubsidiEnergiMembengkak"], S("Energi"), S("TransportasiLogistik", "KonsumenNonPrimer"), [], ["Kom_MinyakBrent", "Kom_MinyakWTI", "Kom_GasLNG"], []),
 ("Mv_HargaMinyakTurun", "Harga Minyak Turun", 0, [], S("TransportasiLogistik"), S("Energi"), [], [], ["Kom_MinyakBrent", "Kom_MinyakWTI"]),
 ("Mv_PetrodolarDolarKuat", "Efek Petrodolar: Dolar Menguat", 0, ["Mv_DolarMenguat"], [], [], [], [], []),
 ("Mv_YieldUSNaik", "Yield US Treasury Naik", 0, ["Mv_DolarMenguat"], [], S("Teknologi", "PropertiRealEstat"), [], [], []),
 ("Mv_DolarMenguat", "Indeks Dolar (DXY) Menguat", 0, ["Mv_RupiahMelemah", "Mv_AliranAsingKeluarEM"], [], [], [], [], []),
 ("Mv_RupiahMelemah", "Rupiah Melemah", 0, ["Mv_PendapatanEksportirNaik", "Mv_BiayaImporNaik"], [], [], [], [], []),
 ("Mv_PendapatanEksportirNaik", "Pendapatan Eksportir (USD) Naik dalam Rupiah", 0, [], S("Energi", "BarangBaku"), [], [], [], []),
 ("Mv_BiayaImporNaik", "Biaya Bahan Baku Impor Naik", 0, ["Mv_InflasiNaik"], [], S("Kesehatan", "KonsumenPrimer", "KonsumenNonPrimer"), [], ["Kom_Gandum", "Kom_JagungKedelai"], []),
 ("Mv_InflasiNaik", "Inflasi Naik", 0, ["Mv_DayaBeliTurun", "Mv_SukuBungaBINaik"], [], [], [], [], []),
 ("Mv_DayaBeliTurun", "Daya Beli Melemah", 0, [], [], S("KonsumenNonPrimer", "PropertiRealEstat"), [], [], []),
 ("Mv_SukuBungaBINaik", "Suku Bunga BI Naik/Tinggi", 0, ["Mv_BiayaKreditNaik"], [], S("PropertiRealEstat", "Teknologi"), [], [], []),
 ("Mv_BiayaKreditNaik", "Biaya Kredit Naik", 0, ["Mv_PenjualanPropertiOtoMelemah"], [], S("Keuangan"), [], [], []),
 ("Mv_PenjualanPropertiOtoMelemah", "Penjualan Properti & Otomotif Melemah", 0, [], [], S("PropertiRealEstat", "Perindustrian"), [], [], []),
 ("Mv_AliranAsingKeluarEM", "Dana Asing Keluar dari Emerging Market", 0, ["Mv_IHSGTertekan"], [], S("Keuangan"), [], [], []),
 ("Mv_AliranPasifKeluar", "Outflow Dana Pasif (MSCI/S&P)", 0, ["Mv_IHSGTertekan", "Mv_DiskonValuasiBigCaps"], [], S("Keuangan", "Infrastruktur"), [], [], []),
 ("Mv_IHSGTertekan", "IHSG Tertekan", 0, [], [], [], [], [], []),
 ("Mv_DiskonValuasiBigCaps", "Diskon Valuasi Ekstrem Big Caps", 0, [], [], [], S("Keuangan", "Infrastruktur", "KonsumenPrimer"), [], []),
 ("Mv_SafeHavenEmas", "Permintaan Safe Haven Emas", 1, [], S("BarangBaku"), [], [], ["Kom_Emas", "Kom_Perak"], []),
 ("Mv_RiskOffGlobal", "Risk-off Global", 1, ["Mv_AliranAsingKeluarEM"], S("Kesehatan"), S("Teknologi"), [], [], []),
 ("Mv_SubstitusiBatuBara", "Substitusi ke Batu Bara (Minyak Mahal)", 0, [], S("Energi"), [], [], ["Kom_BatuBara"], []),
 ("Mv_PermintaanBiodiesel", "Permintaan Biodiesel Naik", 0, ["Mv_HargaCPONaik"], [], [], [], [], []),
 ("Mv_HargaCPONaik", "Harga CPO Naik", 0, [], S("KonsumenPrimer"), [], [], ["Kom_CPO"], []),
 ("Mv_SubsidiEnergiMembengkak", "Subsidi Energi Membengkak", 0, ["Mv_TekananFiskal"], [], [], [], [], []),
 ("Mv_TekananFiskal", "Tekanan Fiskal / Twin Deficit", 0, ["Mv_RupiahMelemah", "Mv_RuangBelanjaTerbatas"], [], [], [], [], []),
 ("Mv_RuangBelanjaTerbatas", "Ruang Belanja Infrastruktur Terbatas", 0, [], [], S("Infrastruktur", "PropertiRealEstat"), [], [], []),
 ("Mv_GangguanPelayaran", "Gangguan Jalur Pelayaran", 1, ["Mv_TarifAngkutLautNaik"], [], [], [], [], []),
 ("Mv_TarifAngkutLautNaik", "Tarif Angkut Laut Naik", 0, [], S("TransportasiLogistik"), [], [], [], []),
 ("Mv_PasokanDieselMembaik", "Pasokan Diesel Global Membaik", 1, [], S("TransportasiLogistik"), S("Energi"), [], [], []),
 ("Mv_PerangDagang", "Eskalasi Perang Dagang", 1, ["Mv_PermintaanChinaTurun"], [], S("Teknologi"), [], [], []),
 ("Mv_PermintaanChinaTurun", "Permintaan China Melemah", 0, ["Mv_HargaLogamIndustriTurun"], [], S("Energi"), [], [], ["Kom_BatuBara"]),
 ("Mv_HargaLogamIndustriTurun", "Harga Logam Industri Turun", 0, [], [], S("BarangBaku"), [], [], ["Kom_Nikel", "Kom_Tembaga", "Kom_Timah"]),
 ("Mv_HargaNikelTertopang", "Harga Nikel Tertopang Kuota", 0, [], S("BarangBaku"), [], [], ["Kom_Nikel"], []),
 ("Mv_BelanjaProgramPemerintah", "Belanja Program Pemerintah (MBG)", 0, ["Mv_PermintaanProteinNaik"], [], [], [], [], []),
 ("Mv_PermintaanProteinNaik", "Permintaan Protein & Pangan Naik", 0, [], S("KonsumenPrimer"), [], [], [], []),
 ("Mv_InvestasiDataCenter", "Investasi Data Center & AI", 0, ["Mv_PermintaanKonektivitas"], [], [], [], [], []),
 ("Mv_PermintaanKonektivitas", "Permintaan Konektivitas & Fiber Naik", 0, [], S("Infrastruktur", "Teknologi"), [], [], [], []),
 ("Mv_ReformasiTransparansi", "Reformasi Transparansi Pasar Modal", 0, ["Mv_KepercayaanAsingPulih"], [], [], [], [], []),
 ("Mv_KepercayaanAsingPulih", "Kepercayaan Investor Asing Pulih (1-3 th)", 0, [], S("Keuangan", "Infrastruktur"), [], [], [], []),
 ("Mv_LikuiditasBankLonggar", "Likuiditas Bank Longgar (GWM turun)", 0, [], S("Keuangan"), [], [], [], []),
 ("Mv_StabilitasRating", "Stabilitas Rating Investment Grade", 0, [], S("Keuangan"), [], [], [], []),
 ("Mv_RegulasiPlatformKetat", "Regulasi Platform Digital Mengetat", 0, [], [], S("Teknologi"), [], [], []),
 ("Mv_PremiRisikoNegaraNaik", "Premi Risiko Negara (CDS) Naik", 0, ["Mv_AliranAsingKeluarEM", "Mv_OutflowSBN"], [], S("Keuangan", "PropertiRealEstat"), [], [], []),
 ("Mv_OutflowSBN", "Outflow Asing dari SBN", 0, ["Mv_RupiahMelemah"], [], S("Keuangan"), [], [], []),
 ("Mv_KenaikanHargaBBM", "Penyesuaian Harga BBM Bersubsidi (Antisipasi)", 0, ["Mv_InflasiNaik", "Mv_DayaBeliTurun"], [], S("KonsumenNonPrimer", "TransportasiLogistik"), [], [], []),
 ("Mv_DukunganLikuiditasDomestik", "Dukungan Likuiditas Domestik (institusi lokal, buyback)", 0, [], S("Keuangan", "Infrastruktur"), [], S("Keuangan", "Infrastruktur"), [], []),
 ("Mv_PenghapusanHSC", "Penghapusan Saham HSC dari IHSG", 0, [], [], [], [], [], []),
 ("Mv_PasokanMinyakStabil", "Pasokan Minyak Stabil", 0, ["Mv_HargaMinyakTurun"], [], [], [], [], []),
]

# ------------------------------------------------------------------ BERITA
# id, tanggal, media, url, judul, kelas, kredibilitas, peristiwa[], sektor[], emiten[], variabel, arahOverride(None/±1/0)
BERITA = [
 ("N01", "2026-10-08", "Bisnis.com", "https://market.bisnis.com/read/20261008/7/2010804/fomc-minutes-buka-peluang-kenaikan-bunga-ihsg-dibayangi-tekanan", "FOMC Minutes Buka Peluang Kenaikan Bunga, IHSG Dibayangi Tekanan", "BeritaMakroGeopolitik", 0.9, ["Ev_FOMC_Hawkish_2026"], [], [], "BUNGA", None),
 ("N02", "2026-10-09", "Investortrust", "https://investortrust.id/international/89954/risalah-fomc-ungkap-perpecahan-pejabat-the-fed-indikasikan-suku-bunga-mendekati-3-pada-2027", "Risalah FOMC Ungkap Perpecahan Pejabat The Fed, Indikasikan Suku Bunga Mendekati 3% pada 2027", "BeritaMakroGeopolitik", 0.85, ["Ev_FOMC_Hawkish_2026"], [], [], "BUNGA", -1),
 ("N03", "2026-10-05", "IDX Channel/RCTI+", "https://www.rctiplus.com/news/detail/idxchannel/5485054/tiga-petinggi-the-fed-kecilkan-peluang-kenaikan-suku-bunga-pada-oktober-2026", "Tiga Petinggi The Fed Kecilkan Peluang Kenaikan Suku Bunga pada Oktober 2026", "BeritaMakroGeopolitik", 0.8, ["Ev_FOMC_Hawkish_2026"], [], [], "BUNGA", None),
 ("N04", "2026-10-06", "KuCoin News", "https://www.kucoin.com/id/news/flash/fed-dissenters-push-for-rate-hike-amid-inflation-concerns", "Pembantah Fed Dorong Kenaikan Suku Bunga di Tengah Kekhawatiran Inflasi", "BeritaMakroGeopolitik", 0.6, ["Ev_FOMC_Hawkish_2026"], [], [], "BUNGA", None),
 ("N05", "2026-10-21", "Bisnis.com", "https://finansial.bisnis.com/read/20261021/11/2014413/breaking-bank-indonesia-tahan-bi-rate-575-pada-rdg-oktober-2026", "Breaking: Bank Indonesia Tahan BI Rate 5,75% pada RDG Oktober 2026", "BeritaMakroGeopolitik", 0.95, ["Ev_BI_RDG_Okt2026"], [], [], "BUNGA", None),
 ("N06", "2026-10-21", "Bisnis.com", "https://finansial.bisnis.com/read/20261021/11/2014377/bi-rate-diproyeksi-naik-ke-6-rupiah-dan-arus-modal-asing-jadi-pertimbangan", "BI Rate Diproyeksi Naik ke 6%, Rupiah dan Arus Modal Asing Jadi Pertimbangan", "BeritaMakroGeopolitik", 0.9, ["Ev_EkspektasiKenaikanBIRate"], [], [], "BUNGA", None),
 ("N07", "2026-10-21", "Kontan", "https://insight.kontan.co.id/news/deposit-facility-naik-saat-bi-rate-tetap-pada-oktober-2026-bi-akan-turunkan-gwm-bank", "Deposit Facility Naik Saat BI Rate Tetap pada Oktober 2026, BI Akan Turunkan GWM Bank", "BeritaMakroGeopolitik", 0.9, ["Ev_BI_TurunkanGWM", "Ev_BI_RDG_Okt2026"], ["Sektor_Keuangan"], [], None, None),
 ("N08", "2026-10-21", "RRI", "https://rri.co.id/en/business/2664084/bi-holds-benchmark-rate-at-575-percent-amid-rupiah-pressure-global-uncertainty", "BI Holds Benchmark Rate at 5.75 Percent Amid Rupiah Pressure, Global Uncertainty", "BeritaMakroGeopolitik", 0.85, ["Ev_RupiahTertekan_2026"], [], [], "USD", 1),
 ("N09", "2026-10-21", "Databoks Katadata", "https://databoks.katadata.co.id/en/market/statistics/6ad888653144b/ihsg-edges-up-after-bi-keeps-interest-rates-steady-wednesday-october-21-2026", "IHSG Edges Up After BI Keeps Interest Rates Steady", "BeritaMakroGeopolitik", 0.85, [], [], [], "PASAR", None),
 ("N10", "2026-10-20", "Kontan", "https://insight.kontan.co.id/news/ihsg-terendah-6-tahun-waspadai-tekanan-jual-saham-big-caps-hari-ini-2010", "IHSG Terendah 6 Tahun, Waspadai Tekanan Jual Saham Big Caps Hari Ini", "BeritaMakroGeopolitik", 0.9, ["Ev_KrisisPasarModal_2026"], ["Sektor_Keuangan", "Sektor_Infrastruktur"], [], "PASAR", None),
 ("N11", "2026-10-18", "Bisnis.com", "https://market.bisnis.com/read/20261018/7/2013517/ihsg-ambruk-asing-net-sell-jumbo-di-saham-big-banks-bbca-bmri", "IHSG Ambruk, Asing Net Sell Jumbo di Saham Big Banks BBCA-BMRI", "BeritaMakroGeopolitik", 0.9, ["Ev_KrisisPasarModal_2026"], ["Sektor_Keuangan"], ["BBCA", "BMRI"], "PASAR", None),
 ("N12", "2026-07-01", "Investortrust", "https://investortrust.id/market/108011/semester-i-kelam-ihsg-ambles-34-73-disertai-kejatuhaan-saham-big-caps-dan-net-sell-asing", "Semester I Kelam, IHSG Ambles 34,73% Disertai Kejatuhan Saham Big Caps dan Net Sell Asing", "BeritaMakroGeopolitik", 0.85, ["Ev_TwinDeficit_2026", "Ev_KrisisPasarModal_2026"], ["Sektor_Energi", "Sektor_PropertiRealEstat", "Sektor_Infrastruktur"], ["BBCA", "BBRI", "TLKM", "AMMN", "BMRI"], "PASAR", None),
 ("N13", "2026-07-01", "Investortrust", "https://investortrust.id/market/108011/semester-i-kelam-ihsg-ambles-34-73-disertai-kejatuhaan-saham-big-caps-dan-net-sell-asing", "MDKA dan ADRO Menguat, Menahan Kejatuhan IHSG Semester I", "BeritaEmiten", 0.85, [], [], ["MDKA"], None, None),
 ("N14", "2026-03-09", "Bisnis.com", "https://ekonomi.bisnis.com/read/20260309/620/1958952/perang-iran-vs-as-israel-makin-panas-bikin-harga-minyak-mendidih-dan-pasar-saham-tumbang", "Perang Iran vs AS-Israel Makin Panas Bikin Harga Minyak Mendidih dan Pasar Saham Tumbang", "BeritaMakroGeopolitik", 0.9, ["Ev_PerangIran_AS_Israel_2026"], [], [], "MINYAK", None),
 ("N15", "2026-03-16", "CNBC Indonesia", "https://www.cnbcindonesia.com/market/20260316085914-17-719251/perang-iran-vs-as-israel-makin-gila-minyak-sentuh-us-100-lagi", "Perang Iran vs AS-Israel Makin Gila, Minyak Sentuh US$100 Lagi", "BeritaMakroGeopolitik", 0.9, ["Ev_PerangIran_AS_Israel_2026"], [], [], "MINYAK", None),
 ("N16", "2026-04-09", "Bloomberg", "https://www.bloomberg.com/news/articles/2026-04-09/goldman-flags-100-plus-brent-if-hormuz-shut-for-another-month", "Goldman Flags $100-Plus Brent If Hormuz Shut for Another Month", "BeritaMakroGeopolitik", 0.95, ["Ev_PenutupanHormuz_2026"], [], [], "MINYAK", 1),
 ("N17", "2026-04-15", "Bloomberg Government", "https://news.bloomberglaw.com/bloomberg-government-news/oil-and-gas-prices-plunge-after-us-and-iran-agree-to-a-ceasefire", "Oil and Gas Prices Plunge After US and Iran Agree to a Ceasefire", "BeritaMakroGeopolitik", 0.95, ["Ev_GencatanSenjata_AS_Iran_Apr2026"], [], [], "MINYAK", None),
 ("N18", "2026-07-08", "OilPrice.com", "https://oilprice.com/Latest-Energy-News/World-News/Oil-Prices-Jump-over-7-as-Iran-Ceasefire-Declared-Over.amp.html", "Oil Prices Jump over 7% as Iran Ceasefire Declared Over", "BeritaMakroGeopolitik", 0.85, ["Ev_PenutupanHormuz_2026"], [], [], "MINYAK", None),
 ("N19", "2026-10-13", "KabarBursa", "https://www.kabarbursa.com/market-hari-ini/houthi-gempur-arab-saudi-harga-minyak-brent-naik-ke-level-usd106-per-barel", "Houthi Gempur Arab Saudi, Harga Minyak Brent Naik ke Level USD106 per Barel", "BeritaMakroGeopolitik", 0.8, ["Ev_EskalasiTimurTengah_Okt2026"], [], [], "MINYAK", None),
 ("N20", "2026-10-13", "KabarBursa", "https://www.kabarbursa.com/market-hari-ini/houthi-gempur-arab-saudi-harga-minyak-brent-naik-ke-level-usd106-per-barel", "Trump Umumkan Gencatan Senjata Rusia-Ukraina Mencakup Infrastruktur Energi, Pasokan Diesel Bertambah", "BeritaMakroGeopolitik", 0.8, ["Ev_GencatanRusiaUkraina_Okt2026"], [], [], "MINYAK", -1),
 ("N21", "2026-10-07", "IDNFinancials", "https://www.idnfinancials.com/id/news/61580/goldman-sachs-naikkan-proyeksi-harga-minyak-akhir-2026", "Goldman Sachs Naikkan Proyeksi Harga Minyak Akhir 2026", "BeritaRisetAnalis", 0.85, ["Ev_EskalasiTimurTengah_Okt2026"], [], [], "MINYAK", None),
 ("N22", "2026-04-20", "Investortrust", "https://investortrust.id/market/100712/msci-freezes-indonesia-weightings-as-jakarta-scrambles-to-save-emerging-market-status", "MSCI Freezes Indonesia Weightings as Jakarta Scrambles to Save Emerging Market Status", "BeritaMakroGeopolitik", 0.85, ["Ev_MSCI_Freeze_2026", "Ev_ReformasiFreeFloat_OJK"], [], [], "MSCI", None),
 ("N23", "2026-07-07", "Bisnis.com", "https://market.bisnis.com/read/20260707/7/1986188/msci-pertahankan-freeze-saham-ri-hingga-review-november-2026", "MSCI Pertahankan Freeze Saham RI hingga Review November 2026", "BeritaMakroGeopolitik", 0.9, ["Ev_MSCI_Freeze_2026"], [], [], "MSCI", None),
 ("N24", "2026-08-12", "IDX Channel/RCTI+", "https://www.rctiplus.com/news/detail/idxchannel/5422425/msci-tetap-bekukan-saham-indonesia--tak-ada-penambahan-emiten-pada-review-agustus-2026", "MSCI Tetap Bekukan Saham Indonesia, Tak Ada Penambahan Emiten pada Review Agustus 2026", "BeritaMakroGeopolitik", 0.8, ["Ev_MSCI_Freeze_2026"], [], [], "MSCI", None),
 ("N25", "2026-08-12", "Investortrust", "https://investortrust.id/market/103129/msci-tetap-freeze-saham-indonesia-reformasi-ojk-dinilai-belum-meyakinkan", "MSCI Tetap Freeze Saham Indonesia, Reformasi OJK Dinilai Belum Meyakinkan", "BeritaMakroGeopolitik", 0.85, ["Ev_MSCI_Freeze_2026", "Ev_ReformasiFreeFloat_OJK"], [], [], "MSCI", None),
 ("N26", "2026-07-08", "Investortrust", "https://investortrust.id/market/92712/free-float-dipertanyakan-msci-tangguhkan-review-msci-februari-hingga-peluang-turun-jadi-frontier-market-pasar-saham-indonesia", "Free Float Dipertanyakan, MSCI Tangguhkan Review hingga Peluang Turun Jadi Frontier Market", "BeritaMakroGeopolitik", 0.8, ["Ev_SPDJI_FrontierFlag", "Ev_MSCI_Freeze_2026"], [], [], "MSCI", None),
 ("N27", "2026-07-15", "Investortrust", "https://investortrust.id/market/109557/target-ihsg-7200-ini-daftar-saham-pilihan-bri-danareksa-dan-target-harganya", "Target IHSG 7.200, Ini Daftar Saham Pilihan BRI Danareksa: BBCA, BBNI, ISAT, EXCL, ANTM, TINS, AADI", "BeritaRisetAnalis", 0.85, ["Ev_SnP_AfirmasiBBB"], [], ["BBCA", "BBNI", "ISAT", "EXCL", "ANTM", "TINS", "AADI"], None, None),
 ("N28", "2026-10-01", "Bisnis.com", "https://market.bisnis.com/read/20261001/189/2008873/ihsg-berpeluang-ke-7000-cek-rekomendasi-saham-oktober-2026", "IHSG Berpeluang ke 7.000, Cek Rekomendasi Saham Oktober 2026", "BeritaRisetAnalis", 0.85, [], [], [], "PASAR", None),
 ("N29", "2026-09-01", "Bisnis.com", "https://market.bisnis.com/read/20260901/189/2000529/peluang-ihsg-ke-6650-kiwoom-jagokan-9-saham-pilihan", "Peluang IHSG ke 6.650, Kiwoom Jagokan 9 Saham Pilihan", "BeritaRisetAnalis", 0.85, [], [], [], "PASAR", None),
 ("N30", "2026-10-01", "Investortrust", "https://investortrust.id/macro/118018/bps-inflasi-september-2026-tembus-0-30-tahunan-3-28", "BPS: Inflasi September 2026 Tembus 0,30%, Tahunan 3,28%", "BeritaMakroGeopolitik", 0.9, ["Ev_InflasiNaik_Sep2026"], [], [], "INFLASI", None),
 ("N31", "2026-10-01", "Kontan", "https://insight.kontan.co.id/news/inflasi-september-2026-naik-jadi-328-harga-pangan-dan-emas-jadi-pendorong", "Inflasi September 2026 Naik Jadi 3,28%, Harga Pangan dan Emas Jadi Pendorong", "BeritaMakroGeopolitik", 0.9, ["Ev_InflasiNaik_Sep2026", "Ev_EmasRekor_2026"], [], [], "INFLASI", None),
 ("N32", "2026-09-30", "Kontan", "https://industri.kontan.co.id/news/harga-referensi-cpo-naik-344-pada-oktober-2026", "Harga Referensi CPO Naik 3,44% pada Oktober 2026", "BeritaMakroGeopolitik", 0.9, ["Ev_HargaCPONaik_Okt2026"], ["Sektor_KonsumenPrimer"], [], "CPO", None),
 ("N33", "2026-09-30", "BCA Sekuritas", "https://bcasekuritas.co.id/latest-news/news/kemendag-hr-cpo-naik-pada-oktober-2026", "Kemendag: HR CPO Naik pada Oktober 2026", "BeritaMakroGeopolitik", 0.85, ["Ev_HargaCPONaik_Okt2026"], [], [], "CPO", None),
 ("N35", "2026-05-28", "Bisnis.com", "https://market.bisnis.com/read/20260528/7/1976875/tertahan-di-level-rp50-msci-bakal-bekukan-saham-goto", "Tertahan di Level Rp50, MSCI Bakal Bekukan Saham GOTO", "BeritaEmiten", 0.9, ["Ev_GOTO_DidepakMSCI"], [], ["GOTO"], None, None),
 ("N36", "2026-05-29", "Investortrust", "https://investortrust.id/market/112721/msci-depak-goto-manajemen-perseroan-tegaskan-hal-ini", "MSCI Depak GOTO, Manajemen Perseroan Tegaskan Hal Ini", "BeritaEmiten", 0.85, ["Ev_GOTO_DidepakMSCI"], [], ["GOTO"], None, None),
 ("N37", "2026-08-31", "Bisnis.com", "https://market.bisnis.com/read/20260831/189/2000049/tantangan-saham-gocap-hingga-perpres-ojol-goto-masih-ada-peluang", "Tantangan Saham Gocap hingga Perpres Ojol, GOTO Masih Ada Peluang?", "BeritaEmiten", 0.9, ["Ev_PerpresOjol_2026"], ["Sektor_Teknologi"], ["GOTO"], None, None),
 ("N38", "2025-12-18", "Bisnis.com", "https://market.bisnis.com/read/20251218/189/1938020/ihsg-diproyeksi-tembus-9820-pada-2026-cek-saham-jagoan-bri-danareksa", "IHSG Diproyeksi Tembus 9.820 pada 2026, Cek Saham Jagoan BRI Danareksa", "BeritaRisetAnalis", 0.85, [], [], [], "PASAR", None),
 ("N39", "2025-12-03", "Bisnis.com", "https://market.bisnis.com/read/20251203/7/1933944/mandiri-sekuritas-ramal-ihsg-pada-2026-tembus-level-9350-cek-sektor-unggulannya", "Mandiri Sekuritas Ramal IHSG pada 2026 Tembus Level 9.350", "BeritaRisetAnalis", 0.85, [], [], [], "PASAR", None),
 ("N40", "2025-12-08", "KabarBursa", "https://www.kabarbursa.com/market-hari-ini/minyak-brent-naik-ke-usd75-ancaman-suplai-bikin-pasar-waspada", "Minyak Brent Naik ke USD75, Ancaman Suplai Bikin Pasar Waspada", "BeritaMakroGeopolitik", 0.8, ["Ev_OPEC_PertahankanProduksi"], [], [], "MINYAK", None),
 ("N41", "2026-10-19", "Kontan", "https://keuangan.kontan.co.id/news/aksi-jual-asing-tekan-saham-big-banks-simak-rekomendasinya", "Aksi Jual Asing Tekan Saham Big Banks, Simak Rekomendasinya", "BeritaMakroGeopolitik", 0.85, ["Ev_KrisisPasarModal_2026"], ["Sektor_Keuangan"], ["BBCA", "BBRI", "BMRI"], None, None),
 ("N42", "2026-10-10", "KabarBursa", "https://www.kabarbursa.com/makro/subsidi-energi-rp3768-triliun-seberapa-kuat-apbn-menahan-lonjakan-harga-minyak", "Subsidi Energi Rp376,8 Triliun: Seberapa Kuat APBN Menahan Lonjakan Harga Minyak", "BeritaMakroGeopolitik", 0.75, ["Ev_TekananFiskalSubsidi"], [], [], "MINYAK", None),
 ("N43", "2026-10-02", "JournalArta", "https://journalarta.com/news/2026/10/02/the-fed-pause-oktober-2026-pce-inflasi-melandai/?all=1", "The Fed Pause Oktober 2026, PCE Inflasi Melandai", "BeritaMakroGeopolitik", 0.6, ["Ev_FOMC_Hawkish_2026"], [], [], "BUNGA", -1),
 ("N44", "2025-04-03", "Arsip pasar", "", "Tarif Resiprokal AS Picu Aksi Jual Global, Bursa Asia Anjlok", "BeritaMakroGeopolitik", 0.8, ["Ev_TarifAS_LiberationDay_2025"], [], [], "PASAR", None),
 ("N45", "2026-10-16", "Bisnis.com", "https://market.bisnis.com/read/20261016/7/2013088/bei-minta-klarifikasi-msci-soal-usulan-status-standalone-market", "BEI Minta Klarifikasi MSCI soal Usulan Status Standalone Market", "BeritaMakroGeopolitik", 0.9, ["Ev_MSCI_KonsultasiStandalone_Okt2026"], [], [], "MSCI", None),
 ("N46", "2026-10-16", "Bisnis.com", "https://market.bisnis.com/read/20261016/7/2013233/wamenko-perekonomian-minta-investor-tak-panik-msci-tak-selalu-benar", "Wamenko Perekonomian Minta Investor Tak Panik: MSCI Tak Selalu Benar", "BeritaMakroGeopolitik", 0.85, ["Ev_MSCI_KonsultasiStandalone_Okt2026"], [], [], "MSCI", None),
 ("N47", "2026-10-20", "KabarBursa", "https://www.kabarbursa.com/market-hari-ini/pelemahan-dinilai-mulai-terbatas-simak-arah-ihsg-hari-ini", "Pelemahan Dinilai Mulai Terbatas; IHSG Anjlok 11,57% Jumat, Investor Domestik Borong Blue Chip Terdiskon", "BeritaMakroGeopolitik", 0.8, ["Ev_CrashIHSG_16Okt2026", "Ev_PembelianDomestikBlueChip", "Ev_RencanaBEI_KeluarkanHSC"], ["Sektor_Keuangan", "Sektor_Infrastruktur"], [], "PASAR", None),
 ("N48", "2026-10-21", "Kontan", "https://investasi.kontan.co.id/news/cds-indonesia-terus-menanjak-sentimen-msci-tekan-persepsi-risiko-investor", "CDS Indonesia Terus Menanjak, Sentimen MSCI Tekan Persepsi Risiko Investor", "BeritaMakroGeopolitik", 0.9, ["Ev_MSCI_KonsultasiStandalone_Okt2026"], [], [], "MSCI", None),
 ("N49", "2026-09-17", "Investortrust", "https://investortrust.id/market/116614/the-fed-naikkan-suku-bunga-ke-3-754-00-ini-implikasinya-bagi-pasar-obligasi-indonesia", "The Fed Naikkan Suku Bunga ke 3,75%-4,00%, Ini Implikasinya bagi Pasar Obligasi Indonesia", "BeritaMakroGeopolitik", 0.9, ["Ev_FedHike_Sep2026"], [], [], "BUNGA", None),
 ("N50", "2026-09-19", "KabarBursa", "https://www.kabarbursa.com/makro/emas-spot-sentuh-usd439011-antam-diprediksi-capai-rp32-juta-per-gram", "Emas Spot Sentuh USD4.390,11, Antam Diprediksi Capai Rp3,2 Juta per Gram", "BeritaMakroGeopolitik", 0.8, ["Ev_EmasRekor_2026"], [], ["ANTM"], "EMAS", 1),
 ("N51", "2026-08-13", "KabarBursa", "https://www.kabarbursa.com/makro/msci-coret-goto-dan-cpin-bukan-masalah-besar-november-justru-jadi-penentu", "MSCI Coret GOTO dan CPIN, Bukan Masalah Besar, November Justru Jadi Penentu", "BeritaEmiten", 0.8, ["Ev_MSCI_ReviewAgustus2026"], [], ["GOTO", "CPIN"], None, None),
 ("N52", "2026-10-01", "KabarBursa", "https://www.kabarbursa.com/market-hari-ini/hsbc-pasang-target-ihsg-6200-ruang-penguatan-tinggal-17-persen", "HSBC Pasang Target IHSG 6.200, Rupiah Mulai Stabil dan Modal Mulai Kembali", "BeritaRisetAnalis", 0.85, [], [], [], "PASAR", None),
 ("N53", "2026-02-06", "Bisnis.com", "https://market.bisnis.com/read/20260206/92/1950691/premi-risiko-cds-indonesia-naik-tipis-usai-moody-s-turunkan-outlook-utang-ri-ke-negatif", "Premi Risiko (CDS) Indonesia Naik Tipis Usai Moody's Turunkan Outlook Utang RI ke Negatif", "BeritaMakroGeopolitik", 0.9, ["Ev_MoodysOutlookNegatif_Feb2026"], [], [], "PASAR", None),
 ("N54", "2026-08-13", "Bisnis.com", "https://market.bisnis.com/read/20260813/7/1995834/msci-umumkan-jadwal-8-index-review-hingga-agustus-2028", "MSCI Umumkan Jadwal 8 Index Review hingga Agustus 2028 (Nov 2026: umum 11 Nov, efektif 1 Des)", "BeritaMakroGeopolitik", 0.9, [], [], [], None, None),
]

# ------------------------------------------------------------------ SKENARIO
# nama, label, aktif, probabilitas, fase, arah[12 faktor], cbr(fed, minyak, usd, riskoff, komoditas, inflasi), deskripsi
SKENARIO = [
 ("Skenario_Base_2027_2028", "Base Case 2027-2028: Normalisasi Bertahap", 1, 0.50, "Fase_LateCycle",
  [1, 1, 1, 1, 1, 0, 1, 1, -1, 1, 1, 1], (2, 2, 2, 2, 1, 1),
  "Premi risiko Timur Tengah bertahan namun minyak menormal ke US$80-90; Fed (sudah naik ke 4%) tahan tinggi lalu turun 2027; rupiah lemah; konsultasi MSCI standalone berlarut hingga Jun 2027; emas kuat tetapi tertahan kenaikan Fed (arah +1)."),
 ("Skenario_Bull_Pemulihan", "Bull Case: Pemulihan & Re-rating", 0, 0.25, "Fase_EarlyCycle",
  [0, -1, -1, 0, 1, 1, -2, 2, 1, 0, 1, 2], (-1, 0, -1, -1, 1, 0),
  "Fed pivot, reformasi free float diterima: MSCI mempertahankan status EM & mencabut freeze, asing kembali ke big caps, rupiah menguat."),
 ("Skenario_Bear_Stagflasi", "Bear Case: Stagflasi & Reklasifikasi", 0, 0.25, "Fase_ResesiStagflasi",
  [2, 2, 2, 2, 2, -1, 2, 0, -2, 2, 1, 0], (2, 2, 2, 2, 0, 2),
  "Hormuz tertutup lagi, Brent >US$120, Fed naik ke 4,5%, BI Rate 6,5%, MSCI final menetapkan Indonesia standalone (Jun 2027)."),
]

# ------------------------------------------------------------------ KASUS HISTORIS (CBR)
# nama, label, tahun, cbr(fed, minyak, usd, riskoff, komoditas, inflasi), unggul[], terpuruk[], pelajaran
PERIODE = [
 ("Kasus_Krisis1998", "Krisis Moneter Asia 1997-98", 1998, (0, -1, 2, 2, 0, 2), ["Energi", "BarangBaku"], ["Keuangan", "PropertiRealEstat"], "Eksportir berpendapatan USD selamat; bank & properti berutang USD kolaps."),
 ("Kasus_GFC_2008", "Krisis Keuangan Global 2008", 2008, (-2, -2, 2, 2, -2, 0), ["KonsumenPrimer", "Kesehatan"], ["Energi", "BarangBaku", "PropertiRealEstat"], "IHSG -50% (2008) lalu +87% (2009); pemulihan dipimpin komoditas & bank."),
 ("Kasus_TaperTantrum_2013", "Taper Tantrum 2013", 2013, (1, 0, 2, 1, -1, 2), ["KonsumenPrimer", "Infrastruktur"], ["PropertiRealEstat", "Keuangan"], "Rupiah anjlok, BI naikkan bunga agresif; properti terpukul paling dalam."),
 ("Kasus_DevaluasiYuan_2015", "Devaluasi Yuan & Jatuhnya Komoditas 2015", 2015, (1, -2, 2, 1, -2, 0), ["KonsumenPrimer", "Kesehatan"], ["Energi", "BarangBaku", "Perindustrian"], "Komoditas jatuh; defensif unggul."),
 ("Kasus_FedHike_PerangDagang_2018", "Kenaikan Fed & Perang Dagang 2018", 2018, (2, 1, 2, 1, 0, 0), ["Energi", "Keuangan"], ["PropertiRealEstat", "KonsumenNonPrimer"], "Batu bara tinggi; bank besar relatif tahan; properti & ritel tertekan."),
 ("Kasus_COVID_2020", "Pandemi COVID-19 2020", 2020, (-2, -2, 1, 2, -1, -1), ["Kesehatan", "Teknologi"], ["TransportasiLogistik", "PropertiRealEstat", "Energi"], "IHSG ke 3.937 (Mar 2020); kesehatan & digital memimpin."),
 ("Kasus_Supercycle_2022", "Supercycle Komoditas & Perang Rusia-Ukraina 2022", 2022, (2, 2, 2, 1, 2, 2), ["Energi", "BarangBaku", "Keuangan"], ["Teknologi", "PropertiRealEstat"], "Batu bara & nikel melonjak; bank big-4 rekor; teknologi runtuh."),
 ("Kasus_SVB_PuncakBunga_2023", "SVB & Puncak Suku Bunga 2023", 2023, (1, 0, 1, 1, -1, 1), ["Keuangan", "Infrastruktur"], ["Energi", "Teknologi"], "Normalisasi batu bara; bank & telko unggul."),
 ("Kasus_TarifAS_2025", "Shock Tarif AS 2025", 2025, (0, -1, -1, 2, 0, 0), ["BarangBaku"], ["Teknologi", "KonsumenNonPrimer"], "Emas rekor; penambang emas memimpin."),
]

# ------------------------------------------------------------------ STAKEHOLDER
# nama, kelas, label, kebutuhan, mengonsumsi[], profil, horizon, modal
STAKEHOLDER = [
 ("Stk_MitraSekuritas", "StakeholderUtama", "Perusahaan Sekuritas Mitra Implementasi", "Fitur riset sektoral prediktif yang embedded di aplikasi trading; meningkatkan retensi & kepercayaan nasabah ritel.",
  ["Output_PrediksiSektor", "Output_TopPickEmiten", "Output_KesehatanFundamental", "Output_SinyalQuantTrade", "Output_SkenarioWhatIf", "Output_KecocokanProfil", "Output_PenjelasanEdukatif", "Output_PeringatanRisiko"], None, None, None),
 ("Stk_TimEquityResearch", "StakeholderKandidat", "Tim Riset Ekuitas (Equity Research)", "Outlook sektoral yang konsisten & dapat ditelusuri jejak alasannya.", ["Output_PrediksiSektor", "Output_SkenarioWhatIf", "Output_KesehatanFundamental"], None, None, None),
 ("Stk_AnalisJunior", "StakeholderKandidat", "Analis Junior Sekuritas", "Alat bantu penalaran terstruktur & pembelajaran heuristik pakar.", ["Output_PenjelasanEdukatif", "Output_PrediksiSektor"], None, None, None),
 ("Stk_ManajerInvestasi", "StakeholderKandidat", "Manajer Investasi / Fund Manager", "Sinyal rotasi sektor untuk alokasi portofolio & manajemen risiko outflow pasif.", ["Output_PrediksiSektor", "Output_SkenarioWhatIf", "Output_PeringatanRisiko"], None, None, None),
 ("Stk_EdukatorKomunitas", "StakeholderKandidat", "Edukator & Komunitas Investasi", "Materi belajar berbasis kasus nyata & penalaran pakar.", ["Output_PenjelasanEdukatif"], None, None, None),
 ("Stk_PanelPakar", "Validator", "Panel Pakar / Analis Senior", "Memvalidasi bobot, ambang aturan, dan hasil backtest walk-forward.", ["Output_PrediksiSektor", "Output_TopPickEmiten"], None, None, None),
 ("Stk_OJK_Kepatuhan", "RegulatorStakeholder", "OJK (Konteks Kepatuhan)", "Sistem diposisikan sebagai alat riset & edukasi, bukan nasihat investasi personal; wajib disclaimer.", [], None, None, None),
 ("Stk_BEI_Kepatuhan", "RegulatorStakeholder", "BEI (Konteks Data & Aturan Perdagangan)", "Kepatuhan penggunaan data pasar & aturan perdagangan.", [], None, None, None),
 ("Persona_Mahasiswa_Konservatif", "InvestorRitel", "Persona: Mahasiswa, Konservatif", "Modal kecil, ingin dividen & keamanan, horizon 1-3 tahun.", ["Output_PenjelasanEdukatif", "Output_KecocokanProfil"], "ProfilKonservatif", "Horizon_Menengah", 5.0),
 ("Persona_PekerjaMuda_Moderat", "InvestorRitel", "Persona: Pekerja Muda, Moderat", "Menabung rutin (DCA) di saham sektor unggulan.", ["Output_PrediksiSektor", "Output_TopPickEmiten", "Output_KecocokanProfil"], "ProfilModerat", "Horizon_Menengah", 25.0),
 ("Persona_GenZ_Agresif", "InvestorRitel", "Persona: Gen Z, Agresif (Swing)", "Mencari momentum, rawan FOMO; butuh peringatan distribusi.", ["Output_SinyalQuantTrade", "Output_PeringatanRisiko"], "ProfilAgresif", "Horizon_Pendek", 10.0),
 ("Persona_TraderScalper", "InvestorRitel", "Persona: Trader Scalper", "Entry-exit intraday berbasis VWAP & order book.", ["Output_SinyalQuantTrade"], "ProfilAgresif", "Horizon_Intraday", 50.0),
]

KELUARAN_SDG = {
 "Output_PrediksiSektor": ["SDG8_DecentWork"], "Output_TopPickEmiten": ["SDG8_DecentWork", "SDG1_NoPoverty"],
 "Output_KesehatanFundamental": ["SDG1_NoPoverty"], "Output_SinyalQuantTrade": ["SDG8_DecentWork"],
 "Output_SkenarioWhatIf": ["SDG4_QualityEducation"], "Output_KecocokanProfil": ["SDG10_ReducedInequalities"],
 "Output_PenjelasanEdukatif": ["SDG4_QualityEducation", "SDG10_ReducedInequalities"], "Output_PeringatanRisiko": ["SDG1_NoPoverty"],
}

SEKTOR_KATEGORI = {
 "Sektor_Energi": "SektorKomoditas", "Sektor_BarangBaku": "SektorKomoditas", "Sektor_Perindustrian": "SektorSiklikal",
 "Sektor_KonsumenPrimer": "SektorDefensif", "Sektor_KonsumenNonPrimer": "SektorSiklikal", "Sektor_Kesehatan": "SektorDefensif",
 "Sektor_Keuangan": "SektorSiklikal", "Sektor_PropertiRealEstat": "SektorSiklikal", "Sektor_Teknologi": "SektorSiklikal",
 "Sektor_Infrastruktur": "SektorDefensif", "Sektor_TransportasiLogistik": "SektorSiklikal",
}


# ------------------------------------------------------------------ v2: data berita dari CSV (bila ada)
import os as _os, csv as _csv
_CSV_BERITA = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "berita.csv")
if _os.path.exists(_CSV_BERITA):
    _sp = lambda x: [y.strip() for y in (x or "").split(";") if y.strip()]
    with open(_CSV_BERITA, encoding="utf-8-sig", newline="") as _f:
        BERITA = [(r["id"], r["tanggal"], r["media"], r["url"], r["judul"], r["kelas"], float(r["kredibilitas"].replace(",", ".")),
                   _sp(r["peristiwa"]), _sp(r["sektor"]), _sp(r["emiten"]), (r["variabel"] or None),
                   (int(r["arah_manual"]) if (r.get("arah_manual") or "").strip() else None))
                  for r in __import__('kb_market').baca_dict_csv(_f) if (r.get("id") or "").strip()]
