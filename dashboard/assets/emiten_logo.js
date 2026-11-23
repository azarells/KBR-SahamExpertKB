// =====================================================================================
// LOGO EMITEN
// Urutan pencarian logo untuk setiap kode saham:
//   1. file lokal  dashboard/logo/<KODE>.png   (paling bagus — unduh logo resmi, simpan dengan nama kode)
//   2. URL di kolom "logo" di bawah (boleh diisi/diganti sendiri, mis. link PNG dari situs resmi)
//   3. ikon situs resmi lewat layanan favicon Google (butuh internet)
//   4. lencana inisial berwarna (selalu tersedia, tanpa internet)
// =====================================================================================
const EMITEN_INFO = {
  AADI: { nama: 'Adaro Andalan Indonesia', web: 'adaro.com', logo: '' },
  PTBA: { nama: 'Bukit Asam', web: 'ptba.co.id', logo: '' },
  ITMG: { nama: 'Indo Tambangraya Megah', web: 'itmg.co.id', logo: '' },
  MEDC: { nama: 'Medco Energi Internasional', web: 'medcoenergi.com', logo: '' },
  PGAS: { nama: 'Perusahaan Gas Negara', web: 'pgn.co.id', logo: '' },
  AKRA: { nama: 'AKR Corporindo', web: 'akr.co.id', logo: '' },
  ANTM: { nama: 'Aneka Tambang', web: 'antam.com', logo: '' },
  MDKA: { nama: 'Merdeka Copper Gold', web: 'merdekacoppergold.com', logo: '' },
  INCO: { nama: 'Vale Indonesia', web: 'vale.com', logo: '' },
  NCKL: { nama: 'Trimegah Bangun Persada (Harita Nickel)', web: 'haritanickel.com', logo: '' },
  AMMN: { nama: 'Amman Mineral Internasional', web: 'amman.co.id', logo: '' },
  BRMS: { nama: 'Bumi Resources Minerals', web: 'bumiresourcesminerals.com', logo: '' },
  TINS: { nama: 'Timah', web: 'timah.com', logo: '' },
  INKP: { nama: 'Indah Kiat Pulp & Paper', web: 'asiapulppaper.com', logo: '' },
  SMGR: { nama: 'Semen Indonesia', web: 'sig.id', logo: '' },
  ASII: { nama: 'Astra International', web: 'astra.co.id', logo: '' },
  UNTR: { nama: 'United Tractors', web: 'unitedtractors.com', logo: '' },
  IMPC: { nama: 'Impack Pratama Industri', web: 'impack-pratama.com', logo: '' },
  ICBP: { nama: 'Indofood CBP Sukses Makmur', web: 'indofoodcbp.com', logo: '' },
  INDF: { nama: 'Indofood Sukses Makmur', web: 'indofood.com', logo: '' },
  MYOR: { nama: 'Mayora Indah', web: 'mayora.com', logo: '' },
  CPIN: { nama: 'Charoen Pokphand Indonesia', web: 'cp.co.id', logo: '' },
  JPFA: { nama: 'Japfa Comfeed Indonesia', web: 'japfacomfeed.co.id', logo: '' },
  AMRT: { nama: 'Sumber Alfaria Trijaya (Alfamart)', web: 'alfamart.co.id', logo: '' },
  AALI: { nama: 'Astra Agro Lestari', web: 'astra-agro.co.id', logo: '' },
  LSIP: { nama: 'PP London Sumatra Indonesia', web: 'londonsumatra.com', logo: '' },
  DSNG: { nama: 'Dharma Satya Nusantara', web: 'dsn.co.id', logo: '' },
  UNVR: { nama: 'Unilever Indonesia', web: 'unilever.co.id', logo: '' },
  MAPI: { nama: 'Mitra Adiperkasa', web: 'map.co.id', logo: '' },
  MAPA: { nama: 'MAP Aktif Adiperkasa', web: 'mapactive.id', logo: '' },
  ACES: { nama: 'Aspirasi Hidup Indonesia', web: 'azko.id', logo: '' },
  ERAA: { nama: 'Erajaya Swasembada', web: 'erajaya.com', logo: '' },
  AUTO: { nama: 'Astra Otoparts', web: 'astra-otoparts.com', logo: '' },
  KLBF: { nama: 'Kalbe Farma', web: 'kalbe.co.id', logo: '' },
  SIDO: { nama: 'Industri Jamu & Farmasi Sido Muncul', web: 'sidomuncul.co.id', logo: '' },
  MIKA: { nama: 'Mitra Keluarga Karyasehat', web: 'mitrakeluarga.com', logo: '' },
  HEAL: { nama: 'Medikaloka Hermina', web: 'herminahospitals.com', logo: '' },
  SILO: { nama: 'Siloam International Hospitals', web: 'siloamhospitals.com', logo: '' },
  BBCA: { nama: 'Bank Central Asia', web: 'bca.co.id', logo: '' },
  BBRI: { nama: 'Bank Rakyat Indonesia', web: 'bri.co.id', logo: '' },
  BMRI: { nama: 'Bank Mandiri', web: 'bankmandiri.co.id', logo: '' },
  BBNI: { nama: 'Bank Negara Indonesia', web: 'bni.co.id', logo: '' },
  BRIS: { nama: 'Bank Syariah Indonesia', web: 'bankbsi.co.id', logo: '' },
  BBTN: { nama: 'Bank Tabungan Negara', web: 'btn.co.id', logo: '' },
  CTRA: { nama: 'Ciputra Development', web: 'ciputra.com', logo: '' },
  BSDE: { nama: 'Bumi Serpong Damai (Sinar Mas Land)', web: 'sinarmasland.com', logo: '' },
  PWON: { nama: 'Pakuwon Jati', web: 'pakuwon.com', logo: '' },
  SMRA: { nama: 'Summarecon Agung', web: 'summarecon.com', logo: '' },
  DMAS: { nama: 'Puradelta Lestari (Kota Deltamas)', web: 'kotadeltamas.com', logo: '' },
  GOTO: { nama: 'GoTo Gojek Tokopedia', web: 'gotocompany.com', logo: '' },
  BUKA: { nama: 'Bukalapak.com', web: 'bukalapak.com', logo: '' },
  DCII: { nama: 'DCI Indonesia', web: 'dci-indonesia.com', logo: '' },
  MTDL: { nama: 'Metrodata Electronics', web: 'metrodata.co.id', logo: '' },
  EMTK: { nama: 'Elang Mahkota Teknologi', web: 'emtek.co.id', logo: '' },
  TLKM: { nama: 'Telkom Indonesia', web: 'telkom.co.id', logo: '' },
  ISAT: { nama: 'Indosat Ooredoo Hutchison', web: 'ioh.co.id', logo: '' },
  EXCL: { nama: 'XLSmart Telecom Sejahtera', web: 'xl.co.id', logo: '' },
  TOWR: { nama: 'Sarana Menara Nusantara (Protelindo)', web: 'protelindo.net', logo: '' },
  MTEL: { nama: 'Dayamitra Telekomunikasi (Mitratel)', web: 'mitratel.co.id', logo: '' },
  JSMR: { nama: 'Jasa Marga', web: 'jasamarga.co.id', logo: '' },
  BIRD: { nama: 'Blue Bird', web: 'bluebirdgroup.com', logo: '' },
  ASSA: { nama: 'Adi Sarana Armada', web: 'assa.id', logo: '' },
  SMDR: { nama: 'Samudera Indonesia', web: 'samudera.id', logo: '' },
  TMAS: { nama: 'Temas', web: 'temasline.com', logo: '' },
};
const LOGO_WARNA = ['#8b0d18', '#b3122a', '#d1495b', '#6d0a12', '#a3324a', '#c0392b', '#7a1f2b', '#9e2a2b'];

// Mengembalikan HTML <span class="logo"> yang otomatis mencoba sumber logo satu per satu.
function logoEmiten(kode, size = 28) {
  const info = EMITEN_INFO[kode] || {};
  const src = [`logo/${kode}.png`];
  if (info.logo) src.push(info.logo);
  if (info.web) src.push(`https://www.google.com/s2/favicons?domain=${info.web}&sz=128`);
  const warna = LOGO_WARNA[[...kode].reduce((a, c) => a + c.charCodeAt(0), 0) % LOGO_WARNA.length];
  return `<span class="logo" style="width:${size}px;height:${size}px;--lw:${warna};font-size:${Math.round(size * 0.34)}px" title="${info.nama || kode}">` +
    `<img alt="" data-src='${JSON.stringify(src.slice(1))}' src="${src[0]}" onerror="logoNext(this)" onload="logoOk(this)">` +
    `<b>${kode.slice(0, 2)}</b></span>`;
}
function logoOk(img) {
  // layanan favicon mengembalikan ikon bola dunia 16 px bila situs tidak punya ikon → anggap gagal
  if (img.naturalWidth <= 16 && /favicons/.test(img.src)) return logoNext(img);
  img.parentNode.classList.add('ok');
}
function logoNext(img) {
  const rest = JSON.parse(img.dataset.src || '[]');
  if (!rest.length) { img.remove(); return; }
  img.dataset.src = JSON.stringify(rest.slice(1));
  img.src = rest[0];
}
if (typeof module !== 'undefined') module.exports = { EMITEN_INFO };
