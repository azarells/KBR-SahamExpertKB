# -*- coding: utf-8 -*-
"""
Validasi data/emiten.csv sebelum membangun ontologi (setara unit SKKNI J.62DMI00.006.1 "Memvalidasi Data").
Jalankan: python3 validasi_data.py   -> menampilkan kesalahan/peringatan dalam bahasa Indonesia.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb_market as M
SEKTOR = {s[0] for s in M.SEKTOR}; SUB = {s[0]: s[2] for s in M.SUBSEKTOR}
INDEKS = {i[0] for i in M.INDEKS}; KOM = {k[0] for k in M.KOMODITAS}
POLA_OK = None
try:
    from kb_concepts import C
    POLA_OK = {c[0] for c in C}
except Exception:
    pass
RENTANG = {"rsi": (0, 100), "ff": (0, 100), "acc": (-100, 100), "dy": (0, 50), "dpr": (0, 300), "atr": (0, 30), "volr": (0, 50), "macd": (-1, 1)}
err, warn = [], []
rows = M.baca_csv_emiten()
kode = set()
for n, r in enumerate(rows, start=2):
    k = r["kode"]
    if k in kode: err.append(f"baris {n}: kode {k} ganda")
    kode.add(k)
    if r["sektor"] not in SEKTOR: err.append(f"baris {n} ({k}): sektor '{r['sektor']}' tidak dikenal")
    if r["sub"] not in SUB: err.append(f"baris {n} ({k}): subsektor '{r['sub']}' tidak dikenal")
    elif SUB[r["sub"]] != r["sektor"]: warn.append(f"baris {n} ({k}): subsektor {r['sub']} bukan bagian dari {r['sektor']}")
    for i in r["indeks"]:
        if i not in INDEKS: err.append(f"baris {n} ({k}): indeks '{i}' tidak dikenal")
    for i in r["komU"] + r["komB"]:
        if i not in KOM: err.append(f"baris {n} ({k}): komoditas '{i}' tidak dikenal")
    for p in r["pola"]:
        if POLA_OK and p not in POLA_OK: err.append(f"baris {n} ({k}): pola '{p}' tidak dikenal")
    for c, (lo, hi) in RENTANG.items():
        if not (lo <= r[c] <= hi): warn.append(f"baris {n} ({k}): {c}={r[c]} di luar rentang wajar {lo}..{hi}")
    if r["per"] > 0 and r["per5"] <= 0: err.append(f"baris {n} ({k}): PER positif tetapi PER 5 tahun ≤ 0")
    if r["bank"] == 0 and r["altman"] == 0: warn.append(f"baris {n} ({k}): Altman Z non-bank bernilai 0 (belum diisi?)")
    if r["bank"] == 1 and r["f5"] < 8: warn.append(f"baris {n} ({k}): CAR bank {r['f5']}% sangat rendah — cek kolom f5")
    if r["harga"] <= 0: err.append(f"baris {n} ({k}): harga harus > 0")
print(f"Diperiksa {len(rows)} emiten dari {M.CSV_EMITEN}")
for e in err: print("  ERROR  :", e)
for w in warn: print("  CEK    :", w)
print("HASIL: " + ("GAGAL — perbaiki ERROR dulu" if err else "LULUS — data siap dibangun (jalankan: python run_all.py)"))
sys.exit(1 if err else 0)
