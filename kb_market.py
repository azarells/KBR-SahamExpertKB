# -*- coding: utf-8 -*-
"""
ABox pasar: sektor, indeks, penyedia indeks, broker, institusi, komoditas, indikator makro, emiten.
CATATAN DATA: angka emiten (harga, rasio, teknikal, bandar) = SNAPSHOT INDIKATIF untuk demonstrasi
penalaran (disusun dari kisaran historis 2024-2025 yang disesuaikan dengan kondisi pasar Okt 2026).
WAJIB diperbarui dari laporan keuangan & data pasar terbaru (IDX, RTI, Stockbit) sebelum dipakai.
Indikator makro & peristiwa diambil dari berita Okt 2026 (lihat sumberReferensi).
"""

# Urutan faktor makro (dipakai sensitivitas sektor & arah skenario)
FAKTOR = ["Energi", "USD", "SukuBunga", "Inflasi", "Emas", "LogamChina",
          "RiskOff", "BelanjaPemerintah", "DayaBeli", "Tarif", "CPO", "Digital"]

FAKTOR_DESC = {
 "Energi": "Harga minyak/gas/batu bara (+ = naik)",
 "USD": "Dolar AS menguat / rupiah melemah (+)",
 "SukuBunga": "Suku bunga Fed & BI (+ = naik)",
 "Inflasi": "Inflasi domestik (+ = naik)",
 "Emas": "Harga emas (+ = naik)",
 "LogamChina": "Harga logam industri & permintaan China (+ = naik)",
 "RiskOff": "Risk-off global / outflow dana asing EM (+ = makin risk-off)",
 "BelanjaPemerintah": "Belanja & program pemerintah (+ = ekspansif)",
 "DayaBeli": "Daya beli konsumen (+ = menguat)",
 "Tarif": "Eskalasi perang dagang/tarif (+ = memburuk)",
 "CPO": "Harga CPO (+ = naik)",
 "Digital": "Adopsi digital/AI/data center (+ = akseleratif)",
}

# kode, label, indeks BEI, PER, PER 5th, aliran asing 3 bln (Rp T), skorTema, fase(E,M,L,R), sensitivitas[12]
SEKTOR = [
 ("Sektor_Energi", "Energi", "IDXENERGY", 4.5, 7.5, -1.5, 0, (-1, 1, 2, -1), [2, 2, 0, 0, 0, 1, -1, 0, 0, -1, 0, 0]),
 ("Sektor_BarangBaku", "Barang Baku", "IDXBASIC", 12.0, 17.0, 0.5, 3, (0, 2, 2, -1), [-1, 1, -1, 0, 2, 2, -1, 1, 0, -1, 0, 0]),
 ("Sektor_Perindustrian", "Perindustrian", "IDXINDUST", 5.5, 9.0, -1.0, 1, (1, 2, 0, -1), [1, 0, -1, 0, 1, 1, -1, 1, 1, -1, 1, 0]),
 ("Sektor_KonsumenPrimer", "Barang Konsumen Primer", "IDXNONCYC", 10.0, 15.0, -0.8, 2, (0, 0, 1, 2), [-1, -1, -1, -1, 0, 0, 1, 2, 1, 0, 1, 0]),
 ("Sektor_KonsumenNonPrimer", "Barang Konsumen Non-Primer", "IDXCYCLIC", 8.0, 14.0, -0.5, 0, (2, 1, -1, -1), [-1, -1, -1, -2, 0, 0, -1, 0, 2, -1, 0, 1]),
 ("Sektor_Kesehatan", "Kesehatan", "IDXHEALTH", 18.0, 26.0, -0.3, 2, (0, 0, 1, 2), [0, -1, 0, -1, 0, 0, 2, 1, 1, 0, 0, 1]),
 ("Sektor_Keuangan", "Keuangan", "IDXFINANCE", 8.0, 15.0, -25.0, 2, (2, 1, 0, -1), [0, -1, -1, -1, 0, 0, -2, 1, 2, 0, 0, 1]),
 ("Sektor_PropertiRealEstat", "Properti & Real Estat", "IDXPROPERT", 6.0, 11.0, -0.6, 1, (2, 0, -1, -1), [0, -1, -2, -1, 0, 0, -1, 1, 1, 0, 0, 0]),
 ("Sektor_Teknologi", "Teknologi", "IDXTECHNO", 40.0, 38.0, -1.2, 1, (2, 1, -1, -1), [0, -1, -2, 0, 0, 0, -2, 0, 1, -1, 0, 2]),
 ("Sektor_Infrastruktur", "Infrastruktur", "IDXINFRA", 10.0, 17.0, -4.0, 2, (1, 1, 0, 1), [0, -1, -1, 0, 0, 0, -1, 2, 1, 0, 0, 2]),
 ("Sektor_TransportasiLogistik", "Transportasi & Logistik", "IDXTRANS", 7.0, 9.0, -0.2, 0, (1, 1, -1, -1), [-2, -1, -1, -1, 0, 1, -1, 1, 1, 1, 0, 0]),
]

SEKTOR_TEMA = {
 "Sektor_Energi": ["Tema_KetahananEnergi", "Tema_TransisiEnergi"],
 "Sektor_BarangBaku": ["Tema_HilirisasiMineral", "Tema_EmasSafeHaven"],
 "Sektor_Perindustrian": ["Tema_HilirisasiMineral"],
 "Sektor_KonsumenPrimer": ["Tema_MakanBergiziGratis", "Tema_Biodiesel"],
 "Sektor_KonsumenNonPrimer": ["Tema_DigitalisasiKonsumen"],
 "Sektor_Kesehatan": ["Tema_PopulasiKesehatan"],
 "Sektor_Keuangan": ["Tema_InklusiKeuangan", "Tema_ReformasiPasarModal", "Tema_Danantara"],
 "Sektor_PropertiRealEstat": ["Tema_TigaJutaRumah"],
 "Sektor_Teknologi": ["Tema_DigitalisasiKonsumen", "Tema_DataCenterAI"],
 "Sektor_Infrastruktur": ["Tema_DataCenterAI", "Tema_KonsolidasiTelko"],
 "Sektor_TransportasiLogistik": [],
}

SUBSEKTOR = [
 ("Sub_BatuBara", "Batu Bara", "Sektor_Energi"), ("Sub_MinyakGas", "Minyak & Gas", "Sektor_Energi"),
 ("Sub_DistribusiEnergi", "Distribusi & Jasa Energi", "Sektor_Energi"),
 ("Sub_LogamMineral", "Logam & Mineral", "Sektor_BarangBaku"), ("Sub_Emas", "Pertambangan Emas", "Sektor_BarangBaku"),
 ("Sub_Nikel", "Nikel", "Sektor_BarangBaku"), ("Sub_KertasPulp", "Kertas & Pulp", "Sektor_BarangBaku"),
 ("Sub_Semen", "Semen & Bahan Konstruksi", "Sektor_BarangBaku"), ("Sub_AlatBerat", "Alat Berat & Konglomerasi Industri", "Sektor_Perindustrian"),
 ("Sub_BahanBangunan", "Bahan Bangunan & Industri", "Sektor_Perindustrian"),
 ("Sub_MakananOlahan", "Makanan & Minuman Olahan", "Sektor_KonsumenPrimer"), ("Sub_Unggas", "Peternakan Unggas & Pakan", "Sektor_KonsumenPrimer"),
 ("Sub_Perkebunan", "Perkebunan Sawit", "Sektor_KonsumenPrimer"), ("Sub_RitelPrimer", "Ritel Kebutuhan Pokok", "Sektor_KonsumenPrimer"),
 ("Sub_ProdukRumahTangga", "Produk Rumah Tangga", "Sektor_KonsumenPrimer"),
 ("Sub_RitelGayaHidup", "Ritel Gaya Hidup", "Sektor_KonsumenNonPrimer"), ("Sub_Otomotif", "Komponen Otomotif", "Sektor_KonsumenNonPrimer"),
 ("Sub_Farmasi", "Farmasi & Jamu", "Sektor_Kesehatan"), ("Sub_RumahSakit", "Rumah Sakit", "Sektor_Kesehatan"),
 ("Sub_Bank", "Perbankan", "Sektor_Keuangan"), ("Sub_BankSyariah", "Bank Syariah", "Sektor_Keuangan"),
 ("Sub_Properti", "Pengembang Properti", "Sektor_PropertiRealEstat"), ("Sub_KawasanIndustri", "Kawasan Industri & Data Center Land", "Sektor_PropertiRealEstat"),
 ("Sub_Internet", "Platform Internet", "Sektor_Teknologi"), ("Sub_DataCenter", "Data Center", "Sektor_Teknologi"),
 ("Sub_DistribusiTI", "Solusi & Distribusi TI", "Sektor_Teknologi"),
 ("Sub_Telekomunikasi", "Telekomunikasi", "Sektor_Infrastruktur"), ("Sub_Menara", "Menara Telekomunikasi", "Sektor_Infrastruktur"),
 ("Sub_JalanTol", "Jalan Tol", "Sektor_Infrastruktur"),
 ("Sub_Transportasi", "Transportasi Darat", "Sektor_TransportasiLogistik"), ("Sub_Pelayaran", "Pelayaran & Logistik Laut", "Sektor_TransportasiLogistik"),
]

PENYEDIA = [
 ("Penyedia_BEI", "Bursa Efek Indonesia"), ("Penyedia_MSCI", "MSCI Inc."), ("Penyedia_FTSERussell", "FTSE Russell (LSEG)"),
 ("Penyedia_SPDJI", "S&P Dow Jones Indices"), ("Penyedia_NasdaqInc", "Nasdaq Inc."), ("Penyedia_Nikkei", "Nikkei Inc."),
 ("Penyedia_HSIL", "Hang Seng Indexes Co."), ("Penyedia_SSE", "Shanghai Stock Exchange / CSI"), ("Penyedia_SGX", "SGX / SPH (STI)"),
 ("Penyedia_KRX", "Korea Exchange"), ("Penyedia_Deutsche", "Deutsche Börse (STOXX)"), ("Penyedia_Euronext", "Euronext"),
 ("Penyedia_BSE_NSE", "BSE / NSE India"), ("Penyedia_ICE", "ICE (DXY)"), ("Penyedia_CBOE", "Cboe Global Markets"),
 ("Penyedia_Kompas", "BEI - Harian Kompas"), ("Penyedia_KEHATI", "Yayasan KEHATI - BEI"), ("Penyedia_ASX", "S&P/ASX"),
 ("Penyedia_Bursa_Malaysia", "Bursa Malaysia / FTSE"), ("Penyedia_SET", "Stock Exchange of Thailand"), ("Penyedia_PSE", "Philippine Stock Exchange"),
]

# nama, kelas, label, penyedia, negara, jumlahKonstituen (0=tidak dicatat), keterangan
INDEKS = [
 ("IHSG", "IndeksKomposit", "Indeks Harga Saham Gabungan (IHSG/JCI)", "Penyedia_BEI", "Indonesia", 0, "Seluruh saham tercatat. 19 Okt 2026 ditutup 4.996,61 (terendah sejak Okt 2020; -42,22% YTD)."),
 ("LQ45", "IndeksLikuiditas", "LQ45", "Penyedia_BEI", "Indonesia", 45, "45 saham paling likuid & berkapitalisasi besar; evaluasi berkala (Feb & Agu) dengan review triwulanan."),
 ("IDX30", "IndeksLikuiditas", "IDX30", "Penyedia_BEI", "Indonesia", 30, "30 saham dari LQ45 dengan likuiditas & kapitalisasi tertinggi."),
 ("IDX80", "IndeksLikuiditas", "IDX80", "Penyedia_BEI", "Indonesia", 80, "80 saham likuid berkapitalisasi besar."),
 ("Kompas100", "IndeksLikuiditas", "Kompas100", "Penyedia_Kompas", "Indonesia", 100, "Kerja sama BEI-Kompas."),
 ("IDXHIDIV20", "IndeksTematik", "IDX High Dividend 20", "Penyedia_BEI", "Indonesia", 20, "20 saham dividen tinggi & konsisten."),
 ("IDXBUMN20", "IndeksTematik", "IDX BUMN20", "Penyedia_BEI", "Indonesia", 20, "20 saham BUMN, anak usaha, dan afiliasi."),
 ("IDXV30", "IndeksTematik", "IDX Value30", "Penyedia_BEI", "Indonesia", 30, "Faktor value (PER & PBV rendah)."),
 ("IDXG30", "IndeksTematik", "IDX Growth30", "Penyedia_BEI", "Indonesia", 30, "Faktor pertumbuhan laba & pendapatan."),
 ("IDXQ30", "IndeksTematik", "IDX Quality30", "Penyedia_BEI", "Indonesia", 30, "Faktor kualitas (ROE, leverage, stabilitas laba)."),
 ("IDXLQ45LCL", "IndeksTematik", "IDX LQ45 Low Carbon Leaders", "Penyedia_BEI", "Indonesia", 0, "Konstituen LQ45 dengan emisi karbon rendah."),
 ("JII", "IndeksSyariah", "Jakarta Islamic Index (JII)", "Penyedia_BEI", "Indonesia", 30, "30 saham syariah paling likuid."),
 ("JII70", "IndeksSyariah", "JII70", "Penyedia_BEI", "Indonesia", 70, "70 saham syariah paling likuid."),
 ("ISSI", "IndeksSyariah", "Indeks Saham Syariah Indonesia (ISSI)", "Penyedia_BEI", "Indonesia", 0, "Seluruh saham dalam Daftar Efek Syariah."),
 ("SRIKEHATI", "IndeksESG", "SRI-KEHATI", "Penyedia_KEHATI", "Indonesia", 25, "Emiten dengan kinerja keberlanjutan baik."),
 ("IDXESGL", "IndeksESG", "IDX ESG Leaders", "Penyedia_BEI", "Indonesia", 30, "Skor ESG terbaik (Sustainalytics)."),
 ("IDXENERGY", "IndeksSektoralBEI", "IDX Sector Energy", "Penyedia_BEI", "Indonesia", 0, "H1 2026 turun > 40%."),
 ("IDXBASIC", "IndeksSektoralBEI", "IDX Sector Basic Materials", "Penyedia_BEI", "Indonesia", 0, ""),
 ("IDXINDUST", "IndeksSektoralBEI", "IDX Sector Industrials", "Penyedia_BEI", "Indonesia", 0, ""),
 ("IDXNONCYC", "IndeksSektoralBEI", "IDX Sector Consumer Non-Cyclicals", "Penyedia_BEI", "Indonesia", 0, ""),
 ("IDXCYCLIC", "IndeksSektoralBEI", "IDX Sector Consumer Cyclicals", "Penyedia_BEI", "Indonesia", 0, ""),
 ("IDXHEALTH", "IndeksSektoralBEI", "IDX Sector Healthcare", "Penyedia_BEI", "Indonesia", 0, ""),
 ("IDXFINANCE", "IndeksSektoralBEI", "IDX Sector Financials", "Penyedia_BEI", "Indonesia", 0, ""),
 ("IDXPROPERT", "IndeksSektoralBEI", "IDX Sector Properties & Real Estate", "Penyedia_BEI", "Indonesia", 0, "H1 2026 turun > 38%."),
 ("IDXTECHNO", "IndeksSektoralBEI", "IDX Sector Technology", "Penyedia_BEI", "Indonesia", 0, ""),
 ("IDXINFRA", "IndeksSektoralBEI", "IDX Sector Infrastructures", "Penyedia_BEI", "Indonesia", 0, "H1 2026 turun > 35%."),
 ("IDXTRANS", "IndeksSektoralBEI", "IDX Sector Transportation & Logistic", "Penyedia_BEI", "Indonesia", 0, ""),
 # MSCI
 ("MSCI_Indonesia", "IndeksMSCI", "MSCI Indonesia Index", "Penyedia_MSCI", "Indonesia", 0, "Konstituen big caps; acuan ETF EIDO. 2026: FIF dibekukan (freeze) pada review Feb-Mei-Agu; dipertahankan hingga review Nov 2026."),
 ("MSCI_Indonesia_SmallCap", "IndeksMSCI", "MSCI Indonesia Small Cap", "Penyedia_MSCI", "Indonesia", 0, "Konstituen kapitalisasi kecil."),
 ("MSCI_Indonesia_IMI", "IndeksMSCI", "MSCI Indonesia IMI", "Penyedia_MSCI", "Indonesia", 0, "Large + mid + small cap."),
 ("MSCI_EmergingMarkets", "IndeksMSCI", "MSCI Emerging Markets", "Penyedia_MSCI", "Global", 0, "Acuan triliunan USD dana EM; bobot Indonesia tertekan oleh freeze."),
 ("MSCI_EM_Asia", "IndeksMSCI", "MSCI EM Asia", "Penyedia_MSCI", "Asia", 0, ""),
 ("MSCI_AC_AsiaExJapan", "IndeksMSCI", "MSCI AC Asia ex Japan", "Penyedia_MSCI", "Asia", 0, ""),
 ("MSCI_ACWI", "IndeksMSCI", "MSCI All Country World Index", "Penyedia_MSCI", "Global", 0, ""),
 ("MSCI_World", "IndeksMSCI", "MSCI World", "Penyedia_MSCI", "Global (DM)", 0, "Pasar maju."),
 ("MSCI_FrontierMarkets", "IndeksMSCI", "MSCI Frontier Markets", "Penyedia_MSCI", "Global", 0, "Risiko reklasifikasi Indonesia ke frontier/standalone jika reformasi gagal."),
 ("MSCI_ASEAN", "IndeksMSCI", "MSCI AC ASEAN", "Penyedia_MSCI", "ASEAN", 0, ""),
 ("FTSE_Indonesia", "IndeksFTSERussell", "FTSE Indonesia", "Penyedia_FTSERussell", "Indonesia", 0, ""),
 ("FTSE_AllWorld", "IndeksFTSERussell", "FTSE All-World", "Penyedia_FTSERussell", "Global", 0, ""),
 ("FTSE_ASEAN40", "IndeksFTSERussell", "FTSE/ASEAN 40", "Penyedia_FTSERussell", "ASEAN", 40, ""),
 ("SP_Indonesia_BMI", "IndeksSPDowJones", "S&P Indonesia BMI", "Penyedia_SPDJI", "Indonesia", 0, "Juli 2026: S&P DJI menandai potensi penurunan klasifikasi ke frontier."),
 # Amerika
 ("NASDAQ_Composite", "IndeksAmerika", "NASDAQ Composite", "Penyedia_NasdaqInc", "Amerika Serikat", 0, "Seluruh saham Nasdaq; proksi sentimen teknologi global."),
 ("NASDAQ100", "IndeksAmerika", "NASDAQ-100", "Penyedia_NasdaqInc", "Amerika Serikat", 100, "100 non-finansial terbesar Nasdaq (big tech/AI)."),
 ("SP500", "IndeksAmerika", "S&P 500", "Penyedia_SPDJI", "Amerika Serikat", 500, ""),
 ("DowJones", "IndeksAmerika", "Dow Jones Industrial Average", "Penyedia_SPDJI", "Amerika Serikat", 30, ""),
 ("Russell2000", "IndeksAmerika", "Russell 2000", "Penyedia_FTSERussell", "Amerika Serikat", 2000, "Small caps AS; sensitif suku bunga."),
 ("PHLX_Semiconductor", "IndeksAmerika", "PHLX Semiconductor (SOX)", "Penyedia_NasdaqInc", "Amerika Serikat", 30, "Proksi siklus AI/semikonduktor."),
 # Eropa
 ("FTSE100", "IndeksEropa", "FTSE 100", "Penyedia_FTSERussell", "Inggris", 100, ""),
 ("DAX40", "IndeksEropa", "DAX 40", "Penyedia_Deutsche", "Jerman", 40, ""),
 ("CAC40", "IndeksEropa", "CAC 40", "Penyedia_Euronext", "Prancis", 40, ""),
 ("EuroStoxx50", "IndeksEropa", "Euro Stoxx 50", "Penyedia_Deutsche", "Zona Euro", 50, ""),
 # Asia Pasifik
 ("Nikkei225", "IndeksAsiaPasifik", "Nikkei 225", "Penyedia_Nikkei", "Jepang", 225, "Turun > 7% saat perang Iran Mar 2026."),
 ("TOPIX", "IndeksAsiaPasifik", "TOPIX", "Penyedia_Nikkei", "Jepang", 0, ""),
 ("HangSeng", "IndeksAsiaPasifik", "Hang Seng Index", "Penyedia_HSIL", "Hong Kong", 0, "Proksi sentimen China."),
 ("ShanghaiComposite", "IndeksAsiaPasifik", "Shanghai Composite", "Penyedia_SSE", "China", 0, "Proksi permintaan komoditas China."),
 ("CSI300", "IndeksAsiaPasifik", "CSI 300", "Penyedia_SSE", "China", 300, ""),
 ("KOSPI", "IndeksAsiaPasifik", "KOSPI", "Penyedia_KRX", "Korea Selatan", 0, "Turun > 8% & trading halt saat perang Iran Mar 2026."),
 ("STI", "IndeksAsiaPasifik", "Straits Times Index", "Penyedia_SGX", "Singapura", 30, ""),
 ("FBMKLCI", "IndeksAsiaPasifik", "FTSE Bursa Malaysia KLCI", "Penyedia_Bursa_Malaysia", "Malaysia", 30, ""),
 ("SET", "IndeksAsiaPasifik", "SET Index", "Penyedia_SET", "Thailand", 0, ""),
 ("PSEi", "IndeksAsiaPasifik", "PSEi", "Penyedia_PSE", "Filipina", 30, ""),
 ("ASX200", "IndeksAsiaPasifik", "S&P/ASX 200", "Penyedia_ASX", "Australia", 200, "Proksi komoditas tambang."),
 ("Sensex", "IndeksAsiaPasifik", "BSE Sensex", "Penyedia_BSE_NSE", "India", 30, ""),
 ("Nifty50", "IndeksAsiaPasifik", "Nifty 50", "Penyedia_BSE_NSE", "India", 50, "Pesaing utama alokasi dana EM."),
 # Risiko
 ("VIX", "IndikatorRisikoGlobal", "CBOE Volatility Index (VIX)", "Penyedia_CBOE", "Amerika Serikat", 0, "'Indeks ketakutan'; > 30 = risk-off tajam."),
 ("DXY", "IndikatorRisikoGlobal", "US Dollar Index (DXY)", "Penyedia_ICE", "Amerika Serikat", 0, "Dolar vs 6 mata uang utama; DXY naik → tekanan EM."),
]

# (indeks pemengaruh, indeks/ sektor terpengaruh, keterangan)  -> properti memengaruhi
PENGARUH_INDEKS = [
 ("NASDAQ100", "IDXTECHNO"), ("NASDAQ_Composite", "IDXTECHNO"), ("PHLX_Semiconductor", "IDXTECHNO"),
 ("SP500", "IHSG"), ("DowJones", "IHSG"), ("DXY", "IHSG"), ("VIX", "IHSG"), ("MSCI_EmergingMarkets", "IHSG"),
 ("ShanghaiComposite", "IDXBASIC"), ("HangSeng", "IDXBASIC"), ("ShanghaiComposite", "IDXENERGY"),
 ("ASX200", "IDXBASIC"), ("Nikkei225", "IHSG"), ("STI", "IHSG"), ("MSCI_Indonesia", "LQ45"),
 ("MSCI_Indonesia", "IDXFINANCE"), ("Nifty50", "MSCI_EmergingMarkets"), ("LQ45", "IHSG"), ("IDX30", "LQ45"),
]

BROKER = [
 # kode, nama, kelas
 ("YP", "Mirae Asset Sekuritas Indonesia", "BrokerRitel"),
 ("PD", "Indo Premier Sekuritas", "BrokerRitel"),
 ("XL", "Stockbit Sekuritas Digital", "BrokerRitel"),
 ("XC", "Ajaib Sekuritas Asia", "BrokerRitel"),
 ("CC", "Mandiri Sekuritas", "BrokerInstitusiLokal"),
 ("NI", "BNI Sekuritas", "BrokerInstitusiLokal"),
 ("DX", "Bahana Sekuritas", "BrokerInstitusiLokal"),
 ("LG", "Trimegah Sekuritas Indonesia", "BrokerInstitusiLokal"),
 ("AZ", "Sucor Sekuritas", "BrokerInstitusiLokal"),
 ("KZ", "CLSA Sekuritas Indonesia", "BrokerAsing"),
 ("AK", "UBS Sekuritas Indonesia", "BrokerAsing"),
 ("BK", "J.P. Morgan Sekuritas Indonesia", "BrokerAsing"),
 ("ZP", "Maybank Sekuritas Indonesia", "BrokerAsing"),
 ("RX", "Macquarie Sekuritas Indonesia", "BrokerAsing"),
 ("YU", "CGS International Sekuritas Indonesia", "BrokerAsing"),
 ("KK", "Phillip Sekuritas Indonesia", "BrokerAsing"),
]

INSTITUSI = [
 ("OJK", "Regulator", "Otoritas Jasa Keuangan", "Pengatur & pengawas sektor jasa keuangan; 2026 menggulirkan reformasi free float & transparansi."),
 ("BEI_Bursa", "SelfRegulatoryOrganization", "Bursa Efek Indonesia", "Penyelenggara bursa; penerbit IHSG, LQ45, IDX30, dll."),
 ("KSEI", "SelfRegulatoryOrganization", "Kustodian Sentral Efek Indonesia", "Kustodian & penerbit SID."),
 ("KPEI", "SelfRegulatoryOrganization", "Kliring Penjaminan Efek Indonesia", "Kliring & penjaminan penyelesaian T+2."),
 ("BankIndonesia", "BankSentral", "Bank Indonesia", "Otoritas moneter; RDG Okt 2026 menahan BI Rate 5,75%, menaikkan Deposit Facility ke 5%, rencana turunkan GWM."),
 ("TheFed", "BankSentral", "The Federal Reserve (FOMC)", "Bank sentral AS; FOMC 28 Okt & 9 Des 2026; mayoritas pejabat melihat ruang kenaikan."),
 ("ECB", "BankSentral", "European Central Bank", "Bank sentral zona euro."),
 ("BankOfJapan", "BankSentral", "Bank of Japan", "Normalisasi bunga Jepang memengaruhi yen carry trade."),
 ("PBoC", "BankSentral", "People's Bank of China", "Stimulus China memengaruhi permintaan komoditas."),
 ("BPS", "Institusi", "Badan Pusat Statistik", "Rilis inflasi, PDB, neraca dagang."),
 ("Kemenkeu", "Institusi", "Kementerian Keuangan", "Kebijakan fiskal & APBN."),
 ("Kemendag", "Institusi", "Kementerian Perdagangan", "Penetapan harga referensi CPO & bea keluar."),
 ("Danantara", "Institusi", "BPI Danantara", "Superholding/sovereign fund pengelola BUMN (berdiri 2025)."),
 ("OPEC_Plus", "OrganisasiInternasional", "OPEC+", "Kartel produsen minyak + sekutu (Rusia dll)."),
 ("IMF", "OrganisasiInternasional", "International Monetary Fund", "Proyeksi pertumbuhan global."),
 ("SnP_Ratings", "LembagaPemeringkat", "S&P Global Ratings", "Mempertahankan Indonesia BBB/A-2 outlook stabil (2026)."),
 ("Moodys", "LembagaPemeringkat", "Moody's", "Lembaga pemeringkat."),
 ("FitchRatings", "LembagaPemeringkat", "Fitch Ratings", "Lembaga pemeringkat."),
 ("EIA", "OrganisasiInternasional", "U.S. Energy Information Administration", "Proyeksi Brent Q4 2026 ~US$105 (laporan 6 Okt 2026)."),
]

KOMODITAS = [
 ("Kom_MinyakBrent", "KomoditasEnergi", "Minyak Brent", "US$/barel"), ("Kom_MinyakWTI", "KomoditasEnergi", "Minyak WTI", "US$/barel"),
 ("Kom_GasLNG", "KomoditasEnergi", "Gas Alam / LNG", "US$/MMBtu"), ("Kom_BatuBara", "KomoditasEnergi", "Batu Bara Newcastle", "US$/ton"),
 ("Kom_Emas", "LogamMulia", "Emas", "US$/troy ons"), ("Kom_Perak", "LogamMulia", "Perak", "US$/troy ons"),
 ("Kom_Nikel", "KomoditasLogam", "Nikel LME", "US$/ton"), ("Kom_Timah", "KomoditasLogam", "Timah LME", "US$/ton"),
 ("Kom_Tembaga", "KomoditasLogam", "Tembaga LME", "US$/ton"), ("Kom_Bauksit", "KomoditasLogam", "Bauksit/Alumina", "US$/ton"),
 ("Kom_CPO", "KomoditasAgrikultur", "Crude Palm Oil", "US$/MT"), ("Kom_Gandum", "KomoditasAgrikultur", "Gandum", "US$/bushel"),
 ("Kom_JagungKedelai", "KomoditasAgrikultur", "Jagung & Bungkil Kedelai (Pakan)", "US$/ton"), ("Kom_Kakao", "KomoditasAgrikultur", "Kakao", "US$/ton"),
 ("Kom_Karet", "KomoditasAgrikultur", "Karet", "US$/kg"), ("Kom_Pulp", "KomoditasAgrikultur", "Pulp", "US$/ton"),
]

# nama, kelas, label, nilai, satuan, tanggal, sumber url, keterangan
MAKRO = [
 ("Makro_FedFundsRate", "IndikatorMoneter", "Fed Funds Rate (batas atas)", 4.00, "%", "2026-09-16", "https://investortrust.id/market/116614/the-fed-naikkan-suku-bunga-ke-3-754-00-ini-implikasinya-bagi-pasar-obligasi-indonesia", "FOMC 16 Sep 2026 menaikkan 25 bps ke 3,75-4,00% (kenaikan pertama sejak 2023); median dot akhir 2026 4,1%; proyeksi PCE 2026 3,7%."),
 ("Makro_CorePCE_US", "IndikatorEkonomiRiil", "Core PCE AS (yoy)", 3.0, "%", "2026-08", "https://market.bisnis.com/read/20261008/7/2010804/fomc-minutes-buka-peluang-kenaikan-bunga-ihsg-dibayangi-tekanan", "Headline PCE 3,4%; 16 dari 18 pejabat proyeksikan ≥1 kenaikan lagi."),
 ("Makro_BIRate", "IndikatorMoneter", "BI Rate", 5.75, "%", "2026-10-21", "https://finansial.bisnis.com/read/20261021/11/2014413/breaking-bank-indonesia-tahan-bi-rate-575-pada-rdg-oktober-2026", "Ditahan; mayoritas ekonom proyeksikan naik ke 6%."),
 ("Makro_DepositFacility", "IndikatorMoneter", "BI Deposit Facility", 5.0, "%", "2026-10-21", "https://www.idnfinancials.com/news/70614/bank-indonesia-holds-rate-at-5-75-raises-deposit-facility-rate-to-5", "Dinaikkan untuk stabilisasi rupiah."),
 ("Makro_InflasiID", "IndikatorEkonomiRiil", "Inflasi Indonesia (yoy)", 3.28, "%", "2026-09", "https://investortrust.id/macro/118018/bps-inflasi-september-2026-tembus-0-30-tahunan-3-28", "Didorong harga pangan & emas; mtm 0,30%."),
 ("Makro_USDIDR", "IndikatorNilaiTukar", "Kurs USD/IDR", 17938.0, "Rp", "2026-10", "https://market.bisnis.com/read/20261008/7/2010804/fomc-minutes-buka-peluang-kenaikan-bunga-ihsg-dibayangi-tekanan", "Rupiah di bawah tekanan; BI intervensi."),
 ("Makro_IHSG", "IndikatorAliranDana", "Level IHSG", 4996.61, "poin", "2026-10-19", "https://insight.kontan.co.id/news/ihsg-terendah-6-tahun-waspadai-tekanan-jual-saham-big-caps-hari-ini-2010", "Terendah sejak 6 Okt 2020; -15,83% sepekan; -42,22% YTD."),
 ("Makro_IHSG_Akhir2025", "IndikatorAliranDana", "IHSG Akhir 2025", 8646.0, "poin", "2025-12-31", "https://investortrust.id/market/108011/semester-i-kelam-ihsg-ambles-34-73-disertai-kejatuhaan-saham-big-caps-dan-net-sell-asing", ""),
 ("Makro_NetSellAsingH1", "IndikatorAliranDana", "Net Sell Asing H1 2026", -73.6, "Rp triliun", "2026-06-30", "https://investortrust.id/market/108011/semester-i-kelam-ihsg-ambles-34-73-disertai-kejatuhaan-saham-big-caps-dan-net-sell-asing", "Terkonsentrasi di big caps (BBCA, BBRI, BMRI, TLKM, AMMN, dll)."),
 ("Makro_Brent", "IndikatorHargaKomoditas", "Harga Brent", 106.65, "US$/barel", "2026-10-12", "https://www.kabarbursa.com/market-hari-ini/houthi-gempur-arab-saudi-harga-minyak-brent-naik-ke-level-usd106-per-barel", "Tertinggi sejak 15 Sep 2026 setelah serangan Houthi ke Riyadh."),
 ("Makro_WTI", "IndikatorHargaKomoditas", "Harga WTI", 93.74, "US$/barel", "2026-10-12", "https://www.kabarbursa.com/market-hari-ini/houthi-gempur-arab-saudi-harga-minyak-brent-naik-ke-level-usd106-per-barel", "Goldman: WTI rata-rata US$73 pada 2027 (normalisasi)."),
 ("Makro_ProyeksiBrentEIA", "IndikatorHargaKomoditas", "Proyeksi Brent EIA Q4-2026", 105.0, "US$/barel", "2026-10-06", "https://www.kabarbursa.com/market-hari-ini/houthi-gempur-arab-saudi-harga-minyak-brent-naik-ke-level-usd106-per-barel", "Rata-rata 2026 ~US$98."),
 ("Makro_ProyeksiBrentGS", "IndikatorHargaKomoditas", "Proyeksi Brent Goldman Des-2026", 90.0, "US$/barel", "2026-10", "https://www.kabarbursa.com/market-hari-ini/houthi-gempur-arab-saudi-harga-minyak-brent-naik-ke-level-usd106-per-barel", "Premi risiko > US$20."),
 ("Makro_Emas", "IndikatorHargaKomoditas", "Harga Emas Spot", 4390.11, "US$/troy ons", "2026-09-18", "https://www.kabarbursa.com/makro/emas-spot-sentuh-usd439011-antam-diprediksi-capai-rp32-juta-per-gram", "Turun dari puncak; kenaikan Fed menjadi headwind emas."),
 ("Makro_CDS5Y", "IndikatorMoneter", "CDS Indonesia 5Y", 99.73, "bps", "2026-10-21", "https://investasi.kontan.co.id/news/cds-indonesia-terus-menanjak-sentimen-msci-tekan-persepsi-risiko-investor", "Naik dari 92,40 bps (14 Okt) setelah konsultasi MSCI standalone."),
 ("Makro_YieldSBN10Y", "IndikatorMoneter", "Yield SBN 10Y", 7.14, "%", "2026-09-17", "https://investortrust.id/market/116614/the-fed-naikkan-suku-bunga-ke-3-754-00-ini-implikasinya-bagi-pasar-obligasi-indonesia", "Data per 17 Sep 2026 (perlu pembaruan)."),
 ("Makro_UST10Y", "IndikatorMoneter", "Yield UST 10Y", 4.98, "%", "2026-09-17", "https://investortrust.id/market/116614/the-fed-naikkan-suku-bunga-ke-3-754-00-ini-implikasinya-bagi-pasar-obligasi-indonesia", "Spread SBN-UST ~216 bps."),
 ("Makro_SpreadSBN_UST", "IndikatorMoneter", "Spread SBN-UST 10Y", 216.0, "bps", "2026-09-17", "https://investortrust.id/market/116614/the-fed-naikkan-suku-bunga-ke-3-754-00-ini-implikasinya-bagi-pasar-obligasi-indonesia", "Menyempit dari 231,8 bps awal Sep."),
 ("Makro_NetAsingYTD", "IndikatorAliranDana", "Net Sell Asing YTD 2026", -88.19, "Rp triliun", "2026-10-16", "https://www.kabarbursa.com/market-hari-ini/pelemahan-dinilai-mulai-terbatas-simak-arah-ihsg-hari-ini", "Net sell Rp3,34 T pada 16 Okt."),
 ("Makro_IHSG_16Okt", "IndikatorAliranDana", "IHSG 16 Okt 2026 (capitulation day)", 5185.11, "poin", "2026-10-16", "https://www.kabarbursa.com/market-hari-ini/pelemahan-dinilai-mulai-terbatas-simak-arah-ihsg-hari-ini", "Anjlok 11,57% dalam sehari setelah konsultasi MSCI standalone."),
 ("Makro_IHSG_30Sep", "IndikatorAliranDana", "IHSG 30 Sep 2026", 6095.86, "poin", "2026-09-30", "https://www.kabarbursa.com/market-hari-ini/hsbc-pasang-target-ihsg-6200-ruang-penguatan-tinggal-17-persen", "Turun 6,58% sepanjang September."),
 ("Makro_EstimasiOutflowPasif", "IndikatorAliranDana", "Estimasi outflow pasif jika standalone", 4.5, "US$ miliar (titik tengah 3-6)", "2026-10-20", "https://www.kabarbursa.com/market-hari-ini/pelemahan-dinilai-mulai-terbatas-simak-arah-ihsg-hari-ini", "Estimasi ekonom USD3-6 miliar; UBS: investor aktif ~USD15 miliar."),
 ("Makro_RatingSP", "IndikatorEkonomiRiil", "Rating S&P Indonesia", 0.0, "BBB/A-2 stabil", "2026-07", "https://investortrust.id/market/109557/target-ihsg-7200-ini-daftar-saham-pilihan-bri-danareksa-dan-target-harganya", "Investment grade dipertahankan."),
]

# ============================================================== EMITEN
# Kolom: kode|nama|sektor|subsektor|bank(1/0)|bumn|syariah|harga|mcapT|likuidM|freefloat|
#        per|per5y|pbv|roe|f2|f3|epsg|f5|dy|dpr|altman|beneish|
#        ma50|ma200|ma50v200|rsi|macd|volR|atrPct|acc|for20|ret20|chg20|vwap|bo|
#        indeks(;)|komoditasUntung(;)|komoditasBiaya(;)|pola(;)|grup
# Bank: f2=NPL, f3=NIM, f5=CAR. Non-bank: f2=DER, f3=NPM, f5=CFO/Laba bersih.
EMITEN_TABLE = r"""
AADI|Adaro Andalan Indonesia|Sektor_Energi|Sub_BatuBara|0|0|1|5400|42|180|35|4.0|5.5|0.9|24|0.2|24|-12|1.3|13|55|3.8|-2.6|6|2|-3|58|1|1.4|3.2|24|65|-40|-7.0|0.6|1.3|LQ45;IDX30;ISSI;IDXHIDIV20;MSCI_Indonesia|Kom_BatuBara||DoubleBottom;BullishEngulfing|Grup_Adaro
PTBA|Bukit Asam|Sektor_Energi|Sub_BatuBara|0|1|1|1900|22|90|34|5.0|6.5|1.0|17|0.5|12|-18|1.1|12|75|3.2|-2.7|4|-6|-8|52|1|1.1|3.0|12|20|-10|-9.0|0.3|1.1|LQ45;ISSI;JII;IDXBUMN20;IDXHIDIV20|Kom_BatuBara||RectangleRange|Grup_BUMN
ITMG|Indo Tambangraya Megah|Sektor_Energi|Sub_BatuBara|0|0|1|19000|21|60|34|4.6|5.0|0.8|15|0.1|12|-20|1.4|14|80|5.5|-2.8|3|-4|-6|55|1|1.2|2.8|15|30|-15|-10.0|0.2|1.2|LQ45;ISSI;IDXHIDIV20|Kom_BatuBara||Hammer|Grup_Banpu
MEDC|Medco Energi Internasional|Sektor_Energi|Sub_MinyakGas|0|0|1|1150|29|160|45|5.0|6.0|0.7|14|1.6|10|12|1.6|3|20|1.9|-2.5|9|12|4|64|1|1.8|3.8|28|85|-60|-1.0|0.8|1.6|LQ45;IDX30;ISSI;MSCI_Indonesia_SmallCap|Kom_MinyakBrent;Kom_GasLNG;Kom_Tembaga||BullFlag;BullishMarubozu|Grup_Medco
PGAS|Perusahaan Gas Negara|Sektor_Energi|Sub_MinyakGas|0|1|1|1250|30|110|43|5.8|9.0|0.7|11|0.6|9|3|1.5|9|55|2.6|-2.6|-2|-10|-7|46|-1|0.9|2.6|3|-15|5|-16.0|-0.2|0.9|LQ45;IDX30;ISSI;JII;IDXBUMN20|||SymmetricalTriangle|Grup_BUMN
AKRA|AKR Corporindo|Sektor_Energi|Sub_DistribusiEnergi|0|0|1|900|18|70|40|8.5|13.0|1.6|18|0.5|6|0|0.9|6|55|3.3|-2.4|-3|-15|-9|42|-1|0.8|3.0|-5|-20|15|-18.0|-0.4|0.8|LQ45;ISSI;JII||||Grup_AKR
ANTM|Aneka Tambang|Sektor_BarangBaku|Sub_Emas|0|1|1|2900|70|420|35|10.0|18.0|1.6|18|0.3|6|35|1.0|3|30|4.5|-2.5|7|18|9|63|1|1.6|3.5|32|120|-70|-3.0|0.7|1.5|LQ45;IDX30;ISSI;JII;IDXBUMN20;MSCI_Indonesia|Kom_Emas;Kom_Nikel||CupAndHandle;BullFlag|Grup_BUMN
MDKA|Merdeka Copper Gold|Sektor_BarangBaku|Sub_Emas|0|0|1|1900|46|350|45|80.0|70.0|2.2|2|1.2|1|50|2.0|0|0|1.5|-2.2|10|25|12|68|1|2.1|4.5|30|140|-90|2.0|1.1|1.7|LQ45;IDX30;ISSI;MSCI_Indonesia|Kom_Emas;Kom_Tembaga;Kom_Nikel||AscendingTriangle|Grup_Saratoga
INCO|Vale Indonesia|Sektor_BarangBaku|Sub_Nikel|0|0|1|3300|35|110|20|20.0|25.0|0.9|4|0.05|6|10|2.2|1|20|4.0|-2.6|2|-5|-8|49|-1|1.0|3.2|5|10|-5|-11.0|0.1|1.0|LQ45;ISSI;JII;MSCI_Indonesia_SmallCap|Kom_Nikel||FallingWedge|Grup_Vale
NCKL|Trimegah Bangun Persada|Sektor_BarangBaku|Sub_Nikel|0|0|1|780|49|95|14|6.5|10.0|1.4|22|0.6|25|15|1.1|4|30|3.0|-2.5|3|-2|-4|54|1|1.2|3.4|18|35|-20|-9.0|0.3|1.2|LQ45;ISSI;MSCI_Indonesia_SmallCap|Kom_Nikel||InverseHeadAndShoulders|Grup_Harita
AMMN|Amman Mineral Internasional|Sektor_BarangBaku|Sub_LogamMineral|0|0|1|4800|348|380|16|30.0|45.0|3.5|10|0.9|15|55|1.6|0|0|2.8|-2.3|-1|-22|-10|44|1|1.3|4.2|22|-80|40|-15.0|0.2|1.1|LQ45;IDX30;ISSI;MSCI_Indonesia|Kom_Tembaga;Kom_Emas||FallingWedge;MorningStar|Grup_Medco
BRMS|Bumi Resources Minerals|Sektor_BarangBaku|Sub_Emas|0|0|1|430|61|260|60|40.0|60.0|2.0|6|0.3|25|80|0.8|0|0|3.5|-2.0|12|30|15|72|1|2.6|5.2|15|60|20|4.0|1.4|1.8|LQ45;ISSI;MSCI_Indonesia_SmallCap|Kom_Emas||BullFlag;ThreeWhiteSoldiers|Grup_Bakrie_Salim
TINS|Timah|Sektor_BarangBaku|Sub_LogamMineral|0|1|1|1900|14|120|35|8.0|15.0|1.2|12|0.6|9|60|1.2|3|30|2.5|-2.4|5|8|3|61|1|1.5|4.0|20|25|-15|-5.0|0.5|1.4|LQ45;ISSI;IDXBUMN20|Kom_Timah||AscendingTriangle|Grup_BUMN
INKP|Indah Kiat Pulp & Paper|Sektor_BarangBaku|Sub_KertasPulp|0|0|1|5200|28|60|47|5.0|6.0|0.4|6|0.9|10|-10|1.0|1|10|2.2|-2.5|-2|-12|-8|45|-1|0.8|3.0|-6|-25|10|-16.0|-0.3|0.9|LQ45;ISSI|Kom_Pulp|Kom_BatuBara||Grup_Sinarmas
SMGR|Semen Indonesia|Sektor_BarangBaku|Sub_Semen|0|1|1|1900|13|60|49|25.0|20.0|0.4|2|0.5|2|-40|3.0|2|60|1.9|-2.6|-6|-30|-14|35|-1|0.9|3.1|-20|-30|20|-22.0|-0.6|0.7|LQ45;ISSI;JII;IDXBUMN20||Kom_BatuBara|HeadAndShoulders;BearishEngulfing|Grup_BUMN
ASII|Astra International|Sektor_Perindustrian|Sub_AlatBerat|0|0|1|3700|150|450|45|5.5|9.0|0.8|15|0.6|10|-5|1.2|10|55|2.9|-2.6|-1|-18|-9|43|-1|1.1|2.9|18|-120|70|-16.0|-0.1|1.0|LQ45;IDX30;ISSI;JII;MSCI_Indonesia;IDXHIDIV20|Kom_BatuBara;Kom_CPO;Kom_Emas||DoubleBottom|Grup_Astra
UNTR|United Tractors|Sektor_Perindustrian|Sub_AlatBerat|0|0|1|20000|75|180|40|4.5|6.5|0.9|18|0.3|15|-8|1.4|11|50|3.6|-2.6|2|-6|-6|51|1|1.2|2.7|22|45|-30|-10.0|0.3|1.2|LQ45;IDX30;ISSI;JII;MSCI_Indonesia;IDXHIDIV20|Kom_BatuBara;Kom_Emas;Kom_Nikel||InverseHeadAndShoulders|Grup_Astra
IMPC|Impack Pratama Industri|Sektor_Perindustrian|Sub_BahanBangunan|0|0|1|1900|10|25|20|30.0|30.0|7.0|25|0.4|18|20|1.0|1|30|6.0|-2.4|1|5|4|56|1|1.0|3.6|10|5|-3|-10.0|0.2|1.1|ISSI;IDX80||||Grup_Impack
ICBP|Indofood CBP Sukses Makmur|Sektor_KonsumenPrimer|Sub_MakananOlahan|0|0|1|8000|93|150|19|11.0|16.0|2.3|17|0.9|12|8|1.3|3|40|2.8|-2.6|-1|-10|-7|47|1|1.0|2.4|20|-40|20|-14.0|0.1|1.1|LQ45;IDX30;ISSI;JII;MSCI_Indonesia|Kom_CPO|Kom_Gandum|Doji|Grup_Salim
INDF|Indofood Sukses Makmur|Sektor_KonsumenPrimer|Sub_MakananOlahan|0|0|1|5800|51|110|50|5.0|7.0|0.6|12|0.8|8|7|1.6|5|30|2.5|-2.6|1|-4|-5|52|1|1.1|2.5|14|15|-10|-11.0|0.2|1.1|LQ45;IDX30;ISSI;JII;MSCI_Indonesia;IDXV30|Kom_CPO|Kom_Gandum|Hammer|Grup_Salim
MYOR|Mayora Indah|Sektor_KonsumenPrimer|Sub_MakananOlahan|0|0|1|1900|42|40|15|15.0|25.0|3.0|18|0.7|7|-10|0.7|2|30|4.2|-2.3|-4|-16|-8|41|-1|0.8|2.6|-8|-10|8|-17.0|-0.3|0.8|LQ45;ISSI;JII||Kom_Kakao||Grup_Mayora
CPIN|Charoen Pokphand Indonesia|Sektor_KonsumenPrimer|Sub_Unggas|0|0|1|4100|67|90|44|17.0|28.0|2.6|13|0.3|6|25|1.1|2|35|5.0|-2.5|3|-6|-6|55|1|1.3|2.8|26|30|-25|-9.0|0.4|1.3|LQ45;IDX30;ISSI;JII;MSCI_Indonesia_SmallCap||Kom_JagungKedelai|InverseHeadAndShoulders;BullishEngulfing|Grup_Charoen
JPFA|Japfa Comfeed Indonesia|Sektor_KonsumenPrimer|Sub_Unggas|0|0|1|1600|19|80|43|6.0|9.0|1.0|17|0.9|5|30|1.2|6|35|3.4|-2.5|5|3|2|60|1|1.5|3.4|25|25|-20|-6.0|0.5|1.4|LQ45;ISSI;IDX80||Kom_JagungKedelai|AscendingTriangle|Grup_Japfa
AMRT|Sumber Alfaria Trijaya|Sektor_KonsumenPrimer|Sub_RitelPrimer|0|0|1|1800|75|130|45|20.0|35.0|4.0|20|0.6|3|0|1.8|2|40|4.6|-2.6|-3|-25|-12|40|-1|0.9|2.7|10|-60|30|-17.0|-0.2|0.9|LQ45;IDX30;ISSI;JII;MSCI_Indonesia|||DescendingTriangle|Grup_Alfa
AALI|Astra Agro Lestari|Sektor_KonsumenPrimer|Sub_Perkebunan|0|0|1|6000|11|25|20|8.0|12.0|0.6|6|0.15|8|15|1.4|5|45|3.7|-2.6|6|9|3|62|1|1.4|2.6|18|10|-5|-6.0|0.4|1.3|ISSI;JII;IDX80|Kom_CPO||CupAndHandle|Grup_Astra
LSIP|PP London Sumatra Indonesia|Sektor_KonsumenPrimer|Sub_Perkebunan|0|0|1|1050|7|30|40|6.5|8.0|0.7|11|0.1|20|20|1.1|6|40|6.5|-2.6|7|11|4|63|1|1.6|3.0|21|12|-8|-5.0|0.6|1.4|ISSI;JII;IDX80;IDXHIDIV20|Kom_CPO||BullFlag|Grup_Salim
DSNG|Dharma Satya Nusantara|Sektor_KonsumenPrimer|Sub_Perkebunan|0|0|1|850|9|20|30|6.5|8.0|0.9|15|0.6|15|35|1.0|3|20|3.0|-2.4|6|10|5|61|1|1.3|3.2|19|8|-6|-6.0|0.5|1.3|ISSI;IDX80|Kom_CPO||AscendingTriangle|Grup_Triputra
UNVR|Unilever Indonesia|Sektor_KonsumenPrimer|Sub_ProdukRumahTangga|0|0|1|1300|50|70|15|14.0|32.0|20.0|110|2.5|9|-20|1.3|8|100|3.4|-2.3|-5|-28|-15|36|-1|1.1|2.6|-15|-35|25|-20.0|-0.5|0.7|LQ45;ISSI;JII||Kom_CPO|HeadAndShoulders|Grup_Unilever
MAPI|Mitra Adiperkasa|Sektor_KonsumenNonPrimer|Sub_RitelGayaHidup|0|0|1|1000|17|60|49|7.0|14.0|1.3|17|0.9|6|-5|1.8|1|10|3.1|-2.4|-4|-25|-12|39|-1|0.9|3.3|-12|-25|15|-19.0|-0.4|0.8|LQ45;ISSI;JII;IDX80|||DescendingTriangle|Grup_MAP
MAPA|MAP Aktif Adiperkasa|Sektor_KonsumenNonPrimer|Sub_RitelGayaHidup|0|0|1|650|19|30|20|10.0|17.0|2.0|20|0.4|9|0|1.2|1|15|4.5|-2.4|-2|-20|-10|43|-1|0.9|3.4|-4|-5|3|-16.0|-0.2|0.9|ISSI;IDX80|||RectangleRange|Grup_MAP
ACES|Aspirasi Hidup Indonesia|Sektor_KonsumenNonPrimer|Sub_RitelGayaHidup|0|0|1|380|6|30|40|8.0|22.0|1.0|12|0.3|9|-15|1.1|6|50|6.0|-2.5|-5|-30|-14|34|-1|1.0|3.6|-18|-20|18|-21.0|-0.6|0.7|LQ45;ISSI;JII|||HeadAndShoulders|Grup_Kawan_Lama
ERAA|Erajaya Swasembada|Sektor_KonsumenNonPrimer|Sub_RitelGayaHidup|0|0|1|300|5|25|45|5.0|7.0|0.6|11|1.3|2|5|0.6|5|25|3.2|-2.0|-3|-18|-8|42|-1|1.0|3.5|-6|-8|6|-16.0|-0.3|0.9|ISSI;IDX80|||RectangleRange|Grup_Erajaya
AUTO|Astra Otoparts|Sektor_KonsumenNonPrimer|Sub_Otomotif|0|0|1|1700|8|15|20|5.5|7.0|0.7|14|0.3|8|-3|1.2|9|50|3.4|-2.6|-1|-12|-7|47|1|1.0|2.8|8|3|-2|-13.0|0.0|1.0|ISSI;JII;IDXHIDIV20|||Doji|Grup_Astra
KLBF|Kalbe Farma|Sektor_Kesehatan|Sub_Farmasi|0|0|1|1050|49|120|43|15.0|25.0|2.2|14|0.2|10|5|1.0|4|55|7.0|-2.7|0|-14|-9|48|1|1.1|2.6|22|-25|15|-13.0|0.1|1.1|LQ45;IDX30;ISSI;JII;MSCI_Indonesia;SRIKEHATI||Kom_Gandum|DoubleBottom|Grup_Kalbe
SIDO|Industri Jamu & Farmasi Sido Muncul|Sektor_Kesehatan|Sub_Farmasi|0|0|1|480|14|20|22|12.0|20.0|4.0|32|0.1|30|5|1.1|9|95|9.0|-2.8|2|-8|-6|53|1|1.1|2.4|17|5|-4|-11.0|0.2|1.2|LQ45;ISSI;JII;IDXHIDIV20|||Hammer|Grup_Sido
MIKA|Mitra Keluarga Karyasehat|Sektor_Kesehatan|Sub_RumahSakit|0|0|1|2100|29|40|35|24.0|38.0|5.0|16|0.1|28|10|1.2|2|45|10.0|-2.7|1|-9|-7|51|1|1.0|2.5|20|10|-8|-11.0|0.2|1.2|LQ45;ISSI;JII|||FallingWedge|Grup_Mitra
HEAL|Medikaloka Hermina|Sektor_Kesehatan|Sub_RumahSakit|0|0|1|1250|19|30|35|25.0|40.0|3.8|15|0.6|10|15|1.5|1|10|3.6|-2.6|2|-6|-5|54|1|1.2|2.9|23|8|-6|-9.0|0.3|1.2|LQ45;ISSI;IDX80|||InverseHeadAndShoulders|Grup_Hermina
SILO|Siloam International Hospitals|Sektor_Kesehatan|Sub_RumahSakit|0|0|1|2300|30|25|25|22.0|35.0|3.5|15|0.3|12|12|1.6|1|15|4.8|-2.6|1|-7|-5|52|1|1.0|2.8|15|6|-4|-10.0|0.2|1.1|ISSI;IDX80|||RectangleRange|Grup_Lippo
BBCA|Bank Central Asia|Sektor_Keuangan|Sub_Bank|1|0|0|6200|764|1600|43|13.0|24.0|2.8|22|1.9|5.6|6|29|5.0|70|0|-2.6|-6|-30|-14|33|-1|1.9|3.0|22|-2500|-300|-21.0|-0.3|1.1|LQ45;IDX30;MSCI_Indonesia;MSCI_EmergingMarkets;FTSE_Indonesia;SRIKEHATI;IDXQ30|||Hammer;BullishHarami|Grup_Djarum
BBRI|Bank Rakyat Indonesia|Sektor_Keuangan|Sub_Bank|1|1|0|2900|440|1300|46|7.0|13.0|1.4|18|3.0|7.4|-3|25|11.0|85|0|-2.6|-5|-32|-15|31|-1|1.8|3.4|-15|-1800|700|-22.0|-0.4|1.0|LQ45;IDX30;IDXBUMN20;MSCI_Indonesia;MSCI_EmergingMarkets;FTSE_Indonesia;IDXHIDIV20|||Hammer|Grup_BUMN
BMRI|Bank Mandiri|Sektor_Keuangan|Sub_Bank|1|1|0|3600|336|1100|40|6.0|11.0|1.1|20|1.0|4.9|2|20|10.0|60|0|-2.6|-7|-33|-16|30|-1|1.9|3.5|10|-1600|200|-23.0|-0.5|1.0|LQ45;IDX30;IDXBUMN20;MSCI_Indonesia;MSCI_EmergingMarkets;FTSE_Indonesia;IDXHIDIV20|||MorningStar|Grup_BUMN
BBNI|Bank Negara Indonesia|Sektor_Keuangan|Sub_Bank|1|1|0|3000|112|450|40|5.5|9.5|0.7|13|2.0|4.0|-2|21|10.5|60|0|-2.6|-6|-28|-13|34|-1|1.5|3.4|5|-400|100|-21.0|-0.4|1.0|LQ45;IDX30;IDXBUMN20;MSCI_Indonesia;IDXHIDIV20;IDXV30|||Hammer|Grup_BUMN
BRIS|Bank Syariah Indonesia|Sektor_Keuangan|Sub_BankSyariah|1|1|1|1900|88|200|10|12.0|20.0|1.9|17|1.9|5.6|15|19|1.5|15|0|-2.5|-3|-20|-10|42|1|1.2|3.6|12|-30|20|-16.0|0.0|1.1|LQ45;IDX30;IDXBUMN20;JII;ISSI|||DoubleBottom|Grup_BUMN
BBTN|Bank Tabungan Negara|Sektor_Keuangan|Sub_Bank|1|1|0|850|12|90|40|3.5|6.0|0.3|9|3.4|3.3|5|17|5.0|20|0|-2.4|-6|-25|-12|37|-1|1.0|3.8|-5|-30|20|-19.0|-0.5|0.9|LQ45;IDXBUMN20;IDXV30|||DescendingTriangle|Grup_BUMN
CTRA|Ciputra Development|Sektor_PropertiRealEstat|Sub_Properti|0|0|1|700|13|50|45|6.0|10.0|0.6|10|0.4|20|5|0.9|2|15|2.4|-2.5|-4|-22|-11|40|-1|0.9|3.5|5|-12|8|-18.0|-0.3|0.9|LQ45;ISSI;JII;IDX80|||DescendingTriangle|Grup_Ciputra
BSDE|Bumi Serpong Damai|Sektor_PropertiRealEstat|Sub_Properti|0|0|1|700|15|40|35|4.5|8.0|0.4|9|0.4|30|-10|0.7|0|0|2.1|-2.4|-5|-25|-12|38|-1|0.9|3.6|-8|-15|10|-19.0|-0.4|0.8|LQ45;ISSI;IDX80|||BearFlag|Grup_Sinarmas
PWON|Pakuwon Jati|Sektor_PropertiRealEstat|Sub_Properti|0|0|1|280|13|30|30|7.0|12.0|0.7|10|0.3|35|0|1.1|3|20|2.6|-2.6|-3|-20|-10|41|-1|0.9|3.4|3|-8|5|-17.0|-0.2|0.9|LQ45;ISSI;JII;IDX80|||RectangleRange|Grup_Pakuwon
SMRA|Summarecon Agung|Sektor_PropertiRealEstat|Sub_Properti|0|0|1|350|6|25|60|6.5|15.0|0.5|6|1.0|10|-20|0.6|2|15|1.4|-1.6|-7|-30|-14|32|-1|1.3|4.0|-25|-10|15|-24.0|-0.7|0.6|ISSI;IDX80|||HeadAndShoulders;ThreeBlackCrows|Grup_Summarecon
DMAS|Puradelta Lestari|Sektor_PropertiRealEstat|Sub_KawasanIndustri|0|0|1|130|6|8|25|6.0|8.0|1.2|20|0.05|50|-15|1.0|13|95|4.0|-2.6|0|-10|-6|49|1|1.0|3.0|6|2|-1|-12.0|0.0|1.0|ISSI;IDXHIDIV20|||RectangleRange|Grup_Sinarmas
GOTO|GoTo Gojek Tokopedia|Sektor_Teknologi|Sub_Internet|0|0|1|50|60|60|70|-20.0|-1.0|1.5|-8|0.05|-10|60|0|0|0|1.6|-2.5|-2|-30|-15|30|-1|0.7|2.0|-20|-40|30|-15.0|-0.5|0.5|ISSI|||DescendingTriangle|Grup_GoTo
BUKA|Bukalapak.com|Sektor_Teknologi|Sub_Internet|0|0|1|110|11|15|35|30.0|30.0|0.5|3|0.02|20|-50|0.2|0|0|5.0|-2.4|-2|-15|-8|44|-1|0.8|2.8|-3|-2|1|-14.0|-0.1|0.9|ISSI;IDX80||||Grup_Emtek
DCII|DCI Indonesia|Sektor_Teknologi|Sub_DataCenter|0|0|1|150000|358|5|10|250.0|200.0|50.0|25|0.6|35|20|1.3|0|0|4.0|-2.5|0|5|5|55|1|0.6|3.0|5|0|0|-11.0|0.1|1.0|ISSI|||RectangleRange|Grup_DCI
MTDL|Metrodata Electronics|Sektor_Teknologi|Sub_DistribusiTI|0|0|1|450|6|10|40|8.0|12.0|1.3|17|0.3|4|10|0.8|4|30|4.5|-2.6|0|-8|-5|50|1|1.0|2.8|8|2|-1|-11.0|0.1|1.0|ISSI;IDX80|||RectangleRange|Grup_Metrodata
EMTK|Elang Mahkota Teknologi|Sektor_Teknologi|Sub_Internet|0|0|1|380|23|30|35|25.0|20.0|0.6|2|0.1|5|150|0.8|0|0|2.5|-2.3|-3|-18|-10|42|-1|1.1|3.6|-10|-6|5|-17.0|-0.3|0.8|ISSI;IDX80|||BearFlag|Grup_Emtek
TLKM|Telkom Indonesia|Sektor_Infrastruktur|Sub_Telekomunikasi|0|1|1|2100|208|700|48|9.0|15.0|1.5|15|0.8|15|-5|2.4|8|80|2.4|-2.7|-3|-24|-12|38|-1|1.3|3.0|25|-700|-150|-18.0|-0.2|1.0|LQ45;IDX30;ISSI;JII;IDXBUMN20;MSCI_Indonesia;MSCI_EmergingMarkets;IDXHIDIV20|||BullishHarami;DoubleBottom|Grup_BUMN
ISAT|Indosat Ooredoo Hutchison|Sektor_Infrastruktur|Sub_Telekomunikasi|0|0|1|1500|48|120|16|9.0|16.0|1.4|15|2.0|9|5|3.0|6|50|2.1|-2.4|-2|-18|-9|43|1|1.0|3.4|20|-30|15|-15.0|0.0|1.1|LQ45;IDX30;ISSI;MSCI_Indonesia|||FallingWedge|Grup_Ooredoo
EXCL|XLSmart Telecom Sejahtera|Sektor_Infrastruktur|Sub_Telekomunikasi|0|0|1|1800|33|80|35|28.0|25.0|1.4|4|2.5|4|-30|4.0|2|40|1.0|-2.4|-1|-15|-8|45|1|1.1|3.5|14|-10|5|-14.0|0.1|1.1|LQ45;ISSI;IDX80|||FallingWedge|Grup_Axiata_Sinarmas
TOWR|Sarana Menara Nusantara|Sektor_Infrastruktur|Sub_Menara|0|0|1|480|24|60|45|6.5|12.0|1.0|13|2.7|18|0|2.0|5|35|1.9|-2.6|-4|-22|-11|40|-1|0.9|3.3|-5|-15|8|-17.0|-0.3|0.9|LQ45;ISSI;IDX80|||DescendingTriangle|Grup_Djarum
MTEL|Dayamitra Telekomunikasi|Sektor_Infrastruktur|Sub_Menara|0|1|1|500|42|40|20|18.0|28.0|1.0|6|0.5|20|5|2.4|4|80|2.0|-2.6|-2|-14|-8|45|1|0.9|2.8|10|-5|3|-14.0|0.0|1.0|LQ45;ISSI;IDXBUMN20|||RectangleRange|Grup_BUMN
JSMR|Jasa Marga|Sektor_Infrastruktur|Sub_JalanTol|0|1|0|3000|22|60|30|4.5|9.0|0.6|12|2.3|20|5|1.5|3|20|0.9|-2.5|-5|-28|-13|36|-1|1.0|3.3|-10|-20|12|-19.0|-0.4|0.8|LQ45;IDXBUMN20;IDX80|||HeadAndShoulders|Grup_BUMN
BIRD|Blue Bird|Sektor_TransportasiLogistik|Sub_Transportasi|0|0|1|1400|4|8|30|7.0|12.0|0.8|11|0.1|12|10|1.6|6|40|4.0|-2.6|-3|-12|-7|44|-1|0.9|3.0|5|1|-1|-15.0|-0.2|0.9|ISSI;IDX80||Kom_MinyakBrent|RectangleRange|Grup_BlueBird
ASSA|Adi Sarana Armada|Sektor_TransportasiLogistik|Sub_Transportasi|0|0|1|500|2|8|40|8.0|12.0|0.8|10|1.6|3|30|3.0|2|15|1.6|-2.4|-4|-18|-9|41|-1|1.0|3.6|-6|-2|2|-17.0|-0.3|0.8|ISSI;IDX80||Kom_MinyakBrent|BearFlag|Grup_Adi_Sarana
SMDR|Samudera Indonesia|Sektor_TransportasiLogistik|Sub_Pelayaran|0|0|1|260|4|15|30|5.0|6.0|0.5|12|0.4|15|10|1.6|5|25|3.5|-2.6|4|-2|-3|56|1|1.4|3.6|18|5|-3|-8.0|0.4|1.3|ISSI;IDX80|||AscendingTriangle|Grup_Samudera
TMAS|Temas|Sektor_TransportasiLogistik|Sub_Pelayaran|0|0|1|200|2|10|35|5.5|6.0|1.2|22|0.6|13|15|1.4|7|40|3.0|-2.6|3|-4|-4|54|1|1.2|3.4|12|1|-1|-9.0|0.3|1.2|ISSI;IDX80|||RectangleRange|Grup_Temas
"""

import os as _os, csv as _csv
CSV_EMITEN = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "emiten.csv")
_NUM = ["harga", "mcap", "likuid", "ff", "per", "per5", "pbv", "roe", "f2", "f3", "epsg", "f5", "dy", "dpr", "altman", "beneish",
        "ma50", "ma200", "ma50v200", "rsi", "volr", "atr", "acc", "for20", "ret20", "chg20", "vwap", "bo", "revisi"]
_INT = ["bank", "bumn", "syariah", "macd"]
_LIST = ["indeks", "komU", "komB", "pola"]

def baca_dict_csv(f):
    """DictReader yang tahan format Excel Indonesia (pemisah ';')."""
    import csv as _c
    head = f.readline(); f.seek(0)
    if head.startswith("\ufeff"): head = head[1:]
    delim = ";" if head.count(";") > head.count(",") else ","
    return _c.DictReader(f, delimiter=delim)


def baca_csv_emiten(path=CSV_EMITEN):
    """Sumber data utama v2: data/emiten.csv (bisa diedit di Excel, simpan sebagai CSV UTF-8)."""
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in baca_dict_csv(f):
            if not (r.get("kode") or "").strip():
                continue
            d = {k: (v or "").strip() for k, v in r.items() if k}
            for k in _NUM: d[k] = float(d[k].replace(",", ".")) if d.get(k) not in (None, "") else 0.0
            for k in _INT: d[k] = int(float(d[k])) if d.get(k) not in (None, "") else 0
            for k in _LIST: d[k] = [x.strip() for x in d.get(k, "").split(";") if x.strip()]
            rows.append(d)
    return rows

def parse_emiten(table=None):
    if table is None and _os.path.exists(CSV_EMITEN):
        return baca_csv_emiten()
    rows = []
    for line in (table or EMITEN_TABLE).strip().splitlines():
        p = line.split("|")
        assert len(p) == 41, (len(p), p[0])
        r = dict(kode=p[0], nama=p[1], sektor=p[2], sub=p[3], bank=int(p[4]), bumn=int(p[5]), syariah=int(p[6]),
                 harga=float(p[7]), mcap=float(p[8]), likuid=float(p[9]), ff=float(p[10]),
                 per=float(p[11]), per5=float(p[12]), pbv=float(p[13]), roe=float(p[14]), f2=float(p[15]),
                 f3=float(p[16]), epsg=float(p[17]), f5=float(p[18]), dy=float(p[19]), dpr=float(p[20]),
                 altman=float(p[21]), beneish=float(p[22]),
                 ma50=float(p[23]), ma200=float(p[24]), ma50v200=float(p[25]), rsi=float(p[26]), macd=int(p[27]),
                 volr=float(p[28]), atr=float(p[29]), acc=float(p[30]), for20=float(p[31]), ret20=float(p[32]),
                 chg20=float(p[33]), vwap=float(p[34]), bo=float(p[35]),
                 indeks=[x for x in p[36].split(";") if x], komU=[x for x in p[37].split(";") if x],
                 komB=[x for x in p[38].split(";") if x], pola=[x for x in p[39].split(";") if x], grup=p[40])
        rows.append(r)
    return rows

CSV_MAKRO = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "makro.csv")
if _os.path.exists(CSV_MAKRO):
    with open(CSV_MAKRO, encoding="utf-8-sig", newline="") as _f:
        MAKRO = [(r["id"], r["kelas"], r["label"], float(r["nilai"].replace(",", ".")), r["satuan"], r["tanggal"], r["url"], r["keterangan"])
                 for r in baca_dict_csv(_f) if (r.get("id") or "").strip()]

EMITEN = parse_emiten()
GRUP = sorted({r["grup"] for r in EMITEN})
