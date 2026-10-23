import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Fikri",
    brideFull: "Nadia Aulia Rahmah, S.Pd.", groomFull: "Fikri Maulana Hakim, S.Ds.",
    brideParents: "Putri pertama dari\nBapak H. Abdul Rozak & Ibu Hj. Siti Mualifah", groomParents: "Putra ketiga dari\nBapak H. Mashuri & Ibu Hj. Nur Hidayah",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti ukiran jati yang dipahat sedikit demi sedikit, semoga rumah tangga kami tumbuh indah dengan kesabaran dan ridha-Nya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-16T08:00:00+07:00",
  place: "Pendapa Griya Ukir Mulyoharjo",
  address: "Jl. Pemuda No. 27, Mulyoharjo, Jepara, Jawa Tengah",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2019", title: "Bengkel Ukir Mulyoharjo", body: "Fikri sedang merancang kursi ukir untuk pameran; Nadia datang mengantar murid-muridnya belajar mengenal ukiran Jepara." },
    { date: "2022", title: "Pahat Demi Pahat", body: "Kami belajar sabar seperti para pengukir: sedikit demi sedikit, tetapi tidak pernah berhenti." },
    { date: "2027", title: "Menuju Akad", body: "Dengan restu orang tua dan izin Allah, kami bersiap menyempurnakan separuh agama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Baitul Makmur", address: "Jl. Kartini, Kauman, Jepara, Jawa Tengah" },
    { name: "Walimatul 'Ursy", date: "2027-10-16T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendapa Griya Ukir Mulyoharjo", address: "Jl. Pemuda No. 27, Mulyoharjo, Jepara, Jawa Tengah" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r57.webp", "/themes/img/r58.webp", "/themes/img/a27.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7234 5612 09", account_name: "Nadia Aulia Rahmah" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0213 0100 4567 503", account_name: "Fikri Maulana Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Pemuda No. 27, Mulyoharjo, Jepara 59431" },
  ],
  guestName: "Bapak H. Sholikhin & Keluarga",
  guestTable: "Meja Jati 5",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Diiringi rebana dan shalawat" },
      { time: "11.30", title: "Kirab pengantin & doa bersama" },
      { time: "12.00", title: "Ramah tamah & santap siang" },
      { time: "13.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim atau batik. Nuansa cokelat jati, krem, dan emas tembaga dipersilakan.", colors: ["#7a3e16", "#c88a46", "#f2e4cc", "#3d1a07"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-16T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Rozak (Mulyoharjo)", "Kel. Besar H. Mashuri (Tahunan, Jepara)"] },
  },
});
