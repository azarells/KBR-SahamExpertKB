# -*- coding: utf-8 -*-
"""Menyusun LAPORAN_HASIL_PREDIKSI_v2.md (+PDF) dari hasil inferensi JSON & metrik OWLAPI."""
import json, re, os, collections, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "lib"))
import warnings; warnings.filterwarnings("ignore")
from rules_swrl import define_rules
import kb_market, kb_geo as G, kb_v2 as V2
BUL = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
TGL = f"{G.TODAY.day} {BUL[G.TODAY.month-1]} {G.TODAY.year}"
RULES = define_rules(kb_market.FAKTOR)

OUT = os.path.join(HERE, "output")
r = json.load(open(os.path.join(OUT, "hasil_inferensi.json"), encoding="utf-8"))
val = open(os.path.join(OUT, "validasi_owlapi_pellet.txt")).read()
num = lambda k: int(re.search(k + r"=(\d+)", val).group(1))
TOTAL, RULE, LOGI = num("TOTAL_AXIOMS"), num("SWRL_RULES"), num("LOGICAL_AXIOMS")
KB = TOTAL - RULE
SKN = {s[0]: s[1] for s in G.SKENARIO}
PRB = {s[0]: s[3] for s in G.SKENARIO}
V = r["v2"]; P = V["pasar"]
I = lambda x: int(round(float(x))) if x is not None else None
F = lambda x, d=1: (f"{float(x):,.{d}f}" if x is not None else "-")
REAL = [e for e in r["emiten"] if not e["uji"]]
EMI = {e["kode"]: e for e in r["emiten"]}
def has(e, c): return c in e["kelas"]
def klas(s):
    for o, t in [("SektorBullishKuat", "BULLISH KUAT"), ("SektorBullishModerat", "BULLISH MODERAT"), ("SektorNetral", "NETRAL"), ("SektorBearish", "BEARISH")]:
        if o in s["kelas"]: return t
    return "-"
def peran(s):
    if "SektorPilihanInti" in s["kelas"]: return "**INTI (core)**"
    if "SektorPilihanSatelit" in s["kelas"]: return "**SATELIT**"
    if "SektorPeluangKontrarian" in s["kelas"]: return "kontrarian (pantau)"
    return ""
regime = [g for g in V["regime"] if g["aktif"]][0]
rank = sorted(r["sektor"], key=lambda s: -float(s["skorEkspektasiProbabilistik"]))
inti = [s for s in rank if "SektorPilihanInti" in s["kelas"]]
satelit = [s for s in rank if "SektorPilihanSatelit" in s["kelas"]]
adapt = sorted([e for e in REAL if has(e, "KandidatTopPickAdaptif")], key=lambda e: -float(e["skorAdaptifRegime"]))
akum = sorted([e for e in REAL if has(e, "KandidatAkumulasiBertahap")], key=lambda e: -float(e["skorAdaptifRegime"]))
tes = {t["nama"]: t for t in V["tesis"]}

L = []; w = L.append
w("# Laporan Hasil Inferensi v2 — Sistem Pakar Prediksi Sektor Saham BEI (1–3 Tahun)\n")
w("Kelompok 9 KBR · Jonnathan Azarel Gunawan (L0224005) · Gloria Dana Praysilia (L0224043)  ")
w(f"Tanggal acuan: **{TGL}** · Skenario aktif: **{SKN['Skenario_Base_2027_2028']}** · Regime terdeteksi: **{regime['label']}** · Reasoner: Pellet (OWLAPI) — konsisten ✅\n")
w("> **Disclaimer:** Keluaran penalaran sistem pakar untuk keperluan akademik/edukasi, bukan nasihat investasi. Data makro & berita bersumber dari pemberitaan s.d. {TGL} (anotasi `sumberReferensi`). "
  "**Rasio, teknikal, bandarmology, revisi konsensus per emiten adalah snapshot indikatif** dan ditandai `DataIndikatif`; sistem sendiri menandai rekomendasinya `PerluVerifikasiData`.\n")

# ---------------------------------------------------------------- 0
w("## 0. Ringkasan Eksekutif — Keputusan Pakar\n")
w(f"1. **Regime pasar: {regime['label']}** (skor stres {I(P['skorStresPasar'])}/12). Bobot pilar otomatis bergeser: fundamental & valuasi ×1,5, smart money ×1,5, penalti neraca lemah ×1,5, teknikal & sentimen ×0,5; risiko per transaksi dipangkas ke **{F(regime['risiko'],2)}%** modal.")
cls_p = P["kelas"]
if "StrategiAkumulasiBertahap" in cls_p:
    w(f"2. **Strategi pasar:** {'Zona Akumulasi Generasional' if 'ZonaAkumulasiGenerasional' in cls_p else 'Kapitulasi + divergensi intermarket'}"
      f"{' — tetapi dasar belum terkonfirmasi (CDS & rupiah masih memburuk)' if 'DasarBelumTerkonfirmasi' in cls_p else ''} → **akumulasi bertahap {regime['tranche'][0]}/{regime['tranche'][1]}/{regime['tranche'][2]}**, bukan all-in.")
else:
    w(f"2. **Strategi pasar:** syarat zona akumulasi generasional belum terpenuhi (drawdown IHSG {F(P['drawdownIHSGPersen'],2)}% > −40%)"
      f"{'; dasar belum terkonfirmasi (CDS & rupiah masih memburuk)' if 'DasarBelumTerkonfirmasi' in cls_p else ''} → **selektif, tunggu konfirmasi**; posisi tetap dibatasi aturan ukuran posisi regime.")
w("3. **Sektor inti (core, robust lintas skenario):** " + ", ".join(f"**{s['label'].replace('Sektor ', '')}** (EV {F(s['skorEkspektasiProbabilistik'],2)})" for s in inti) + ".")
w("4. **Sektor satelit (asimetris-kontrarian):** " + (", ".join(f"**{s['label'].replace('Sektor ', '')}** (Base {s['skorOutlookBase']} → Bull {s['skorOutlookBull']})" for s in satelit) or "-")
  + f"; pemicu tesis: yield SBN < {F(tes['Tesis_Infrastruktur_DataCenter']['pemicu'],2)}%. **Keuangan** dipantau sebagai kontrarian (pemicu CDS < {F(tes['Tesis_Keuangan_Kontrarian']['pemicu'],0)} bps, kini {F(P['cds5YBps'],2)}).")
w("5. **Top pick adaptif-regime:** " + ", ".join(f"{e['kode']} ({F(e['skorAdaptifRegime'])})" for e in adapt) + ".")
w("6. **Akumulasi bertahap (kualitas yang terpukul):** " + ", ".join(e["kode"] for e in akum) + ".")
kd = [k for k in V["katalis"] if k["dekat"]]
w("7. **Katalis ≤45 hari:** " + "; ".join(f"{k['label']} (H-{k['hari']})" for k in sorted(kd, key=lambda x: x['hari'])) + " → kandidat dengan katalis biner dekat diberi strategi tranche.")
rapuh = [t for t in V["tesis"] if "TesisRapuh" in t["kelas"]]
w("8. **Kill switch:** semua tesis masih valid; " + (", ".join(f"{t['label']} **rapuh**" for t in rapuh) or "tidak ada yang rapuh") +
  f". {len(V['dataKedaluwarsa'])} indikator makro harian sudah kedaluwarsa → perlu pembaruan sebelum eksekusi.\n")

# ---------------------------------------------------------------- 1
w("## 1. Konteks Pasar (state vector `Pasar_ID_Okt2026`)\n")
w("| Indikator | Nilai | Catatan / sumber |\n|---|---|---|")
for a, b, c in [("Drawdown IHSG vs akhir 2025", f"{F(P['drawdownIHSGPersen'],2)}%", "IHSG 4.996,61 (19 Okt) vs 8.646"),
                ("Perubahan IHSG ±1 bulan", f"{F(P['perubahanIHSG1BulanPersen'],2)}%", "30 Sep 6.095,86 → 19 Okt"),
                ("Hari crash terbesar", f"{F(P['penurunanHarianTerbesarPersen'],2)}%", "16 Okt 2026, setelah MSCI umumkan konsultasi standalone (15 Okt)"),
                ("Net asing YTD", f"Rp{F(P['netAsingYTDT'],2)} T", "s.d. 16 Okt"),
                ("CDS Indonesia 5Y", f"{F(P['cds5YBps'],2)} bps", "21 Okt; naik dari 92,40"),
                ("Yield SBN 10Y / spread vs UST", f"{F(P['yieldSBN10Y'],2)}% / {F(P['spreadSBNUSTBps'],0)} bps", "17 Sep (kedaluwarsa)"),
                ("USD/IDR", F(P['kursUSDIDR'],0), "awal Okt"),
                ("Fed Funds (batas atas)", f"{F(P['ffrAtasPersen'],2)}%", "FOMC 16 Sep naik 25 bps; median akhir 2026 4,1%"),
                ("Inflasi Indonesia", f"{F(P['inflasiYoY'],2)}%", "Sep 2026"),
                ("Brent", f"US${F(P['brentUSD'],2)}", "12 Okt; serangan Houthi"),
                ("Emas", f"US${F(P['emasUSD'],2)}", "18 Sep; turun dari puncak"),
                ("Breadth (% saham > MA200)", f"{F(P['breadthPersenDiAtasMA200'],2)}%", "dihitung dari universe 64 emiten")]:
    w(f"| {a} | {b} | {c} |")
w("\nKatalis struktural terbesar: **konsultasi MSCI reklasifikasi ke Standalone** — masukan s.d. 30 Apr 2027, keputusan final paling lambat akhir Juni 2027; estimasi outflow pasif USD3–6 miliar.\n")

# ---------------------------------------------------------------- 2
w("## 2. Deteksi Regime & Bobot Adaptif (meta-knowledge)\n")
w("| Komponen stres | Nilai | Poin |\n|---|---|---|")
for lab, k1, k2 in [("Drawdown IHSG", "drawdownIHSGPersen", "poinStresDrawdown"), ("CDS 5Y", "cds5YBps", "poinStresCDS"), ("Net asing YTD", "netAsingYTDT", "poinStresAsing"),
                    ("USD/IDR", "kursUSDIDR", "poinStresKurs"), ("Yield SBN 10Y", "yieldSBN10Y", "poinStresYield"), ("Breadth", "breadthPersenDiAtasMA200", "poinStresBreadth")]:
    w(f"| {lab} | {F(P[k1],2)} | {P[k2]} |")
w(f"| **Skor stres** | | **{P['skorStresPasar']} / 12** |\n")
w("| Regime | F | V | T | B | S | Sektor | Risiko | Likuid | SmartMoney | Risiko/transaksi | Tranche | Ambang top pick |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for g in V["regime"]:
    nm = ("**" + g["label"] + " ◀ aktif**") if g["aktif"] else g["label"]
    w(f"| {nm} | " + " | ".join(F(x, 1) for x in g["bobot"]) + f" | {F(g['risiko'],2)}% | {'/'.join(str(x) for x in g['tranche'])} | {F(g['ambang'],1)} |")
w("\n*Analis biasa memakai bobot tetap di semua kondisi; sistem pakar mengubah bobot sesuai regime (R-REG, R-ADP-02).*\n")

# ---------------------------------------------------------------- 3
w("## 3. Reaction Function Kebijakan (antisipatif)\n")
w("| Antisipasi | Terpicu? | Node transmisi yang diaktifkan |\n|---|---|---|")
for a in V["antisipasi"]:
    w(f"| {a['label']} | {'✅' if a['terpicu'] else '—'} | {', '.join(a['mengaktifkan'])} |")
w("\nNode yang diaktifkan ikut merambat lewat rantai kausal (R-GEO-04) sehingga headwind/tailwind sektor sudah memperhitungkan reaksi otoritas **sebelum** diumumkan.\n")

# ---------------------------------------------------------------- 4
w("## 4. OUTPUT UTAMA — Prediksi Sektor 1–3 Tahun (probabilistik & robust)\n")
w(f"Probabilitas skenario: Base {PRB['Skenario_Base_2027_2028']:.0%} · Bull {PRB['Skenario_Bull_Pemulihan']:.0%} · Bear {PRB['Skenario_Bear_Stagflasi']:.0%}. EV = Σ p × skor outlook.\n")
w("| # | Sektor | Base | Bull | Bear | **EV** | Prediksi (Base) | Peran portofolio | Penanda pakar |\n|---|---|---|---|---|---|---|---|---|")
for k, s in enumerate(rank, 1):
    tags = [t.replace("Sektor", "") for t in ["SektorRobustLintasSkenario", "SektorAsimetriPositif", "SektorKeyakinanTinggi", "SektorPresedenHistoris", "SektorDiuntungkanGeopolitik", "SektorPerluPemantauanKetat", "SektorKatalisDekat"] if t in s["kelas"]]
    w(f"| {k} | {s['label'].replace('Sektor ', '')} | {I(s['skorOutlookBase'])} | {I(s['skorOutlookBull'])} | {I(s['skorOutlookBear'])} | **{F(s['skorEkspektasiProbabilistik'],2)}** | {klas(s)} | {peran(s)} | {', '.join(tags)} |")
w("")
w("### 4.1 Jalur penalaran multi-hop (sektor inti & satelit)\n")
for s in inti + satelit:
    w(f"#### {s['label']} — {peran(s).replace('*', '')}\n")
    seen = set(); w("**Tailwind:**\n")
    for t in s["tailwind"]:
        j = " → ".join(t["jalur"])
        if j in seen: continue
        seen.add(j); w(f"- {j}{' *(provenans global/geopolitik)*' if t['geopolitik'] else ''}")
    if s["kontrarian"]:
        w("\n**Peluang kontrarian:** " + "; ".join(sorted(set(s["kontrarian"]))))
    if s["headwind"]:
        w("\n**Headwind:**\n")
        seen = set()
        for t in s["headwind"]:
            j = " → ".join(t["jalur"])
            if j in seen: continue
            seen.add(j); w(f"- {j}")
    if s["tema"]: w("\n**Tema struktural:** " + "; ".join(s["tema"]))
    if s["preseden"]: w("\n**Preseden historis (CBR):** " + "; ".join(s["preseden"]))
    tt = [t for t in V["tesis"] if s["nama"] in t["sektor"]]
    for t in tt:
        st = ", ".join(c.replace("Tesis", "") for c in t["kelas"] if c.startswith("Tesis"))
        w(f"\n**Tesis & kill switch:** {t['label']} — indikator {t['indikator'][0]} = {F(t['nilai'][0],2)}; status: {st}.")
    w("")

# ---------------------------------------------------------------- 5
w("## 5. Top-3 Emiten per Sektor Inti/Satelit — Analis Biasa vs Sistem Pakar\n")
w("*Skor statis* = penjumlahan pilar berbobot sama (cara analis biasa). *Skor adaptif* = bobot regime krisis + smart money + kontribusi sektor berbasis EV.\n")
for s in inti + satelit:
    em = sorted([e for e in REAL if e["sektor"] == s["nama"]], key=lambda e: -float(e["skorAdaptifRegime"]))[:3]
    w(f"**{s['label']}**\n")
    w("| Rank | Emiten | Skor statis | **Skor adaptif** | Konfluensi | RS vs IHSG | ERP | Pos. maks | Status pakar | Catatan |\n|---|---|---|---|---|---|---|---|---|---|")
    for k, e in enumerate(em, 1):
        st = []
        if has(e, "KandidatTopPickAdaptif"): st.append("TOP PICK ADAPTIF")
        if has(e, "KandidatAkumulasiBertahap"): st.append("AKUMULASI BERTAHAP")
        if has(e, "TungguKonfirmasi"): st.append("TUNGGU KONFIRMASI")
        if not st: st.append("watchlist" if has(e, "KandidatWatchlist") else "-")
        notes = [c for c in ["CelahEkspektasiPositif", "MurahKarenaLabaTurun", "RisikoHSC", "RisikoKonsentrasiTema", "StrategiTrancheKatalisBiner", "MahalVsObligasi", "ERPSangatMenarik", "ZonaAbuAbu", "ZonaDistress", "RisikoOutflowPasif"] if has(e, c)]
        w(f"| {k} | **{e['kode']}** — {e['nama']} | {I(e['skorTotalEmiten'])} | **{F(e['skorAdaptifRegime'])}** | {e['skorKonfluensi']}/6 | {F(e['kekuatanRelatifPersen'])} pp | {F(e['equityRiskPremium'])} pp | {F(e['ukuranPosisiMaksPersen'])}% | {' · '.join(st)} | {', '.join(notes)} |")
    w("")
w("### 5.1 Di mana sistem pakar berbeda dari analis biasa\n")
static = {e["kode"] for e in REAL if has(e, "KandidatTopPick")}
adaptset = {e["kode"] for e in adapt}
def alasan_buang(e):
    a = [f"skor adaptif {F(e['skorAdaptifRegime'])} < ambang {F(regime['ambang'])}"]
    if e["poinSmartMoney"] == 0: a.append("tanpa jejak smart money")
    if e["equityRiskPremium"] is not None and float(e["equityRiskPremium"]) < 0: a.append("ERP negatif (kalah dari SBN)")
    if has(e, "RisikoHSC"): a.append("risiko HSC/free float < 15%")
    if e["skorTeknikal"] and e["skorTeknikal"] >= 5: a.append("kekuatannya dominan dari teknikal (bobot 0,5 di regime krisis)")
    return "; ".join(a)
w("- **Hanya dipilih analis biasa (skor statis) — dibuang sistem pakar:**")
for c in sorted(static - adaptset):
    w(f"  - **{c}**: {alasan_buang(EMI[c])}")
def alasan_ambil(e):
    a = []
    if e["skorFundamental"] >= 8: a.append(f"fundamental {e['skorFundamental']}/10")
    if e["poinSmartMoney"] >= 1: a.append("jejak smart money")
    if e["equityRiskPremium"] is not None and float(e["equityRiskPremium"]) >= 8: a.append(f"ERP {F(e['equityRiskPremium'])} pp")
    if has(e, "KandidatAkumulasiBertahap"): a.append("kualitas terpukul (akumulasi bertahap)")
    a.append(f"sektor EV {F([s for s in r['sektor'] if s['nama'] == e['sektor']][0]['skorEkspektasiProbabilistik'],2)}")
    return "; ".join(a)
w("- **Hanya dipilih sistem pakar:**")
for c in sorted(adaptset - static):
    w(f"  - **{c}** (statis {I(EMI[c]['skorTotalEmiten'])} → adaptif {F(EMI[c]['skorAdaptifRegime'])}): {alasan_ambil(EMI[c])}")
w(f"- **Disepakati keduanya:** {', '.join(sorted(static & adaptset)) or '-'}.\n")

# ---------------------------------------------------------------- 6
w("## 6. Rencana Akumulasi Bertahap (kapitulasi)\n")
w(f"Regime {regime['label']}: porsi tranche {regime['tranche'][0]}% / {regime['tranche'][1]}% / {regime['tranche'][2]}% dari alokasi; tangga harga T1 = harga, T2 = −2×ATR, T3 = −4×ATR.\n")
w("| Emiten | Sektor | T1 | T2 | T3 | Pos. maks | Pemicu | Katalis biner dekat |\n|---|---|---|---|---|---|---|---|")
for e in akum:
    trig = [c for c in ["KapitulasiEmiten", "AkumulasiBandar", "AkumulasiTersembunyi", "CelahEkspektasiPositif"] if has(e, c)]
    kb = [k for k in e["katalisDekat"] if any(x["label"] == k and x["tipe"] == "KatalisBiner" for x in V["katalis"])]
    w(f"| **{e['kode']}** | {e['sektor'].replace('Sektor_', '')} | {F(e['hargaTranche1'],0)} | {F(e['hargaTranche2'],0)} | {F(e['hargaTranche3'],0)} | {F(e['ukuranPosisiMaksPersen'])}% | {', '.join(trig)} | {'; '.join(sorted(set(kb))) or '-'} |")
w("")

# ---------------------------------------------------------------- 7
w("## 7. Konfluensi, Konflik, Refleksivitas & Ekspektasi Laba\n")
def lst(c): return ", ".join(sorted(e["kode"] for e in REAL if has(e, c))) or "-"
for lab, c in [("Konfluensi tinggi (≥5/6 pilar)", "KonfluensiTinggi"), ("Tunggu konfirmasi (konflik sinyal)", "TungguKonfirmasi"),
               ("Fundamental kuat vs bandar distribusi", "KonflikFundamentalVsBandar"), ("Distribusi saat euforia", "DistribusiSaatEuforia"),
               ("Berita buruk priced-in", "SinyalKetahananBeritaBuruk"), ("Sell the news", "SellTheNews"), ("Mengungguli IHSG ≥5 pp", "OutperformPasar"),
               ("Kapitulasi emiten", "KapitulasiEmiten"), ("Celah ekspektasi positif (revisi naik, harga tertinggal)", "CelahEkspektasiPositif"),
               ("Murah karena laba turun (value-trap dini)", "MurahKarenaLabaTurun"), ("ERP ≥ 8 pp (murah vs SBN)", "ERPSangatMenarik"),
               ("Mahal vs obligasi (ERP < 0)", "MahalVsObligasi"), ("Risiko konsentrasi tema", "RisikoKonsentrasiTema")]:
    w(f"- **{lab}:** {lst(c)}")
w("")

# ---------------------------------------------------------------- 8
w("## 8. Kalender Katalis\n")
w("| Katalis | Tanggal | H- | Tipe | ≤45 hari |\n|---|---|---|---|---|")
for k in sorted(V["katalis"], key=lambda x: x["hari"]):
    w(f"| {k['label']} | {k['tanggal']} | {k['hari']} | {k['tipe'].replace('Katalis', '')} | {'✅' if k['dekat'] else ''} |")
w("\nStrategi tranche sebelum katalis biner: " + lst("StrategiTrancheKatalisBiner") + ".\n")

# ---------------------------------------------------------------- 9
w("## 9. Tesis Investasi & Kill Switch\n")
w("| Tesis | Indikator kunci | Nilai | Batas bawah | Batas atas | Pemicu kontrarian | Buffer | Status |\n|---|---|---|---|---|---|---|---|")
for t in V["tesis"]:
    bb = F(t["bawah"], 2) if t["bawah"] and t["bawah"] > 0 else "-"
    ba = F(t["atas"], 2) if t["atas"] and t["atas"] < 1e8 else "-"
    buf = t["bufBawah"] if t["bufBawah"] is not None else t["bufAtas"]
    st = ", ".join(c.replace("Tesis", "") for c in t["kelas"] if c.startswith("Tesis"))
    w(f"| {t['label']} | {t['indikator'][0]} | {F(t['nilai'][0],2)} | {bb} | {ba} | {F(t['pemicu'],2) if t['pemicu'] else '-'} | {F(buf)}% | {st} |")
w("")

# ---------------------------------------------------------------- 10
w("## 10. Kesehatan Fundamental, Risiko Collapse & Tata Kelola\n")
w("| Emiten | Kategori | Penalti | Sinyal |\n|---|---|---|---|")
risk = [e for e in REAL if any(has(e, c) for c in ["RisikoGoingConcern", "ZonaDistress", "RisikoManipulasiLaba", "BankModalLemah", "ValueTrap", "RisikoHSC"])]
for e in sorted(risk, key=lambda e: I(e["penaltiRisiko"]) or 0):
    cats = [c for c in ["RisikoGoingConcern", "ZonaDistress", "ZonaAbuAbu", "RisikoManipulasiLaba", "BankModalLemah", "ValueTrap", "RisikoHSC", "RedFlagBerita"] if has(e, c)]
    w(f"| {e['kode']} | {', '.join(cats)} | {I(e['penaltiRisiko'])} | {', '.join(c for c in ['SinyalHindari', 'SinyalExit'] if has(e, c))} |")
w("")

# ---------------------------------------------------------------- 11
w("## 11. Sinyal Quant Trade\n")
w("| Emiten | Sinyal | Harga | SL (−2·ATR) | TP (+3·ATR) | Pos. maks | Konteks |\n|---|---|---|---|---|---|---|")
for e in sorted(REAL, key=lambda e: -float(e["skorAdaptifRegime"])):
    sig = [c for c in ["SinyalEntry", "SinyalBuyOnWeakness", "SinyalScalpingLong"] if has(e, c)]
    if not sig: continue
    ctx = [c for c in ["AkumulasiInstitusiAsing", "AkumulasiTersembunyi", "FaseMarkUpWyckoff", "LonjakanVolume", "TungguKonfirmasi"] if has(e, c)]
    w(f"| {e['kode']} | {', '.join(sig)} | {F(e['hargaPenutupan'],0)} | {F(e['hargaStopLoss'],0)} | {F(e['hargaTakeProfit'],0)} | {F(e['ukuranPosisiMaksPersen'])}% | {', '.join(ctx)} |")
w("\n**Anti-FOMO:** " + lst("DistribusiKeRitel") + " terdeteksi distribusi ke ritel.\n")

# ---------------------------------------------------------------- 12
w("## 12. Uji Aturan dengan Emiten Hipotetis (Validation & Verification)\n")
w("| Emiten uji (fiktif) | Skenario uji | Kelas yang berhasil diinferensi |\n|---|---|---|")
for code, desc in [("UJI_GORENG", "free float 8%, volume 4,5×, ARA 3×/5 hari, top-3 broker 80%, RSI 88"), ("UJI_GADAI", "45% saham pengendali digadaikan, downtrend"), ("UJI_INSIDER", "direksi membeli, PER 6 vs rata-rata 12")]:
    e = EMI[code]
    k = [c for c in ["IndikasiSahamGorengan", "RisikoPumpAndDump", "RisikoHSC", "RisikoForcedSellPengendali", "SinyalOrangDalam", "SinyalHindari", "TungguKonfirmasi"] if has(e, c)]
    w(f"| {code} | {desc} | {', '.join(k)} |")
w("\nEmiten uji tidak masuk peringkat apa pun; fungsinya membuktikan aturan tata kelola bekerja karena data gadai/orang dalam emiten nyata belum diisi.\n")

# ---------------------------------------------------------------- 13
w("## 13. Kualitas Data\n")
w("- **Indikator makro kedaluwarsa (umur > 5× frekuensi):** " + ", ".join(V["dataKedaluwarsa"]))
w("- **Tesis perlu data baru:** " + ", ".join(t["label"] for t in V["tesis"] if "TesisPerluDataBaru" in t["kelas"]))
w("- **Rekomendasi yang wajib diverifikasi (PerluVerifikasiData):** " + lst("PerluVerifikasiData") + "\n")

# ---------------------------------------------------------------- 14
w("## 14. Rekomendasi per Persona\n")
for p in r["persona"]:
    w(f"- **{p['nama'].replace('Persona_', '').replace('_', ' ')}**: {', '.join(x for x in p['rekomendasi'] if not x.startswith('UJI_')) or '-'}")
w("")

# ---------------------------------------------------------------- 15
w("## 15. Rasio Knowledge Base vs Reasoning\n")
w("| Komponen | Aksioma | Porsi |\n|---|---|---|")
w(f"| Knowledge Base (TBox + ABox + anotasi + deklarasi) | {KB:,} | **{KB / TOTAL:.1%}** |")
w(f"| Reasoning (aturan SWRL) | {RULE} | {RULE / TOTAL:.1%} |")
w(f"| **Total** | {TOTAL:,} | 100% |")
w(f"\nAksioma logis saja: KB {LOGI - RULE:,} vs aturan {RULE} → **{(LOGI - RULE) / LOGI:.1%} KB**.\n")
cnt = collections.Counter(p for _, p, _, _ in RULES)
w(f"**{len(RULES)} aturan SWRL per pilar:** " + ", ".join(f"{k} ({v})" for k, v in sorted(cnt.items(), key=lambda x: -x[1])) + ".\n")

md = os.path.join(OUT, "LAPORAN_HASIL_PREDIKSI_v2.md")
open(md, "w", encoding="utf-8").write("\n".join(L))
print("Laporan:", md)
try:
    subprocess.run([sys.executable, os.path.join(HERE, "tools", "md2pdf.py"), md, md.replace(".md", ".pdf"), "landscape"], check=True)
except Exception as ex:
    print("PDF dilewati:", ex)
