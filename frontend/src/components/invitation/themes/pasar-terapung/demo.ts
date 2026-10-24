import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Raudah", groom: "Rizani",
    brideFull: "Siti Raudhatul Jannah, S.Pd.", groomFull: "Muhammad Rizani Arsyad, S.T.",
    brideParents: "Putri ketiga dari\nBapak H. Abdul Gani & Ibu Hj. Norhayati", groomParents: "Putra sulung dari\nBapak H. Syahrani & Ibu Hj. Masliana",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Bertemu di antara jukung yang berdesakan, berlabuh di satu dermaga yang sama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T09:00:00+08:00",
  place: "Gedung Mahligai Pancasila",
  address: "Jl. Jenderal Sudirman No. 4, Antasan Besar, Banjarmasin Tengah, Kota Banjarmasin",
  stories: [
    { date: "2021", title: "Subuh di Lok Baintan", body: "Raudah menemani acilnya berjualan jeruk di atas jukung, Rizani datang memotret pasar terapung untuk tugas kuliah. Satu kantong jeruk jadi awal perkenalan." },
    { date: "2024", title: "Menyusuri Martapura", body: "Kami sering menghabiskan pagi di Siring Menara Pandang, berbagi wadai dan cerita tentang masa depan." },
    { date: "2027", title: "Badatang & Baantar Jujuran", body: "Dengan restu kedua keluarga, Rizani datang melamar secara adat. Kini kami menambatkan jukung kami pada satu tiang." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T09:00:00+08:00", time: "09.00 – 10.00 WITA", venue: "Masjid Raya Sabilal Muhtadin", address: "Jl. Jenderal Sudirman No. 1, Antasan Besar, Banjarmasin Tengah, Kota Banjarmasin" },
    { name: "Basanding (Resepsi)", date: "2027-09-18T11:00:00+08:00", time: "11.00 – 14.00 WITA", venue: "Gedung Mahligai Pancasila", address: "Jl. Jenderal Sudirman No. 4, Antasan Besar, Banjarmasin Tengah, Kota Banjarmasin" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a28.webp", "/themes/img/a29.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Kalsel", account_number: "0410 2245 7781", account_name: "Siti Raudhatul Jannah" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7193 5520 18", account_name: "Muhammad Rizani Arsyad" },
    { id: "demo-kado", type: "address", address: "Jl. Pramuka Komplek Semanda Indah No. 21, Pemurus Luar, Banjarmasin Timur 70238" },
  ],
  guestName: "Bapak H. Fahrurrazi & Keluarga",
  guestTable: "Jukung 7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin", note: "Diiringi sinoman hadrah" },
      { time: "11.30", title: "Basanding di pelaminan" },
      { time: "12.00", title: "Ramah tamah & makan bersama", note: "Soto Banjar dan wadai khas" },
      { time: "13.00", title: "Foto bersama keluarga & tamu" },
    ] },
    dressCode: { note: "Busana muslim atau kain sasirangan. Nuansa jingga, hijau sungai, dan krem.", colors: ["#d9772b", "#2f5a55", "#f6dcb8", "#8a2f3a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Gani (Martapura)", "Kel. Besar H. Syahrani (Kuin)", "Bubuhan Lok Baintan"] },
  },
});
