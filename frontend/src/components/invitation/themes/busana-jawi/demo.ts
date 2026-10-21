import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinanti", groom: "Raden",
    brideFull: "Kinanti Ayuning Tyas, S.Psi.", groomFull: "Raden Arya Bimantara, S.Ars.",
    brideParents: "Putri sulung dari\nBapak KRT. Hadi Pranoto & Ibu Siti Rahayu", groomParents: "Putra kedua dari\nBapak R. Soetomo Adi & Ibu Dwi Astuti",
    bridePhoto: "/themes/img/a47.webp", groomPhoto: "/themes/img/a48.webp",
    note: "Tresna iku ora mung tembung, nanging laku — cinta bukan sekadar kata, melainkan langkah bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-23T10:00:00+07:00",
  place: "Pendapi Ageng Taman Budaya",
  address: "Jl. Ir. Sutami No. 57, Jebres, Kota Surakarta",
  stories: [
    { date: "2020", title: "Pameran Batik", body: "Raden memotret, Kinanti menjelaskan filosofi parang kepada pengunjung. Satu percakapan, lalu banyak cerita." },
    { date: "2024", title: "Belajar Bersama", body: "Dari kelas membatik akhir pekan sampai merancang rumah impian di Solo." },
    { date: "2027", title: "Siraman & Dhaup", body: "Dengan restu kedua keluarga, kami melangkah dalam busana pusaka yang diwariskan Eyang." },
  ],
  events: [
    { name: "Siraman", date: "2027-10-22T09:00:00+07:00", time: "09.00 WIB", venue: "Ndalem Kediaman Mempelai Putri", address: "Jl. Kepatihan Wetan No. 12, Jebres, Kota Surakarta" },
    { name: "Ijab Kabul", date: "2027-10-23T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Surakarta", address: "Jl. Masjid Agung, Kauman, Pasar Kliwon, Kota Surakarta" },
    { name: "Dhaup & Resepsi", date: "2027-10-23T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Pendapi Ageng Taman Budaya", address: "Jl. Ir. Sutami No. 57, Jebres, Kota Surakarta" },
  ],
  gallery: ["/themes/img/a34.webp", "/themes/img/a46.webp", "/themes/img/a47.webp", "/themes/img/a48.webp", "/themes/img/a24.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0388 2211 90", account_name: "Kinanti Ayuning Tyas" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0815 4433 2211", account_name: "Raden Arya Bimantara" },
  ],
  guestName: "Ibu Rr. Sri Lestari",
  guestTable: "VIP 2",
  extras: {
    rundown: { items: [
      { time: "10.00", title: "Kirab pengantin", note: "Busana basahan & dodot" },
      { time: "10.30", title: "Upacara panggih" },
      { time: "11.15", title: "Resepsi", note: "Diiringi gamelan Kebo Giro & Ladrang Wilujeng" },
    ] },
    dressCode: { note: "Busana Jawa atau batik. Hitam, emas, dan sogan dipersilakan.", colors: ["#1d140e", "#c9a45a", "#6b4a2b", "#f4ead8"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-23T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. KRT. Hadi Pranoto", "Kel. Besar Bpk. R. Soetomo Adi"] },
  },
});
