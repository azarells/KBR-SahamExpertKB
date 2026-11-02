# -*- coding: utf-8 -*-
"""
KOMPONEN ML/STATISTIK PENDUKUNG (<20% sistem)
Aspect-Based Financial Sentiment Scorer (Bahasa Indonesia + Inggris)

Bukan sekadar menghitung kata positif/negatif:
 1. Nada (tone) dihitung dari leksikon finansial dengan penanganan negasi ("kecilkan peluang kenaikan").
 2. Untuk berita makro, sistem mendeteksi ARAH variabel (minyak naik? bunga naik?) lalu
    menerjemahkannya ke dampak per sektor = arah × sensitivitas sektor terhadap faktor itu
    (sensitivitas berasal dari knowledge base pakar, kb_market.SEKTOR).
    Contoh: "Brent naik ke US$106" → +Energi, -Transportasi, -Konsumen Non-Primer.
 3. Bobot = kredibilitas sumber × peluruhan waktu exp(-umur/90); berita > 180 hari diabaikan.
Output dipakai sebagai data property di ontologi (skorSentimenBerita, skorSentimenSektor, skorSentimenEmiten),
lalu ditafsirkan oleh aturan SWRL (R-SEN-*).
"""
import math, re, datetime
from kb_geo import BERITA, TODAY
from kb_market import SEKTOR, FAKTOR, EMITEN

POS = ["naik", "menguat", "rekor", "tembus", "laba", "tumbuh", "akumulasi", "beli", "overweight", "optimis", "peluang",
       "pulih", "surplus", "rebound", "melesat", "diburu", "jagokan", "pilihan", "murah", "positif", "ekspansi",
       "edges up", "turunkan gwm", "menahan kejatuhan", "berpeluang", "target", "pertahankan rating", "jump", "rise", "gains"]
NEG = ["turun", "melemah", "anjlok", "ambruk", "ambles", "tekanan", "tertekan", "net sell", "aksi jual", "perang", "konflik",
       "gempur", "krisis", "bekukan", "freeze", "depak", "frontier", "defisit", "waspada", "kelam", "terendah", "mendidih",
       "tumbang", "rugi", "kekhawatiran", "dibayangi", "gocap", "tantangan", "tertahan", "plunge", "makin gila", "makin panas",
       "dipertanyakan", "tangguhkan", "belum meyakinkan", "pressure", "uncertainty", "membengkak", "kejatuhan", "anjlok"]
UP = ["naik", "kenaikan", "tembus", "melonjak", "mendidih", "sentuh", "jump", "rekor", "100-plus", "menguat", "melesat", "rise", "hike"]
DOWN = ["turun", "anjlok", "plunge", "melandai", "pangkas", "cut", "melemah"]
NEGATOR = ["kecilkan", "tahan", "holds", "tetap", "pause", "batal", "tak ", "tidak "]

FAKTOR_VAR = {"MINYAK": "Energi", "EMAS": "Emas", "BUNGA": "SukuBunga", "USD": "USD", "CPO": "CPO",
              "INFLASI": "Inflasi", "MSCI": "RiskOff", "PASAR": "RiskOff"}

def tone(text):
    t = text.lower()
    p = sum(t.count(w) for w in POS)
    n = sum(t.count(w) for w in NEG)
    return round((p - n) / (p + n + 1), 3)

def arah(text, var, override):
    if override is not None:
        return override, "anotasi-analis"
    t = text.lower()
    if var in ("MSCI",):
        return 1, "otomatis"              # berita freeze/frontier = risk-off naik
    if var == "PASAR":                     # arah risk-off = kebalikan tone pasar
        tn = tone(text)
        return (1 if tn < 0 else (-1 if tn > 0 else 0)), "otomatis"
    neg = any(w in t for w in NEGATOR)
    up = any(w in t for w in UP)
    dn = any(w in t for w in DOWN)
    if neg and up and not dn:
        return (-1 if "kecilkan" in t else 0), "otomatis-negasi"
    if up and not dn:
        return 1, "otomatis"
    if dn and not up:
        return -1, "otomatis"
    return 0, "otomatis"

def umur(tgl):
    return (TODAY - datetime.date.fromisoformat(tgl)).days

def score_all():
    sens = {s[0]: dict(zip(FAKTOR, s[8])) for s in SEKTOR}
    news = []
    for (nid, tgl, media, url, judul, kelas, kred, ev, sek, emi, var, ov) in BERITA:
        d = umur(tgl)
        tn = tone(judul)
        ar, metode = (arah(judul, var, ov) if var else (0, "-"))
        dampak = {}
        if var:
            f = FAKTOR_VAR[var]
            for s in sens:
                dampak[s] = round(max(-1, min(1, ar * sens[s][f] / 2.0)), 3)
        news.append(dict(id=nid, umur=d, tone=tn, arah=ar, metode=metode, dampak=dampak, kred=kred,
                         sek=sek, emi=emi, valid=(kred >= 0.7 and d <= 180)))
    # agregasi sektor
    sektor_score = {}
    for s in sens:
        num = den = 0.0
        for n in news:
            if not n["valid"]:
                continue
            w = n["kred"] * math.exp(-n["umur"] / 90.0)
            vals = []
            if s in n["dampak"] and n["dampak"][s] != 0:
                vals.append(n["dampak"][s])
            if s in n["sek"]:
                vals.append(n["tone"])
            for v in vals:
                num += w * v; den += w
        sektor_score[s] = round(num / den, 3) if den else 0.0
    # agregasi emiten: 60% berita emiten sendiri + 40% sektor (atau 40% sektor saja)
    emiten_score, emiten_count = {}, {}
    for e in EMITEN:
        num = den = 0.0; cnt = 0
        for n in news:
            if n["valid"] and e["kode"] in n["emi"]:
                w = n["kred"] * math.exp(-n["umur"] / 90.0)
                num += w * n["tone"]; den += w; cnt += 1
        own = num / den if den else None
        sec = sektor_score[e["sektor"]]
        emiten_score[e["kode"]] = round((0.6 * own + 0.4 * sec) if own is not None else 0.4 * sec, 3)
        emiten_count[e["kode"]] = cnt
    return news, sektor_score, emiten_score, emiten_count

if __name__ == "__main__":
    news, ss, es, ec = score_all()
    for n in news:
        print(n["id"], n["umur"], n["tone"], n["arah"], n["metode"], "VALID" if n["valid"] else "stale/low-cred")
    print("\nSKOR SENTIMEN SEKTOR")
    for k, v in sorted(ss.items(), key=lambda x: -x[1]):
        print(f"  {k:32s} {v:+.3f}")
    print("\nSKOR SENTIMEN EMITEN (non-nol)")
    for k, v in sorted(es.items(), key=lambda x: -x[1]):
        print(f"  {k:6s} {v:+.3f} (berita: {ec[k]})")
