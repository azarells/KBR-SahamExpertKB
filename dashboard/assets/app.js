// =====================================================================================
// SahamExpertKB · Dashboard Live — semua angka diambil dengan SPARQL dari Apache Jena Fuseki
// =====================================================================================
const API = location.protocol === 'file:' ? 'http://localhost:3030' : '/fuseki';
const PREFIX = `PREFIX ex: <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
`;
let SRC = 'saham-pellet';
const NUMERIC = /#(integer|int|decimal|double|float|long|short)$/;

async function sparql(q, ds = SRC) {
  const r = await fetch(`${API}/${ds}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/sparql-results+json' },
    body: 'query=' + encodeURIComponent(PREFIX + q)
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
  const j = await r.json();
  if (j.boolean !== undefined) return j.boolean;
  return j.results.bindings.map(b => {
    const o = {};
    for (const k in b) {
      const v = b[k];
      o[k] = v.type === 'uri' ? v.value.split('#').pop()
           : (v.datatype && NUMERIC.test(v.datatype)) ? Number(v.value) : v.value;
    }
    return o;
  });
}
async function update(u) {
  const r = await fetch(`${API}/saham/update`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'update=' + encodeURIComponent(PREFIX + u) });
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
}

// ----------------------------------------------------------------- util
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const fmt = (x, d = 2) => (x === undefined || x === null || x === '' || isNaN(x)) ? '–' : Math.abs(x) >= 1e8 ? '–' : Number(x).toLocaleString('id-ID', { maximumFractionDigits: d });
const nm = s => String(s).replace(/^(Sektor_|Ev_|Mv_|Tesis_|Persona_|Regime_|Skenario_|K_|Kasus_)/, '');
const SEKTOR = { BarangBaku: 'Barang Baku', Kesehatan: 'Kesehatan', Infrastruktur: 'Infrastruktur', KonsumenPrimer: 'Konsumen Primer', Perindustrian: 'Perindustrian', Energi: 'Energi', Keuangan: 'Keuangan', PropertiRealEstat: 'Properti', Teknologi: 'Teknologi', TransportasiLogistik: 'Transportasi', KonsumenNonPrimer: 'Konsumen Non-Primer' };
const sek = s => SEKTOR[nm(s)] || String(s).replace(/^Sektor (Barang )?/, '').replace(' & Real Estat', '').replace(' & Logistik', '');
const C = { m9: '#5c0a12', m8: '#7a0e17', m7: '#8b0d18', m6: '#a8131f', m5: '#c8202d', m4: '#e04a55', m3: '#f08a92', m2: '#f9cdd1', good: '#1d8a57', neu: '#9a8a8d', bad: '#c8202d' };
const PAL = ['#8b0d18', '#e04a55', '#f4a3aa', '#5c0a12', '#c8202d', '#f6c7cb', '#a8131f', '#d9737c', '#3d0a0f', '#ee8d95'];
const charts = {};
function chart(id, cfg) { if (charts[id]) charts[id].destroy(); const el = typeof id === 'string' ? $(id) : id; charts[id] = new Chart(el, cfg); return charts[id]; }
if (window.Chart) {
  Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
  Chart.defaults.color = '#4a3b3e';
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.tooltip.backgroundColor = '#2a0d11';
}
function clearLoading() { document.querySelectorAll('.loading').forEach(e => { if (e.children.length) e.classList.remove('loading'); }); }
new MutationObserver(clearLoading).observe(document.body, { childList: true, subtree: true });
function toggleQ(id) { $(id).classList.toggle('show'); }
function showQ(id, q) { $(id).textContent = q.trim(); }
function setErr(id, e) { $(id).innerHTML = `<div class="err">${esc(e.message || e)}</div>`; }
function badgeKelas(k) {
  const bad = /Risiko|Trap|Distribusi|Lemah|Turun|Hindari|Gugur|Distress|Overvalued|Mahal|Konflik|Bearish|Negatif|Underperform|Manipulasi|Gorengan|MarkDown|RedFlag|Korban/;
  const warn = /Tunggu|Momentum|Rapuh|Perlu|Abu|Indikatif|Overbought|Watchlist|Kedaluwarsa/;
  const good = /Kuat|Naik|Akumulasi|TopPick|Undervalued|Positif|Aman|Keyakinan|Konfirmasi|Menarik|Andalan|Entry|Outperform|MarkUp|Tinggi|Valid|Bullish|Cocok|Penerima|BuyOn/;
  const c = bad.test(k) ? 'b-bad' : warn.test(k) ? 'b-warn' : good.test(k) ? 'b-good' : 'b-neu';
  return `<span class="badge ${c}">${esc(k.replace(/([a-z])([A-Z])/g, '$1 $2'))}</span>`;
}
const ek = (kode, size = 24) => `<span class="ek">${logoEmiten(kode, size)}${esc(kode)}</span>`;
const ICON = {
  rate: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>',
  shield: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg>',
  down: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6l7 7 4-4 7 7"/><path d="M21 10v6h-6"/></svg>',
  fx: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 7h11l-3-3M17 17H6l3 3"/></svg>',
  gold: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 18h16l-3-7H7z"/><path d="M8 11l2-5h4l2 5"/></svg>',
  oil: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3s6 6.5 6 11a6 6 0 01-12 0c0-4.5 6-11 6-11z"/></svg>',
};

// =====================================================================================
// QUERY PANEL
// =====================================================================================
const NOU = 'FILTER NOT EXISTS { ?e a ex:EmitenUji }';
const Q = {
  ping: `SELECT (COUNT(*) AS ?triple) WHERE { ?s ?p ?o }`,
  pasar: `SELECT ?regime ?stres ?drawdown ?cds ?kurs ?biRate ?emas ?brent ?inflasi ?asing ?crash ?yield ?breadth
       ?pDD ?pCDS ?pAsing ?pKurs ?pYield ?pBreadth WHERE {
  ?k a ex:KondisiPasarAktif ; ex:regimeTerdeteksi ?r ; ex:skorStresPasar ?stres ;
     ex:drawdownIHSGPersen ?drawdown ; ex:cds5YBps ?cds ; ex:kursUSDIDR ?kurs ; ex:biRatePersen ?biRate ;
     ex:emasUSD ?emas ; ex:brentUSD ?brent ; ex:inflasiYoY ?inflasi ; ex:netAsingYTDT ?asing ; ex:penurunanHarianTerbesarPersen ?crash ;
     ex:yieldSBN10Y ?yield ; ex:breadthPersenDiAtasMA200 ?breadth ;
     ex:poinStresDrawdown ?pDD ; ex:poinStresCDS ?pCDS ; ex:poinStresAsing ?pAsing ; ex:poinStresKurs ?pKurs ; ex:poinStresYield ?pYield ; ex:poinStresBreadth ?pBreadth .
  ?r rdfs:label ?regime }`,
  hero: `SELECT (COUNT(DISTINCT ?i) AS ?inti) (COUNT(DISTINCT ?t) AS ?pick) (COUNT(DISTINCT ?b) AS ?biasa) WHERE {
  { ?i a ex:SektorPilihanInti } UNION { ?t a ex:KandidatTopPickAdaptif } UNION { ?b a ex:KandidatTopPick } }`,
  sektor: `SELECT ?s ?base ?bull ?bear ?ev ?aktif ?prediksi (GROUP_CONCAT(DISTINCT ?peranN; separator=",") AS ?peran) WHERE {
  ?s a ex:Sektor ; ex:skorOutlookBase ?base ; ex:skorOutlookBull ?bull ; ex:skorOutlookBear ?bear ;
     ex:skorEkspektasiProbabilistik ?ev ; ex:skorOutlookAktif ?aktif ; a ?k .
  FILTER(?k IN (ex:SektorBullishKuat, ex:SektorBullishModerat, ex:SektorNetral, ex:SektorBearish))
  BIND(STRAFTER(STR(?k), "Sektor") AS ?prediksi)
  OPTIONAL { ?s a ?p . FILTER(?p IN (ex:SektorPilihanInti, ex:SektorPilihanSatelit, ex:SektorPeluangKontrarian))
             BIND(STRAFTER(STR(?p), "Sektor") AS ?peranN) }
} GROUP BY ?s ?base ?bull ?bear ?ev ?aktif ?prediksi ORDER BY DESC(?ev)`,
  topSektor: `SELECT ?s ?kode ?adaptif ?pakar WHERE {
  { ?s a ex:SektorPilihanInti } UNION { ?s a ex:SektorPilihanSatelit }
  ?e ex:termasukSektor ?s ; ex:kodeSaham ?kode ; ex:skorAdaptifRegime ?adaptif . ${NOU}
  BIND(EXISTS { ?e a ex:KandidatTopPickAdaptif } AS ?pakar)
} ORDER BY ?s DESC(?adaptif)`,
  picks: `SELECT ?kode ?nama ?sektor ?statis ?adaptif ?posisi ?upside ?harga WHERE {
  ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode ; ex:termasukSektor ?sektor ; ex:skorTotalEmiten ?statis ; ex:skorAdaptifRegime ?adaptif .
  OPTIONAL { ?e ex:namaPerusahaan ?nama } OPTIONAL { ?e ex:ukuranPosisiMaksPersen ?posisi } OPTIONAL { ?e ex:potensiUpsidePersen ?upside } OPTIONAL { ?e ex:hargaPenutupan ?harga }
} ORDER BY DESC(?adaptif)`,
  pick: `SELECT ?kode ?statis ?adaptif ?biasa ?pakar WHERE {
  ?e ex:kodeSaham ?kode ; ex:skorTotalEmiten ?statis ; ex:skorAdaptifRegime ?adaptif .
  BIND(EXISTS { ?e a ex:KandidatTopPick } AS ?biasa)
  BIND(EXISTS { ?e a ex:KandidatTopPickAdaptif } AS ?pakar)
  FILTER(?biasa || ?pakar)
} ORDER BY DESC(?adaptif)`,
  rank: `SELECT ?kode ?nama ?sektor ?statis ?adaptif ?harga ?upside ?pakar ?biasa WHERE {
  ?e a ex:Emiten ; ex:kodeSaham ?kode ; ex:termasukSektor ?sektor ; ex:skorTotalEmiten ?statis ; ex:skorAdaptifRegime ?adaptif . ${NOU}
  OPTIONAL { ?e ex:namaPerusahaan ?nama } OPTIONAL { ?e ex:hargaPenutupan ?harga } OPTIONAL { ?e ex:potensiUpsidePersen ?upside }
  BIND(EXISTS { ?e a ex:KandidatTopPickAdaptif } AS ?pakar) BIND(EXISTS { ?e a ex:KandidatTopPick } AS ?biasa)
} ORDER BY DESC(?adaptif)`,
  ambang: `SELECT ?ambang WHERE { ?r a ex:RegimeAktif ; ex:ambangTopPickAdaptif ?ambang }`,
  daftarEmiten: `SELECT ?kode ?nama WHERE { ?e a ex:Emiten ; ex:kodeSaham ?kode . OPTIONAL { ?e ex:namaPerusahaan ?nama } ${NOU} } ORDER BY ?kode`,
  emiten: kode => `SELECT ?nama ?sektor ?harga ?F ?V ?T ?B ?S ?Sek ?R ?L ?total ?adaptif ?sl ?tp ?wajar ?upside ?posisi ?roe ?der ?per ?pbv ?rsi ?dy WHERE {
  ?e ex:kodeSaham "${kode}" ; ex:termasukSektor ?sektor ; ex:hargaPenutupan ?harga ;
     ex:skorFundamental ?F ; ex:skorValuasi ?V ; ex:skorTeknikal ?T ; ex:skorBandar ?B ; ex:skorSentimen ?S ;
     ex:skorKontribusiSektor ?Sek ; ex:penaltiRisiko ?R ; ex:poinLikuiditas ?L ; ex:skorTotalEmiten ?total ; ex:skorAdaptifRegime ?adaptif .
  OPTIONAL { ?e ex:namaPerusahaan ?nama } OPTIONAL { ?e ex:hargaStopLoss ?sl } OPTIONAL { ?e ex:hargaTakeProfit ?tp }
  OPTIONAL { ?e ex:nilaiWajar ?wajar } OPTIONAL { ?e ex:potensiUpsidePersen ?upside } OPTIONAL { ?e ex:ukuranPosisiMaksPersen ?posisi }
  OPTIONAL { ?e ex:roe ?roe } OPTIONAL { ?e ex:der ?der } OPTIONAL { ?e ex:per ?per } OPTIONAL { ?e ex:pbv ?pbv } OPTIONAL { ?e ex:rsi14 ?rsi } OPTIONAL { ?e ex:dividendYield ?dy }
} LIMIT 1`,
  kelasEmiten: kode => `SELECT DISTINCT ?kelas WHERE {
  ?e ex:kodeSaham "${kode}" ; a ?k . ?k rdfs:subClassOf* ex:KategoriInferensi .
  FILTER(?k NOT IN (ex:KategoriInferensi, ex:InferensiEmiten))
  BIND(STRAFTER(STR(?k), "#") AS ?kelas) } ORDER BY ?kelas`,
  tesis: `SELECT ?t ?label ?ind ?nilai ?bawah ?atas ?pemicu (GROUP_CONCAT(DISTINCT ?st; separator=",") AS ?status) WHERE {
  ?t a ex:TesisInvestasi ; rdfs:label ?label ; ex:indikatorKunciTesis ?i . ?i ex:nilaiIndikator ?nilai ; rdfs:label ?ind .
  OPTIONAL { ?t ex:ambangInvalidasiBawah ?bawah } OPTIONAL { ?t ex:ambangInvalidasiAtas ?atas } OPTIONAL { ?t ex:ambangPemicuBawah ?pemicu }
  OPTIONAL { ?t a ?k . FILTER(?k IN (ex:TesisGugur, ex:TesisRapuh, ex:TesisValid, ex:TesisTerpicu)) BIND(STRAFTER(STR(?k), "Tesis") AS ?st) }
} GROUP BY ?t ?label ?ind ?nilai ?bawah ?atas ?pemicu ORDER BY ?t`,
  risk: `SELECT ?jenis (COUNT(DISTINCT ?e) AS ?jumlah) (GROUP_CONCAT(DISTINCT ?kode; separator=",") AS ?kodes) WHERE {
  VALUES (?k ?jenis) { (ex:RisikoGoingConcern "Going concern") (ex:RisikoOutflowPasif "Outflow pasif") (ex:ValueTrap "Value trap")
    (ex:RisikoManipulasiLaba "Manipulasi laba") (ex:RedFlagBerita "Red flag berita") (ex:DistribusiBandar "Distribusi bandar") (ex:ZonaDistress "Zona distress Altman") (ex:SinyalHindari "Sinyal hindari") }
  ?e a ?k ; ex:kodeSaham ?kode . ${NOU} } GROUP BY ?jenis ORDER BY DESC(?jumlah)`,
  geo: `SELECT ?ev ?evL ?h1 ?h1L ?h2 ?h2L ?sektor WHERE {
  ?ev a ex:PeristiwaAktif ; rdfs:label ?evL ; ex:memicuPergerakan ?h1 . ?h1 rdfs:label ?h1L ; ex:menyebabkan ?h2 . ?h2 rdfs:label ?h2L ; ex:menguntungkanSektor ?sektor
} ORDER BY ?sektor ?ev`,
  katalis: `SELECT ?label ?hari ?tanggal (COUNT(DISTINCT ?e) AS ?emiten) WHERE {
  ?k a ex:Katalis ; rdfs:label ?label ; ex:hariMenujuKatalis ?hari ; ex:tanggalKatalis ?tanggal . FILTER(?hari >= 0)
  OPTIONAL { ?e ex:memilikiKatalisDekat ?k }
} GROUP BY ?label ?hari ?tanggal ORDER BY ?hari`,
  cbr: `SELECT ?periode ?kemiripan WHERE { ?c a ex:PeriodeHistoris ; rdfs:label ?periode ; ex:skorKemiripan ?kemiripan } ORDER BY DESC(?kemiripan)`,
};

// =====================================================================================
// PANEL
// =====================================================================================
async function ping() {
  try {
    const r = await sparql(Q.ping);
    $('dot').className = 'dot ok';
    $('conn').textContent = `Terhubung · ${r[0].triple.toLocaleString('id-ID')} triple`;
    return true;
  } catch (e) {
    $('dot').className = 'dot err'; $('conn').textContent = 'Fuseki tidak terhubung';
    $('regime').innerHTML = `<div class="lbl">Fuseki belum menyala</div><div class="nm" style="font-size:18px">Jalankan dulu dashboard/start_demo.sh</div>
      <div class="note">./dashboard/start_demo.sh ~/Downloads/apache-jena-fuseki-6.3.0 — tunggu sampai Fuseki siap, lalu muat ulang halaman ini.<br><br>${esc(e.message)}</div>`;
    return false;
  }
}

async function loadPasar() {
  try {
    const [p] = await sparql(Q.pasar);
    const [h] = await sparql(Q.hero);
    $('hstats').innerHTML = `
      <div><div class="v">${p.stres}/12</div><div class="l">skor stres pasar</div></div>
      <div><div class="v">${h.inti}</div><div class="l">sektor inti</div></div>
      <div><div class="v">${h.pick}</div><div class="l">top pick pakar</div></div>
      <div><div class="v">303</div><div class="l">aturan SWRL</div></div>`;
    const st = [['Drawdown IHSG', p.pDD], ['CDS 5Y', p.pCDS], ['Net asing', p.pAsing], ['Kurs USD/IDR', p.pKurs], ['Yield SBN', p.pYield], ['Breadth', p.pBreadth]];
    $('regime').innerHTML = `<div class="lbl">Regime pasar terdeteksi</div><div class="nm">${esc(p.regime)}</div>
      <div class="rc-grid"><div class="gauge-wrap"><canvas id="c-gauge" width="170" height="170"></canvas><div class="gv"><b>${p.stres}</b><span>dari 12</span></div></div>
      <div>${st.map(([n, v]) => `<div class="stress-row"><span>${n}</span><span class="t"><i style="width:${v / 2 * 100}%"></i></span><b>${v}</b></div>`).join('')}</div></div>
      <div class="note">Regime menentukan bobot semua pilar: saat krisis, fundamental, valuasi, risiko &amp; smart money ×1,5, teknikal &amp; sentimen ×0,5.</div>`;
    chart('c-gauge', { type: 'doughnut', data: { datasets: [{ data: [p.stres, 12 - p.stres], backgroundColor: ['#ffd0d4', 'rgba(255,255,255,.14)'], borderWidth: 0 }] },
      options: { cutout: '76%', rotation: -120, circumference: 240, plugins: { legend: { display: false }, tooltip: { enabled: false } }, responsive: false } });
    const k = (ic, l, v, n, tag) => `<div class="card kpi">${tag || ''}<span class="ic">${ICON[ic]}</span><span class="lbl">${l}</span><span class="val">${v}</span><span class="note">${n}</span></div>`;
    const tg = (txt, c) => `<span class="tag badge ${c}">${txt}</span>`;
    $('kpi').innerHTML =
      k('rate', 'BI-Rate', fmt(p.biRate) + '%', `inflasi ${fmt(p.inflasi)}% yoy`) +
      k('shield', 'CDS Indonesia 5Y', fmt(p.cds, 1), 'bps · premi risiko negara', p.cds >= 90 ? tg('tinggi', 'b-bad') : '') +
      k('down', 'Drawdown IHSG', fmt(p.drawdown, 1) + '%', `crash harian terbesar ${fmt(p.crash)}%`, p.drawdown <= -40 ? tg('kapitulasi', 'b-bad') : tg('belum kapitulasi', 'b-warn')) +
      k('fx', 'USD/IDR', fmt(p.kurs, 0), `net asing YTD ${fmt(p.asing)} T`, tg('stres', 'b-bad')) +
      k('gold', 'Emas', 'US$' + fmt(p.emas, 0), 'per troy ounce', p.emas < 3800 ? tg('tesis gugur', 'b-bad') : '') +
      k('oil', 'Brent', 'US$' + fmt(p.brent), 'per barel', p.brent >= 75 ? tg('tesis valid', 'b-good') : tg('tesis gugur', 'b-bad'));
    $('c-cds').value = p.cds; $('c-emas').value = p.emas; $('c-brent').value = p.brent; $('c-dd').value = p.drawdown; $('c-crash').value = p.crash;
  } catch (e) { setErr('hstats', e); }
}

async function loadSektor() {
  showQ('q-sektor', Q.sektor);
  try {
    const rows = await sparql(Q.sektor);
    const top = await sparql(Q.topSektor);
    const tops = {}; top.forEach(r => (tops[r.s] = tops[r.s] || []).push(r));
    // kartu sektor inti & satelit
    const pilihan = rows.filter(r => /PilihanInti|PilihanSatelit/.test(r.peran || ''));
    $('sk-cards').innerHTML = pilihan.map(r => {
      const inti = /PilihanInti/.test(r.peran);
      return `<div class="skc ${inti ? 'inti' : ''}"><div class="role">${inti ? '★ Sektor inti' : 'Sektor satelit'}</div><div class="nm">${esc(sek(r.s))}</div>
        <div class="row3"><div><b>${fmt(r.aktif)}</b>skor base</div><div><b>${fmt(r.ev)}</b>ekspektasi</div><div><b>${fmt(r.bear)} → ${fmt(r.bull)}</b>bear → bull</div></div>
        <div style="margin-top:10px;display:flex;gap:6px;flex-wrap:wrap">${(tops[r.s] || []).slice(0, 3).map(t => `<span class="badge ${t.pakar === 'true' ? 'b-good' : 'b-neu'}" style="cursor:pointer" onclick="pilihEmiten('${t.kode}')">${logoEmiten(t.kode, 16)} ${t.pakar === 'true' ? '★ ' : ''}${t.kode} ${fmt(t.adaptif, 1)}</span>`).join('')}</div></div>`;
    }).join('');
    // dumbbell
    const lo = Math.min(...rows.map(r => r.bear), 0) - 2, hi = Math.max(...rows.map(r => r.bull), 0) + 2;
    const W = 700, L = 172, R = 160, rowH = 34, top0 = 30, H = top0 + rows.length * rowH + 28;
    const X = v => L + (v - lo) / (hi - lo) * (W - L - R);
    const warna = { BullishKuat: C.good, BullishModerat: '#36a370', Netral: C.neu, Bearish: C.bad };
    let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Skor sektor per skenario">`;
    for (let v = Math.ceil(lo / 5) * 5; v <= hi; v += 5) {
      s += `<line x1="${X(v)}" x2="${X(v)}" y1="${top0 - 8}" y2="${H - 24}" stroke="${v === 0 ? '#c9a9ad' : '#f4e7e9'}" stroke-width="${v === 0 ? 1.5 : 1}"/>`;
      s += `<text x="${X(v)}" y="${H - 8}" text-anchor="middle" font-size="11" fill="#7c6b6e">${v}</text>`;
    }
    s += `<text x="${L}" y="14" font-size="11" fill="#7c6b6e">← lebih buruk</text><text x="${W - R}" y="14" text-anchor="end" font-size="11" fill="#7c6b6e">lebih baik →</text>`;
    rows.forEach((r, i) => {
      const y = top0 + i * rowH + rowH / 2, c = warna[r.prediksi] || C.neu;
      const peran = (r.peran || '').split(',').filter(Boolean).map(p => p.replace('Pilihan', '').replace('Peluang', '')).join(' · ');
      if (i % 2 === 0) s += `<rect x="0" y="${y - rowH / 2}" width="${W}" height="${rowH}" fill="#fff8f9"/>`;
      s += `<text x="${L - 12}" y="${y + 4}" text-anchor="end" font-size="13" fill="#1f1416" font-weight="${peran.includes('Inti') ? 800 : 500}">${esc(sek(r.s))}</text>`;
      s += `<line x1="${X(r.bear)}" x2="${X(r.bull)}" y1="${y}" y2="${y}" stroke="${c}" stroke-width="6" stroke-opacity=".22" stroke-linecap="round"/>`;
      s += `<circle cx="${X(r.bear)}" cy="${y}" r="3.5" fill="#fff" stroke="${c}" stroke-width="1.5"/><circle cx="${X(r.bull)}" cy="${y}" r="3.5" fill="#fff" stroke="${c}" stroke-width="1.5"/>`;
      s += `<circle cx="${X(r.aktif)}" cy="${y}" r="7" fill="${c}"><title>Skenario aktif: ${r.aktif}</title></circle>`;
      s += `<path d="M${X(r.ev)} ${y - 7} l7 7 l-7 7 l-7 -7z" fill="#fff" stroke="#2a0d11" stroke-width="1.4"><title>Ekspektasi: ${fmt(r.ev)}</title></path>`;
      s += `<text x="${W - R + 14}" y="${y + (peran ? 0 : 4)}" font-size="12" fill="${c}" font-weight="800">${r.prediksi.replace('Bullish', 'Bullish ')}</text>`;
      if (peran) s += `<text x="${W - R + 14}" y="${y + 13}" font-size="10.5" fill="#7c6b6e">${esc(peran)}</text>`;
    });
    $('chart-sektor').innerHTML = s + `</svg>`;
    // heatmap
    const cell = v => { const a = Math.min(Math.abs(v) / 18, 1); const bg = v >= 7 ? `rgba(29,138,87,${.25 + a * .6})` : v >= 2 ? `rgba(154,138,141,${.15 + a * .3})` : `rgba(200,32,45,${.2 + a * .6})`; return `<td style="background:${bg};color:${a > .55 ? '#fff' : '#1f1416'}">${fmt(v)}</td>`; };
    $('heat').innerHTML = `<table class="heat"><tr><th>Sektor</th><th style="text-align:center">Bear 25%</th><th style="text-align:center">Base 50%</th><th style="text-align:center">Bull 25%</th></tr>` +
      rows.map(r => `<tr><td>${esc(sek(r.s))}</td>${cell(r.bear)}${cell(r.base)}${cell(r.bull)}</tr>`).join('') + `</table>`;
    chart('c-ev', { type: 'bar', data: { labels: rows.map(r => sek(r.s)), datasets: [{ data: rows.map(r => r.ev), backgroundColor: rows.map(r => r.ev >= 7 ? C.m7 : r.ev >= 2 ? C.m3 : '#c9bcbe'), borderRadius: 6 }] },
      options: { indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { grid: { color: '#f4e7e9' } }, y: { grid: { display: false } } } } });
  } catch (e) { setErr('chart-sektor', e); }
}

async function loadPicks() {
  showQ('q-pick', Q.pick); showQ('q-rank', Q.rank);
  try {
    const [p, pick, rank, amb] = await Promise.all([sparql(Q.picks), sparql(Q.pick), sparql(Q.rank), sparql(Q.ambang)]);
    const mx = Math.max(...p.map(r => r.adaptif), 1);
    $('picks').innerHTML = p.map(r => `<div class="pc" onclick="pilihEmiten('${r.kode}')">
      <div class="top">${logoEmiten(r.kode, 44)}<div><div class="kd">${esc(r.kode)}</div><div class="nmx">${esc(r.nama || (EMITEN_INFO[r.kode] || {}).nama || '')}</div></div></div>
      <div class="sc"><div><span class="small muted">skor adaptif</span><br><b>${fmt(r.adaptif, 1)}</b></div><span class="badge b-acc">${esc(sek(r.sektor))}</span></div>
      <div class="bar"><i style="width:${r.adaptif / mx * 100}%"></i></div>
      <div class="meta"><span>statis ${fmt(r.statis)}</span><span>upside ${r.upside !== undefined ? fmt(r.upside, 0) + '%' : '–'}</span><span>posisi ≤ ${fmt(r.posisi, 1)}%</span></div></div>`).join('');
    chart('c-pick', { type: 'bar', data: { labels: pick.map(r => r.kode), datasets: [
        { label: 'Skor statis (analis biasa)', data: pick.map(r => r.statis), backgroundColor: '#e7c9cc', borderRadius: 6 },
        { label: 'Skor adaptif (sistem pakar)', data: pick.map(r => r.adaptif), backgroundColor: C.m7, borderRadius: 6 }] },
      options: { plugins: { legend: { position: 'bottom' } }, scales: { x: { grid: { display: false } }, y: { grid: { color: '#f4e7e9' }, beginAtZero: true } } } });
    const tambah = pick.filter(r => r.pakar === 'true' && r.biasa !== 'true').map(r => r.kode);
    $('pick-note').innerHTML = `Analis biasa memilih <b>${pick.filter(r => r.biasa === 'true').length}</b> emiten, sistem pakar <b>${pick.filter(r => r.pakar === 'true').length}</b>. Tambahan dari sistem pakar: ${tambah.map(k => ek(k, 18)).join(' ') || '–'}`;
    const ambang = amb[0] ? amb[0].ambang : 24.7;
    const lineAmbang = { id: 'ambang', afterDraw(c) { const y = c.scales.y.getPixelForValue(ambang), a = c.chartArea; const g = c.ctx; g.save(); g.setLineDash([5, 4]); g.strokeStyle = C.m5; g.beginPath(); g.moveTo(a.left, y); g.lineTo(a.right, y); g.stroke(); g.fillStyle = C.m5; g.font = '11px sans-serif'; g.fillText(`ambang regime ${fmt(ambang)}`, a.left + 6, y - 5); g.restore(); } };
    chart('c-scatter', { type: 'scatter', data: { datasets: [
        { label: 'Top pick pakar', data: rank.filter(r => r.pakar === 'true').map(r => ({ x: r.statis, y: r.adaptif, k: r.kode })), backgroundColor: C.m7, pointRadius: 7 },
        { label: 'Emiten lain', data: rank.filter(r => r.pakar !== 'true').map(r => ({ x: r.statis, y: r.adaptif, k: r.kode })), backgroundColor: 'rgba(224,74,85,.35)', pointRadius: 5 }] },
      options: { plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { label: c => `${c.raw.k}: statis ${c.raw.x}, adaptif ${c.raw.y}` } } },
        scales: { x: { title: { display: true, text: 'skor statis' }, grid: { color: '#f4e7e9' } }, y: { title: { display: true, text: 'skor adaptif' }, grid: { color: '#f4e7e9' } } } },
      plugins: [lineAmbang, pointLabels(r => r.pakar)] });
    RANK = rank; renderRankFilter(); renderRank();
  } catch (e) { setErr('picks', e); }
}
function pointLabels() {
  return { id: 'plab', afterDatasetsDraw(c) { const g = c.ctx; g.save(); g.font = '600 10.5px sans-serif'; g.fillStyle = '#2a0d11';
    c.data.datasets.forEach((ds, i) => { if (i !== 0 && c.data.datasets.length > 1 && ds.data.length > 25) return;
      c.getDatasetMeta(i).data.forEach((pt, j) => { const k = ds.data[j].k; if (k) g.fillText(k, pt.x + 8, pt.y + 3); }); }); g.restore(); } };
}
let RANK = [], RANK_F = 'Semua';
function renderRankFilter() {
  const s = ['Semua', ...new Set(RANK.map(r => sek(r.sektor)))];
  $('rank-filter').innerHTML = s.map(x => `<button class="${x === RANK_F ? 'on' : ''}" onclick="RANK_F='${x}';renderRankFilter();renderRank()">${x}</button>`).join('');
}
function renderRank() {
  const rows = RANK.filter(r => RANK_F === 'Semua' || sek(r.sektor) === RANK_F);
  const mx = Math.max(...RANK.map(r => r.adaptif), 1);
  $('rank').innerHTML = `<table><thead><tr><th>#</th><th>Emiten</th><th>Sektor</th><th class="num">Harga</th><th class="num">Statis</th><th style="width:28%">Skor adaptif</th><th class="num">Upside</th><th>Status</th></tr></thead><tbody>` +
    rows.map((r, i) => `<tr style="cursor:pointer" onclick="pilihEmiten('${r.kode}')"><td class="muted">${i + 1}</td><td>${ek(r.kode, 26)}<div class="small muted" style="margin-left:34px;margin-top:-4px">${esc(r.nama || '')}</div></td>
      <td>${esc(sek(r.sektor))}</td><td class="num">${fmt(r.harga, 0)}</td><td class="num">${fmt(r.statis)}</td>
      <td><div style="display:flex;align-items:center;gap:8px"><div class="bar" style="flex:1;margin:0"><i style="width:${Math.max(r.adaptif, 0) / mx * 100}%"></i></div><b>${fmt(r.adaptif, 1)}</b></div></td>
      <td class="num">${r.upside !== undefined ? fmt(r.upside, 0) + '%' : '–'}</td>
      <td>${r.pakar === 'true' ? '<span class="badge b-good">★ top pick</span>' : r.biasa === 'true' ? '<span class="badge b-acc">analis biasa</span>' : '<span class="badge b-neu">pantau</span>'}</td></tr>`).join('') + `</tbody></table>`;
}

async function loadDaftarEmiten() {
  const rows = await sparql(Q.daftarEmiten);
  const cur = $('sel-emiten').value || 'ANTM';
  $('sel-emiten').innerHTML = rows.map(r => `<option value="${r.kode}">${r.kode} — ${esc(r.nama || '')}</option>`).join('');
  $('sel-emiten').value = cur;
}
function pilihEmiten(k) { $('sel-emiten').value = k; loadEmiten(); $('bedah').scrollIntoView({ behavior: 'smooth' }); }

async function loadEmiten() {
  const kode = $('sel-emiten').value || 'ANTM';
  showQ('q-emiten', Q.emiten(kode) + '\n\n' + Q.kelasEmiten(kode));
  try {
    const [d] = await sparql(Q.emiten(kode));
    const kelas = (await sparql(Q.kelasEmiten(kode))).map(r => r.kelas);
    if (!d) { $('bd-out').innerHTML = '<p class="muted">Data skor tidak lengkap untuk emiten ini.</p>'; return; }
    const komp = [['Fundamental', d.F], ['Valuasi', d.V], ['Teknikal', d.T], ['Bandarmology', d.B], ['Sentimen', d.S], ['Kontribusi sektor', d.Sek], ['Penalti risiko', d.R], ['Likuiditas', d.L]];
    const top = kelas.includes('KandidatTopPickAdaptif');
    // level harga
    const lv = [['Stop loss', d.sl, C.bad], ['Harga', d.harga, '#2a0d11'], ['Take profit', d.tp, C.good], ['Nilai wajar', d.wajar, C.m7]].filter(x => x[1] !== undefined);
    const vmin = Math.min(...lv.map(x => x[1])) * 0.97, vmax = Math.max(...lv.map(x => x[1])) * 1.03;
    const pos = v => 4 + (v - vmin) / (vmax - vmin) * 92;
    $('bd-out').innerHTML = `
      <div class="bd-head">${logoEmiten(kode, 64)}<div style="flex:1"><div class="kd">${esc(kode)}</div><div class="muted">${esc(d.nama || '')} · ${esc(sek(d.sektor))}</div></div>
        <div style="text-align:right"><span class="badge b-neu">statis ${fmt(d.total, 1)}</span><span class="badge b-acc">adaptif ${fmt(d.adaptif, 1)}</span><br>
        ${top ? '<span class="badge b-good" style="margin-top:6px">★ Top pick sistem pakar</span>' : '<span class="badge b-warn" style="margin-top:6px">Belum lolos ambang top pick</span>'}</div></div>
      <div class="mini-kpi">${[['ROE', d.roe, '%'], ['DER', d.der, 'x'], ['PER', d.per, 'x'], ['PBV', d.pbv, 'x'], ['RSI 14', d.rsi, ''], ['Dividend yield', d.dy, '%']].map(([n, v, u]) => `<div><span>${n}</span><b>${fmt(v, 1)}${v !== undefined ? u : ''}</b></div>`).join('')}</div>
      <div class="grid g2e" style="gap:18px">
        <div><h3 style="font-size:14px">Kontribusi delapan pilar</h3><canvas id="c-pilar" height="240"></canvas></div>
        <div><h3 style="font-size:14px">Profil radar</h3><canvas id="c-radar" height="240"></canvas></div>
      </div>
      <h3 style="font-size:14px;margin-top:14px">Level harga dari manajemen risiko ${d.upside !== undefined ? `<span class="badge b-good">upside ke nilai wajar ${fmt(d.upside, 0)}%</span>` : ''} ${d.posisi !== undefined ? `<span class="badge b-acc">posisi maks ${fmt(d.posisi, 1)}% modal</span>` : ''}</h3>
      <div class="ladder"><div class="ln"></div>${lv.map(([n, v, c]) => `<div class="mk" style="left:${pos(v)}%;color:${c}"><b>${fmt(v, 0)}</b><i style="background:${c}"></i><span>${n}</span></div>`).join('')}</div>
      <p class="small muted" style="margin:2px 0 12px">Stop loss = harga − 2×ATR · take profit = harga + 3×ATR · posisi maks = risiko per transaksi regime ÷ (2×ATR%).</p>
      <h3 style="font-size:14px">Kelas yang disimpulkan reasoner (${kelas.length})</h3>
      <div class="chips">${kelas.map(badgeKelas).join('')}</div>`;
    chart('c-pilar', { type: 'bar', data: { labels: komp.map(x => x[0]), datasets: [{ data: komp.map(x => x[1]), backgroundColor: komp.map(x => x[1] > 0 ? C.m7 : x[1] < 0 ? '#8d98a6' : '#e8dcdd'), borderRadius: 6 }] },
      options: { indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { grid: { color: '#f4e7e9' } }, y: { grid: { display: false } } } } });
    chart('c-radar', { type: 'radar', data: { labels: komp.map(x => x[0]), datasets: [{ label: kode, data: komp.map(x => x[1]), backgroundColor: 'rgba(200,32,45,.18)', borderColor: C.m6, pointBackgroundColor: C.m7 }] },
      options: { plugins: { legend: { display: false } }, scales: { r: { grid: { color: '#f0dfe1' }, angleLines: { color: '#f0dfe1' }, ticks: { backdropColor: 'transparent', font: { size: 9 } } } } } });
  } catch (e) { setErr('bd-out', e); }
}

async function loadTesis() {
  showQ('q-tesis', Q.tesis);
  try {
    const rows = await sparql(Q.tesis);
    $('tesis').innerHTML = rows.map(r => {
      const st = (r.status || '').split(',').filter(Boolean);
      const utama = st.includes('Gugur') ? 'Gugur' : st.includes('Terpicu') ? 'Terpicu' : st.includes('Rapuh') ? 'Rapuh' : 'Valid';
      const cls = { Gugur: 'b-bad', Rapuh: 'b-warn', Valid: 'b-good', Terpicu: 'b-acc' }[utama];
      const lo = r.bawah > 0 ? r.bawah : null, hi = r.atas !== undefined && r.atas < 1e8 ? r.atas : null;
      const ref = [r.nilai, lo, hi, r.pemicu].filter(x => x !== null && x !== undefined);
      const a = Math.min(...ref) * 0.85, b = Math.max(...ref) * 1.15, P = v => (v - a) / (b - a) * 100;
      return `<div class="ts"><div class="h"><b>${esc(r.label.replace(/^Tesis( kontrarian)?:\s*/, ''))}</b><span class="badge ${cls}">${utama}${st.length > 1 ? ' · ' + st.filter(x => x !== utama).join(', ') : ''}</span></div>
        <div class="track">${lo !== null ? `<span class="lim" style="left:${P(lo)}%" title="batas bawah"></span>` : ''}${hi !== null ? `<span class="lim" style="left:${P(hi)}%" title="batas atas"></span>` : ''}
        ${r.pemicu ? `<span class="lim" style="left:${P(r.pemicu)}%;background:${C.good}" title="pemicu kontrarian"></span>` : ''}<span class="cur" style="left:${P(r.nilai)}%"></span></div>
        <div class="lg"><span>${esc(r.ind)}: <b style="color:#1f1416">${fmt(r.nilai)}</b></span><span>${lo !== null ? 'gugur bila &lt; ' + fmt(lo) : ''}${hi !== null ? 'gugur bila &gt; ' + fmt(hi) : ''}${r.pemicu ? ' · terpicu bila &lt; ' + fmt(r.pemicu) : ''}</span></div></div>`;
    }).join('');
    const rk = await sparql(Q.risk);
    chart('c-risk', { type: 'bar', data: { labels: rk.map(r => r.jenis), datasets: [{ data: rk.map(r => r.jumlah), backgroundColor: PAL, borderRadius: 6 }] },
      options: { indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { grid: { color: '#f4e7e9' }, ticks: { precision: 0 } }, y: { grid: { display: false } } } } });
    $('risk-list').innerHTML = rk.slice(0, 4).map(r => `<div style="margin:6px 0"><span class="small muted" style="display:inline-block;width:130px;font-weight:700">${esc(r.jenis)}</span>${r.kodes.split(',').slice(0, 8).map(k => `<span style="cursor:pointer;margin-right:6px" onclick="pilihEmiten('${k}')">${ek(k, 18)}</span>`).join('')}</div>`).join('');
  } catch (e) { setErr('tesis', e); }
}

async function loadGeo() {
  showQ('q-geo', Q.geo); showQ('q-kat', Q.katalis);
  try {
    const rows = await sparql(Q.geo);
    const uniq = k => [...new Map(rows.map(r => [r[k], r])).values()];
    const col = (t, items, cls = '') => `<div class="col"><h4>${t}</h4>${items.map(x => `<div class="node ${cls}">${esc(x)}</div>`).join('')}</div>`;
    const ev = uniq('ev').slice(0, 7), h1 = uniq('h1').slice(0, 7), h2 = uniq('h2').slice(0, 7), sk = uniq('sektor');
    $('geo-flow').innerHTML = `<div class="flow">${col('Peristiwa aktif', ev.map(r => r.evL))}${col('Gerakan pasar', h1.map(r => r.h1L))}${col('Gerakan lanjutan', h2.map(r => r.h2L))}${col('Sektor diuntungkan', sk.map(r => sek(r.sektor)), 'sk')}</div>
      <p class="small muted" style="margin:8px 0 0">${rows.length} jalur sebab-akibat tiga langkah ditemukan reasoner. Contoh: <b>${esc(rows[0] ? rows[0].evL : '')}</b> → ${esc(rows[0] ? rows[0].h1L : '')} → ${esc(rows[0] ? rows[0].h2L : '')} → <b>${esc(rows[0] ? sek(rows[0].sektor) : '')}</b>.</p>`;
    const k = await sparql(Q.katalis);
    const mx = Math.max(...k.map(r => r.hari), 30);
    $('kat').innerHTML = `<div class="timeline"><div class="axis"></div>${k.map((r, i) => `<span class="ev" style="left:${3 + r.hari / mx * 94}%" title="${esc(r.label)}">${i + 1}</span>`).join('')}</div>
      <div class="kat-list">${k.map((r, i) => `<div><b>${i + 1}.</b> ${esc(r.label)} · <b>${r.hari} hari</b>${r.emiten ? ` · ${r.emiten} emiten` : ''}</div>`).join('')}</div>`;
    const c = await sparql(Q.cbr);
    chart('c-cbr', { type: 'bar', data: { labels: c.map(r => r.periode.length > 30 ? r.periode.slice(0, 29) + '…' : r.periode), datasets: [{ data: c.map(r => r.kemiripan), backgroundColor: c.map(r => r.kemiripan >= 13 ? C.m7 : '#e7c9cc'), borderRadius: 6 }] },
      options: { indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { max: 20, grid: { color: '#f4e7e9' } }, y: { grid: { display: false }, ticks: { font: { size: 10.5 } } } } } });
  } catch (e) { setErr('geo-flow', e); }
}

async function refreshAll() {
  if (!(await ping())) return;
  await Promise.all([loadPasar(), loadSektor(), loadPicks(), loadTesis(), loadGeo(), loadDaftarEmiten().then(loadEmiten)]);
}
function setSource(ds) {
  SRC = ds;
  $('src-pellet').classList.toggle('on', ds === 'saham-pellet');
  $('src-jena').classList.toggle('on', ds === 'saham');
  refreshAll();
  if (QA_CUR !== null) runQA(QA_CUR);
}

// =====================================================================================
// WHAT-IF (SPARQL UPDATE ke /saham)
// =====================================================================================
const D = (s, p, v) => ({ s, p, v, t: 'double' }), I = (s, p, v) => ({ s, p, v, t: 'integer' });
const skenario = k => [I('Skenario_Base_2027_2028', 'statusAktif', k === 'base' ? 1 : 0), I('Skenario_Bull_Pemulihan', 'statusAktif', k === 'bull' ? 1 : 0), I('Skenario_Bear_Stagflasi', 'statusAktif', k === 'bear' ? 1 : 0)];
const PRESET = {
  bull: () => skenario('bull'), bear: () => skenario('bear'),
  cds: () => [D('Pasar_ID_Okt2026', 'cds5YBps', 75), I('Pasar_ID_Okt2026', 'trenCDS1Bulan', -1), I('Pasar_ID_Okt2026', 'trenRupiah1Bulan', -1), D('Makro_CDS5Y', 'nilaiIndikator', 75)],
  emas: () => [D('Pasar_ID_Okt2026', 'emasUSD', 4000), D('Makro_Emas', 'nilaiIndikator', 4000)],
  brent: () => [D('Pasar_ID_Okt2026', 'brentUSD', 70), D('Makro_Brent', 'nilaiIndikator', 70)],
  kapitulasi: () => [D('Pasar_ID_Okt2026', 'drawdownIHSGPersen', -45), D('Pasar_ID_Okt2026', 'penurunanHarianTerbesarPersen', -10.5)],
  custom: () => [D('Pasar_ID_Okt2026', 'cds5YBps', +$('c-cds').value), D('Makro_CDS5Y', 'nilaiIndikator', +$('c-cds').value),
    D('Pasar_ID_Okt2026', 'emasUSD', +$('c-emas').value), D('Makro_Emas', 'nilaiIndikator', +$('c-emas').value),
    D('Pasar_ID_Okt2026', 'brentUSD', +$('c-brent').value), D('Makro_Brent', 'nilaiIndikator', +$('c-brent').value),
    D('Pasar_ID_Okt2026', 'drawdownIHSGPersen', +$('c-dd').value), D('Pasar_ID_Okt2026', 'penurunanHarianTerbesarPersen', +$('c-crash').value), ...skenario($('c-sk').value)],
};
const DIUBAH = [['Pasar_ID_Okt2026', ['cds5YBps', 'trenCDS1Bulan', 'trenRupiah1Bulan', 'emasUSD', 'brentUSD', 'drawdownIHSGPersen', 'penurunanHarianTerbesarPersen']],
  ['Makro_CDS5Y', ['nilaiIndikator']], ['Makro_Emas', ['nilaiIndikator']], ['Makro_Brent', ['nilaiIndikator']],
  ['Skenario_Base_2027_2028', ['statusAktif']], ['Skenario_Bull_Pemulihan', ['statusAktif']], ['Skenario_Bear_Stagflasi', ['statusAktif']]];
function buatUpdate(list) { return list.map(x => `DELETE WHERE { ex:${x.s} ex:${x.p} ?lama } ;\nINSERT DATA { ex:${x.s} ex:${x.p} "${x.v}"^^xsd:${x.t} }`).join(' ;\n'); }
async function bacaNilai(ds) {
  const pasangan = DIUBAH.flatMap(([s, ps]) => ps.map(p => `(ex:${s} ex:${p})`)).join(' ');
  const r = await sparql(`SELECT ?s ?p ?v (DATATYPE(?v) AS ?dt) WHERE { VALUES (?s ?p) { ${pasangan} } ?s ?p ?v }`, ds);
  return r.map(x => ({ s: x.s, p: x.p, v: x.v, t: /integer|int$/.test(x.dt) ? 'integer' : 'double' }));
}
async function hanyaYangBerubah(list) {
  const kini = {}; (await bacaNilai('saham')).forEach(x => kini[x.s + ' ' + x.p] = Number(x.v));
  return list.filter(x => kini[x.s + ' ' + x.p] !== Number(x.v));
}
async function snapshot() {
  const ds = 'saham';
  const [pr, naikR, intiR, pickR, tesR, akumR, kap] = await Promise.all([
    sparql(`SELECT ?stres ?r WHERE { ex:Pasar_ID_Okt2026 ex:skorStresPasar ?stres ; ex:regimeTerdeteksi ?r }`, ds),
    sparql(`SELECT ?s WHERE { ?s a ex:SektorBullish } ORDER BY ?s`, ds),
    sparql(`SELECT ?s WHERE { ?s a ex:SektorPilihanInti } ORDER BY ?s`, ds),
    sparql(`SELECT ?k WHERE { ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?k } ORDER BY ?k`, ds),
    sparql(`SELECT ?t ?x WHERE { ?t a ex:TesisInvestasi ; a ?k . FILTER(?k IN (ex:TesisGugur, ex:TesisTerpicu, ex:TesisRapuh, ex:TesisValid)) BIND(STRAFTER(STR(?k),"Tesis") AS ?x) } ORDER BY ?t ?x`, ds),
    sparql(`SELECT ?k WHERE { ?e a ex:KandidatAkumulasiBertahap ; ex:kodeSaham ?k } ORDER BY ?k`, ds),
    sparql(`ASK { ?k a ex:KapitulasiPasar }`, ds)]);
  const p = pr[0], tes = {};
  tesR.forEach(r => (tes[nm(r.t)] = tes[nm(r.t)] || []).push(r.x));
  return { 'Regime': nm(p.r), 'Skor stres': `${p.stres}/12`,
    'Sektor naik (bullish)': naikR.map(r => sek(r.s)).join(', ') || '–', 'Sektor inti': intiR.map(r => sek(r.s)).join(', ') || '–',
    'Top pick pakar': pickR.map(r => r.k).join(', ') || '–', 'Kapitulasi pasar': kap ? 'ya' : 'tidak',
    'Kandidat akumulasi bertahap': akumR.map(r => r.k).join(', ') || '–',
    'Status tesis': Object.entries(tes).map(([t, st]) => `${t}: ${st.sort().join('/')}`).join(' · ') };
}
const kodeList = s => s.split(', ').map(k => /^[A-Z]{4}$/.test(k) ? ek(k, 18) : esc(k)).join(' ');
async function whatif(kind) {
  const btns = document.querySelectorAll('#whatif button');
  btns.forEach(b => b.disabled = true);
  $('whatif-out').innerHTML = '<p class="loading">Mengirim SPARQL UPDATE dan menunggu aturan menalar ulang…</p>';
  try {
    const sebelum = await snapshot();
    const list = await hanyaYangBerubah(kind === 'reset' ? await bacaNilai('saham-pellet') : PRESET[kind]());
    if (!list.length) { $('whatif-out').innerHTML = '<div class="diff">Tidak ada nilai yang berubah: data di /saham sudah sama dengan permintaan ini.</div>'; if (kind === 'reset') setSource('saham-pellet'); btns.forEach(b => b.disabled = false); return; }
    const u = buatUpdate(list);
    $('q-whatif').classList.add('show'); $('q-whatif').textContent = '# SPARQL UPDATE yang dikirim ke /saham/update\n' + u;
    const t0 = performance.now(); await update(u); const ms = Math.round(performance.now() - t0);
    const sesudah = await snapshot();
    const kodeKey = /Top pick|akumulasi/;
    const baris = Object.keys(sebelum).map(k => {
      const beda = sebelum[k] !== sesudah[k], f = kodeKey.test(k) ? kodeList : esc;
      return `<tr><td><b>${k}</b></td><td class="small">${f(sebelum[k])}</td><td class="small ${beda ? 'chg' : ''}">${f(sesudah[k])}${beda ? ' ◀' : ''}</td></tr>`;
    }).join('');
    const nBeda = Object.keys(sebelum).filter(k => sebelum[k] !== sesudah[k]).length;
    $('whatif-out').innerHTML = `<div class="diff"><b>${kind === 'reset' ? 'Data dikembalikan ke nilai asli.' : 'Simulasi selesai.'}</b> Update diproses ${ms} ms · <b>${nBeda}</b> keluaran berubah (ditandai ◀).
      <table style="margin-top:8px"><tr><th style="width:22%">Keluaran KB</th><th>Sebelum</th><th>Sesudah</th></tr>${baris}</table></div>`;
    setSource(kind === 'reset' ? 'saham-pellet' : 'saham');
  } catch (e) { setErr('whatif-out', e); }
  btns.forEach(b => b.disabled = false);
}

// =====================================================================================
// 100 PERTANYAAN → VISUAL OTOMATIS
// =====================================================================================
let QA_CUR = null;
const VIZ_NAMA = { kpi: 'angka kunci', gauge: 'gauge', bar: 'grafik batang', hbar: 'batang horizontal', donut: 'donat', scatter: 'peta sebaran', radar: 'radar', emiten: 'kartu emiten', chips: 'label', table: 'tabel' };
function renderQList() {
  const cari = ($('q-cari').value || '').toLowerCase();
  let html = '', kat = '';
  Q100.forEach((q, i) => {
    if (cari && !(q[1] + ' ' + q[0]).toLowerCase().includes(cari)) return;
    if (q[0] !== kat) { kat = q[0]; html += `<h5>${esc(kat)}</h5>`; }
    html += `<button class="qi ${QA_CUR === i ? 'on' : ''}" onclick="runQA(${i})"><span class="n">${i + 1}</span><span>${esc(q[1])}</span><span class="t">${VIZ_NAMA[q[2]] || ''}</span></button>`;
  });
  $('qlist').innerHTML = html || '<p class="muted small">Tidak ada pertanyaan yang cocok.</p>';
}
const isKode = v => typeof v === 'string' && /^[A-Z]{4}$/.test(v) && EMITEN_INFO[v];
const lbl = (row, col) => { const v = row[col]; return col === 'sektor' ? sek(v) : String(v ?? '').replace(/^(Persona|Tesis)( kontrarian)?: /, ''); };
function cellHTML(v) {
  if (typeof v === 'number') return `<span class="num">${fmt(v)}</span>`;
  if (isKode(v)) return ek(v, 22);
  if (typeof v === 'string' && /^Sektor /.test(v)) return esc(sek(v));
  if (typeof v === 'string' && /^https?:/.test(v)) return `<a href="${esc(v)}" target="_blank">tautan</a>`;
  return esc(String(v).replace(/^Sektor_/, ''));
}
function tableHTML(rows) {
  const cols = Object.keys(rows.reduce((a, b) => Object.assign(a, b), {}));
  return `<div class="tscroll"><table><thead><tr>${cols.map(c => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${cols.map(c => `<td>${r[c] === undefined ? '–' : cellHTML(r[c])}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}
async function runQA(i) {
  QA_CUR = i; renderQList();
  const [kat, tanya, viz, o, q] = Q100[i];
  $('qa-head').innerHTML = `<div class="qt">${i + 1}. ${esc(tanya)}</div><div class="qm"><span class="badge b-acc">${esc(kat)}</span><span class="badge b-neu">${VIZ_NAMA[viz]}</span><span class="small muted" id="qa-time"></span></div>`;
  showQ('q-qa', q);
  $('qa-viz').innerHTML = '<p class="loading">Menjalankan SPARQL ke Fuseki…</p>'; $('qa-data').innerHTML = '';
  const t0 = performance.now();
  try {
    const rows = await sparql(q);
    $('qa-time').textContent = `${rows.length} baris · ${Math.round(performance.now() - t0)} ms · /${SRC}`;
    $('qa-data').innerHTML = rows.length ? tableHTML(rows) : '';
    if (!rows.length) { $('qa-viz').innerHTML = '<p class="muted">Knowledge base tidak menemukan jawaban untuk kondisi data saat ini (hasil kosong). Coba sumber lain atau setelah simulasi what-if.</p>'; return; }
    renderViz(viz, o, rows);
  } catch (e) { setErr('qa-viz', e); }
}
function renderViz(viz, o, rows) {
  const el = $('qa-viz');
  const unit = o.unit ? ` ${o.unit}` : '';
  if (viz === 'kpi') {
    const r = rows[0];
    el.innerHTML = `<div class="kpi-big">${Object.keys(r).map(k => `<div><span>${esc(k.replace(/([a-z])([A-Z])/g, '$1 $2'))}</span><b>${typeof r[k] === 'number' ? fmt(r[k]) : esc(r[k])}</b></div>`).join('')}</div>`;
  } else if (viz === 'gauge') {
    const v = rows[0][o.value], mx = o.max || 100;
    el.innerHTML = `<div style="display:flex;justify-content:center"><div class="gauge-wrap" style="width:260px;height:260px"><canvas id="qa-c" width="260" height="260"></canvas><div class="gv" style="color:var(--m8)"><b style="font-size:58px">${fmt(v)}</b><span>dari ${mx}</span></div></div></div>`;
    chart('qa-c', { type: 'doughnut', data: { datasets: [{ data: [v, mx - v], backgroundColor: [C.m7, '#f6e3e5'], borderWidth: 0 }] }, options: { responsive: false, cutout: '76%', rotation: -120, circumference: 240, plugins: { legend: { display: false }, tooltip: { enabled: false } } } });
  } else if (viz === 'hbar') {
    const vals = rows.map(r => Number(r[o.value]) || 0), mx = Math.max(...vals.map(Math.abs), 1e-9), signed = o.signed || vals.some(v => v < 0);
    const zero = signed ? 50 : 0;
    el.innerHTML = rows.map((r, j) => { const v = vals[j], w = Math.abs(v) / mx * (signed ? 50 : 100), left = signed ? (v >= 0 ? 50 : 50 - w) : 0; const L = r[o.label];
      return `<div class="hb"><span class="lb">${isKode(L) ? ek(L, 22) : esc(lbl(r, o.label))}</span><span class="tr">${signed ? `<span class="z" style="left:${zero}%"></span>` : ''}<i class="${v < 0 ? 'neg' : ''}" style="left:${left}%;width:${Math.max(w, .6)}%"></i></span><span class="vv">${fmt(v)}${o.unit && o.unit.length < 4 ? o.unit : ''}</span></div>`; }).join('') + (o.unit && o.unit.length >= 4 ? `<p class="small muted">Satuan: ${esc(o.unit)}</p>` : '');
  } else if (viz === 'emiten') {
    const mx = Math.max(...rows.map(r => Math.abs(Number(r[o.value]) || 0)), 1e-9);
    el.innerHTML = `<div class="ecards">${rows.map(r => `<div class="pc" onclick="pilihEmiten('${r.kode}')"><div class="top">${logoEmiten(r.kode, 40)}<div><div class="kd">${esc(r.kode)}</div><div class="nmx">${esc((EMITEN_INFO[r.kode] || {}).nama || '')}</div></div></div>
      <div class="sc"><div><span class="small muted">${esc(o.unit || o.value)}</span><br><b style="font-size:22px">${fmt(r[o.value])}</b></div></div><div class="bar"><i style="width:${Math.abs(Number(r[o.value]) || 0) / mx * 100}%"></i></div></div>`).join('')}</div>`;
  } else if (viz === 'chips') {
    el.innerHTML = `<div class="chips" style="gap:8px">${rows.map(r => `<span class="badge b-acc" style="font-size:14px;padding:8px 14px">${esc(String(r[o.label]).replace(/([a-z])([A-Z])/g, '$1 $2'))}</span>`).join('')}</div>`;
  } else if (viz === 'table') {
    el.innerHTML = tableHTML(rows);
  } else {
    el.innerHTML = (viz === 'donut' ? '<div style="height:330px;position:relative"><canvas id="qa-c"></canvas></div>' : '<canvas id="qa-c" height="300"></canvas>') + (rows.some(r => isKode(r[o.label])) && viz === 'bar' ? `<div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:8px">${rows.map(r => ek(r[o.label], 20)).join('')}</div>` : '');
    const labels = rows.map(r => lbl(r, o.label));
    if (viz === 'bar') {
      const cols = o.values || [o.value];
      chart('qa-c', { type: 'bar', data: { labels, datasets: cols.map((c, j) => ({ label: c, data: rows.map(r => r[c]), backgroundColor: cols.length > 1 ? PAL[j * 2 % PAL.length] : rows.map((r, k) => k === 0 ? C.m7 : C.m4), borderRadius: 6 })) },
        options: { plugins: { legend: { display: cols.length > 1, position: 'bottom' }, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${fmt(c.raw)}${unit}` } } },
          scales: { x: { stacked: !!o.stacked, grid: { display: false } }, y: { stacked: !!o.stacked, grid: { color: '#f4e7e9' }, beginAtZero: true, max: o.max } } } });
    } else if (viz === 'donut') {
      chart('qa-c', { type: 'doughnut', data: { labels: labels.map(s => s.replace(/([a-z])([A-Z])/g, '$1 $2')), datasets: [{ data: rows.map(r => r[o.value]), backgroundColor: PAL, borderColor: '#fff', borderWidth: 3 }] },
        options: { cutout: '58%', maintainAspectRatio: false, plugins: { legend: { position: 'right' } } } });
    } else if (viz === 'radar') {
      chart('qa-c', { type: 'radar', data: { labels, datasets: [{ label: o.value, data: rows.map(r => r[o.value]), backgroundColor: 'rgba(200,32,45,.18)', borderColor: C.m6, pointBackgroundColor: C.m7 }] },
        options: { plugins: { legend: { display: false } }, scales: { r: { beginAtZero: true, grid: { color: '#f0dfe1' }, ticks: { backdropColor: 'transparent' } } } } });
    } else if (viz === 'scatter') {
      chart('qa-c', { type: 'scatter', data: { datasets: [{ label: o.label, data: rows.map(r => ({ x: r[o.x], y: r[o.y], k: lbl(r, o.label) })), backgroundColor: 'rgba(168,19,31,.6)', pointRadius: 6, pointHoverRadius: 8 }] },
        options: { plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.raw.k}: ${o.x} ${fmt(c.raw.x)}, ${o.y} ${fmt(c.raw.y)}` } } },
          scales: { x: { title: { display: true, text: o.x }, grid: { color: '#f4e7e9' } }, y: { title: { display: true, text: o.y }, grid: { color: '#f4e7e9' } } } },
        plugins: [pointLabels()] });
    }
  }
}

// =====================================================================================
// KONSOL SPARQL
// =====================================================================================
const CONTOH = [
  ['Sektor yang diprediksi naik', `SELECT ?sektor ?skor WHERE {\n  ?s a ex:SektorBullish ; rdfs:label ?sektor ; ex:skorOutlookAktif ?skor .\n} ORDER BY DESC(?skor)`],
  ['Top pick sistem pakar', `SELECT ?kode ?adaptif WHERE {\n  ?e a ex:KandidatTopPickAdaptif ; ex:kodeSaham ?kode ; ex:skorAdaptifRegime ?adaptif .\n} ORDER BY DESC(?adaptif)`],
  ['Semua fakta tentang ANTM', `SELECT ?properti ?nilai WHERE {\n  ex:ANTM ?properti ?nilai .\n} ORDER BY ?properti`],
  ['Anggota LQ45', `SELECT ?kode WHERE {\n  ?e ex:anggotaIndeks ex:LQ45 ; ex:kodeSaham ?kode .\n} ORDER BY ?kode`],
  ['Rumus & ambang PER', `SELECT ?rumus ?interpretasi ?ambang WHERE {\n  ex:PER ex:rumus ?rumus ; ex:interpretasi ?interpretasi ; ex:ambangBatas ?ambang .\n}`],
  ['Dampak The Fed', `SELECT ?peristiwa ?gerakan ?lanjutan WHERE {\n  ?peristiwa ex:memicuPergerakan ?gerakan .\n  FILTER(?peristiwa IN (ex:Ev_FedHike_Sep2026, ex:Ev_FOMC_Hawkish_2026))\n  OPTIONAL { ?gerakan ex:menyebabkan ?lanjutan }\n}`],
  ['Aturan SWRL per pilar', `SELECT ?pilar (COUNT(?r) AS ?aturan) WHERE {\n  ?r ex:kodeAturan ?kode ; ex:pilarAnalisis ?pilar .\n} GROUP BY ?pilar ORDER BY DESC(?aturan)`],
];
function initKonsol() { $('ex-sel').innerHTML = CONTOH.map((c, i) => `<option value="${i}">Contoh: ${c[0]}</option>`).join(''); loadExample(); }
function loadExample() { $('con-q').value = CONTOH[+$('ex-sel').value][1]; }
async function runConsole() {
  $('run-btn').disabled = true; $('con-out').innerHTML = '<p class="loading">Menjalankan…</p>';
  const t0 = performance.now();
  try {
    const r = await sparql($('con-q').value, $('con-ds').value);
    $('con-time').textContent = `${Array.isArray(r) ? r.length : 1} baris · ${Math.round(performance.now() - t0)} ms`;
    if (!Array.isArray(r)) $('con-out').innerHTML = `<p>ASK → <b>${r}</b></p>`;
    else if (!r.length) $('con-out').innerHTML = '<p class="muted">Query berhasil, tetapi tidak ada hasil.</p>';
    else $('con-out').innerHTML = `<div style="margin-top:10px">${tableHTML(r)}</div>`;
  } catch (e) { $('con-time').textContent = ''; setErr('con-out', e); }
  $('run-btn').disabled = false;
}

// navigasi aktif saat menggulir
const secs = [...document.querySelectorAll('main section')];
addEventListener('scroll', () => { const y = scrollY + 160; let cur = secs[0].id; secs.forEach(s => { if (s.offsetTop <= y) cur = s.id; });
  document.querySelectorAll('#nav a').forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + cur)); }, { passive: true });

initKonsol();
renderQList();
refreshAll().then(() => runQA(0));
