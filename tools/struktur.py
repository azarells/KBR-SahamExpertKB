import sys, html, json, subprocess, collections
sys.path.insert(0, 'lib')
import warnings; warnings.filterwarnings('ignore')
from owlready2 import *
w = World(); o = w.get_ontology('file:///home/claude/kbr/output/SahamExpertKB_v2.owl').load()
E = html.escape
lab = lambda x: (str(x.label[0]) if x.label else x.name)
com = lambda x: (str(x.comment[0]) if x.comment else '')
INF = set(o.KategoriInferensi.descendants())
def direct_inst(c): return [i for i in c.instances() if c in i.is_a]
rows = []
ALL = list(o.classes())
kids = collections.defaultdict(list)
for c in ALL:
    pars = [p for p in c.is_a if isinstance(p, ThingClass) and p in ALL]
    kids[pars[0] if pars else None].append(c)
def walk(c, d):
    for s in sorted(kids[c], key=lambda x: x.name):
        rows.append((d, s)); walk(s, d + 1)
walk(None, 0)
roots = [s for d, s in rows if d == 0]
H = []; a = H.append
a("<!doctype html><html lang='id'><head><meta charset='utf-8'><style>@page{size:A4;margin:14mm 13mm 16mm 13mm}body{font-family:'DejaVu Sans',Arial;font-size:8.6pt;color:#1d2433;line-height:1.4}"
  "h1{font-size:18pt;color:#0b3d6e;margin:0}h2{font-size:12.5pt;color:#fff;background:#0b3d6e;padding:5px 9px;margin:16px 0 6px;break-after:avoid}"
  "h3{font-size:10pt;color:#0b3d6e;margin:10px 0 3px;break-after:avoid}table{border-collapse:collapse;width:100%;font-size:7.8pt;margin:4px 0 8px}"
  "th{background:#174f86;color:#fff;padding:3px 5px;text-align:left}td{border-bottom:1px solid #d6dbe3;padding:2px 5px;vertical-align:top}tr{break-inside:avoid}"
  "code{background:#eef1f6;padding:0 3px;border-radius:3px;font-size:7.8pt}.inf{color:#a86b00}.box{border:2px solid #0b3d6e;padding:10px;margin-bottom:8px}"
  ".step{border-left:4px solid #e0a100;background:#f7f9fc;padding:5px 9px;margin:5px 0}</style></head><body>")
a("<div class='box'><h1>Struktur Ontologi SahamExpertKB v2</h1>Class · Subclass · Object Property · Data Property · Individu · Aturan SWRL — Kelompok 9 KBR<br>")
nC = len(rows); nOP = len(list(o.object_properties())); nDP = len(list(o.data_properties())); nI = len([i for i in o.individuals() if not isinstance(i, Imp)]); nR = len(list(o.rules()))
a(f"<b>{nC}</b> kelas · <b>{nOP}</b> object property · <b>{nDP}</b> data property · <b>{nI}</b> individu · <b>{nR}</b> aturan SWRL</div>")
a("<h2>Di mana melihatnya di Protégé</h2>")
for t, d in [("Class &amp; Subclass", "Tab <b>Entities</b> → sub-tab <b>Classes</b> → buka pohon <code>owl:Thing</code> (klik segitiga ▸). Subclass tampil menjorok di bawah induknya; panel kanan <b>Description</b> menampilkan <i>SubClass Of</i> dan <i>Disjoint With</i>. Bila tab Entities tidak ada: <b>Window → Tabs → Entities</b>."),
             ("Object Property", "Tab <b>Entities</b> → sub-tab <b>Object properties</b> → pilih properti → panel <i>Domains</i>, <i>Ranges</i>, <i>Characteristics</i> (Functional, Symmetric)."),
             ("Data Property", "Tab <b>Entities</b> → sub-tab <b>Data properties</b> → <i>Domains</i> &amp; <i>Ranges</i> (xsd:decimal, xsd:integer, xsd:string)."),
             ("Individu (instance)", "Tab <b>Individuals by class</b> → pilih kelas di kiri → individu di tengah → <i>Property assertions</i> di kanan."),
             ("Aturan SWRL", "<b>Window → Tabs → SWRLTab</b> (303 aturan), atau tab <b>Active ontology</b> → bagian <i>Rules</i>."),
             ("Label bahasa Indonesia", "<b>View → Render by label (rdfs:label)</b>; nama teknis kembali lewat <i>Render by entity IRI short name</i>.")]:
    a(f"<div class='step'><b>{t}:</b> {d}</div>")
a("<h2>1. Ringkasan Kelas Akar (anak langsung owl:Thing)</h2><table><tr><th>Kelas akar</th><th>Jumlah subclass (semua level)</th><th>Isi</th></tr>")
for r in roots:
    a(f"<tr><td><b>{r.name}</b></td><td>{len(list(r.descendants())) - 1}</td><td>{E(com(r))}</td></tr>")
a("</table>")
a("<h2>2. Hierarki Class &amp; Subclass Lengkap</h2><p>Indentasi = level subclass. <span class='inf'>Oranye</span> = kelas hasil inferensi SWRL (diisi reasoner). Kolom individu = jumlah instance langsung (sebelum reasoning).</p>")
a("<table><tr><th style='width:40%'>Kelas (subClassOf induk)</th><th>Label</th><th>Individu</th></tr>")
for d, c in rows:
    st = " class='inf'" if c in INF else ""
    a(f"<tr><td style='padding-left:{5 + d * 14}px'{st}>{'└ ' if d else ''}<b>{c.name}</b></td><td>{E(lab(c))}</td><td>{len(direct_inst(c)) or ''}</td></tr>")
a("</table>")
a("<h3>Kelas yang saling lepas (Disjoint)</h3><ul>")
for dj in o.disjoint_classes():
    a("<li>" + " ⟂ ".join(x.name for x in dj.entities) + "</li>")
a("</ul>")
a("<h2>3. Object Property</h2><table><tr><th>Properti</th><th>Domain</th><th>Range</th><th>Karakteristik</th><th>Keterangan</th></tr>")
for p in sorted(o.object_properties(), key=lambda x: x.name):
    ch = [n for n, k in [("Functional", FunctionalProperty), ("Symmetric", SymmetricProperty), ("Transitive", TransitiveProperty)] if k in p.is_a]
    if p.inverse_property: ch.append("inverse " + p.inverse_property.name)
    a(f"<tr><td><b>{p.name}</b></td><td>{', '.join(getattr(x,'name',str(x)) for x in p.domain)}</td><td>{', '.join(getattr(x,'name',str(x)) for x in p.range)}</td><td>{', '.join(ch)}</td><td>{E(com(p))}</td></tr>")
a("</table>")
a("<h2>4. Data Property</h2><table><tr><th>Properti</th><th>Domain</th><th>Tipe</th><th>Keterangan</th></tr>")
tn = {float: 'xsd:decimal', int: 'xsd:integer', str: 'xsd:string'}
for p in sorted(o.data_properties(), key=lambda x: x.name):
    rg = ', '.join(tn.get(x, getattr(x, '__name__', str(x))) for x in p.range)
    a(f"<tr><td><b>{p.name}</b></td><td>{', '.join(getattr(x,'name',str(x)) for x in p.domain)}</td><td>{rg}</td><td>{E(com(p) or lab(p))}</td></tr>")
a("</table>")
a("<h2>5. Jumlah Individu per Kelas (instance langsung)</h2><table><tr><th>Kelas</th><th>Jumlah</th><th>Contoh</th></tr>")
cnt = []
for d, c in rows:
    di = direct_inst(c)
    if di: cnt.append((c, di))
for c, di in sorted(cnt, key=lambda x: -len(x[1])):
    a(f"<tr><td>{c.name}</td><td>{len(di)}</td><td>{E(', '.join(i.name for i in di[:8]))}{' …' if len(di) > 8 else ''}</td></tr>")
a("</table>")
a("<h2>6. Aturan SWRL per Pilar</h2><table><tr><th>Pilar</th><th>Jumlah</th><th>Kode</th></tr>")
byp = collections.defaultdict(list)
for r in o.rules():
    pil = r.pilarAnalisis[0] if r.pilarAnalisis else '-'
    byp[pil].append(str(r.label[0]) if r.label else r.name)
for pil, codes in sorted(byp.items(), key=lambda x: -len(x[1])):
    a(f"<tr><td>{E(pil)}</td><td>{len(codes)}</td><td>{E(', '.join(sorted(codes)))}</td></tr>")
a("</table></body></html>")
open('/tmp/claude-0/struktur.html', 'w', encoding='utf-8').write('\n'.join(H))
print(nC, nOP, nDP, nI, nR, len(roots))
