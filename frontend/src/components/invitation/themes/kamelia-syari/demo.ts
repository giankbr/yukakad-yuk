import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Azkia", groom: "Hilmi",
    brideFull: "Azkia Nur Rahmadhani, S.Pd.", groomFull: "Muhammad Hilmi Fadhlurrahman, S.T.",
    brideParents: "Putri pertama dari\nBapak H. Zainal Arifin & Ibu Hj. Siti Maryam",
    groomParents: "Putra kedua dari\nBapak Ahmad Syaukani & Ibu Nurul Aini",
    note: "Seperti kamelia yang mekar di musim yang tenang, semoga cinta kami tumbuh dalam ridha-Nya: rapi, teduh, dan tak lekang.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-03-20T08:00:00+07:00",
  place: "Gedung Kemuning Gading",
  address: "Jl. Pajajaran No. 18, Bantarjati, Kota Bogor",
  story: { title: "Ikhtiar Kami", body: "" },
  stories: [
    { date: "Syawal 1446 H", title: "Ta'aruf", body: "Dipertemukan lewat guru ngaji kami di Bogor. Pertemuan pertama ditemani keluarga, dengan teh hangat dan banyak doa." },
    { date: "Rabiul Awal 1447 H", title: "Khitbah", body: "Keluarga Hilmi datang bersilaturahmi ke rumah Azkia di Bantarjati untuk menyampaikan niat baik." },
    { date: "Ramadhan 1448 H", title: "Menuju Akad", body: "Dengan restu kedua orang tua, kami memantapkan hati untuk menyempurnakan separuh agama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-20T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Bantarjati, Kota Bogor" },
    { name: "Walimatul 'Ursy", date: "2027-03-20T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Kemuning Gading", address: "Jl. Pajajaran No. 18, Bantarjati, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7211 0456 89", account_name: "Azkia Nur Rahmadhani" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0953 3021 47", account_name: "Muhammad Hilmi Fadhlurrahman" },
    { id: "demo-kado", type: "address", address: "Jl. Kemuning Raya No. 7, Bantarjati, Kota Bogor 16153" },
  ],
  guestName: "Ibu Hj. Aminah & Keluarga",
  guestTable: "Meja Kamelia 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.30", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra dan putri terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim/muslimah yang longgar dan sopan, nuansa merah muda pudar, hijau tua, dan krem.", colors: ["#e3819b", "#f7e6e1", "#2d5c45", "#c99a45"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak H. Zainal Arifin", "Kel. Besar Bapak Ahmad Syaukani", "Majelis Taklim Al-Hikmah Bantarjati"] },
  },
});
