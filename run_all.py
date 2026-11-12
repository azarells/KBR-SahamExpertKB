# -*- coding: utf-8 -*-
"""Pipeline lintas OS (Windows / macOS / Linux) — padanan run_all.sh.
Pakai:  python run_all.py          (Windows)
        python3 run_all.py         (macOS / Linux)
"""
import glob, os, subprocess, sys, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
PY = sys.executable
ENV = dict(os.environ, PYTHONPATH=os.path.join(HERE, "lib"), PYTHONIOENCODING="utf-8")
CP = os.pathsep.join(sorted(glob.glob(os.path.join("lib", "owlready2", "pellet", "*.jar"))) + [os.path.join("tools", "java")])
JAVA = shutil.which("java")


def langkah(no, judul, cmd, out=None, wajib=True):
    print(f"\n[{no}] {judul} ...", flush=True)
    f = open(out, "w", encoding="utf-8") if out else None
    r = subprocess.run(cmd, env=ENV, stdout=f or None, stderr=subprocess.DEVNULL if cmd[0] == JAVA else None)
    if f: f.close()
    if r.returncode != 0:
        print(f"    GAGAL (kode {r.returncode}).", flush=True)
        if wajib: sys.exit(r.returncode)
    else:
        print("    OK", flush=True)


if JAVA is None:
    sys.exit("Java tidak ditemukan. Pasang JDK 21+ (disarankan JDK 25) dan pastikan perintah 'java -version' berjalan.")
os.makedirs(os.path.join("output", "fuseki"), exist_ok=True)
langkah(1, "Validasi data (data/*.csv)", [PY, "validasi_data.py"])
langkah(2, "Skor sentimen berita", [PY, "sentiment_scorer.py"], out=os.path.join("output", "log_sentimen.txt"))
langkah(3, "Bangun ontologi + SWRL + reasoning Pellet", [PY, "-W", "ignore", "build_ontology.py", "--reason"])
langkah(4, "Ekspor hasil inferensi (OWLAPI)", [JAVA, "-Xmx3g", "-cp", CP, "ExportInferred",
         "output/SahamExpertKB_v2.owl", "output/SahamExpertKB_v2_inferred.owl"])
langkah(5, "Validasi konsistensi (OWLAPI + Pellet)", [JAVA, "-Xmx3g", "-cp", CP, "Validate", "output/SahamExpertKB_v2.owl",
         "SektorBullishKuat,SektorBullishModerat,SektorNetral,SektorBearish,SektorPilihanInti,SektorPilihanSatelit,"
         "KandidatTopPick,KandidatTopPickAdaptif,KandidatAkumulasiBertahap,RegimeAktif,AntisipasiTerpicu,PeriodeAnalog,PeristiwaAktif"],
        out=os.path.join("output", "validasi_owlapi_pellet.txt"))
langkah(6, "Laporan hasil prediksi (MD + PDF)", [PY, "make_report.py"], wajib=False)
langkah(7, "Aturan Jena untuk Fuseki", [PY, "-W", "ignore", "tools/swrl2jena.py", "output/fuseki/saham_rules.rules"])
langkah(8, "Data Fuseki (angka -> xsd:double)", [JAVA, "-cp", CP, "ToDouble", "output/SahamExpertKB_v2.owl", "output/fuseki/saham_data.ttl"])
shutil.copy(os.path.join("output", "SahamExpertKB_v2_inferred.owl"), os.path.join("output", "fuseki"))
langkah(9, "Dokumen pengembangan (PDF)", [PY, "make_blueprint.py"], wajib=False)
langkah(10, "Uji 12 competency questions", [PY, "tools/uji_cq.py"], out=os.path.join("output", "log_uji_cq.txt"), wajib=False)
langkah(11, "Panduan proyek (PDF)", [PY, "tools/make_panduan.py", tempfile.mkdtemp()], wajib=False)
print("\nSELESAI. Buka folder output/ — file utama: SahamExpertKB_v2.owl, LAPORAN_HASIL_PREDIKSI_v2.pdf, validasi_owlapi_pellet.txt")
print("Catatan: langkah 6, 9 & 11 (PDF) butuh Node.js + Playwright; bila gagal, file .md dan .owl tetap terbentuk.")
