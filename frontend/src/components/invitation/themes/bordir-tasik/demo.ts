import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Fajar",
    brideFull: "Salma Nurul Aini, S.Pd.", groomFull: "Fajar Ramdani Saepuloh, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Ujang Sukmana & Ibu Hj. Euis Rohaeti",
    groomParents: "Putra kedua dari\nBapak Dadang Supriatna & Ibu Iis Nurjanah",
    bridePhoto: "/themes/img/r57.webp",
    groomPhoto: "/themes/img/r58.webp",
    note: "Seperti bordir kerancang yang dijahit setusuk demi setusuk, semoga ikatan kami tumbuh pelan, rapi, dan kuat.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Agung Kota Tasikmalaya",
  address: "Jl. Masjid Agung No. 1, Empangsari, Kec. Tawang, Kota Tasikmalaya",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2023", title: "Pameran Kerajinan Tasik", body: "Fajar datang meliput pameran bordir untuk tugas kantornya. Stan pertama yang ia singgahi adalah stan bordir milik keluarga Salma dari Kawalu." },
    { date: "2025", title: "Ta'aruf", body: "Lewat perantara guru mengaji keluarga, kami dipertemukan kembali dan saling mengenal dengan didampingi orang tua." },
    { date: "Januari 2027", title: "Khitbah", body: "Keluarga Fajar datang bersilaturahmi ke Kawalu, dan dengan izin Allah lamaran diterima dengan hangat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Kota Tasikmalaya", address: "Jl. Masjid Agung No. 1, Empangsari, Kec. Tawang, Kota Tasikmalaya" },
    { name: "Walimah", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Sukapura", address: "Jl. Mayor S.L. Tobing No. 34, Kahuripan, Kec. Tawang, Kota Tasikmalaya" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r75.webp", "/themes/img/r57.webp", "/themes/img/r58.webp"],
  gifts: [
    { id: "demo-bjbs", type: "bank", bank_name: "BJB Syariah", account_number: "5130 2027 0815", account_name: "Salma Nurul Aini" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7219 5506 41", account_name: "Fajar Ramdani Saepuloh" },
    { id: "demo-address", type: "address", address: "Kp. Cibeuti RT 02/05, Kel. Cibeuti, Kec. Kawalu, Kota Tasikmalaya 46182", account_name: "Keluarga H. Ujang Sukmana" },
  ],
  guestName: "Ibu Hj. Nenden Kurniasih & Keluarga",
  guestTable: "Meja Kerancang 4",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Sungkeman & nasihat pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra & putri terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim yang rapi. Nuansa putih, gading, atau hijau pupus dipersilakan, bordiran pun sangat cocok.", colors: ["#fbfaf4", "#e8ecd9", "#cfe0c3", "#7f9a74"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ujang Sukmana", "Kel. Besar Dadang Supriatna", "Paguyuban Pengrajin Bordir Kawalu"] },
  },
});
