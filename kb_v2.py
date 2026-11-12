# -*- coding: utf-8 -*-
"""
v2 — LAPISAN PAKAR LANJUTAN (Expert Layer v2)
Kondisi pasar & deteksi regime, bobot adaptif per regime, reaction function kebijakan, katalis terjadwal,
tesis investasi + kriteria invalidasi, data tambahan emiten (revisi laba, tata kelola), emiten uji (unit test aturan),
dan heuristik pakar v2.
"""
import datetime
from kb_geo import TODAY

TAXONOMY_V2 = r"""
SumberData | Thing | Sumber Data | Asal data yang memasok basis pengetahuan (resmi, pasar, alternatif, berita).
SumberDataResmi | SumberData | Sumber Data Resmi | Otoritas & lembaga pemerintah (IDX, KSEI, OJK, BI, BPS, Kemenkeu, ESDM, Fed).
SumberDataPasar | SumberData | Penyedia Data Pasar | Terminal, aplikasi broker, penyedia indeks & harga.
SumberDataAlternatif | SumberData | Data Alternatif & Geopolitik | GDELT, GPR Index, ACLED, AIS kapal, Google Trends, satelit.
SumberDataBerita | SumberData | Media & Riset | Media nasional/global, riset sekuritas, media sosial.
IndikatorKatalog | Thing | Katalog Indikator | Definisi indikator yang dapat/telah dimasukkan ke sistem beserta sifat waktunya.
IndikatorLeading | IndikatorKatalog | Indikator Leading | Bergerak mendahului harga/ekonomi (CDS, revisi konsensus, PMI, breadth).
IndikatorCoincident | IndikatorKatalog | Indikator Coincident | Bergerak bersamaan (harga, kurs, volume).
IndikatorLagging | IndikatorKatalog | Indikator Lagging | Mengonfirmasi setelah kejadian (laba, inflasi, rasio keuangan).
PenandaKualitasData | Thing | Penanda Kualitas Data | Penanda asal & kualitas data (indikatif, terverifikasi).
DataIndikatif | PenandaKualitasData | Data Indikatif | Data snapshot/indikatif yang wajib diverifikasi sebelum keputusan.
DataKedaluwarsa | KategoriInferensi | Data Kedaluwarsa | (Inferensi) umur data > 5 × frekuensi pembaruannya.
PerluVerifikasiData | KategoriInferensi | Perlu Verifikasi Data | (Inferensi) rekomendasi bertumpu pada data indikatif/kedaluwarsa.
KondisiPasar | PenalaranPakar | Kondisi Pasar (State Vector) | Vektor keadaan pasar terkini untuk deteksi regime.
KondisiPasarAktif | KategoriInferensi | Kondisi Pasar Aktif | (Inferensi) state yang dipakai penalaran.
RegimePasar | PenalaranPakar | Regime Pasar | Rezim pasar dengan bobot pilar berbeda (meta-knowledge pakar).
RegimeAktif | KategoriInferensi | Regime Aktif | (Inferensi) regime terdeteksi dari skor stres pasar.
InferensiPasar | KategoriInferensi | Inferensi Level Pasar | Kesimpulan atas keadaan pasar keseluruhan.
KapitulasiPasar | InferensiPasar | Kapitulasi Pasar | Drawdown ≥ 40% + hari crash ≥ 10%: penjualan paksa/panik selesai sebagian.
BreadthWashout | InferensiPasar | Breadth Washout | ≤ 25% saham di atas MA200 (jenuh jual luas).
ZonaAkumulasiGenerasional | InferensiPasar | Zona Akumulasi Generasional | Kapitulasi + washout + premi risiko tinggi: peluang 1-3 th terbaik secara historis.
DasarBelumTerkonfirmasi | InferensiPasar | Dasar Belum Terkonfirmasi | CDS & rupiah masih memburuk: jangan all-in, akumulasi bertahap.
DivergensiIntermarketBullish | InferensiPasar | Divergensi Intermarket Bullish | CDS & rupiah membaik mendahului IHSG (sinyal dasar).
StrategiAkumulasiBertahap | InferensiPasar | Strategi Akumulasi Bertahap | Rencana masuk 3 tranche.
PremiRisikoNegaraTinggi | InferensiPasar | Premi Risiko Negara Tinggi | CDS 5Y ≥ 90 bps.
AntisipasiKebijakan | PenalaranPakar | Antisipasi Reaksi Kebijakan | Reaction function otoritas yang diantisipasi pakar sebelum diumumkan.
AntisipasiTerpicu | KategoriInferensi | Antisipasi Terpicu | (Inferensi) kondisi pemicu reaction function terpenuhi.
Katalis | PenalaranPakar | Katalis Terjadwal | Peristiwa terjadwal yang dapat menggerakkan harga.
KatalisBiner | Katalis | Katalis Biner | Hasil dua arah dengan dampak besar (FOMC, MSCI, pemilu).
KatalisMusiman | Katalis | Katalis Musiman | Pola kalender (window dressing, Ramadan-Lebaran, musim dividen).
KatalisTerjadwal | Katalis | Katalis Terjadwal Rutin | Rilis laporan keuangan, rebalancing indeks.
KatalisDekat | KategoriInferensi | Katalis Dekat | (Inferensi) katalis ≤ 45 hari ke depan.
TesisInvestasi | PenalaranPakar | Tesis Investasi | Alasan utama sebuah posisi + indikator kunci + kriteria invalidasi (kill switch).
TesisValid | KategoriInferensi | Tesis Valid | (Inferensi) indikator kunci masih dalam batas tesis.
TesisGugur | KategoriInferensi | Tesis Gugur | (Inferensi) indikator kunci menembus batas invalidasi: keluar.
TesisRapuh | KategoriInferensi | Tesis Rapuh | (Inferensi) jarak ke batas invalidasi < 10%.
TesisTerpicu | KategoriInferensi | Tesis Kontrarian Terpicu | (Inferensi) syarat pemicu tesis kontrarian terpenuhi.
TesisPerluDataBaru | KategoriInferensi | Tesis Perlu Data Baru | (Inferensi) indikator kunci tesis kedaluwarsa.
EmitenUji | Emiten | Emiten Hipotetis (Uji Aturan) | Emiten fiktif untuk pengujian aturan (validation & verification), BUKAN saham nyata.
SinyalKetahananBeritaBuruk | InferensiEmiten | Ketahanan terhadap Berita Buruk | Berita negatif tetapi harga mengungguli pasar & bandar akumulasi (bad news priced-in).
SellTheNews | InferensiEmiten | Sell the News | Berita positif tetapi harga kalah dari pasar & bandar distribusi.
OutperformPasar | InferensiEmiten | Mengungguli Pasar | Kekuatan relatif vs IHSG ≥ +5 pp.
UnderperformPasar | InferensiEmiten | Kalah dari Pasar | Kekuatan relatif vs IHSG ≤ -5 pp.
KapitulasiEmiten | InferensiEmiten | Kapitulasi Emiten | Volume ≥ 1,8×, RSI < 35, turun ≥ 15% sebulan.
RevisiLabaNaik | InferensiEmiten | Revisi Laba Naik | Konsensus EPS 3 bulan direvisi naik ≥ 5%.
RevisiLabaTurun | InferensiEmiten | Revisi Laba Turun | Konsensus EPS 3 bulan direvisi turun ≥ 5%.
CelahEkspektasiPositif | InferensiEmiten | Celah Ekspektasi Positif | Laba direvisi naik & murah, tetapi harga belum bereaksi (teknikal ≤ 4).
MurahKarenaLabaTurun | InferensiEmiten | Murah karena Laba Turun | Undervalued + revisi turun: peringatan dini value trap.
ERPSangatMenarik | InferensiEmiten | ERP Sangat Menarik | Earnings yield − yield SBN ≥ 8 pp.
ERPMenarik | InferensiEmiten | ERP Menarik | 4 ≤ ERP < 8 pp.
MahalVsObligasi | InferensiEmiten | Mahal vs Obligasi | ERP < 0 (SBN lebih menarik).
RisikoHSC | InferensiEmiten | Risiko HSC / Free Float Rendah | Free float < 15%: risiko dikeluarkan dari IHSG/MSCI.
RisikoForcedSellPengendali | InferensiEmiten | Risiko Forced Sell Pengendali | Saham pengendali digadaikan ≥ 30% saat downtrend.
SinyalOrangDalam | InferensiEmiten | Sinyal Pembelian Orang Dalam | Direksi/pengendali membeli saat undervalued.
IndikasiSahamGorengan | InferensiEmiten | Indikasi Saham Gorengan | Free float kecil, ARA beruntun, volume meledak, broker terkonsentrasi.
RisikoPumpAndDump | InferensiEmiten | Risiko Pump & Dump | Gorengan + overvalued + RSI ≥ 80.
KonflikFundamentalVsBandar | InferensiEmiten | Konflik: Fundamental vs Bandar | Fundamental kuat tetapi bandar distribusi.
MomentumTanpaFundamental | InferensiEmiten | Momentum tanpa Fundamental | Tren naik tetapi fundamental lemah.
DistribusiSaatEuforia | InferensiEmiten | Distribusi saat Euforia | Sentimen positif tetapi bandar distribusi.
TungguKonfirmasi | InferensiEmiten | Tunggu Konfirmasi | Ada konflik sinyal antarpilar: tunda entry penuh.
KonfluensiTinggi | InferensiEmiten | Konfluensi Tinggi | ≥ 5 dari 6 pilar searah bullish.
KonfluensiRendah | InferensiEmiten | Konfluensi Rendah | ≤ 2 dari 6 pilar bullish.
KandidatTopPickAdaptif | InferensiEmiten | Top Pick Adaptif-Regime | Skor terbobot regime ≥ ambang regime & sektor ber-ekspektasi ≥ 2.
KandidatAkumulasiBertahap | InferensiEmiten | Kandidat Akumulasi Bertahap | Saat kapitulasi: kualitas + murah + jejak akumulasi → beli 3 tranche.
StrategiTrancheKatalisBiner | InferensiEmiten | Strategi Tranche Sebelum Katalis Biner | Kandidat dengan katalis biner ≤ 45 hari: jangan full position.
RisikoKonsentrasiTema | InferensiEmiten | Risiko Konsentrasi Tema | Dua top pick berbagi eksposur komoditas yang sama.
SektorRobustLintasSkenario | InferensiSektor | Sektor Robust Lintas Skenario | Bullish di Base & Bull dan tidak bearish di Bear.
SektorAsimetriPositif | InferensiSektor | Sektor Asimetri Positif | Upside (Bull−Base) ≥ 1,5 × downside (Base−Bear) dan ekspektasi ≥ 2.
SektorKatalisDekat | InferensiSektor | Sektor dengan Katalis Dekat | Ada katalis ≤ 45 hari untuk sektor ini.
SektorPerluPemantauanKetat | InferensiSektor | Sektor Perlu Pemantauan Ketat | Tesis sektor rapuh atau gugur.
SektorPilihanInti | InferensiSektor | Sektor Pilihan Inti (Core) | Bullish & robust lintas skenario: porsi utama portofolio.
SektorPilihanSatelit | InferensiSektor | Sektor Pilihan Satelit | Taruhan asimetris kontrarian: porsi kecil, menunggu pemicu.
"""

# ------------------------------------------------------------------ KONDISI PASAR (state vector, 26 Okt 2026)
KONDISI = dict(
    nama="Pasar_ID_Okt2026", label="Kondisi Pasar Indonesia per 26 Okt 2026",
    drawdownIHSGPersen=round((4996.61 / 8646.0 - 1) * 100, 2),        # vs akhir 2025
    perubahanIHSG1BulanPersen=round((4996.61 / 6095.86 - 1) * 100, 2),  # 30 Sep -> 19 Okt
    penurunanHarianTerbesarPersen=-11.57, netAsingYTDT=-88.19, cds5YBps=99.73, yieldSBN10Y=7.14,
    spreadSBNUSTBps=216.0, kursUSDIDR=17938.0, inflasiYoY=3.28, biRatePersen=5.75, ffrAtasPersen=4.00,
    brentUSD=106.65, emasUSD=4390.11, trenCDS1Bulan=1, trenRupiah1Bulan=1, trenYieldSBN1Bulan=0,
)

import os as _os, csv as _csv
_CSV_KONDISI = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "kondisi_pasar.csv")
if _os.path.exists(_CSV_KONDISI):
    with open(_CSV_KONDISI, encoding="utf-8-sig", newline="") as _f:
        for _r in __import__('kb_market').baca_dict_csv(_f):
            if (_r.get("variabel") or "").strip():
                KONDISI[_r["variabel"].strip()] = float(_r["nilai"].replace(",", "."))

# ------------------------------------------------------------------ REGIME & BOBOT (meta-knowledge)
# nama, label, deskripsi, bobot (F, V, T, B, S, Sektor, Risiko, Likuiditas, SmartMoney), risiko/transaksi %, tranche (%)
REGIME = [
 ("Regime_KrisisLikuiditas", "Krisis Likuiditas / Kapitulasi",
  "Harga digerakkan penjualan paksa. Pakar: utamakan neraca kuat & valuasi, ikuti jejak smart money, abaikan teknikal jangka pendek & kebisingan sentimen, hukum berat neraca lemah, risiko per transaksi dipangkas setengah.",
  (1.5, 1.5, 0.5, 1.0, 0.5, 1.0, 1.5, 1.0, 1.5), 0.5, (30, 30, 40)),
 ("Regime_RiskOff", "Risk-Off Normal",
  "Tekanan makro tanpa kepanikan. Kualitas & aliran dana lebih penting dari momentum.",
  (1.2, 1.0, 0.8, 1.2, 0.8, 1.0, 1.2, 1.0, 1.2), 0.75, (40, 30, 30)),
 ("Regime_Netral", "Netral", "Semua pilar berbobot sama.", (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), 1.0, (50, 30, 20)),
 ("Regime_RiskOn", "Risk-On / Euforia",
  "Likuiditas melimpah: momentum & aliran dana bekerja, valuasi kurang menentukan; waspada distribusi.",
  (0.8, 0.7, 1.3, 1.2, 1.2, 1.0, 0.8, 1.0, 1.0), 1.0, (60, 40, 0)),
]
MAKS_PILAR = (10, 3, 7, 5, 2, 4, 0, 2, 2)   # nilai maksimum tiap pilar

# ------------------------------------------------------------------ ANTISIPASI KEBIJAKAN
ANTISIPASI = [
 ("Antisipasi_BIHikePreemptif", "BI Naikkan Suku Bunga Pre-emptif", "Rupiah ≥ 17.500 & inflasi ≥ 3% → BI cenderung menaikkan bunga sebelum konsensus.", "Mv_SukuBungaBINaik"),
 ("Antisipasi_PenyesuaianBBM", "Penyesuaian Harga BBM / Subsidi", "Brent ≥ US$100 → tekanan subsidi → probabilitas kenaikan harga BBM.", "Mv_KenaikanHargaBBM"),
 ("Antisipasi_OutflowSBN", "Outflow Asing dari SBN", "Fed ≥ 4% & spread SBN-UST ≤ 225 bps → daya tarik SBN turun.", "Mv_OutflowSBN"),
 ("Antisipasi_StabilisasiPasar", "Stabilisasi Pasar oleh Otoritas & Institusi Domestik", "Drawdown ≤ -35% → buyback tanpa RUPS, dana pensiun/BUMN membeli blue chip (buyer of last resort).", "Mv_DukunganLikuiditasDomestik"),
 ("Antisipasi_PremiRisikoNegara", "Kenaikan Premi Risiko Negara", "CDS ≥ 90 bps → asing mengurangi eksposur Indonesia.", "Mv_PremiRisikoNegaraNaik"),
]

# ------------------------------------------------------------------ KATALIS (tanggal; "≈" = perkiraan)
KATALIS = [
 ("K_FOMC_Okt2026", "KatalisBiner", "FOMC 28 Okt 2026", "2026-10-28", ["Sektor_Keuangan", "Sektor_PropertiRealEstat", "Sektor_Teknologi"], [], "Peluang kenaikan lanjutan."),
 ("K_RilisLK_Q3_2026", "KatalisTerjadwal", "Batas rilis laporan keuangan Q3-2026 (≈31 Okt)", "2026-10-31", [], ["LQ45"], "Earnings surprise & revisi konsensus."),
 ("K_PemiluSelaAS", "KatalisBiner", "Pemilu Sela AS 3 Nov 2026", "2026-11-03", ["Sektor_Teknologi", "Sektor_Energi"], [], "Arah kebijakan tarif/fiskal AS."),
 ("K_MSCI_ReviewNov2026", "KatalisBiner", "MSCI Index Review Nov 2026 (umum 11 Nov)", "2026-11-11", [], ["MSCI_Indonesia"], "Freeze FIF/NOS dicabut atau diperpanjang."),
 ("K_MSCI_EfektifDes2026", "KatalisTerjadwal", "Efektif MSCI Review (1 Des 2026)", "2026-12-01", [], ["MSCI_Indonesia"], "Eksekusi aliran pasif."),
 ("K_RDG_BI_Nov2026", "KatalisBiner", "RDG Bank Indonesia 17-18 Nov 2026", "2026-11-18", ["Sektor_Keuangan", "Sektor_PropertiRealEstat"], [], "Konsensus ekonom: BI-Rate naik 25 bps ke 6% untuk menjaga rupiah."),
 ("K_FOMC_Des2026", "KatalisBiner", "FOMC 9 Des 2026", "2026-12-09", ["Sektor_Keuangan", "Sektor_PropertiRealEstat"], [], ""),
 ("K_RDG_BI_Des2026", "KatalisBiner", "RDG Bank Indonesia 15-16 Des 2026", "2026-12-16", ["Sektor_Keuangan", "Sektor_PropertiRealEstat"], [], ""),
 ("K_WindowDressing", "KatalisMusiman", "Window dressing akhir tahun (≈pertengahan Des)", "2026-12-15", [], ["LQ45"], "Big caps cenderung dijaga menjelang tutup buku."),
 ("K_EvaluasiLQ45_Jan2027", "KatalisTerjadwal", "Evaluasi mayor LQ45 (≈akhir Jan 2027)", "2027-01-25", [], ["LQ45"], "Keluar-masuk konstituen."),
 ("K_MSCI_ReviewFeb2027", "KatalisBiner", "MSCI Index Review Feb 2027 (umum 9 Feb)", "2027-02-09", [], ["MSCI_Indonesia"], ""),
 ("K_RamadanLebaran2027", "KatalisMusiman", "Ramadan-Lebaran 2027 (≈Feb-Mar)", "2027-02-08", ["Sektor_KonsumenPrimer", "Sektor_KonsumenNonPrimer"], [], "Puncak konsumsi."),
 ("K_MusimDividen2027", "KatalisMusiman", "Musim RUPS & dividen (≈Mar-Jun 2027)", "2027-03-15", [], ["IDXHIDIV20"], "Dividend play."),
 ("K_BatasKonsultasiMSCI", "KatalisBiner", "Batas akhir konsultasi MSCI (30 Apr 2027)", "2027-04-30", [], ["MSCI_Indonesia"], ""),
 ("K_KeputusanFinalMSCI", "KatalisBiner", "Keputusan final MSCI standalone (≈akhir Jun 2027)", "2027-06-30", ["Sektor_Keuangan", "Sektor_Infrastruktur"], ["MSCI_Indonesia"], "Katalis terbesar horizon 1-3 th."),
]
for i, kt in enumerate(KATALIS):
    pass
def hari_menuju(tgl):
    return (datetime.date.fromisoformat(tgl) - TODAY).days

# ------------------------------------------------------------------ TESIS INVESTASI & KILL SWITCH
# nama, label, sektor, indikator kunci (individu Makro_*), invalidasi bawah, invalidasi atas, pemicu bawah (None), deskripsi
TESIS = [
 ("Tesis_BarangBaku_EmasNikel", "Tesis: Emas & nikel menopang Barang Baku", "Sektor_BarangBaku", "Makro_Emas", 3800.0, 1e9, None,
  "Emas tetap tinggi (safe haven, bank sentral) & kuota nikel. Gugur bila emas < US$3.800."),
 ("Tesis_Energi_PremiGeopolitik", "Tesis: Premi geopolitik minyak", "Sektor_Energi", "Makro_Brent", 75.0, 1e9, None,
  "Premi risiko Timur Tengah menjaga harga energi. Gugur bila Brent < US$75 (de-eskalasi penuh)."),
 ("Tesis_Kesehatan_Defensif", "Tesis: Kesehatan defensif", "Sektor_Kesehatan", "Makro_USDIDR", 0.0, 19500.0, None,
  "Permintaan stabil & valuasi turun. Gugur bila USD/IDR > 19.500 (bahan baku impor)."),
 ("Tesis_Keuangan_Kontrarian", "Tesis kontrarian: Big banks pasca-kapitulasi", "Sektor_Keuangan", "Makro_CDS5Y", 0.0, 150.0, 85.0,
  "Diskon ekstrem akibat outflow pasif. Terpicu bila CDS < 85 bps; gugur bila CDS > 150 bps."),
 ("Tesis_Infrastruktur_DataCenter", "Tesis kontrarian: Infrastruktur digital", "Sektor_Infrastruktur", "Makro_YieldSBN10Y", 0.0, 8.0, 6.75,
  "Data center & konsolidasi telko. Terpicu bila yield SBN < 6,75%; gugur bila > 8%."),
 ("Tesis_KonsumenPrimer_MBG", "Tesis: Konsumen primer (MBG & CPO)", "Sektor_KonsumenPrimer", "Makro_InflasiID", 0.0, 5.0, None,
  "Belanja MBG & biodiesel. Gugur bila inflasi > 5% (daya beli runtuh)."),
]

# frekuensi pembaruan (hari) untuk indikator makro bernilai -> kesegaran data
FREKUENSI_MAKRO = {
 "Makro_FedFundsRate": 45, "Makro_CorePCE_US": 30, "Makro_BIRate": 30, "Makro_DepositFacility": 30, "Makro_InflasiID": 30,
 "Makro_USDIDR": 1, "Makro_IHSG": 1, "Makro_IHSG_Akhir2025": 365, "Makro_NetSellAsingH1": 180, "Makro_Brent": 1, "Makro_WTI": 1,
 "Makro_ProyeksiBrentEIA": 30, "Makro_ProyeksiBrentGS": 30, "Makro_Emas": 1, "Makro_RatingSP": 180, "Makro_CDS5Y": 1,
 "Makro_YieldSBN10Y": 1, "Makro_UST10Y": 1, "Makro_SpreadSBN_UST": 1, "Makro_NetAsingYTD": 1, "Makro_IHSG_16Okt": 365,
 "Makro_IHSG_30Sep": 365, "Makro_EstimasiOutflowPasif": 90,
}

# ------------------------------------------------------------------ DATA TAMBAHAN EMITEN (indikatif)
# revisi konsensus EPS 3 bulan (%), saham digadaikan (%), transaksi orang dalam (+1/0/-1), konsentrasi top-3 broker (%), ARA dalam 5 hari
REVISI = {
 "ANTM": 8, "BRMS": 10, "MDKA": 5, "AMMN": 6, "TINS": 6, "NCKL": 5, "INCO": 3, "INKP": -4, "SMGR": -10,
 "AADI": -5, "PTBA": -8, "ITMG": -7, "MEDC": 4, "PGAS": 0, "AKRA": -2,
 "BBCA": -3, "BBRI": -8, "BMRI": -5, "BBNI": -6, "BRIS": 2, "BBTN": -4,
 "TLKM": -4, "ISAT": 2, "EXCL": -6, "TOWR": -3, "MTEL": 0, "JSMR": -2,
 "ICBP": 0, "INDF": 1, "MYOR": -5, "CPIN": 5, "JPFA": 6, "AMRT": -3, "AALI": 7, "LSIP": 7, "DSNG": 7, "UNVR": -10,
 "MAPI": -6, "MAPA": -3, "ACES": -8, "ERAA": -4, "AUTO": -2,
 "KLBF": -1, "SIDO": 1, "MIKA": 3, "HEAL": 5, "SILO": 3,
 "ASII": -4, "UNTR": -3, "IMPC": 5, "CTRA": -5, "BSDE": -7, "PWON": -4, "SMRA": -10, "DMAS": -5,
 "GOTO": 0, "BUKA": -5, "DCII": 5, "MTDL": 0, "EMTK": 0, "BIRD": -2, "ASSA": 0, "SMDR": 3, "TMAS": 2,
}

# Emiten uji (fiktif) — format sama dengan EMITEN_TABLE (41 kolom) + ekstra
EMITEN_UJI_TABLE = r"""
UJI_GORENG|PT Uji Gorengan Tbk (FIKTIF)|Sektor_Perindustrian|Sub_BahanBangunan|0|0|0|750|1.2|40|8|85.0|30.0|9.0|5|1.8|3|-20|0.4|0|0|1.5|-1.5|45|120|60|88|1|4.5|9.0|-25|0|35|80|2.0|2.5|||||Grup_Uji
UJI_GADAI|PT Uji Gadai Pengendali Tbk (FIKTIF)|Sektor_Perindustrian|Sub_BahanBangunan|0|0|0|400|3.0|25|30|6.0|10.0|0.8|9|1.2|6|-10|0.8|2|20|2.2|-2.4|-8|-30|-12|30|-1|1.6|4.0|-15|-10|5|-25|-0.5|0.7|||||Grup_Uji
UJI_INSIDER|PT Uji Pembelian Direksi Tbk (FIKTIF)|Sektor_Perindustrian|Sub_BahanBangunan|0|0|0|900|5.0|30|35|6.0|12.0|1.0|18|0.3|14|12|1.2|5|40|4.0|-2.6|-3|-12|-6|42|1|1.2|3.0|15|5|-8|-10|0.1|1.1|||||Grup_Uji
"""
EKSTRA_UJI = {"UJI_GORENG": (0, 0, 0, 80, 3), "UJI_GADAI": (0, 45, 0, 40, 0), "UJI_INSIDER": (4, 0, 1, 35, 0)}

# ------------------------------------------------------------------ HEURISTIK PAKAR v2
HEUR_V2 = [
 ("H16_RegimeAware", "Sinyal yang sama bermakna berbeda per regime", "Saat krisis likuiditas, teknikal & sentimen menyesatkan (semua saham di bawah MA200); bobot dipindah ke neraca, valuasi, dan jejak smart money (R-REG, R-ADP)."),
 ("H17_PricedIn", "Berita buruk, harga tidak turun", "Bila berita negatif tidak lagi menekan harga dan bandar akumulasi, berita sudah priced-in (R-REF-01)."),
 ("H18_SellTheNews", "Berita bagus, harga tidak naik", "Berita positif + kalah dari pasar + distribusi = sell the news (R-REF-02)."),
 ("H19_Kapitulasi", "Kapitulasi & akumulasi bertahap", "Hari crash ≥10% + drawdown ≥40% + breadth washout = zona akumulasi generasional; beli 3 tranche, bukan sekaligus (R-PAS, R-KAP)."),
 ("H20_RevisiLaba", "Ikuti arah revisi, bukan level", "Pasar membayar perubahan ekspektasi; revisi naik + harga tertinggal = celah ekspektasi (R-REV)."),
 ("H21_ReactionFunction", "Antisipasi reaksi otoritas", "Rupiah lemah + inflasi naik → BI naik pre-emptif; Brent >100 → risiko penyesuaian BBM; drawdown dalam → stabilisasi pasar (R-ANT)."),
 ("H22_ERP", "Bandingkan dengan obligasi", "Earnings yield − yield SBN: ERP tinggi berarti saham murah relatif aset bebas risiko domestik (R-ERP)."),
 ("H23_Robustness", "Pilih posisi yang tahan banyak skenario", "Utamakan sektor robust lintas skenario; ambil taruhan asimetris bila upside ≥ 1,5× downside (R-ROB)."),
 ("H24_Konfluensi", "Keyakinan dari konfluensi, kehati-hatian dari konflik", "≥5 pilar searah = keyakinan; fundamental vs bandar bertentangan = tunggu konfirmasi (R-KON)."),
 ("H25_Sizing", "Ukuran posisi dari risiko, bukan keyakinan", "Ukuran = risiko per transaksi / jarak stop (2×ATR); risiko dipangkas di regime krisis (R-POS)."),
 ("H26_KillSwitch", "Setiap tesis punya kriteria gugur", "Tetapkan indikator kunci & ambang invalidasi sebelum masuk; buffer < 10% = tesis rapuh (R-TES)."),
 ("H27_KatalisBiner", "Jangan full position sebelum katalis biner", "FOMC, review MSCI, pemilu: masuk bertahap dan sisakan kas (R-KAT)."),
 ("H28_Governance", "Diskon tata kelola", "Free float < 15%, gadai saham pengendali, ARA beruntun dengan broker terkonsentrasi = risiko yang tak terlihat di rasio (R-GOV)."),
 ("H29_Intermarket", "Pasar obligasi & CDS mendahului saham", "Dasar IHSG lebih kredibel bila CDS & rupiah sudah membaik lebih dulu (R-PAS-06/07)."),
 ("H30_DataKualitas", "Tahu batas data sendiri", "Rekomendasi yang bertumpu pada data indikatif/kedaluwarsa wajib diverifikasi (R-DAT)."),
 ("H31_ForcedSelling", "Penjualan paksa tidak sensitif harga", "Outflow pasif (reklasifikasi indeks) menjual tanpa melihat valuasi; setelah tanggal efektif tekanan mekanis berakhir — pakar membeli setelah, bukan sebelum, eksekusi."),
]
