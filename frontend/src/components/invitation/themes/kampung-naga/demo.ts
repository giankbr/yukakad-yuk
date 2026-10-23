import { makeDemo } from "../demo-base";

// Adat Sunda, Tasikmalaya: akad nikah di masjid agung, lalu resepsi bernuansa lembur (kampung) di jalan Garut–Tasik.
export const demo = makeDemo({
  couple: {
    bride: "Wulan", groom: "Dadan",
    brideFull: "Wulan Sari Rahayu, S.Hut.", groomFull: "Dadan Ramdani, S.Sos.",
    brideParents: "Putri kahiji ti\nBapak H. Ujang Sopandi & Ibu Hj. Iis Rosita", groomParents: "Putra kadua ti\nBapak Entis Sutisna & Ibu Imas Masitoh",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/a96.webp",
    note: "Sapertos imah di lembur: basajan, rapih, sareng silih jaga. Mugia rumah tangga kami kitu ogé.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T08:00:00+07:00",
  place: "Aula Saung Ciwulan",
  address: "Jl. Raya Garut–Tasikmalaya Km. 30, Neglasari, Salawu, Kab. Tasikmalaya",
  stories: [
    { date: "2021", title: "Tepang di Sengked", body: "Kami bertemu saat menuruni ratusan anak tangga batu menuju lembah, sama-sama ikut kegiatan kampus belajar kearifan kampung adat." },
    { date: "2024", title: "Neundeun Omong", body: "Keluarga Dadan datang bersilaturahmi ke Tasikmalaya, menitipkan niat baik untuk melamar." },
    { date: "2027", title: "Ijab Kabul", body: "Insyaallah kami mengikat janji suci, dengan restu sepuh dan keluarga besar." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-21T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Tasikmalaya", address: "Jl. Otto Iskandardinata, Empangsari, Tawang, Kota Tasikmalaya" },
    { name: "Resepsi", date: "2027-08-21T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Saung Ciwulan", address: "Jl. Raya Garut–Tasikmalaya Km. 30, Neglasari, Salawu, Kab. Tasikmalaya" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r1.webp", "/themes/img/r42.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BJB", account_number: "0098 1234 5670 1", account_name: "Wulan Sari Rahayu" },
    { id: "demo-kado", type: "address", address: "Kp. Babakan RT 02/05, Ds. Tanjungkarang, Kec. Cigalontang, Kab. Tasikmalaya 46463" },
  ],
  guestName: "Bapak Haji Endang & Kulawarga",
  guestTable: "Saung 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Mapag panganten", note: "Penyambutan diiringi kacapi suling" },
      { time: "11.30", title: "Saweran & huap lingkung" },
      { time: "12.00", title: "Ramah tamah, nasi liwet & pepes" },
      { time: "13.30", title: "Poto babarengan" },
    ] },
    dressCode: { note: "Busana sopan bernuansa alam: putih kapur, hijau sawah, dan cokelat ijuk.", colors: ["#f3efe4", "#7f9a4a", "#2e2622", "#8fb5b0"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ujang Sopandi (Cigalontang)", "Kel. Besar Entis Sutisna (Garut)"] },
    travel: { note: "Jalan menuju lokasi berkelok; berangkat lebih awal ya.", items: [
      { name: "Dari Kota Tasikmalaya", detail: "± 1 jam via Jl. Raya Garut–Tasikmalaya" },
      { name: "Dari Garut", detail: "± 45 menit, parkir luas di halaman aula" },
    ] },
  },
});
