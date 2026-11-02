# ======================================================================
# WHAT-IF (SPARQL Update) — jalankan di tab "query" dataset /saham dengan endpoint UPDATE
# Skenario: premi risiko negara membaik (CDS 99,73 -> 75 bps; CDS & rupiah membaik)
# Setelah update, jalankan ulang query Q05 & Q08: skorStres turun ke 9, muncul
# DivergensiIntermarketBullish, dan Tesis_Keuangan_Kontrarian menjadi TesisTerpicu.
# ======================================================================
PREFIX ex:  <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
DELETE { ex:Pasar_ID_Okt2026 ex:cds5YBps ?c ; ex:trenCDS1Bulan ?t ; ex:trenRupiah1Bulan ?r . ex:Makro_CDS5Y ex:nilaiIndikator ?n . }
INSERT { ex:Pasar_ID_Okt2026 ex:cds5YBps "75.0"^^xsd:double ; ex:trenCDS1Bulan -1 ; ex:trenRupiah1Bulan -1 . ex:Makro_CDS5Y ex:nilaiIndikator "75.0"^^xsd:double . }
WHERE  { ex:Pasar_ID_Okt2026 ex:cds5YBps ?c ; ex:trenCDS1Bulan ?t ; ex:trenRupiah1Bulan ?r . ex:Makro_CDS5Y ex:nilaiIndikator ?n . }
