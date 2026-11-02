# -*- coding: utf-8 -*-
"""Ekstraksi hasil inferensi Pellet → JSON + ringkasan teks, termasuk jalur penjelasan multi-hop."""
import json, os

def _v(ind, prop):
    vals = getattr(ind, prop, [])
    if not isinstance(vals, list):
        return vals
    return vals[0] if vals else None

def _lbl(x):
    return str(x.label[0]) if getattr(x, "label", None) else x.name

def export(onto, out):
    C = lambda n: onto[n]
    res = {"sektor": [], "emiten": [], "penilaian": [], "cbr": [], "peristiwaAktif": [], "pergerakanAktif": [], "persona": []}
    aktif = set(i.name for i in C("PeristiwaAktif").instances())
    mv_aktif = set(i.name for i in C("PergerakanAktif").instances())
    res["peristiwaAktif"] = sorted(aktif)
    res["pergerakanAktif"] = sorted(mv_aktif)
    # parent map for explanation paths (event -> mv -> mv ...)
    parent = {}
    for ev in C("PeristiwaGeopolitik").instances():
        if ev.name in aktif:
            for m in ev.memicuPergerakan:
                parent.setdefault(m.name, (ev.name, "peristiwa"))
    changed = True
    while changed:
        changed = False
        for m in C("PergerakanMakro").instances():
            if m.name in mv_aktif and m.name in parent:
                for n in m.menyebabkan:
                    if n.name in mv_aktif and n.name not in parent:
                        parent[n.name] = (m.name, "pergerakan"); changed = True
    def path(mname):
        chain = [mname]; cur = mname; guard = 0
        while cur in parent and guard < 12:
            p, kind = parent[cur]; chain.append(p); guard += 1
            if kind == "peristiwa": break
            cur = p
        return [(_lbl(onto[x])) for x in reversed(chain)]

    def classes_of(i):
        return sorted({c.name for c in i.is_a if hasattr(c, "name")} | {c.name for c in i.INDIRECT_is_a if hasattr(c, "name") and c.name in INF_NAMES})
    INF_NAMES = {c.name for c in C("KategoriInferensi").descendants()}

    for s in C("Sektor").instances():
        if not s.name.startswith("Sektor_"): continue
        tw = [{"node": _lbl(m), "jalur": path(m.name), "geopolitik": C("PergerakanGeopolitik") in m.INDIRECT_is_a} for m in s.memilikiTailwind]
        hw = [{"node": _lbl(m), "jalur": path(m.name), "geopolitik": C("PergerakanGeopolitik") in m.INDIRECT_is_a} for m in s.memilikiHeadwind]
        kn = [_lbl(m) for m in s.memilikiPeluangKontrarian]
        res["sektor"].append(dict(
            nama=s.name, label=_lbl(s), skorOutlookAktif=_v(s, "skorOutlookAktif"), skorValuasiSektor=_v(s, "skorValuasiSektor"),
            rasioValuasi=_v(s, "rasioValuasiSektor"), skorTema=_v(s, "skorTemaTertimbang"), poinSentimen=_v(s, "poinSentimenSektor"),
            sentimen=_v(s, "skorSentimenSektor"), poinAsing=_v(s, "poinAliranAsing"),
            kelas=[c for c in classes_of(s) if c in INF_NAMES], tailwind=tw, headwind=hw, kontrarian=kn,
            preseden=[_lbl(p) for p in s.memilikiPreseden], tema=[_lbl(t) for t in s.didukungTema],
            topPick=sorted([e.name for e in s.topPickSektor]), watchlist=sorted([e.name for e in s.watchlistSektor])))
    for a in C("PenilaianSektor").instances():
        res["penilaian"].append(dict(nama=a.name, sektor=a.menilaiSektor.name, skenario=a.dibawahSkenario.name,
                                     makro=_v(a, "skorMakroGeo"), rotasi=_v(a, "skorRotasi"), outlook=_v(a, "skorOutlook"),
                                     kelas=[c for c in classes_of(a) if c in INF_NAMES]))
    num = ["skorFundamental", "skorValuasi", "skorTeknikal", "skorBandar", "skorSentimen", "skorKontribusiSektor", "penaltiRisiko",
           "poinLikuiditas", "skorTotalEmiten", "rasioPERvsHistoris", "nilaiWajar", "potensiUpsidePersen", "hargaStopLoss", "hargaTakeProfit",
           "hargaPenutupan", "atrRupiah"]
    for e in C("Emiten").instances():
        d = dict(kode=e.name, nama=_v(e, "namaPerusahaan"), sektor=e.termasukSektor.name if e.termasukSektor else None)
        for n in num:
            v = _v(e, n)
            d[n] = round(float(v), 2) if isinstance(v, float) else v
        d["kelas"] = [c for c in classes_of(e) if c in INF_NAMES]
        d["diuntungkanOleh"] = [_lbl(m) for m in e.diuntungkanOleh]
        d["ditekanOleh"] = [_lbl(m) for m in e.ditekanOleh]
        d["redFlag"] = [_lbl(n) for n in e.memilikiRedFlag]
        d["direkomendasikanUntuk"] = [i.name for i in e.direkomendasikanUntuk]
        res["emiten"].append(d)
    # ---------------- v2
    res["v2"] = {}
    k = C("Pasar_ID_Okt2026")
    res["v2"]["pasar"] = {n: _v(k, n) for n in ["drawdownIHSGPersen", "perubahanIHSG1BulanPersen", "penurunanHarianTerbesarPersen", "netAsingYTDT", "cds5YBps",
                          "yieldSBN10Y", "spreadSBNUSTBps", "kursUSDIDR", "inflasiYoY", "ffrAtasPersen", "brentUSD", "emasUSD", "breadthPersenDiAtasMA200",
                          "poinStresDrawdown", "poinStresCDS", "poinStresAsing", "poinStresKurs", "poinStresYield", "poinStresBreadth", "skorStresPasar"]}
    res["v2"]["pasar"]["kelas"] = [c for c in classes_of(k) if c in INF_NAMES]
    res["v2"]["regime"] = [dict(nama=g.name, label=_lbl(g), aktif=C("RegimeAktif") in g.INDIRECT_is_a,
                                bobot=[_v(g, x) for x in ["bobotFundamental", "bobotValuasi", "bobotTeknikal", "bobotBandar", "bobotSentimen", "bobotSektor", "bobotRisiko", "bobotLikuiditas", "bobotSmartMoney"]],
                                ambang=_v(g, "ambangTopPickAdaptif"), risiko=_v(g, "risikoPerTransaksiPersen"),
                                tranche=[_v(g, "porsiTranche1"), _v(g, "porsiTranche2"), _v(g, "porsiTranche3")]) for g in C("RegimePasar").instances()]
    res["v2"]["antisipasi"] = [dict(nama=a.name, label=_lbl(a), terpicu=C("AntisipasiTerpicu") in a.INDIRECT_is_a,
                                    mengaktifkan=[_lbl(m) for m in a.antisipasiMengaktifkan]) for a in C("AntisipasiKebijakan").instances()]
    res["v2"]["katalis"] = [dict(nama=x.name, label=_lbl(x), tanggal=_v(x, "tanggalKatalis"), hari=_v(x, "hariMenujuKatalis"),
                                 tipe=[c.name for c in x.is_a if hasattr(c, "name")][0], dekat=C("KatalisDekat") in x.INDIRECT_is_a) for x in C("Katalis").instances()]
    res["v2"]["tesis"] = [dict(nama=t.name, label=_lbl(t), sektor=[s.name for s in t.tesisUntukSektor], indikator=[_lbl(i) for i in t.indikatorKunciTesis],
                               nilai=[_v(i, "nilaiIndikator") for i in t.indikatorKunciTesis], bawah=_v(t, "ambangInvalidasiBawah"), atas=_v(t, "ambangInvalidasiAtas"),
                               pemicu=_v(t, "ambangPemicuBawah"), bufBawah=_v(t, "bufferBawahPersen"), bufAtas=_v(t, "bufferAtasPersen"),
                               kelas=[c for c in classes_of(t) if c in INF_NAMES]) for t in C("TesisInvestasi").instances()]
    res["v2"]["dataKedaluwarsa"] = sorted(i.name for i in C("DataKedaluwarsa").instances())
    for s in res["sektor"]:
        si = C(s["nama"])
        for n in ["skorEkspektasiProbabilistik", "skorOutlookBase", "skorOutlookBull", "skorOutlookBear", "upsideSkenario", "downsideSkenario"]:
            s[n] = _v(si, n)
        s["topPickAdaptif"] = sorted(e.name for e in si.topPickAdaptifSektor)
        s["katalis"] = [_lbl(x) for x in si.sektorMemilikiKatalis]
    for d in res["emiten"]:
        e = C(d["kode"])
        for n in ["kekuatanRelatifPersen", "equityRiskPremium", "skorAdaptifRegime", "ukuranPosisiMaksPersen", "hargaTranche1", "hargaTranche2", "hargaTranche3",
                  "poinSmartMoney", "skorKonfluensi", "skorKontribusiSektorEV", "revisiEPS3BulanPersen"]:
            v = _v(e, n); d[n] = round(float(v), 2) if isinstance(v, (float,)) or (v is not None and not isinstance(v, int)) else v
        d["katalisDekat"] = [_lbl(x) for x in e.memilikiKatalisDekat]
        d["terkonsentrasiDengan"] = sorted(x.name for x in e.terkonsentrasiDengan)
        d["uji"] = C("EmitenUji") in e.INDIRECT_is_a
    for p in C("PeriodeHistoris").instances():
        res["cbr"].append(dict(nama=p.name, label=_lbl(p), kemiripan=_v(p, "skorKemiripan"), analog=C("PeriodeAnalog") in p.INDIRECT_is_a,
                               unggul=[x.name for x in p.unggulPadaPeriode]))
    for i in C("InvestorRitel").instances():
        res["persona"].append(dict(nama=i.name, rekomendasi=sorted([e.name for e in C("Emiten").instances() if i in e.direkomendasikanUntuk])))
    with open(os.path.join(out, "hasil_inferensi.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=str)
    print("Hasil diekspor ke", os.path.join(out, "hasil_inferensi.json"))
    return res
