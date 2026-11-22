# SahamExpertKB v2 — Sistem Pakar Prediksi Sektor Saham BEI (Protégé OWL + SWRL)

**Kelompok 9 KBR** · Jonnathan Azarel Gunawan (L0224005) · Gloria Dana Praysilia (L0224043)
Horizon prediksi: **1–3 tahun** · Tanggal acuan data: **19 November 2026** · Versi 2.0

Ontologi pakar yang menggabungkan Fundamental, Teknikal, Bandarmology, Sentimen (aspect-based), Geopolitik-Makro multi-hop, CBR, dan rotasi siklus,
ditambah **lapisan meta-penalaran v2**: deteksi regime + bobot adaptif, reaction function kebijakan, refleksivitas (priced-in), kapitulasi & akumulasi bertahap,
revisi laba, ERP vs SBN, tata kelola/gorengan, ekspektasi probabilistik & robustness (inti–satelit), konfluensi/konflik, ukuran posisi, katalis, tesis & kill switch,
dan kesadaran kualitas data. **303 aturan SWRL**; knowledge base = **98,0% dari seluruh aksioma**.

---

## 1. Isi folder

| File | Fungsi |
|---|---|
| `output/SahamExpertKB_v2.owl` | **File utama untuk Protégé** — TBox + ABox + 303 aturan SWRL (RDF/XML). |
| `output/SahamExpertKB_v2_inferred.owl` | Ontologi + seluruh hasil inferensi Pellet (±7.900 aksioma inferensi). Bisa dibuka tanpa reasoner. |
| `output/LAPORAN_HASIL_PREDIKSI_v2.md` / `.pdf` | Laporan hasil v2: regime, reaction function, prediksi sektor probabilistik (inti/satelit), analis biasa vs pakar, akumulasi bertahap, katalis, kill switch, dll. |
| `output/DOKUMEN_PENGEMBANGAN_v2.pdf` | Sumber data (35), katalog indikator (132), modul pakar pembeda, jejak penalaran, roadmap pipeline. |
| `output/TUTORIAL_AKSES_PROTEGE_v2.pdf` | Tutorial langkah demi langkah (termasuk demo fitur v2 & what-if yang sudah diuji). |
| `output/fuseki/` | **Paket Apache Jena Fuseki 6**: `saham_data.ttl`, `saham_rules.rules` (303 aturan SWRL → aturan Jena, hasil identik dengan Pellet), config 2 dataset (`/saham` penalaran langsung, `/saham-pellet`), `start_fuseki.sh/.bat`, 15 query SPARQL, contoh what-if SPARQL Update. |
| `output/PANDUAN_FUSEKI_PELLET_SWRLTAB.pdf` | Panduan Protégé + Pellet, JDK 25, Fuseki, dan perbaikan SWRLTab/SQWRLTab kosong. |
| `output/uji_swrltab.owl` | Ontologi mini (1 aturan) untuk mendiagnosis SWRLTab. |
| `output/SQWRL_queries.txt` | 32 query siap tempel di SQWRLTab (Q01–Q17 v1, Q18–Q32 v2). |
| `output/hasil_inferensi.json` | Hasil inferensi terstruktur (integrasi aplikasi sekuritas). |
| `output/validasi_owlapi_pellet.txt` | Validasi OWLAPI + Pellet: konsisten, metrik aksioma. |
| `kb_taxonomy.py`, `kb_concepts.py` | TBox & basic knowledge (rasio + rumus + ambang, teknikal, pola, mekanisme BEI, aksi korporasi, bias perilaku, heuristik pakar). |
| `kb_market.py` | Sektor IDX-IC (sensitivitas 12 faktor), 66 indeks, broker, institusi, komoditas, indikator makro, 64 emiten. |
| `kb_geo.py` | 36 peristiwa, 49 node transmisi, 53 berita 2025–2026 (URL), 3 skenario, 9 kasus CBR, stakeholder & persona. |
| `kb_sources.py` | **v2** — 35 sumber data & 132 indikator (pilar, leading/coincident/lagging, frekuensi, status integrasi). |
| `kb_v2.py` | **v2** — kelas pakar lanjutan, state vector pasar, 4 regime + bobot, reaction function, 13 katalis, 6 tesis + kill switch, revisi konsensus, emiten uji fiktif, heuristik H16–H31. |
| `rules_swrl.py`, `rules_v2.py` | 182 aturan v1 + 121 aturan v2 (R-DAT, R-STR, R-REG, R-PAS, R-ANT, R-RS, R-REF, R-KAP, R-REV, R-ERP, R-GOV, R-ROB, R-ADP, R-KON, R-POS, R-KAT, R-TES). |
| `sentiment_scorer.py` | Komponen ML pendukung (<20%): sentimen aspect-based. |
| `build_ontology.py`, `export_results.py`, `make_report.py`, `make_blueprint.py`, `run_all.sh`, `tools/*` | Pipeline build → reasoning → ekspor → validasi → laporan PDF. |

## 2. Cara membuka & menjalankan di Protégé (5.6.x)

1. **File › Open** → `SahamExpertKB_v2.owl`.
2. **Pilih reasoner Pellet** (aturan memakai built-in `swrlb:greaterThan`, `add`, `multiply`, `abs`, `divide`):
   - Jika belum ada: **File › Check for plugins…** → centang **Pellet** (atau *Openllet*) → install → restart Protégé.
   - **Reasoner › Pellet › Start reasoner**. Hasil inferensi tampil berlatar kuning di tab *Individuals by class*.
   - ⚠️ **HermiT tidak mendukung SWRL built-in** — jangan gunakan HermiT untuk ontologi ini.
3. **Alternatif: SWRLTab (engine Drools)** — *Window › Tabs › SWRLTab* → tombol **OWL+SWRL→Drools**, **Run Drools**, **Drools→OWL**. Semua 303 aturan terlihat dengan nama kode (kolom *Name*) dan penjelasan (kolom *Comment*).
4. **SQWRLTab** — *Window › Tabs › SQWRLTab* → tempel query dari `SQWRL_queries.txt`, mis. top-3 emiten Barang Baku:
   ```
   termasukSektor(?e, Sektor_BarangBaku) ^ skorTotalEmiten(?e, ?t) -> sqwrl:select(?e, ?t) ^ sqwrl:orderByDescending(?t) ^ sqwrl:limit(3)
   ```
5. Yang perlu dilihat saat demo:
   - Individu `Sektor_BarangBaku` → *Property assertions*: `skorOutlookAktif`, `memilikiTailwind`, `memilikiPreseden`, `topPickSektor`.
   - Kelas `SektorBullishKuat`, `KandidatTopPick`, `RisikoGoingConcern`, `AkumulasiTersembunyi`, `PeriodeAnalog` → *Instances*.
   - Klik tanda **?** pada aksioma inferensi untuk melihat *explanation* (aturan mana yang memicunya).

**Ganti skenario (what-if):** ubah `statusAktif` pada `Skenario_Base_2027_2028` menjadi 0 dan `Skenario_Bull_Pemulihan` atau `Skenario_Bear_Stagflasi` menjadi 1, lalu jalankan ulang reasoner. Skor ketiga skenario juga selalu tersedia di individu `Penilaian_*`.

## 3. Arsitektur penalaran

```
 BERITA (44, kredibilitas, umur)  ──R-GEO-01──►  PERISTIWA AKTIF (perang, Fed, OPEC+, MSCI, inflasi, ...)
                                                     │ memicuPergerakan (hop-1)
                                                     ▼
                                    NODE TRANSMISI MAKRO ──menyebabkan──► ... (multi-hop, R-GEO-04)
                                     │ menguntungkan / merugikan / peluang kontrarian / harga komoditas
                    ┌────────────────┴─────────────────┐
                    ▼                                  ▼
       SEKTOR: tailwind/headwind (penjelasan)   EMITEN: diuntungkanOleh / ditekanOleh (eksposur komoditas)

 SEKTOR × SKENARIO (PenilaianSektor): Σ sensitivitas×arah (12 faktor) + valuasi PER-band + tema×2
                                      + sentimen + aliran asing + rotasi siklus  ──►  BULLISH KUAT/MODERAT/NETRAL/BEARISH
 CBR: kemiripan skenario aktif vs 9 periode historis  ──►  PeriodeAnalog ──► SektorPresedenHistoris
 EMITEN: fundamental(10) + valuasi(3) + teknikal(7) + bandar(5) + sentimen(±2) + sektor(−3..4) + risiko(−5..0) + likuiditas(2)
         ──►  KandidatTopPick / Watchlist / KeyakinanTinggi, SinyalEntry/BuyOnWeakness/Exit/Hindari/Scalping, SL/TP (ATR)
 PERSONA (profil risiko + horizon)  ──►  direkomendasikanUntuk
```

Prinsip desain SWRL: semua aturan skor memakai interval **[bawah, atas)** yang saling lepas dan menutup seluruh domain, karena SWRL monoton (tanpa *negation-as-failure*); dengan begitu setiap emiten/sektor selalu mendapat tepat satu nilai per pilar dan penjumlahan `swrlb:add` selalu terpicu.

## 4. Stakeholder

| Peran | Individu | Keluaran yang dikonsumsi |
|---|---|---|
| Utama (mitra implementasi) | `Stk_MitraSekuritas` | Semua keluaran (engine tertanam di aplikasi trading) |
| Kandidat | `Stk_TimEquityResearch`, `Stk_AnalisJunior`, `Stk_ManajerInvestasi`, `Stk_EdukatorKomunitas` | Prediksi sektor, what-if, kesehatan fundamental, edukasi |
| Validator | `Stk_PanelPakar` | Validasi ambang & backtest walk-forward |
| Regulator (kepatuhan) | `Stk_OJK_Kepatuhan`, `Stk_BEI_Kepatuhan` | Batasan: alat riset/edukasi, bukan nasihat investasi personal |
| End user (persona) | Mahasiswa-Konservatif, PekerjaMuda-Moderat, GenZ-Agresif, Trader-Scalper | Rekomendasi sesuai profil (aturan R-PRF) |

## 5. Memperbarui data & membangun ulang

Semua data yang diisi manusia ada di folder `data/` (bukan di file .py / .owl):

| File | Isi |
|---|---|
| `data/emiten.csv` | 1 baris per emiten (fundamental, valuasi, teknikal, bandar, indeks). Isi lewat `output/Template_Data_Emiten.xlsx` (sheet KAMUS_KOLOM = cara hitung tiap kolom, NILAI_VALID = nama sektor/indeks yang sah), lalu simpan sebagai CSV UTF-8. |
| `data/berita.csv` | Berita (tanggal, URL, peristiwa, sektor, label arah). |
| `data/makro.csv` | Indikator makro (BI-Rate, Fed, kurs, Brent, emas, CDS, ...). |
| `data/kondisi_pasar.csv` | State vector pasar untuk deteksi regime. |
| `data/kamus_kolom.json` | Kamus kolom emiten.csv. |

```
python validasi_data.py    # harus LULUS
python run_all.py          # build OWL -> Pellet -> laporan -> paket Fuseki (Windows/macOS/Linux; ./run_all.sh juga tersedia)
```
File `.owl` adalah hasil build — jangan diedit langsung bila ingin perubahan permanen.
Tanggal acuan data: `data/tanggal_acuan.txt`. CSV dengan pemisah `;` dan koma desimal (Excel Indonesia) diterima.
Langkah kerja detail dari awal sampai akhir: `output/BUKU_KERJA_LANGKAH_DEMI_LANGKAH.pdf`. Panduan lengkap alur data, pembagian tugas berdua, dan langkah end-to-end: `output/PANDUAN_LENGKAP_PROYEK_DAN_PEMBAGIAN_TUGAS.pdf`.

## 6. Catatan penting data

- Indikator makro, peristiwa, dan berita bersumber dari pemberitaan Okt 2026 (URL di anotasi `sumberReferensi`/`urlSumber`).
- **Rasio keuangan, harga, teknikal, dan bandarmology emiten adalah snapshot indikatif** (anotasi `catatanData`) untuk demonstrasi penalaran. Kode broker dan keanggotaan indeks juga indikatif. Perbarui dari IDX/laporan keuangan/terminal data sebelum dipakai untuk keputusan.
- Keluaran sistem adalah alat bantu riset & edukasi, **bukan nasihat investasi**.

## 7. Menguji knowledge base (103 soal)

```
python3 tools/uji_kb.py            # 98 soal statis (SPARQL ke ontologi hasil Pellet), ±5 detik
python3 tools/uji_kb.py --whatif   # + 5 what-if (ubah data -> Pellet ulang), ±35 detik
```

- Hasil per soal (pertanyaan, cara uji di Protégé, jawaban KB, query SPARQL): `output/HASIL_UJI_KB.md`.
- Semua query SPARQL untuk Fuseki: `output/uji_kb/queries_uji.rq`; hasil terstruktur: `output/uji_kb/hasil_uji_kb.json`.
- `run_all.py` menjalankan uji ini otomatis sebagai langkah 12 (log: `output/log_uji_kb.txt`). Kode keluar 0 = semua lulus.
- 17 modul: struktur KB, kebenaran aturan (tepat satu skor per pilar, penjumlahan skor), pengetahuan dasar, fundamental, teknikal,
  bandarmology, sentimen, geopolitik & makro, indeks, prediksi sektor, rekomendasi emiten, meta-penalaran, stakeholder, kualitas data,
  dan what-if (skenario bull/bear, emiten memburuk, kapitulasi IHSG, CDS membaik). 12 competency questions proposal = B01, C04, G01, I01, I03, I04, J01, J02, K01, K04, K08, L02 (pemetaan lengkap ada di HASIL_UJI_KB.md).
- `tools/uji_cq.py` (12 CQ versi lama) tetap tersedia.
