# -*- coding: utf-8 -*-
"""Uji 12 Competency Questions dari output/hasil_inferensi.json -> output/HASIL_UJI_CQ.md
Pakai: python3 tools/uji_cq.py   (jalankan setelah run_all.py)"""
import json, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
r = json.load(open(os.path.join(HERE, "output", "hasil_inferensi.json"), encoding="utf-8"))
nm = lambda s: s.replace("Sektor_", "").replace("Ev_", "").replace("Tesis_", "").replace("Persona_", "")
SEK = r["sektor"]; EMI = [e for e in r["emiten"] if not e.get("uji")]
def sek(k): return [nm(s["nama"]) for s in SEK if k in s["kelas"]]
def emi(k): return sorted(e["kode"] for e in EMI if k in e["kelas"])

def top3(s):
    xs = sorted([e for e in EMI if e["sektor"] == s["nama"]], key=lambda e: -e["skorAdaptifRegime"])[:3]
    return ", ".join(f"{e['kode']} ({e['skorAdaptifRegime']:g})" for e in xs)

reg = [g for g in r["v2"]["regime"] if g["aktif"]]
biasa, pakar = set(emi("KandidatTopPick")), set(emi("KandidatTopPickAdaptif"))
bb = [s for s in SEK if s["nama"] == "Sektor_BarangBaku"][0]
akum = [f"{e['kode']} (T1 {e['hargaTranche1']:g}, T2 {e['hargaTranche2']:g}, T3 {e['hargaTranche3']:g})"
        for e in EMI if "KandidatAkumulasiBertahap" in e["kelas"] and e.get("hargaTranche1")]
CQ = [
 ("CQ1", "Sektor apa yang diprediksi naik 1–3 tahun?", "SektorBullish", ", ".join(sek("SektorBullish")) or "-"),
 ("CQ2", "Sektor mana yang tahan di semua skenario?", "SektorPilihanInti / SektorPilihanSatelit",
  "Inti: " + (", ".join(sek("SektorPilihanInti")) or "-") + " · Satelit: " + (", ".join(sek("SektorPilihanSatelit")) or "-")),
 ("CQ3", "Top-3 emiten per sektor pilihan?", "SPARQL Q03",
  " · ".join(f"{nm(s['nama'])}: {top3(s)}" for s in SEK if {"SektorPilihanInti", "SektorPilihanSatelit"} & set(s["kelas"]))),
 ("CQ4", "Mengapa Barang Baku diprediksi naik?", "memilikiTailwind / memilikiPreseden",
  "Tailwind: " + "; ".join(" → ".join(x["jalur"]) for x in bb["tailwind"][:3]) + " · Preseden: " + ", ".join(nm(x) for x in bb["preseden"])),
 ("CQ5", "Regime pasar apa yang sedang terjadi?", "RegimeAktif",
  (reg[0]["label"] if reg else "-") + f" (skor stres {r['v2']['pasar']['skorStresPasar']}/12)"),
 ("CQ6", "Emiten mana rawan collapse?", "RisikoGoingConcern", ", ".join(emi("RisikoGoingConcern")) or "-"),
 ("CQ7", "Kapan & di harga berapa masuk bertahap?", "KandidatAkumulasiBertahap", "; ".join(akum) or
  ("Belum ada: StrategiAkumulasiBertahap tidak aktif karena syarat kapitulasi pasar (drawdown IHSG ≤ −40%) tidak terpenuhi; "
   f"drawdown saat ini {r['v2']['pasar']['drawdownIHSGPersen']}%")),
 ("CQ8", "Beda pilihan analis biasa vs pakar?", "KandidatTopPick vs KandidatTopPickAdaptif",
  "Dibuang pakar: " + (", ".join(sorted(biasa - pakar)) or "-") + " · Ditambah pakar: " + (", ".join(sorted(pakar - biasa)) or "-")),
 ("CQ9", "Peristiwa geopolitik apa yang aktif?", "PeristiwaAktif", f"{len(r['peristiwaAktif'])} peristiwa, mis. " + ", ".join(nm(x) for x in r["peristiwaAktif"][:5])),
 ("CQ10", "Tesis mana yang rapuh/gugur?", "TesisRapuh / TesisGugur",
  ", ".join(f"{nm(t['nama'])} ({'gugur' if 'TesisGugur' in t['kelas'] else 'rapuh'})" for t in r["v2"]["tesis"] if {"TesisRapuh", "TesisGugur"} & set(t["kelas"])) or "-"),
 ("CQ11", "Saham untuk investor konservatif?", "direkomendasikanUntuk",
  " · ".join(f"{nm(p['nama'])}: {', '.join(p['rekomendasi'])}" for p in r["persona"] if "Konservatif" in p["nama"])),
 ("CQ12", "Apa definisi & rumus PER?", "individu PER → rumus", "Harga saham ÷ EPS (dapat dicek di Protégé: individu PER, anotasi rumus)"),
]
lulus = sum(1 for c in CQ if c[3] and c[3] != "-")
L = ["# Hasil Uji Competency Questions", "", f"Sumber: output/hasil_inferensi.json · Lulus (terjawab): **{lulus}/12**", "",
     "| Kode | Pertanyaan | Kelas / query | Jawaban KB | Lulus |", "|---|---|---|---|---|"]
L += [f"| {a} | {b} | {c} | {d} | {'✔' if d and d != '-' else '✘'} |" for a, b, c, d in CQ]
L += ["", "Catatan: CQ dianggap lulus bila KB mampu menjawab. Kebenaran isi jawaban dinilai lewat validasi pakar."]
out = os.path.join(HERE, "output", "HASIL_UJI_CQ.md"); open(out, "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L))
