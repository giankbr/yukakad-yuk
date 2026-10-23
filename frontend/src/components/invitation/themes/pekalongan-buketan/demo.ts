import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laila", groom: "Faris",
    brideFull: "Nur Laila Khasanah, S.Pd.", groomFull: "Muhammad Faris Alfarizi, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Abdul Rozak & Ibu Hj. Siti Maesaroh", groomParents: "Putra pertama dari\nBapak Ahmad Syarif & Ibu Nur Hidayah",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti buket di selembar kain, semoga rumah tangga kami selalu berbunga dan berwarna.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-14T09:00:00+07:00",
  place: "Pendapa Rumah Batik Kauman",
  address: "Jl. Hayam Wuruk No. 12, Kauman, Pekalongan Timur, Kota Pekalongan",
  stories: [
    { date: "2021", title: "Kelas Canting", body: "Kami bertemu di kelas membatik akhir pekan di Kampung Batik Kauman. Faris menumpahkan malam, Laila menolong membersihkannya." },
    { date: "2024", title: "Warna-warni Pesisir", body: "Setiap Sabtu kami berburu kain buketan lawas di Pasar Grosir Setono, sambil belajar mengenal keluarga masing-masing." },
    { date: "2026", title: "Khitbah", body: "Dengan restu kedua orang tua, Faris datang melamar membawa seserahan berbungkus kain buketan." },
    { date: "2027", title: "Akad di Kota Batik", body: "Insyaallah kami mengikat janji suci di Pekalongan, kota tempat kisah ini dimulai." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jami' Kauman", address: "Jl. Kauman, Kauman, Pekalongan Timur, Kota Pekalongan" },
    { name: "Resepsi", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendapa Rumah Batik Kauman", address: "Jl. Hayam Wuruk No. 12, Kauman, Pekalongan Timur, Kota Pekalongan" },
  ],
  gallery: ["/themes/img/a24.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a22.webp", "/themes/img/a25.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0071 0102 3456 507", account_name: "Nur Laila Khasanah" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7212 4455 90", account_name: "Muhammad Faris Alfarizi" },
    { id: "demo-kado", type: "address", address: "Jl. Kenanga No. 7, Klego, Pekalongan Timur, Kota Pekalongan 51124" },
  ],
  guestName: "Bapak H. Maskur & Keluarga",
  guestTable: "Meja Buketan 3",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin & sambutan keluarga" },
      { time: "11.30", title: "Doa bersama", note: "Dipimpin KH. Ahmad Zuhri" },
      { time: "12.00", title: "Ramah tamah & megono khas Pekalongan" },
    ] },
    dressCode: { note: "Batik pesisir warna-warni dipersilakan: merah muda, biru langit, hijau mint, dan kuning.", colors: ["#e97c9c", "#4f9ccb", "#5aa784", "#eda042"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Rozak", "Kel. Besar Ahmad Syarif"] },
  },
});
