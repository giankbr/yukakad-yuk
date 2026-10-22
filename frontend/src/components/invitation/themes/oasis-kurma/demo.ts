import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nayla", groom: "Rafif",
    brideFull: "Nayla Syakira Ramadhani, S.Farm.", groomFull: "Rafif Hanif Alamsyah, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Dedi Supriadi & Ibu Hj. Euis Rohaeni",
    groomParents: "Putra kedua dari\nBapak H. Agus Setiawan Alamsyah & Ibu Hj. Ratna Komalasari",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti oasis yang menyejukkan di tengah perjalanan, semoga rumah tangga kami menjadi tempat berteduh yang penuh berkah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-03-27T08:30:00+07:00",
  place: "Masjid Raya Bandung",
  address: "Jl. Dalem Kaum No. 14, Balonggede, Regol, Kota Bandung",
  stories: [
    { date: "2022", title: "Satu Rombongan Umrah", body: "Kami berangkat bersama keluarga masing-masing, dan berkenalan saat berbagi kurma selepas Subuh." },
    { date: "2025", title: "Ta'aruf", body: "Dua keluarga dipertemukan kembali. Kami saling mengenal dengan sederhana dan mantap beristikharah." },
    { date: "Januari 2027", title: "Khitbah", body: "Rafif datang bersama orang tuanya ke Bandung, membawa doa dan sekeranjang kurma." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-27T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid Raya Bandung", address: "Jl. Dalem Kaum No. 14, Balonggede, Regol, Kota Bandung" },
    { name: "Walimah", date: "2027-03-27T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Rumah Teduh", address: "Jl. Raya Lembang No. 120, Gudangkahuripan, Lembang, Bandung Barat" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a64.webp", "/themes/img/a18.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7125 6630 18", account_name: "Nayla Syakira Ramadhani" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "085722190344", account_name: "Rafif Hanif Alamsyah" },
  ],
  guestName: "Bapak Ust. Hendra Gunawan & Keluarga",
  guestTable: "Meja Ajwa 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.30", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.30", title: "Doa & nasihat pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Jamuan di taman" },
      { time: "13.00", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim santun. Biru langit, pasir, dan hijau daun dipersilakan.", colors: ["#8fc3e6", "#f3e2c2", "#4f8241", "#d58a2c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-03-27T08:30:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dedi Supriadi", "Kel. Besar H. Agus Setiawan Alamsyah"] },
  },
});
