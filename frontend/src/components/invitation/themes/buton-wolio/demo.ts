import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Haliza", groom: "Ihsan",
    brideFull: "Wa Ode Nurhaliza Sabila, S.E.", groomFull: "La Ode Muhammad Ihsan, S.Kom.",
    brideParents: "Putri sulung dari\nBapak La Ode Kamaluddin & Ibu Wa Ode Sitti Hasnah", groomParents: "Putra kedua dari\nBapak La Ode Abdul Rahim & Ibu Wa Ode Murni",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti batu-batu benteng Wolio yang disusun satu demi satu, kami ingin membangun rumah tangga yang kokoh, saling menopang dan menjaga.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-20T08:00:00+08:00",
  place: "Gedung Serbaguna Betoambari",
  address: "Jl. Betoambari No. 12, Lanto, Batupoaro, Kota Baubau",
  stories: [
    { date: "2018", title: "Senja di Pantai Kamali", body: "Kami bertemu saat menjadi panitia festival budaya. Sepulang rapat, obrolan berlanjut sambil menunggu matahari tenggelam di Kamali." },
    { date: "2022", title: "Pakande-kandea", body: "Haliza menyuapkan kasuami di tradisi makan bersama itu. Ihsan diam-diam berjanji akan melamarnya suatu hari." },
    { date: "2026", title: "Lamaran", body: "Keluarga Ihsan datang dengan adat yang lengkap. Dua keluarga besar bermufakat dan memilih hari baik di bulan November." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-11-20T08:00:00+08:00", time: "08.00 – 09.30 WITA", venue: "Masjid Agung Keraton Buton", address: "Kawasan Benteng Keraton Buton, Melai, Murhum, Kota Baubau" },
    { name: "Resepsi", date: "2027-11-20T11:00:00+08:00", time: "11.00 – 15.00 WITA", venue: "Gedung Serbaguna Betoambari", address: "Jl. Betoambari No. 12, Lanto, Batupoaro, Kota Baubau" },
  ],
  gallery: ["/themes/img/r105.webp", "/themes/img/r57.webp", "/themes/img/r101.webp", "/themes/img/r86.webp", "/themes/img/a124.webp", "/themes/img/r55.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7301 4455 20", account_name: "Wa Ode Nurhaliza Sabila" },
    { id: "demo-sultra", type: "bank", bank_name: "Bank Sultra", account_number: "0701 0200 3344 9", account_name: "La Ode Muhammad Ihsan" },
    { id: "demo-kado", type: "address", address: "Jl. Sultan Hasanuddin No. 7, Tomba, Wolio, Kota Baubau 93714" },
  ],
  guestName: "Bapak La Ode Ahmad Saleh & Keluarga",
  guestTable: "Meja Baluara 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan pengantin", note: "Diiringi tabuhan gendang dan tari linda" },
      { time: "11.45", title: "Kabanti & doa keluarga" },
      { time: "12.30", title: "Ramah tamah", note: "Kasuami, parende, dan kue cucuru" },
    ] },
    dressCode: { note: "Busana muslim atau sarung tenun Buton. Merah, kuning, dan hijau dipersilakan.", colors: ["#c8202a", "#f2c21b", "#178a4a", "#1c5a86"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-11-20T08:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar La Ode Kamaluddin (Wolio, Baubau)", "Kel. Besar La Ode Abdul Rahim (Pasarwajo, Buton)"] },
  },
});
