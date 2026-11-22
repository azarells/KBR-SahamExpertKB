#!/usr/bin/env bash
# Pipeline v2: sentimen (ML <20%) -> bangun KB + SWRL -> reasoning Pellet -> ekspor inferensi -> validasi -> laporan (MD + PDF)
set -e
cd "$(dirname "$0")"
CP=$(ls lib/owlready2/pellet/*.jar | tr '\n' ':'):tools/java
python3 validasi_data.py
python3 sentiment_scorer.py > output/log_sentimen.txt
PYTHONPATH=lib python3 -W ignore build_ontology.py --reason
java -Xmx3g -cp "$CP" ExportInferred output/SahamExpertKB_v2.owl output/SahamExpertKB_v2_inferred.owl 2>/dev/null
java -Xmx3g -cp "$CP" Validate output/SahamExpertKB_v2.owl SektorBullishKuat,SektorBullishModerat,SektorNetral,SektorBearish,SektorPilihanInti,SektorPilihanSatelit,KandidatTopPick,KandidatTopPickAdaptif,KandidatAkumulasiBertahap,RegimeAktif,AntisipasiTerpicu,PeriodeAnalog,PeristiwaAktif 2>/dev/null > output/validasi_owlapi_pellet.txt
python3 make_report.py
echo "Selesai. Lihat folder output/"
# --- Paket Apache Jena Fuseki (aturan SWRL -> Jena, data angka -> xsd:double)
mkdir -p output/fuseki
PYTHONPATH=lib python3 -W ignore tools/swrl2jena.py output/fuseki/saham_rules.rules
java -cp "$CP" ToDouble output/SahamExpertKB_v2.owl output/fuseki/saham_data.ttl 2>/dev/null
cp output/SahamExpertKB_v2_inferred.owl output/fuseki/
echo "Paket Fuseki siap di output/fuseki/"
python3 tools/make_panduan.py "$(mktemp -d)" || true
# --- Uji knowledge base lengkap (98 soal statis + 5 what-if) -> output/HASIL_UJI_KB.md
python3 tools/uji_kb.py --whatif > output/log_uji_kb.txt || echo "Ada soal uji yang GAGAL, lihat output/HASIL_UJI_KB.md"
