import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Naila", groom: "Hafiz",
    brideFull: "Naila Khairunnisa, S.Ars.", groomFull: "Hafiz Abdurrahman, M.T.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Fauzan & Ibu Hj. Siti Maryam", groomParents: "Putra pertama dari\nBapak Drs. Abdul Karim & Ibu Rahmawati",
    note: "Seperti dua belas sudut bintang yang bertemu di satu pusat, kami ingin melangkah ke arah yang sama.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung, Jawa Barat",
  stories: [
    { date: "2019", title: "Studio Ornamen", body: "Kami bertemu di kelas gambar ornamen geometri. Naila menggambar dengan jangka, Hafiz menghitung sudutnya. Bintang dua belas pertama kami selesai jam sebelas malam." },
    { date: "2024", title: "Proyek Masjid", body: "Bertahun kemudian kami bertemu lagi di proyek renovasi masjid di Garut: Naila merancang panel ubinnya, Hafiz menghitung strukturnya." },
    { date: "Januari 2027", title: "Khitbah", body: "Dengan restu kedua keluarga, Hafiz datang melamar. Pola yang dulu kami gambar bersama kini dibingkai di ruang tamu." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung, Jawa Barat" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Serbaguna Pusdai", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kec. Cibeunying Kaler, Kota Bandung, Jawa Barat" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7204 1188 63", account_name: "Naila Khairunnisa" },
    { id: "demo-muamalat", type: "bank", bank_name: "Bank Muamalat", account_number: "1430 0571 22", account_name: "Hafiz Abdurrahman" },
    { id: "demo-kado", type: "address", address: "Jl. Sukaluyu No. 18, Cihaurgeulis, Kec. Cibeunying Kaler, Kota Bandung 40122", account_name: "Keluarga H. Ahmad Fauzan" },
  ],
  guestName: "Bapak Ir. Yusuf Hidayat & Keluarga",
  guestTable: "Meja Rosette 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Iringan nasyid dan rebana" },
      { time: "11.30", title: "Tausiyah pernikahan", note: "Ustaz H. Mahmud Syarifuddin" },
      { time: "12.15", title: "Ramah tamah & santap siang" },
      { time: "13.30", title: "Doa bersama & foto keluarga" },
    ] },
    dressCode: { note: "Busana muslim rapi dengan nuansa ubin: gading, hijau toska, dan terakota.", colors: ["#efe5cf", "#1f6d6a", "#b4532e", "#d2a24c"] },
    guestPass: {},
    family: { names: ["Kel. Besar H. Ahmad Fauzan", "Kel. Besar Drs. Abdul Karim"] },
  },
});
